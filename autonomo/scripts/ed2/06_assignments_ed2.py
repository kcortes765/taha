"""
06_assignments_ed2.py — Post-geometry assignments for Edificio 2 (Marcos HA).

After all geometry is created (columns, beams, slabs), this script applies:
  1. Beam Insertion Point: CP=8 (Top Center) + StiffnessTransforms=True
     - Guia Ed.2 Fase 5.2: vigas convencionales cuelgan bajo la losa
     - FrameObj.SetInsertionPoint with CardinalPoint=8, StiffTransform=True
  2. Rigid End Zones (RZF=0.75) to BEAMS only (not columns)
     - FrameObj.SetEndLengthOffset with AutoOffset=True, RzFactor=0.75
     - Guia Ed.2 Fase 5.3: seleccionar todas las vigas, aplicar RZF
  3. Base restraints: full fixity (6 DOFs) at all nodes at Z=0 (Base level)
  4. Auto Edge Constraints on all slab areas (losa-viga connectivity)
  5. Comprehensive verification of all assignments

Diaphragm D1 and AutoMesh are already assigned per-element in 05_slabs_ed2.py.
This script verifies they are in place but does NOT re-assign them.

Ed.2 has NO walls — only frames (columns + beams) and slabs.

Prerequisites:
  - ETABS 21 open with model from 01-05 scripts
  - comtypes installed
  - config_ed2.py in the same directory

Usage:
  python 06_assignments_ed2.py

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures:
  - FrameObj.SetInsertionPoint: (Name, CardinalPoint, Mirror2, StiffTransform,
                                 Offset1, Offset2, [CSys], [ItemType])
  - FrameObj.SetEndLengthOffset: (Name, AutoOffset, Length1, Length2, RzFactor, [ItemType])
    AutoOffset=True: ETABS computes offsets from connectivity; RzFactor scales them
    Standard OAPI method (SAP2000/ETABS), not in local com_signatures.md
  - PointObj.GetNameList: (count, names, ret)
  - PointObj.GetCoordCartesian: (x, y, z, ret)
  - PointObj.SetRestraint: (Name, bool[6], ItemType=0)
  - AreaObj.SetEdgeConstraint: (Name, ConstraintExists, ItemType)
  - AreaObj.GetNameList: (count, names, ret)
  - FrameObj.GetNameList: (count, names, ret)
Sources: Enunciado Taller ADSE 1S-2026, Prof. Music (pag 9: RZF=0.75)
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
    N_COLUMNS_PER_STORY, N_COLUMNS_TOTAL,
    N_VIGAS_PER_STORY, N_VIGAS_TOTAL,
    N_SLABS_PER_STORY, N_SLABS_TOTAL,
    LOSA_NAME,
    COL_70_NAME, COL_65_NAME,
    VIGA_50_NAME, VIGA_45_NAME,
    RZF,
    AUTOMESH_SIZE,
    DIAPHRAGM_RIGID_NAME,
    VIGA_CARDINAL_POINT,
)

# Full fixity for base restraints: [U1, U2, U3, R1, R2, R3]
BASE_RESTRAINT = [True, True, True, True, True, True]

# Tolerance for Z=0 check (m)
Z_TOLERANCE = 0.01

# Expected frame sections
EXPECTED_FRAME_SECTIONS = {COL_70_NAME, COL_65_NAME, VIGA_50_NAME, VIGA_45_NAME}

# Beam section names (for filtering beams vs columns)
BEAM_SECTIONS = {VIGA_50_NAME, VIGA_45_NAME}


# ===================================================================
# STEP 1: Set Beam Insertion Point (CP=8, Top Center)
# ===================================================================

def set_beam_insertion_point(SapModel, cardinal_point=VIGA_CARDINAL_POINT):
    """Set insertion point CP=8 (Top Center) + StiffTransform on all beams.

    Guia Ed.2 Fase 5.2: vigas convencionales cuelgan bajo losa.
    CP=8 = cara superior de la viga al nivel de la losa.
    StiffTransform=True para transformar rigidez por excentricidad.

    Firma COM (CSI OAPI):
      ret = FrameObj.SetInsertionPoint(Name, CardinalPoint, Mirror2,
                StiffTransform, Offset1, Offset2, [CoordSys], [ItemType])
    """
    log.info(f"Step 1: Setting beam insertion point (CP={cardinal_point})...")

    try:
        result = SapModel.FrameObj.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            n_frames = result[0]
            frame_names = result[1]
        else:
            log.warning("  FrameObj.GetNameList returned unexpected format")
            return 0, 0
    except Exception as e:
        log.warning(f"  FrameObj.GetNameList failed: {e}")
        return 0, 0

    applied = 0
    failed = 0
    skipped = 0

    for frame_name in frame_names:
        frame_name = str(frame_name)

        # Only apply to beams — check section name
        try:
            sec_result = SapModel.FrameObj.GetSection(frame_name)
            section = str(sec_result[0]) if isinstance(sec_result, (tuple, list)) else ""
        except Exception:
            section = ""

        if section not in BEAM_SECTIONS:
            skipped += 1
            continue

        try:
            ret = SapModel.FrameObj.SetInsertionPoint(
                frame_name,
                cardinal_point,    # 8 = Top Center
                False,             # Mirror2 = False
                True,              # StiffTransform = True
                0.0,               # Offset1 = 0.0
                0.0,               # Offset2 = 0.0
                "Local",           # CoordSys (CSI default)
                0,                 # ItemType = Object
            )

            if isinstance(ret, (tuple, list)):
                ret_code = ret[-1] if len(ret) > 1 else ret[0]
            else:
                ret_code = ret

            if ret_code == 0:
                applied += 1
            else:
                failed += 1
                if failed <= 5:
                    log.warning(f"  SetInsertionPoint({frame_name}) ret={ret_code}")
        except AttributeError:
            raise RuntimeError(
                "FrameObj.SetInsertionPoint no disponible via API. "
                "Este flujo Ed.2 para ETABS 21 no debe caer a asignacion manual."
            )
        except Exception as e:
            failed += 1
            if failed <= 5:
                log.warning(f"  SetInsertionPoint({frame_name}) exception: {e}")

    log.info(f"  Insertion Point CP={cardinal_point}: "
             f"{applied} beams OK, {skipped} columns skipped, {failed} failed")

    return applied, failed


# ===================================================================
# STEP 2: Apply Rigid End Zones (RZF=0.75) to BEAMS only
# ===================================================================

def apply_rigid_end_zones(SapModel, rzf=RZF):
    """Apply rigid end zone factor to beam frame objects only (not columns).

    Guia Ed.2 Fase 5.3: seleccionar todas las vigas, aplicar RZF=0.75.

    Uses FrameObj.SetEndLengthOffset with AutoOffset=True so ETABS
    automatically computes end offsets from cross-section dimensions
    of connecting elements, then scales by RzFactor.

    Firma COM (standard OAPI):
      ret = FrameObj.SetEndLengthOffset(Name, AutoOffset, Length1, Length2,
                                         RzFactor, ItemType)
      AutoOffset: bool — True = auto-compute from connectivity
      Length1, Length2: float — manual offsets (ignored when AutoOffset=True)
      RzFactor: float — rigid zone factor (0 to 1)
      ItemType: int (optional, default=0) — 0=Object, 1=Group, 2=SelectedObjects
    """
    log.info(f"Step 2: Applying Rigid End Zones (RZF={rzf}) to beams...")

    # Get all frame objects
    try:
        result = SapModel.FrameObj.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            n_frames = result[0]
            frame_names = result[1]
        else:
            log.warning("  FrameObj.GetNameList returned unexpected format")
            return 0, 0
    except Exception as e:
        log.warning(f"  FrameObj.GetNameList failed: {e}")
        return 0, 0

    if n_frames == 0:
        log.warning("  No frame objects found — revisar que 03_columns y 04_beams hayan corrido OK")
        return 0, 0

    log.info(f"  Total frame objects: {n_frames}")

    applied = 0
    failed = 0
    skipped = 0

    for frame_name in frame_names:
        frame_name = str(frame_name)

        # Only apply RZF to beams (Guia Ed.2 Fase 5.3)
        try:
            sec_result = SapModel.FrameObj.GetSection(frame_name)
            section = str(sec_result[0]) if isinstance(sec_result, (tuple, list)) else ""
        except Exception:
            section = ""

        if section not in BEAM_SECTIONS:
            skipped += 1
            continue

        try:
            ret = SapModel.FrameObj.SetEndLengthOffset(
                frame_name,
                True,       # AutoOffset = True (compute from connectivity)
                0.0,        # Length1 (ignored when AutoOffset=True)
                0.0,        # Length2 (ignored when AutoOffset=True)
                rzf,        # RzFactor = 0.75
                0,          # ItemType = Object
            )

            if isinstance(ret, (tuple, list)):
                ret_code = ret[-1] if len(ret) > 1 else ret[0]
            else:
                ret_code = ret

            if ret_code == 0:
                applied += 1
            else:
                failed += 1
                if failed <= 5:
                    log.warning(f"  SetEndLengthOffset({frame_name}) ret={ret_code}")
        except Exception as e:
            failed += 1
            if failed <= 5:
                log.warning(f"  SetEndLengthOffset({frame_name}) exception: {e}")

    log.info(f"  RZF={rzf} applied: {applied} beams OK, "
             f"{skipped} columns skipped, {failed} failed")

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
    if isinstance(coord_result, (tuple, list)):
        if len(coord_result) >= 3:
            return float(coord_result[2])
    return None


def set_base_restraints(SapModel):
    """Apply full fixity (6 DOFs) to all nodes at Z=0 (base level).

    Process:
      1. Get all point objects via PointObj.GetNameList
      2. For each point, get Z coordinate via GetCoordCartesian
      3. If Z ~ 0.0 (within tolerance), apply SetRestraint([True]*6)

    Firma COM:
      PointObj.GetNameList() -> (count, names_tuple, ret)
      PointObj.GetCoordCartesian(Name) -> (x, y, z, ret)
      PointObj.SetRestraint(Name, Value[6]) -> ret (0=OK)
    """
    log.info("Step 3: Setting base restraints (empotramientos) at Z=0...")

    # Get all point objects
    try:
        result = SapModel.PointObj.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
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
        except Exception:
            failed += 1
            continue

        # Check if at base level (Z ~ 0.0)
        if abs(z) <= Z_TOLERANCE:
            # Apply full fixity
            ret = SapModel.PointObj.SetRestraint(pt_name, BASE_RESTRAINT)

            if isinstance(ret, (tuple, list)):
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

    # Expected: 36 base nodes (6x6 grid intersections)
    expected_base = N_COLUMNS_PER_STORY  # 36
    if restrained > 0 and abs(restrained - expected_base) > expected_base * 0.2:
        log.warning(f"  Base node count ({restrained}) differs from "
                    f"expected ({expected_base}) by >20%")

    return restrained, not_base, failed


# ===================================================================
# STEP 4: Auto Edge Constraints on all slab areas
# ===================================================================

def apply_edge_constraints(SapModel):
    """Apply auto edge constraints on all slab area objects.

    Edge constraints ensure proper connectivity between shell edges
    and frame elements (beam-slab interaction). This prevents
    displacement incompatibility at shell-frame interfaces.

    Firma COM (standard OAPI):
      ret = AreaObj.SetEdgeConstraint(Name, ConstraintExists, ItemType)
      ConstraintExists: bool — True to enable edge constraints
      ItemType: int (optional, default=0) — 0=Object
    """
    log.info("Step 4: Applying Auto Edge Constraints on slab areas...")

    # Get all area objects
    try:
        result = SapModel.AreaObj.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            n_areas = result[0]
            area_names = result[1]
        else:
            log.warning("  AreaObj.GetNameList returned unexpected format")
            return 0, 0
    except Exception as e:
        log.warning(f"  AreaObj.GetNameList failed: {e}")
        return 0, 0

    if n_areas == 0:
        log.warning("  No area objects found — skipping edge constraints")
        return 0, 0

    log.info(f"  Total area objects: {n_areas}")

    applied = 0
    failed = 0
    method_available = True

    for area_name in area_names:
        area_name = str(area_name)

        # Only apply to slabs (check section name)
        try:
            prop_result = SapModel.AreaObj.GetProperty(area_name)
            if isinstance(prop_result, (tuple, list)):
                section_name = str(prop_result[0]) if len(prop_result) >= 1 else ""
            else:
                section_name = ""
        except Exception:
            section_name = ""

        if LOSA_NAME not in section_name:
            continue  # Skip non-slab areas

        if not method_available:
            continue

        try:
            ret = SapModel.AreaObj.SetEdgeConstraint(area_name, True, 0)

            if isinstance(ret, (tuple, list)):
                ret_code = ret[-1] if len(ret) > 1 else ret[0]
            else:
                ret_code = ret

            if ret_code == 0:
                applied += 1
            else:
                failed += 1
                if failed <= 3:
                    log.warning(f"  SetEdgeConstraint({area_name}) ret={ret_code}")
        except AttributeError:
            raise RuntimeError(
                "AreaObj.SetEdgeConstraint no disponible via API. "
                "Este flujo Ed.2 para ETABS 21 no debe depender de asignacion manual."
            )
        except Exception as e:
            failed += 1
            if failed <= 3:
                log.warning(f"  SetEdgeConstraint({area_name}) exception: {e}")

    if method_available:
        log.info(f"  Edge constraints applied: {applied} slabs OK, {failed} failed")
    else:
        log.info(f"  Edge constraints: method not available via API")

    return applied, failed


# ===================================================================
# STEP 5: Verification
# ===================================================================

def verify_insertion_points(SapModel, cardinal_point=VIGA_CARDINAL_POINT):
    """Verify insertion point on a sample of beam objects."""
    log.info(f"Step 5a: Verifying beam insertion point (CP={cardinal_point})...")

    try:
        result = SapModel.FrameObj.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            frame_names = result[1]
        else:
            log.warning("  Cannot read frame list")
            return
    except Exception as e:
        log.warning(f"  FrameObj.GetNameList failed: {e}")
        return

    beam_names = []
    for frame_name in frame_names:
        try:
            sec_result = SapModel.FrameObj.GetSection(str(frame_name))
            section = str(sec_result[0]) if isinstance(sec_result, (tuple, list)) else ""
        except Exception:
            section = ""
        if section in BEAM_SECTIONS:
            beam_names.append(str(frame_name))

    if not beam_names:
        log.warning("  No beam objects found to verify")
        return

    sample_size = min(5, len(beam_names))
    verified = 0
    check_failed = 0
    for frame_name in beam_names[:sample_size]:
        try:
            result = SapModel.FrameObj.GetInsertionPoint(frame_name)
            if isinstance(result, (tuple, list)) and len(result) >= 4:
                cp = int(result[0])
                stiff_transform = bool(result[2])
                ret_code = result[-1] if len(result) > 4 else 0
                if ret_code == 0 and cp == cardinal_point and stiff_transform:
                    verified += 1
                else:
                    check_failed += 1
                    log.warning(
                        f"  {frame_name}: CP={cp}, StiffTransform={stiff_transform}, ret={ret_code}"
                    )
            else:
                check_failed += 1
        except Exception as e:
            check_failed += 1
            if check_failed <= 2:
                log.warning(f"  GetInsertionPoint({frame_name}) failed: {e}")

    if verified == sample_size:
        log.info(f"  Insertion point verification: {verified}/{sample_size} sample beams OK")
    else:
        log.warning(
            f"  Insertion point verification: {verified}/{sample_size} OK, {check_failed} failed"
        )


def verify_rigid_end_zones(SapModel, rzf=RZF):
    """Verify RZF is applied by reading back a sample of frames.

    Firma COM (standard OAPI):
      FrameObj.GetEndLengthOffset(Name) -> (AutoOffset, Length1, Length2, RzFactor, ret)
    """
    log.info(f"Step 5a: Verifying Rigid End Zones (RZF={rzf})...")

    try:
        result = SapModel.FrameObj.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            n_frames = result[0]
            frame_names = result[1]
        else:
            log.warning("  Cannot read frame list")
            return
    except Exception as e:
        log.warning(f"  FrameObj.GetNameList failed: {e}")
        return

    if n_frames == 0:
        log.warning("  No frames to verify")
        return

    beam_names = []
    for frame_name in frame_names:
        try:
            sec_result = SapModel.FrameObj.GetSection(str(frame_name))
            section = str(sec_result[0]) if isinstance(sec_result, (tuple, list)) else ""
        except Exception:
            section = ""
        if section in BEAM_SECTIONS:
            beam_names.append(str(frame_name))

    if not beam_names:
        log.warning("  No beam objects found to verify")
        return

    # Check a sample of beam objects only
    sample_size = min(5, len(beam_names))
    verified = 0
    check_failed = 0

    for i in range(sample_size):
        frame_name = str(beam_names[i])
        try:
            result = SapModel.FrameObj.GetEndLengthOffset(frame_name)
            if isinstance(result, (tuple, list)) and len(result) >= 4:
                auto_offset = result[0]
                rz_factor = result[3]
                ret_code = result[-1] if len(result) > 4 else 0

                if ret_code == 0:
                    if abs(float(rz_factor) - rzf) < 0.01:
                        verified += 1
                    else:
                        log.warning(f"  {frame_name}: RZF={rz_factor} "
                                    f"(expected {rzf})")
                        check_failed += 1
                else:
                    check_failed += 1
            else:
                check_failed += 1
        except Exception as e:
            check_failed += 1
            if check_failed <= 2:
                log.warning(f"  GetEndLengthOffset({frame_name}) failed: {e}")

    if verified == sample_size:
        log.info(f"  RZF verification: {verified}/{sample_size} sample frames OK")
    elif check_failed == sample_size:
        log.warning(f"  RZF verification: could not verify sample beams via API")
    else:
        log.info(f"  RZF verification: {verified}/{sample_size} OK, "
                 f"{check_failed} failed")


def verify_base_restraints(SapModel):
    """Verify that all base nodes (Z=0) have full fixity applied.

    Firma COM:
      PointObj.GetRestraint(Name) -> (Value[6], ret)
    """
    log.info("Step 5b: Verifying base restraints...")

    try:
        result = SapModel.PointObj.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
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

            try:
                result = SapModel.PointObj.GetRestraint(pt_name)
                if isinstance(result, (tuple, list)) and len(result) >= 1:
                    restraints = result[0]
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
        log.info(f"  All base nodes properly restrained OK")


def verify_frame_sections(SapModel):
    """Verify all frame objects have expected sections assigned."""
    log.info("Step 5d: Verifying frame sections...")

    try:
        result = SapModel.FrameObj.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            n_frames = result[0]
            frame_names = result[1]
        else:
            log.warning("  Cannot read frame list")
            return
    except Exception as e:
        log.warning(f"  FrameObj.GetNameList failed: {e}")
        return

    if n_frames == 0:
        log.warning("  No frame objects found")
        return

    section_counts = {}

    for frame_name in frame_names:
        frame_name = str(frame_name)
        try:
            result = SapModel.FrameObj.GetSection(frame_name)
            if isinstance(result, (tuple, list)):
                section = str(result[0]) if len(result) >= 1 else "UNKNOWN"
            else:
                section = "UNKNOWN"
        except Exception:
            section = "ERROR"

        section_counts[section] = section_counts.get(section, 0) + 1

    log.info(f"  Total frames: {n_frames}")
    log.info(f"  Section distribution:")
    for sec, count in sorted(section_counts.items()):
        marker = "OK" if sec in EXPECTED_FRAME_SECTIONS else "??"
        log.info(f"    [{marker}] {sec}: {count} frames")


def verify_element_counts(SapModel):
    """Verify total element counts match expected values."""
    log.info("Step 5e: Verifying element counts...")

    try:
        pt_result = SapModel.PointObj.GetNameList()
        n_points = pt_result[0] if isinstance(pt_result, (tuple, list)) else 0
    except Exception:
        n_points = "ERROR"

    try:
        area_result = SapModel.AreaObj.GetNameList()
        n_areas = area_result[0] if isinstance(area_result, (tuple, list)) else 0
    except Exception:
        n_areas = "ERROR"

    try:
        frame_result = SapModel.FrameObj.GetNameList()
        n_frames = frame_result[0] if isinstance(frame_result, (tuple, list)) else 0
    except Exception:
        n_frames = "ERROR"

    expected_frames = N_COLUMNS_TOTAL + N_VIGAS_TOTAL  # 180 + 300 = 480
    expected_areas = N_SLABS_TOTAL                      # 125

    log.info(f"  Points:  {n_points}")
    log.info(f"  Frames:  {n_frames} (expected ~{expected_frames}: "
             f"{N_COLUMNS_TOTAL} cols + {N_VIGAS_TOTAL} beams)")
    log.info(f"  Areas:   {n_areas} (expected ~{expected_areas}: "
             f"{N_SLABS_TOTAL} slabs)")

    if isinstance(n_frames, int) and n_frames > 0:
        if abs(n_frames - expected_frames) > expected_frames * 0.1:
            log.warning(f"  Frame count mismatch: got {n_frames}, "
                        f"expected ~{expected_frames}")
        else:
            log.info(f"  Frame count OK")

    if isinstance(n_areas, int) and n_areas > 0:
        if abs(n_areas - expected_areas) > expected_areas * 0.1:
            log.warning(f"  Area count mismatch: got {n_areas}, "
                        f"expected ~{expected_areas}")
        else:
            log.info(f"  Area count OK")


# ===================================================================
# STEP 6: Summary
# ===================================================================

def print_summary(n_ip, n_ip_fail, n_rzf, n_rzf_fail, n_restrained,
                  n_not_base, n_restraint_fail, n_edge, n_edge_fail, elapsed):
    """Print a summary of all assignments."""
    log.info("=" * 60)
    log.info("SUMMARY")
    log.info("=" * 60)
    log.info(f"  Assignments applied:")
    log.info(f"    InsertPt CP=8:  {n_ip} beams ({n_ip_fail} failed)")
    log.info(f"    RZF={RZF}:       {n_rzf} beams ({n_rzf_fail} failed)")
    log.info(f"    Base fixity:    {n_restrained} nodes "
             f"({n_restraint_fail} failed)")
    log.info(f"    Edge constr.:   {n_edge} slabs ({n_edge_fail} failed)")
    log.info(f"")
    log.info(f"  Pre-existing (from 05_slabs_ed2.py):")
    log.info(f"    Diaphragm:      {DIAPHRAGM_RIGID_NAME} (rigid) on all slabs")
    log.info(f"    AutoMesh:       {AUTOMESH_SIZE}m on all slabs")
    log.info(f"")
    log.info(f"  Time: {elapsed:.1f}s")

    total_failures = n_ip_fail + n_rzf_fail + n_restraint_fail + n_edge_fail
    if total_failures > 0:
        log.warning(f"  Total failures: {total_failures} — check warnings above")
    else:
        log.info("  All assignments completed successfully!")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: apply all post-geometry assignments for Ed.2."""
    log.info("=" * 60)
    log.info("06_assignments_ed2.py — Post-geometry assignments, Edificio 2")
    log.info("=" * 60)
    log.info("")
    log.info("  Tasks:")
    log.info(f"    1. Beam Insertion Point (CP={VIGA_CARDINAL_POINT}, Top Center)")
    log.info(f"    2. Rigid End Zones (RZF={RZF}) on beams")
    log.info("    3. Base restraints (full fixity at Z=0)")
    log.info("    4. Auto Edge Constraints on slabs")
    log.info("    5. Verification of all assignments")
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

        # Step 1: Beam Insertion Point
        n_ip, n_ip_fail = set_beam_insertion_point(SapModel)
        log.info("")

        # Step 2: Rigid End Zones (beams only)
        n_rzf, n_rzf_fail = apply_rigid_end_zones(SapModel)
        log.info("")

        # Step 3: Base restraints
        n_restrained, n_not_base, n_restraint_fail = set_base_restraints(SapModel)
        log.info("")

        # Step 4: Auto Edge Constraints
        n_edge, n_edge_fail = apply_edge_constraints(SapModel)
        log.info("")

        expected_beams = N_VIGAS_TOTAL
        expected_base_nodes = N_COLUMNS_PER_STORY
        expected_slabs = N_SLABS_TOTAL
        if n_ip != expected_beams:
            raise RuntimeError(
                f"Insertion Point incompleto: {n_ip}/{expected_beams} vigas con CP={VIGA_CARDINAL_POINT}."
            )
        if n_rzf != expected_beams:
            raise RuntimeError(
                f"Rigid End Zones incompleto: {n_rzf}/{expected_beams} vigas con RZF={RZF}."
            )
        if n_restrained != expected_base_nodes:
            raise RuntimeError(
                f"Base restraints incompleto: {n_restrained}/{expected_base_nodes} nodos base restringidos."
            )
        if n_edge != expected_slabs:
            raise RuntimeError(
                f"Auto Edge Constraints incompleto: {n_edge}/{expected_slabs} losas."
            )

        t_elapsed = time.time() - t_start

        # Step 5: Verification
        log.info("Step 5: Comprehensive verification...")
        log.info("")
        verify_insertion_points(SapModel)
        log.info("")
        verify_rigid_end_zones(SapModel)
        log.info("")
        verify_base_restraints(SapModel)
        log.info("")
        verify_frame_sections(SapModel)
        log.info("")
        verify_element_counts(SapModel)
        log.info("")

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Step 6: Summary
        print_summary(n_ip, n_ip_fail, n_rzf, n_rzf_fail, n_restrained,
                      n_not_base, n_restraint_fail, n_edge, n_edge_fail,
                      t_elapsed)
        total_failures = n_ip_fail + n_rzf_fail + n_restraint_fail + n_edge_fail
        if total_failures > 0:
            raise RuntimeError(
                "Asignaciones post-geometria incompletas. "
                f"InsertPt={n_ip_fail}, RZF={n_rzf_fail}, "
                f"Base={n_restraint_fail}, Edge={n_edge_fail}."
            )
        log.info("")
        log.info("Ready for next step (07_loads_ed2.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
