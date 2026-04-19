r"""
diag_story_cm_ed2.py - Sonda cruda para centro de masa por historia en ETABS 21.

Uso en WS:
    python diag_story_cm_ed2.py --model C:\Users\Civil\Documents\taha\models\Edificio2_parte1_oficial.edb

Genera en results/:
    - ed2_story_cm_probe.json

No modifica el modelo. Solo inspecciona:
    - tablas CM/CR disponibles
    - joints del modelo y su mapeo por historia
    - respuestas crudas de Results.AssembledJointMass(...)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    RESULTS_DIR,
    STORY_ELEVATIONS,
    STORY_NAMES,
    UNITS_TONF_M_C,
    connect,
    disconnect,
    log,
    set_units,
)
from ed2_static_official import (
    _extract_story_cm_from_assembled_joint_masses,
    _extract_story_cm_from_table,
    collect_joint_lookup,
    find_table_candidates,
    list_available_tables,
    parse_db_table,
)


def stringify(value):
    if isinstance(value, (list, tuple)):
        return [stringify(item) for item in value]
    if value is None:
        return None
    try:
        return str(value)
    except Exception:
        return repr(value)


def story_from_z(z_value: float, tol: float = 0.05) -> str:
    for story_name, elevation in zip(STORY_NAMES, STORY_ELEVATIONS):
        if abs(z_value - elevation) <= tol:
            return story_name
    return ""


def probe_assembled_joint_mass(sap_model, item_name: str, item_type: int):
    try:
        result = sap_model.Results.AssembledJointMass(
            item_name,
            item_type,
            0,
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        )
        return {
            "item_name": item_name,
            "item_type": item_type,
            "result_type": type(result).__name__,
            "result_len": len(result) if isinstance(result, (tuple, list)) else None,
            "result": stringify(result),
        }
    except Exception as exc:
        return {
            "item_name": item_name,
            "item_type": item_type,
            "error": repr(exc),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="", help="Ruta .edb a abrir si hace falta")
    args = parser.parse_args()

    sap_model = None
    try:
        sap_model = connect(model_path=args.model or None, force_open_model=bool(args.model))
        set_units(sap_model, UNITS_TONF_M_C)

        payload = {
            "current_model": "",
            "available_tables_filtered": [],
            "cm_table_candidates": [],
            "cm_table_rows": {},
            "point_objects": {},
            "joint_lookup": {},
            "assembled_joint_mass": {},
            "cm_from_table": {},
            "cm_from_assembled_joint_masses": {},
        }

        try:
            current_model = sap_model.GetModelFilename()
            if isinstance(current_model, (tuple, list)):
                current_model = current_model[0]
            payload["current_model"] = str(current_model or "")
        except Exception as exc:
            payload["current_model_error"] = repr(exc)

        available_tables = list_available_tables(sap_model)
        payload["available_tables_filtered"] = [
            table
            for table in available_tables
            if any(
                token in (table.get("key", "") + " " + table.get("name", "")).lower()
                for token in ["mass", "story", "joint", "center", "rigid"]
            )
        ]

        cm_table_candidates = find_table_candidates(
            sap_model,
            exact_names=[
                "Centers Of Mass And Rigidity",
                "Center Of Mass And Rigidity",
                "Centers of Mass and Rigidity",
            ],
            keyword_groups=[
                ["center", "mass", "rigid"],
                ["mass", "rigid"],
                ["center", "rigidity"],
            ],
        )
        payload["cm_table_candidates"] = cm_table_candidates
        for table_name in cm_table_candidates:
            fields, rows = parse_db_table(sap_model, table_name)
            payload["cm_table_rows"][table_name] = {
                "fields": fields or [],
                "row_count": len(rows or []),
                "sample_rows": (rows or [])[:10],
            }

        point_names = []
        try:
            point_result = sap_model.PointObj.GetNameList()
            point_names = [
                str(name).strip()
                for name in (point_result[1] if isinstance(point_result, (tuple, list)) and len(point_result) >= 2 else [])
                if str(name).strip()
            ]
        except Exception as exc:
            payload["point_objects"]["error"] = repr(exc)

        point_samples = []
        per_story_counts = defaultdict(int)
        for point_name in point_names:
            try:
                coord = sap_model.PointObj.GetCoordCartesian(point_name)
                x = float(coord[0])
                y = float(coord[1])
                z = float(coord[2])
            except Exception:
                continue
            story = story_from_z(z)
            if story:
                per_story_counts[story] += 1
            if len(point_samples) < 20:
                point_samples.append(
                    {
                        "name": point_name,
                        "x": x,
                        "y": y,
                        "z": z,
                        "story": story,
                    }
                )
        payload["point_objects"]["count"] = len(point_names)
        payload["point_objects"]["per_story_counts"] = dict(per_story_counts)
        payload["point_objects"]["sample"] = point_samples

        joint_lookup = collect_joint_lookup(sap_model)
        lookup_story_counts = defaultdict(int)
        lookup_sample = []
        for alias, item in joint_lookup.items():
            story = str(item.get("story", "")).strip()
            if story:
                lookup_story_counts[story] += 1
            if len(lookup_sample) < 20:
                lookup_sample.append(
                    {
                        "alias": alias,
                        "name": item.get("name", ""),
                        "x": item.get("x", 0.0),
                        "y": item.get("y", 0.0),
                        "z": item.get("z", 0.0),
                        "story": story,
                    }
                )
        payload["joint_lookup"]["count"] = len(joint_lookup)
        payload["joint_lookup"]["per_story_counts"] = dict(lookup_story_counts)
        payload["joint_lookup"]["sample"] = lookup_sample

        payload["assembled_joint_mass"]["all_item_types"] = [
            probe_assembled_joint_mass(sap_model, "ALL", item_type)
            for item_type in [0, 1, 2, 3]
        ]

        sample_points = []
        for point_name in point_names:
            point_meta = joint_lookup.get("".join(ch for ch in point_name.lower() if ch.isalnum()), {})
            if str(point_meta.get("story", "")).strip() in STORY_NAMES:
                sample_points.append(point_name)
            if len(sample_points) >= 10:
                break

        payload["assembled_joint_mass"]["per_point_item0"] = [
            probe_assembled_joint_mass(sap_model, point_name, 0)
            for point_name in sample_points
        ]

        payload["cm_from_table"] = _extract_story_cm_from_table(sap_model)
        payload["cm_from_assembled_joint_masses"] = _extract_story_cm_from_assembled_joint_masses(sap_model)

        os.makedirs(RESULTS_DIR, exist_ok=True)
        out_path = os.path.join(RESULTS_DIR, "ed2_story_cm_probe.json")
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)

        log.info(f"Story CM probe written: {out_path}")
        return 0
    except Exception as exc:
        log.error(f"[FATAL] {exc}")
        return 1
    finally:
        if sap_model is not None:
            try:
                disconnect(False)
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
