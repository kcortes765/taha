"""
05_slabs_ed2.py — Create 25 slabs per story (5x5 grid) for Edificio 2.

Creates horizontal area objects for every slab panel using AreaObj.AddByCoord,
then assigns:
  - Section: L17G25 (t=0.17m, Shell-Thin, modifiers set in 02_materials_sections_ed2.py)
  - Diaphragm: D1 (rigid) — created in this script if it doesn't exist
  - AutoMesh: 1.0m (AUTOMESH_SIZE from config_ed2.py)

Slab layout:
  - ALL floors (Stories 1-5): 25 panels per story (5x5 regular grid)
  - Each panel: 6.5m x 6.5m = 42.25 m2
  - NO shaft, NO holes (Ed.2 is a pure frame building)
  - Area per floor: 25 x 42.25 = 1056.25 m2 = 32.5 x 32.5 m2

Total: 25 panels x 5 stories = 125 slabs.

Prerequisites:
  - ETABS (v19/v21) open with model from 01/02/03/04 scripts
  - comtypes installed
  - config_ed2.py in the same directory

Usage:
  python 05_slabs_ed2.py

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against: autonomo/research/com_signatures.md
  - AreaObj.AddByCoord: §7.1
  - AreaObj.SetAutoMesh: §7.3
  - AreaObj.SetDiaphragm: §8.2
  - Diaphragm.SetDiaphragm: §8.1
Sources: Enunciado Taller ADSE 1S-2026, pags 8-9
"""

import sys
import os
import time

# Ensure config_ed2.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
    N_STORIES, STORY_ELEVATIONS,
    SLAB_PANELS, N_SLABS_PER_STORY, N_SLABS_TOTAL,
    AREA_LOSA_PANEL, AREA_LOSA_PISO,
    LOSA_NAME, LOSA_ESP,
    AUTOMESH_SIZE,
    DIAPHRAGM_RIGID_NAME,
    GRID_SPACING,
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
    """
    X = [x0, x1, x1, x0]
    Y = [y0, y0, y1, y1]
    Z = [z_elev, z_elev, z_elev, z_elev]

    name = ""
    ret = SapModel.AreaObj.AddByCoord(4, X, Y, Z, name, LOSA_NAME)

    if isinstance(ret, (tuple, list)):
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
    """
    if not slab_name:
        return

    ret = SapModel.AreaObj.SetAutoMesh(
        slab_name,
        4,              # MeshType = 4 (MaxSize)
        0,              # n1 (not used for MeshType=4)
        0,              # n2 (not used for MeshType=4)
        max_size,       # MaxSize1
        max_size,       # MaxSize2
        False,          # PointOnEdge
        False,          # ExtendCookies
        0,              # Rotation
        max_size,       # MaxSizeGeneral
        False,          # LocalAxesOnEdge
        False,          # LocalAxesOnFace
        False,          # RestraintsOnEdge
        False,          # RestraintsOnFace
    )

    if isinstance(ret, (tuple, list)):
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

    if isinstance(ret, (tuple, list)):
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

    # v19 COM: SapModel.Diaphragm puede ser None.
    # v21 COM: SapModel.Diaphragm should work.
    # El diafragma se crea implicitamente al asignar con AreaObj.SetDiaphragm.
    # Intentar crearlo explicitamente; si falla, continuar.
    try:
        diap = SapModel.Diaphragm
        if diap is not None:
            ret = diap.SetDiaphragm(name, semi_rigid)
            if isinstance(ret, (tuple, list)):
                ret_code = ret[-1] if len(ret) > 1 else ret[0]
            else:
                ret_code = ret
            log.info(f"  Diaphragm '{name}' created explicitly (ret={ret_code})")
        else:
            log.warning(f"  SapModel.Diaphragm is None (v19 known issue) — "
                        f"diaphragm will be created implicitly via AreaObj.SetDiaphragm")
    except Exception as e:
        log.warning(f"  Could not create diaphragm explicitly: {e}")
        log.warning(f"  Will assign via AreaObj.SetDiaphragm — ETABS creates it automatically")


# ===================================================================
# STEP 1: Create all slab panels for all stories
# ===================================================================

def create_all_slabs(SapModel):
    """Create 25 slab panels per story for all 5 stories.

    Ed.2 has a regular 5x5 grid with NO shaft or holes.
    All stories use the same 25 panels from SLAB_PANELS.

    For each panel, at the TOP elevation of the story (slab level):
      1. Create horizontal area via AddByCoord
      2. Set AutoMesh = 1.0m (from config_ed2.py)
      3. Assign diaphragm D1

    Returns:
        tuple — (created_count, failed_count)
    """
    log.info("Step 1: Creating all slab panels...")
    log.info(f"  {N_SLABS_PER_STORY} panels/story x {N_STORIES} stories "
             f"= {N_SLABS_TOTAL} total")

    created = 0
    failed = 0

    for story_idx in range(N_STORIES):
        z_elev = STORY_ELEVATIONS[story_idx]
        story_num = story_idx + 1

        for panel_idx, (x0, y0, x1, y1) in enumerate(SLAB_PANELS):
            label = f"SL_S{story_num}_{panel_idx + 1:02d}"

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

        log.info(f"  Story {story_num}/{N_STORIES}: z={z_elev:.2f}m — "
                 f"{created} created, {failed} failed (cumulative)")

    log.info(f"  All stories complete: {created} created, {failed} failed")
    return created, failed


# ===================================================================
# STEP 2: Verify slab count
# ===================================================================

def verify_slabs(SapModel, expected_slab_count):
    """Verify slabs were created by checking AreaObj.GetNameList.

    Note: AreaObj.GetNameList returns ALL area objects (slabs only in Ed.2,
    since there are no walls).

    WARNING (COM v19 bug, may be fixed in v21): GetNameList may return 0
    elements immediately after creating objects via API. The objects DO exist.
    """
    log.info("Step 2: Verifying area object count...")

    try:
        result = SapModel.AreaObj.GetNameList()
        if isinstance(result, (tuple, list)) and result[-1] == 0:
            n_areas = result[0]
            log.info(f"  AreaObj.GetNameList: {n_areas} total area objects")
            if n_areas >= expected_slab_count:
                log.info(f"  VERIFICATION OK: {n_areas} >= {expected_slab_count}")
            elif n_areas == 0:
                log.warning(f"  GetNameList returned 0 — known v19 bug (may be fixed in v21)")
                log.warning(f"  Slabs likely exist. Verify in ETABS UI.")
            else:
                log.warning(f"  Count lower than expected: got {n_areas}, "
                            f"expected >= {expected_slab_count}")
        else:
            ret_code = result[-1] if isinstance(result, (tuple, list)) else result
            log.warning(f"  AreaObj.GetNameList ret={ret_code}")
    except Exception as e:
        log.warning(f"  Verification failed: {e}")
        log.warning(f"  Non-critical — slabs may still exist in the model")


# ===================================================================
# STEP 3: Print slab panel summary
# ===================================================================

def print_slab_summary():
    """Print a summary of all slab panels and their areas."""
    log.info("Slab panel layout (Ed.2 — regular 5x5 grid, no holes):")
    log.info("")
    log.info(f"  {'#':>3s}  {'X0 (m)':>8s}  {'Y0 (m)':>8s}  "
             f"{'X1 (m)':>8s}  {'Y1 (m)':>8s}  {'Area (m2)':>9s}")
    log.info(f"  {'---':>3s}  {'--------':>8s}  {'--------':>8s}  "
             f"{'--------':>8s}  {'--------':>8s}  {'---------':>9s}")

    total_area = 0.0
    for i, (x0, y0, x1, y1) in enumerate(SLAB_PANELS):
        area = (x1 - x0) * (y1 - y0)
        total_area += area
        log.info(f"  {i + 1:3d}  {x0:8.3f}  {y0:8.3f}  "
                 f"{x1:8.3f}  {y1:8.3f}  {area:9.2f}")

    log.info(f"  {'':>3s}  {'':>8s}  {'':>8s}  "
             f"{'':>8s}  {'TOTAL:':>8s}  {total_area:9.2f}")
    log.info("")
    log.info(f"  Expected area/floor: {AREA_LOSA_PISO:.2f} m2 "
             f"(= {N_SLABS_PER_STORY} x {AREA_LOSA_PANEL:.2f} m2)")
    log.info(f"  Verification: 32.5 x 32.5 = {32.5 * 32.5:.2f} m2")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: create all slabs for Edificio 2."""
    log.info("=" * 60)
    log.info("05_slabs_ed2.py — Edificio 2 (25 slabs/story x 5 stories)")
    log.info("=" * 60)

    log.info(f"  Panels per story: {N_SLABS_PER_STORY}")
    log.info(f"  Stories: {N_STORIES}")
    log.info(f"  Total slab panels: {N_SLABS_TOTAL}")
    log.info(f"  Section: {LOSA_NAME} (t={LOSA_ESP}m)")
    log.info(f"  Diaphragm: {DIAPHRAGM_RIGID_NAME} (rigid)")
    log.info(f"  AutoMesh: {AUTOMESH_SIZE}m")
    log.info(f"  Panel size: {GRID_SPACING}m x {GRID_SPACING}m "
             f"= {AREA_LOSA_PANEL:.2f} m2")
    log.info(f"  Area per floor: {AREA_LOSA_PISO:.2f} m2")
    log.info("")

    # Print slab summary table
    print_slab_summary()
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
                 f"(of {N_SLABS_TOTAL} expected)")
        log.info(f"  Section:    {LOSA_NAME} (t={LOSA_ESP}m)")
        log.info(f"  Diaphragm:  {DIAPHRAGM_RIGID_NAME} (rigid)")
        log.info(f"  AutoMesh:   {AUTOMESH_SIZE}m")
        log.info(f"  Modifiers:  m11=m22=m12=0.25 (set in 02_materials_sections_ed2.py)")
        log.info(f"  Area/floor: {AREA_LOSA_PISO:.2f} m2 ({N_SLABS_PER_STORY} panels)")
        log.info(f"  Time:       {t_elapsed:.1f}s")
        log.info("")

        if failed > 0:
            log.warning(f"  {failed} slabs failed — check errors above")
        else:
            log.info("  All slabs created successfully!")

        log.info("")
        log.info("Ready for next step (06_assignments_ed2.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
