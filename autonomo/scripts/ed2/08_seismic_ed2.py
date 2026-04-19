"""
08_seismic_ed2.py - Base sismica oficial Ed.2 Parte 1.

Flujo oficial:
1. Configurar Mass Source del taller
2. Configurar caso modal "Modal"
3. Ejecutar analisis modal
4. Extraer T*, Ty*, Tz* desde ETABS
5. Guardar semilla documental para el metodo estatico oficial

No define response spectrum ni casos dinamicos. En Ed.2 Parte 1 el caso
modal solo apoya la determinacion de periodos.
"""

import os
import sys
import time
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    MASS_SOURCE_PATTERNS,
    MODELS_DIR,
    UNITS_TONF_M_C,
    check_ret,
    connect,
    disconnect,
    log,
    set_units,
)
from ed2_static_official import (
    MODAL_CASE,
    compute_story_weights_analytic,
    extract_story_weights_from_db,
    export_story_weights,
    extract_modal_rows_from_db,
    modal_directional_summary,
    write_csv,
    write_json,
)


MODAL_MAX_MODES = 15
MODAL_MIN_MODES = 1
MODAL_EIGEN_SHIFT = 0.0
MODAL_EIGEN_CUTOFF = 0.0
MODAL_EIGEN_TOL = 1.0e-9
MODAL_AUTO_SHIFT = 1


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
    filepath = os.path.join(MODELS_DIR, "Edificio2_parte1_oficial.edb")
    ret = SapModel.File.Save(filepath)
    check_ret(ret, f"File.Save('{filepath}')")
    return filepath


def configure_mass_source(SapModel) -> None:
    log.info("Step 1: Configuring official Mass Source...")
    load_patterns = list(MASS_SOURCE_PATTERNS.keys())
    scale_factors = list(MASS_SOURCE_PATTERNS.values())

    if "PP" in load_patterns:
        idx = load_patterns.index("PP")
        load_patterns.pop(idx)
        scale_factors.pop(idx)

    ret = SapModel.PropMaterial.SetMassSource_1(
        True,
        False,
        True,
        len(load_patterns),
        load_patterns,
        scale_factors,
    )
    check_ret(ret, "PropMaterial.SetMassSource_1")
    log.info("  Mass Source OK")


def configure_modal_case(SapModel) -> None:
    log.info("Step 2: Configuring modal case...")
    ret = SapModel.LoadCases.ModalEigen.SetCase(MODAL_CASE)
    check_ret(ret, f"ModalEigen.SetCase('{MODAL_CASE}')")

    ret = SapModel.LoadCases.ModalEigen.SetNumberModes(
        MODAL_CASE, MODAL_MAX_MODES, MODAL_MIN_MODES
    )
    check_ret(ret, "ModalEigen.SetNumberModes")

    ret = SapModel.LoadCases.ModalEigen.SetParameters(
        MODAL_CASE,
        MODAL_EIGEN_SHIFT,
        MODAL_EIGEN_CUTOFF,
        MODAL_EIGEN_TOL,
        MODAL_AUTO_SHIFT,
    )
    check_ret(ret, "ModalEigen.SetParameters")

    try:
        ret = SapModel.LoadCases.ModalEigen.SetInitialCase(MODAL_CASE, "")
        check_ret(ret, "ModalEigen.SetInitialCase")
    except Exception:
        pass

    try:
        SapModel.Analyze.SetRunCaseFlag("", False, True)
    except Exception:
        pass
    try:
        SapModel.Analyze.SetRunCaseFlag(MODAL_CASE, True, False)
    except Exception:
        pass
    log.info("  Modal case OK")


def run_modal_analysis(SapModel) -> None:
    log.info("Step 3: Running modal analysis...")
    filepath = ensure_model_path(SapModel)
    log.info(f"  Model file: {filepath}")
    try:
        SapModel.SetModelIsLocked(False)
    except Exception:
        pass
    ret = SapModel.Analyze.RunAnalysis()
    check_ret(ret, "Analyze.RunAnalysis")
    time.sleep(1)
    log.info("  Modal analysis completed")


def export_modal_seed(SapModel) -> None:
    log.info("Step 4: Extracting modal seed...")
    modal_rows = extract_modal_rows_from_db(SapModel)
    if not modal_rows:
        raise RuntimeError(
            "No se pudieron extraer periodos modales desde ETABS. "
            "El metodo estatico oficial requiere T*, Ty* y Tz* reales."
        )

    write_csv(
        "ed2_modal_results.csv",
        ["Mode", "Period", "UX", "UY", "RZ", "SumUX", "SumUY"],
        [
            [
                row["Mode"],
                row["Period"],
                row["UX"],
                row["UY"],
                row["RZ"],
                row["SumUX"],
                row["SumUY"],
            ]
            for row in modal_rows
        ],
    )

    directional = modal_directional_summary(modal_rows)
    payload = {
        "modal_case": MODAL_CASE,
        "directional_periods": directional,
    }
    write_json("ed2_modal_seed.json", payload)
    log.info(
        "  Periods: "
        f"Tx={directional['X']['period']:.4f}s, "
        f"Ty={directional['Y']['period']:.4f}s, "
        f"Tz={directional['RZ']['period']:.4f}s"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-analytic-fallback",
        action="store_true",
        help="Permite pesos analiticos solo para precheck no oficial.",
    )
    args = parser.parse_args()
    SapModel = None
    try:
        log.info("=" * 72)
        log.info("ED2 PARTE 1 - BASE SISMICA OFICIAL (MODAL AUXILIAR)")
        log.info("=" * 72)
        SapModel = connect()
        set_units(SapModel, UNITS_TONF_M_C)

        configure_mass_source(SapModel)
        configure_modal_case(SapModel)
        run_modal_analysis(SapModel)
        export_modal_seed(SapModel)

        real_story_weights = extract_story_weights_from_db(SapModel)
        if real_story_weights:
            export_story_weights(real_story_weights)
            write_json(
                "ed2_story_weights_source.json",
                {
                    "source": "etabs_table",
                    "table": real_story_weights[0]["source_table"],
                    "field": real_story_weights[0]["source_field"],
                },
            )
            log.info(f"  Story weights source: {real_story_weights[0]['source_table']}")
        else:
            if not args.allow_analytic_fallback:
                raise RuntimeError(
                    "ETABS no expuso 'Mass Summary by Story'/'Story Mass Summary'. "
                    "El flujo oficial exige pesos reales por piso. "
                    "Usa --allow-analytic-fallback solo para precheck no oficial."
                )
            export_story_weights(compute_story_weights_analytic())
            write_json(
                "ed2_story_weights_source.json",
                {
                    "source": "analytic_fallback",
                    "table": "",
                    "field": "",
                    "mode": "precheck_only",
                },
            )
            log.warning("  Story weights source: analytic fallback (ETABS table unavailable)")

        log.info("")
        log.info("Ready for step 09: static seismic cases EX/EY/TEX/TEY")
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
