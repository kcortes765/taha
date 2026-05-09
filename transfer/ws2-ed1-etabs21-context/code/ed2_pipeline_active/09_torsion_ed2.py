"""
09_torsion_ed2.py - Casos estaticos oficiales EX/EY/TEX/TEY.

Construye el vector sismico oficial del metodo estatico usando:
- T* reales desde el caso modal "Modal"
- story weights del modelo oficial
- torsion accidental estatica por piso

Salida:
- patrones/casos ETABS: EX, EY, TEX, TEY
- `results/ed2_static_distribution.csv`
- `results/ed2_static_seed.json`
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    LTYPE_QUAKE,
    UNITS_TONF_M_C,
    check_ret,
    connect,
    disconnect,
    log,
    set_units,
)
from ed2_static_official import (
    EX_CASE,
    EY_CASE,
    TEX_CASE,
    TEY_CASE,
    compute_static_distribution,
    export_static_distribution,
    find_story_center_points,
    find_story_torsion_points,
    read_csv,
    read_json,
    write_json,
)

ENV_ALLOW_GEOMETRIC_CM_FALLBACK = "ED2_ALLOW_CM_GEOMETRIC_FALLBACK"


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name, "")
    if not value:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on", "si"}


def reset_pattern(SapModel, name: str) -> None:
    try:
        SapModel.LoadPatterns.Delete(name)
    except Exception:
        pass
    ret = SapModel.LoadPatterns.Add(name, LTYPE_QUAKE, 0.0, False)
    check_ret(ret, f"LoadPatterns.Add('{name}')")


def build_static_inputs(allow_analytic_fallback: bool = False):
    modal_seed = read_json("ed2_modal_seed.json")
    directional = modal_seed["directional_periods"]
    tx = float(directional["X"]["period"])
    ty = float(directional["Y"]["period"])
    if tx <= 0 or ty <= 0:
        raise RuntimeError("T* reales no disponibles. Ejecuta primero 08_seismic_ed2.py.")

    weight_filename = "ed2_story_weights.csv"
    _, weight_rows = read_csv(weight_filename)
    story_weights = [
        {
            "story": row["story"],
            "elevation_m": float(str(row["elevation_m"]).replace(",", ".")),
            "weight_tonf": float(str(row["weight_tonf"]).replace(",", ".")),
        }
        for row in weight_rows
        if row.get("story")
    ]
    if len(story_weights) != 5:
        raise RuntimeError(
            "Story weights oficiales no disponibles o incompletos. "
            "Ejecuta primero 08_seismic_ed2.py."
        )
    static_data = compute_static_distribution(tx, ty, story_weights)
    try:
        story_weight_source = read_json("ed2_story_weights_source.json")
    except Exception:
        story_weight_source = {"source": "unknown"}
    if story_weight_source.get("source") != "etabs_table" and not allow_analytic_fallback:
        raise RuntimeError(
            "Los pesos por piso no provienen de tabla ETABS. "
            "El flujo oficial no acepta continuar con fuente analitica."
        )
    export_static_distribution(static_data)
    write_json(
        "ed2_static_seed.json",
        {
            "directional_periods": directional,
            "story_weight_source": story_weight_source,
            "story_weight_file": weight_filename,
            "summary": {
                "W_total_tonf": static_data["W_total_tonf"],
                "Cx": static_data["Cx"],
                "Cy": static_data["Cy"],
                "Cmin": static_data["Cmin"],
                "Cmax": static_data["Cmax"],
                "Vdx_tonf": static_data["Vdx_tonf"],
                "Vdy_tonf": static_data["Vdy_tonf"],
            },
        },
    )
    return static_data


def apply_pure_torsion(SapModel, pattern_name: str, target_mz: float, points, story: str, allow_nodal_fallback: bool = False):
    """Apply a floor torque as a force couple on distributed diaphragm joints.

    This is closer to the ETABS UI workflow than concentrating the full Mz on
    a single arbitrary joint. If the geometry is degenerate, it falls back to
    a nodal Mz on the first available point.
    """
    if abs(target_mz) <= 1e-9:
        return "zero"
    if not points:
        raise RuntimeError(f"Story sin puntos para torsion: {story}")

    if len(points) >= 2:
        cx = sum(point["x"] for point in points) / len(points)
        cy = sum(point["y"] for point in points) / len(points)
        denom = sum(
            (point["x"] - cx) ** 2 + (point["y"] - cy) ** 2
            for point in points
        )
        if denom > 1e-9:
            alpha = target_mz / denom
            for point in points:
                dx = point["x"] - cx
                dy = point["y"] - cy
                fx = -alpha * dy
                fy = alpha * dx
                ret = SapModel.PointObj.SetLoadForce(
                    point["name"],
                    pattern_name,
                    [fx, fy, 0.0, 0.0, 0.0, 0.0],
                    True,
                    "Global",
                    0,
                )
                check_ret(ret, f"SetLoadForce({point['name']}, {pattern_name})")
            resultant_fx = sum(-alpha * (point["y"] - cy) for point in points)
            resultant_fy = sum(alpha * (point["x"] - cx) for point in points)
            achieved_mz = sum(
                (point["x"] - cx) * (alpha * (point["x"] - cx))
                - (point["y"] - cy) * (-alpha * (point["y"] - cy))
                for point in points
            )
            return {
                "method": "force_couple",
                "target_mz_tonf_m": round(float(target_mz), 6),
                "achieved_mz_tonf_m": round(float(achieved_mz), 6),
                "resultant_fx_tonf": round(float(resultant_fx), 9),
                "resultant_fy_tonf": round(float(resultant_fy), 9),
                "centroid_x_m": round(float(cx), 6),
                "centroid_y_m": round(float(cy), 6),
                "point_count": len(points),
            }

    if not allow_nodal_fallback:
        raise RuntimeError(
            f"No se pudo construir force_couple estable para {pattern_name} en {story}. "
            "El flujo oficial no acepta nodal_mz_fallback."
        )
    reference_joint = points[0]["name"]
    ret = SapModel.PointObj.SetLoadForce(
        reference_joint,
        pattern_name,
        [0.0, 0.0, 0.0, 0.0, 0.0, target_mz],
        True,
        "Global",
        0,
    )
    check_ret(ret, f"SetLoadForce({reference_joint}, {pattern_name})")
    return {
        "method": "nodal_mz_fallback",
        "target_mz_tonf_m": round(float(target_mz), 6),
        "achieved_mz_tonf_m": round(float(target_mz), 6),
        "resultant_fx_tonf": 0.0,
        "resultant_fy_tonf": 0.0,
        "reference_joint": reference_joint,
        "point_count": len(points),
    }


def apply_story_forces(
    SapModel,
    static_data,
    allow_nodal_fallback: bool = False,
    allow_geometric_cm_fallback: bool = False,
) -> None:
    log.info("Step 1: Resetting official static patterns...")
    for pattern in [EX_CASE, EY_CASE, TEX_CASE, TEY_CASE]:
        reset_pattern(SapModel, pattern)

    log.info("Step 2: Locating diaphragm joints per story...")
    story_force_points = find_story_center_points(
        SapModel,
        per_story=4,
        allow_geometric_fallback=allow_geometric_cm_fallback,
    )
    story_torsion_points = find_story_torsion_points(
        SapModel,
        per_story=4,
        allow_geometric_fallback=allow_geometric_cm_fallback,
    )
    missing = [story for story, points in story_force_points.items() if not points]
    if missing:
        raise RuntimeError(
            "No se encontraron joints para aplicar el vector estatico en: "
            + ", ".join(missing)
        )

    log.info("Step 3: Applying EX/EY/TEX/TEY loads...")
    torsion_methods = {}
    for row in static_data["rows"]:
        story = row["story"]
        force_points = story_force_points.get(story, [])
        torsion_points = story_torsion_points.get(story) or force_points
        if not force_points:
            raise RuntimeError(f"Story sin joints centrales: {story}")

        fx_each = row["Fx_tonf"] / len(force_points)
        fy_each = row["Fy_tonf"] / len(force_points)

        for point in force_points:
            joint = point["name"]
            ret = SapModel.PointObj.SetLoadForce(
                joint,
                EX_CASE,
                [fx_each, 0.0, 0.0, 0.0, 0.0, 0.0],
                True,
                "Global",
                0,
            )
            check_ret(ret, f"SetLoadForce({joint}, EX)")

            ret = SapModel.PointObj.SetLoadForce(
                joint,
                EY_CASE,
                [0.0, fy_each, 0.0, 0.0, 0.0, 0.0],
                True,
                "Global",
                0,
            )
            check_ret(ret, f"SetLoadForce({joint}, EY)")

        tex_meta = apply_pure_torsion(
            SapModel,
            TEX_CASE,
            row["MtX_tonf_m"],
            torsion_points,
            story,
            allow_nodal_fallback=allow_nodal_fallback,
        )
        tey_meta = apply_pure_torsion(
            SapModel,
            TEY_CASE,
            row["MtY_tonf_m"],
            torsion_points,
            story,
            allow_nodal_fallback=allow_nodal_fallback,
        )

        torsion_methods[story] = {
            "force_point_count": len(force_points),
            "torsion_point_count": len(torsion_points),
            "force_centroid_x_m": round(sum(point["x"] for point in force_points) / len(force_points), 6),
            "force_centroid_y_m": round(sum(point["y"] for point in force_points) / len(force_points), 6),
            "sum_fx_each_tonf": round(float(fx_each * len(force_points)), 6),
            "sum_fy_each_tonf": round(float(fy_each * len(force_points)), 6),
            "TEX": tex_meta,
            "TEY": tey_meta,
        }

    write_json("ed2_torsion_application.json", torsion_methods)
    log.info("  Static loads applied")


def create_static_cases(SapModel) -> None:
    log.info("Step 4: Creating static load cases...")
    for case_name, pattern_name in [
        (EX_CASE, EX_CASE),
        (EY_CASE, EY_CASE),
        (TEX_CASE, TEX_CASE),
        (TEY_CASE, TEY_CASE),
    ]:
        ret = SapModel.LoadCases.StaticLinear.SetCase(case_name)
        check_ret(ret, f"StaticLinear.SetCase('{case_name}')")
        ret = SapModel.LoadCases.StaticLinear.SetLoads(
            case_name, 1, ["Load"], [pattern_name], [1.0]
        )
        check_ret(ret, f"StaticLinear.SetLoads('{case_name}')")
    log.info("  Static cases OK")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-nodal-fallback",
        action="store_true",
        help="Permite fallback nodal solo para depuracion no oficial.",
    )
    parser.add_argument(
        "--allow-analytic-fallback",
        action="store_true",
        help="Permite story weights analiticos solo para depuracion no oficial.",
    )
    parser.add_argument(
        "--allow-geometric-cm-fallback",
        action="store_true",
        help="Permite CM=centro geometrico solo para precheck no oficial.",
    )
    args = parser.parse_args()
    allow_geometric_cm_fallback = args.allow_geometric_cm_fallback or env_flag(
        ENV_ALLOW_GEOMETRIC_CM_FALLBACK,
        False,
    )
    SapModel = None
    try:
        log.info("=" * 72)
        log.info("ED2 PARTE 1 - CASOS ESTATICOS OFICIALES")
        log.info("=" * 72)
        static_data = build_static_inputs(allow_analytic_fallback=args.allow_analytic_fallback)

        SapModel = connect()
        set_units(SapModel, UNITS_TONF_M_C)
        try:
            SapModel.SetModelIsLocked(False)
        except Exception:
            pass

        apply_story_forces(
            SapModel,
            static_data,
            allow_nodal_fallback=args.allow_nodal_fallback,
            allow_geometric_cm_fallback=allow_geometric_cm_fallback,
        )
        create_static_cases(SapModel)

        log.info(
            "  Summary: "
            f"W={static_data['W_total_tonf']:.2f} tonf, "
            f"Vx={static_data['Vdx_tonf']:.2f} tonf, "
            f"Vy={static_data['Vdy_tonf']:.2f} tonf"
        )
        log.info("Ready for step 10: official combinations")
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
