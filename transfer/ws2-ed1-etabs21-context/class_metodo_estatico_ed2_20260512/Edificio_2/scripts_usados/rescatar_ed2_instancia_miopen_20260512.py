from __future__ import annotations

import importlib.util
import json
import os
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
    check_ret,
    current_model_path,
    export_table_csv,
    get_etabs_processes,
    guarded_run_analysis,
    normalize_path,
)


STAMP = time.strftime("%Y%m%d_%H%M%S")
ED2_ROOT = CLASS_ROOT / "Edificio_2"
MODEL_DIR = ED2_ROOT / "models"
REPORTS_DIR = ED2_ROOT / "reports"
RESULTS_DIR = ED2_ROOT / "results"

ACTIVE_MODEL = MODEL_DIR / "ED2_CLASE_METODO_ESTATICO_CORREGIDO_20260512_162839.EDB"
CORRECTION_SCRIPT = THIS.with_name("corregir_ed2_modelo_excel_20260512.py")

LOG = REPORTS_DIR / f"RESCATE_ED2_MIOPEN_{STAMP}.log"
REPORT = REPORTS_DIR / f"RESCATE_ED2_MIOPEN_{STAMP}.md"
JSON_REPORT = REPORTS_DIR / f"RESCATE_ED2_MIOPEN_{STAMP}.json"


def load_correction_module():
    spec = importlib.util.spec_from_file_location("ed2corr", CORRECTION_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {CORRECTION_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CORRECTED_MODEL = ACTIVE_MODEL
    module.LOG = LOG
    module.REPORT = REPORT
    module.JSON_REPORT = JSON_REPORT
    return module


def attach_active_etabs(log: RunLog):
    processes = get_etabs_processes()
    log.write(f"ETABS processes before rescue: {processes}")
    if len(processes) != 1:
        raise RuntimeError(f"El rescate exige exactamente una instancia ETABS; encontradas={len(processes)}")
    pid = int(processes[0]["Id"])
    title = str(processes[0].get("MainWindowTitle", ""))
    if ACTIVE_MODEL.stem.lower() not in title.lower():
        raise RuntimeError(f"La instancia activa no parece contener el modelo esperado. Title={title}")

    comtypes_client = _load_comtypes(log)
    helper = _create_helper(comtypes_client)
    etabs = helper.GetObjectProcess(ETABS_PROGID, pid)
    sap = etabs.SapModel
    check_etabs_dialogs_once(pid, log, "rescue_precheck", dismiss=True, fail_on_events=False)
    active = current_model_path(sap)
    log.write(f"Active model path from OAPI: {active}")
    if active and normalize_path(active) != normalize_path(ACTIVE_MODEL):
        raise RuntimeError(f"Modelo activo no coincide. active={active}; expected={ACTIVE_MODEL}")
    return pid, etabs, sap


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    log = RunLog(LOG)
    data: dict[str, object] = {"stamp": STAMP, "active_model": str(ACTIVE_MODEL)}
    etabs = None
    try:
        corr = load_correction_module()
        pid, etabs, sap = attach_active_etabs(log)
        data["pid"] = pid
        data["version"] = str(sap.GetVersion()[0] if isinstance(sap.GetVersion(), (tuple, list)) else sap.GetVersion())

        data["frame_offset_edit"] = corr.correct_frame_offsets(sap, log)
        data["mass_source_edit"] = corr.correct_mass_source(sap, log)
        corr.set_run_modal_only(sap, log)
        check_ret(sap.File.Save(str(ACTIVE_MODEL)), f"File.Save({ACTIVE_MODEL}) pre-run")

        ret = guarded_run_analysis(sap, log, pid=pid, context="ED2 rescue corrected modal run")
        check_ret(ret, "Analyze.RunAnalysis rescue corrected")

        corr.select_modal_output(sap, log)
        modal_rows = corr.get_modal_rows(sap)
        check_ret(sap.File.Save(str(ACTIVE_MODEL)), f"File.Save({ACTIVE_MODEL}) post-run")

        exports_dir = RESULTS_DIR / f"rescate_miopen_corregido_{STAMP}"
        exports_dir.mkdir(parents=True, exist_ok=True)
        for table in [
            "Modal Periods And Frequencies",
            "Modal Participating Mass Ratios",
            "Mass Source Definition",
            "Mass Summary by Story",
            "Base Reactions",
        ]:
            export_table_csv(sap, table, exports_dir / f"{table.replace(' ', '_')}_{STAMP}.csv", log)

        story_rows = corr.parse_story_weights_from_out(ACTIVE_MODEL.with_suffix(".OUT"))
        calc = corr.compute_static_values(story_rows, modal_rows)

        modal_csv = RESULTS_DIR / f"modal_participating_mass_ratios_rescate_{STAMP}.csv"
        story_csv = RESULTS_DIR / f"story_weights_rescate_{STAMP}.csv"
        dist_csv = RESULTS_DIR / f"ed2_static_distribution_rescate_{STAMP}.csv"
        corr.write_csv(modal_csv, modal_rows)
        corr.write_csv(story_csv, story_rows)
        corr.write_csv(dist_csv, calc["dist"])

        corr.patch_excel_template(story_rows, modal_rows, calc)
        data.update(
            {
                "corrected_model": str(ACTIVE_MODEL),
                "corrected_excel": str(corr.CORRECTED_EXCEL),
                "downloads_excel_copy": str(corr.DOWNLOADS_EXCEL_COPY),
                "story_rows": story_rows,
                "modal_rows": modal_rows,
                "calc": calc,
                "modal_csv": str(modal_csv),
                "story_csv": str(story_csv),
                "dist_csv": str(dist_csv),
                "exports_dir": str(exports_dir),
                "et_export_verification": corr.verify_et_export(ACTIVE_MODEL.with_suffix(".$et")),
            }
        )
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        corr.write_report(data)

        REPORT.write_text(
            "\n".join(
                [
                    "# Rescate instancia ETABS por miOpen",
                    "",
                    f"- Fecha: `{STAMP}`",
                    f"- PID recuperado: `{pid}`",
                    f"- Modelo activo corregido: `{ACTIVE_MODEL}`",
                    f"- Excel actualizado: `{corr.CORRECTED_EXCEL}`",
                    f"- Copia en Descargas: `{corr.DOWNLOADS_EXCEL_COPY}`",
                    f"- Tx*: `{calc['tx_mode']['period']:.6f} s` modo `{calc['tx_mode']['mode']}`",
                    f"- Ty*: `{calc['ty_mode']['period']:.6f} s` modo `{calc['ty_mode']['mode']}`",
                    f"- Tz*: `{calc['tz_mode']['period']:.6f} s` modo `{calc['tz_mode']['mode']}`",
                    f"- Peso sísmico total: `{calc['p_total']:.3f} tonf`",
                    f"- Q0x: `{calc['qx']:.3f} tonf`; Q0y: `{calc['qy']:.3f} tonf`",
                    f"- sum(Fx)-Q0x: `{calc['sum_fx_error']:.6g}`",
                    f"- sum(Fy)-Q0y: `{calc['sum_fy_error']:.6g}`",
                    "",
                    "La sesión se enganchó al PID existente; no se abrió una segunda instancia.",
                    "Se cerró ETABS al terminar para dejar el equipo limpio después de la anormalidad.",
                    f"JSON técnico: `{JSON_REPORT}`",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        log.write(f"Rescue report written: {REPORT}")
        return 0
    except Exception as exc:
        data["error"] = repr(exc)
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        log.write(f"ERROR: {exc!r}")
        return 1
    finally:
        if etabs is not None:
            try:
                etabs.ApplicationExit(True)
                log.write("Closed rescued ETABS instance after save.")
            except Exception as exc:
                log.write(f"WARNING: could not close rescued ETABS instance: {exc!r}")
        log.close()


if __name__ == "__main__":
    raise SystemExit(main())
