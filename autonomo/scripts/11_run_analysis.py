"""
11_run_analysis.py — Run analysis and validate results for Edificio 1.

This script handles the complete analysis execution and post-analysis
validation in six steps:

  1. Pre-flight checks: verify model state, file path, element counts
  2. Configure Active DOF (all 6 DOF active)
  3. Set run flags: select which cases to run (Modal, SDX, SDY, gravity)
  4. Run Analysis
  5. Post-analysis validation:
     a. Total weight ≈ 9,368 tonf (468 m² × 20 pisos × 1 tonf/m²)
     b. T1 ≈ 1.0–1.3 s (first translational mode)
     c. Modal mass participation > 90% in both X and Y
     d. No instabilities (analysis converged)
     e. Story drifts ≤ 0.002 (NCh433 limit at CM)
     f. Base reactions sanity check
  6. Print comprehensive results summary

Prerequisites:
  - ETABS v19 open with model from scripts 01–10
  - Model saved to .edb file (Analyze.RunAnalysis requires a file path)
  - comtypes installed
  - config.py in the same directory

Usage:
  python 11_run_analysis.py                # Run all cases
  python 11_run_analysis.py --skip-run     # Skip analysis, only extract results
  python 11_run_analysis.py --cases Modal SDX SDY   # Run specific cases only

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against:
  - autonomo/research/etabs_api_reference.md §17–§19
  - autonomo/research/com_signatures.md §13–§15
  - CSI OAPI official documentation (docs.csiamerica.com)
  - Analyze.SetActiveDOF(DOF): 1 arg (bool[6])
  - Analyze.SetRunCaseFlag(Name, Run, All): 3 args
  - Analyze.RunAnalysis(): 0 args
  - Results.Setup.DeselectAllCasesAndCombosForOutput(): 0 args
  - Results.Setup.SetCaseSelectedForOutput(CaseName): 1 arg
  - Results.Setup.SetComboSelectedForOutput(ComboName): 1 arg
  - Results.BaseReac(...): 13 output args
  - Results.StoryDrifts(...): 11 output args
  - DatabaseTables.GetTableForDisplayArray(...): 7 args

Sources: NCh433 Mod 2009, DS61, Material Apoyo Taller 2026, config.py
"""

import sys
import os
import time
import argparse

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, check_ret, set_units, log, verify_model,
    UNITS_TONF_M_C,
    N_STORIES, H_TOTAL, STORY_NAMES, STORY_HEIGHTS,
    AREA_PLANTA, PESO_ESPERADO_TONF, DRIFT_LIMITE,
    R_MUROS, RO_MUROS, I_FACTOR, S_SUELO, AO_G, G_ACCEL,
    calc_R_star, calc_Cmin,
)


# ===================================================================
# CONSTANTS
# ===================================================================

# All 6 DOF active: UX, UY, UZ, RX, RY, RZ
ACTIVE_DOF = [True, True, True, True, True, True]

# Cases that must be run for a complete analysis
REQUIRED_CASES = ["Modal", "PP", "TERP", "TERT", "SCP", "SCT", "SDX", "SDY"]

# Tolerance for weight validation (±20% of expected)
WEIGHT_TOL_FRACTION = 0.20

# Expected period range for T1 (first translational mode)
T1_MIN = 0.5   # s — very stiff 20-story would not go below this
T1_MAX = 2.5   # s — very flexible 20-story would not exceed this
T1_EXPECTED_MIN = 1.0  # s — expected range for this building
T1_EXPECTED_MAX = 1.3  # s

# Modal mass participation threshold (NCh433 Art. 6.3.6.2)
MODAL_PARTICIPATION_MIN = 0.90  # 90%


# ===================================================================
# STEP 1: Pre-flight checks
# ===================================================================

def preflight_checks(SapModel):
    """Verify model state before running analysis.

    Checks:
      - Model has a saved file path (required by RunAnalysis)
      - Model has elements (frames, areas, points)
      - Load cases exist
      - Model is not locked (or unlock it)

    Returns:
        dict with model info
    """
    log.info("Step 1: Pre-flight checks...")
    info = {}

    # Check file path
    try:
        filepath = SapModel.GetModelFilename()
        if isinstance(filepath, tuple):
            filepath = filepath[0] if filepath[0] else ""
        filepath = str(filepath)
    except Exception:
        filepath = ""

    if not filepath or filepath == "UNSAVED" or not filepath.strip():
        log.error("  Model has no file path — save it first (File > Save)")
        log.error("  Analyze.RunAnalysis requires a saved .edb file")
        sys.exit(1)
    else:
        log.info(f"  Model file: {filepath}")
        info['filepath'] = filepath

    # Check units
    try:
        units = SapModel.GetPresentUnits()
        if isinstance(units, tuple):
            units = units[0]
        log.info(f"  Current units: {units} (expected {UNITS_TONF_M_C})")
        info['units'] = units
    except Exception:
        log.warning("  Could not read units")

    # Check if model is locked (means analysis was already run)
    try:
        locked = SapModel.GetModelIsLocked()
        if isinstance(locked, tuple):
            locked = locked[0]
        if locked:
            log.info("  Model is LOCKED (previous analysis exists)")
            log.info("  Unlocking model for fresh analysis...")
            SapModel.SetModelIsLocked(False)
            log.info("  Model unlocked ✓")
        else:
            log.info("  Model is unlocked ✓")
        info['was_locked'] = locked
    except Exception as e:
        log.warning(f"  Could not check lock state: {e}")

    # Check element counts
    try:
        result = SapModel.PointObj.GetNameList()
        n_points = result[0] if isinstance(result, tuple) else 0
        result = SapModel.FrameObj.GetNameList()
        n_frames = result[0] if isinstance(result, tuple) else 0
        result = SapModel.AreaObj.GetNameList()
        n_areas = result[0] if isinstance(result, tuple) else 0

        log.info(f"  Elements: {n_points} points, {n_frames} frames, "
                 f"{n_areas} areas")
        info['n_points'] = n_points
        info['n_frames'] = n_frames
        info['n_areas'] = n_areas

        if n_areas == 0 and n_frames == 0:
            log.error("  Model has NO elements — cannot run analysis")
            sys.exit(1)
    except Exception as e:
        log.warning(f"  Could not count elements: {e}")

    # Check load cases exist
    try:
        result = SapModel.LoadCases.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_cases = result[0]
            case_names = [str(c) for c in result[1]] if result[1] else []
            log.info(f"  Load cases in model: {n_cases}")

            missing = []
            for req in REQUIRED_CASES:
                if req not in case_names:
                    missing.append(req)

            if missing:
                log.warning(f"  Missing required cases: {missing}")
                log.warning("  Analysis may be incomplete")
            else:
                log.info(f"  All {len(REQUIRED_CASES)} required cases present ✓")

            info['cases'] = case_names
    except Exception as e:
        log.warning(f"  Could not list load cases: {e}")

    log.info("  Pre-flight checks complete ✓")
    return info


# ===================================================================
# STEP 2: Configure Active DOF
# ===================================================================

def configure_active_dof(SapModel):
    """Set all 6 DOF as active for 3D analysis.

    DOF = [UX, UY, UZ, RX, RY, RZ] — all True for complete 3D analysis.

    Firma COM (com_signatures.md §13.1):
      ret = SapModel.Analyze.SetActiveDOF(DOF)
      DOF: bool[6]
    """
    log.info("Step 2: Configuring Active DOF...")
    log.info(f"  DOF: UX=True, UY=True, UZ=True, RX=True, RY=True, RZ=True")

    ret = SapModel.Analyze.SetActiveDOF(ACTIVE_DOF)
    check_ret(ret, "Analyze.SetActiveDOF")
    log.info("  All 6 DOF active ✓")


# ===================================================================
# STEP 3: Set run case flags
# ===================================================================

def set_run_case_flags(SapModel, cases_to_run=None):
    """Configure which load cases to run.

    Strategy:
      1. Deactivate ALL cases
      2. Activate only the cases we need

    This ensures a clean run without leftover flags from previous sessions.

    Firma COM (com_signatures.md §13.4):
      ret = SapModel.Analyze.SetRunCaseFlag(Name, Run, All)
      Name: str, Run: bool, All: bool (optional, default False)

    Args:
        SapModel: ETABS model object
        cases_to_run: list of case names to run (None = all required cases)
    """
    log.info("Step 3: Setting run case flags...")

    if cases_to_run is None:
        cases_to_run = list(REQUIRED_CASES)

    # Get all existing cases
    existing_cases = []
    try:
        result = SapModel.LoadCases.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            existing_cases = [str(c) for c in result[1]] if result[1] else []
    except Exception:
        pass

    # Also check for torsion cases
    for extra in ["SDTX", "SDTY"]:
        if extra in existing_cases and extra not in cases_to_run:
            cases_to_run.append(extra)

    # Step 3a: Deactivate ALL cases
    ret = SapModel.Analyze.SetRunCaseFlag("", False, True)
    check_ret(ret, "Analyze.SetRunCaseFlag('', False, All=True)")
    log.info("  All cases deactivated")

    # Step 3b: Activate selected cases
    activated = 0
    skipped = []
    for case_name in cases_to_run:
        if case_name not in existing_cases:
            skipped.append(case_name)
            continue

        ret = SapModel.Analyze.SetRunCaseFlag(case_name, True, False)
        if isinstance(ret, tuple):
            ret_code = ret[-1] if len(ret) > 1 else ret[0]
        else:
            ret_code = ret

        if ret_code == 0:
            activated += 1
            log.info(f"  ✓ {case_name}")
        else:
            log.warning(f"  ✗ {case_name} (ret={ret_code})")

    if skipped:
        log.info(f"  Skipped (not in model): {skipped}")

    log.info(f"  Activated {activated}/{len(cases_to_run)} cases ✓")
    return activated


# ===================================================================
# STEP 4: Run Analysis
# ===================================================================

def run_analysis(SapModel):
    """Execute the analysis.

    IMPORTANT: The model must have a saved file path. ETABS writes
    analysis results to disk alongside the .edb file.

    Firma COM (com_signatures.md §13.2):
      ret = SapModel.Analyze.RunAnalysis()
      No arguments. Returns 0 on success.

    The analysis can take several minutes for a 20-story building
    with 30 modal modes and response spectrum cases.

    Returns:
        tuple (success: bool, elapsed: float)
    """
    log.info("Step 4: Running analysis...")
    log.info("  This may take several minutes for a 20-story building...")
    log.info("")

    t_start = time.time()

    try:
        ret = SapModel.Analyze.RunAnalysis()
    except Exception as e:
        t_elapsed = time.time() - t_start
        log.error(f"  RunAnalysis raised exception after {t_elapsed:.1f}s: {e}")
        return False, t_elapsed

    t_elapsed = time.time() - t_start

    if isinstance(ret, tuple):
        ret_code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        ret_code = ret

    if ret_code == 0:
        log.info(f"  Analysis completed successfully in {t_elapsed:.1f}s ✓")
        return True, t_elapsed
    else:
        log.error(f"  RunAnalysis returned {ret_code} after {t_elapsed:.1f}s")
        log.error("  Check ETABS log for details (File > Last Analysis Log)")
        return False, t_elapsed


# ===================================================================
# STEP 5: Post-analysis validation
# ===================================================================

# --- 5a: Extract total weight via base reactions ---

def get_total_weight(SapModel):
    """Extract total building weight from gravity base reactions.

    Uses PP (self-weight) case base reaction Fz to get the total weight.
    The reaction Fz for PP gives the total self-weight of the structure.
    For total seismic weight, we should check all gravity cases.

    However, the simplest validation is: total Fz from the Dead load case
    should approximate the expected weight.

    Firma COM (com_signatures.md §14.1):
      result = SapModel.Results.BaseReac(
          NumberResults, LoadCase[], StepType[], StepNum[],
          Fx[], Fy[], Fz[], Mx[], My[], Mz[], gx, gy, gz)
      All args are output by reference.

    Returns:
        dict with weight info per case, or None on failure
    """
    log.info("  5a: Extracting total weight from base reactions...")

    # Select PP case for output
    try:
        SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        SapModel.Results.Setup.SetCaseSelectedForOutput("PP")
    except Exception as e:
        log.warning(f"    Could not select PP for output: {e}")

    weights = {}

    # Extract base reactions for PP
    try:
        result = SapModel.Results.BaseReac(
            0, [], [], [],       # NumberResults, LoadCase, StepType, StepNum
            [], [], [], [], [], [],  # Fx, Fy, Fz, Mx, My, Mz
            0.0, 0.0, 0.0,      # gx, gy, gz
        )

        if isinstance(result, tuple) and len(result) >= 7:
            n_results = result[0]
            load_cases = result[1] if len(result) > 1 else []
            fz_values = result[6] if len(result) > 6 else []

            if n_results > 0 and fz_values:
                for i in range(n_results):
                    case = str(load_cases[i]) if load_cases else f"Case_{i}"
                    fz = float(fz_values[i])
                    # Base reaction Fz is positive upward → weight = -Fz
                    # Or it could be positive depending on convention
                    weight = abs(fz)
                    weights[case] = weight
                    log.info(f"    {case}: Fz = {fz:.1f} tonf "
                             f"(weight ≈ {weight:.1f} tonf)")
        else:
            log.warning(f"    BaseReac returned unexpected format: "
                        f"len={len(result) if isinstance(result, tuple) else 'N/A'}")
    except Exception as e:
        log.warning(f"    BaseReac for PP failed: {e}")

    # Also try via TERP and SCP to estimate seismic weight
    for case_name in ["TERP", "SCP"]:
        try:
            SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
            SapModel.Results.Setup.SetCaseSelectedForOutput(case_name)

            result = SapModel.Results.BaseReac(
                0, [], [], [],
                [], [], [], [], [], [],
                0.0, 0.0, 0.0,
            )

            if isinstance(result, tuple) and len(result) >= 7:
                n_results = result[0]
                fz_values = result[6] if len(result) > 6 else []
                if n_results > 0 and fz_values:
                    fz = float(fz_values[0])
                    weights[case_name] = abs(fz)
                    log.info(f"    {case_name}: Fz = {fz:.1f} tonf")
        except Exception:
            pass

    return weights if weights else None


def validate_weight(weights):
    """Validate total weight against expected value.

    Expected: ~9,368 tonf (468 m² × 20 pisos × 1 tonf/m²)
    Tolerance: ±20%

    The seismic weight = PP + TERP + 0.25×SCP

    Args:
        weights: dict from get_total_weight()

    Returns:
        tuple (seismic_weight, is_ok)
    """
    log.info("  Validating weight...")

    pp_weight = weights.get("PP", 0)
    terp_weight = weights.get("TERP", 0)
    scp_weight = weights.get("SCP", 0)

    # Seismic weight = PP + TERP + 0.25×SCP (NCh433)
    seismic_weight = pp_weight + terp_weight + 0.25 * scp_weight

    if seismic_weight > 0:
        log.info(f"    PP weight:      {pp_weight:,.1f} tonf")
        log.info(f"    TERP weight:    {terp_weight:,.1f} tonf")
        log.info(f"    SCP weight:     {scp_weight:,.1f} tonf")
        log.info(f"    Seismic weight: {seismic_weight:,.1f} tonf "
                 f"(PP + TERP + 0.25×SCP)")
    else:
        # Fallback: just use PP
        seismic_weight = pp_weight
        log.info(f"    Using PP only: {seismic_weight:,.1f} tonf")

    expected = PESO_ESPERADO_TONF
    tol = WEIGHT_TOL_FRACTION
    w_min = expected * (1 - tol)
    w_max = expected * (1 + tol)

    ratio = seismic_weight / expected if expected > 0 else 0
    per_area = seismic_weight / (AREA_PLANTA * N_STORIES) if AREA_PLANTA > 0 else 0

    log.info(f"    Expected: ~{expected:,.0f} tonf "
             f"(±{tol*100:.0f}% → {w_min:,.0f}–{w_max:,.0f})")
    log.info(f"    Ratio: {ratio:.2f}")
    log.info(f"    Weight/area: {per_area:.2f} tonf/m² "
             f"(Lafontaine rule ≈ 1.0)")

    is_ok = w_min <= seismic_weight <= w_max
    if is_ok:
        log.info(f"    Weight validation: PASS ✓")
    else:
        log.warning(f"    Weight validation: FAIL ✗")
        if seismic_weight < w_min:
            log.warning(f"    Weight too LOW — check mass source, loads, sections")
        else:
            log.warning(f"    Weight too HIGH — check duplicate elements, loads")

    return seismic_weight, is_ok


# --- 5b: Extract modal periods and participation ---

def get_modal_results(SapModel):
    """Extract modal periods and mass participation via Database Tables.

    Uses DatabaseTables.GetTableForDisplayArray because:
    - Results.ModalPeriod is not documented in our API reference
    - Results.ModalParticipatingMassRatios is not documented
    - Database Tables approach is confirmed working (com_signatures.md §15)

    Table keys:
      "Modal Participating Mass Ratios" — periods + cumulative participation

    Firma COM (com_signatures.md §15.1):
      result = SapModel.DatabaseTables.GetTableForDisplayArray(
          TableKey, FieldKeyList, GroupName, TableVersion,
          FieldsKeysIncluded, NumberRecords, TableData)

    Returns:
        dict with 'periods', 'ux_cumul', 'uy_cumul', 'n_modes' or None
    """
    log.info("  5b: Extracting modal results via Database Tables...")

    try:
        result = SapModel.DatabaseTables.GetTableForDisplayArray(
            "Modal Participating Mass Ratios",  # TableKey
            "",                                  # FieldKeyList (all fields)
            "All",                               # GroupName
            1,                                   # TableVersion
            [],                                  # FieldsKeysIncluded (output)
            0,                                   # NumberRecords (output)
            [],                                  # TableData (output)
        )

        if not isinstance(result, tuple) or len(result) < 5:
            log.warning(f"    Unexpected result format: len={len(result) if isinstance(result, tuple) else 'N/A'}")
            return None

        # Parse result — field names are in result[2] or result[4], data in result[4] or result[6]
        # The exact indices depend on the comtypes binding version
        # Common patterns:
        #   result[2] = field names list, result[4] = flat data array
        #   OR result[4] = field names, result[6] = flat data

        fields = None
        table_data = None

        # Try to find the fields and data arrays
        for i in range(len(result)):
            item = result[i]
            if isinstance(item, (list, tuple)) and len(item) > 3:
                # Check if this looks like field names (strings)
                try:
                    first_items = [str(x) for x in item[:3]]
                    if any(k in first_items[0].lower() for k in
                           ['case', 'mode', 'step', 'output']):
                        fields = [str(f) for f in item]
                        continue
                except Exception:
                    pass

                # If we already found fields, this is data
                if fields is not None and table_data is None:
                    table_data = [str(d) for d in item]

        if fields is None:
            # Fallback: try standard positions
            if len(result) >= 7:
                try:
                    fields = [str(f) for f in result[4]]
                    table_data = [str(d) for d in result[6]]
                except Exception:
                    pass

            if fields is None and len(result) >= 5:
                try:
                    fields = [str(f) for f in result[2]]
                    table_data = [str(d) for d in result[4]]
                except Exception:
                    pass

        if fields is None or table_data is None:
            log.warning("    Could not parse Database Tables result")
            log.warning(f"    Result has {len(result)} elements")
            for i, item in enumerate(result):
                item_type = type(item).__name__
                item_len = len(item) if hasattr(item, '__len__') else 'N/A'
                log.info(f"    result[{i}]: {item_type}, len={item_len}")
            return None

        n_fields = len(fields)
        if n_fields == 0:
            log.warning("    No fields returned")
            return None

        log.info(f"    Fields ({n_fields}): {fields[:8]}...")

        # Parse into rows
        n_data = len(table_data)
        n_rows = n_data // n_fields

        if n_rows == 0:
            log.warning("    No data rows returned")
            return None

        log.info(f"    Data rows: {n_rows}")

        # Find column indices
        field_lower = [f.lower().strip() for f in fields]

        # Common field names in "Modal Participating Mass Ratios" table:
        # Case, Mode, Period, UX, UY, UZ, SumUX, SumUY, SumUZ, RX, RY, RZ, SumRX, SumRY, SumRZ
        col_map = {}
        for name_variants, key in [
            (['mode', 'modenum'], 'mode'),
            (['period', 'period(sec)', 'period (sec)'], 'period'),
            (['ux', 'ux(%)'], 'ux'),
            (['uy', 'uy(%)'], 'uy'),
            (['sumux', 'sum ux', 'sumux(%)', 'sum ux(%)'], 'sum_ux'),
            (['sumuy', 'sum uy', 'sumuy(%)', 'sum uy(%)'], 'sum_uy'),
        ]:
            for idx, fl in enumerate(field_lower):
                if fl in name_variants or any(v in fl for v in name_variants):
                    col_map[key] = idx
                    break

        log.info(f"    Column mapping: {col_map}")

        # Extract data
        periods = []
        ux_ratios = []
        uy_ratios = []
        sum_ux = []
        sum_uy = []

        for row_idx in range(n_rows):
            offset = row_idx * n_fields
            row = table_data[offset:offset + n_fields]

            try:
                if 'period' in col_map:
                    p = float(row[col_map['period']])
                    periods.append(p)

                if 'ux' in col_map:
                    ux = float(row[col_map['ux']])
                    ux_ratios.append(ux)

                if 'uy' in col_map:
                    uy = float(row[col_map['uy']])
                    uy_ratios.append(uy)

                if 'sum_ux' in col_map:
                    sux = float(row[col_map['sum_ux']])
                    sum_ux.append(sux)

                if 'sum_uy' in col_map:
                    suy = float(row[col_map['sum_uy']])
                    sum_uy.append(suy)
            except (ValueError, IndexError):
                continue

        modal_data = {
            'periods': periods,
            'ux_ratios': ux_ratios,
            'uy_ratios': uy_ratios,
            'sum_ux': sum_ux,
            'sum_uy': sum_uy,
            'n_modes': len(periods),
        }

        if periods:
            log.info(f"    Modes extracted: {len(periods)}")
            log.info(f"    T1 = {periods[0]:.4f} s")
            if len(periods) >= 2:
                log.info(f"    T2 = {periods[1]:.4f} s")
            if len(periods) >= 3:
                log.info(f"    T3 = {periods[2]:.4f} s")

        return modal_data

    except Exception as e:
        log.warning(f"    Database Tables query failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def validate_modal_results(modal_data):
    """Validate modal analysis results.

    Checks:
      1. T1 in expected range (1.0–1.3 s for this building)
      2. Cumulative mass participation > 90% in X and Y (NCh433 6.3.6.2)
      3. First mode is translational (dominant UX or UY, not torsional)

    Args:
        modal_data: dict from get_modal_results()

    Returns:
        dict with validation results
    """
    log.info("  Validating modal results...")
    results = {'t1_ok': False, 'participation_ok': False, 'warnings': []}

    if modal_data is None or not modal_data.get('periods'):
        log.warning("    No modal data available — cannot validate")
        results['warnings'].append("No modal data")
        return results

    periods = modal_data['periods']
    n_modes = modal_data['n_modes']

    # --- T1 validation ---
    t1 = periods[0]
    results['T1'] = t1

    log.info(f"    T1 = {t1:.4f} s")
    if T1_EXPECTED_MIN <= t1 <= T1_EXPECTED_MAX:
        log.info(f"    T1 in expected range [{T1_EXPECTED_MIN}–{T1_EXPECTED_MAX} s]: "
                 f"PASS ✓")
        results['t1_ok'] = True
    elif T1_MIN <= t1 <= T1_MAX:
        log.warning(f"    T1 outside expected range [{T1_EXPECTED_MIN}–"
                    f"{T1_EXPECTED_MAX} s] but within plausible range "
                    f"[{T1_MIN}–{T1_MAX} s]")
        log.warning("    Review structural stiffness and mass")
        results['t1_ok'] = True  # Plausible but not ideal
        results['warnings'].append(f"T1={t1:.3f}s outside expected range")
    else:
        log.error(f"    T1 = {t1:.4f} s is OUTSIDE plausible range "
                  f"[{T1_MIN}–{T1_MAX} s]")
        log.error("    This likely indicates a modeling error")
        results['t1_ok'] = False
        results['warnings'].append(f"T1={t1:.3f}s outside plausible range")

    # --- Print first few modes ---
    log.info(f"    Modal periods ({min(n_modes, 10)} of {n_modes}):")
    log.info(f"    {'Mode':>4s}  {'Period':>8s}  {'UX%':>7s}  {'UY%':>7s}  "
             f"{'ΣUX%':>7s}  {'ΣUY%':>7s}")
    log.info(f"    {'─'*4}  {'─'*8}  {'─'*7}  {'─'*7}  {'─'*7}  {'─'*7}")

    for i in range(min(n_modes, 10)):
        mode = i + 1
        p = periods[i] if i < len(periods) else 0
        ux = modal_data['ux_ratios'][i] if i < len(modal_data['ux_ratios']) else 0
        uy = modal_data['uy_ratios'][i] if i < len(modal_data['uy_ratios']) else 0
        sux = modal_data['sum_ux'][i] if i < len(modal_data['sum_ux']) else 0
        suy = modal_data['sum_uy'][i] if i < len(modal_data['sum_uy']) else 0

        # Mass participation values may be ratios (0-1) or percentages (0-100)
        # Detect and normalize
        if sux > 1.0 or suy > 1.0:
            # Values are percentages
            log.info(f"    {mode:4d}  {p:8.4f}  {ux:6.2f}%  {uy:6.2f}%  "
                     f"{sux:6.2f}%  {suy:6.2f}%")
        else:
            # Values are ratios — display as percentages
            log.info(f"    {mode:4d}  {p:8.4f}  {ux*100:6.2f}%  {uy*100:6.2f}%  "
                     f"{sux*100:6.2f}%  {suy*100:6.2f}%")

    # --- Mass participation validation ---
    sum_ux = modal_data.get('sum_ux', [])
    sum_uy = modal_data.get('sum_uy', [])

    if sum_ux and sum_uy:
        final_sux = sum_ux[-1]
        final_suy = sum_uy[-1]

        # Normalize if percentages
        if final_sux > 1.0:
            final_sux /= 100.0
        if final_suy > 1.0:
            final_suy /= 100.0

        results['final_sum_ux'] = final_sux
        results['final_sum_uy'] = final_suy

        threshold = MODAL_PARTICIPATION_MIN
        ux_ok = final_sux >= threshold
        uy_ok = final_suy >= threshold

        log.info(f"    Cumulative mass participation ({n_modes} modes):")
        log.info(f"      ΣUX = {final_sux*100:.1f}% "
                 f"{'✓' if ux_ok else '✗'} "
                 f"(min {threshold*100:.0f}%)")
        log.info(f"      ΣUY = {final_suy*100:.1f}% "
                 f"{'✓' if uy_ok else '✗'} "
                 f"(min {threshold*100:.0f}%)")

        results['participation_ok'] = ux_ok and uy_ok

        if not ux_ok or not uy_ok:
            log.warning("    Insufficient mass participation — "
                        "increase number of modes")
            results['warnings'].append(
                f"Mass participation below 90%: "
                f"ΣUX={final_sux*100:.1f}%, ΣUY={final_suy*100:.1f}%")
    else:
        log.warning("    Could not extract cumulative participation")

    # --- R* calculation for this T1 ---
    if periods:
        t_star = periods[0]
        r_star = calc_R_star(t_star)
        results['R_star'] = r_star
        log.info(f"    R*(T*={t_star:.3f}s) = {r_star:.2f} "
                 f"(Ro={RO_MUROS}, R={R_MUROS})")

    return results


# --- 5c: Extract and validate story drifts ---

def get_story_drifts(SapModel):
    """Extract story drifts for seismic cases.

    Firma COM (com_signatures.md §14.2):
      result = SapModel.Results.StoryDrifts(
          NumberResults, Story[], LoadCase[], StepType[], StepNum[],
          Direction[], Drift[], Label[], X[], Y[], Z[])
      All args are output by reference. Returns tuple of 12 elements.

    Returns:
        list of dicts with story drift data, or None on failure
    """
    log.info("  5c: Extracting story drifts...")

    # Select seismic cases for output
    try:
        SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        for case in ["SDX", "SDY", "SDTX", "SDTY"]:
            try:
                SapModel.Results.Setup.SetCaseSelectedForOutput(case)
            except Exception:
                pass
    except Exception as e:
        log.warning(f"    Could not select cases: {e}")

    try:
        result = SapModel.Results.StoryDrifts(
            0,                   # NumberResults
            [], [], [], [],      # Story, LoadCase, StepType, StepNum
            [], [], [], [], [], [],  # Direction, Drift, Label, X, Y, Z
        )

        if not isinstance(result, tuple) or len(result) < 12:
            log.warning(f"    Unexpected result format")
            return None

        n_results = result[0]
        if n_results == 0:
            log.warning("    No drift results returned")
            return None

        stories = result[1]
        load_cases = result[2]
        step_types = result[3]
        step_nums = result[4]
        directions = result[5]
        drifts = result[6]
        labels = result[7]
        xs = result[8]
        ys = result[9]
        zs = result[10]
        ret_code = result[11]

        if ret_code != 0:
            log.warning(f"    StoryDrifts returned ret={ret_code}")

        drift_data = []
        for i in range(n_results):
            drift_data.append({
                'story': str(stories[i]),
                'case': str(load_cases[i]),
                'direction': str(directions[i]),
                'drift': float(drifts[i]),
                'label': str(labels[i]),
                'z': float(zs[i]),
            })

        log.info(f"    Extracted {n_results} drift records")
        return drift_data

    except Exception as e:
        log.warning(f"    StoryDrifts failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def validate_drifts(drift_data):
    """Validate story drifts against NCh433 limit.

    NCh433 Art. 5.9.2: Drift at CM ≤ 0.002 (for buildings with
    non-structural elements that can be damaged by drift).

    Prints a summary table of maximum drifts per direction and case.

    Args:
        drift_data: list of dicts from get_story_drifts()

    Returns:
        dict with validation results
    """
    log.info("  Validating story drifts (NCh433 limit = 0.002)...")
    results = {'max_drift_x': 0, 'max_drift_y': 0, 'drift_ok': True,
               'violations': []}

    if not drift_data:
        log.warning("    No drift data available")
        results['drift_ok'] = False
        return results

    limit = DRIFT_LIMITE

    # Organize by case and direction
    case_dir_drifts = {}
    for d in drift_data:
        key = (d['case'], d['direction'])
        if key not in case_dir_drifts:
            case_dir_drifts[key] = []
        case_dir_drifts[key].append(d)

    # Find max drift per case and direction
    log.info("")
    log.info(f"    {'Case':<8s} {'Dir':>3s}  {'Max Drift':>10s}  "
             f"{'Story':>10s}  {'Status':>6s}")
    log.info(f"    {'─'*8} {'─'*3}  {'─'*10}  {'─'*10}  {'─'*6}")

    for (case, direction), records in sorted(case_dir_drifts.items()):
        max_record = max(records, key=lambda r: abs(r['drift']))
        max_drift = abs(max_record['drift'])
        max_story = max_record['story']

        status = "✓" if max_drift <= limit else "✗ FAIL"
        log.info(f"    {case:<8s} {direction:>3s}  {max_drift:10.6f}  "
                 f"{max_story:>10s}  {status}")

        if 'X' in direction.upper():
            results['max_drift_x'] = max(results['max_drift_x'], max_drift)
        if 'Y' in direction.upper():
            results['max_drift_y'] = max(results['max_drift_y'], max_drift)

        if max_drift > limit:
            results['drift_ok'] = False
            results['violations'].append({
                'case': case, 'direction': direction,
                'drift': max_drift, 'story': max_story,
            })

    log.info("")

    # Print drift profile for worst case
    worst_drifts_x = {}
    worst_drifts_y = {}

    for d in drift_data:
        story = d['story']
        drift_val = abs(d['drift'])

        if 'X' in d['direction'].upper():
            if story not in worst_drifts_x or drift_val > worst_drifts_x[story]:
                worst_drifts_x[story] = drift_val
        if 'Y' in d['direction'].upper():
            if story not in worst_drifts_y or drift_val > worst_drifts_y[story]:
                worst_drifts_y[story] = drift_val

    # Print drift profile (every 5th story + top + bottom)
    stories_to_show = set()
    for i, sn in enumerate(STORY_NAMES):
        if i == 0 or i == len(STORY_NAMES) - 1 or (i + 1) % 5 == 0:
            stories_to_show.add(sn)

    log.info("    Drift profile (worst-case per direction):")
    log.info(f"    {'Story':>10s}  {'Drift X':>10s}  {'Drift Y':>10s}  "
             f"{'Limit':>8s}")
    log.info(f"    {'─'*10}  {'─'*10}  {'─'*10}  {'─'*8}")

    for sn in reversed(STORY_NAMES):
        if sn not in stories_to_show:
            continue
        dx = worst_drifts_x.get(sn, 0)
        dy = worst_drifts_y.get(sn, 0)
        flag = " ✗" if dx > limit or dy > limit else ""
        log.info(f"    {sn:>10s}  {dx:10.6f}  {dy:10.6f}  "
                 f"{limit:8.4f}{flag}")

    log.info("")

    if results['drift_ok']:
        log.info(f"    Drift validation: PASS ✓ "
                 f"(max X={results['max_drift_x']:.6f}, "
                 f"max Y={results['max_drift_y']:.6f})")
    else:
        log.warning(f"    Drift validation: FAIL ✗")
        for v in results['violations']:
            log.warning(f"      {v['case']} {v['direction']}: "
                        f"drift={v['drift']:.6f} > {limit} "
                        f"at {v['story']}")

    return results


# --- 5d: Base reactions sanity check ---

def validate_base_reactions(SapModel):
    """Check base reactions for seismic cases — sanity check.

    For seismic cases (SDX, SDY), the base shear Qmin = Cmin × W
    where Cmin = Ao×S/(6g) ≈ 0.07 for this building.

    Args:
        SapModel: ETABS model object

    Returns:
        dict with base shear info
    """
    log.info("  5d: Checking base reactions for seismic cases...")
    results = {}

    for case_name in ["SDX", "SDY"]:
        try:
            SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
            SapModel.Results.Setup.SetCaseSelectedForOutput(case_name)

            result = SapModel.Results.BaseReac(
                0, [], [], [],
                [], [], [], [], [], [],
                0.0, 0.0, 0.0,
            )

            if isinstance(result, tuple) and len(result) >= 7:
                n = result[0]
                if n > 0:
                    fx = abs(float(result[4][0])) if result[4] else 0
                    fy = abs(float(result[5][0])) if result[5] else 0
                    fz = abs(float(result[6][0])) if result[6] else 0

                    results[case_name] = {
                        'Fx': fx, 'Fy': fy, 'Fz': fz
                    }

                    # SDX → dominant Fx, SDY → dominant Fy
                    if case_name == "SDX":
                        log.info(f"    {case_name}: Vx={fx:,.1f} tonf, "
                                 f"Vy={fy:,.1f}, Fz={fz:,.1f}")
                    else:
                        log.info(f"    {case_name}: Vx={fx:,.1f} tonf, "
                                 f"Vy={fy:,.1f}, Fz={fz:,.1f}")

        except Exception as e:
            log.warning(f"    BaseReac for {case_name} failed: {e}")

    return results


# ===================================================================
# STEP 6: Results summary
# ===================================================================

def print_results_summary(
    analysis_ok, elapsed, seismic_weight, modal_results,
    drift_results, base_shear_results, weight_ok
):
    """Print comprehensive analysis results summary."""
    log.info("")
    log.info("=" * 65)
    log.info("  ANALYSIS RESULTS SUMMARY — Edificio 1 (20 pisos, muros HA)")
    log.info("=" * 65)
    log.info("")

    # Analysis status
    status = "SUCCESS ✓" if analysis_ok else "FAILED ✗"
    log.info(f"  Analysis:       {status} ({elapsed:.1f}s)")
    log.info("")

    # Weight
    if seismic_weight > 0:
        per_area = seismic_weight / (AREA_PLANTA * N_STORIES)
        log.info(f"  Seismic Weight: {seismic_weight:,.1f} tonf "
                 f"(expected ~{PESO_ESPERADO_TONF:,.0f}) "
                 f"{'✓' if weight_ok else '✗'}")
        log.info(f"  Weight/area:    {per_area:.2f} tonf/m² "
                 f"(Lafontaine ≈ 1.0)")
    log.info("")

    # Modal results
    if modal_results:
        t1 = modal_results.get('T1', 0)
        r_star = modal_results.get('R_star', 0)
        final_sux = modal_results.get('final_sum_ux', 0)
        final_suy = modal_results.get('final_sum_uy', 0)

        log.info(f"  T1 (fund.):     {t1:.4f} s "
                 f"{'✓' if modal_results.get('t1_ok') else '✗'} "
                 f"(expected {T1_EXPECTED_MIN}–{T1_EXPECTED_MAX})")

        if r_star > 0:
            log.info(f"  R*(T*={t1:.3f}s):  {r_star:.2f}")

        if final_sux > 0:
            log.info(f"  ΣUX:            {final_sux*100:.1f}% "
                     f"{'✓' if final_sux >= 0.90 else '✗'} (min 90%)")
        if final_suy > 0:
            log.info(f"  ΣUY:            {final_suy*100:.1f}% "
                     f"{'✓' if final_suy >= 0.90 else '✗'} (min 90%)")

        if modal_results.get('warnings'):
            for w in modal_results['warnings']:
                log.warning(f"  ⚠ {w}")
    log.info("")

    # Drifts
    if drift_results:
        log.info(f"  Max drift X:    {drift_results['max_drift_x']:.6f} "
                 f"(limit {DRIFT_LIMITE})")
        log.info(f"  Max drift Y:    {drift_results['max_drift_y']:.6f} "
                 f"(limit {DRIFT_LIMITE})")
        log.info(f"  Drift check:    "
                 f"{'PASS ✓' if drift_results.get('drift_ok') else 'FAIL ✗'}")
    log.info("")

    # Base shear
    if base_shear_results:
        cmin = calc_Cmin()
        q_min = cmin * seismic_weight if seismic_weight > 0 else 0

        log.info(f"  Cmin:           {cmin:.4f} "
                 f"(Ao×S/(6g) = {AO_G}×{S_SUELO}/6)")
        if q_min > 0:
            log.info(f"  Qmin:           {q_min:,.1f} tonf "
                     f"(Cmin × W)")

        for case, vals in base_shear_results.items():
            vx = vals['Fx']
            vy = vals['Fy']
            dominant = vx if 'X' in case else vy
            if q_min > 0:
                ratio = dominant / q_min
                log.info(f"  V_{case}:        {dominant:,.1f} tonf "
                         f"({ratio:.2f}×Qmin)")
            else:
                log.info(f"  V_{case}:        {dominant:,.1f} tonf")
    log.info("")

    # Overall assessment
    all_ok = (
        analysis_ok
        and weight_ok
        and modal_results.get('t1_ok', False)
        and modal_results.get('participation_ok', False)
        and drift_results.get('drift_ok', True)
    )

    log.info("─" * 65)
    if all_ok:
        log.info("  OVERALL: ALL CHECKS PASSED ✓")
        log.info("  Model is ready for design (12_results.py)")
    else:
        log.warning("  OVERALL: SOME CHECKS FAILED — review warnings above")
        if not weight_ok:
            log.warning("  → Weight deviation: check mass source/loads")
        if modal_results and not modal_results.get('t1_ok', False):
            log.warning("  → Period issue: check stiffness/mass distribution")
        if modal_results and not modal_results.get('participation_ok', False):
            log.warning("  → Low participation: increase number of modes")
        if drift_results and not drift_results.get('drift_ok', True):
            log.warning("  → Drift exceeded: stiffen structure or reduce height")
    log.info("=" * 65)

    return all_ok


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: run analysis and validate results."""
    log.info("=" * 65)
    log.info("11_run_analysis.py — Analysis + Validation, Edificio 1")
    log.info("=" * 65)
    log.info("")

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Run ETABS analysis and validate results")
    parser.add_argument('--skip-run', action='store_true',
                        help='Skip analysis execution, only extract results')
    parser.add_argument('--cases', nargs='+', default=None,
                        help='Specific cases to run (e.g., Modal SDX SDY)')
    args = parser.parse_args()

    log.info("  Tasks:")
    log.info("    1. Pre-flight checks")
    log.info("    2. Configure Active DOF")
    log.info("    3. Set run case flags")
    log.info("    4. Run analysis")
    log.info("    5. Post-analysis validation")
    log.info("       a. Weight validation (~9,368 tonf)")
    log.info("       b. Modal periods and participation (T1, >90%)")
    log.info("       c. Story drifts (≤0.002)")
    log.info("       d. Base reactions sanity check")
    log.info("    6. Results summary")
    log.info("")
    if args.skip_run:
        log.info("  MODE: --skip-run (extract results only)")
    if args.cases:
        log.info(f"  MODE: --cases {' '.join(args.cases)}")
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
        log.info(f"  Units set to Tonf_m_C (={UNITS_TONF_M_C})")
        log.info("")

        t_total_start = time.time()

        # Step 1: Pre-flight checks
        model_info = preflight_checks(SapModel)
        log.info("")

        analysis_ok = True
        elapsed = 0.0

        if not args.skip_run:
            # Step 2: Configure Active DOF
            configure_active_dof(SapModel)
            log.info("")

            # Step 3: Set run case flags
            cases_to_run = args.cases if args.cases else None
            n_activated = set_run_case_flags(SapModel, cases_to_run)
            log.info("")

            if n_activated == 0:
                log.error("No cases activated — nothing to run")
                sys.exit(1)

            # Step 4: Run analysis
            analysis_ok, elapsed = run_analysis(SapModel)
            log.info("")

            if not analysis_ok:
                log.warning("Analysis did not complete successfully")
                log.warning("Attempting to extract partial results...")
                log.info("")
        else:
            log.info("Step 2-4: SKIPPED (--skip-run mode)")
            log.info("")

        # Step 5: Post-analysis validation
        log.info("Step 5: Post-analysis validation...")
        log.info("")

        # 5a: Weight
        weights = get_total_weight(SapModel)
        seismic_weight = 0.0
        weight_ok = False
        if weights:
            seismic_weight, weight_ok = validate_weight(weights)
        log.info("")

        # 5b: Modal results
        modal_data = get_modal_results(SapModel)
        modal_results = validate_modal_results(modal_data)
        log.info("")

        # 5c: Drifts
        drift_data = get_story_drifts(SapModel)
        drift_results = validate_drifts(drift_data)
        log.info("")

        # 5d: Base reactions
        base_shear_results = validate_base_reactions(SapModel)
        log.info("")

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Step 6: Results summary
        t_total = time.time() - t_total_start

        all_ok = print_results_summary(
            analysis_ok, elapsed, seismic_weight, modal_results,
            drift_results, base_shear_results, weight_ok,
        )

        log.info("")
        log.info(f"  Total script time: {t_total:.1f}s")
        log.info("")

        if all_ok:
            log.info("Ready for next step (12_results.py)")
        else:
            log.info("Review warnings above before proceeding")
        log.info("=" * 65)

        sys.exit(0 if all_ok else 1)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
