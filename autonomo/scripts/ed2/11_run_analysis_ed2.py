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
from ed2_static_official import GRAVITY_CASES, OFFICIAL_CASES, select_cases_for_output, write_json


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


def get_base_reaction(SapModel, case_name: str):
    select_cases_for_output(SapModel, [case_name])
    try:
        result = SapModel.Results.BaseReac()
        if not isinstance(result, (tuple, list)) or len(result) < 10:
            return None
        n = int(result[0])
        if n <= 0:
            return None
        load_cases = result[1]
        fx = result[4]
        fy = result[5]
        fz = result[6]
        mx = result[7]
        my = result[8]
        mz = result[9]
        for i in range(n):
            if str(load_cases[i]).upper() == case_name.upper():
                return {
                    "case": case_name,
                    "fx": abs(float(fx[i])),
                    "fy": abs(float(fy[i])),
                    "fz": abs(float(fz[i])),
                    "mx": abs(float(mx[i])),
                    "my": abs(float(my[i])),
                    "mz": abs(float(mz[i])),
                }
    except Exception:
        return None
    return None


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
        set_run_flags(SapModel)

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
        for case_name in ["PP", "TERP", "TERT", "SCP", "SCT", "EX", "EY", "TEX", "TEY"]:
            snapshot["cases"][case_name] = get_base_reaction(SapModel, case_name)

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

        write_json("ed2_analysis_run.json", snapshot)
        ret = SapModel.File.Save(filepath)
        check_ret(ret, f"File.Save('{filepath}')")

        log.info("Pre-check base reactions:")
        for case_name in ["EX", "EY", "TEX", "TEY"]:
            info = snapshot["cases"].get(case_name)
            if info:
                log.info(
                    f"  {case_name}: Fx={info['fx']:.3f}, Fy={info['fy']:.3f}, "
                    f"Fz={info['fz']:.3f}, Mz={info['mz']:.3f}"
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
