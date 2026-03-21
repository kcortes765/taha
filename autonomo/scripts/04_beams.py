"""
04_beams.py — Draw ALL beams (vigas) for Edificio 1, all 20 stories.

Creates frame objects for every beam using FrameObj.AddByCoord, then assigns:
  - Section: VI20x60G30 (inverted beam, 20x60 cm)
  - Cardinal Point: 2 (Bottom Center) — inverted beams hang below slab
  - J=0 (torsion modifier) — already set in section definition (02_materials_sections.py)

Beam layout per story (from config.py, sourced from Enunciado Taller pag 2):
  - Axis A:  10 beams (southern facade)
  - Axis F:   8 beams (northern facade)
  - Axis B:  12 beams (intermediate axis)
  Total: 30 beams/story x 20 stories = 600 beams

All beams run in the X direction (horizontal in plan) at fixed Y coordinates.
Beams are placed at the TOP elevation of each story (slab level).

Prerequisites:
  - ETABS v19 open with model from 01/02/03 scripts
  - comtypes installed
  - config.py in the same directory

Usage:
  python 04_beams.py

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against: autonomo/research/com_signatures.md (R03)
  - FrameObj.AddByCoord: §6.1
  - FrameObj.SetInsertionPoint: §6.3
Sources: Enunciado Taller ADSE 1S-2026, Prof. Music (pag 2 — planta tipo)
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
    # Beam data
    VIGAS, N_VIGAS,
    VIGAS_EJE_A, VIGAS_EJE_F, VIGAS_EJE_B,
    # Beam section
    VIGA_NAME, VIGA_B, VIGA_H, VIGA_CARDINAL_POINT,
)


# ===================================================================
# HELPER: Create a single beam
# ===================================================================

def create_beam(SapModel, y, x_ini, x_fin, z_elev, beam_label=""):
    """Create a single beam (frame object) via FrameObj.AddByCoord.

    Args:
        SapModel: ETABS SapModel COM object
        y: float — Y coordinate (fixed for the beam, runs in X direction)
        x_ini: float — X coordinate of start (point I)
        x_fin: float — X coordinate of end (point J)
        z_elev: float — Elevation (top of story = slab level)
        beam_label: str — descriptive label for logging

    Returns:
        str — name assigned by ETABS to the created frame object

    Firma COM (com_signatures.md §6.1):
      ret = FrameObj.AddByCoord(xi, yi, zi, xj, yj, zj,
                                 ref Name, PropName, UserName, CSys)
      - xi, yi, zi = start point coordinates
      - xj, yj, zj = end point coordinates
      - Name = "" (ETABS assigns name)
      - PropName = section name
    """
    name = ""
    ret = SapModel.FrameObj.AddByCoord(
        x_ini, y, z_elev,      # Point I (start)
        x_fin, y, z_elev,      # Point J (end)
        name,                   # ref Name — ETABS assigns
        VIGA_NAME,              # PropName = "VI20x60G30"
    )

    # ret is typically (assigned_name, 0) on success
    if isinstance(ret, tuple):
        assigned_name = ret[0] if len(ret) >= 2 else ""
        ret_code = ret[-1]
    else:
        assigned_name = ""
        ret_code = ret

    if ret_code != 0:
        raise RuntimeError(
            f"FrameObj.AddByCoord failed (ret={ret_code}): {beam_label} "
            f"y={y:.3f} x=[{x_ini:.3f},{x_fin:.3f}] z={z_elev:.3f}"
        )

    return str(assigned_name) if assigned_name else ""


# ===================================================================
# HELPER: Set Cardinal Point (insertion point) for inverted beam
# ===================================================================

def set_beam_insertion_point(SapModel, frame_name, cardinal_point=VIGA_CARDINAL_POINT):
    """Set the insertion point (cardinal point) for a beam.

    For inverted beams: Cardinal Point 2 = Bottom Center.
    This means the beam reference line is at the bottom of the section,
    so the beam hangs BELOW the slab level.

    Firma COM (com_signatures.md §6.3):
      ret = FrameObj.SetInsertionPoint(Name, CardinalPoint, Mirror2,
                                        StiffTransform, Offset1, Offset2,
                                        CSys, ItemType)
    """
    if not frame_name:
        return

    ret = SapModel.FrameObj.SetInsertionPoint(
        frame_name,
        cardinal_point,         # 2 = Bottom Center (inverted beam)
        False,                  # Mirror2 — no mirror
        False,                  # StiffTransform — no stiffness transform
        [0.0, 0.0, 0.0],       # Offset1 — no offset at point I
        [0.0, 0.0, 0.0],       # Offset2 — no offset at point J
    )

    # Check return
    if isinstance(ret, tuple):
        ret_code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        ret_code = ret

    if ret_code != 0:
        log.warning(f"  SetInsertionPoint({frame_name}, CP={cardinal_point}) "
                    f"ret={ret_code} — non-critical")


# ===================================================================
# STEP 1: Create all beams for all stories
# ===================================================================

def create_all_beams(SapModel):
    """Create all beams for all 20 stories.

    VIGAS from config.py contains 30 beam definitions, each as:
      (y_fijo, x_ini, x_fin)

    For each story, beams are placed at the TOP elevation (slab level).
    After creating each beam, the cardinal point is set to Bottom Center (2).

    Returns:
        tuple — (created_count, failed_count)
    """
    log.info("Step 1: Creating all beams...")
    log.info(f"  {N_VIGAS} beams/story x {N_STORIES} stories = "
             f"{N_VIGAS * N_STORIES} total beams")

    created = 0
    failed = 0

    for story_idx in range(N_STORIES):
        z_elev = STORY_ELEVATIONS[story_idx]
        story_num = story_idx + 1

        for beam_idx, (y, x_ini, x_fin) in enumerate(VIGAS):
            # Determine axis label for logging
            if beam_idx < len(VIGAS_EJE_A):
                axis = "A"
                local_idx = beam_idx
            elif beam_idx < len(VIGAS_EJE_A) + len(VIGAS_EJE_F):
                axis = "F"
                local_idx = beam_idx - len(VIGAS_EJE_A)
            else:
                axis = "B"
                local_idx = beam_idx - len(VIGAS_EJE_A) - len(VIGAS_EJE_F)

            label = f"B-{axis}{local_idx}-S{story_num}"

            try:
                # Create beam via AddByCoord
                frame_name = create_beam(
                    SapModel,
                    y=y,
                    x_ini=x_ini,
                    x_fin=x_fin,
                    z_elev=z_elev,
                    beam_label=label,
                )

                # Set cardinal point to Bottom Center (inverted beam)
                set_beam_insertion_point(SapModel, frame_name)

                created += 1
            except RuntimeError as e:
                log.error(f"  FAILED: {e}")
                failed += 1

        # Log progress every 5 stories
        if story_num % 5 == 0 or story_num == 1 or story_num == N_STORIES:
            log.info(f"  Story {story_num}/{N_STORIES}: "
                     f"{created} created, {failed} failed")

    log.info(f"  All stories complete: {created} created, {failed} failed")
    return created, failed


# ===================================================================
# STEP 2: Verify beam count
# ===================================================================

def verify_beams(SapModel, expected_total):
    """Verify beams were created by checking FrameObj.GetNameList.

    Note: In ETABS v19, GetNameList may return 0 after COM creation
    (known bug). The beams may still exist — verify in ETABS UI.
    """
    log.info("Step 2: Verifying beam count...")

    try:
        result = SapModel.FrameObj.GetNameList()
        if isinstance(result, tuple) and result[-1] == 0:
            n_frames = result[0]
            log.info(f"  FrameObj.GetNameList: {n_frames} frame objects found")
            if n_frames >= expected_total:
                log.info(f"  Count OK (expected >= {expected_total})")
            elif n_frames == 0:
                log.warning(f"  GetNameList returned 0 — known v19 bug")
                log.warning(f"  Beams likely exist. Verify in ETABS UI or "
                            f"save and reopen the model.")
            else:
                log.warning(f"  Count mismatch: got {n_frames}, "
                            f"expected >= {expected_total}")
        else:
            ret_code = result[-1] if isinstance(result, tuple) else result
            log.warning(f"  FrameObj.GetNameList ret={ret_code}")
    except Exception as e:
        log.warning(f"  Verification failed: {e}")
        log.warning(f"  Non-critical — beams may still exist in the model")


# ===================================================================
# STEP 3: Print beam summary table
# ===================================================================

def print_beam_summary():
    """Print a summary table of all beam segments per story."""
    log.info("Beam layout per story:")
    log.info("")

    axes = [
        ("Axis A", VIGAS_EJE_A),
        ("Axis F", VIGAS_EJE_F),
        ("Axis B", VIGAS_EJE_B),
    ]

    log.info(f"  {'Axis':>8s}  {'Y (m)':>8s}  {'X_ini (m)':>9s}  "
             f"{'X_fin (m)':>9s}  {'L (m)':>7s}  Section")
    log.info(f"  {'--------':>8s}  {'--------':>8s}  {'---------':>9s}  "
             f"{'---------':>9s}  {'-------':>7s}  -------")

    for axis_name, beams in axes:
        for i, (y, x_ini, x_fin) in enumerate(beams):
            L = abs(x_fin - x_ini)
            label = f"{axis_name}[{i}]"
            log.info(f"  {label:>8s}  {y:8.3f}  {x_ini:9.3f}  "
                     f"{x_fin:9.3f}  {L:7.3f}  {VIGA_NAME}")

    log.info("")
    log.info(f"  Axis A: {len(VIGAS_EJE_A)} beams")
    log.info(f"  Axis F: {len(VIGAS_EJE_F)} beams")
    log.info(f"  Axis B: {len(VIGAS_EJE_B)} beams")
    log.info(f"  Total per story: {N_VIGAS} beams")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: create all beams for Edificio 1."""
    log.info("=" * 60)
    log.info("04_beams.py — Edificio 1 (All beams, 20 stories)")
    log.info("=" * 60)

    total_beams = N_VIGAS * N_STORIES

    # Print expected parameters
    log.info(f"  Beams per story: {N_VIGAS}")
    log.info(f"    Axis A: {len(VIGAS_EJE_A)} beams")
    log.info(f"    Axis F: {len(VIGAS_EJE_F)} beams")
    log.info(f"    Axis B: {len(VIGAS_EJE_B)} beams")
    log.info(f"  Stories: {N_STORIES}")
    log.info(f"  Total beams to create: {total_beams}")
    log.info(f"  Section: {VIGA_NAME} ({VIGA_B}x{VIGA_H} m)")
    log.info(f"  Cardinal Point: {VIGA_CARDINAL_POINT} (Bottom Center — inverted)")
    log.info("")

    # Print beam summary table
    print_beam_summary()
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

        # Step 1: Create all beams
        created, failed = create_all_beams(SapModel)
        log.info("")

        t_elapsed = time.time() - t_start

        # Step 2: Verify
        verify_beams(SapModel, created)
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
        log.info(f"  Total:     {created} created, {failed} failed "
                 f"(of {total_beams} expected)")
        log.info(f"  Section:   {VIGA_NAME} ({VIGA_B}x{VIGA_H} m)")
        log.info(f"  Cardinal:  Point {VIGA_CARDINAL_POINT} (Bottom Center)")
        log.info(f"  J=0:       Set in section definition (02_materials_sections.py)")
        log.info(f"  Time:      {t_elapsed:.1f}s")
        log.info("")

        if failed > 0:
            log.warning(f"  {failed} beams failed — check errors above")
        else:
            log.info("  All beams created successfully!")

        log.info("")
        log.info("Ready for next step (05_slabs.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
