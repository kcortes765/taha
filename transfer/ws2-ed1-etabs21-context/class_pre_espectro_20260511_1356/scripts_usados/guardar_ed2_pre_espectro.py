from __future__ import annotations

import json
import os
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
CLASS_ROOT = THIS.parents[1]
HECRAS2 = CLASS_ROOT.parents[1]
ED2_WORKBENCH = HECRAS2 / "prog2" / "Edif2" / "workbench" / "ed2_pipeline_active"

sys.path.insert(0, str(ED2_WORKBENCH))

TARGET = CLASS_ROOT / "Edificio_2" / "models" / "ED2_CLASE_PRE_ESPECTRO_20260511.EDB"
REPORT = CLASS_ROOT / "Edificio_2" / "reports" / "ED2_CLASE_PRE_ESPECTRO_20260511.md"
JSON_REPORT = CLASS_ROOT / "Edificio_2" / "reports" / "ED2_CLASE_PRE_ESPECTRO_20260511.json"


def get_names(obj) -> list[str]:
    try:
        result = obj.GetNameList()
    except Exception:
        return []
    names: list[str] = []
    if isinstance(result, (tuple, list)):
        for item in result:
            if isinstance(item, (tuple, list)):
                names.extend(str(value) for value in item)
    return names


def current_model(sap) -> str:
    for call in (
        lambda: sap.GetModelFilename(),
        lambda: sap.GetModelFilepath(),
    ):
        try:
            value = call()
            if isinstance(value, (tuple, list)):
                value = value[0]
            return str(value or "")
        except Exception:
            pass
    return ""


def main() -> int:
    from config_ed2 import UNITS_TONF_M_C, connect, disconnect, set_units

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    sap = connect(create_if_missing=False)
    try:
        set_units(sap, UNITS_TONF_M_C)
        before = current_model(sap)
        load_patterns = get_names(sap.LoadPatterns)
        load_cases = get_names(sap.LoadCases)
        combos = get_names(sap.RespCombo)
        forbidden = ["EX", "EY", "TEX", "TEY", "TEX_WS2", "TEY_WS2"]
        forbidden_present = [
            name
            for name in forbidden
            if name in set(load_patterns) or name in set(load_cases) or name in set(combos)
        ]
        if forbidden_present:
            raise RuntimeError(f"El modelo ya contiene cargas/casos sísmicos estáticos: {forbidden_present}")

        ret = sap.File.Save(str(TARGET))
        payload = {
            "active_model_before_save": before,
            "target": str(TARGET),
            "save_ret": ret,
            "load_patterns": load_patterns,
            "load_cases": load_cases,
            "response_combos": combos,
            "forbidden_static_seismic_items_present": forbidden_present,
            "intended_stop": "después de masa/modal auxiliar y antes de EX/EY/TEX/TEY",
        }
        JSON_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

        modal_seed = CLASS_ROOT / "Edificio_2" / "results" / "ed2_modal_seed.json"
        modal_text = ""
        if modal_seed.exists():
            modal_text = modal_seed.read_text(encoding="utf-8")

        lines = [
            "# ED2 clase - modelo previo a cargas sísmicas estáticas",
            "",
            f"- Modelo generado: `{TARGET}`",
            f"- Modelo activo al guardar: `{before}`",
            "- Estado: geometría, materiales, secciones, columnas, vigas, losas, diafragma, apoyos, cargas gravitacionales, fuente de masa y modal auxiliar listos.",
            "- Corte exacto: no se aplicaron casos sísmicos estáticos `EX/EY` ni torsión `TEX/TEY`.",
            "",
            "## Resumen verificado",
            "",
            f"- Patrones de carga: `{', '.join(load_patterns)}`",
            f"- Casos de carga: `{', '.join(load_cases)}`",
            f"- Combinaciones: `{', '.join(combos) if combos else 'sin combinaciones agregadas por este script'}`",
            "",
            "## Modal auxiliar",
            "",
            "```json",
            modal_text.strip() if modal_text else "ed2_modal_seed.json no encontrado",
            "```",
            "",
            "## Uso en clase",
            "",
            "Desde este modelo corresponde seguir con el método estático: cálculo/aplicación de `EX/EY`, torsión accidental `TEX/TEY`, combinaciones, análisis y extracción de resultados.",
        ]
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0
    finally:
        disconnect(False)


if __name__ == "__main__":
    raise SystemExit(main())
