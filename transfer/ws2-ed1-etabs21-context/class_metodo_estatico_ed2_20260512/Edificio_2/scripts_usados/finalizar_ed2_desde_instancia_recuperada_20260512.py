from __future__ import annotations

import importlib.util
import json
import re
import sys
import time
from pathlib import Path


THIS = Path(__file__).resolve()
CLASS_ROOT = THIS.parents[1]
HECRAS2 = CLASS_ROOT.parents[1]
PROG2 = HECRAS2 / "prog2"
COMMON = PROG2 / "_common"
sys.path.insert(0, str(COMMON))

from ws2_etabs_oapi import (  # noqa: E402
    ETABS_PROGID,
    RunLog,
    _create_helper,
    _load_comtypes,
    check_etabs_dialogs_once,
    current_model_path,
    export_table_csv,
    get_etabs_processes,
    normalize_path,
)


STAMP = time.strftime("%Y%m%d_%H%M%S")
ED2_ROOT = CLASS_ROOT / "Edificio_2"
MODEL_DIR = ED2_ROOT / "models"
REPORTS_DIR = ED2_ROOT / "reports"
RESULTS_DIR = ED2_ROOT / "results"

MODEL = MODEL_DIR / "ED2_CLASE_METODO_ESTATICO_CORREGIDO_20260512_162839.EDB"
CORRECTION_SCRIPT = THIS.with_name("corregir_ed2_modelo_excel_20260512.py")

LOG = REPORTS_DIR / f"FINALIZAR_ED2_INSTANCIA_RECUPERADA_{STAMP}.log"
REPORT = REPORTS_DIR / f"FINALIZAR_ED2_INSTANCIA_RECUPERADA_{STAMP}.md"
JSON_REPORT = REPORTS_DIR / f"FINALIZAR_ED2_INSTANCIA_RECUPERADA_{STAMP}.json"


def load_correction_module():
    spec = importlib.util.spec_from_file_location("ed2corr", CORRECTION_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {CORRECTION_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CORRECTED_MODEL = MODEL
    module.LOG = LOG
    module.REPORT = REPORT
    module.JSON_REPORT = JSON_REPORT
    return module


def parse_periods_from_log(path: Path) -> list[float]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    pairs = re.findall(r"Found mode\s+(\d+)\s+of\s+\d+:\s+.*?T=\s*([0-9.]+)", text)
    periods = [0.0] * len(pairs)
    for mode_s, period_s in pairs:
        periods[int(mode_s) - 1] = float(period_s)
    if not periods:
        raise RuntimeError(f"No se encontraron periodos modales en {path}")
    return periods


def fallback_modal_rows(corr) -> list[dict[str, float]]:
    periods = parse_periods_from_log(MODEL.with_suffix(".LOG"))
    previous = RESULTS_DIR / "modal_participating_mass_ratios_api_20260512_150626.csv"
    lines = previous.read_text(encoding="utf-8").splitlines()
    header = lines[0].split(",")
    rows: list[dict[str, float]] = []
    for idx, line in enumerate(lines[1 : len(periods) + 1]):
        row = dict(zip(header, line.split(",")))
        rows.append(
            {
                "mode": int(row["mode"]),
                "period": periods[idx],
                "UX": float(row["UX"]),
                "UY": float(row["UY"]),
                "RZ": float(row["RZ"]),
                "SumUX": float(row["SumUX"]),
                "SumUY": float(row["SumUY"]),
                "SumRZ": float(row["SumRZ"]),
            }
        )
    return rows


def attach_recovered_instance(log: RunLog):
    processes = get_etabs_processes()
    log.write(f"ETABS processes before recovered attach: {processes}")
    if len(processes) != 1:
        raise RuntimeError(f"Se esperaba exactamente una instancia ETABS; encontradas={len(processes)}")
    pid = int(processes[0]["Id"])
    title = str(processes[0].get("MainWindowTitle", ""))
    if MODEL.stem.lower() not in title.lower():
        raise RuntimeError(f"La instancia activa no corresponde al modelo esperado. Title={title}")

    for attempt in range(1, 4):
        events = check_etabs_dialogs_once(
            pid,
            log,
            f"recover_results_dialog_attempt_{attempt}",
            dismiss=True,
            fail_on_events=False,
        )
        if not events:
            break
        log.write(f"Dismissed {len(events)} ETABS dialog(s), waiting for model recovery.")
        time.sleep(4)

    comtypes_client = _load_comtypes(log)
    helper = _create_helper(comtypes_client)
    etabs = helper.GetObjectProcess(ETABS_PROGID, pid)
    sap = etabs.SapModel
    active = current_model_path(sap)
    log.write(f"Active model from OAPI: {active}")
    if active and normalize_path(active) != normalize_path(MODEL):
        raise RuntimeError(f"Modelo activo no coincide: {active}")
    return pid, etabs, sap


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    log = RunLog(LOG)
    data: dict[str, object] = {"stamp": STAMP, "model": str(MODEL)}
    etabs = None
    try:
        corr = load_correction_module()
        pid, etabs, sap = attach_recovered_instance(log)
        data["pid"] = pid
        version = sap.GetVersion()
        data["version"] = str(version[0] if isinstance(version, (tuple, list)) else version)

        corr.select_modal_output(sap, log)
        modal_source = "OAPI ModalParticipatingMassRatios"
        try:
            modal_rows = corr.get_modal_rows(sap)
        except Exception as exc:
            modal_source = f"LOG periods + participation fallback after OAPI failure: {exc!r}"
            modal_rows = fallback_modal_rows(corr)

        try:
            sap.File.Save(str(MODEL))
            log.write("Saved model after results recovery to set compatibility flag.")
        except Exception as exc:
            log.write(f"WARNING: save after recovery failed: {exc!r}")

        story_rows = corr.parse_story_weights_from_out(MODEL.with_suffix(".OUT"))
        calc = corr.compute_static_values(story_rows, modal_rows)

        exports_dir = RESULTS_DIR / f"instancia_recuperada_{STAMP}"
        exports_dir.mkdir(parents=True, exist_ok=True)
        for table in [
            "Modal Periods And Frequencies",
            "Modal Participating Mass Ratios",
            "Mass Source Definition",
            "Mass Summary by Story",
        ]:
            export_table_csv(sap, table, exports_dir / f"{table.replace(' ', '_')}_{STAMP}.csv", log)

        modal_csv = RESULTS_DIR / f"modal_participating_mass_ratios_instancia_recuperada_{STAMP}.csv"
        story_csv = RESULTS_DIR / f"story_weights_instancia_recuperada_{STAMP}.csv"
        dist_csv = RESULTS_DIR / f"ed2_static_distribution_instancia_recuperada_{STAMP}.csv"
        corr.write_csv(modal_csv, modal_rows)
        corr.write_csv(story_csv, story_rows)
        corr.write_csv(dist_csv, calc["dist"])
        corr.patch_excel_template(story_rows, modal_rows, calc)

        data.update(
            {
                "modal_source": modal_source,
                "modal_rows": modal_rows,
                "story_rows": story_rows,
                "calc": calc,
                "modal_csv": str(modal_csv),
                "story_csv": str(story_csv),
                "dist_csv": str(dist_csv),
                "exports_dir": str(exports_dir),
                "corrected_excel": str(corr.CORRECTED_EXCEL),
                "downloads_excel_copy": str(corr.DOWNLOADS_EXCEL_COPY),
                "et_export_verification": corr.verify_et_export(MODEL.with_suffix(".$et")),
            }
        )
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        REPORT.write_text(
            "\n".join(
                [
                    "# Finalización ED2 desde instancia recuperada",
                    "",
                    f"- Fecha: `{STAMP}`",
                    f"- Modelo corregido: `{MODEL}`",
                    f"- Fuente modal: `{modal_source}`",
                    f"- Excel corregido: `{corr.CORRECTED_EXCEL}`",
                    f"- Copia en Descargas: `{corr.DOWNLOADS_EXCEL_COPY}`",
                    f"- Tx*: `{calc['tx_mode']['period']:.6f} s` modo `{calc['tx_mode']['mode']}`",
                    f"- Ty*: `{calc['ty_mode']['period']:.6f} s` modo `{calc['ty_mode']['mode']}`",
                    f"- Tz*: `{calc['tz_mode']['period']:.6f} s` modo `{calc['tz_mode']['mode']}`",
                    f"- Peso sísmico total: `{calc['p_total']:.3f} tonf`",
                    f"- Q0x: `{calc['qx']:.3f} tonf`; Q0y: `{calc['qy']:.3f} tonf`",
                    f"- sum(Fx)-Q0x: `{calc['sum_fx_error']:.6g}`",
                    f"- sum(Fy)-Q0y: `{calc['sum_fy_error']:.6g}`",
                    f"- CSV modal: `{modal_csv}`",
                    f"- CSV pesos: `{story_csv}`",
                    f"- CSV distribución: `{dist_csv}`",
                    f"- JSON técnico: `{JSON_REPORT}`",
                    "",
                    "Se seleccionó la recuperación de resultados existente y se guardó el modelo.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        log.write(f"Final recovered report written: {REPORT}")
        return 0
    except Exception as exc:
        data["error"] = repr(exc)
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        log.write(f"ERROR: {exc!r}")
        return 1
    finally:
        if etabs is not None:
            try:
                etabs.ApplicationExit(False)
                log.write("Closed ETABS after recovered extraction.")
            except Exception as exc:
                log.write(f"WARNING: could not close ETABS after recovered extraction: {exc!r}")
        log.close()


if __name__ == "__main__":
    raise SystemExit(main())
