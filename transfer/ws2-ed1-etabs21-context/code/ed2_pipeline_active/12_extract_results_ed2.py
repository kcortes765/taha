"""
12_extract_results_ed2.py - Extraccion oficial Ed.2 Parte 1.

Extrae y guarda:
- resultados modales
- drifts
- reacciones basales
- CM/CR por piso
- resumen oficial

Si faltan resultados reales o semillas oficiales del flujo estatico, falla.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    AREA_PLANTA,
    H_TOTAL,
    I_FACTOR,
    LX_PLANTA,
    LY_PLANTA,
    N_STORIES,
    STORY_ELEVATIONS,
    STORY_NAMES,
    UNITS_TONF_M_C,
    RESULTS_DIR,
    check_ret,
    DRIFT_LIMITE_CM,
    DRIFT_LIMITE_PUNTO,
    calc_C,
    calc_Cmax,
    calc_Cmin,
    connect,
    disconnect,
    log,
    set_units,
)
from ed2_static_official import (
    GRAVITY_CASES,
    OFFICIAL_DRIFT_COMBINATIONS,
    OFFICIAL_CASES,
    clamp,
    collect_joint_lookup,
    extract_base_reaction_case,
    extract_cm_cr_rows,
    extract_story_cm_data,
    REQUIRED_RESULT_FILES,
    export_summary_csv,
    extract_modal_rows_from_db,
    modal_first_three_summary,
    modal_directional_summary,
    parse_db_table,
    read_csv,
    read_json,
    select_combos_for_output,
    select_cases_for_output,
    write_csv,
    write_json,
)

ENV_ALLOW_GEOMETRIC_CM_FALLBACK = "ED2_ALLOW_CM_GEOMETRIC_FALLBACK"
ENV_ALLOW_THEORETICAL_STORY_FORCES_FALLBACK = "ED2_ALLOW_STORY_FORCES_THEORETICAL_FALLBACK"


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name, "")
    if not value:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on", "si"}


def extract_modal() -> list:
    modal_rows = extract_modal_rows_from_db(SapModel)
    if not modal_rows:
        try:
            _, cached_rows = read_csv("ed2_modal_results.csv")
        except Exception:
            cached_rows = []

        reused_rows = []
        for row in cached_rows:
            period = float(str(row.get("Period", "0")).replace(",", "."))
            if period <= 0:
                continue
            reused_rows.append(
                {
                    "Mode": str(row.get("Mode", "")),
                    "Period": f"{period:.6f}",
                    "UX": str(row.get("UX", "0")),
                    "UY": str(row.get("UY", "0")),
                    "RZ": str(row.get("RZ", "0")),
                    "SumUX": str(row.get("SumUX", "0")),
                    "SumUY": str(row.get("SumUY", "0")),
                }
            )
        if reused_rows:
            log.warning(
                "Las tablas modales no quedaron visibles via DB; se reutiliza "
                "ed2_modal_results.csv generado en step 08."
            )
            modal_rows = reused_rows

    if not modal_rows:
        raise RuntimeError("No se pudieron extraer resultados modales reales desde ETABS.")
    write_csv(
        "ed2_modal_results.csv",
        ["Mode", "Period", "UX", "UY", "RZ", "SumUX", "SumUY"],
        [
            [row["Mode"], row["Period"], row["UX"], row["UY"], row["RZ"], row["SumUX"], row["SumUY"]]
            for row in modal_rows
        ],
    )
    return modal_rows


def extract_base_reactions() -> list:
    cases = GRAVITY_CASES + ["EX", "EY", "TEX", "TEY"]
    rows = []
    for case_name in cases:
        reaction = extract_base_reaction_case(SapModel, case_name)
        if not reaction:
            continue
        rows.append(
            {
                "case": case_name,
                "Fx": abs(float(reaction.get("fx", 0.0))),
                "Fy": abs(float(reaction.get("fy", 0.0))),
                "Fz": abs(float(reaction.get("fz", 0.0))),
                "Mx": abs(float(reaction.get("mx", 0.0))),
                "My": abs(float(reaction.get("my", 0.0))),
                "Mz": abs(float(reaction.get("mz", 0.0))),
                "source": str(reaction.get("source", "")),
            }
        )
    write_csv(
        "ed2_base_reactions.csv",
        ["case", "Fx_tonf", "Fy_tonf", "Fz_tonf", "Mx_tonf_m", "My_tonf_m", "Mz_tonf_m", "source"],
        [
            [
                row["case"],
                f"{row['Fx']:.6f}",
                f"{row['Fy']:.6f}",
                f"{row['Fz']:.6f}",
                f"{row['Mx']:.6f}",
                f"{row['My']:.6f}",
                f"{row['Mz']:.6f}",
                row.get("source", ""),
            ]
            for row in rows
        ],
    )
    return rows


def extract_story_forces(allow_theoretical_fallback: bool = False) -> tuple[list, dict]:
    def f(row, key):
        return float(str(row.get(key, "0")).replace(",", "."))

    def export_story_force_outputs(raw_rows: list, summary_rows: list, source: str) -> tuple[list, dict]:
        write_csv(
            "ed2_story_forces.csv",
            ["story", "case", "location", "Vx_tonf", "Vy_tonf", "Mx_tonf_m", "My_tonf_m", "source"],
            [
                [
                    row["story"],
                    row["case"],
                    row["location"],
                    f"{row['Vx']:.6f}",
                    f"{row['Vy']:.6f}",
                    f"{row['Mx']:.6f}",
                    f"{row['My']:.6f}",
                    source,
                ]
                for row in raw_rows
            ],
        )

        write_csv(
            "ed2_story_forces_summary.csv",
            [
                "story",
                "case",
                "selected_location",
                "Vx_accum_tonf",
                "Vy_accum_tonf",
                "floor_Fx_tonf",
                "floor_Fy_tonf",
                "Mx_overturning_tonf_m",
                "My_overturning_tonf_m",
                "source",
            ],
            [
                [
                    row["story"],
                    row["case"],
                    row["selected_location"],
                    f"{row['Vx_accum_tonf']:.6f}",
                    f"{row['Vy_accum_tonf']:.6f}",
                    f"{row['floor_Fx_tonf']:.6f}",
                    f"{row['floor_Fy_tonf']:.6f}",
                    f"{row['Mx_overturning_tonf_m']:.6f}",
                    f"{row['My_overturning_tonf_m']:.6f}",
                    source,
                ]
                for row in summary_rows
            ],
        )
        return summary_rows, {"source": source}

    select_cases_for_output(SapModel, ["EX", "EY"])
    fields = None
    rows = None
    for table_name in ["Story Forces"]:
        fields, rows = parse_db_table(SapModel, table_name)
        if rows:
            break
    if not rows:
        fields = None

    lower_map = {field.lower().strip(): field for field in (fields or [])}

    def pick_field(candidates):
        for candidate in candidates:
            for lower_name, original in lower_map.items():
                if candidate == lower_name or candidate in lower_name:
                    return original
        return None

    story_key = pick_field(["story"])
    case_key = pick_field(["outputcase", "load case", "case", "combo"])
    location_key = pick_field(["location"])
    vx_key = pick_field(["vx"])
    vy_key = pick_field(["vy"])
    mx_key = pick_field(["mx"])
    my_key = pick_field(["my"])

    raw = []
    if story_key and case_key and (vx_key or vy_key):
        for row in rows or []:
            story = str(row.get(story_key, "")).strip()
            case = str(row.get(case_key, "")).strip()
            if story not in STORY_NAMES or case.upper() not in {"EX", "EY"}:
                continue
            raw.append(
                {
                    "story": story,
                    "case": case.upper(),
                    "location": str(row.get(location_key, "")).strip(),
                    "Vx": abs(float(str(row.get(vx_key, "0")).replace(",", "."))) if vx_key else 0.0,
                    "Vy": abs(float(str(row.get(vy_key, "0")).replace(",", "."))) if vy_key else 0.0,
                    "Mx": abs(float(str(row.get(mx_key, "0")).replace(",", "."))) if mx_key else 0.0,
                    "My": abs(float(str(row.get(my_key, "0")).replace(",", "."))) if my_key else 0.0,
                }
            )

    if raw:
        summary_rows = []
        for case_name in ["EX", "EY"]:
            case_rows = [row for row in raw if row["case"] == case_name]
            selected = {}
            for story in STORY_NAMES:
                story_rows = [row for row in case_rows if row["story"] == story]
                if not story_rows:
                    continue
                bottom_rows = [
                    row
                    for row in story_rows
                    if str(row["location"]).strip().upper() in {"BOTTOM", "BOT", "B"}
                ]
                choice_pool = bottom_rows or story_rows
                selected[story] = max(
                    choice_pool,
                    key=lambda item: max(item["Vx"], item["Vy"], item["Mx"], item["My"]),
                )

            if len(selected) != len(STORY_NAMES):
                raise RuntimeError(
                    f"'Story Forces' no entrego las 5 historias completas para {case_name}."
                )

            ordered_desc = sorted(
                selected.values(),
                key=lambda item: STORY_ELEVATIONS[STORY_NAMES.index(item["story"])],
                reverse=True,
            )
            prev_vx = 0.0
            prev_vy = 0.0
            for row in ordered_desc:
                floor_fx = max(0.0, row["Vx"] - prev_vx)
                floor_fy = max(0.0, row["Vy"] - prev_vy)
                summary_rows.append(
                    {
                        "story": row["story"],
                        "case": case_name,
                        "selected_location": row["location"],
                        "Vx_accum_tonf": row["Vx"],
                        "Vy_accum_tonf": row["Vy"],
                        "floor_Fx_tonf": floor_fx,
                        "floor_Fy_tonf": floor_fy,
                        "Mx_overturning_tonf_m": row["Mx"],
                        "My_overturning_tonf_m": row["My"],
                    }
                )
                prev_vx = row["Vx"]
                prev_vy = row["Vy"]

        summary_rows.sort(key=lambda item: (item["case"], STORY_NAMES.index(item["story"])))
        return export_story_force_outputs(raw, summary_rows, "etabs_table")

    if not allow_theoretical_fallback:
        raise RuntimeError("La tabla 'Story Forces' no trae campos suficientes para Ed.2.")

    _, static_rows = read_csv("ed2_static_distribution.csv")
    if len(static_rows) != len(STORY_NAMES):
        raise RuntimeError(
            "Story Forces real no disponible y ed2_static_distribution.csv no tiene las 5 historias."
        )

    raw_fallback = []
    summary_rows = []
    for row in static_rows:
        story = str(row.get("story", "")).strip()
        vx_accum = f(row, "Vx_accum_tonf")
        vy_accum = f(row, "Vy_accum_tonf")
        floor_fx = f(row, "Fx_tonf")
        floor_fy = f(row, "Fy_tonf")
        mx_overturning = f(row, "Mx_overturning_tonf_m")
        my_overturning = f(row, "My_overturning_tonf_m")

        raw_fallback.append(
            {
                "story": story,
                "case": "EX",
                "location": "THEORETICAL_STATIC_DISTRIBUTION",
                "Vx": vx_accum,
                "Vy": 0.0,
                "Mx": mx_overturning,
                "My": my_overturning,
            }
        )
        raw_fallback.append(
            {
                "story": story,
                "case": "EY",
                "location": "THEORETICAL_STATIC_DISTRIBUTION",
                "Vx": 0.0,
                "Vy": vy_accum,
                "Mx": mx_overturning,
                "My": my_overturning,
            }
        )

        summary_rows.append(
            {
                "story": story,
                "case": "EX",
                "selected_location": "THEORETICAL_STATIC_DISTRIBUTION",
                "Vx_accum_tonf": vx_accum,
                "Vy_accum_tonf": 0.0,
                "floor_Fx_tonf": floor_fx,
                "floor_Fy_tonf": 0.0,
                "Mx_overturning_tonf_m": mx_overturning,
                "My_overturning_tonf_m": my_overturning,
            }
        )
        summary_rows.append(
            {
                "story": story,
                "case": "EY",
                "selected_location": "THEORETICAL_STATIC_DISTRIBUTION",
                "Vx_accum_tonf": 0.0,
                "Vy_accum_tonf": vy_accum,
                "floor_Fx_tonf": 0.0,
                "floor_Fy_tonf": floor_fy,
                "Mx_overturning_tonf_m": mx_overturning,
                "My_overturning_tonf_m": my_overturning,
            }
        )

    summary_rows.sort(key=lambda item: (item["case"], STORY_NAMES.index(item["story"])))
    log.warning(
        "Story Forces real no disponible via DB; se reutiliza ed2_static_distribution.csv "
        "solo como precheck no oficial."
    )
    return export_story_force_outputs(raw_fallback, summary_rows, "theoretical_static_distribution")


def extract_story_drifts(allow_geometric_cm_fallback: bool = False) -> tuple:
    combo_names = list(OFFICIAL_DRIFT_COMBINATIONS.keys())
    select_combos_for_output(SapModel, combo_names)
    joint_lookup = collect_joint_lookup(SapModel)

    def infer_direction(case_name: str, explicit_direction: str = "") -> str:
        direction = str(explicit_direction or "").upper()
        if direction.startswith("X"):
            return "X"
        if direction.startswith("Y"):
            return "Y"
        case_upper = str(case_name or "").upper()
        if "_X" in case_upper or case_upper.startswith("DRIFT_X"):
            return "X"
        if "_Y" in case_upper or case_upper.startswith("DRIFT_Y"):
            return "Y"
        return ""

    def parse_float_row(row, *keys):
        for key in keys:
            if key in row and str(row.get(key, "")).strip() != "":
                return float(str(row.get(key, "0")).replace(",", "."))
        raise ValueError

    def parse_coord_row(row, *keys):
        for key in keys:
            if key in row and str(row.get(key, "")).strip() != "":
                return float(str(row.get(key, "0")).replace(",", ".")), True
        return 0.0, False

    raw_records = []
    joint_records = []
    for table_name in ["Joint Drifts", "Story Drifts"]:
        _, rows = parse_db_table(SapModel, table_name)
        if not rows:
            continue
        for row in rows:
            story = str(row.get("Story", row.get("story", ""))).strip()
            case = str(row.get("OutputCase", row.get("Load Case", row.get("Case", row.get("Combo", ""))))).strip()
            label = str(row.get("Label", row.get("Point Label", row.get("Joint", row.get("label", ""))))).strip()
            if story not in STORY_NAMES or not case:
                continue
            x, has_x = parse_coord_row(row, "X", "JointX", "X Coord", "CoordX")
            y, has_y = parse_coord_row(row, "Y", "JointY", "Y Coord", "CoordY")
            if label and not (has_x and has_y):
                joint_meta = joint_lookup.get("".join(ch for ch in label.lower() if ch.isalnum()))
                if joint_meta:
                    x = float(joint_meta.get("x", 0.0))
                    y = float(joint_meta.get("y", 0.0))
                    has_x = True
                    has_y = True

            explicit_direction = str(row.get("Direction", row.get("Dir", row.get("direction", "")))).strip()
            if explicit_direction:
                try:
                    drift = parse_float_row(row, "Drift", "drift")
                except Exception:
                    drift = 0.0
                direction = infer_direction(case, explicit_direction)
                if direction:
                    record = {
                        "story": story,
                        "case": case,
                        "direction": direction,
                        "drift": drift,
                        "label": label,
                        "x": x,
                        "y": y,
                        "has_coord": has_x and has_y,
                    }
                    raw_records.append(record)
                    joint_records.append(record)
                continue

            directional_keys = [
                ("X", ("Drift X", "DriftX", "X Drift")),
                ("Y", ("Drift Y", "DriftY", "Y Drift")),
            ]
            for direction, keys in directional_keys:
                drift_value = None
                for key in keys:
                    if key in row and str(row.get(key, "")).strip() != "":
                        drift_value = float(str(row.get(key, "0")).replace(",", "."))
                        break
                if drift_value is None:
                    continue
                record = {
                    "story": story,
                    "case": case,
                    "direction": direction,
                    "drift": drift_value,
                    "label": label,
                    "x": x,
                    "y": y,
                    "has_coord": has_x and has_y,
                }
                raw_records.append(record)
                joint_records.append(record)
        if raw_records:
            break

    if not raw_records:
        try:
            raw = SapModel.Results.StoryDrifts()
        except Exception:
            raw = None

        if isinstance(raw, (tuple, list)) and len(raw) >= 11:
            try:
                n = int(raw[0])
            except Exception:
                n = 0
            if n > 0:
                for i in range(n):
                    raw_records.append({
                        "story": str(raw[1][i]),
                        "case": str(raw[2][i]),
                        "direction": infer_direction(str(raw[2][i]), str(raw[5][i])),
                        "drift": float(raw[6][i]),
                        "label": str(raw[7][i]),
                        "x": 0.0,
                        "y": 0.0,
                        "has_coord": False,
                    })

    if not raw_records:
        raise RuntimeError("No se pudieron extraer drifts reales desde ETABS.")

    if joint_lookup:
        for record in raw_records:
            if record["has_coord"] or not record["label"]:
                continue
            joint_meta = joint_lookup.get("".join(ch for ch in str(record["label"]).lower() if ch.isalnum()))
            if not joint_meta:
                continue
            record["x"] = float(joint_meta.get("x", 0.0))
            record["y"] = float(joint_meta.get("y", 0.0))
            record["has_coord"] = True

    write_csv(
        "ed2_story_drifts.csv",
        ["story", "case", "direction", "drift", "label", "x_m", "y_m"],
        [
            [
                r["story"],
                r["case"],
                r["direction"],
                f"{r['drift']:.8f}",
                r["label"],
                f"{r['x']:.6f}",
                f"{r['y']:.6f}",
            ]
            for r in raw_records
        ],
    )

    diaphragm_rows = []
    for table_name in ["Diaphragm Max Over Avg Drifts", "Story Max/Avg Drifts"]:
        fields, rows = parse_db_table(SapModel, table_name)
        if not rows:
            continue
        for row in rows:
            story = row.get("Story", row.get("story", ""))
            case = row.get("OutputCase", row.get("Load Case", row.get("Case", row.get("Combo", ""))))
            direction = infer_direction(case, row.get("Direction", row.get("Dir", row.get("direction", ""))))
            if story not in STORY_NAMES or not case or not direction:
                continue
            max_drift = float(str(row.get("Max Drift", row.get("MaxDrift", row.get("drift", "0")))).replace(",", ".") or "0")
            avg_drift = float(str(row.get("Avg Drift", row.get("Average Drift", row.get("AvgDrift", "0")))).replace(",", ".") or "0")
            ratio = float(str(row.get("Ratio", row.get("Max/Avg", row.get("ratio", "0")))).replace(",", ".") or "0")
            label = str(row.get("Label", row.get("Point Label", row.get("label", ""))))
            diaphragm_rows.append({
                "story": story,
                "case": case,
                "direction": direction,
                "max_drift": abs(max_drift),
                "avg_drift": abs(avg_drift),
                "ratio": abs(ratio),
                "label": label,
            })
        if diaphragm_rows:
            break

    if not diaphragm_rows:
        raise RuntimeError(
            "No se pudo extraer 'Diaphragm Max Over Avg Drifts' para verificar drift CM/exceso torsional."
        )

    cm_meta = extract_story_cm_data(SapModel, allow_geometric_fallback=allow_geometric_cm_fallback)
    cm_targets = cm_meta.get("cm_map", {})
    cm_source = "diaphragm_avg_fallback"
    cm_records_by_case = {}
    if cm_targets:
        nearest = {}
        for record in joint_records:
            if record["story"] not in cm_targets or not record["has_coord"] or not record["direction"]:
                continue
            target = cm_targets[record["story"]]
            distance = ((record["x"] - target["xcm"]) ** 2 + (record["y"] - target["ycm"]) ** 2) ** 0.5
            key = (record["story"], record["case"], record["direction"])
            current = nearest.get(key)
            if current is None or distance < current["distance"]:
                nearest[key] = {**record, "distance": distance}
        if nearest:
            cm_records_by_case = {
                (key[0], key[1], key[2]): {
                    "story": value["story"],
                    "case": value["case"],
                    "direction": value["direction"],
                    "drift": value["drift"],
                    "label": value["label"],
                    "x": value["x"],
                    "y": value["y"],
                    "has_coord": value["has_coord"],
                }
                for key, value in nearest.items()
            }
            if cm_records_by_case:
                if cm_meta.get("source") == "cm_table":
                    cm_source = "nearest_cm_table"
                elif cm_meta.get("source") == "assembled_joint_masses":
                    cm_source = "nearest_cm_assembled_joint_masses"
                elif cm_meta.get("source") == "geometric_center":
                    cm_source = "nearest_cm_geometric_center"
                else:
                    cm_source = "nearest_cm_unknown"

    if not cm_records_by_case:
        fallback_cm = {}
        for record in raw_records:
            direction = record["direction"]
            if record["story"] not in STORY_NAMES or direction not in ("X", "Y"):
                continue
            key = (record["story"], record["case"], direction)
            current = fallback_cm.get(key)
            if current is None or abs(record["drift"]) > abs(current["drift"]):
                fallback_cm[key] = record
        if fallback_cm:
            cm_records_by_case = fallback_cm
            cm_source = "story_drifts_fallback"

    def best_cm_record(story_name: str, direction: str):
        candidates = [
            record
            for (story, _, dir_name), record in cm_records_by_case.items()
            if story == story_name and dir_name == direction
        ]
        if not candidates:
            return {"drift": 0.0, "case": "", "label": ""}
        return max(candidates, key=lambda item: abs(item["drift"]))

    def governing_point_row(story_name: str, direction: str):
        return max(
            [r for r in diaphragm_rows if r["story"] == story_name and r["direction"] == direction],
            key=lambda item: item["max_drift"],
            default={"avg_drift": 0.0, "max_drift": 0.0, "ratio": 0.0, "case": "", "label": ""},
        )

    def governing_excess_row(story_name: str, direction: str):
        candidates = []
        for point_row in [r for r in diaphragm_rows if r["story"] == story_name and r["direction"] == direction]:
            paired_cm = cm_records_by_case.get((story_name, point_row["case"], direction))
            if paired_cm:
                cm_value = abs(paired_cm["drift"])
                source = "paired_combo_cm"
                cm_label = paired_cm.get("label", "")
            else:
                cm_value = abs(point_row["avg_drift"])
                source = "diaphragm_avg_fallback"
                cm_label = ""
            candidates.append(
                {
                    "case": point_row["case"],
                    "label": point_row["label"],
                    "max_drift": point_row["max_drift"],
                    "cm_drift": cm_value,
                    "cm_label": cm_label,
                    "excess": max(0.0, point_row["max_drift"] - cm_value),
                    "source": source,
                }
            )
        if not candidates:
            return {
                "case": "",
                "label": "",
                "max_drift": 0.0,
                "cm_drift": 0.0,
                "cm_label": "",
                "excess": 0.0,
                "source": "missing",
            }
        return max(candidates, key=lambda item: item["excess"])

    envelope = []
    for story_name, elevation in zip(STORY_NAMES, STORY_ELEVATIONS):
        cm_row_x = best_cm_record(story_name, "X")
        cm_row_y = best_cm_record(story_name, "Y")
        row_x = governing_point_row(story_name, "X")
        row_y = governing_point_row(story_name, "Y")
        excess_x = governing_excess_row(story_name, "X")
        excess_y = governing_excess_row(story_name, "Y")
        envelope.append({
            "story": story_name,
            "elevation_m": elevation,
            "drift_x": abs(cm_row_x.get("drift", 0.0)),
            "drift_y": abs(cm_row_y.get("drift", 0.0)),
            "max_drift_x": row_x["max_drift"],
            "max_drift_y": row_y["max_drift"],
            "excess_x": excess_x["excess"],
            "excess_y": excess_y["excess"],
            "governing_cm_combo_x": cm_row_x.get("case", ""),
            "governing_cm_combo_y": cm_row_y.get("case", ""),
            "governing_combo_x": row_x["case"],
            "governing_combo_y": row_y["case"],
            "governing_excess_combo_x": excess_x["case"],
            "governing_excess_combo_y": excess_y["case"],
            "cm_label_x": cm_row_x.get("label", ""),
            "cm_label_y": cm_row_y.get("label", ""),
            "label_x": row_x["label"],
            "label_y": row_y["label"],
            "excess_label_x": excess_x["label"],
            "excess_label_y": excess_y["label"],
            "excess_cm_label_x": excess_x["cm_label"],
            "excess_cm_label_y": excess_y["cm_label"],
            "ratio_x": row_x["ratio"],
            "ratio_y": row_y["ratio"],
            "cm_source": cm_source,
            "excess_source_x": excess_x["source"],
            "excess_source_y": excess_y["source"],
        })

    write_csv(
        "ed2_drift_envelope.csv",
        [
            "story",
            "elevation_m",
            "drift_x",
            "drift_y",
            "max_drift_x",
            "max_drift_y",
            "excess_x",
            "excess_y",
            "governing_cm_combo_x",
            "governing_cm_combo_y",
            "governing_combo_x",
            "governing_combo_y",
            "governing_excess_combo_x",
            "governing_excess_combo_y",
            "cm_label_x",
            "cm_label_y",
            "label_x",
            "label_y",
            "excess_label_x",
            "excess_label_y",
            "excess_cm_label_x",
            "excess_cm_label_y",
            "ratio_x",
            "ratio_y",
            "cm_source",
            "excess_source_x",
            "excess_source_y",
        ],
        [
            [
                row["story"],
                f"{row['elevation_m']:.3f}",
                f"{row['drift_x']:.8f}",
                f"{row['drift_y']:.8f}",
                f"{row['max_drift_x']:.8f}",
                f"{row['max_drift_y']:.8f}",
                f"{row['excess_x']:.8f}",
                f"{row['excess_y']:.8f}",
                row["governing_cm_combo_x"],
                row["governing_cm_combo_y"],
                row["governing_combo_x"],
                row["governing_combo_y"],
                row["governing_excess_combo_x"],
                row["governing_excess_combo_y"],
                row["cm_label_x"],
                row["cm_label_y"],
                row["label_x"],
                row["label_y"],
                row["excess_label_x"],
                row["excess_label_y"],
                row["excess_cm_label_x"],
                row["excess_cm_label_y"],
                f"{row['ratio_x']:.6f}",
                f"{row['ratio_y']:.6f}",
                row["cm_source"],
                row["excess_source_x"],
                row["excess_source_y"],
            ]
            for row in envelope
        ],
    )

    write_csv(
        "ed2_drift_service_summary.csv",
        [
            "direction",
            "max_avg_drift",
            "max_point_drift",
            "max_excess_drift",
            "governing_story",
            "governing_combo",
            "governing_label",
            "governing_excess_story",
            "governing_excess_combo",
            "governing_excess_label",
            "limit_cm",
            "limit_excess",
            "cm_source",
            "excess_source",
        ],
        [
            [
                "X",
                f"{max((row['drift_x'] for row in envelope), default=0.0):.8f}",
                f"{max((row['max_drift_x'] for row in envelope), default=0.0):.8f}",
                f"{max((row['excess_x'] for row in envelope), default=0.0):.8f}",
                max(envelope, key=lambda item: item["max_drift_x"], default={"story": ""})["story"],
                max(envelope, key=lambda item: item["max_drift_x"], default={"governing_combo_x": ""})["governing_combo_x"],
                max(envelope, key=lambda item: item["max_drift_x"], default={"label_x": ""})["label_x"],
                max(envelope, key=lambda item: item["excess_x"], default={"story": ""})["story"],
                max(envelope, key=lambda item: item["excess_x"], default={"governing_excess_combo_x": ""})["governing_excess_combo_x"],
                max(envelope, key=lambda item: item["excess_x"], default={"excess_label_x": ""})["excess_label_x"],
                f"{DRIFT_LIMITE_CM:.6f}",
                f"{DRIFT_LIMITE_PUNTO:.6f}",
                cm_source,
                "paired_combo_cm"
                if all(row["excess_source_x"] == "paired_combo_cm" for row in envelope)
                else "mixed_fallback",
            ],
            [
                "Y",
                f"{max((row['drift_y'] for row in envelope), default=0.0):.8f}",
                f"{max((row['max_drift_y'] for row in envelope), default=0.0):.8f}",
                f"{max((row['excess_y'] for row in envelope), default=0.0):.8f}",
                max(envelope, key=lambda item: item["max_drift_y"], default={"story": ""})["story"],
                max(envelope, key=lambda item: item["max_drift_y"], default={"governing_combo_y": ""})["governing_combo_y"],
                max(envelope, key=lambda item: item["max_drift_y"], default={"label_y": ""})["label_y"],
                max(envelope, key=lambda item: item["excess_y"], default={"story": ""})["story"],
                max(envelope, key=lambda item: item["excess_y"], default={"governing_excess_combo_y": ""})["governing_excess_combo_y"],
                max(envelope, key=lambda item: item["excess_y"], default={"excess_label_y": ""})["excess_label_y"],
                f"{DRIFT_LIMITE_CM:.6f}",
                f"{DRIFT_LIMITE_PUNTO:.6f}",
                cm_source,
                "paired_combo_cm"
                if all(row["excess_source_y"] == "paired_combo_cm" for row in envelope)
                else "mixed_fallback",
            ],
        ],
    )
    all_excess_paired = all(
        row["excess_source_x"] == "paired_combo_cm" and row["excess_source_y"] == "paired_combo_cm"
        for row in envelope
    )
    return raw_records, envelope, {
        "cm_source": cm_source,
        "excess_source": "paired_combo_cm" if all_excess_paired else "mixed_fallback",
    }


def extract_cm_cr(allow_geometric_cm_fallback: bool = False) -> tuple:
    parsed, meta = extract_cm_cr_rows(
        SapModel,
        allow_geometric_fallback=allow_geometric_cm_fallback,
    )
    if len(parsed) != len(STORY_NAMES):
        raise RuntimeError("CM/CR no contiene exactamente las 5 historias del modelo.")

    write_csv(
        "ed2_cm_cr_per_story.csv",
        ["story", "xcm_m", "ycm_m", "xcr_m", "ycr_m", "ex_m", "ey_m", "source", "cr_available"],
        [
            [
                row["story"],
                f"{row['xcm']:.6f}",
                f"{row['ycm']:.6f}",
                f"{row['xcr']:.6f}",
                f"{row['ycr']:.6f}",
                f"{row['ex']:.6f}",
                f"{row['ey']:.6f}",
                row.get("source", ""),
                str(int(bool(row.get("cr_available", 0)))),
            ]
            for row in parsed
        ],
    )
    return sorted(parsed, key=lambda item: STORY_NAMES.index(item["story"])), meta


def build_summary(modal_rows, base_rows, envelope, drift_meta, story_force_summary, story_force_meta, cm_cr_rows, cm_cr_meta):
    static_seed = read_json("ed2_static_seed.json")
    torsion_application = read_json("ed2_torsion_application.json")
    analysis_run = read_json("ed2_analysis_run.json")
    directional = modal_directional_summary(modal_rows)
    modal_first_three = modal_first_three_summary(modal_rows)
    base_map = {row["case"]: row for row in base_rows}
    w_total = (
        base_map.get("PP", {}).get("Fz", 0.0)
        + base_map.get("TERP", {}).get("Fz", 0.0)
        + base_map.get("TERT", {}).get("Fz", 0.0)
        + 0.25 * base_map.get("SCP", {}).get("Fz", 0.0)
        + 0.25 * base_map.get("SCT", {}).get("Fz", 0.0)
    )
    cmin = calc_Cmin()
    cmax = calc_Cmax()
    cx = clamp(calc_C(float(directional["X"]["period"])), cmin, cmax)
    cy = clamp(calc_C(float(directional["Y"]["period"])), cmin, cmax)
    vdx = cx * I_FACTOR * w_total
    vdy = cy * I_FACTOR * w_total
    max_drift_cm = max([max(row["drift_x"], row["drift_y"]) for row in envelope] or [0.0])
    max_drift_point = max([max(row["max_drift_x"], row["max_drift_y"]) for row in envelope] or [0.0])
    max_drift_excess = max([max(row["excess_x"], row["excess_y"]) for row in envelope] or [0.0])
    total_floor_area = AREA_PLANTA * N_STORIES
    w_per_area = w_total / total_floor_area if total_floor_area > 0 else 0.0
    torsion_methods = []
    for story_data in torsion_application.values():
        for key in ("TEX", "TEY"):
            value = story_data.get(key, {})
            if isinstance(value, dict):
                torsion_methods.append(str(value.get("method", "unknown")))
            else:
                torsion_methods.append(str(value or "unknown"))
    torsion_force_couple_count = sum(1 for method in torsion_methods if method == "force_couple")
    torsion_nodal_fallback_count = sum(1 for method in torsion_methods if method == "nodal_mz_fallback")
    tex_target_mz = sum(
        float(story_data.get("TEX", {}).get("target_mz_tonf_m", 0.0))
        for story_data in torsion_application.values()
        if isinstance(story_data.get("TEX"), dict)
    )
    tey_target_mz = sum(
        float(story_data.get("TEY", {}).get("target_mz_tonf_m", 0.0))
        for story_data in torsion_application.values()
        if isinstance(story_data.get("TEY"), dict)
    )
    cm_cr_real = bool(cm_cr_meta.get("cr_available", False))
    cm_cr_all_within_plan = all(
        0.0 <= row["xcm"] <= LX_PLANTA
        and 0.0 <= row["ycm"] <= LY_PLANTA
        and (not cm_cr_real or 0.0 <= row["xcr"] <= LX_PLANTA)
        and (not cm_cr_real or 0.0 <= row["ycr"] <= LY_PLANTA)
        for row in cm_cr_rows
    )
    cm_cr_no_zero = cm_cr_real and all(
        abs(row["xcr"]) > 1.0e-9 and abs(row["ycr"]) > 1.0e-9
        for row in cm_cr_rows
    )
    summary = {
        "W_total_tonf": round(w_total, 6),
        "W_per_area_tonf_m2": round(w_per_area, 6),
        "Tx_s": round(float(directional["X"]["period"]), 6),
        "Ty_s": round(float(directional["Y"]["period"]), 6),
        "Tz_s": round(float(directional["RZ"]["period"]), 6),
        "Cx": round(cx, 6),
        "Cy": round(cy, 6),
        "Cmin": round(cmin, 6),
        "Cmax": round(cmax, 6),
        "Vdx_tonf": round(vdx, 6),
        "Vdy_tonf": round(vdy, 6),
        "EX_base_Fx_tonf": round(float(base_map.get("EX", {}).get("Fx", 0.0)), 6),
        "EY_base_Fy_tonf": round(float(base_map.get("EY", {}).get("Fy", 0.0)), 6),
        "EX_base_My_tonf_m": round(float(base_map.get("EX", {}).get("My", 0.0)), 6),
        "EY_base_Mx_tonf_m": round(float(base_map.get("EY", {}).get("Mx", 0.0)), 6),
        "TEX_base_Mz_tonf_m": round(float(base_map.get("TEX", {}).get("Mz", 0.0)), 6),
        "TEY_base_Mz_tonf_m": round(float(base_map.get("TEY", {}).get("Mz", 0.0)), 6),
        "TEX_target_Mz_tonf_m": round(tex_target_mz, 6),
        "TEY_target_Mz_tonf_m": round(tey_target_mz, 6),
        "max_drift": round(max_drift_cm, 8),
        "drift_limit": DRIFT_LIMITE_CM,
        "max_drift_cm": round(max_drift_cm, 8),
        "max_drift_point": round(max_drift_point, 8),
        "max_drift_excess": round(max_drift_excess, 8),
        "drift_limit_cm": DRIFT_LIMITE_CM,
        "drift_limit_point": DRIFT_LIMITE_PUNTO,
        "H_total_m": H_TOTAL,
        "story_weight_source": static_seed.get("story_weight_source", {}).get("source", "unknown"),
        "story_weight_file": static_seed.get("story_weight_file", ""),
        "drift_cm_source": drift_meta.get("cm_source", "unknown"),
        "drift_excess_source": drift_meta.get("excess_source", "unknown"),
        "cm_cr_source": cm_cr_meta.get("source", "unknown"),
        "cm_cr_real": cm_cr_real,
        "first_three_modes_ok": modal_first_three["covers_xyz"],
        "first_three_modes": modal_first_three["first_three"],
        "torsion_force_couple_count": torsion_force_couple_count,
        "torsion_nodal_fallback_count": torsion_nodal_fallback_count,
        "torsion_all_force_couple": bool(torsion_methods) and torsion_nodal_fallback_count == 0,
        "cm_cr_story_count": len(cm_cr_rows),
        "cm_cr_all_within_plan": cm_cr_all_within_plan,
        "cm_cr_no_zero": cm_cr_no_zero,
        "story_forces_source": story_force_meta.get("source", "unknown"),
        "story_forces_story_count_ex": sum(1 for row in story_force_summary if row["case"] == "EX"),
        "story_forces_story_count_ey": sum(1 for row in story_force_summary if row["case"] == "EY"),
        "etabs_expected_major": analysis_run.get("etabs_runtime", {}).get("expected_major", 0),
        "etabs_detected_major": analysis_run.get("etabs_runtime", {}).get("detected_major", 0),
        "etabs_detected_version": analysis_run.get("etabs_runtime", {}).get("detected_version", "unknown"),
        "etabs_strict_ret_mode": analysis_run.get("etabs_runtime", {}).get("strict_ret_mode", False),
        "analysis_return_code": analysis_run.get("analysis_return_code", None),
    }
    export_summary_csv(summary)
    write_json("ed2_summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-summary", action="store_true")
    parser.add_argument(
        "--allow-geometric-cm-fallback",
        action="store_true",
        help="Permite CM=centro geometrico solo para precheck no oficial.",
    )
    parser.add_argument(
        "--allow-theoretical-story-forces-fallback",
        action="store_true",
        help="Permite Story Forces desde distribucion estatica solo para precheck no oficial.",
    )
    args = parser.parse_args()
    allow_geometric_cm_fallback = args.allow_geometric_cm_fallback or env_flag(
        ENV_ALLOW_GEOMETRIC_CM_FALLBACK,
        False,
    )
    allow_theoretical_story_forces_fallback = args.allow_theoretical_story_forces_fallback or env_flag(
        ENV_ALLOW_THEORETICAL_STORY_FORCES_FALLBACK,
        False,
    )

    missing_seeds = [
        name
        for name in ["ed2_modal_seed.json", "ed2_static_seed.json", "ed2_static_distribution.csv"]
        if not os.path.exists(os.path.join(RESULTS_DIR, name))
    ]
    if missing_seeds:
        log.error("Faltan semillas oficiales previas: " + ", ".join(missing_seeds))
        log.error("Ejecuta 08_seismic_ed2.py y 09_torsion_ed2.py antes de extraer resultados.")
        return 1

    global SapModel
    SapModel = None
    try:
        log.info("=" * 72)
        log.info("ED2 PARTE 1 - EXTRACCION OFICIAL")
        log.info("=" * 72)
        SapModel = connect()
        set_units(SapModel, UNITS_TONF_M_C)

        modal_rows = extract_modal()
        base_rows = extract_base_reactions()
        story_force_summary, story_force_meta = extract_story_forces(
            allow_theoretical_fallback=allow_theoretical_story_forces_fallback
        )
        _, envelope, drift_meta = extract_story_drifts(
            allow_geometric_cm_fallback=allow_geometric_cm_fallback
        )
        cm_cr_rows, cm_cr_meta = extract_cm_cr(
            allow_geometric_cm_fallback=allow_geometric_cm_fallback
        )
        summary = build_summary(
            modal_rows,
            base_rows,
            envelope,
            drift_meta,
            story_force_summary,
            story_force_meta,
            cm_cr_rows,
            cm_cr_meta,
        )

        if not args.no_summary:
            log.info(
                f"Summary: W={summary['W_total_tonf']:.2f} tonf, "
                f"Tx={summary['Tx_s']:.4f}s, "
                f"Ty={summary['Ty_s']:.4f}s, "
                f"DriftMax={summary['max_drift']:.6f}"
            )

        log.info("Official extraction completed")
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
