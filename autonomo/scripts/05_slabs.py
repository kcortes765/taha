"""
05_slabs.py — Draw ALL slabs (losas) for Edificio 1, all 20 stories.

Creates horizontal area objects for every slab panel using AreaObj.AddByCoord,
then assigns:
  - Section: Losa15G30 (t=0.15m, Shell-Thin, modifiers set in 02_materials_sections.py)
  - Diaphragm: D1 (rigid) — created in this script if it doesn't exist
  - AutoMesh: 0.4m (max element size)

Slab panels are defined as real floor footprint (NOT full envelope):
  - Typical floors (Stories 1-19): 7 panels per story (~468 m2)
    Excludes: shaft elevator (axes 9-11, C-D), stairwell zone (axes 1-3, A-B)
  - Roof (Story 20): 5 panels (~420 m2)
    Excludes: same shaft + no southern balconies/overhangs

Total: 7*19 + 5*1 = 138 slab panels

Prerequisites:
  - ETABS v19 open with model from 01/02/03/04 scripts
  - comtypes installed
  - config.py in the same directory

Usage:
  python 05_slabs.py

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against: autonomo/research/com_signatures.md
  - AreaObj.AddByCoord: §7.1
  - AreaObj.SetAutoMesh: §7.3
  - AreaObj.SetDiaphragm: §8.2
  - Diaphragm.SetDiaphragm: §8.1
Sources: Enunciado Taller ADSE 1S-2026, Prof. Music (pag 2 — planta tipo)
         config.py SLAB_PANELS_FLOOR / SLAB_PANELS_ROOF
"""

import sys
import os
import time

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
    # Stories
    N_STORIES, STORY_ELEVATIONS,
    # Slab data
    SLAB_PANELS_FLOOR, SLAB_PANELS_ROOF,
    AREA_PISO_TIPO, AREA_TECHO,
    # Slab section
    LOSA_NAME, LOSA_ESP,
    # AutoMesh
    AUTOMESH_SIZE,
    # Diaphragm
    DIAPHRAGM_RIGID_NAME,
    # Helpers for area calculation
    _panels_area, _rect_area,
)


# ===================================================================
# HELPER: Create a single slab panel (horizontal area object)
# ===================================================================

def create_slab_panel(SapModel, x0, y0, x1, y1, z_elev, slab_label=""):
    """Create a single horizontal slab panel (4-node area object) via AreaObj.AddByCoord.

    Args:
        SapModel: ETABS SapModel COM object
        x0, y0: float — bottom-left corner coordinates
        x1, y1: float — top-right corner coordinates
        z_elev: float — elevation (top of story = slab level)
        slab_label: str — descriptive label for logging

    Returns:
        str — name assigned by ETABS to the created area object

    Vertices defined counterclockwise (looking from above):
      P1: (x0, y0, z)  — bottom-left
      P2: (x1, y0, z)  — bottom-right
      P3: (x1, y1, z)  — top-right
      P4: (x0, y1, z)  — top-left

    Firma COM (com_signatures.md §7.1):
      ret = AreaObj.AddByCoord(NumberPoints, X[], Y[], Z[],
                               ref Name, PropName, UserName, CSys)
      NumberPoints = 4 (rectangular panel)
      X, Y, Z = float arrays with 4 elements each
      Name = "" (ETABS assigns name)
      PropName = section name
    """
    X = [x0, x1, x1, x0]
    Y = [y0, y0, y1, y1]
    Z = [z_elev, z_elev, z_elev, z_elev]

    name = ""
    ret = SapModel.AreaObj.AddByCoord(4, X, Y, Z, name, LOSA_NAME)

    # ret is typically (assigned_name, 0) on success
    if isinstance(ret, tuple):
        assigned_name = ret[0] if len(ret) >= 2 else ""
        ret_code = ret[-1]
    else:
        assigned_name = ""
        ret_code = ret

    if ret_code != 0:
        raise RuntimeError(
            f"AreaObj.AddByCoord failed (ret={ret_code}): {slab_label} "
            f"x=[{x0:.3f},{x1:.3f}] y=[{y0:.3f},{y1:.3f}] z={z_elev:.3f}"
        )

    return str(assigned_name) if assigned_name else ""


# ===================================================================
# HELPER: Set AutoMesh on a slab panel
# ===================================================================

def set_slab_automesh(SapModel, slab_name, max_size=AUTOMESH_SIZE):
    """Set AutoMesh on a slab panel.

    Firma COM (com_signatures.md §7.3):
      ret = AreaObj.SetAutoMesh(Name, MeshType, n1, n2,
                                MaxSize1, MaxSize2, PointOnEdge,
                                ExtendCookies, Rotation, MaxSizeGeneral,
                                LocalAxesOnEdge, LocalAxesOnFace,
                                RestraintsOnEdge, RestraintsOnFace)
      MeshType = 4 (MaxSize — mesh by maximum element size)
      MaxSize1, MaxSize2, MaxSizeGeneral = 0.4 m
    """
    if not slab_name:
        return

    ret = SapModel.AreaObj.SetAutoMesh(
        slab_name,
        4,              # MeshType = 4 (MaxSize)
        0,              # n1 (not used for MeshType=4)
        0,              # n2 (not used for MeshType=4)
        max_size,       # MaxSize1 = 0.4 m
        max_size,       # MaxSize2 = 0.4 m
        False,          # PointOnEdge
        False,          # ExtendCookies
        0,              # Rotation
        max_size,       # MaxSizeGeneral = 0.4 m
        False,          # LocalAxesOnEdge
        False,          # LocalAxesOnFace
        False,          # RestraintsOnEdge
        False,          # RestraintsOnFace
    )

    if isinstance(ret, tuple):
        ret = ret[-1] if len(ret) > 1 else ret[0]
    if ret != 0:
        log.warning(f"  SetAutoMesh({slab_name}) ret={ret} — non-critical")


# ===================================================================
# HELPER: Assign diaphragm to a slab panel
# ===================================================================

def set_slab_diaphragm(SapModel, slab_name, diaphragm=DIAPHRAGM_RIGID_NAME):
    """Assign rigid diaphragm to a slab panel.

    Firma COM (com_signatures.md §8.2):
      ret = AreaObj.SetDiaphragm(Name, DiaphragmName, ItemType)
      ItemType = 0 (Object) — default, optional
    """
    if not slab_name:
        return

    ret = SapModel.AreaObj.SetDiaphragm(slab_name, diaphragm)

    if isinstance(ret, tuple):
        ret_code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        ret_code = ret

    if ret_code != 0:
        log.warning(f"  SetDiaphragm({slab_name}, {diaphragm}) "
                    f"ret={ret_code} — non-critical")


# ===================================================================
# STEP 0: Create diaphragm D1 (rigid)
# ===================================================================

def create_diaphragm(SapModel, name=DIAPHRAGM_RIGID_NAME, semi_rigid=False):
    """Create (or overwrite) a diaphragm constraint.

    Firma COM (com_signatures.md §8.1):
      ret = Diaphragm.SetDiaphragm(Name, SemiRigid)
      SemiRigid: True=semi-rigid, False=rigid
    """
    log.info(f"Step 0: Creating diaphragm '{name}' "
             f"(rigid={not semi_rigid})...")

    ret = SapModel.Diaphragm.SetDiaphragm(name, semi_rigid)

    if isinstance(ret, tuple):
        ret_code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        ret_code = ret

    if ret_code != 0:
        log.warning(f"  Diaphragm.SetDiaphragm('{name}') ret={ret_code}")
        log.warning(f"  May already exist — proceeding anyway")
    else:
        log.info(f"  Diaphragm '{name}' created successfully")


# ===================================================================
# STEP 1: Create all slab panels for all stories
# ===================================================================

def create_all_slabs(SapModel):
    """Create all slab panels for all 20 stories.

    Stories 1-19: SLAB_PANELS_FLOOR (7 panels per story)
    Story 20: SLAB_PANELS_ROOF (5 panels)

    For each panel, at the TOP elevation of the story (slab level):
      1. Create horizontal area via AddByCoord
      2. Set AutoMesh = 0.4m
      3. Assign diaphragm D1

    Returns:
        tuple — (created_count, failed_count)
    """
    log.info("Step 1: Creating all slab panels...")

    n_floor_panels = len(SLAB_PANELS_FLOOR)
    n_roof_panels = len(SLAB_PANELS_ROOF)
    n_floor_stories = N_STORIES - 1  # 19
    total_expected = n_floor_panels * n_floor_stories + n_roof_panels
    log.info(f"  Floor: {n_floor_panels} panels/story x {n_floor_stories} stories "
             f"= {n_floor_panels * n_floor_stories}")
    log.info(f"  Roof:  {n_roof_panels} panels x 1 story = {n_roof_panels}")
    log.info(f"  Total: {total_expected} slab panels")

    created = 0
    failed = 0

    for story_idx in range(N_STORIES):
        z_elev = STORY_ELEVATIONS[story_idx]
        story_num = story_idx + 1

        # Select panel set: roof for last story, typical for others
        if story_num == N_STORIES:
            panels = SLAB_PANELS_ROOF
            panel_type = "ROOF"
        else:
            panels = SLAB_PANELS_FLOOR
            panel_type = "FLOOR"

        for panel_idx, (x0, y0, x1, y1) in enumerate(panels):
            label = f"SL-{panel_type[0]}{panel_idx}-S{story_num}"

            try:
                # Create horizontal slab panel
                slab_name = create_slab_panel(
                    SapModel,
                    x0=x0, y0=y0,
                    x1=x1, y1=y1,
                    z_elev=z_elev,
                    slab_label=label,
                )

                # Set AutoMesh
                set_slab_automesh(SapModel, slab_name)

                # Assign diaphragm D1
                set_slab_diaphragm(SapModel, slab_name)

                created += 1
            except RuntimeError as e:
                log.error(f"  FAILED: {e}")
                failed += 1

        # Log progress every 5 stories
        if story_num % 5 == 0 or story_num == 1 or story_num == N_STORIES:
            log.info(f"  Story {story_num}/{N_STORIES} ({panel_type}): "
                     f"{created} created, {failed} failed")

    log.info(f"  All stories complete: {created} created, {failed} failed")
    return created, failed


# ===================================================================
# STEP 2: Verify slab count
# ===================================================================

def verify_slabs(SapModel, expected_slab_count):
    """Verify slabs were created by checking AreaObj.GetNameList.

    Note: AreaObj.GetNameList returns ALL area objects (walls + slabs).
    We compare against expected_slab_count + walls from previous scripts.
    In ETABS v19, GetNameList may return 0 after COM creation (known bug).
    """
    log.info("Step 2: Verifying area object count...")

    try:
        result = SapModel.AreaObj.GetNameList()
        if isinstance(result, tuple) and result[-1] == 0:
            n_areas = result[0]
            log.info(f"  AreaObj.GetNameList: {n_areas} total area objects")
            log.info(f"  (includes walls from 03_walls.py + slabs from this script)")
            if n_areas >= expected_slab_count:
                log.info(f"  Count OK (expected >= {expected_slab_count} slabs)")
            elif n_areas == 0:
                log.warning(f"  GetNameList returned 0 — known v19 bug")
                log.warning(f"  Slabs likely exist. Verify in ETABS UI.")
            else:
                log.warning(f"  Count lower than expected: got {n_areas}, "
                            f"expected >= {expected_slab_count}")
        else:
            ret_code = result[-1] if isinstance(result, tuple) else result
            log.warning(f"  AreaObj.GetNameList ret={ret_code}")
    except Exception as e:
        log.warning(f"  Verification failed: {e}")
        log.warning(f"  Non-critical — slabs may still exist in the model")


# ===================================================================
# STEP 3: Print slab panel summary
# ===================================================================

def print_slab_summary():
    """Print a summary of all slab panels and their areas."""
    log.info("Slab panel layout:")
    log.info("")

    # Typical floor panels
    log.info(f"  Typical Floor Panels (Stories 1-{N_STORIES - 1}):")
    log.info(f"    {'#':>3s}  {'X0 (m)':>8s}  {'Y0 (m)':>8s}  "
             f"{'X1 (m)':>8s}  {'Y1 (m)':>8s}  {'Area (m2)':>9s}")
    log.info(f"    {'---':>3s}  {'--------':>8s}  {'--------':>8s}  "
             f"{'--------':>8s}  {'--------':>8s}  {'---------':>9s}")

    total_floor_area = 0.0
    for i, (x0, y0, x1, y1) in enumerate(SLAB_PANELS_FLOOR):
        area = _rect_area((x0, y0, x1, y1))
        total_floor_area += area
        log.info(f"    {i:3d}  {x0:8.3f}  {y0:8.3f}  "
                 f"{x1:8.3f}  {y1:8.3f}  {area:9.2f}")

    log.info(f"    {'':>3s}  {'':>8s}  {'':>8s}  "
             f"{'':>8s}  {'TOTAL:':>8s}  {total_floor_area:9.2f}")
    log.info("")

    # Roof panels
    log.info(f"  Roof Panels (Story {N_STORIES}):")
    log.info(f"    {'#':>3s}  {'X0 (m)':>8s}  {'Y0 (m)':>8s}  "
             f"{'X1 (m)':>8s}  {'Y1 (m)':>8s}  {'Area (m2)':>9s}")
    log.info(f"    {'---':>3s}  {'--------':>8s}  {'--------':>8s}  "
             f"{'--------':>8s}  {'--------':>8s}  {'---------':>9s}")

    total_roof_area = 0.0
    for i, (x0, y0, x1, y1) in enumerate(SLAB_PANELS_ROOF):
        area = _rect_area((x0, y0, x1, y1))
        total_roof_area += area
        log.info(f"    {i:3d}  {x0:8.3f}  {y0:8.3f}  "
                 f"{x1:8.3f}  {y1:8.3f}  {area:9.2f}")

    log.info(f"    {'':>3s}  {'':>8s}  {'':>8s}  "
             f"{'':>8s}  {'TOTAL:':>8s}  {total_roof_area:9.2f}")
    log.info("")

    # Shaft gap description
    log.info("  Shaft elevator gap (omitted from panels):")
    log.info("    Between axes 9-11 (X), C-D (Y)")
    log.info("    Size: ~7.7 x 2.345 m (from enunciado)")
    log.info("")

    # Totals
    n_floor = len(SLAB_PANELS_FLOOR)
    n_roof = len(SLAB_PANELS_ROOF)
    n_floor_stories = N_STORIES - 1
    log.info(f"  Summary:")
    log.info(f"    Floor panels: {n_floor} x {n_floor_stories} stories = "
             f"{n_floor * n_floor_stories}")
    log.info(f"    Roof panels:  {n_roof} x 1 story = {n_roof}")
    log.info(f"    Total panels: {n_floor * n_floor_stories + n_roof}")
    log.info(f"    Floor area:   {total_floor_area:.1f} m2/story "
             f"(expected ~468 m2)")
    log.info(f"    Roof area:    {total_roof_area:.1f} m2")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: create all slabs for Edificio 1."""
    log.info("=" * 60)
    log.info("05_slabs.py — Edificio 1 (All slabs, 20 stories)")
    log.info("=" * 60)

    n_floor_panels = len(SLAB_PANELS_FLOOR)
    n_roof_panels = len(SLAB_PANELS_ROOF)
    n_floor_stories = N_STORIES - 1
    total_panels = n_floor_panels * n_floor_stories + n_roof_panels

    # Print expected parameters
    log.info(f"  Floor panels per story: {n_floor_panels}")
    log.info(f"  Roof panels: {n_roof_panels}")
    log.info(f"  Stories (floor): {n_floor_stories}")
    log.info(f"  Total slab panels to create: {total_panels}")
    log.info(f"  Section: {LOSA_NAME} (t={LOSA_ESP}m)")
    log.info(f"  Diaphragm: {DIAPHRAGM_RIGID_NAME} (rigid)")
    log.info(f"  AutoMesh: {AUTOMESH_SIZE}m")
    log.info(f"  Expected floor area: ~{AREA_PISO_TIPO:.1f} m2/story")
    log.info(f"  Expected roof area:  ~{AREA_TECHO:.1f} m2")
    log.info("")

    # Print slab summary table
    print_slab_summary()
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

        # Step 0: Create diaphragm D1
        create_diaphragm(SapModel)
        log.info("")

        # Step 1: Create all slab panels
        created, failed = create_all_slabs(SapModel)
        log.info("")

        t_elapsed = time.time() - t_start

        # Step 2: Verify
        verify_slabs(SapModel, created)
        log.info("")

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Summary
        log.info("=" * 60)
        log.info("SUMMARY")
        log.info("=" * 60)
        log.info(f"  Total:      {created} created, {failed} failed "
                 f"(of {total_panels} expected)")
        log.info(f"  Section:    {LOSA_NAME} (t={LOSA_ESP}m)")
        log.info(f"  Diaphragm:  {DIAPHRAGM_RIGID_NAME} (rigid)")
        log.info(f"  AutoMesh:   {AUTOMESH_SIZE}m")
        log.info(f"  Modifiers:  m11=m22=m12=0.25 (set in 02_materials_sections.py)")
        log.info(f"  Floor area: ~{AREA_PISO_TIPO:.1f} m2/story ({n_floor_panels} panels)")
        log.info(f"  Roof area:  ~{AREA_TECHO:.1f} m2 ({n_roof_panels} panels)")
        log.info(f"  Time:       {t_elapsed:.1f}s")
        log.info("")

        if failed > 0:
            log.warning(f"  {failed} slabs failed — check errors above")
        else:
            log.info("  All slabs created successfully!")

        log.info("")
        log.info("Ready for next step (06_loads.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
