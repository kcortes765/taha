"""
10_combinations.py — Define load combinations per NCh3171 for Edificio 1.

Creates 11 LRFD load combinations (NCh3171:2017) and one design envelope:

  Gravitational:
    C1:  1.4·D
    C2:  1.2·D + 1.6·L + 0.5·Lr
    C3:  1.2·D + 1.6·Lr + 1.0·L

  Seismic X (SDX):
    C4:  1.2·D + 1.0·L + 1.4·SDX
    C5:  1.2·D + 1.0·L - 1.4·SDX

  Seismic Y (SDY):
    C6:  1.2·D + 1.0·L + 1.4·SDY
    C7:  1.2·D + 1.0·L - 1.4·SDY

  Uplift / minimum gravity + seismic:
    C8:  0.9·D + 1.4·SDX
    C9:  0.9·D - 1.4·SDX
    C10: 0.9·D + 1.4·SDY
    C11: 0.9·D - 1.4·SDY

  Envelope:
    ENV: Envelope of C1 through C11

Where:
  D  = PP + TERP + TERT  (dead load = self-weight + floor finishes + roof finishes)
  L  = SCP               (floor live load — offices + corridors)
  Lr = SCT               (roof live load)
  SDX, SDY = Response spectrum cases in X (U1) and Y (U2) from 08_seismic.py

NCh3171 reference (Material de Apoyo Taller 2026, Sección I):
  - 1.4 factor on E is the load factor for seismic per NCh3171.
  - Seismic cases SDX/SDY are response spectrum results (CQC combined,
    always positive). ETABS internally generates 8 sub-combinations with
    all sign permutations of (P, V2, V3, T, M2, M3) for each combo that
    includes a spectrum case.
  - The explicit ±1.4·SDX combos ensure both "gravity + seismic" and
    "gravity - seismic" envelopes are captured for design.

TERT inclusion:
  TERP applies to floors 1-19 only, TERT to roof (story 20) only.
  Both are permanent loads (SuperDead) and must be factored with the same
  factor as PP in every combination. Including both is safe because their
  loads never overlap (different stories).

Envelope:
  The ENV combo (type=Envelope) captures the maximum/minimum response
  across all 11 individual combos. This is used for design checks.

Torsion note:
  These combos use SDX/SDY (no accidental torsion). If 09_torsion.py
  created SDTX/SDTY cases (Forma 2), duplicate these combos replacing
  SDX→SDTX and SDY→SDTY. For Forma 1, also add ±1.4·TEX/TEY terms.
  The script supports --torsion-f2 flag to auto-create torsion combos.

Prerequisites:
  - ETABS v19 open with model from scripts 01-09
  - Load patterns PP, TERP, TERT, SCP, SCT defined (07_loads.py)
  - Spectrum cases SDX, SDY defined (08_seismic.py)
  - comtypes installed
  - config.py in the same directory

Usage:
  python 10_combinations.py                # Basic 11 combos + ENV
  python 10_combinations.py --torsion-f2   # Also create SDTX/SDTY combos

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against: autonomo/research/etabs_api_reference.md §16
  - RespCombo.Add(Name, ComboType): §16.1
  - RespCombo.SetCaseList(Name, CNameType, CName, SF): §16.2
  - RespCombo.GetNameList(): §16.4
  - RespCombo.GetCaseList(Name): §16.3
  - RespCombo.Delete(Name): §16.5
Sources: NCh3171:2017, Material Apoyo Taller 2026 (Sección I), config.py
"""

import sys
import os
import time

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
)


# ===================================================================
# CONSTANTS
# ===================================================================

# ComboType constants (eComboType)
COMBO_LINEAR_ADD = 0   # Linear additive combination
COMBO_ENVELOPE = 1     # Envelope (max/min across sub-combos)
COMBO_ABSOLUTE_ADD = 2 # Absolute additive
COMBO_SRSS = 3         # SRSS combination
COMBO_RANGE_ADD = 4    # Range additive

# CNameType constants (eCNameType)
CNAME_LOAD_CASE = 0    # Load case (pattern auto-case or spectrum case)
CNAME_LOAD_COMBO = 1   # Load combination

# Seismic case names (from 08_seismic.py)
SDX_CASE = "SDX"
SDY_CASE = "SDY"

# Torsion Forma 2 case names (from 09_torsion.py, if created)
SDTX_CASE = "SDTX"
SDTY_CASE = "SDTY"

# Envelope combo name
ENVELOPE_NAME = "ENV"


# ===================================================================
# COMBINATION DEFINITIONS — NCh3171:2017
# ===================================================================
# Each combo is a list of (scale_factor, load_case_name) tuples.
# D = PP + TERP + TERT (all permanent loads, same factor).
# L = SCP (floor live).  Lr = SCT (roof live).
# SDX/SDY = response spectrum cases.

def _build_combos(sx_case, sy_case):
    """Build the 11 NCh3171 combinations for given seismic case names.

    Args:
        sx_case: str — seismic X case name ("SDX" or "SDTX")
        sy_case: str — seismic Y case name ("SDY" or "SDTY")

    Returns:
        list of (combo_name, [(sf, case_name), ...]) tuples
    """
    combos = []

    # --- Gravitational combinations ---

    # C1: 1.4·D = 1.4·PP + 1.4·TERP + 1.4·TERT
    combos.append(("C1", [
        (1.4, "PP"), (1.4, "TERP"), (1.4, "TERT"),
    ]))

    # C2: 1.2·D + 1.6·L + 0.5·Lr
    combos.append(("C2", [
        (1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"),
        (1.6, "SCP"), (0.5, "SCT"),
    ]))

    # C3: 1.2·D + 1.6·Lr + 1.0·L
    combos.append(("C3", [
        (1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"),
        (1.6, "SCT"), (1.0, "SCP"),
    ]))

    # --- Seismic X combinations ---

    # C4: 1.2·D + 1.0·L + 1.4·SDX
    combos.append(("C4", [
        (1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"),
        (1.0, "SCP"), (1.4, sx_case),
    ]))

    # C5: 1.2·D + 1.0·L - 1.4·SDX
    combos.append(("C5", [
        (1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"),
        (1.0, "SCP"), (-1.4, sx_case),
    ]))

    # --- Seismic Y combinations ---

    # C6: 1.2·D + 1.0·L + 1.4·SDY
    combos.append(("C6", [
        (1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"),
        (1.0, "SCP"), (1.4, sy_case),
    ]))

    # C7: 1.2·D + 1.0·L - 1.4·SDY
    combos.append(("C7", [
        (1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"),
        (1.0, "SCP"), (-1.4, sy_case),
    ]))

    # --- Minimum gravity + seismic (uplift check) ---

    # C8: 0.9·D + 1.4·SDX
    combos.append(("C8", [
        (0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"),
        (1.4, sx_case),
    ]))

    # C9: 0.9·D - 1.4·SDX
    combos.append(("C9", [
        (0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"),
        (-1.4, sx_case),
    ]))

    # C10: 0.9·D + 1.4·SDY
    combos.append(("C10", [
        (0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"),
        (1.4, sy_case),
    ]))

    # C11: 0.9·D - 1.4·SDY
    combos.append(("C11", [
        (0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"),
        (-1.4, sy_case),
    ]))

    return combos


# ===================================================================
# STEP 1: Verify prerequisites
# ===================================================================

def verify_prerequisites(SapModel):
    """Verify that required load patterns and cases exist.

    Checks:
      - Load patterns: PP, TERP, TERT, SCP, SCT
      - Load cases: SDX, SDY (response spectrum)

    Returns:
        tuple (patterns_ok, cases_ok, existing_cases)
    """
    log.info("Step 1: Verifying prerequisites...")

    # Check load patterns
    expected_patterns = {"PP", "TERP", "TERT", "SCP", "SCT"}
    found_patterns = set()

    try:
        result = SapModel.LoadPatterns.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            pattern_names = [str(p) for p in result[1]] if result[1] else []
            for p in pattern_names:
                if p in expected_patterns:
                    found_patterns.add(p)
    except Exception as e:
        log.warning(f"  LoadPatterns.GetNameList failed: {e}")

    missing_patterns = expected_patterns - found_patterns
    patterns_ok = len(missing_patterns) == 0

    if patterns_ok:
        log.info(f"  Load patterns: all {len(expected_patterns)} present ✓")
    else:
        log.warning(f"  MISSING load patterns: {missing_patterns}")
        log.warning("  Run 07_loads.py first to create load patterns")

    # Check load cases (SDX, SDY and optionally SDTX, SDTY)
    expected_cases = {SDX_CASE, SDY_CASE}
    found_cases = set()
    all_cases = []

    try:
        result = SapModel.LoadCases.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            case_names = [str(c) for c in result[1]] if result[1] else []
            all_cases = case_names
            for c in case_names:
                if c in expected_cases:
                    found_cases.add(c)
    except Exception as e:
        log.warning(f"  LoadCases.GetNameList failed: {e}")

    missing_cases = expected_cases - found_cases
    cases_ok = len(missing_cases) == 0

    if cases_ok:
        log.info(f"  Seismic cases: {SDX_CASE}, {SDY_CASE} present ✓")
    else:
        log.warning(f"  MISSING seismic cases: {missing_cases}")
        log.warning("  Run 08_seismic.py first to create spectrum cases")

    # Check for torsion cases (optional)
    has_torsion_f2 = SDTX_CASE in all_cases and SDTY_CASE in all_cases
    if has_torsion_f2:
        log.info(f"  Torsion Forma 2 cases: {SDTX_CASE}, {SDTY_CASE} present ✓")
    else:
        log.info(f"  Torsion Forma 2 cases: not found (optional)")

    return patterns_ok, cases_ok, set(all_cases)


# ===================================================================
# STEP 2: Delete existing combos (if re-running)
# ===================================================================

def delete_existing_combos(SapModel, combo_names):
    """Delete combos that already exist to allow clean re-creation.

    This enables re-running the script without accumulating duplicates.
    Only deletes combos whose names match our expected names.

    Args:
        SapModel: ETABS model object
        combo_names: list of combo names to check and delete
    """
    log.info("Step 2: Checking for existing combos to replace...")

    existing = set()
    try:
        result = SapModel.RespCombo.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_combos = result[0]
            names = [str(n) for n in result[1]] if result[1] else []
            existing = set(names)
            if n_combos > 0:
                log.info(f"  Existing combos in model: {n_combos}")
    except Exception:
        log.info("  No existing combos found")
        return

    deleted = 0
    for name in combo_names:
        if name in existing:
            try:
                ret = SapModel.RespCombo.Delete(name)
                if isinstance(ret, tuple):
                    ret_code = ret[-1] if len(ret) > 1 else ret[0]
                else:
                    ret_code = ret

                if ret_code == 0:
                    deleted += 1
                    log.info(f"  Deleted existing combo '{name}' ✓")
                else:
                    log.warning(f"  Delete('{name}') ret={ret_code}")
            except Exception as e:
                log.warning(f"  Delete('{name}') failed: {e}")

    if deleted > 0:
        log.info(f"  Deleted {deleted} existing combos for clean re-creation")
    else:
        log.info(f"  No conflicting combos found — proceeding with creation")


# ===================================================================
# STEP 3: Create individual combinations
# ===================================================================

def create_combo(SapModel, name, case_factors):
    """Create a single load combination.

    Firma COM (etabs_api_reference.md §16.1):
      ret = SapModel.RespCombo.Add(Name, ComboType)
      ComboType: 0=LinearAdd

    Firma COM (etabs_api_reference.md §16.2):
      ret = SapModel.RespCombo.SetCaseList(Name, CNameType, CName, SF)
      CNameType: 0=LoadCase, 1=LoadCombo

    Args:
        SapModel: ETABS model object
        name: str — combo name (e.g., "C1")
        case_factors: list of (sf, case_name) tuples

    Returns:
        True if all operations succeeded
    """
    # Create the combo (LinearAdd type)
    ret = SapModel.RespCombo.Add(name, COMBO_LINEAR_ADD)
    if isinstance(ret, tuple):
        ret_code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        ret_code = ret

    if ret_code != 0:
        log.warning(f"  RespCombo.Add('{name}') ret={ret_code}")
        return False

    # Add each load case to the combo
    all_ok = True
    for sf, case_name in case_factors:
        ret = SapModel.RespCombo.SetCaseList(
            name,              # Name — combo name
            CNAME_LOAD_CASE,   # CNameType = 0 (LoadCase)
            case_name,         # CName — load case name
            sf,                # SF — scale factor
        )

        if isinstance(ret, tuple):
            ret_code = ret[-1] if len(ret) > 1 else ret[0]
        else:
            ret_code = ret

        if ret_code != 0:
            log.warning(f"  SetCaseList('{name}', '{case_name}', "
                        f"SF={sf:+.1f}) ret={ret_code}")
            all_ok = False

    return all_ok


def create_all_combos(SapModel, combos):
    """Create all load combinations.

    Args:
        SapModel: ETABS model object
        combos: list of (name, [(sf, case_name), ...]) tuples

    Returns:
        tuple (created, failed) — counts
    """
    log.info("Step 3: Creating load combinations...")
    log.info("")

    created = 0
    failed = 0

    for name, case_factors in combos:
        # Format the combo expression for logging
        terms = []
        for sf, case_name in case_factors:
            if sf == 1.0:
                terms.append(case_name)
            elif sf == -1.0:
                terms.append(f"-{case_name}")
            else:
                terms.append(f"{sf:+.1f}·{case_name}")
        expr = " ".join(terms)

        ok = create_combo(SapModel, name, case_factors)
        if ok:
            created += 1
            log.info(f"  ✓ {name:4s} = {expr}")
        else:
            failed += 1
            log.warning(f"  ✗ {name:4s} = {expr}")

    log.info("")
    log.info(f"  Created: {created}/{len(combos)}, Failed: {failed}")
    return created, failed


# ===================================================================
# STEP 4: Create envelope combination
# ===================================================================

def create_envelope(SapModel, env_name, combo_names):
    """Create an envelope combination containing all individual combos.

    The envelope combo uses ComboType=1 (Envelope) which captures the
    maximum and minimum values across all included combinations.
    This is used for design verification.

    Firma COM:
      RespCombo.Add(Name, 1)  — 1 = Envelope type
      RespCombo.SetCaseList(Name, 1, SubComboName, 1.0)  — 1 = LoadCombo

    Args:
        SapModel: ETABS model object
        env_name: str — envelope combo name (e.g., "ENV")
        combo_names: list of combo names to include

    Returns:
        True if successful
    """
    log.info(f"Step 4: Creating envelope combination '{env_name}'...")

    # Create envelope combo
    ret = SapModel.RespCombo.Add(env_name, COMBO_ENVELOPE)
    if isinstance(ret, tuple):
        ret_code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        ret_code = ret

    if ret_code != 0:
        log.warning(f"  RespCombo.Add('{env_name}', Envelope) ret={ret_code}")
        return False

    # Add each individual combo to the envelope
    all_ok = True
    for combo_name in combo_names:
        ret = SapModel.RespCombo.SetCaseList(
            env_name,            # Name — envelope combo name
            CNAME_LOAD_COMBO,    # CNameType = 1 (LoadCombo)
            combo_name,          # CName — sub-combo name
            1.0,                 # SF = 1.0 (no additional scaling)
        )

        if isinstance(ret, tuple):
            ret_code = ret[-1] if len(ret) > 1 else ret[0]
        else:
            ret_code = ret

        if ret_code != 0:
            log.warning(f"  SetCaseList('{env_name}', combo='{combo_name}') "
                        f"ret={ret_code}")
            all_ok = False

    if all_ok:
        log.info(f"  ✓ {env_name} = Envelope({', '.join(combo_names)})")
    else:
        log.warning(f"  Some sub-combos could not be added to {env_name}")

    return all_ok


# ===================================================================
# STEP 5: Verification
# ===================================================================

def verify_combos(SapModel, expected_names):
    """Verify all expected combinations exist and have correct case lists.

    Args:
        SapModel: ETABS model object
        expected_names: set of expected combo names

    Returns:
        True if all expected combos are present
    """
    log.info("Step 5: Verifying combinations...")

    found = set()
    try:
        result = SapModel.RespCombo.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_combos = result[0]
            combo_names = [str(n) for n in result[1]] if result[1] else []
            log.info(f"  Total combos in model: {n_combos}")

            for name in combo_names:
                marker = "✓" if name in expected_names else " "
                log.info(f"    {marker} {name}")
                if name in expected_names:
                    found.add(name)
    except Exception as e:
        log.warning(f"  RespCombo.GetNameList failed: {e}")
        return False

    missing = expected_names - found
    if missing:
        log.warning(f"  MISSING combos: {missing}")
        return False

    log.info(f"  All {len(expected_names)} expected combos present ✓")

    # Verify case counts for a few key combos
    for check_name in ["C1", "C4", "C8"]:
        if check_name not in found:
            continue
        try:
            result = SapModel.RespCombo.GetCaseList(check_name)
            if isinstance(result, tuple) and len(result) >= 4:
                n_items = result[0]
                case_names = result[2] if len(result) > 2 else []
                sf_values = result[3] if len(result) > 3 else []
                log.info(f"  Spot check '{check_name}': "
                         f"{n_items} cases/combos")
                if case_names and sf_values:
                    for cn, sf in zip(case_names, sf_values):
                        log.info(f"    {float(sf):+.1f} × {cn}")
        except Exception as e:
            log.info(f"  Spot check '{check_name}': could not read ({e})")

    return True


def print_combo_summary(combos, env_name, torsion_combos=None):
    """Print a formatted summary of all combinations."""
    log.info("")
    log.info("  NCh3171 Load Combination Summary:")
    log.info("  ┌─────┬────────────────────────────────────────────────┐")
    log.info("  │ ID  │ Expression                                     │")
    log.info("  ├─────┼────────────────────────────────────────────────┤")

    for name, case_factors in combos:
        terms = []
        for sf, cn in case_factors:
            if sf == 1.0:
                terms.append(f"+{cn}")
            elif sf == -1.0:
                terms.append(f"-{cn}")
            elif sf > 0:
                terms.append(f"+{sf:.1f}·{cn}")
            else:
                terms.append(f"{sf:.1f}·{cn}")
        expr = " ".join(terms)
        log.info(f"  │ {name:3s} │ {expr:<47s}│")

    log.info("  ├─────┼────────────────────────────────────────────────┤")

    # Envelope
    combo_names = [c[0] for c in combos]
    env_expr = f"Envelope({combo_names[0]}..{combo_names[-1]})"
    log.info(f"  │ {env_name:3s} │ {env_expr:<47s}│")
    log.info("  └─────┴────────────────────────────────────────────────┘")

    if torsion_combos:
        log.info("")
        log.info("  Torsion Forma 2 Combinations (SDTX/SDTY):")
        log.info("  ┌──────┬───────────────────────────────────────────────┐")
        for name, case_factors in torsion_combos:
            terms = []
            for sf, cn in case_factors:
                if sf == 1.0:
                    terms.append(f"+{cn}")
                elif sf == -1.0:
                    terms.append(f"-{cn}")
                elif sf > 0:
                    terms.append(f"+{sf:.1f}·{cn}")
                else:
                    terms.append(f"{sf:.1f}·{cn}")
            expr = " ".join(terms)
            log.info(f"  │ {name:4s} │ {expr:<46s}│")
        log.info("  └──────┴───────────────────────────────────────────────┘")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: create NCh3171 load combinations."""
    log.info("=" * 60)
    log.info("10_combinations.py — NCh3171 Load Combinations, Edificio 1")
    log.info("=" * 60)
    log.info("")

    # Parse command-line flags
    create_torsion = "--torsion-f2" in sys.argv

    # Build combo definitions
    combos = _build_combos(SDX_CASE, SDY_CASE)
    combo_names = [c[0] for c in combos]

    torsion_combos = None
    torsion_combo_names = []
    if create_torsion:
        # Build torsion Forma 2 combos with SDTX/SDTY
        # Use CT prefix to distinguish from base combos
        torsion_combos_raw = _build_combos(SDTX_CASE, SDTY_CASE)
        torsion_combos = []
        for name, factors in torsion_combos_raw:
            # Skip gravitational combos (C1-C3) — already created as base
            if name in ("C1", "C2", "C3"):
                continue
            t_name = name.replace("C", "CT")  # CT4, CT5, ... CT11
            torsion_combos.append((t_name, factors))
        torsion_combo_names = [c[0] for c in torsion_combos]

    all_combo_names = combo_names + torsion_combo_names + [ENVELOPE_NAME]
    if create_torsion:
        all_combo_names.append("ENVT")

    log.info("  Configuration:")
    log.info(f"    Base combos: {len(combos)} (C1-C11)")
    log.info(f"    Seismic cases: {SDX_CASE}, {SDY_CASE}")
    if create_torsion:
        log.info(f"    Torsion combos: {len(torsion_combos)} "
                 f"(CT4-CT11, using {SDTX_CASE}/{SDTY_CASE})")
    log.info(f"    Envelope: {ENVELOPE_NAME}")
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

        t_start = time.time()

        # Step 1: Verify prerequisites
        patterns_ok, cases_ok, existing_cases = verify_prerequisites(SapModel)
        log.info("")

        if not patterns_ok:
            log.error("Missing load patterns — run 07_loads.py first")
            sys.exit(1)

        if not cases_ok:
            log.warning("Missing seismic cases — seismic combos will fail")
            log.warning("Run 08_seismic.py first, then re-run this script")
            # Continue anyway — gravitational combos will still work

        if create_torsion:
            if SDTX_CASE not in existing_cases or SDTY_CASE not in existing_cases:
                log.warning(f"Torsion cases {SDTX_CASE}/{SDTY_CASE} not found")
                log.warning("Run 09_torsion.py with Forma 2 first")
                log.warning("Skipping torsion combo creation")
                create_torsion = False
                torsion_combos = None
                torsion_combo_names = []
                all_combo_names = combo_names + [ENVELOPE_NAME]

        # Step 2: Delete existing combos (for clean re-run)
        delete_existing_combos(SapModel, all_combo_names)
        log.info("")

        # Step 3: Create individual combinations
        n_created, n_failed = create_all_combos(SapModel, combos)
        log.info("")

        # Step 3b: Create torsion combos if requested
        t_created, t_failed = 0, 0
        if create_torsion and torsion_combos:
            log.info("Step 3b: Creating torsion Forma 2 combinations...")
            t_created, t_failed = create_all_combos(SapModel, torsion_combos)
            log.info("")

        # Step 4: Create envelope
        env_ok = create_envelope(SapModel, ENVELOPE_NAME, combo_names)
        log.info("")

        # Create torsion envelope if applicable
        envt_ok = True
        if create_torsion and torsion_combos:
            # Torsion envelope includes gravitational C1-C3 + torsion CT4-CT11
            envt_combos = ["C1", "C2", "C3"] + torsion_combo_names
            envt_ok = create_envelope(SapModel, "ENVT", envt_combos)
            log.info("")

        t_elapsed = time.time() - t_start

        # Step 5: Verify
        all_expected = set(combo_names + [ENVELOPE_NAME])
        if create_torsion and torsion_combos:
            all_expected.update(torsion_combo_names)
            all_expected.add("ENVT")
        verify_ok = verify_combos(SapModel, all_expected)
        log.info("")

        # Summary table
        print_combo_summary(combos, ENVELOPE_NAME, torsion_combos)
        log.info("")

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Final report
        total_created = n_created + t_created
        total_failed = n_failed + t_failed
        total_expected = len(combos) + (len(torsion_combos) if torsion_combos else 0)

        log.info("=" * 60)
        log.info("RESULTS")
        log.info("=" * 60)
        log.info(f"  Combos created: {total_created}/{total_expected}")
        log.info(f"  Combos failed:  {total_failed}")
        log.info(f"  Envelope '{ENVELOPE_NAME}': "
                 f"{'✓' if env_ok else '✗'}")
        if create_torsion and torsion_combos:
            log.info(f"  Torsion envelope 'ENVT': "
                     f"{'✓' if envt_ok else '✗'}")
        log.info(f"  Verification: {'✓' if verify_ok else '✗'}")
        log.info(f"  Time: {t_elapsed:.1f}s")
        log.info("")

        if total_failed > 0:
            log.warning(f"  {total_failed} combos failed — check warnings")
        else:
            log.info("  All combinations created successfully!")

        log.info("")
        log.info("NCh3171 Notes:")
        log.info("  - Factor 1.4 on E per NCh3171:2017 (seismic load factor)")
        log.info("  - D = PP + TERP + TERT (all permanent loads)")
        log.info("  - L = SCP (floor live), Lr = SCT (roof live)")
        log.info("  - ETABS generates 8 sign sub-combos for each seismic combo")
        log.info("  - ENV envelope captures max/min across all 11 states")
        if not create_torsion:
            log.info("  - To add torsion combos: python 10_combinations.py "
                     "--torsion-f2")
        log.info("")
        log.info("Ready for next step (analysis or 11_adjust_Rstar.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
