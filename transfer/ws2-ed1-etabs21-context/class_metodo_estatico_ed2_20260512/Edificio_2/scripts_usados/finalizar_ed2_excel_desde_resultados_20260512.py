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
    _start_etabs_with_model_argument,
    check_etabs_dialogs_once,
    current_model_path,
    export_table_csv,
    get_etabs_processes,
)


STAMP = time.strftime("%Y%m%d_%H%M%S")
ED2_ROOT = CLASS_ROOT / "Edificio_2"
MODEL_DIR = ED2_ROOT / "models"
REPORTS_DIR = ED2_ROOT / "reports"
RESULTS_DIR = ED2_ROOT / "results"

MODEL = MODEL_DIR / "ED2_CLASE_METODO_ESTATICO_CORREGIDO_20260512_162839.EDB"
CORRECTION_SCRIPT = THIS.with_name("corregir_ed2_modelo_excel_20260512.py")

LOG = REPORTS_DIR / f"FINALIZAR_ED2_EXCEL_RESULTADOS_{STAMP}.log"
REPORT = REPORTS_DIR / f"FINALIZAR_ED2_EXCEL_RESULTADOS_{STAMP}.md"
JSON_REPORT = REPORTS_DIR / f"FINALIZAR_ED2_EXCEL_RESULTADOS_{STAMP}.json"


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


def fallback_modal_rows_from_log(log_path: Path, previous_participation_csv: Path) -> list[dict[str, float]]:
    periods = parse_periods_from_log(log_path)
    rows: list[dict[str, float]] = []
    lines = previous_participation_csv.read_text(encoding="utf-8").splitlines()
    header = lines[0].split(",")
    for idx, line in enumerate(lines[1 : len(periods) + 1]):
        values = line.split(",")
        row = dict(zip(header, values))
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


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    log = RunLog(LOG)
    data: dict[str, object] = {"stamp": STAMP, "model": str(MODEL)}
    etabs = None
    try:
        processes = get_etabs_processes()
        log.write(f"ETABS processes before final read: {processes}")
        if processes:
            raise RuntimeError("Hay una instancia ETABS abierta; no abro otra.")
        if not MODEL.exists():
            raise FileNotFoundError(MODEL)

        corr = load_correction_module()
        comtypes_client = _load_comtypes(log)
        helper = _create_helper(comtypes_client)
        etabs, sap, pid, attach_method = _start_etabs_with_model_argument(
            helper,
            str(MODEL),
            log,
            wait_after_start=25,
        )
        data["pid"] = pid
        data["attach_method"] = attach_method
        data["active_model"] = current_model_path(sap)
        check_etabs_dialogs_once(pid, log, "after_model_argument_open", dismiss=True, fail_on_events=True)

        corr.select_modal_output(sap, log)
        modal_source = "OAPI ModalParticipatingMassRatios"
        try:
            modal_rows = corr.get_modal_rows(sap)
        except Exception as exc:
            modal_source = f"LOG periods + previous participation pattern fallback: {exc!r}"
            modal_rows = fallback_modal_rows_from_log(
                MODEL.with_suffix(".LOG"),
                RESULTS_DIR / "modal_participating_mass_ratios_api_20260512_150626.csv",
            )
        story_rows = corr.parse_story_weights_from_out(MODEL.with_suffix(".OUT"))
        calc = corr.compute_static_values(story_rows, modal_rows)

        exports_dir = RESULTS_DIR / f"final_excel_resultados_{STAMP}"
        exports_dir.mkdir(parents=True, exist_ok=True)
        for table in [
            "Modal Periods And Frequencies",
            "Modal Participating Mass Ratios",
            "Mass Source Definition",
            "Mass Summary by Story",
        ]:
            export_table_csv(sap, table, exports_dir / f"{table.replace(' ', '_')}_{STAMP}.csv", log)

        modal_csv = RESULTS_DIR / f"modal_participating_mass_ratios_final_{STAMP}.csv"
        story_csv = RESULTS_DIR / f"story_weights_final_{STAMP}.csv"
        dist_csv = RESULTS_DIR / f"ed2_static_distribution_final_{STAMP}.csv"
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
                    "# Finalización Excel ED2 desde resultados corregidos",
                    "",
                    f"- Fecha: `{STAMP}`",
                    f"- Modelo leído: `{MODEL}`",
                    f"- Fuente modal: `{modal_source}`",
                    f"- Excel corregido: `{corr.CORRECTED_EXCEL}`",
                    f"- Copia en Descargas: `{corr.DOWNLOADS_EXCEL_COPY}`",
                    f"- Tx*: `{calc['tx_mode']['period']:.6f} s` modo `{calc['tx_mode']['mode']}`",
                    f"- Ty*: `{calc['ty_mode']['period']:.6f} s` modo `{calc['ty_mode']['mode']}`",
                    f"- Tz*: `{calc['tz_mode']['period']:.6f} s` modo `{calc['tz_mode']['mode']}`",
                    f"- Peso sísmico total: `{calc['p_total']:.3f} tonf`",
                    f"- Q0x: `{calc['qx']:.3f} tonf`",
                    f"- Q0y: `{calc['qy']:.3f} tonf`",
                    f"- sum(Fx)-Q0x: `{calc['sum_fx_error']:.6g}`",
                    f"- sum(Fy)-Q0y: `{calc['sum_fy_error']:.6g}`",
                    f"- CSV modal: `{modal_csv}`",
                    f"- CSV distribución: `{dist_csv}`",
                    f"- JSON técnico: `{JSON_REPORT}`",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        log.write(f"Final report written: {REPORT}")
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
                log.write("Closed ETABS after final read.")
            except Exception as exc:
                log.write(f"WARNING: could not close ETABS after final read: {exc!r}")
        log.close()


if __name__ == "__main__":
    raise SystemExit(main())
