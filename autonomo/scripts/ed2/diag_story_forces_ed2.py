r"""
diag_story_forces_ed2.py - Diagnostico crudo de tablas de fuerzas por historia.

Uso en WS:
    python diag_story_forces_ed2.py --model C:\Users\Civil\Documents\taha\models\Edificio2_parte1_oficial.edb

Genera en results/:
    - ed2_story_forces_probe.json

No modifica el modelo. Solo inspecciona tablas candidatas para EX/EY.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import connect, disconnect, log, set_units, UNITS_TONF_M_C, get_runtime_etabs_info
from ed2_static_official import find_table_candidates, list_available_tables, select_cases_for_output


def stringify(value):
    if isinstance(value, (list, tuple)):
        return [stringify(item) for item in value]
    if value is None:
        return None
    try:
        return str(value)
    except Exception:
        return repr(value)


def current_model_path(sap_model) -> str:
    try:
        filepath = sap_model.GetModelFilename()
        if isinstance(filepath, (tuple, list)):
            filepath = filepath[0]
        return str(filepath or "")
    except Exception:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="", help="Ruta .edb a abrir si hace falta")
    args = parser.parse_args()

    sap_model = None
    try:
        sap_model = connect(model_path=args.model or None, force_open_model=bool(args.model))
        set_units(sap_model, UNITS_TONF_M_C)
        select_cases_for_output(sap_model, ["EX", "EY"])

        exact_names = [
            "Story Forces",
            "Story Shears",
            "Story Force Output",
            "Story Response",
        ]
        table_candidates = find_table_candidates(
            sap_model,
            exact_names=exact_names,
            keyword_groups=[
                ["story", "force"],
                ["story", "forces"],
                ["story", "shear"],
                ["story", "shears"],
            ],
        )

        available_tables = list_available_tables(sap_model)
        filtered_available = []
        for table in available_tables:
            hay = f"{table.get('key', '')} {table.get('name', '')}".lower()
            if "story" in hay and ("force" in hay or "shear" in hay):
                filtered_available.append(table)

        payload = {
            "current_model": current_model_path(sap_model),
            "etabs_runtime": get_runtime_etabs_info(),
            "selected_cases": ["EX", "EY"],
            "available_story_force_tables": filtered_available,
            "table_candidates": table_candidates,
            "raw_results": {},
        }

        for table_name in table_candidates:
            table_payload = {"table": table_name, "attempts": []}
            for group_name in ["All", "", None]:
                label = "None" if group_name is None else group_name
                try:
                    result = sap_model.DatabaseTables.GetTableForDisplayArray(
                        table_name,
                        "",
                        group_name if group_name is not None else "",
                        1,
                        [],
                        0,
                        [],
                    )
                    converted = stringify(result)
                    fields = []
                    sample_rows = []
                    if isinstance(result, (tuple, list)) and len(result) >= 5:
                        try:
                            fields = stringify(result[2]) or []
                        except Exception:
                            fields = []
                        try:
                            raw_data = list(result[4]) if isinstance(result[4], (tuple, list)) else []
                            n_fields = len(fields)
                            if n_fields > 0:
                                for offset in range(0, min(len(raw_data), n_fields * 5), n_fields):
                                    chunk = raw_data[offset : offset + n_fields]
                                    if len(chunk) == n_fields:
                                        sample_rows.append(
                                            {str(fields[i]): stringify(chunk[i]) for i in range(n_fields)}
                                        )
                        except Exception:
                            sample_rows = []

                    table_payload["attempts"].append(
                        {
                            "group": label,
                            "result_type": type(result).__name__,
                            "result_len": len(result) if isinstance(result, (tuple, list)) else None,
                            "fields": fields,
                            "sample_rows": sample_rows,
                            "result": converted,
                        }
                    )
                except Exception as exc:
                    table_payload["attempts"].append(
                        {
                            "group": label,
                            "error": repr(exc),
                        }
                    )
            payload["raw_results"][table_name] = table_payload

        out_path = os.path.join(os.path.dirname(__file__), "results", "ed2_story_forces_probe.json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)

        log.info(f"Story forces probe written: {out_path}")
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
