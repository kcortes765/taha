"""
06_assignments.py — Post-geometry assignments for Edificio 1.

After all geometry is created (walls, beams, slabs), this script applies:
  1. Diaphragm D1 (rigid) to ALL slab area objects
  2. AutoMesh = 0.4m to ALL area objects (walls + slabs) as safety net
  3. Base restraints: full fixity (6 DOFs) at all nodes at Z=0 (Base level)
  4. Comprehensive verification of all assignments

The first two steps are safety nets — 03_walls.py and 05_slabs.py already
assign AutoMesh and diaphragm individually, but this script ensures nothing
was missed by iterating over ALL area objects in the model.

Base restraints (empotramientos) are the primary new functionality:
  - All nodes at elevation Z=0.0 get full fixity [U1,U2,U3,R1,R2,R3] = True
  - This represents the fixed base condition per the building design

Prerequisites:
  - ETABS v19 open with model from 01-05 scripts
  - comtypes installed
  - config.py in the same directory

Usage:
  python 06_assignments.py

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against: autonomo/research/com_signatures.md
  - Diaphragm.SetDiaphragm: §8.1
  - AreaObj.SetDiaphragm: §8.2
  - AreaObj.SetAutoMesh: §7.3
  - PointObj.GetNameList: §5 (tuple: count, names, ret)
  - PointObj.GetCoordCartesian: (x, y, z, ret)
  - PointObj.SetRestraint: (Name, bool[6], ItemType=0)
Sources: Enunciado Taller ADSE 1S-2026, Prof. Music
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
    # Wall data
    MUROS_DIR_Y, MUROS_DIR_X, N_MUROS_DIR_Y, N_MUROS_DIR_X,
    # Beam data
    N_VIGAS,
    # Slab data
    SLAB_PANELS_FLOOR, SLAB_PANELS_ROOF,
    # Sections
    MURO_30_NAME, MURO_20_NAME, LOSA_NAME, VIGA_NAME,
    # AutoMesh
    AUTOMESH_SIZE,
    # Diaphragm
    DIAPHRAGM_RIGID_NAME,
)

# Full fixity for base restraints: [U1, U2, U3, R1, R2, R3]
BASE_RESTRAINT = [True, True, True, True, True, True]

# Tolerance for Z=0 check (m)
Z_TOLERANCE = 0.01


# ===================================================================
# STEP 0: Create/ensure diaphragm D1 exists
# ===================================================================

def ensure_diaphragm(SapModel, name=DIAPHRAGM_RIGID_NAME, semi_rigid=False):
    """Create or overwrite diaphragm constraint D1 (rigid).

    Firma COM (com_signatures.md §8.1):
      ret = Diaphragm.SetDiaphragm(Name, SemiRigid)
      SemiRigid: False = rigid, True = semi-rigid
    """
    log.info(f"Step 0: Ensuring diaphragm '{name}' exists (rigid={not semi_rigid})...")

    ret = SapModel.Diaphragm.SetDiaphragm(name, semi_rigid)

    if isinstance(ret, tuple):
        ret_code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        ret_code = ret

    if ret_code != 0:
        log.warning(f"  Diaphragm.SetDiaphragm('{name}') ret={ret_code}")
        log.warning(f"  May already exist — proceeding")
    else:
        log.info(f"  Diaphragm '{name}' OK")


# ===================================================================
# STEP 1: Assign diaphragm D1 to ALL slab areas
# ===================================================================

def assign_diaphragm_to_all_areas(SapModel):
    """Assign rigid diaphragm D1 to all area objects in the model.

    Uses AreaObj.GetNameList to get all areas, then filters by section
    to only assign diaphragm to slabs (Losa15G30), not walls.

    Firma COM (com_signatures.md §8.2):
      ret = AreaObj.SetDiaphragm(Name, DiaphragmName)
    """
    log.info("Step 1: Assigning diaphragm D1 to all slab areas...")

    # Get all area objects
    try:
        result = SapModel.AreaObj.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_areas = result[0]
            area_names = result[1]
            ret_code = result[-1] if len(result) > 2 else 0
        else:
            log.warning("  GetNameList returned unexpected format")
            return 0, 0
    except Exception as e:
        log.warning(f"  AreaObj.GetNameList failed: {e}")
        return 0, 0

    if n_areas == 0:
        log.warning("  No area objects found (known v19 bug — areas may still exist)")
        return 0, 0

    log.info(f"  Total area objects: {n_areas}")

    assigned = 0
    skipped = 0
    failed = 0

    for area_name in area_names:
        area_name = str(area_name)

        # Check if this is a slab (not a wall) by reading its section
        try:
            result = SapModel.AreaObj.GetProperty(area_name)
            if isinstance(result, tuple):
                section_name = str(result[0]) if len(result) >= 1 else ""
            else:
                section_name = ""
        except Exception:
            section_name = ""

        # Only assign diaphragm to slabs
        if LOSA_NAME in section_name:
            ret = SapModel.AreaObj.SetDiaphragm(area_name, DIAPHRAGM_RIGID_NAME)
            if isinstance(ret, tuple):
                ret_code = ret[-1] if len(ret) > 1 else ret[0]
            else:
                ret_code = ret

            if ret_code == 0:
                assigned += 1
            else:
                failed += 1
        else:
            skipped += 1

    log.info(f"  Diaphragm assigned: {assigned} slabs, {skipped} non-slabs skipped, "
             f"{failed} failed")
    return assigned, failed


# ===================================================================
# STEP 2: Ensure AutoMesh on ALL area objects
# ===================================================================

def ensure_automesh_all_areas(SapModel, max_size=AUTOMESH_SIZE):
    """Apply AutoMesh = 0.4m to ALL area objects (walls + slabs).

    Safety net: 03_walls.py and 05_slabs.py already set this per-element,
    but this ensures nothing was missed.

    Firma COM (com_signatures.md §7.3):
      ret = AreaObj.SetAutoMesh(Name, MeshType, n1, n2,
                                MaxSize1, MaxSize2, PointOnEdge,
                                ExtendCookies, Rotation, MaxSizeGeneral,
                                LocalAxesOnEdge, LocalAxesOnFace,
                                RestraintsOnEdge, RestraintsOnFace)
      MeshType = 4 (MaxSize)
    """
    log.info(f"Step 2: Ensuring AutoMesh={max_size}m on all area objects...")

    try:
        result = SapModel.AreaObj.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_areas = result[0]
            area_names = result[1]
        else:
            log.warning("  GetNameList returned unexpected format")
            return 0, 0
    except Exception as e:
        log.warning(f"  AreaObj.GetNameList failed: {e}")
        return 0, 0

    if n_areas == 0:
        log.warning("  No area objects found — skipping AutoMesh assignment")
        return 0, 0

    log.info(f"  Applying AutoMesh to {n_areas} area objects...")

    applied = 0
    failed = 0

    for area_name in area_names:
        area_name = str(area_name)

        ret = SapModel.AreaObj.SetAutoMesh(
            area_name,
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
            ret_code = ret[-1] if len(ret) > 1 else ret[0]
        else:
            ret_code = ret

        if ret_code == 0:
            applied += 1
        else:
            failed += 1

    log.info(f"  AutoMesh applied: {applied} OK, {failed} failed")
    return applied, failed


# ===================================================================
# STEP 3: Set base restraints (empotramientos) at Z=0
# ===================================================================

def _extract_z(coord_result):
    """Extract Z coordinate from PointObj.GetCoordCartesian result.

    COM return format varies by binding method:
      - Typical: (x, y, z, ret_code)
      - Some bindings: (x, y, z) without ret
    """
    if isinstance(coord_result, tuple):
        if len(coord_result) >= 3:
            return float(coord_result[2])
    return None


def set_base_restraints(SapModel):
    """Apply full fixity (6 DOFs) to all nodes at Z=0 (base level).

    Process:
      1. Get all point objects via PointObj.GetNameList
      2. For each point, get Z coordinate via GetCoordCartesian
      3. If Z ≈ 0.0 (within tolerance), apply SetRestraint([True]*6)

    Firma COM:
      PointObj.GetNameList() → (count, names_tuple, ret)
      PointObj.GetCoordCartesian(Name) → (x, y, z, ret)
      PointObj.SetRestraint(Name, Value[6]) → ret (0=OK)
    """
    log.info("Step 3: Setting base restraints (empotramientos) at Z=0...")

    # Get all point objects
    try:
        result = SapModel.PointObj.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_points = result[0]
            point_names = result[1]
        else:
            log.error("  PointObj.GetNameList returned unexpected format")
            return 0, 0, 0
    except Exception as e:
        log.error(f"  PointObj.GetNameList failed: {e}")
        return 0, 0, 0

    if n_points == 0:
        log.warning("  No point objects found — cannot assign base restraints")
        return 0, 0, 0

    log.info(f"  Total point objects in model: {n_points}")

    restrained = 0
    not_base = 0
    failed = 0

    for pt_name in point_names:
        pt_name = str(pt_name)

        # Get coordinates
        try:
            coord = SapModel.PointObj.GetCoordCartesian(pt_name)
            z = _extract_z(coord)
            if z is None:
                failed += 1
                continue
        except Exception as e:
            failed += 1
            continue

        # Check if at base level (Z ≈ 0.0)
        if abs(z) <= Z_TOLERANCE:
            # Apply full fixity
            ret = SapModel.PointObj.SetRestraint(pt_name, BASE_RESTRAINT)

            if isinstance(ret, tuple):
                ret_code = ret[-1] if len(ret) > 1 else ret[0]
            else:
                ret_code = ret

            if ret_code == 0:
                restrained += 1
            else:
                failed += 1
                if failed <= 5:
                    log.warning(f"  SetRestraint({pt_name}) ret={ret_code}")
        else:
            not_base += 1

    log.info(f"  Base nodes restrained: {restrained}")
    log.info(f"  Non-base nodes skipped: {not_base}")
    if failed > 0:
        log.warning(f"  Failed: {failed}")

    return restrained, not_base, failed


# ===================================================================
# STEP 4: Verification — comprehensive model check
# ===================================================================

def verify_area_sections(SapModel):
    """Verify all area objects have a section assigned (not 'None' or default).

    Reads each area's property via AreaObj.GetProperty and checks it matches
    one of the expected sections: MHA30G30, MHA20G30, Losa15G30.
    """
    log.info("Step 4a: Verifying area sections...")

    expected_sections = {MURO_30_NAME, MURO_20_NAME, LOSA_NAME}

    try:
        result = SapModel.AreaObj.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_areas = result[0]
            area_names = result[1]
        else:
            log.warning("  Cannot read area list")
            return
    except Exception as e:
        log.warning(f"  AreaObj.GetNameList failed: {e}")
        return

    if n_areas == 0:
        log.warning("  No area objects found (known v19 bug)")
        return

    section_counts = {}
    unassigned = []

    for area_name in area_names:
        area_name = str(area_name)
        try:
            result = SapModel.AreaObj.GetProperty(area_name)
            if isinstance(result, tuple):
                section = str(result[0]) if len(result) >= 1 else "UNKNOWN"
            else:
                section = "UNKNOWN"
        except Exception:
            section = "ERROR"

        section_counts[section] = section_counts.get(section, 0) + 1

        if section not in expected_sections:
            unassigned.append((area_name, section))

    log.info(f"  Section distribution:")
    for sec, count in sorted(section_counts.items()):
        marker = "✓" if sec in expected_sections else "✗"
        log.info(f"    {marker} {sec}: {count} areas")

    if unassigned:
        log.warning(f"  {len(unassigned)} areas with unexpected sections:")
        for name, sec in unassigned[:10]:
            log.warning(f"    {name} → '{sec}'")
        if len(unassigned) > 10:
            log.warning(f"    ... and {len(unassigned) - 10} more")
    else:
        log.info(f"  All {n_areas} areas have expected sections ✓")


def verify_frame_sections(SapModel):
    """Verify all frame objects have a section assigned."""
    log.info("Step 4b: Verifying frame sections...")

    try:
        result = SapModel.FrameObj.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_frames = result[0]
            frame_names = result[1]
        else:
            log.warning("  Cannot read frame list")
            return
    except Exception as e:
        log.warning(f"  FrameObj.GetNameList failed: {e}")
        return

    if n_frames == 0:
        log.warning("  No frame objects found (known v19 bug — beams may still exist)")
        return

    section_counts = {}

    for frame_name in frame_names:
        frame_name = str(frame_name)
        try:
            result = SapModel.FrameObj.GetSection(frame_name)
            if isinstance(result, tuple):
                section = str(result[0]) if len(result) >= 1 else "UNKNOWN"
            else:
                section = "UNKNOWN"
        except Exception:
            section = "ERROR"

        section_counts[section] = section_counts.get(section, 0) + 1

    log.info(f"  Total frames: {n_frames}")
    log.info(f"  Section distribution:")
    for sec, count in sorted(section_counts.items()):
        marker = "✓" if VIGA_NAME in sec else "?"
        log.info(f"    {marker} {sec}: {count} frames")


def verify_base_restraints(SapModel):
    """Verify that all base nodes (Z=0) have full fixity applied.

    Firma COM:
      PointObj.GetRestraint(Name) → (Value[6], ret)
    """
    log.info("Step 4c: Verifying base restraints...")

    try:
        result = SapModel.PointObj.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_points = result[0]
            point_names = result[1]
        else:
            log.warning("  Cannot read point list")
            return
    except Exception as e:
        log.warning(f"  PointObj.GetNameList failed: {e}")
        return

    base_count = 0
    restrained_ok = 0
    not_restrained = 0
    check_errors = 0

    for pt_name in point_names:
        pt_name = str(pt_name)

        try:
            coord = SapModel.PointObj.GetCoordCartesian(pt_name)
            z = _extract_z(coord)
            if z is None:
                continue
        except Exception:
            continue

        if abs(z) <= Z_TOLERANCE:
            base_count += 1

            # Check restraint
            try:
                result = SapModel.PointObj.GetRestraint(pt_name)
                if isinstance(result, tuple) and len(result) >= 1:
                    restraints = result[0]
                    # Check all 6 DOFs are True
                    if hasattr(restraints, '__len__') and len(restraints) >= 6:
                        if all(bool(r) for r in restraints[:6]):
                            restrained_ok += 1
                        else:
                            not_restrained += 1
                    else:
                        check_errors += 1
                else:
                    check_errors += 1
            except Exception:
                check_errors += 1

    log.info(f"  Base nodes (Z=0): {base_count}")
    log.info(f"  Fully restrained: {restrained_ok}")
    if not_restrained > 0:
        log.warning(f"  NOT restrained: {not_restrained}")
    if check_errors > 0:
        log.warning(f"  Check errors: {check_errors}")
    if restrained_ok == base_count and base_count > 0:
        log.info(f"  All base nodes properly restrained ✓")


def verify_no_floating_nodes(SapModel):
    """Check for nodes not connected to any element (floating nodes).

    A floating node has no frame or area object connected to it.
    This is a simplified check — counts total points and compares
    against expected count from geometry.
    """
    log.info("Step 4d: Checking for floating nodes...")

    try:
        # Count points
        pt_result = SapModel.PointObj.GetNameList()
        n_points = pt_result[0] if isinstance(pt_result, tuple) else 0

        # Count areas
        area_result = SapModel.AreaObj.GetNameList()
        n_areas = area_result[0] if isinstance(area_result, tuple) else 0

        # Count frames
        frame_result = SapModel.FrameObj.GetNameList()
        n_frames = frame_result[0] if isinstance(frame_result, tuple) else 0

        log.info(f"  Points: {n_points}")
        log.info(f"  Areas: {n_areas} (walls + slabs)")
        log.info(f"  Frames: {n_frames} (beams)")

        # Expected counts (approximate)
        n_muros_total = (N_MUROS_DIR_Y + N_MUROS_DIR_X) * N_STORIES
        n_slabs_total = (len(SLAB_PANELS_FLOOR) * (N_STORIES - 1) +
                         len(SLAB_PANELS_ROOF))
        n_beams_total = N_VIGAS * N_STORIES
        expected_areas = n_muros_total + n_slabs_total
        expected_frames = n_beams_total

        log.info(f"  Expected areas: ~{expected_areas} "
                 f"({n_muros_total} walls + {n_slabs_total} slabs)")
        log.info(f"  Expected frames: ~{expected_frames} beams")

        if n_areas > 0 and abs(n_areas - expected_areas) > expected_areas * 0.1:
            log.warning(f"  Area count mismatch: got {n_areas}, "
                        f"expected ~{expected_areas}")
        if n_frames > 0 and abs(n_frames - expected_frames) > expected_frames * 0.1:
            log.warning(f"  Frame count mismatch: got {n_frames}, "
                        f"expected ~{expected_frames}")

    except Exception as e:
        log.warning(f"  Floating node check failed: {e}")


# ===================================================================
# STEP 5: Summary statistics
# ===================================================================

def print_element_summary(SapModel):
    """Print a summary of all model elements and their assignments."""
    log.info("=" * 60)
    log.info("ELEMENT SUMMARY")
    log.info("=" * 60)

    # Count by type
    try:
        pt_result = SapModel.PointObj.GetNameList()
        n_points = pt_result[0] if isinstance(pt_result, tuple) else 0
    except Exception:
        n_points = "ERROR"

    try:
        area_result = SapModel.AreaObj.GetNameList()
        n_areas = area_result[0] if isinstance(area_result, tuple) else 0
    except Exception:
        n_areas = "ERROR"

    try:
        frame_result = SapModel.FrameObj.GetNameList()
        n_frames = frame_result[0] if isinstance(frame_result, tuple) else 0
    except Exception:
        n_frames = "ERROR"

    log.info(f"  Points:  {n_points}")
    log.info(f"  Areas:   {n_areas} (walls + slabs)")
    log.info(f"  Frames:  {n_frames} (beams)")
    log.info(f"")
    log.info(f"  Assignments applied:")
    log.info(f"    Diaphragm:  {DIAPHRAGM_RIGID_NAME} (rigid) on all slabs")
    log.info(f"    AutoMesh:   {AUTOMESH_SIZE}m on all areas")
    log.info(f"    Base fixity: Full [U1-R3] at Z=0")
    log.info(f"")
    log.info(f"  Expected element counts per story:")
    log.info(f"    Walls: {N_MUROS_DIR_Y + N_MUROS_DIR_X} "
             f"({N_MUROS_DIR_Y} dir-Y + {N_MUROS_DIR_X} dir-X)")
    log.info(f"    Beams: {N_VIGAS}")
    log.info(f"    Slabs: {len(SLAB_PANELS_FLOOR)} (floor) / "
             f"{len(SLAB_PANELS_ROOF)} (roof)")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: apply all post-geometry assignments."""
    log.info("=" * 60)
    log.info("06_assignments.py — Post-geometry assignments, Edificio 1")
    log.info("=" * 60)
    log.info("")
    log.info("  Tasks:")
    log.info("    1. Diaphragm D1 (rigid) → all slab areas")
    log.info("    2. AutoMesh 0.4m → all area objects (safety net)")
    log.info("    3. Base restraints → full fixity at Z=0")
    log.info("    4. Verification of all assignments")
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

        # Step 0: Ensure diaphragm D1 exists
        ensure_diaphragm(SapModel)
        log.info("")

        # Step 1: Assign diaphragm to all slabs
        n_diaphragm, n_diaphragm_fail = assign_diaphragm_to_all_areas(SapModel)
        log.info("")

        # Step 2: Ensure AutoMesh on all areas
        n_mesh, n_mesh_fail = ensure_automesh_all_areas(SapModel)
        log.info("")

        # Step 3: Set base restraints
        n_restrained, n_not_base, n_restraint_fail = set_base_restraints(SapModel)
        log.info("")

        t_elapsed = time.time() - t_start

        # Step 4: Verification
        log.info("Step 4: Comprehensive verification...")
        log.info("")
        verify_area_sections(SapModel)
        log.info("")
        verify_frame_sections(SapModel)
        log.info("")
        verify_base_restraints(SapModel)
        log.info("")
        verify_no_floating_nodes(SapModel)
        log.info("")

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Step 5: Summary
        print_element_summary(SapModel)
        log.info("")

        # Final report
        log.info("=" * 60)
        log.info("RESULTS")
        log.info("=" * 60)
        log.info(f"  Diaphragm D1:  {n_diaphragm} slabs assigned "
                 f"({n_diaphragm_fail} failed)")
        log.info(f"  AutoMesh 0.4m: {n_mesh} areas assigned "
                 f"({n_mesh_fail} failed)")
        log.info(f"  Base fixity:   {n_restrained} nodes restrained "
                 f"({n_restraint_fail} failed)")
        log.info(f"  Time:          {t_elapsed:.1f}s")
        log.info("")

        total_failures = n_diaphragm_fail + n_mesh_fail + n_restraint_fail
        if total_failures > 0:
            log.warning(f"  Total failures: {total_failures} — check warnings above")
        else:
            log.info("  All assignments completed successfully!")

        log.info("")
        log.info("Ready for next step (07_loads.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
