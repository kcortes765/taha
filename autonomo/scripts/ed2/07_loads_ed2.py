"""
07_loads_ed2.py — Define load patterns and apply uniform loads for Edificio 2.

This script handles two related tasks:
  1. Create load patterns (PP, TERP, TERT, SCP, SCT)
  2. Apply uniform distributed loads to all slab area objects

Load Patterns:
  - PP:   Dead  (SWM=1) — self-weight computed automatically by ETABS
  - TERP: Super Dead (SWM=0) — floor finishes (terminaciones pisos 1-4)
  - TERT: Super Dead (SWM=0) — roof finishes (terminaciones techo piso 5)
  - SCP:  Live  (SWM=0) — floor live load (pisos 1-4, uniforme 300 kgf/m2)
  - SCT:  RoofLive (eType=11, SWM=0) — roof live load (piso 5)

Uniform Loads applied to slabs (AreaObj.SetLoadUniform, Dir=6 Global Z):
  Stories 1-4 (floor):
    - TERP = -0.140 tonf/m2 (all floor slabs)
    - SCP  = -0.300 tonf/m2 (all floor slabs — uniform, no corridor distinction)
  Story 5 (roof):
    - TERT = -0.100 tonf/m2 (all roof slabs)
    - SCT  = -0.100 tonf/m2 (all roof slabs)

Ed.2 simplification vs Ed.1:
  - No corridor/office distinction — SCP is uniform 0.300 tonf/m2 everywhere
  - 25 slab panels per story (5x5 regular grid, no shaft)
  - 5 stories (vs 20 in Ed.1)

After creating patterns, the default "Dead" pattern (auto-created by ETABS on
File.NewGridOnly) is removed or zeroed to avoid double-counting self-weight.

Prerequisites:
  - ETABS (v19/v21) open with model from scripts 01-06
  - comtypes installed
  - config_ed2.py in the same directory

Usage:
  python 07_loads_ed2.py

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against: autonomo/research/com_signatures.md
  - LoadPatterns.Add: §9.1
  - AreaObj.SetLoadUniform: §9.2
  - AreaObj.GetNameList: §7 (tuple: count, names, ret)
  - AreaObj.GetProperty: §7 (tuple: section_name, ret)
  - AreaObj.GetPoints: (tuple: count, point_names, ret)
  - PointObj.GetCoordCartesian: (x, y, z, ret)
Sources: Enunciado Taller ADSE 1S-2026 pags 8-9, Prof. Music
         config_ed2.py LOAD_PATTERNS, TERP_PISO, SCP_PISO, etc.
"""

import sys
import os
import time

# Ensure config_ed2.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
    # Stories
    N_STORIES, STORY_ELEVATIONS,
    # Slab data
    SLAB_PANELS, N_SLABS_PER_STORY, N_SLABS_TOTAL,
    AREA_LOSA_PISO, AREA_PLANTA,
    # Section names
    LOSA_NAME,
    # Load definitions
    LOAD_PATTERNS,
    TERP_PISO, TERT_TECHO, SCP_PISO, SCT_TECHO,
)

# ===================================================================
# CONSTANTS
# ===================================================================

# Direction for uniform loads: Global Z axis (positive = up, negative = down)
LOAD_DIR_GLOBAL_Z = 6

# Roof elevation (top of story 5)
ROOF_ELEV = STORY_ELEVATIONS[-1]  # 15.5 m

# Tolerances
Z_TOLERANCE = 0.15   # m — for roof detection

# Floor vs roof story counts
N_FLOOR_STORIES = N_STORIES - 1               # 4
N_ROOF_STORIES = 1
EXPECTED_FLOOR_SLABS = N_SLABS_PER_STORY * N_FLOOR_STORIES  # 100
EXPECTED_ROOF_SLABS = N_SLABS_PER_STORY                      # 25
EXPECTED_TOTAL_SLABS = N_SLABS_TOTAL                          # 125


# ===================================================================
# STEP 0: Remove default "Dead" load pattern
# ===================================================================

def remove_default_dead(SapModel):
    """Remove or neutralize the default 'Dead' load pattern.

    ETABS creates a default 'Dead' pattern (Dead type, SWM=1) when a model
    is initialized via File.NewGridOnly. Since we create our own 'PP' pattern
    (Dead, SWM=1), the default 'Dead' must be removed to avoid double-counting
    self-weight.

    Strategy:
      1. Try LoadPatterns.Delete("Dead")
      2. If delete fails (e.g., pattern in use), set its SWM to 0 as fallback
    """
    log.info("Step 0: Removing default 'Dead' load pattern...")

    # First, try to delete it
    try:
        ret = SapModel.LoadPatterns.Delete("Dead")
        if isinstance(ret, (tuple, list)):
            ret_code = ret[-1] if len(ret) > 1 else ret[0]
        else:
            ret_code = ret

        if ret_code == 0:
            log.info("  Deleted default 'Dead' pattern ✓")
            return True
        else:
            log.info(f"  Delete('Dead') ret={ret_code} — trying fallback")
    except Exception as e:
        log.info(f"  Delete('Dead') exception: {e} — trying fallback")

    # Fallback: set SWM to 0 so it doesn't contribute self-weight
    try:
        ret = SapModel.LoadPatterns.SetSelfWtMultiplier("Dead", 0.0)
        if isinstance(ret, (tuple, list)):
            ret_code = ret[-1] if len(ret) > 1 else ret[0]
        else:
            ret_code = ret

        if ret_code == 0:
            log.info("  Set 'Dead' SWM=0 (fallback) ✓")
            return True
        else:
            log.warning(f"  SetSelfWtMultiplier('Dead') ret={ret_code}")
    except Exception as e:
        log.info(f"  'Dead' pattern likely doesn't exist — OK ({e})")

    return False


# ===================================================================
# STEP 1: Create load patterns
# ===================================================================

def create_load_patterns(SapModel):
    """Create all 5 load patterns: PP, TERP, TERT, SCP, SCT.

    Uses LoadPatterns.Add with AddAnalysisCase=True so ETABS automatically
    creates a corresponding static analysis case for each pattern.

    Firma COM (com_signatures.md §9.1):
      ret = LoadPatterns.Add(Name, MyType, SelfWTMultiplier, AddAnalysisCase)
      MyType: 1=Dead, 2=SuperDead, 3=Live, 5=Quake, 11=RoofLive
      SelfWTMultiplier: 1.0 for PP (self-weight), 0.0 for all others
      AddAnalysisCase: True — auto-create linear static case
    """
    log.info("Step 1: Creating load patterns...")

    created = 0
    already_exists = 0

    for name, (ltype, swm) in LOAD_PATTERNS.items():
        ret = SapModel.LoadPatterns.Add(name, ltype, swm, True)

        if isinstance(ret, (tuple, list)):
            ret_code = ret[-1] if len(ret) > 1 else ret[0]
        else:
            ret_code = ret

        if ret_code == 0:
            created += 1
            log.info(f"  ✓ {name:5s} type={ltype:2d} SWM={swm}")
        else:
            already_exists += 1
            log.warning(f"  {name:5s} ret={ret_code} (may already exist — OK)")

    log.info(f"  Patterns created: {created}, already existed: {already_exists}")
    return created


# ===================================================================
# STEP 2: Classify slab area objects (floor vs roof)
# ===================================================================

def _get_area_centroid_z(SapModel, area_name):
    """Get average Z coordinate of an area object's corner points.

    Returns:
        float or None on failure
    """
    try:
        pts_result = SapModel.AreaObj.GetPoints(area_name)
        if isinstance(pts_result, (tuple, list)) and len(pts_result) >= 2:
            point_names = pts_result[1]
        else:
            return None
    except Exception:
        return None

    if point_names is None:
        return None

    z_vals = []
    for pt in point_names:
        try:
            c = SapModel.PointObj.GetCoordCartesian(str(pt))
            if isinstance(c, (tuple, list)) and len(c) >= 3:
                z_vals.append(float(c[2]))
        except Exception:
            pass

    if not z_vals:
        return None

    return sum(z_vals) / len(z_vals)


def classify_slabs(SapModel):
    """Classify all slab areas into floor (stories 1-4) and roof (story 5).

    Ed.2 simplification: no corridor/office distinction.
    All floor slabs get the same SCP (0.300 tonf/m2).

    Process:
      1. Get all area objects (AreaObj.GetNameList)
      2. Filter slabs only (section = L17G25)
      3. Get Z elevation for each slab
      4. By Z elevation: roof (story 5 = 15.5m) vs floor (stories 1-4)

    Returns:
        dict with keys: 'floor', 'roof'
              values: lists of area object names
    """
    log.info("Step 2: Classifying slab areas (floor vs roof)...")

    result = {
        'floor': [],
        'roof': [],
    }

    # Get all area objects
    try:
        name_result = SapModel.AreaObj.GetNameList()
        if isinstance(name_result, (tuple, list)) and len(name_result) >= 2:
            n_areas = name_result[0]
            area_names = name_result[1]
        else:
            log.warning("  AreaObj.GetNameList returned unexpected format")
            return result
    except Exception as e:
        log.warning(f"  AreaObj.GetNameList failed: {e}")
        return result

    if n_areas == 0:
        log.warning("  No area objects found — cannot classify slabs")
        return result

    log.info(f"  Total area objects in model: {n_areas}")

    non_slab = 0
    no_coords = 0

    for area_name in area_names:
        area_name = str(area_name)

        # Check if this is a slab by section name
        try:
            prop = SapModel.AreaObj.GetProperty(area_name)
            section = str(prop[0]) if isinstance(prop, (tuple, list)) and len(prop) >= 1 else ""
        except Exception:
            section = ""

        if LOSA_NAME not in section:
            non_slab += 1
            continue

        # Get Z elevation
        z_avg = _get_area_centroid_z(SapModel, area_name)
        if z_avg is None:
            no_coords += 1
            continue

        # Classify by elevation: roof vs floor
        if abs(z_avg - ROOF_ELEV) < Z_TOLERANCE:
            result['roof'].append(area_name)
        else:
            result['floor'].append(area_name)

    n_floor = len(result['floor'])
    n_roof = len(result['roof'])
    n_total_slabs = n_floor + n_roof

    log.info(f"  Classification results:")
    log.info(f"    Floor slabs (P1-P4): {n_floor:4d} "
             f"(expected ~{EXPECTED_FLOOR_SLABS})")
    log.info(f"    Roof slabs  (P5):    {n_roof:4d} "
             f"(expected ~{EXPECTED_ROOF_SLABS})")
    log.info(f"    Total slabs:         {n_total_slabs:4d} "
             f"(expected ~{EXPECTED_TOTAL_SLABS})")
    log.info(f"    Non-slab areas:      {non_slab:4d}")
    if no_coords > 0:
        log.warning(f"    Slabs without coords: {no_coords} (could not classify)")

    # Warn if counts are significantly off
    if n_total_slabs > 0:
        if abs(n_total_slabs - EXPECTED_TOTAL_SLABS) > EXPECTED_TOTAL_SLABS * 0.1:
            log.warning(f"  Total slab count differs significantly from expected!")

    return result


# ===================================================================
# STEP 3: Apply uniform loads to slabs
# ===================================================================

def _apply_uniform_load(SapModel, areas, load_pattern, value):
    """Apply uniform load to a list of area objects.

    Firma COM (com_signatures.md §9.2):
      ret = AreaObj.SetLoadUniform(Name, LoadPat, Value, Dir, Replace, CSys, ItemType)
      Dir = 6 (Global Z — positive up, negative down)
      Replace = True (replace existing load for this pattern on this area)

    Args:
        SapModel: ETABS model object
        areas: list of area object names
        load_pattern: str — load pattern name (e.g., "TERP")
        value: float — load value in tonf/m2 (negative = downward)

    Returns:
        tuple (ok_count, fail_count)
    """
    ok = 0
    fail = 0

    for area_name in areas:
        ret = SapModel.AreaObj.SetLoadUniform(
            area_name,          # Name
            load_pattern,       # LoadPat
            value,              # Value (negative = downward)
            LOAD_DIR_GLOBAL_Z,  # Dir = 6 (Global Z)
            True,               # Replace = True
        )

        if isinstance(ret, (tuple, list)):
            ret_code = ret[-1] if len(ret) > 1 else ret[0]
        else:
            ret_code = ret

        if ret_code == 0:
            ok += 1
        else:
            fail += 1
            if fail <= 5:
                log.warning(f"    SetLoadUniform({area_name}, {load_pattern}, "
                            f"{value}) ret={ret_code}")

    return ok, fail


def apply_loads(SapModel, classification):
    """Apply all uniform loads to classified slab areas.

    Load application matrix (Ed.2 — uniform, no corridors):
      ┌──────────────────┬────────────┬────────────┬────────────┬────────────┐
      │ Slab Type        │ TERP       │ SCP        │ TERT       │ SCT        │
      ├──────────────────┼────────────┼────────────┼────────────┼────────────┤
      │ Floor (P1-P4)    │ -0.140     │ -0.300     │ —          │ —          │
      │ Roof  (P5)       │ —          │ —          │ -0.100     │ -0.100     │
      └──────────────────┴────────────┴────────────┴────────────┴────────────┘
      All values in tonf/m2. Negative = downward (Dir=6, Global Z).
      PP has SWM=1 → no uniform load needed (self-weight is automatic).

    Returns:
        tuple (total_ok, total_fail) — cumulative load assignment counts
    """
    log.info("Step 3: Applying uniform loads to slabs...")
    log.info(f"  Load values (tonf/m2, downward):")
    log.info(f"    TERP = {TERP_PISO} (floor finishes, pisos 1-4)")
    log.info(f"    SCP  = {SCP_PISO} (uniform all floor slabs, pisos 1-4)")
    log.info(f"    TERT = {TERT_TECHO} (roof finishes, piso 5)")
    log.info(f"    SCT  = {SCT_TECHO} (roof live load, piso 5)")
    log.info("")

    floor_slabs = classification['floor']
    roof_slabs = classification['roof']

    total_ok = 0
    total_fail = 0

    # --- TERP on ALL floor slabs (stories 1-4) ---
    if floor_slabs:
        log.info(f"  Applying TERP to {len(floor_slabs)} floor slabs...")
        ok, fail = _apply_uniform_load(SapModel, floor_slabs, "TERP", -TERP_PISO)
        log.info(f"    TERP: {ok} OK, {fail} failed "
                 f"(value={-TERP_PISO} tonf/m2)")
        total_ok += ok
        total_fail += fail
    else:
        log.warning("  No floor slabs — skipping TERP")

    # --- SCP on ALL floor slabs (stories 1-4, uniform) ---
    if floor_slabs:
        log.info(f"  Applying SCP to {len(floor_slabs)} floor slabs...")
        ok, fail = _apply_uniform_load(SapModel, floor_slabs, "SCP", -SCP_PISO)
        log.info(f"    SCP: {ok} OK, {fail} failed "
                 f"(value={-SCP_PISO} tonf/m2)")
        total_ok += ok
        total_fail += fail
    else:
        log.warning("  No floor slabs — skipping SCP")

    # --- TERT on ALL roof slabs (story 5) ---
    if roof_slabs:
        log.info(f"  Applying TERT to {len(roof_slabs)} roof slabs...")
        ok, fail = _apply_uniform_load(SapModel, roof_slabs, "TERT", -TERT_TECHO)
        log.info(f"    TERT: {ok} OK, {fail} failed "
                 f"(value={-TERT_TECHO} tonf/m2)")
        total_ok += ok
        total_fail += fail
    else:
        log.warning("  No roof slabs — skipping TERT")

    # --- SCT on ALL roof slabs (story 5) ---
    if roof_slabs:
        log.info(f"  Applying SCT to {len(roof_slabs)} roof slabs...")
        ok, fail = _apply_uniform_load(SapModel, roof_slabs, "SCT", -SCT_TECHO)
        log.info(f"    SCT: {ok} OK, {fail} failed "
                 f"(value={-SCT_TECHO} tonf/m2)")
        total_ok += ok
        total_fail += fail
    else:
        log.warning("  No roof slabs — skipping SCT")

    log.info("")
    return total_ok, total_fail


# ===================================================================
# STEP 4: Verification
# ===================================================================

def verify_load_patterns(SapModel):
    """Verify all expected load patterns exist in the model.

    Uses LoadPatterns.GetNameList to enumerate patterns and checks against
    the expected set: {PP, TERP, TERT, SCP, SCT}.

    Firma COM: LoadPatterns.GetNameList() → (count, names_array, ret)
    """
    log.info("Step 4a: Verifying load patterns...")

    expected = set(LOAD_PATTERNS.keys())

    try:
        result = SapModel.LoadPatterns.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            n_patterns = result[0]
            pattern_names = [str(p) for p in result[1]] if result[1] else []
        else:
            log.warning("  GetNameList returned unexpected format")
            return False
    except Exception as e:
        log.warning(f"  LoadPatterns.GetNameList failed: {e}")
        return False

    log.info(f"  Patterns in model ({n_patterns}):")

    found = set()
    for name in pattern_names:
        marker = "✓" if name in expected else ("✗" if name == "Dead" else "?")
        log.info(f"    {marker} {name}")
        if name in expected:
            found.add(name)

    missing = expected - found
    if missing:
        log.warning(f"  MISSING patterns: {missing}")
        return False

    if "Dead" in pattern_names:
        log.warning("  Default 'Dead' pattern still present — "
                    "verify its SWM is 0 to avoid double self-weight")

    log.info(f"  All {len(expected)} expected patterns present ✓")
    return True


def verify_slab_load_summary(classification):
    """Print summary of expected load assignments based on classification."""
    log.info("Step 4b: Load assignment summary...")

    n_floor = len(classification['floor'])
    n_roof = len(classification['roof'])

    log.info(f"  Load assignments performed:")
    log.info(f"    TERP → {n_floor:4d} floor slabs "
             f"× {TERP_PISO} tonf/m2")
    log.info(f"    SCP  → {n_floor:4d} floor slabs "
             f"× {SCP_PISO} tonf/m2 (uniform)")
    log.info(f"    TERT → {n_roof:4d} roof slabs   "
             f"× {TERT_TECHO} tonf/m2")
    log.info(f"    SCT  → {n_roof:4d} roof slabs   "
             f"× {SCT_TECHO} tonf/m2")

    # 4 load types: TERP+SCP on floor, TERT+SCT on roof
    total_assignments = n_floor * 2 + n_roof * 2
    log.info(f"    Total load assignments: {total_assignments}")

    # Quick weight estimate for validation
    # Peso/area ≈ 1 tonf/m2 including self-weight (Lafontaine rule)
    w_terp = TERP_PISO * AREA_LOSA_PISO * N_FLOOR_STORIES
    w_scp = SCP_PISO * AREA_LOSA_PISO * N_FLOOR_STORIES
    w_tert = TERT_TECHO * AREA_LOSA_PISO  # roof has same area
    w_sct = SCT_TECHO * AREA_LOSA_PISO

    log.info(f"")
    log.info(f"  Estimated superimposed load totals (for validation):")
    log.info(f"    TERP total: {w_terp:8.1f} tonf "
             f"({AREA_LOSA_PISO:.1f} m2 x {N_FLOOR_STORIES} stories x {TERP_PISO})")
    log.info(f"    SCP total:  {w_scp:8.1f} tonf "
             f"({AREA_LOSA_PISO:.1f} m2 x {N_FLOOR_STORIES} stories x {SCP_PISO})")
    log.info(f"    TERT total: {w_tert:8.1f} tonf")
    log.info(f"    SCT total:  {w_sct:8.1f} tonf")
    log.info(f"    Total superimposed: {w_terp + w_scp + w_tert + w_sct:.1f} tonf")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: create load patterns and apply loads."""
    log.info("=" * 60)
    log.info("07_loads_ed2.py — Load patterns and uniform loads, Edificio 2")
    log.info("=" * 60)
    log.info("")
    log.info("  Tasks:")
    log.info("    0. Remove default 'Dead' pattern")
    log.info("    1. Create load patterns (PP, TERP, TERT, SCP, SCT)")
    log.info("    2. Classify slabs (floor P1-P4 / roof P5)")
    log.info("    3. Apply uniform loads to all slab areas")
    log.info("    4. Verify patterns and loads")
    log.info("")
    log.info(f"  Expected slabs: {EXPECTED_TOTAL_SLABS} total")
    log.info(f"    Floor (P1-P4): {EXPECTED_FLOOR_SLABS} "
             f"({N_SLABS_PER_STORY} panels x {N_FLOOR_STORIES} stories)")
    log.info(f"    Roof  (P5):    {EXPECTED_ROOF_SLABS}")
    log.info(f"  Load values:")
    log.info(f"    TERP = {TERP_PISO} tonf/m2 | TERT = {TERT_TECHO} tonf/m2")
    log.info(f"    SCP  = {SCP_PISO} tonf/m2 (uniform) | "
             f"SCT  = {SCT_TECHO} tonf/m2")
    log.info("")

    # Connect to ETABS
    log.info("Connecting to ETABS...")
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

        # Step 1: Create load patterns FIRST (before deleting Dead)
        n_created = create_load_patterns(SapModel)
        log.info("")

        # Step 0: Remove default Dead (after PP exists, so model still has a Dead type)
        remove_default_dead(SapModel)
        log.info("")

        # Step 2: Classify slabs
        classification = classify_slabs(SapModel)
        log.info("")

        # Step 3: Apply loads
        n_ok, n_fail = apply_loads(SapModel, classification)

        t_elapsed = time.time() - t_start

        # Step 4: Verification
        log.info("Step 4: Verification...")
        log.info("")
        patterns_ok = verify_load_patterns(SapModel)
        log.info("")
        verify_slab_load_summary(classification)
        log.info("")

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Final report
        log.info("=" * 60)
        log.info("RESULTS")
        log.info("=" * 60)
        log.info(f"  Patterns created: {n_created}/5")
        log.info(f"  Load assignments: {n_ok} OK, {n_fail} failed")
        log.info(f"  Slabs classified: "
                 f"{len(classification['floor'])} floor + "
                 f"{len(classification['roof'])} roof")
        log.info(f"  Patterns verified: {'✓' if patterns_ok else '✗'}")
        log.info(f"  Time: {t_elapsed:.1f}s")
        log.info("")

        if n_fail > 0:
            log.warning(f"  {n_fail} load assignments failed — check warnings above")
        else:
            log.info("  All load patterns and loads applied successfully!")

        log.info("")
        log.info("Ready for next step (08_seismic_ed2.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
