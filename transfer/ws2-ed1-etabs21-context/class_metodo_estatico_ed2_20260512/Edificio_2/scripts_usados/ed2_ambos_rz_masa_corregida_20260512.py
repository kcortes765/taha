from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any


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
    check_ret,
    current_model_path,
    export_table_csv,
    get_etabs_processes,
    get_frame_property,
    get_name_list,
    guarded_run_analysis,
    unlock_model,
)


STAMP = time.strftime("%Y%m%d_%H%M%S")
ED2_ROOT = CLASS_ROOT / "Edificio_2"
MODEL_DIR = ED2_ROOT / "models"
EXCEL_DIR = ED2_ROOT / "excel"
RESULTS_DIR = ED2_ROOT / "results"
REPORTS_DIR = ED2_ROOT / "reports"
BACKUP_DIR = ED2_ROOT / "backups"

BASE_MODEL = MODEL_DIR / "ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.EDB"
MODEL = MODEL_DIR / f"ED2_CLASE_METODO_ESTATICO_AMBOS_RZ_MASA_CORREGIDA_{STAMP}.EDB"
CORRECTION_SCRIPT = THIS.with_name("corregir_ed2_modelo_excel_20260512.py")

EXCEL = EXCEL_DIR / "ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_20260512.xlsx"
DOWNLOADS_EXCEL_COPY = Path(r"C:\Users\Civil\Downloads\ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_WS2_20260512.xlsx")

LOG = REPORTS_DIR / f"ED2_AMBOS_RZ_MASA_CORREGIDA_{STAMP}.log"
REPORT = REPORTS_DIR / f"ED2_AMBOS_RZ_MASA_CORREGIDA_{STAMP}.md"
JSON_REPORT = REPORTS_DIR / f"ED2_AMBOS_RZ_MASA_CORREGIDA_{STAMP}.json"

BEAM_SECTIONS = {"V50x70G25", "V45x70G25"}
COLUMN_SECTIONS = {"C70x70G25", "C65x65G25"}


def load_correction_module():
    spec = importlib.util.spec_from_file_location("ed2corr", CORRECTION_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {CORRECTION_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CORRECTED_MODEL = MODEL
    module.CORRECTED_EXCEL = EXCEL
    module.DOWNLOADS_EXCEL_COPY = DOWNLOADS_EXCEL_COPY
    module.REPORT = REPORT
    module.JSON_REPORT = JSON_REPORT
    return module


def ensure_dirs() -> None:
    for path in [MODEL_DIR, EXCEL_DIR, RESULTS_DIR, REPORTS_DIR, BACKUP_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def timestamped_backup(path: Path, tag: str) -> str | None:
    if not path.exists():
        return None
    out = BACKUP_DIR / f"{path.stem}_BACKUP_{tag}_{STAMP}{path.suffix}"
    shutil.copy2(path, out)
    return str(out)


def set_rz_both_beams_columns(sap: Any, log: RunLog) -> dict[str, Any]:
    unlock_model(sap)
    frames = get_name_list(sap.FrameObj)
    data = {
        "total_frames": len(frames),
        "beams_rz_075": 0,
        "columns_rz_075": 0,
        "other_skipped": 0,
        "failed": [],
    }
    for frame in frames:
        try:
            section = get_frame_property(sap, frame)
        except Exception as exc:
            data["failed"].append({"frame": frame, "error": f"GetSection {exc!r}"})
            continue
        if section not in BEAM_SECTIONS and section not in COLUMN_SECTIONS:
            data["other_skipped"] += 1
            continue
        try:
            ret = sap.FrameObj.SetEndLengthOffset(frame, True, 0.0, 0.0, 0.75, 0)
        except TypeError:
            ret = sap.FrameObj.SetEndLengthOffset(frame, True, 0.0, 0.0, 0.75)
        if check_ret(ret, f"SetEndLengthOffset both RZ {frame}", soft=True):
            if section in BEAM_SECTIONS:
                data["beams_rz_075"] += 1
            else:
                data["columns_rz_075"] += 1
        else:
            data["failed"].append({"frame": frame, "section": section, "ret": repr(ret)})
    log.write(
        "Rigid end zones both: "
        f"beams={data['beams_rz_075']}, columns={data['columns_rz_075']}, "
        f"failed={len(data['failed'])}"
    )
    return data


def main() -> int:
    ensure_dirs()
    log = RunLog(LOG)
    data: dict[str, Any] = {"stamp": STAMP}
    etabs = None
    try:
        processes = get_etabs_processes()
        log.write(f"ETABS processes before both-RZ run: {processes}")
        if processes:
            raise RuntimeError("Hay una instancia ETABS abierta; no abro otra.")
        if not BASE_MODEL.exists():
            raise FileNotFoundError(BASE_MODEL)
        data["base_model"] = str(BASE_MODEL)
        data["base_backup"] = timestamped_backup(BASE_MODEL, "ANTES_AMBOS_RZ_MASA")
        shutil.copy2(BASE_MODEL, MODEL)
        log.write(f"Working model copied: {MODEL}")

        corr = load_correction_module()
        comtypes_client = _load_comtypes(log)
        helper = _create_helper(comtypes_client)
        etabs, sap, pid, attach_method = _start_etabs_with_model_argument(
            helper,
            str(MODEL),
            log,
            wait_after_start=25,
        )
        data["etabs"] = {"pid": pid, "attach_method": attach_method, "active_model": current_model_path(sap)}

        data["frame_offset_edit"] = set_rz_both_beams_columns(sap, log)
        data["mass_source_edit"] = corr.correct_mass_source(sap, log)
        corr.set_run_modal_only(sap, log)
        check_ret(sap.File.Save(str(MODEL)), f"File.Save({MODEL}) pre-run")

        ret = guarded_run_analysis(sap, log, pid=pid, context="ED2 both RZ corrected mass modal run")
        if not check_ret(ret, "Analyze.RunAnalysis both RZ corrected mass", soft=True):
            log.write(f"Analyze.RunAnalysis returned nonzero ret={ret}; checking modal results anyway.")

        corr.select_modal_output(sap, log)
        modal_rows = corr.get_modal_rows(sap)
        check_ret(sap.File.Save(str(MODEL)), f"File.Save({MODEL}) post-run")

        exports_dir = RESULTS_DIR / f"ambos_rz_masa_corregida_{STAMP}"
        exports_dir.mkdir(parents=True, exist_ok=True)
        for table in [
            "Modal Periods And Frequencies",
            "Modal Participating Mass Ratios",
            "Mass Source Definition",
            "Mass Summary by Story",
        ]:
            export_table_csv(sap, table, exports_dir / f"{table.replace(' ', '_')}_{STAMP}.csv", log)

        story_rows = corr.parse_story_weights_from_out(MODEL.with_suffix(".OUT"))
        calc = corr.compute_static_values(story_rows, modal_rows)
        modal_csv = RESULTS_DIR / f"modal_participating_mass_ratios_ambos_rz_masa_corregida_{STAMP}.csv"
        story_csv = RESULTS_DIR / f"story_weights_ambos_rz_masa_corregida_{STAMP}.csv"
        dist_csv = RESULTS_DIR / f"ed2_static_distribution_ambos_rz_masa_corregida_{STAMP}.csv"
        corr.write_csv(modal_csv, modal_rows)
        corr.write_csv(story_csv, story_rows)
        corr.write_csv(dist_csv, calc["dist"])
        corr.patch_excel_template(story_rows, modal_rows, calc)

        data.update(
            {
                "model": str(MODEL),
                "excel": str(EXCEL),
                "downloads_excel_copy": str(DOWNLOADS_EXCEL_COPY),
                "modal_rows": modal_rows,
                "story_rows": story_rows,
                "calc": calc,
                "modal_csv": str(modal_csv),
                "story_csv": str(story_csv),
                "dist_csv": str(dist_csv),
                "exports_dir": str(exports_dir),
                "et_export_verification": corr.verify_et_export(MODEL.with_suffix(".$et")),
            }
        )
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        REPORT.write_text(
            "\n".join(
                [
                    "# ED2 ambos cachos rígidos + masa corregida",
                    "",
                    f"- Fecha: `{STAMP}`",
                    f"- Modelo base: `{BASE_MODEL}`",
                    f"- Modelo generado: `{MODEL}`",
                    f"- Excel generado: `{EXCEL}`",
                    f"- Copia en Descargas: `{DOWNLOADS_EXCEL_COPY}`",
                    "",
                    "## Criterio",
                    "",
                    "- Se mantiene lo indicado por enunciado: cachos rígidos automáticos `0.75` en vigas y columnas.",
                    "- Se corrige solo la masa sísmica según clase: `PP + TERP + TERT + 0.25*SCP + 0*SCT`.",
                    "",
                    "## Resultados",
                    "",
                    f"- `Tx* = {calc['tx_mode']['period']:.6f} s` modo `{calc['tx_mode']['mode']}`.",
                    f"- `Ty* = {calc['ty_mode']['period']:.6f} s` modo `{calc['ty_mode']['mode']}`.",
                    f"- `Tz* = {calc['tz_mode']['period']:.6f} s` modo `{calc['tz_mode']['mode']}`.",
                    f"- `P = {calc['p_total']:.3f} tonf`.",
                    f"- `Q0x = {calc['qx']:.3f} tonf`, `Q0y = {calc['qy']:.3f} tonf`.",
                    f"- `sum(Fx)-Q0x = {calc['sum_fx_error']:.6g}`.",
                    f"- `sum(Fy)-Q0y = {calc['sum_fy_error']:.6g}`.",
                    "",
                    "## Evidencia",
                    "",
                    f"- CSV modal: `{modal_csv}`",
                    f"- CSV distribución: `{dist_csv}`",
                    f"- JSON técnico: `{JSON_REPORT}`",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        log.write(f"Report written: {REPORT}")
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
                log.write("Closed ETABS after both-RZ run.")
            except Exception as exc:
                log.write(f"WARNING: could not close ETABS after both-RZ run: {exc!r}")
        log.close()


if __name__ == "__main__":
    raise SystemExit(main())
