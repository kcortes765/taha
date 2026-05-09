"""
11_run_analysis_ed2.py - Ejecuta el analisis oficial Ed.2 Parte 1.

Objetivo:
- correr gravedad + modal + EX/EY/TEX/TEY
- guardar el modelo
- dejar una pre-validacion minima antes de la extraccion formal
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    DEFAULT_MODEL_FILENAME,
    MODELS_DIR,
    UNITS_TONF_M_C,
    check_ret,
    connect,
    disconnect,
    get_runtime_etabs_info,
    log,
    set_units,
)
from ed2_static_official import (
    GRAVITY_CASES,
    OFFICIAL_CASES,
    extract_base_reaction_case,
    write_json,
)


def ensure_model_path(SapModel) -> str:
    try:
        filepath = SapModel.GetModelFilename()
        if isinstance(filepath, (tuple, list)):
            filepath = filepath[0]
        filepath = str(filepath or "").strip()
    except Exception:
        filepath = ""

    if filepath and filepath.upper() != "UNSAVED":
        return filepath

    os.makedirs(MODELS_DIR, exist_ok=True)
    filepath = os.path.join(MODELS_DIR, DEFAULT_MODEL_FILENAME)
    ret = SapModel.File.Save(filepath)
    check_ret(ret, f"File.Save('{filepath}')")
    return filepath


def set_run_flags(SapModel) -> None:
    cases = GRAVITY_CASES + OFFICIAL_CASES
    try:
        SapModel.Analyze.SetRunCaseFlag("", False, True)
    except Exception:
        pass
    for case_name in cases:
        try:
            SapModel.Analyze.SetRunCaseFlag(case_name, True, False)
        except Exception:
            continue


def normalize_ret_code(ret) -> int:
    if isinstance(ret, (tuple, list)):
        if len(ret) > 1:
            return int(ret[-1])
        if ret:
            return int(ret[0])
    return int(ret)


def main() -> int:
    SapModel = None
    try:
        log.info("=" * 72)
        log.info("ED2 PARTE 1 - ANALISIS OFICIAL")
        log.info("=" * 72)
        SapModel = connect()
        set_units(SapModel, UNITS_TONF_M_C)
        try:
            SapModel.SetModelIsLocked(False)
        except Exception:
            pass

        filepath = ensure_model_path(SapModel)
        log.info(f"Model file: {filepath}")

        log.info("Step 1: Saving model before analysis...")
        ret = SapModel.File.Save(filepath)
        check_ret(ret, f"File.Save('{filepath}')")

        log.info("Step 2: Enabling official analysis cases...")
        set_run_flags(SapModel)

        log.info("Step 3: Running full official analysis...")
        ret = SapModel.Analyze.RunAnalysis()
        ret_code = normalize_ret_code(ret)
        check_ret(ret, "Analyze.RunAnalysis")
        time.sleep(1)

        snapshot = {
            "model_file": filepath,
            "analysis_return_code": ret_code,
            "etabs_runtime": get_runtime_etabs_info(),
            "cases": {},
        }
        log.info("Step 4: Reading base reactions...")
        for case_name in ["PP", "TERP", "TERT", "SCP", "SCT", "EX", "EY", "TEX", "TEY"]:
            snapshot["cases"][case_name] = extract_base_reaction_case(SapModel, case_name)

        write_json("ed2_analysis_run.json", snapshot)

        ex_info = snapshot["cases"].get("EX") or {}
        ey_info = snapshot["cases"].get("EY") or {}
        tex_info = snapshot["cases"].get("TEX") or {}
        tey_info = snapshot["cases"].get("TEY") or {}
        if float(ex_info.get("fx", 0.0)) <= 0.0:
            raise RuntimeError("EX no genero reaccion basal horizontal real.")
        if float(ey_info.get("fy", 0.0)) <= 0.0:
            raise RuntimeError("EY no genero reaccion basal horizontal real.")
        if float(tex_info.get("mz", 0.0)) <= 0.0:
            raise RuntimeError("TEX no genero momento basal torsor real.")
        if float(tey_info.get("mz", 0.0)) <= 0.0:
            raise RuntimeError("TEY no genero momento basal torsor real.")

        ret = SapModel.File.Save(filepath)
        check_ret(ret, f"File.Save('{filepath}')")

        log.info("Pre-check base reactions:")
        for case_name in ["EX", "EY", "TEX", "TEY"]:
            info = snapshot["cases"].get(case_name)
            if info:
                log.info(
                    f"  {case_name}: Fx={info['fx']:.3f}, Fy={info['fy']:.3f}, "
                    f"Fz={info['fz']:.3f}, Mz={info['mz']:.3f} "
                    f"[{info.get('source', 'unknown')}]"
                )
            else:
                log.info(f"  {case_name}: no data")

        log.info("Ready for step 12: extract official results")
        return 0
    except Exception as exc:
        log.error(f"[FATAL] {exc}")
        return 1
    finally:
        if SapModel is not None:
            try:
                disconnect(False)
            except Exception:
                pass


if __name__ == "__main__":
    sys.exit(main())
