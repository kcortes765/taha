from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
CLASS_ROOT = THIS.parents[1]
HECRAS2 = CLASS_ROOT.parents[1]
PROG2 = HECRAS2 / "prog2"
ED1_WORKBENCH = PROG2 / "Edif1" / "workbench"
COMMON = PROG2 / "_common"

sys.path.insert(0, str(ED1_WORKBENCH))
sys.path.insert(0, str(COMMON))

SOURCE = HECRAS2 / "prog" / "Edif1" / "ED1_PARTE1_COMPLETA_TRABAJO.EDB"
TARGET = CLASS_ROOT / "Edificio_1" / "models" / "ED1_CLASE_PRE_ESPECTRO_20260511.EDB"
REPORT = CLASS_ROOT / "Edificio_1" / "reports" / "ED1_CLASE_PRE_ESPECTRO_20260511.md"
JSON_REPORT = CLASS_ROOT / "Edificio_1" / "reports" / "ED1_CLASE_PRE_ESPECTRO_20260511.json"
LOG = CLASS_ROOT / "Edificio_1" / "reports" / "ED1_CLASE_PRE_ESPECTRO_20260511.log"


def names_from(obj) -> list[str]:
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


def main() -> int:
    if not SOURCE.exists():
        raise FileNotFoundError(str(SOURCE))
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE, TARGET)

    os.environ["ED1_ETABS_MODEL_PATH"] = str(TARGET)

    from ed1_part1_prog2 import (  # noqa: E402
        RunLog,
        assign_diaphragm_and_supports,
        collect_basic_audit,
        configure_mass_and_modal,
        define_patterns_and_loads,
        set_units,
    )
    from ws2_etabs_oapi import connect_etabs21  # noqa: E402

    log = RunLog(LOG)
    session = None
    payload: dict[str, object] = {
        "source": str(SOURCE),
        "target": str(TARGET),
        "intended_stop": "antes de definir funcion/casos de espectro",
    }
    try:
        session = connect_etabs21(TARGET, log, allow_start=True, wait_after_start=20)
        sap = session.sap_model
        set_units(sap)

        payload["audit_before"] = collect_basic_audit(sap, log)
        payload["diaphragm_supports"] = assign_diaphragm_and_supports(sap, log)
        payload["load_assignments"] = define_patterns_and_loads(sap, log)
        payload["mass_modal"] = configure_mass_and_modal(sap, log)

        load_cases = names_from(sap.LoadCases)
        combos = names_from(sap.RespCombo)
        load_patterns = names_from(sap.LoadPatterns)
        payload["load_patterns"] = load_patterns
        payload["load_cases"] = load_cases
        payload["response_combos"] = combos
        payload["audit_after"] = collect_basic_audit(sap, log)

        forbidden = [
            "SEx",
            "SEy",
            "SEx_b2",
            "SEy_b2",
            "ED1_DYN_XP",
            "ED1_DYN_XN",
            "ED1_DYN_YP",
            "ED1_DYN_YN",
        ]
        present_forbidden = [
            name for name in forbidden if name in set(load_cases) or name in set(combos)
        ]
        payload["forbidden_spectrum_or_dynamic_items_present"] = present_forbidden
        if present_forbidden:
            raise RuntimeError(f"Modelo no quedo pre-espectro; elementos presentes: {present_forbidden}")

        save_ret = sap.File.Save(str(TARGET))
        payload["save_ret"] = save_ret
        JSON_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

        lines = [
            "# ED1 clase - modelo previo al espectro",
            "",
            f"- Fuente: `{SOURCE}`",
            f"- Modelo generado: `{TARGET}`",
            "- Estado: geometría, apoyos, diafragma, cargas gravitacionales, fuente de masa y modal listos.",
            "- Corte exacto: no se definieron función de espectro, casos `SEx/SEy/SEx_b2/SEy_b2`, torsión accidental ni combinaciones dinámicas.",
            "",
            "## Resumen verificado",
            "",
            f"- Cargas asignadas: `{payload['load_assignments']}`",
            f"- Masa/modal: `{payload['mass_modal']}`",
            f"- Patrones de carga: `{', '.join(load_patterns)}`",
            f"- Casos de carga: `{', '.join(load_cases)}`",
            f"- Combinaciones: `{', '.join(combos) if combos else 'sin combinaciones agregadas por este script'}`",
            "",
            "## Uso en clase",
            "",
            "Desde este modelo corresponde seguir con la definición del espectro NCh433:2026, casos espectrales y lo posterior.",
        ]
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        log.write(f"REPORT {REPORT}")
        return 0
    finally:
        if session is not None:
            session.close_if_started(save=False)


if __name__ == "__main__":
    raise SystemExit(main())
