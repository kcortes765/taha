"""
verify_ed2.py - Verificador oficial Ed.2 Parte 1.

Valida exclusivamente evidencia real ya extraida en `results/`.
No se conecta a ETABS ni completa resultados faltantes.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import AREA_PLANTA, LX_PLANTA, LY_PLANTA, N_STORIES
from ed2_static_official import REQUIRED_RESULT_FILES, read_csv, read_json, validate_required_results


def main() -> int:
    missing = validate_required_results()
    if missing:
        print("FAIL - faltan resultados oficiales:")
        for name in missing:
            print(f"  - {name}")
        return 1

    summary = read_json("ed2_summary.json")
    _, base_rows = read_csv("ed2_base_reactions.csv")
    _, drift_rows = read_csv("ed2_drift_envelope.csv")
    _, static_rows = read_csv("ed2_static_distribution.csv")
    _, story_weight_rows = read_csv("ed2_story_weights.csv")
    _, story_force_rows = read_csv("ed2_story_forces_summary.csv")
    _, cm_cr_rows = read_csv("ed2_cm_cr_per_story.csv")

    failures = []
    warnings = []

    def f(row, key):
        return float(str(row.get(key, "0")).replace(",", "."))

    if summary["W_total_tonf"] <= 0:
        failures.append("Peso sismico W no valido")
    if summary.get("W_per_area_tonf_m2", 0.0) <= 0:
        failures.append("W/area no fue calculado")

    if summary["Tx_s"] <= 0 or summary["Ty_s"] <= 0 or summary["Tz_s"] <= 0:
        failures.append("Periodos modales no validos")

    if not (summary["Cmin"] <= summary["Cx"] <= summary["Cmax"]):
        failures.append("Cx fuera de limites Cmin/Cmax")
    if not (summary["Cmin"] <= summary["Cy"] <= summary["Cmax"]):
        failures.append("Cy fuera de limites Cmin/Cmax")

    ex_fx = summary.get("EX_base_Fx_tonf", 0.0)
    ey_fy = summary.get("EY_base_Fy_tonf", 0.0)
    if ex_fx <= 0:
        failures.append("No hay reaccion basal real para EX")
    if ey_fy <= 0:
        failures.append("No hay reaccion basal real para EY")

    ex_gap = abs(ex_fx - summary["Vdx_tonf"]) / max(summary["Vdx_tonf"], 1e-9)
    ey_gap = abs(ey_fy - summary["Vdy_tonf"]) / max(summary["Vdy_tonf"], 1e-9)
    if ex_gap > 0.10:
        failures.append("EX no coincide con Vdx dentro de 10%")
    elif ex_gap > 0.05:
        warnings.append("EX no coincide con Vdx dentro de 5%")
    if ey_gap > 0.10:
        failures.append("EY no coincide con Vdy dentro de 10%")
    elif ey_gap > 0.05:
        warnings.append("EY no coincide con Vdy dentro de 5%")

    if summary.get("story_weight_source", "unknown") != "etabs_table":
        failures.append("Los pesos por piso no provienen de tabla ETABS")
    if summary.get("drift_cm_source", "unknown") != "nearest_cm_table":
        failures.append("El drift en CM no proviene de tabla de drifts filtrada al CM")
    if summary.get("drift_excess_source", "unknown") != "paired_combo_cm":
        failures.append("La condicion 2 de drift no esta emparejada por combo CM/punto")
    if summary.get("analysis_return_code", None) != 0:
        failures.append("El analisis no registra return code 0")
    if summary.get("etabs_detected_major", 0) != summary.get("etabs_expected_major", 21):
        failures.append("La corrida no se hizo en la version ETABS esperada")
    if not summary.get("etabs_strict_ret_mode", False):
        failures.append("La corrida no quedo bajo modo estricto de retornos COM")

    if summary.get("max_drift_cm", summary["max_drift"]) > summary.get("drift_limit_cm", summary["drift_limit"]):
        failures.append("Drift en CM supera limite 0.002")
    if summary.get("max_drift_excess", 0.0) > summary.get("drift_limit_point", 0.001):
        failures.append("Exceso torsional de drift supera limite 0.001")

    if summary.get("torsion_nodal_fallback_count", 0) > 0:
        failures.append("La torsion accidental cayo en nodal_mz_fallback en al menos un piso")

    if not summary.get("torsion_all_force_couple", False):
        warnings.append("La torsion accidental no quedo enteramente aplicada como force_couple")

    if not summary.get("first_three_modes_ok", False):
        warnings.append("Los primeros 3 modos no cubren X/Y/RZ en conjunto")

    if len(static_rows) != 5:
        failures.append("La distribucion estatica no tiene 5 pisos")
    if len(drift_rows) != 5:
        failures.append("La envolvente de drift no tiene 5 pisos")
    if len(story_weight_rows) != 5:
        failures.append("Los pesos por piso no tienen 5 historias")
    if len(cm_cr_rows) != 5:
        failures.append("CM/CR no tiene 5 historias")
    if summary.get("story_forces_story_count_ex", 0) != 5:
        failures.append("Story Forces EX no tiene 5 historias")
    if summary.get("story_forces_story_count_ey", 0) != 5:
        failures.append("Story Forces EY no tiene 5 historias")

    story_weight_sum = sum(f(row, "weight_tonf") for row in story_weight_rows)
    weight_gap = abs(story_weight_sum - summary["W_total_tonf"]) / max(summary["W_total_tonf"], 1e-9)
    if weight_gap > 0.05:
        failures.append("La suma de pesos por piso no coincide con W dentro de 5%")
    elif weight_gap > 0.02:
        warnings.append("La suma de pesos por piso no coincide con W dentro de 2%")

    expected_w_per_area = summary["W_total_tonf"] / max(AREA_PLANTA * N_STORIES, 1e-9)
    if abs(expected_w_per_area - summary.get("W_per_area_tonf_m2", 0.0)) > 1e-6:
        failures.append("W/area no es consistente con W_total y area total")

    if not summary.get("cm_cr_all_within_plan", False):
        failures.append("CM/CR contiene coordenadas fuera de la planta")
    if not summary.get("cm_cr_no_zero", False):
        failures.append("CM/CR contiene rigideces con coordenada cero espuria")

    for row in cm_cr_rows:
        xcm = f(row, "xcm_m")
        ycm = f(row, "ycm_m")
        xcr = f(row, "xcr_m")
        ycr = f(row, "ycr_m")
        if not (0.0 <= xcm <= LX_PLANTA and 0.0 <= ycm <= LY_PLANTA):
            failures.append(f"CM fuera de planta en {row.get('story', '?')}")
            break
        if not (0.0 <= xcr <= LX_PLANTA and 0.0 <= ycr <= LY_PLANTA):
            failures.append(f"CR fuera de planta en {row.get('story', '?')}")
            break

    static_by_story = {row["story"]: row for row in static_rows}
    story_force_by_case_story = {(row["case"], row["story"]): row for row in story_force_rows}

    for story in static_by_story:
        ex_row = story_force_by_case_story.get(("EX", story))
        ey_row = story_force_by_case_story.get(("EY", story))
        if not ex_row or not ey_row:
            failures.append(f"Faltan Story Forces resumidas para {story}")
            continue

        ex_accum_gap = abs(f(ex_row, "Vx_accum_tonf") - f(static_by_story[story], "Vx_accum_tonf")) / max(
            f(static_by_story[story], "Vx_accum_tonf"), 1e-9
        )
        ey_accum_gap = abs(f(ey_row, "Vy_accum_tonf") - f(static_by_story[story], "Vy_accum_tonf")) / max(
            f(static_by_story[story], "Vy_accum_tonf"), 1e-9
        )
        ex_floor_gap = abs(f(ex_row, "floor_Fx_tonf") - f(static_by_story[story], "Fx_tonf")) / max(
            f(static_by_story[story], "Fx_tonf"), 1e-9
        )
        ey_floor_gap = abs(f(ey_row, "floor_Fy_tonf") - f(static_by_story[story], "Fy_tonf")) / max(
            f(static_by_story[story], "Fy_tonf"), 1e-9
        )

        if ex_accum_gap > 0.10:
            failures.append(f"Story Forces EX no coincide con Vx teórico en {story} dentro de 10%")
        if ey_accum_gap > 0.10:
            failures.append(f"Story Forces EY no coincide con Vy teórico en {story} dentro de 10%")
        if ex_floor_gap > 0.10:
            failures.append(f"Story Forces EX no coincide con Fx de piso en {story} dentro de 10%")
        if ey_floor_gap > 0.10:
            failures.append(f"Story Forces EY no coincide con Fy de piso en {story} dentro de 10%")

    tex_target = summary.get("TEX_target_Mz_tonf_m", 0.0)
    tey_target = summary.get("TEY_target_Mz_tonf_m", 0.0)
    tex_real = summary.get("TEX_base_Mz_tonf_m", 0.0)
    tey_real = summary.get("TEY_base_Mz_tonf_m", 0.0)
    if tex_target > 0:
        tex_gap = abs(tex_real - tex_target) / max(tex_target, 1e-9)
        if tex_gap > 0.10:
            failures.append("TEX no reproduce el momento basal torsor dentro de 10%")
        elif tex_gap > 0.05:
            warnings.append("TEX no reproduce el momento basal torsor dentro de 5%")
    if tey_target > 0:
        tey_gap = abs(tey_real - tey_target) / max(tey_target, 1e-9)
        if tey_gap > 0.10:
            failures.append("TEY no reproduce el momento basal torsor dentro de 10%")
        elif tey_gap > 0.05:
            warnings.append("TEY no reproduce el momento basal torsor dentro de 5%")

    print("ED2 Parte 1 - Verificacion oficial")
    print(f"W = {summary['W_total_tonf']:.3f} tonf")
    print(f"W/area = {summary.get('W_per_area_tonf_m2', 0.0):.6f} tonf/m2")
    print(f"Tx = {summary['Tx_s']:.4f} s | Ty = {summary['Ty_s']:.4f} s | Tz = {summary['Tz_s']:.4f} s")
    print(f"Cx = {summary['Cx']:.5f} | Cy = {summary['Cy']:.5f} | Cmin = {summary['Cmin']:.5f} | Cmax = {summary['Cmax']:.5f}")
    print(f"Vdx = {summary['Vdx_tonf']:.3f} tonf | EX real = {ex_fx:.3f} tonf")
    print(f"Vdy = {summary['Vdy_tonf']:.3f} tonf | EY real = {ey_fy:.3f} tonf")
    print(
        f"Drift CM max = {summary.get('max_drift_cm', summary['max_drift']):.6f} | "
        f"limite CM = {summary.get('drift_limit_cm', summary['drift_limit']):.6f}"
    )
    print(
        f"Drift punto max = {summary.get('max_drift_point', 0.0):.6f} | "
        f"Exceso max = {summary.get('max_drift_excess', 0.0):.6f} | "
        f"limite exceso = {summary.get('drift_limit_point', 0.001):.6f}"
    )
    print(f"Story weights source = {summary.get('story_weight_source', 'unknown')}")
    print(f"Story weights file = {summary.get('story_weight_file', '')}")
    print(f"Drift CM source = {summary.get('drift_cm_source', 'unknown')}")
    print(f"Drift excess source = {summary.get('drift_excess_source', 'unknown')}")
    print(
        f"ETABS = {summary.get('etabs_detected_version', 'unknown')} | "
        f"major = {summary.get('etabs_detected_major', 0)} | "
        f"strict = {summary.get('etabs_strict_ret_mode', False)}"
    )
    print(
        f"Torsion force_couple = {summary.get('torsion_force_couple_count', 0)} | "
        f"nodal fallback = {summary.get('torsion_nodal_fallback_count', 0)}"
    )
    print(
        f"TEX Mz real/target = {summary.get('TEX_base_Mz_tonf_m', 0.0):.3f} / "
        f"{summary.get('TEX_target_Mz_tonf_m', 0.0):.3f}"
    )
    print(
        f"TEY Mz real/target = {summary.get('TEY_base_Mz_tonf_m', 0.0):.3f} / "
        f"{summary.get('TEY_target_Mz_tonf_m', 0.0):.3f}"
    )
    print(
        f"CM/CR stories = {summary.get('cm_cr_story_count', 0)} | "
        f"within plan = {summary.get('cm_cr_all_within_plan', False)} | "
        f"nonzero CR = {summary.get('cm_cr_no_zero', False)}"
    )
    print(f"First three modes OK = {summary.get('first_three_modes_ok', False)}")

    if warnings:
        print("WARNINGS")
        for item in warnings:
            print(f"  - {item}")

    if failures:
        print("FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
