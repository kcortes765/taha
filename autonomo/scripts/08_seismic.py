"""
08_seismic.py — Complete seismic configuration for Edificio 1.

This script handles all seismic analysis setup in four steps:
  1. Mass Source: elements + TERP×1.0 + SCP×0.25  (NCh433)
  2. Response Spectrum Function: load from espectro_elastico_Z3SC.txt via SetUser
     (SetFromFile does NOT exist in ETABS — confirmed in R03)
  3. Modal Case: Eigen, 30 modes, convergence 1E-9
  4. Spectrum Load Cases: SDX (U1) and SDY (U2)
     - Function: Esp_Elastico_Z3SC, SF=9.81 (Sa/g → m/s²)
     - Modal combination: CQC (ETABS default)
     - Directional combination: SRSS (ETABS default)

Mass Source rationale (NCh433 Art. 5.4.3 + DS61):
  Seismic mass = dead loads (PP, elements) + TERP + 25% live load (SCP).
  PP is captured via IncludeElements=True (SWM=1 in load pattern).
  TERP at 100% because it's permanent (super dead).
  SCP at 25% for office buildings per Chilean practice.

Spectrum function (NCh433 + DS61):
  Sa/g values precomputed by calc_espectro.py for Zona 3, Suelo C.
  The file format is tab-separated: T[s] \t Sa/g
  101 points from T=0.0 to T=5.0 (Δt=0.05s).
  Values are Sa/g (dimensionless) — SF=9.81 converts to m/s².

Modal case:
  30 modes ensures >90% mass participation in both directions for a
  20-story shear wall building. Convergence tolerance 1E-9 (stricter
  than default 1E-7) for better accuracy.

Prerequisites:
  - ETABS v19 open with model from scripts 01-07
  - comtypes installed
  - config.py in the same directory
  - espectro_elastico_Z3SC.txt in the same directory

Usage:
  python 08_seismic.py

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against:
  - autonomo/research/com_signatures.md §10-§12
  - autonomo/research/etabs_api_reference.md §14-§17
  - CSI OAPI official documentation (docs.csiamerica.com)
  - FuncRS.SetUser: §10.1 (5 args)
  - FuncRS.SetFromFile: §10.2 — DOES NOT EXIST IN ETABS
  - ResponseSpectrum.SetCase: §11.1 (1 arg)
  - ResponseSpectrum.SetLoads: §11.2 (7 args)
  - ResponseSpectrum.SetModalCase: §11.3 (2 args)
  - PropMaterial.SetMassSource_1: §12.1 (6 args, in PropMaterial NOT MassSource)
  - LoadCases.ModalEigen.SetCase: confirmed via CSI docs (1 arg)
  - LoadCases.ModalEigen.SetNumberModes: confirmed (3 args)
  - LoadCases.ModalEigen.SetParameters: confirmed (5 args)
Sources: NCh433 Mod 2009, DS61, Lafontaine tutorial, Material Apoyo Taller 2026
"""

import sys
import os
import time

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
    # Seismic parameters
    SPECTRUM_FILE, SPECTRUM_DAMPING, SPECTRUM_SF,
    MASS_SOURCE_PATTERNS,
    G_ACCEL,
)

# ===================================================================
# CONSTANTS
# ===================================================================

# Spectrum function name in ETABS (used by spectrum load cases)
SPECTRUM_FUNC_NAME = "Esp_Elastico_Z3SC"

# Modal case name
MODAL_CASE_NAME = "Modal"

# Spectrum load case names
SDX_CASE_NAME = "SDX"
SDY_CASE_NAME = "SDY"

# Modal analysis parameters
MODAL_MAX_MODES = 30     # 30 modes for 20-story building
MODAL_MIN_MODES = 1      # Minimum 1 mode
MODAL_EIGEN_SHIFT = 0.0  # No frequency shift [cyc/s]
MODAL_EIGEN_CUTOFF = 0.0 # No frequency cutoff [cyc/s]
MODAL_EIGEN_TOL = 1.0E-9 # Convergence tolerance (stricter than default 1E-7)
MODAL_AUTO_SHIFT = 1     # Allow automatic frequency shifting


# ===================================================================
# STEP 1: Configure Mass Source
# ===================================================================

def configure_mass_source(SapModel):
    """Configure seismic mass source: elements + TERP×1.0 + SCP×0.25.

    NCh433 Art. 5.4.3: Seismic weight = dead load + fraction of live load.
    For office buildings (Cat. II): 25% of live load.

    Mass composition:
      - Element self-weight (PP with SWM=1): captured by IncludeElements=True
      - TERP × 1.0: permanent superimposed dead load (floor finishes)
      - SCP  × 0.25: 25% of office live load

    Firma COM (com_signatures.md §12.1):
      ret = SapModel.PropMaterial.SetMassSource_1(
          IncludeElements, IncludeAddedMass, IncludeLoads,
          NumberLoads, LoadPat[], SF[]
      )

    CRITICAL: Function is in PropMaterial, NOT in MassSource.
    This is confirmed by CSI API 2015/2016 documentation.
    """
    log.info("Step 1: Configuring Mass Source...")

    # Build arrays from config
    load_patterns = list(MASS_SOURCE_PATTERNS.keys())
    scale_factors = list(MASS_SOURCE_PATTERNS.values())
    n_loads = len(load_patterns)

    # Remove PP from the list — it's captured by IncludeElements=True
    # PP has SWM=1 → ETABS auto-includes element self-weight
    if 'PP' in load_patterns:
        idx = load_patterns.index('PP')
        load_patterns.pop(idx)
        scale_factors.pop(idx)
        n_loads = len(load_patterns)

    log.info(f"  IncludeElements = True (captures PP with SWM=1)")
    log.info(f"  IncludeAddedMass = False")
    log.info(f"  IncludeLoads = True")
    log.info(f"  Load patterns ({n_loads}):")
    for pat, sf in zip(load_patterns, scale_factors):
        log.info(f"    {pat}: SF={sf}")

    ret = SapModel.PropMaterial.SetMassSource_1(
        True,             # IncludeElements — captures self-weight (PP)
        False,            # IncludeAddedMass — no added mass
        True,             # IncludeLoads — include mass from load patterns
        n_loads,          # NumberLoads
        load_patterns,    # LoadPat[] — ["TERP", "SCP"]
        scale_factors,    # SF[] — [1.0, 0.25]
    )
    check_ret(ret, "PropMaterial.SetMassSource_1")
    log.info("  Mass Source configured ✓")


# ===================================================================
# STEP 2: Define Response Spectrum Function
# ===================================================================

def _read_spectrum_file(filepath):
    """Read spectrum file (tab-separated T, Sa/g).

    File format: each line is "T_value\\tSa_g_value"
    No header lines.

    Returns:
        tuple (periods[], values[]) — both as lists of float
    """
    periods = []
    values = []

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Spectrum file not found: {filepath}")

    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split()
            if len(parts) < 2:
                log.warning(f"  Line {line_num}: skipping (expected 2 columns)")
                continue

            try:
                t = float(parts[0])
                sa = float(parts[1])
                periods.append(t)
                values.append(sa)
            except ValueError:
                log.warning(f"  Line {line_num}: skipping (non-numeric)")

    return periods, values


def define_spectrum_function(SapModel):
    """Define response spectrum function from file via FuncRS.SetUser.

    CRITICAL: FuncRS.SetFromFile does NOT exist in ETABS API.
    This was the root cause of the bug in the original pipeline (R03 §10.2).
    The correct approach is to read the file in Python and use SetUser.

    The spectrum file contains Sa/g values (dimensionless).
    The scale factor SF=9.81 is applied in the load case, NOT here.

    Firma COM (com_signatures.md §10.1):
      ret = SapModel.Func.FuncRS.SetUser(
          Name, NumberItems, Period[], Value[], DampRatio
      )
    Total args: 5 (4 required + 1 optional)

    NOTE on path: Some COM bindings use Func.FuncRS, others use
    Func.ResponseSpectrum. We try FuncRS first, then ResponseSpectrum.
    """
    log.info("Step 2: Defining Response Spectrum Function...")
    log.info(f"  Function name: {SPECTRUM_FUNC_NAME}")
    log.info(f"  Source file: {os.path.basename(SPECTRUM_FILE)}")
    log.info(f"  Damping ratio: {SPECTRUM_DAMPING}")

    # Read spectrum data from file
    periods, values = _read_spectrum_file(SPECTRUM_FILE)
    n_points = len(periods)

    if n_points == 0:
        raise RuntimeError("Spectrum file is empty — cannot define function")

    log.info(f"  Data points: {n_points}")
    log.info(f"  Period range: {periods[0]:.2f} — {periods[-1]:.2f} s")
    log.info(f"  Sa/g range: {min(values):.6f} — {max(values):.6f}")

    # Validate spectrum data
    if periods[0] != 0.0:
        log.warning(f"  Spectrum does not start at T=0 (starts at {periods[0]})")
    if max(values) > 5.0:
        log.warning(f"  Max Sa/g = {max(values):.3f} — unusually high, verify units")

    # Try primary path: Func.FuncRS.SetUser
    success = False
    try:
        ret = SapModel.Func.FuncRS.SetUser(
            SPECTRUM_FUNC_NAME,   # Name
            n_points,             # NumberItems
            periods,              # Period[] (s)
            values,               # Value[] (Sa/g, dimensionless)
            SPECTRUM_DAMPING,     # DampRatio (0.05 = 5%)
        )
        check_ret(ret, "Func.FuncRS.SetUser")
        success = True
        log.info("  Spectrum function defined via Func.FuncRS.SetUser ✓")
    except Exception as e:
        log.warning(f"  Func.FuncRS.SetUser failed: {e}")
        log.info("  Trying alternative path: Func.ResponseSpectrum.SetUser...")

    # Try fallback path: Func.ResponseSpectrum.SetUser
    if not success:
        try:
            ret = SapModel.Func.ResponseSpectrum.SetUser(
                SPECTRUM_FUNC_NAME,
                n_points,
                periods,
                values,
                SPECTRUM_DAMPING,
            )
            check_ret(ret, "Func.ResponseSpectrum.SetUser")
            success = True
            log.info("  Spectrum function defined via "
                     "Func.ResponseSpectrum.SetUser ✓")
        except Exception as e:
            log.error(f"  Func.ResponseSpectrum.SetUser also failed: {e}")

    if not success:
        raise RuntimeError(
            "Could not define spectrum function via any API path.\n"
            "Tried: Func.FuncRS.SetUser, Func.ResponseSpectrum.SetUser\n"
            "Manual alternative: Define > Functions > Response Spectrum > "
            "From File, select espectro_elastico_Z3SC.txt"
        )

    return n_points


# ===================================================================
# STEP 3: Configure Modal Case
# ===================================================================

def configure_modal_case(SapModel):
    """Configure modal analysis case: Eigen, 30 modes, tol=1E-9.

    ETABS typically auto-creates a "Modal" case. This function either
    resets it or creates a new one with our parameters.

    30 modes is standard for a 20-story building to achieve >90% mass
    participation in both X and Y directions (NCh433 6.3.6.2 requires
    at least 90% in each direction).

    Convergence tolerance 1E-9 is stricter than ETABS default (1E-7)
    for better accuracy in eigenvalue computation.

    COM signatures (CSI OAPI docs):
      SetCase(Name) — creates/resets modal eigen case
      SetNumberModes(Name, MaxModes, MinModes)
      SetParameters(Name, EigenShiftFreq, EigenCutOff, EigenTol,
                    AllowAutoFreqShift)
      SetInitialCase(Name, InitialCase)
    """
    log.info("Step 3: Configuring Modal Eigen Case...")
    log.info(f"  Case name: {MODAL_CASE_NAME}")
    log.info(f"  Max modes: {MODAL_MAX_MODES}")
    log.info(f"  Convergence tolerance: {MODAL_EIGEN_TOL}")

    # 3a: Create or reset modal case
    log.info("  3a: Creating/resetting modal eigen case...")
    ret = SapModel.LoadCases.ModalEigen.SetCase(MODAL_CASE_NAME)
    check_ret(ret, f"ModalEigen.SetCase('{MODAL_CASE_NAME}')")
    log.info(f"    SetCase('{MODAL_CASE_NAME}') ✓")

    # 3b: Set number of modes
    log.info("  3b: Setting number of modes...")
    ret = SapModel.LoadCases.ModalEigen.SetNumberModes(
        MODAL_CASE_NAME,     # Name
        MODAL_MAX_MODES,     # MaxModes = 30
        MODAL_MIN_MODES,     # MinModes = 1
    )
    check_ret(ret, "ModalEigen.SetNumberModes")
    log.info(f"    Modes: max={MODAL_MAX_MODES}, min={MODAL_MIN_MODES} ✓")

    # 3c: Set eigenvalue parameters
    log.info("  3c: Setting eigenvalue parameters...")
    ret = SapModel.LoadCases.ModalEigen.SetParameters(
        MODAL_CASE_NAME,     # Name
        MODAL_EIGEN_SHIFT,   # EigenShiftFreq = 0.0 [cyc/s]
        MODAL_EIGEN_CUTOFF,  # EigenCutOff = 0.0 [cyc/s]
        MODAL_EIGEN_TOL,     # EigenTol = 1E-9
        MODAL_AUTO_SHIFT,    # AllowAutoFreqShift = 1 (Yes)
    )
    check_ret(ret, "ModalEigen.SetParameters")
    log.info(f"    ShiftFreq={MODAL_EIGEN_SHIFT}, "
             f"CutOff={MODAL_EIGEN_CUTOFF}, "
             f"Tol={MODAL_EIGEN_TOL}, "
             f"AutoShift={MODAL_AUTO_SHIFT} ✓")

    # 3d: Set initial case (zero initial conditions)
    log.info("  3d: Setting initial case (zero initial conditions)...")
    try:
        ret = SapModel.LoadCases.ModalEigen.SetInitialCase(
            MODAL_CASE_NAME,  # Name
            "",               # InitialCase = "" → zero initial conditions
        )
        check_ret(ret, "ModalEigen.SetInitialCase")
        log.info("    InitialCase = '' (zero) ✓")
    except Exception as e:
        log.warning(f"    SetInitialCase failed: {e} — using default (OK)")

    log.info(f"  Modal case '{MODAL_CASE_NAME}' configured ✓")


# ===================================================================
# STEP 4: Define Spectrum Load Cases (SDX, SDY)
# ===================================================================

def _create_spectrum_case(SapModel, case_name, direction, func_name, sf):
    """Create a single response spectrum load case.

    Steps:
      1. SetCase — create/reset the case
      2. SetLoads — assign direction, function, scale factor
      3. SetModalCase — link to modal case
      4. (Optional) SetEccentricity — accidental torsion (NOT set here,
         handled in a separate torsion script)

    Firma COM (com_signatures.md §11):
      SetCase(Name)
      SetLoads(Name, NumberLoads, LoadType[], LoadName[], SF[], CSys[], Ang[])
      SetModalCase(Name, ModalCase)

    Args:
        SapModel: ETABS model object
        case_name: str — "SDX" or "SDY"
        direction: str — "U1" (X) or "U2" (Y)
        func_name: str — spectrum function name
        sf: float — scale factor (9.81 for Sa/g → m/s²)
    """
    # 4a: Create case
    ret = SapModel.LoadCases.ResponseSpectrum.SetCase(case_name)
    check_ret(ret, f"ResponseSpectrum.SetCase('{case_name}')")
    log.info(f"    SetCase('{case_name}') ✓")

    # 4b: Assign loads
    ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(
        case_name,       # Name
        1,               # NumberLoads = 1 (single direction)
        [direction],     # LoadType[] — "U1" or "U2"
        [func_name],     # LoadName[] — spectrum function
        [sf],            # SF[] — 9.81 (Sa/g → m/s²)
        ["Global"],      # CSys[] — global coordinate system
        [0.0],           # Ang[] — angle = 0°
    )
    check_ret(ret, f"ResponseSpectrum.SetLoads('{case_name}')")
    log.info(f"    SetLoads: dir={direction}, func={func_name}, "
             f"SF={sf} ✓")

    # 4c: Link to modal case
    ret = SapModel.LoadCases.ResponseSpectrum.SetModalCase(
        case_name,           # Name
        MODAL_CASE_NAME,     # ModalCase = "Modal"
    )
    check_ret(ret, f"ResponseSpectrum.SetModalCase('{case_name}')")
    log.info(f"    SetModalCase: '{MODAL_CASE_NAME}' ✓")

    # 4d: Modal combination is CQC by default in ETABS.
    # Directional combination is SRSS by default for single-direction cases.
    # No explicit API call needed — defaults are correct.
    # (CQC and SRSS are the standard choices per NCh433 6.3.6.2)
    log.info(f"    Modal combination: CQC (default)")
    log.info(f"    Directional combination: SRSS (default)")


def define_spectrum_cases(SapModel):
    """Define spectrum load cases SDX and SDY.

    SDX: Earthquake in X direction (U1)
      - Function: Esp_Elastico_Z3SC (Sa/g from NCh433+DS61)
      - Scale Factor: 9.81 (converts Sa/g to m/s²)
      - Modal: linked to "Modal" case (30 Eigen modes)
      - Combination: CQC (modal) + SRSS (directional) — both default

    SDY: Earthquake in Y direction (U2)
      - Same as SDX but in U2 direction

    NOTE: Accidental torsion eccentricity is NOT set here.
    It will be handled in a separate script (09_torsion_cases.py)
    or applied manually via ETABS UI (3 methods per Prof. Music).
    """
    log.info("Step 4: Defining Spectrum Load Cases...")
    log.info(f"  Spectrum function: {SPECTRUM_FUNC_NAME}")
    log.info(f"  Scale factor: {SPECTRUM_SF} (Sa/g → m/s²)")
    log.info(f"  Modal case: {MODAL_CASE_NAME}")
    log.info("")

    # SDX — Earthquake in X (U1)
    log.info(f"  Creating {SDX_CASE_NAME} (U1)...")
    _create_spectrum_case(
        SapModel, SDX_CASE_NAME, "U1",
        SPECTRUM_FUNC_NAME, SPECTRUM_SF,
    )
    log.info("")

    # SDY — Earthquake in Y (U2)
    log.info(f"  Creating {SDY_CASE_NAME} (U2)...")
    _create_spectrum_case(
        SapModel, SDY_CASE_NAME, "U2",
        SPECTRUM_FUNC_NAME, SPECTRUM_SF,
    )
    log.info("")

    log.info(f"  Both spectrum cases created ✓")


# ===================================================================
# STEP 5: Verification
# ===================================================================

def verify_spectrum_function(SapModel):
    """Verify the spectrum function was created correctly.

    Uses Func.FuncRS.GetNameList to check the function exists.
    """
    log.info("Step 5a: Verifying spectrum function...")

    found = False
    try:
        result = SapModel.Func.FuncRS.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_funcs = result[0]
            func_names = [str(f) for f in result[1]] if result[1] else []
            log.info(f"  Spectrum functions in model ({n_funcs}):")
            for name in func_names:
                marker = "✓" if name == SPECTRUM_FUNC_NAME else " "
                log.info(f"    {marker} {name}")
                if name == SPECTRUM_FUNC_NAME:
                    found = True
    except Exception:
        # Try alternative path
        try:
            result = SapModel.Func.ResponseSpectrum.GetNameList()
            if isinstance(result, tuple) and len(result) >= 2:
                func_names = [str(f) for f in result[1]] if result[1] else []
                for name in func_names:
                    if name == SPECTRUM_FUNC_NAME:
                        found = True
                        log.info(f"  Found {SPECTRUM_FUNC_NAME} via "
                                 "Func.ResponseSpectrum ✓")
        except Exception as e:
            log.warning(f"  Could not verify spectrum function: {e}")

    if found:
        log.info(f"  Spectrum function '{SPECTRUM_FUNC_NAME}' exists ✓")
    else:
        log.warning(f"  Spectrum function '{SPECTRUM_FUNC_NAME}' NOT found!")

    return found


def verify_load_cases(SapModel):
    """Verify all expected load cases exist.

    Expected: Modal, SDX, SDY (plus any auto-created cases).
    """
    log.info("Step 5b: Verifying load cases...")

    expected = {MODAL_CASE_NAME, SDX_CASE_NAME, SDY_CASE_NAME}
    found = set()

    try:
        result = SapModel.LoadCases.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_cases = result[0]
            case_names = [str(c) for c in result[1]] if result[1] else []
            log.info(f"  Load cases in model ({n_cases}):")
            for name in case_names:
                marker = "✓" if name in expected else " "
                log.info(f"    {marker} {name}")
                if name in expected:
                    found.add(name)
    except Exception as e:
        log.warning(f"  LoadCases.GetNameList failed: {e}")
        return False

    missing = expected - found
    if missing:
        log.warning(f"  MISSING cases: {missing}")
        return False

    log.info(f"  All {len(expected)} expected cases present ✓")
    return True


def verify_modal_parameters(SapModel):
    """Verify modal case parameters (number of modes, tolerance)."""
    log.info("Step 5c: Verifying modal parameters...")

    try:
        result = SapModel.LoadCases.ModalEigen.GetNumberModes(
            MODAL_CASE_NAME, 0, 0
        )
        if isinstance(result, tuple) and len(result) >= 3:
            max_modes = result[0]
            min_modes = result[1]
            ret_code = result[-1]
            log.info(f"  Modes: max={max_modes}, min={min_modes}")
            if max_modes != MODAL_MAX_MODES:
                log.warning(f"  Expected max={MODAL_MAX_MODES}, "
                            f"got {max_modes}")
            else:
                log.info(f"  Number of modes OK ✓")
    except Exception as e:
        log.warning(f"  Could not verify modal modes: {e}")

    try:
        result = SapModel.LoadCases.ModalEigen.GetParameters(
            MODAL_CASE_NAME, 0.0, 0.0, 0.0, 0
        )
        if isinstance(result, tuple) and len(result) >= 4:
            shift = result[0]
            cutoff = result[1]
            tol = result[2]
            auto_shift = result[3]
            log.info(f"  Parameters: shift={shift}, cutoff={cutoff}, "
                     f"tol={tol}, autoShift={auto_shift}")
            if abs(tol - MODAL_EIGEN_TOL) > 1E-15:
                log.warning(f"  Expected tol={MODAL_EIGEN_TOL}, got {tol}")
            else:
                log.info(f"  Convergence tolerance OK ✓")
    except Exception as e:
        log.warning(f"  Could not verify modal parameters: {e}")


def print_seismic_summary():
    """Print a summary of all seismic parameters for reference."""
    log.info("")
    log.info("  Seismic Configuration Summary:")
    log.info("  ┌────────────────────────────────────────────────────┐")
    log.info("  │ Mass Source                                        │")
    log.info("  │   Elements (PP): included (SWM=1)                  │")
    for pat, sf in MASS_SOURCE_PATTERNS.items():
        if pat != 'PP':
            log.info(f"  │   {pat}: SF={sf:<6.2f}"
                     f"{'':>36s}│")
    log.info("  ├────────────────────────────────────────────────────┤")
    log.info(f"  │ Spectrum: {SPECTRUM_FUNC_NAME:<40s}│")
    log.info(f"  │   Damping: {SPECTRUM_DAMPING:<39}│")
    log.info(f"  │   Points: from {os.path.basename(SPECTRUM_FILE):<30s}│")
    log.info("  ├────────────────────────────────────────────────────┤")
    log.info(f"  │ Modal: {MODAL_CASE_NAME:<43s}│")
    log.info(f"  │   Type: Eigen, {MODAL_MAX_MODES} modes"
             f"{'':>27s}│")
    log.info(f"  │   Tol: {MODAL_EIGEN_TOL:<43}│")
    log.info("  ├────────────────────────────────────────────────────┤")
    log.info(f"  │ {SDX_CASE_NAME}: U1, {SPECTRUM_FUNC_NAME}, "
             f"SF={SPECTRUM_SF}"
             f"{'':>14s}│")
    log.info(f"  │ {SDY_CASE_NAME}: U2, {SPECTRUM_FUNC_NAME}, "
             f"SF={SPECTRUM_SF}"
             f"{'':>14s}│")
    log.info("  │   Modal combo: CQC   |   Dir combo: SRSS          │")
    log.info("  │   Eccentricity: NOT SET (handled separately)       │")
    log.info("  └────────────────────────────────────────────────────┘")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: complete seismic configuration."""
    log.info("=" * 60)
    log.info("08_seismic.py — Seismic configuration, Edificio 1")
    log.info("=" * 60)
    log.info("")
    log.info("  Tasks:")
    log.info("    1. Configure Mass Source (elements + TERP + 0.25×SCP)")
    log.info("    2. Define Response Spectrum Function (from file)")
    log.info("    3. Configure Modal Case (Eigen, 30 modes, tol=1E-9)")
    log.info("    4. Define Spectrum Cases (SDX: U1, SDY: U2)")
    log.info("    5. Verify all settings")
    log.info("")

    # Connect to ETABS
    log.info("Connecting to ETABS v19...")
    try:
        SapModel = connect()
    except ConnectionError as e:
        log.error(str(e))
        sys.exit(1)
    except ImportError:
        log.error("comtypes not installed — run: pip install comtypes")
        sys.exit(1)

    try:
        # Ensure correct units
        set_units(UNITS_TONF_M_C)
        log.info(f"  Units set to Tonf_m_C (={UNITS_TONF_M_C})")
        log.info("")

        t_start = time.time()

        # Step 1: Mass Source
        configure_mass_source(SapModel)
        log.info("")

        # Step 2: Spectrum Function
        n_points = define_spectrum_function(SapModel)
        log.info("")

        # Step 3: Modal Case
        configure_modal_case(SapModel)
        log.info("")

        # Step 4: Spectrum Cases
        define_spectrum_cases(SapModel)

        t_elapsed = time.time() - t_start

        # Step 5: Verification
        log.info("Step 5: Verification...")
        log.info("")
        func_ok = verify_spectrum_function(SapModel)
        log.info("")
        cases_ok = verify_load_cases(SapModel)
        log.info("")
        verify_modal_parameters(SapModel)
        log.info("")

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Summary
        print_seismic_summary()
        log.info("")

        # Final report
        log.info("=" * 60)
        log.info("RESULTS")
        log.info("=" * 60)
        log.info(f"  Mass Source: elements + TERP×1.0 + SCP×0.25 ✓")
        log.info(f"  Spectrum function: {SPECTRUM_FUNC_NAME} "
                 f"({n_points} points) "
                 f"{'✓' if func_ok else '✗'}")
        log.info(f"  Modal case: {MODAL_CASE_NAME} "
                 f"(Eigen, {MODAL_MAX_MODES} modes) ✓")
        log.info(f"  Spectrum cases: {SDX_CASE_NAME} (U1), "
                 f"{SDY_CASE_NAME} (U2) "
                 f"{'✓' if cases_ok else '✗'}")
        log.info(f"  Time: {t_elapsed:.1f}s")
        log.info("")

        if not func_ok or not cases_ok:
            log.warning("  Some verifications failed — check warnings above")
        else:
            log.info("  All seismic settings configured successfully!")

        log.info("")
        log.info("Ready for next step (09_torsion_cases.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
