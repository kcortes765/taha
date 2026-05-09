"""
10_combinations_ed2.py - Combinaciones oficiales Ed.2 Parte 1.

Define el set oficial del canon:
- C1, C2, C3 gravitacionales
- C4-C7 expandidas en variantes explicitas +/- torsion accidental
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import UNITS_TONF_M_C, check_ret, connect, disconnect, log, set_units
from ed2_static_official import OFFICIAL_COMBINATIONS, OFFICIAL_DRIFT_COMBINATIONS


def reset_combo(SapModel, combo_name: str) -> None:
    try:
        SapModel.RespCombo.Delete(combo_name)
    except Exception:
        pass


def combo_type_linear_additive() -> int:
    # CSI enum eCNameType is not needed here; RespCombo.SetCaseList uses
    # a simple combo already created with type 0 in typical ETABS COM flows.
    return 0


def create_combo(SapModel, combo_name: str, terms) -> None:
    reset_combo(SapModel, combo_name)
    ret = SapModel.RespCombo.Add(combo_name, combo_type_linear_additive())
    check_ret(ret, f"RespCombo.Add('{combo_name}')")

    for scale_factor, case_name in terms:
        ret = SapModel.RespCombo.SetCaseList(
            combo_name,
            0,  # 0 = case, 1 = combo
            case_name,
            float(scale_factor),
        )
        check_ret(ret, f"RespCombo.SetCaseList('{combo_name}', '{case_name}')")


def main() -> int:
    SapModel = None
    try:
        log.info("=" * 72)
        log.info("ED2 PARTE 1 - COMBINACIONES OFICIALES")
        log.info("=" * 72)
        SapModel = connect()
        set_units(SapModel, UNITS_TONF_M_C)
        try:
            SapModel.SetModelIsLocked(False)
        except Exception:
            pass

        for combo_name, terms in OFFICIAL_COMBINATIONS.items():
            create_combo(SapModel, combo_name, terms)
            log.info(f"  {combo_name}: {len(terms)} terms")

        for combo_name, terms in OFFICIAL_DRIFT_COMBINATIONS.items():
            create_combo(SapModel, combo_name, terms)
            log.info(f"  {combo_name}: {len(terms)} terms")

        log.info("Ready for step 11: full official analysis")
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
