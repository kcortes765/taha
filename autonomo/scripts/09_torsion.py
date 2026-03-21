"""
09_torsion.py — Accidental Torsion: 3 methods, 6 cases total.

Implements accidental torsion per NCh433 Art. 6.3.4 for Edificio 1.

NCh433 Art. 6.3.4: Accidental eccentricity varies linearly with height:
    ek = 0.10 × (zk / H_total) × b_perp
    At top: 10% of perpendicular dimension. At base: 0%.
    Uniform 5% approximation is the height-averaged value.

Three methods (per Prof. Music / Material Apoyo Taller 2026):

  Method a) Shift CM:
    - 4 Mass Sources with ±5% CM offset (manual GUI step)
    - 4 Nonlinear Static auxiliary cases (mass matrix providers)
    - 4 Modal Eigen cases linked to auxiliaries
    - 4 Response Spectrum cases with shifted modals
    NOTE: Mass Source CM offset NOT available via SetMassSource_1.

  Method b) Form 1 — Static Moments:
    - Compute torsional moments Mtk = Fk × ek per floor
    - Create load patterns TEX, TEY with Mz at each floor
    - Combine: SDX ± TEX, SDY ± TEY
    NOTE: Requires model to be analyzed first for story shears,
    or uses approximate static distribution as fallback.

  Method b) Form 2 — Eccentricity per Floor:
    - Create SDTX, SDTY with SetEccentricity(0.05)
    - ETABS internally generates ±5% sub-cases (envelope)
    - Simplest and most API-friendly method.

Six cases for the taller:
  Case 1: Method a   + rigid diaphragm
  Case 2: Method b-F1 + rigid diaphragm
  Case 3: Method b-F2 + rigid diaphragm
  Case 4: Method a   + semi-rigid diaphragm
  Case 5: Method b-F1 + semi-rigid diaphragm
  Case 6: Method b-F2 + semi-rigid diaphragm

Prerequisites:
  - ETABS v19 open with model from scripts 01-08
  - Modal and SDX/SDY cases defined (08_seismic.py)
  - comtypes installed
  - config.py in same directory

Usage:
  python 09_torsion.py                     # All 3 methods, rigid diaphragm
  python 09_torsion.py --method a          # Method a only
  python 09_torsion.py --method b1         # Method b-F1 only
  python 09_torsion.py --method b2         # Method b-F2 only
  python 09_torsion.py --method all        # All 3 methods

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against:
  - autonomo/research/com_signatures.md
  - autonomo/research/etabs_api_reference.md
  - CSI OAPI official documentation (docs.csiamerica.com)
  - ResponseSpectrum.SetEccentricity: §11.4 (2 args)
  - PointObj.SetLoadForce: §8.1 (6 args)
  - PointObj.GetNameList: §8.2
  - PointObj.GetCoordCartesian: §8.3 (4 args)
  - StaticLinear.SetCase/SetLoads: §9.1-§9.2
  - LoadPatterns.Add: §7.1 (4 args)

Sources: NCh433 Mod 2009, DS61, Material Apoyo Taller 2026 (Sec. H)
"""

import sys
import os
import time
import argparse

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
    # Building geometry
    N_STORIES, STORY_NAMES, STORY_HEIGHTS, STORY_ELEVATIONS, H_TOTAL,
    LX_PLANTA, LY_PLANTA,
    AREA_PLANTA,
    # Seismic parameters
    SPECTRUM_SF, MASS_SOURCE_PATTERNS,
    G_ACCEL, AO_G, S_SUELO, TO_SUELO, T_PRIME, P_SUELO, N_SUELO,
    R_MUROS, RO_MUROS, I_FACTOR,
    EA_X, EA_Y,
    # Diaphragm
    DIAPHRAGM_RIGID_NAME, DIAPHRAGM_SEMI_NAME,
    # Load pattern types
    LTYPE_QUAKE,
    # Formulas
    calc_alpha, calc_R_star,
)


# ===================================================================
# SECTION 1: CONSTANTS AND NAMING CONVENTIONS
# ===================================================================

# Spectrum function and base cases (from 08_seismic.py)
SPECTRUM_FUNC_NAME = "Esp_Elastico_Z3SC"
MODAL_CASE_NAME = "Modal"
SDX_CASE = "SDX"
SDY_CASE = "SDY"

# --- Method a: Shifted CM names ---
# Mass Sources (manual GUI configuration required)
MS_PLUS_X = "MS_PlusX"       # CM shifted +5% in X
MS_MINUS_X = "MS_MinusX"     # CM shifted -5% in X
MS_PLUS_Y = "MS_PlusY"       # CM shifted +5% in Y
MS_MINUS_Y = "MS_MinusY"     # CM shifted -5% in Y

# Nonlinear Static auxiliary cases (mass matrix providers)
AUX_PX = "AUX_PX"
AUX_MX = "AUX_MX"
AUX_PY = "AUX_PY"
AUX_MY = "AUX_MY"

# Modal cases with shifted mass
MOD_PX = "Modal_PX"
MOD_MX = "Modal_MX"
MOD_PY = "Modal_PY"
MOD_MY = "Modal_MY"

# Response Spectrum cases — Method a
# Sismo X + eccentricity perpendicular (Y)
SDX_A_PY = "SDX_aPY"      # SDX with CM shifted +Y
SDX_A_MY = "SDX_aMY"      # SDX with CM shifted -Y
# Sismo Y + eccentricity perpendicular (X)
SDY_A_PX = "SDY_aPX"      # SDY with CM shifted +X
SDY_A_MX = "SDY_aMX"      # SDY with CM shifted -X

# --- Method b-F1: Static Moments ---
LP_TEX = "TEX"     # Torsion pattern from earthquake X
LP_TEY = "TEY"     # Torsion pattern from earthquake Y

# --- Method b-F2: Eccentricity per floor ---
SDTX_CASE = "SDTX"   # SDX + 5% eccentricity
SDTY_CASE = "SDTY"   # SDY + 5% eccentricity

# Eccentricity ratio (uniform approximation of NCh433 linear variation)
ECC_RATIO = 0.05     # 5%

# Modal parameters (same as 08_seismic.py)
MODAL_MAX_MODES = 30
MODAL_MIN_MODES = 1
MODAL_EIGEN_TOL = 1.0E-9
MODAL_AUTO_SHIFT = 1


# ===================================================================
# SECTION 2: ECCENTRICITY TABLE (NCh433 Art. 6.3.4)
# ===================================================================

def compute_eccentricity_table():
    """Compute accidental eccentricity per floor per NCh433 Art. 6.3.4.

    Formula: ek = 0.10 × (zk / H_total) × b_perp

    For sismo X → eccentricity in Y direction (perpendicular):
      ek_Y = 0.10 × (zk / 52.80) × 13.821 m

    For sismo Y → eccentricity in X direction (perpendicular):
      ek_X = 0.10 × (zk / 52.80) × 38.505 m

    Returns:
        list of dicts: {story, floor, zk, ek_y, ek_x}
    """
    table = []
    for i, (name, zk) in enumerate(zip(STORY_NAMES, STORY_ELEVATIONS)):
        ratio = zk / H_TOTAL
        ek_y = 0.10 * ratio * LY_PLANTA   # For sismo X
        ek_x = 0.10 * ratio * LX_PLANTA   # For sismo Y
        table.append({
            'story': name,
            'floor': i + 1,
            'zk': zk,
            'zk_ratio': ratio,
            'ek_y': round(ek_y, 4),
            'ek_x': round(ek_x, 4),
        })
    return table


def print_eccentricity_table():
    """Print eccentricity table for reference."""
    table = compute_eccentricity_table()
    log.info("  NCh433 Art. 6.3.4 — Accidental Eccentricity:")
    log.info(f"  ek = 0.10 × (zk / {H_TOTAL:.2f}) × b_perp")
    log.info(f"  LX = {LX_PLANTA:.3f} m | LY = {LY_PLANTA:.3f} m")
    log.info("")
    log.info(f"  {'Floor':>5s}  {'zk(m)':>6s}  {'zk/H':>5s}  "
             f"{'ek_Y(m)':>8s}  {'ek_X(m)':>8s}")
    log.info(f"  {'─'*5}  {'─'*6}  {'─'*5}  {'─'*8}  {'─'*8}")
    for row in table:
        log.info(f"  {row['floor']:5d}  {row['zk']:6.2f}  "
                 f"{row['zk_ratio']:5.3f}  {row['ek_y']:8.4f}  "
                 f"{row['ek_x']:8.4f}")
    log.info("")
    log.info(f"  Top: ek_Y={table[-1]['ek_y']:.3f}m, "
             f"ek_X={table[-1]['ek_x']:.3f}m")
    log.info(f"  Uniform 5%: ea_Y={EA_Y:.3f}m, ea_X={EA_X:.3f}m")


def compute_approx_story_forces():
    """Compute approximate lateral forces per floor using static method.

    Used as fallback when model hasn't been analyzed yet (no story shears).

    Method: Inverted triangle distribution (NCh433 Art. 6.3.3)
      Fk = Qo × (wk × zk) / Σ(wi × zi)

    Assumes uniform floor weight (wk = constant for all floors).
    T1 ≈ H/40 for shear wall buildings (empirical).

    Returns:
        tuple: (Qo_x, Qo_y, forces_x[], forces_y[])
        where forces are in tonf per floor (floor 1 to 20)
    """
    # Approximate fundamental period
    T1 = H_TOTAL / 40.0    # ~1.32 s for shear wall building

    # Approximate Sa/g
    alpha = calc_alpha(T1)
    Sa_g = S_SUELO * AO_G * alpha

    # R* factor
    R_star = calc_R_star(T1)

    # Approximate seismic weight
    W = AREA_PLANTA * N_STORIES * 1.0   # ~1 tonf/m² rule (Lafontaine)

    # Base shear (same in X and Y for symmetric spectrum)
    Qo = Sa_g * W / R_star

    # Inverted triangle: Fk ∝ zk (uniform floor weight)
    sum_zk = sum(STORY_ELEVATIONS)
    forces = []
    for zk in STORY_ELEVATIONS:
        Fk = Qo * zk / sum_zk
        forces.append(round(Fk, 4))

    log.info(f"  Approximate static forces (T1≈{T1:.2f}s):")
    log.info(f"    Sa/g = {Sa_g:.4f}, R* = {R_star:.2f}")
    log.info(f"    W ≈ {W:.0f} tonf, Qo ≈ {Qo:.1f} tonf")
    log.info(f"    Distribution: inverted triangle (uniform floor weight)")

    return Qo, Qo, forces, forces


def compute_torsion_moments(forces_x, forces_y):
    """Compute torsional moments Mtk = Fk × ek per floor.

    Args:
        forces_x: list of lateral forces from sismo X per floor (tonf)
        forces_y: list of lateral forces from sismo Y per floor (tonf)

    Returns:
        tuple: (moments_tex[], moments_tey[])
        TEX = moments from sismo X forces × eccentricity in Y
        TEY = moments from sismo Y forces × eccentricity in X
    """
    ecc_table = compute_eccentricity_table()
    moments_tex = []
    moments_tey = []

    for i, row in enumerate(ecc_table):
        fx = forces_x[i] if i < len(forces_x) else 0.0
        fy = forces_y[i] if i < len(forces_y) else 0.0
        mt_ex = fx * row['ek_y']   # Sismo X × eccentricity Y
        mt_ey = fy * row['ek_x']   # Sismo Y × eccentricity X
        moments_tex.append(round(mt_ex, 4))
        moments_tey.append(round(mt_ey, 4))

    return moments_tex, moments_tey


# ===================================================================
# SECTION 3: METHOD A — SHIFT CM (±5%)
# ===================================================================

def _create_nl_static_auxiliary(SapModel, case_name):
    """Create a Nonlinear Static auxiliary case (no loads).

    These cases serve as mass matrix providers for modal cases
    with shifted CM. They carry no loads — just establish the
    mass/stiffness state for the subsequent modal analysis.

    COM path: LoadCases.StaticNonlinear.SetCase(Name)
    """
    log.info(f"    Creating NL Static auxiliary: {case_name}...")
    try:
        ret = SapModel.LoadCases.StaticNonlinear.SetCase(case_name)
        check_ret(ret, f"StaticNonlinear.SetCase('{case_name}')")
        log.info(f"      {case_name} created ✓")
        return True
    except Exception as e:
        log.warning(f"      StaticNonlinear.SetCase failed: {e}")
        log.warning(f"      Create '{case_name}' manually: "
                    "Define > Load Cases > Add > Nonlinear Static")
        return False


def _create_modal_shifted(SapModel, modal_name, initial_case):
    """Create a Modal Eigen case linked to an auxiliary NL Static case.

    The modal case inherits the mass matrix from the auxiliary case,
    which has the shifted CM. This gives eigenvalues/eigenvectors
    that account for the shifted mass distribution.

    COM signatures:
      ModalEigen.SetCase(Name) — create/reset
      ModalEigen.SetNumberModes(Name, Max, Min)
      ModalEigen.SetParameters(Name, Shift, Cutoff, Tol, AutoShift)
      ModalEigen.SetInitialCase(Name, InitialCase)
    """
    log.info(f"    Creating Modal case: {modal_name} "
             f"(from {initial_case})...")

    # Create modal case
    ret = SapModel.LoadCases.ModalEigen.SetCase(modal_name)
    check_ret(ret, f"ModalEigen.SetCase('{modal_name}')")

    # Set number of modes (same as base modal case)
    ret = SapModel.LoadCases.ModalEigen.SetNumberModes(
        modal_name, MODAL_MAX_MODES, MODAL_MIN_MODES,
    )
    check_ret(ret, f"ModalEigen.SetNumberModes('{modal_name}')")

    # Set eigenvalue parameters
    ret = SapModel.LoadCases.ModalEigen.SetParameters(
        modal_name,
        0.0,                 # EigenShiftFreq
        0.0,                 # EigenCutOff
        MODAL_EIGEN_TOL,     # EigenTol = 1E-9
        MODAL_AUTO_SHIFT,    # AllowAutoFreqShift = 1
    )
    check_ret(ret, f"ModalEigen.SetParameters('{modal_name}')")

    # Link to auxiliary case (inherits shifted mass matrix)
    ret = SapModel.LoadCases.ModalEigen.SetInitialCase(
        modal_name, initial_case,
    )
    check_ret(ret, f"ModalEigen.SetInitialCase('{modal_name}', "
              f"'{initial_case}')")

    log.info(f"      {modal_name}: {MODAL_MAX_MODES} modes, "
             f"tol={MODAL_EIGEN_TOL}, initial={initial_case} ✓")


def _create_rs_case(SapModel, case_name, direction, modal_case,
                    eccentricity=0.0):
    """Create a Response Spectrum load case.

    Args:
        case_name: str — name for the RS case
        direction: str — "U1" (X) or "U2" (Y)
        modal_case: str — name of the modal case to use
        eccentricity: float — eccentricity ratio (0.0 = none, 0.05 = 5%)

    COM signatures:
      ResponseSpectrum.SetCase(Name)
      ResponseSpectrum.SetLoads(Name, N, LoadType[], LoadName[], SF[],
                                CSys[], Ang[])
      ResponseSpectrum.SetModalCase(Name, ModalCase)
      ResponseSpectrum.SetEccentricity(Name, Eccen)
    """
    log.info(f"    Creating RS case: {case_name} "
             f"(dir={direction}, modal={modal_case})...")

    # Create case
    ret = SapModel.LoadCases.ResponseSpectrum.SetCase(case_name)
    check_ret(ret, f"ResponseSpectrum.SetCase('{case_name}')")

    # Assign spectrum load
    ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(
        case_name,
        1,                      # NumberLoads
        [direction],            # LoadType — "U1" or "U2"
        [SPECTRUM_FUNC_NAME],   # LoadName — spectrum function
        [SPECTRUM_SF],          # SF — 9.81 (Sa/g → m/s²)
        ["Global"],             # CSys
        [0.0],                  # Ang
    )
    check_ret(ret, f"ResponseSpectrum.SetLoads('{case_name}')")

    # Link to modal case
    ret = SapModel.LoadCases.ResponseSpectrum.SetModalCase(
        case_name, modal_case,
    )
    check_ret(ret, f"ResponseSpectrum.SetModalCase('{case_name}')")

    # Set eccentricity if specified
    if eccentricity > 0.0:
        try:
            ret = SapModel.LoadCases.ResponseSpectrum.SetEccentricity(
                case_name, eccentricity,
            )
            check_ret(ret, f"ResponseSpectrum.SetEccentricity"
                      f"('{case_name}', {eccentricity})")
            log.info(f"      Eccentricity = {eccentricity} ✓")
        except Exception as e:
            log.warning(f"      SetEccentricity failed: {e}")
            log.warning(f"      Set eccentricity={eccentricity} manually "
                        f"in Load Case '{case_name}'")

    log.info(f"      {case_name}: {direction}, "
             f"{SPECTRUM_FUNC_NAME}, SF={SPECTRUM_SF}, "
             f"modal={modal_case} ✓")


def setup_method_a(SapModel):
    """Set up Method a) Shift CM — creates all cases.

    Method a) shifts the center of mass ±5% in each direction by
    modifying the Mass Source. Since SetMassSource_1 does NOT support
    the "Adjust Diaphragm Lateral Mass" parameter, the mass sources
    must be configured manually in the ETABS GUI.

    This function creates the downstream cases:
      1. 4 NL Static auxiliary cases (mass matrix providers)
      2. 4 Modal Eigen cases linked to auxiliaries
      3. 4 RS cases using shifted modals

    Naming convention:
      Sismo X → eccentricity in Y (perpendicular):
        SDX_aPY (CM+Y), SDX_aMY (CM-Y)
      Sismo Y → eccentricity in X (perpendicular):
        SDY_aPX (CM+X), SDY_aMX (CM-X)
    """
    log.info("=" * 60)
    log.info("METHOD A: SHIFT CM (±5%)")
    log.info("=" * 60)
    log.info("")

    # ---------------------------------------------------------------
    # Step 1: NL Static auxiliary cases
    # ---------------------------------------------------------------
    log.info("  Step 1: Nonlinear Static auxiliary cases...")
    aux_cases = [
        (AUX_PX, MS_PLUS_X),
        (AUX_MX, MS_MINUS_X),
        (AUX_PY, MS_PLUS_Y),
        (AUX_MY, MS_MINUS_Y),
    ]
    nl_ok = True
    for case_name, ms_name in aux_cases:
        ok = _create_nl_static_auxiliary(SapModel, case_name)
        nl_ok = nl_ok and ok
    log.info("")

    if not nl_ok:
        log.warning("  Some NL Static cases could not be created via API.")
        log.warning("  Create them manually: Define > Load Cases > Add New")
        log.warning("  Type: Nonlinear Static, no loads, assign Mass Source.")
        log.info("")

    # ---------------------------------------------------------------
    # Step 2: Modal Eigen cases with shifted mass
    # ---------------------------------------------------------------
    log.info("  Step 2: Modal Eigen cases (shifted mass)...")
    modal_cases = [
        (MOD_PX, AUX_PX),   # Shifted +X
        (MOD_MX, AUX_MX),   # Shifted -X
        (MOD_PY, AUX_PY),   # Shifted +Y
        (MOD_MY, AUX_MY),   # Shifted -Y
    ]
    for modal_name, aux_name in modal_cases:
        try:
            _create_modal_shifted(SapModel, modal_name, aux_name)
        except Exception as e:
            log.warning(f"    {modal_name} failed: {e}")
            log.warning(f"    Create manually: Modal Eigen, "
                        f"initial case = {aux_name}")
    log.info("")

    # ---------------------------------------------------------------
    # Step 3: Response Spectrum cases with shifted modals
    # ---------------------------------------------------------------
    log.info("  Step 3: Response Spectrum cases (shifted modals)...")
    log.info("    Sismo X → eccentricity in Y (perpendicular):")

    # SDX with CM shifted in Y
    try:
        _create_rs_case(SapModel, SDX_A_PY, "U1", MOD_PY, eccentricity=0.0)
    except Exception as e:
        log.warning(f"    {SDX_A_PY} failed: {e}")

    try:
        _create_rs_case(SapModel, SDX_A_MY, "U1", MOD_MY, eccentricity=0.0)
    except Exception as e:
        log.warning(f"    {SDX_A_MY} failed: {e}")

    log.info("")
    log.info("    Sismo Y → eccentricity in X (perpendicular):")

    # SDY with CM shifted in X
    try:
        _create_rs_case(SapModel, SDY_A_PX, "U2", MOD_PX, eccentricity=0.0)
    except Exception as e:
        log.warning(f"    {SDY_A_PX} failed: {e}")

    try:
        _create_rs_case(SapModel, SDY_A_MX, "U2", MOD_MX, eccentricity=0.0)
    except Exception as e:
        log.warning(f"    {SDY_A_MX} failed: {e}")

    log.info("")

    # ---------------------------------------------------------------
    # Step 4: Manual instructions for Mass Source setup
    # ---------------------------------------------------------------
    log.info("  ┌────────────────────────────────────────────────────┐")
    log.info("  │ MANUAL STEP REQUIRED: Mass Source CM Offset        │")
    log.info("  │                                                    │")
    log.info("  │ The API function SetMassSource_1 does NOT support  │")
    log.info("  │ the 'Adjust Diaphragm Lateral Mass' parameter.    │")
    log.info("  │ You must configure this manually in ETABS GUI:     │")
    log.info("  │                                                    │")
    log.info("  │ 1. Define > Mass Source...                         │")
    log.info("  │ 2. Create 4 new mass sources:                     │")
    log.info(f"  │    {MS_PLUS_X:15s}: X=+0.05, Y=0{'':12s}│")
    log.info(f"  │    {MS_MINUS_X:15s}: X=-0.05, Y=0{'':12s}│")
    log.info(f"  │    {MS_PLUS_Y:15s}: X=0, Y=+0.05{'':12s}│")
    log.info(f"  │    {MS_MINUS_Y:15s}: X=0, Y=-0.05{'':12s}│")
    log.info("  │ 3. Each source: same loads as default              │")
    log.info("  │    (Elements + TERP×1.0 + SCP×0.25)                │")
    log.info("  │ 4. Check 'Adjust Diaphragm Lateral Mass to Move   │")
    log.info("  │    Mass Centroid by: X: ±0.05  Y: ±0.05'          │")
    log.info("  │ 5. Assign each mass source to its NL Static case:  │")
    log.info(f"  │    {AUX_PX} → {MS_PLUS_X}{'':24s}│")
    log.info(f"  │    {AUX_MX} → {MS_MINUS_X}{'':23s}│")
    log.info(f"  │    {AUX_PY} → {MS_PLUS_Y}{'':24s}│")
    log.info(f"  │    {AUX_MY} → {MS_MINUS_Y}{'':23s}│")
    log.info("  └────────────────────────────────────────────────────┘")
    log.info("")

    log.info("  Method A setup complete.")
    log.info(f"  Cases created: {AUX_PX}, {AUX_MX}, {AUX_PY}, {AUX_MY}")
    log.info(f"                 {MOD_PX}, {MOD_MX}, {MOD_PY}, {MOD_MY}")
    log.info(f"                 {SDX_A_PY}, {SDX_A_MY}, "
             f"{SDY_A_PX}, {SDY_A_MX}")
    log.info("")


# ===================================================================
# SECTION 4: METHOD B-F1 — STATIC MOMENTS
# ===================================================================

def _find_one_joint_per_story(SapModel):
    """Find one joint name per story level.

    Iterates all joints, matches Z-coordinates to story elevations
    (±0.05m tolerance). Returns the first match per story.

    Returns:
        dict: {story_index (0-based): joint_name}
    """
    log.info("    Finding one joint per story...")

    try:
        result = SapModel.PointObj.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_joints = result[0]
            joint_names = list(result[1]) if result[1] else []
        else:
            log.warning("    GetNameList returned unexpected format")
            return {}
    except Exception as e:
        log.warning(f"    GetNameList failed: {e}")
        return {}

    if not joint_names:
        log.warning("    No joints found in model")
        return {}

    log.info(f"    Total joints in model: {n_joints}")

    story_joints = {}
    for jnt in joint_names:
        # Early exit if all stories found
        if len(story_joints) == N_STORIES:
            break

        try:
            result = SapModel.PointObj.GetCoordCartesian(
                jnt, 0.0, 0.0, 0.0
            )
            z = result[2] if isinstance(result, tuple) else 0.0
        except Exception:
            continue

        # Match to story elevation
        for i, elev in enumerate(STORY_ELEVATIONS):
            if i not in story_joints and abs(z - elev) < 0.05:
                story_joints[i] = jnt
                break

    log.info(f"    Found joints for {len(story_joints)}/{N_STORIES} stories")
    return story_joints


def _extract_story_shears(SapModel):
    """Try to extract story shears from an analyzed model.

    Uses Results.StoryForces or similar API to get Qk per floor
    for SDX and SDY cases.

    Returns:
        tuple: (shears_x[], shears_y[]) — cumulative shears per story
        Returns (None, None) if extraction fails (model not analyzed).
    """
    log.info("    Attempting to extract story shears...")

    try:
        # Select SDX for output
        SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        SapModel.Results.Setup.SetCaseSelectedForOutput(SDX_CASE)

        # Try StoryForces
        result = SapModel.Results.StoryForces(
            "", 0, 0, 0,
            [], [], [], [], [], [], [], [], [], [], []
        )

        if isinstance(result, tuple) and len(result) >= 10:
            n_results = result[0]
            if n_results > 0:
                stories = list(result[1]) if result[1] else []
                vx_vals = list(result[7]) if result[7] else []

                # Build shear per story (bottom location)
                shears_x = [0.0] * N_STORIES
                for j in range(n_results):
                    story = str(stories[j]) if j < len(stories) else ""
                    if story in STORY_NAMES:
                        idx = STORY_NAMES.index(story)
                        if idx < len(shears_x) and j < len(vx_vals):
                            shears_x[idx] = abs(float(vx_vals[j]))

                # Now get SDY shears
                SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
                SapModel.Results.Setup.SetCaseSelectedForOutput(SDY_CASE)
                result2 = SapModel.Results.StoryForces(
                    "", 0, 0, 0,
                    [], [], [], [], [], [], [], [], [], [], []
                )

                shears_y = [0.0] * N_STORIES
                if isinstance(result2, tuple) and len(result2) >= 10:
                    n2 = result2[0]
                    stories2 = list(result2[1]) if result2[1] else []
                    vy_vals = list(result2[8]) if result2[8] else []
                    for j in range(n2):
                        story = str(stories2[j]) if j < len(stories2) else ""
                        if story in STORY_NAMES:
                            idx = STORY_NAMES.index(story)
                            if idx < len(shears_y) and j < len(vy_vals):
                                shears_y[idx] = abs(float(vy_vals[j]))

                log.info("    Story shears extracted from analysis results ✓")
                return shears_x, shears_y

    except Exception as e:
        log.info(f"    Could not extract story shears: {e}")
        log.info("    Using approximate static distribution instead.")

    return None, None


def _compute_forces_from_shears(shears):
    """Convert cumulative story shears to floor forces.

    Fk = Qk - Qk+1 (for top floor: Fk = Qk since Qk+1 = 0)

    The shears list is indexed 0 = Story1 (bottom) to N-1 = StoryN (top).
    Qk is the cumulative shear AT floor k (sum of forces above and at k).
    """
    forces = [0.0] * len(shears)
    for i in range(len(shears)):
        if i == len(shears) - 1:
            # Top floor: F = Q (no floor above)
            forces[i] = shears[i]
        else:
            # Fk = Qk - Qk+1
            forces[i] = max(0.0, shears[i] - shears[i + 1])
    return forces


def setup_method_b_f1(SapModel):
    """Set up Method b) Form 1 — Static Moments.

    Steps:
      1. Extract story shears (or use approximate distribution)
      2. Compute torsional moments Mtk = Fk × ek per floor
      3. Create load patterns TEX, TEY (type = Quake)
      4. Find one joint per story
      5. Apply Mz moments at each floor joint
      6. Create static linear cases for TEX, TEY

    The moments are computed from:
      - Story shears extracted from the analyzed model (preferred)
      - Or approximate inverted-triangle distribution (fallback)

    In load combinations, use ±1.0 scale factor:
      SDX + TEX, SDX - TEX → captures both ± torsion directions
    """
    log.info("=" * 60)
    log.info("METHOD B-F1: STATIC MOMENTS")
    log.info("=" * 60)
    log.info("")

    # ---------------------------------------------------------------
    # Step 1: Get lateral forces per floor
    # ---------------------------------------------------------------
    log.info("  Step 1: Lateral forces per floor...")
    shears_x, shears_y = _extract_story_shears(SapModel)

    if shears_x is not None and shears_y is not None:
        # Convert cumulative shears to floor forces
        forces_x = _compute_forces_from_shears(shears_x)
        forces_y = _compute_forces_from_shears(shears_y)
        source = "analysis results"
    else:
        # Approximate using static method
        log.info("  Using approximate static distribution...")
        _, _, forces_x, forces_y = compute_approx_story_forces()
        source = "approximate static method"
    log.info(f"  Force source: {source}")
    log.info("")

    # ---------------------------------------------------------------
    # Step 2: Compute torsional moments
    # ---------------------------------------------------------------
    log.info("  Step 2: Torsional moments Mtk = Fk × ek...")
    moments_tex, moments_tey = compute_torsion_moments(forces_x, forces_y)

    log.info(f"  {'Floor':>5s}  {'Fx(tonf)':>9s}  {'ek_Y(m)':>8s}  "
             f"{'Mt_X(tf·m)':>11s}  │  {'Fy(tonf)':>9s}  {'ek_X(m)':>8s}  "
             f"{'Mt_Y(tf·m)':>11s}")
    log.info(f"  {'─'*5}  {'─'*9}  {'─'*8}  {'─'*11}  │  "
             f"{'─'*9}  {'─'*8}  {'─'*11}")
    ecc_table = compute_eccentricity_table()
    for i in range(N_STORIES):
        log.info(f"  {i+1:5d}  {forces_x[i]:9.2f}  "
                 f"{ecc_table[i]['ek_y']:8.4f}  {moments_tex[i]:11.4f}  │  "
                 f"{forces_y[i]:9.2f}  {ecc_table[i]['ek_x']:8.4f}  "
                 f"{moments_tey[i]:11.4f}")
    log.info(f"  Total Mt_X = {sum(moments_tex):.2f} tonf·m | "
             f"Mt_Y = {sum(moments_tey):.2f} tonf·m")
    log.info("")

    # ---------------------------------------------------------------
    # Step 3: Create load patterns TEX, TEY
    # ---------------------------------------------------------------
    log.info("  Step 3: Creating load patterns TEX, TEY...")

    for pattern_name in [LP_TEX, LP_TEY]:
        try:
            ret = SapModel.LoadPatterns.Add(
                pattern_name,   # Name
                LTYPE_QUAKE,    # Type = 5 (Seismic)
                0.0,            # SelfWTMultiplier = 0
                False,          # AddAnalysisCase = False (we create manually)
            )
            check_ret(ret, f"LoadPatterns.Add('{pattern_name}')")
            log.info(f"    {pattern_name}: created (type=Quake, SWM=0) ✓")
        except Exception as e:
            # Pattern might already exist
            log.info(f"    {pattern_name}: may already exist ({e})")
    log.info("")

    # ---------------------------------------------------------------
    # Step 4: Find joints per story
    # ---------------------------------------------------------------
    log.info("  Step 4: Finding joints for moment application...")
    story_joints = _find_one_joint_per_story(SapModel)

    if not story_joints:
        log.warning("  Could not find joints — moments NOT applied.")
        log.warning("  Apply moments manually via ETABS GUI:")
        log.warning("  Define > Load Patterns > TEX/TEY > "
                    "Modify Lateral Load...")
        log.warning("  Enter Mz values per floor from the table above.")
    else:
        # ---------------------------------------------------------------
        # Step 5: Apply Mz at each floor joint
        # ---------------------------------------------------------------
        log.info("  Step 5: Applying torsional moments Mz...")

        for i in range(N_STORIES):
            if i not in story_joints:
                log.warning(f"    Floor {i+1}: no joint found — skipping")
                continue

            jnt = story_joints[i]
            mz_tex = moments_tex[i]
            mz_tey = moments_tey[i]

            # Apply TEX moment (Mz about global Z)
            # Value array: [F1, F2, F3, M1, M2, M3]
            if abs(mz_tex) > 1e-6:
                try:
                    ret = SapModel.PointObj.SetLoadForce(
                        jnt,                              # Joint name
                        LP_TEX,                           # Load pattern
                        [0.0, 0.0, 0.0, 0.0, 0.0, mz_tex],  # Mz only
                        True,                             # Replace
                        "Global",                         # CSys
                        0,                                # ItemType=Object
                    )
                    check_ret(ret, f"SetLoadForce({jnt}, TEX, Mz={mz_tex})")
                except Exception as e:
                    log.warning(f"    Floor {i+1} TEX at {jnt} failed: {e}")

            # Apply TEY moment
            if abs(mz_tey) > 1e-6:
                try:
                    ret = SapModel.PointObj.SetLoadForce(
                        jnt,
                        LP_TEY,
                        [0.0, 0.0, 0.0, 0.0, 0.0, mz_tey],
                        True,
                        "Global",
                        0,
                    )
                    check_ret(ret, f"SetLoadForce({jnt}, TEY, Mz={mz_tey})")
                except Exception as e:
                    log.warning(f"    Floor {i+1} TEY at {jnt} failed: {e}")

        log.info(f"    Moments applied to {len(story_joints)} stories ✓")
        log.info("")

    # ---------------------------------------------------------------
    # Step 6: Create static linear cases for TEX, TEY
    # ---------------------------------------------------------------
    log.info("  Step 6: Creating static linear cases...")

    for pattern_name in [LP_TEX, LP_TEY]:
        case_name = pattern_name  # Same name as pattern
        try:
            ret = SapModel.LoadCases.StaticLinear.SetCase(case_name)
            check_ret(ret, f"StaticLinear.SetCase('{case_name}')")

            ret = SapModel.LoadCases.StaticLinear.SetLoads(
                case_name,
                1,                  # NumberLoads
                ["Load"],           # LoadType
                [pattern_name],     # LoadName
                [1.0],              # SF
            )
            check_ret(ret, f"StaticLinear.SetLoads('{case_name}')")
            log.info(f"    {case_name}: Static Linear, "
                     f"loads=[{pattern_name}×1.0] ✓")
        except Exception as e:
            log.warning(f"    {case_name} failed: {e}")
    log.info("")

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    log.info("  Method B-F1 setup complete.")
    log.info(f"  Load patterns: {LP_TEX}, {LP_TEY}")
    log.info(f"  Static cases: {LP_TEX}, {LP_TEY}")
    log.info(f"  Force source: {source}")
    log.info("")
    log.info("  In load combinations, use:")
    log.info(f"    SDX ± TEX  (1.4×SDX + 1.4×TEX, 1.4×SDX - 1.4×TEX)")
    log.info(f"    SDY ± TEY  (1.4×SDY + 1.4×TEY, 1.4×SDY - 1.4×TEY)")
    log.info("")


# ===================================================================
# SECTION 5: METHOD B-F2 — ECCENTRICITY PER FLOOR
# ===================================================================

def setup_method_b_f2(SapModel):
    """Set up Method b) Form 2 — Eccentricity per Floor.

    Creates Response Spectrum cases SDTX and SDTY with uniform 5%
    eccentricity applied via SetEccentricity.

    ETABS internally generates ±5% sub-cases and takes the envelope,
    so NO separate +/- cases are needed.

    This is the simplest method and fully API-programmable.

    NCh433 Art. 6.3.4 prescribes linearly varying eccentricity:
      ek = 0.10 × (zk/H) × b_perp
    The uniform 5% is the height-averaged value — a standard
    approximation accepted in Chilean practice.

    COM signatures:
      ResponseSpectrum.SetCase(Name)
      ResponseSpectrum.SetLoads(Name, N, Type[], Name[], SF[], CSys[], Ang[])
      ResponseSpectrum.SetModalCase(Name, ModalCase)
      ResponseSpectrum.SetEccentricity(Name, Eccen)
    """
    log.info("=" * 60)
    log.info("METHOD B-F2: ECCENTRICITY PER FLOOR")
    log.info("=" * 60)
    log.info("")
    log.info(f"  Eccentricity ratio: {ECC_RATIO} (uniform 5%)")
    log.info(f"  ETABS applies ±{ECC_RATIO*100:.0f}% internally (envelope)")
    log.info("")

    # ---------------------------------------------------------------
    # SDTX: Sismo X + 5% eccentricity
    # ---------------------------------------------------------------
    log.info("  Creating SDTX (Sismo X + accidental torsion)...")
    try:
        _create_rs_case(
            SapModel, SDTX_CASE, "U1", MODAL_CASE_NAME,
            eccentricity=ECC_RATIO,
        )
        log.info(f"    {SDTX_CASE}: U1, ecc={ECC_RATIO} ✓")
    except Exception as e:
        log.error(f"    {SDTX_CASE} failed: {e}")
    log.info("")

    # ---------------------------------------------------------------
    # SDTY: Sismo Y + 5% eccentricity
    # ---------------------------------------------------------------
    log.info("  Creating SDTY (Sismo Y + accidental torsion)...")
    try:
        _create_rs_case(
            SapModel, SDTY_CASE, "U2", MODAL_CASE_NAME,
            eccentricity=ECC_RATIO,
        )
        log.info(f"    {SDTY_CASE}: U2, ecc={ECC_RATIO} ✓")
    except Exception as e:
        log.error(f"    {SDTY_CASE} failed: {e}")
    log.info("")

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    log.info("  Method B-F2 setup complete.")
    log.info(f"  Cases: {SDTX_CASE} (U1 ±5%), {SDTY_CASE} (U2 ±5%)")
    log.info("")
    log.info("  In load combinations, use SDTX/SDTY instead of SDX/SDY:")
    log.info("    C4: 1.2PP + 1.2TERP + 1.0SCP + 1.4×SDTX")
    log.info("    C6: 1.2PP + 1.2TERP + 1.0SCP + 1.4×SDTY")
    log.info("    (No ± needed — ETABS handles envelope internally)")
    log.info("")

    # Per-floor eccentricity note
    log.info("  ┌────────────────────────────────────────────────────┐")
    log.info("  │ NOTE: For per-floor varying eccentricity (NCh433   │")
    log.info("  │ Art. 6.3.4 exact), use ETABS GUI:                  │")
    log.info("  │                                                    │")
    log.info("  │ 1. Edit SDTX/SDTY load case                       │")
    log.info("  │ 2. Click 'Diaphragm Eccentricity' > 'Modify...'   │")
    log.info("  │ 3. Set Eccentricity Ratio = 0 (clear uniform)     │")
    log.info("  │ 4. Enter eccentricity (m) per floor from table:    │")
    log.info("  │    (Run print_eccentricity_table() for values)     │")
    log.info("  │                                                    │")
    log.info("  │ The uniform 5% is an accepted approximation.       │")
    log.info("  └────────────────────────────────────────────────────┘")
    log.info("")


# ===================================================================
# SECTION 6: VERIFICATION
# ===================================================================

def verify_torsion_cases(SapModel, method="all"):
    """Verify that torsion cases were created successfully.

    Args:
        method: "a", "b1", "b2", or "all"
    """
    log.info("Verification: Checking torsion cases...")

    expected = set()
    if method in ("a", "all"):
        expected.update([
            AUX_PX, AUX_MX, AUX_PY, AUX_MY,
            MOD_PX, MOD_MX, MOD_PY, MOD_MY,
            SDX_A_PY, SDX_A_MY, SDY_A_PX, SDY_A_MX,
        ])
    if method in ("b1", "all"):
        expected.update([LP_TEX, LP_TEY])
    if method in ("b2", "all"):
        expected.update([SDTX_CASE, SDTY_CASE])

    # Get all load cases
    found_cases = set()
    try:
        result = SapModel.LoadCases.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            case_names = [str(c) for c in result[1]] if result[1] else []
            found_cases = set(case_names)
    except Exception as e:
        log.warning(f"  LoadCases.GetNameList failed: {e}")
        return False

    # Get all load patterns (for b-F1)
    found_patterns = set()
    if method in ("b1", "all"):
        try:
            result = SapModel.LoadPatterns.GetNameList()
            if isinstance(result, tuple) and len(result) >= 2:
                pat_names = [str(p) for p in result[1]] if result[1] else []
                found_patterns = set(pat_names)
        except Exception:
            pass

    # Check
    all_found = found_cases | found_patterns
    present = expected & all_found
    missing = expected - all_found

    log.info(f"  Expected: {len(expected)} items")
    log.info(f"  Found:    {len(present)} items")

    if missing:
        log.warning(f"  MISSING: {sorted(missing)}")
    else:
        log.info("  All expected cases/patterns present ✓")

    return len(missing) == 0


def print_torsion_summary(method="all"):
    """Print summary of all torsion cases and combinations."""
    log.info("")
    log.info("  ╔════════════════════════════════════════════════════╗")
    log.info("  ║  TORSION ACCIDENTAL — SUMMARY                     ║")
    log.info("  ╠════════════════════════════════════════════════════╣")

    if method in ("a", "all"):
        log.info("  ║                                                    ║")
        log.info("  ║  METHOD A: Shift CM ±5%                            ║")
        log.info("  ║  ──────────────────────                            ║")
        log.info(f"  ║  NL Static: {AUX_PX}, {AUX_MX}, "
                 f"{AUX_PY}, {AUX_MY}{'':9s}║")
        log.info(f"  ║  Modal:     {MOD_PX}, {MOD_MX}, "
                 f"{MOD_PY}, {MOD_MY}{'':3s}║")
        log.info(f"  ║  RS X:      {SDX_A_PY}, {SDX_A_MY}{'':25s}║")
        log.info(f"  ║  RS Y:      {SDY_A_PX}, {SDY_A_MX}{'':25s}║")
        log.info("  ║  ⚠ Mass Sources must be set in GUI               ║")

    if method in ("b1", "all"):
        log.info("  ║                                                    ║")
        log.info("  ║  METHOD B-F1: Static Moments                       ║")
        log.info("  ║  ───────────────────────────                       ║")
        log.info(f"  ║  Patterns: {LP_TEX}, {LP_TEY} (Mz per floor)"
                 f"{'':14s}║")
        log.info("  ║  Combos: SDX±TEX, SDY±TEY                         ║")

    if method in ("b2", "all"):
        log.info("  ║                                                    ║")
        log.info("  ║  METHOD B-F2: Eccentricity 5%                      ║")
        log.info("  ║  ────────────────────────────                      ║")
        log.info(f"  ║  Cases: {SDTX_CASE} (U1±5%), "
                 f"{SDTY_CASE} (U2±5%){'':17s}║")
        log.info("  ║  ETABS handles ± envelope internally              ║")

    log.info("  ║                                                    ║")
    log.info("  ║  DIAPHRAGM TYPES                                   ║")
    log.info("  ║  ────────────────                                   ║")
    log.info(f"  ║  Rigid:     {DIAPHRAGM_RIGID_NAME}{'':39s}║")
    log.info(f"  ║  Semi-rigid: {DIAPHRAGM_SEMI_NAME}{'':34s}║")
    log.info("  ║  Cases 1-3: rigid | Cases 4-6: semi-rigid          ║")
    log.info("  ╚════════════════════════════════════════════════════╝")
    log.info("")


# ===================================================================
# SECTION 7: LOAD COMBINATIONS FOR TORSION CASES
# ===================================================================

def create_torsion_combinations(SapModel, method="b2"):
    """Create load combinations that include torsion effects.

    NCh3171 combinations with seismic cases that include torsion.

    For Method a:
      Uses SDX_aPY, SDX_aMY (max of ± CM shift) instead of SDX
    For Method b-F1:
      Uses SDX ± TEX (static torsion added/subtracted)
    For Method b-F2:
      Uses SDTX, SDTY (with built-in ±5% eccentricity)
    """
    log.info("  Creating load combinations with torsion...")

    # Define the seismic case names based on method
    if method == "a":
        # Method a: 4 RS cases (SDX+Y, SDX-Y, SDY+X, SDY-X)
        sx_cases = [SDX_A_PY, SDX_A_MY]
        sy_cases = [SDY_A_PX, SDY_A_MX]
        combos = _build_method_a_combos(sx_cases, sy_cases)
    elif method == "b1":
        # Method b-F1: SDX ± TEX, SDY ± TEY
        combos = _build_method_b1_combos()
    elif method == "b2":
        # Method b-F2: SDTX, SDTY (envelope built-in)
        combos = _build_method_b2_combos()
    else:
        log.warning(f"  Unknown method '{method}' for combinations")
        return

    # Create combinations in ETABS
    for combo_name, case_list in combos.items():
        try:
            ret = SapModel.RespCombo.Add(combo_name, 0)  # 0=LinearAdd
            check_ret(ret, f"RespCombo.Add('{combo_name}')")

            for cname_type, cname, sf in case_list:
                ret = SapModel.RespCombo.SetCaseList(
                    combo_name, cname_type, cname, sf,
                )
                check_ret(ret, f"SetCaseList('{combo_name}', "
                          f"'{cname}', {sf})")

            log.info(f"    {combo_name}: {len(case_list)} terms ✓")
        except Exception as e:
            log.warning(f"    {combo_name} failed: {e}")

    log.info(f"  Created {len(combos)} combinations ✓")
    log.info("")


def _build_method_a_combos(sx_cases, sy_cases):
    """Build NCh3171 combinations for Method a."""
    combos = {}
    # Gravity (same for all methods)
    combos['C1_a'] = [(0, 'PP', 1.4), (0, 'TERP', 1.4)]
    combos['C2_a'] = [(0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.6)]
    combos['C3_a'] = [(0, 'PP', 1.2), (0, 'TERP', 1.2),
                      (0, 'SCT', 1.6), (0, 'SCP', 0.5)]

    # Seismic X — use SDX_aPY and SDX_aMY (max of both)
    for i, sx in enumerate(sx_cases):
        suffix = f"a{i+1}"
        combos[f'C4_{suffix}'] = [
            (0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.0),
            (0, sx, 1.4),
        ]
        combos[f'C8_{suffix}'] = [
            (0, 'PP', 0.9), (0, 'TERP', 0.9), (0, sx, 1.4),
        ]

    # Seismic Y — use SDY_aPX and SDY_aMX (max of both)
    for i, sy in enumerate(sy_cases):
        suffix = f"a{i+1}"
        combos[f'C6_{suffix}'] = [
            (0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.0),
            (0, sy, 1.4),
        ]
        combos[f'C10_{suffix}'] = [
            (0, 'PP', 0.9), (0, 'TERP', 0.9), (0, sy, 1.4),
        ]

    return combos


def _build_method_b1_combos():
    """Build NCh3171 combinations for Method b-F1."""
    combos = {}
    # Gravity
    combos['C1_b1'] = [(0, 'PP', 1.4), (0, 'TERP', 1.4)]
    combos['C2_b1'] = [(0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.6)]
    combos['C3_b1'] = [(0, 'PP', 1.2), (0, 'TERP', 1.2),
                       (0, 'SCT', 1.6), (0, 'SCP', 0.5)]

    # Seismic X + torsion (SDX ± TEX)
    combos['C4_b1p'] = [
        (0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.0),
        (0, SDX_CASE, 1.4), (0, LP_TEX, 1.4),
    ]
    combos['C4_b1m'] = [
        (0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.0),
        (0, SDX_CASE, 1.4), (0, LP_TEX, -1.4),
    ]
    combos['C8_b1p'] = [
        (0, 'PP', 0.9), (0, 'TERP', 0.9),
        (0, SDX_CASE, 1.4), (0, LP_TEX, 1.4),
    ]
    combos['C8_b1m'] = [
        (0, 'PP', 0.9), (0, 'TERP', 0.9),
        (0, SDX_CASE, 1.4), (0, LP_TEX, -1.4),
    ]

    # Seismic Y + torsion (SDY ± TEY)
    combos['C6_b1p'] = [
        (0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.0),
        (0, SDY_CASE, 1.4), (0, LP_TEY, 1.4),
    ]
    combos['C6_b1m'] = [
        (0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.0),
        (0, SDY_CASE, 1.4), (0, LP_TEY, -1.4),
    ]
    combos['C10_b1p'] = [
        (0, 'PP', 0.9), (0, 'TERP', 0.9),
        (0, SDY_CASE, 1.4), (0, LP_TEY, 1.4),
    ]
    combos['C10_b1m'] = [
        (0, 'PP', 0.9), (0, 'TERP', 0.9),
        (0, SDY_CASE, 1.4), (0, LP_TEY, -1.4),
    ]

    return combos


def _build_method_b2_combos():
    """Build NCh3171 combinations for Method b-F2."""
    combos = {}
    # Gravity
    combos['C1_b2'] = [(0, 'PP', 1.4), (0, 'TERP', 1.4)]
    combos['C2_b2'] = [(0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.6)]
    combos['C3_b2'] = [(0, 'PP', 1.2), (0, 'TERP', 1.2),
                       (0, 'SCT', 1.6), (0, 'SCP', 0.5)]

    # Seismic X (SDTX has ±5% built-in)
    combos['C4_b2'] = [
        (0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.0),
        (0, SDTX_CASE, 1.4),
    ]
    combos['C8_b2'] = [
        (0, 'PP', 0.9), (0, 'TERP', 0.9), (0, SDTX_CASE, 1.4),
    ]

    # Seismic Y (SDTY has ±5% built-in)
    combos['C6_b2'] = [
        (0, 'PP', 1.2), (0, 'TERP', 1.2), (0, 'SCP', 1.0),
        (0, SDTY_CASE, 1.4),
    ]
    combos['C10_b2'] = [
        (0, 'PP', 0.9), (0, 'TERP', 0.9), (0, SDTY_CASE, 1.4),
    ]

    return combos


# ===================================================================
# SECTION 8: MAIN
# ===================================================================

def main():
    """Main entry point: configure accidental torsion."""
    parser = argparse.ArgumentParser(
        description="09_torsion.py — Accidental torsion for Edificio 1"
    )
    parser.add_argument(
        '--method', choices=['a', 'b1', 'b2', 'all'],
        default='all',
        help='Torsion method: a (shift CM), b1 (static moments), '
             'b2 (eccentricity), all (default)',
    )
    parser.add_argument(
        '--combos', action='store_true',
        help='Also create load combinations',
    )
    parser.add_argument(
        '--table-only', action='store_true',
        help='Only print eccentricity table (no ETABS connection)',
    )
    args = parser.parse_args()

    # Table-only mode (no ETABS needed)
    if args.table_only:
        print_eccentricity_table()
        return

    log.info("=" * 60)
    log.info("09_torsion.py — Accidental Torsion, Edificio 1")
    log.info("=" * 60)
    log.info("")
    log.info(f"  Method: {args.method}")
    log.info(f"  NCh433 Art. 6.3.4: ek = 0.10 × (zk/H) × b_perp")
    log.info(f"  H = {H_TOTAL:.2f}m | LX = {LX_PLANTA:.3f}m | "
             f"LY = {LY_PLANTA:.3f}m")
    log.info(f"  Uniform 5%: ea_X = {EA_X:.3f}m, ea_Y = {EA_Y:.3f}m")
    log.info("")

    # Print eccentricity table
    print_eccentricity_table()
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
        # Set units
        set_units(UNITS_TONF_M_C)
        log.info(f"  Units: Tonf_m_C (={UNITS_TONF_M_C})")
        log.info("")

        t_start = time.time()

        # -------------------------------------------------------
        # Execute selected method(s)
        # -------------------------------------------------------
        if args.method in ('a', 'all'):
            setup_method_a(SapModel)

        if args.method in ('b1', 'all'):
            setup_method_b_f1(SapModel)

        if args.method in ('b2', 'all'):
            setup_method_b_f2(SapModel)

        # -------------------------------------------------------
        # Create combinations if requested
        # -------------------------------------------------------
        if args.combos:
            if args.method == 'all':
                for m in ['a', 'b1', 'b2']:
                    create_torsion_combinations(SapModel, method=m)
            else:
                create_torsion_combinations(SapModel, method=args.method)

        t_elapsed = time.time() - t_start

        # -------------------------------------------------------
        # Verification
        # -------------------------------------------------------
        log.info("")
        ok = verify_torsion_cases(SapModel, method=args.method)

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Summary
        print_torsion_summary(method=args.method)

        # Final report
        log.info("=" * 60)
        log.info("RESULTS")
        log.info("=" * 60)

        if args.method in ('a', 'all'):
            log.info(f"  Method A: 4 NL Static + 4 Modal + 4 RS cases")
            log.info(f"    ⚠ Mass Sources require manual GUI config")

        if args.method in ('b1', 'all'):
            log.info(f"  Method B-F1: {LP_TEX}, {LP_TEY} patterns + "
                     "static cases")
            log.info(f"    Moments applied via PointObj.SetLoadForce")

        if args.method in ('b2', 'all'):
            log.info(f"  Method B-F2: {SDTX_CASE} (U1±5%), "
                     f"{SDTY_CASE} (U2±5%)")
            log.info(f"    Eccentricity applied via SetEccentricity")

        log.info(f"  Time: {t_elapsed:.1f}s")
        log.info(f"  Verification: {'PASS ✓' if ok else 'INCOMPLETE ⚠'}")
        log.info("")
        log.info("Ready for next step (10_save_run.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
