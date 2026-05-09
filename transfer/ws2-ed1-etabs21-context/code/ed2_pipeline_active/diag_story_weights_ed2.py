r"""
diag_story_weights_ed2.py - Diagnostico crudo de tablas de masa/peso por historia.

Uso en WS:
    python diag_story_weights_ed2.py --model C:\Users\Civil\Documents\taha\models\Edificio2_parte1_oficial.edb

Genera en results/:
    - ed2_story_weight_probe.json

No modifica el modelo. Solo inspecciona las tablas candidatas.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import connect, disconnect, log, set_units, UNITS_TONF_M_C
from ed2_static_official import find_table_candidates, list_available_tables


def stringify(value):
    if isinstance(value, (list, tuple)):
        return [stringify(item) for item in value]
    if value is None:
        return None
    try:
        return str(value)
    except Exception:
        return repr(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="", help="Ruta .edb a abrir si hace falta")
    args = parser.parse_args()

    sap_model = None
    try:
        sap_model = connect(model_path=args.model or None, force_open_model=bool(args.model))
        set_units(sap_model, UNITS_TONF_M_C)

        exact_names = [
            "Mass Summary by Story",
            "Story Mass Summary",
            "Mass Summary By Story",
            "Story Masses",
            "Masses by Story",
        ]
        table_candidates = find_table_candidates(
            sap_model,
            exact_names=exact_names,
            keyword_groups=[
                ["mass", "story"],
                ["mass", "summary", "story"],
                ["story", "mass", "summary"],
                ["story", "masses"],
            ],
        )

        payload = {
            "available_tables": list_available_tables(sap_model),
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
                    table_payload["attempts"].append(
                        {
                            "group": label,
                            "result_type": type(result).__name__,
                            "result_len": len(result) if isinstance(result, (tuple, list)) else None,
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

        out_path = os.path.join(os.path.dirname(__file__), "results", "ed2_story_weight_probe.json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)

        log.info(f"Story weight probe written: {out_path}")
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
