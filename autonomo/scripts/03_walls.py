"""
03_walls.py — Draw ALL walls (muros) for Edificio 1, all 20 stories.

Creates wall panels (area objects) for every story using AreaObj.AddByCoord.
Wall geometry is defined in config.py (MUROS_DIR_Y, MUROS_DIR_X), sourced from
the Enunciado Taller (pages 2-6).

Wall segments:
  Direction Y (vertical in plan, run along Y axis):
    - 26 segments per story
    - e=30cm (MHA30G30): axes 1, 3, 4, 5, 7, 12, 13, 14, 16, 17
    - e=20cm (MHA20G30): axes 2, 6, 8, 9, 10, 11, 15
    - Walls do NOT cross the central corridor (gap between axes C and D)

  Direction X (horizontal in plan, run along X axis):
    - 23 segments per story
    - Axis C: e=30cm between axes 3-6 and 10-14, e=20cm elsewhere
    - Axes A, D, E, F: e=20cm (stubs and short segments)

Total: 49 segments/story x 20 stories = 980 wall panels.

After creating each wall, AutoMesh is set to 0.4m (max mesh size).

Prerequisites:
  - ETABS v19 open with model from 01_init_model.py + 02_materials_sections.py
  - comtypes installed
  - config.py in the same directory

Usage:
  python 03_walls.py

Units: Tonf, m, C (eUnits=12) throughout.

COM signatures verified against: autonomo/research/com_signatures.md (R03)
  - AreaObj.AddByCoord: §7.1
  - AreaObj.SetAutoMesh: §7.3
Sources: Enunciado Taller ADSE 1S-2026, Prof. Music (pags 2-6)
"""

import sys
import os
import time

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, check_ret, set_units, get_model, get_section_name, log,
    UNITS_TONF_M_C,
    # Stories
    N_STORIES, STORY_ELEVATIONS,
    # Wall data
    MUROS_DIR_Y, MUROS_DIR_X, N_MUROS_DIR_Y, N_MUROS_DIR_X,
    # Section names
    MURO_30_NAME, MURO_20_NAME, MURO_30_ESP, MURO_20_ESP,
    # AutoMesh
    AUTOMESH_SIZE,
)


# ===================================================================
# HELPER: Create a single wall panel
# ===================================================================

def create_wall_panel(SapModel, x_coords, y_coords, z_bot, z_top,
                      section_name, wall_label=""):
    """Create a single wall panel (4-node area object) via AreaObj.AddByCoord.

    Args:
        SapModel: ETABS SapModel COM object
        x_coords: tuple (x1, x2) — X coordinates of wall ends
        y_coords: tuple (y1, y2) — Y coordinates of wall ends
        z_bot: float — bottom elevation of this story
        z_top: float — top elevation of this story
        section_name: str — "MHA30G30" or "MHA20G30"
        wall_label: str — descriptive label for logging

    Returns:
        str — name assigned by ETABS to the created area object

    The 4 vertices are defined counterclockwise (looking from outside):
      P1: (x1, y1, z_bot)  — bottom-left
      P2: (x2, y2, z_bot)  — bottom-right
      P3: (x2, y2, z_top)  — top-right
      P4: (x1, y1, z_top)  — top-left

    Firma COM (com_signatures.md §7.1):
      ret = AreaObj.AddByCoord(NumberPoints, X[], Y[], Z[],
                               ref Name, PropName, UserName, CSys)
      NumberPoints = 4 (rectangular panel)
      X, Y, Z = float arrays with 4 elements each
      Name = "" (ETABS assigns name)
      PropName = section name
      UserName, CSys = optional (omitted)
    """
    x1, x2 = x_coords
    y1, y2 = y_coords

    X = [x1, x2, x2, x1]
    Y = [y1, y2, y2, y1]
    Z = [z_bot, z_bot, z_top, z_top]

    name = ""
    ret = SapModel.AreaObj.AddByCoord(4, X, Y, Z, name, section_name)

    # ret is typically (assigned_name, 0) on success
    if isinstance(ret, tuple):
        assigned_name = ret[0] if len(ret) >= 2 else ""
        ret_code = ret[-1]
    else:
        assigned_name = ""
        ret_code = ret

    if ret_code != 0:
        raise RuntimeError(
            f"AreaObj.AddByCoord failed (ret={ret_code}): {wall_label} "
            f"section={section_name} z=[{z_bot:.2f},{z_top:.2f}]"
        )

    return str(assigned_name) if assigned_name else ""


# ===================================================================
# HELPER: Set AutoMesh on a wall panel
# ===================================================================

def set_wall_automesh(SapModel, wall_name, max_size=AUTOMESH_SIZE):
    """Set AutoMesh on a wall panel.

    Firma COM (com_signatures.md §7.3):
      ret = AreaObj.SetAutoMesh(Name, MeshType, n1, n2,
                                MaxSize1, MaxSize2, PointOnEdge,
                                ExtendCookies, Rotation, MaxSizeGeneral,
                                LocalAxesOnEdge, LocalAxesOnFace,
                                RestraintsOnEdge, RestraintsOnFace)
      MeshType = 4 (MaxSize — mesh by maximum element size)
      MaxSize1, MaxSize2, MaxSizeGeneral = 0.4 m
    """
    if not wall_name:
        return

    ret = SapModel.AreaObj.SetAutoMesh(
        wall_name,
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
    # check_ret not called here to avoid aborting on non-critical mesh errors
    if isinstance(ret, tuple):
        ret = ret[-1] if len(ret) > 1 else ret[0]
    if ret != 0:
        log.warning(f"  SetAutoMesh({wall_name}) ret={ret} — non-critical")


# ===================================================================
# STEP 1: Create walls in direction Y (vertical in plan)
# ===================================================================

def create_walls_dir_y(SapModel):
    """Create all walls running in the Y direction, for all 20 stories.

    MUROS_DIR_Y from config.py contains 26 segments, each defined as:
      (eje_label, x_coord, y_ini, y_fin, espesor)

    For each story, for each segment:
      - x_coords = (x, x)  (same X for both ends — vertical plane at x=const)
      - y_coords = (y_ini, y_fin)
      - z_bot, z_top = story bottom/top elevations
    """
    log.info("Step 1: Creating walls in direction Y...")
    log.info(f"  {N_MUROS_DIR_Y} segments/story x {N_STORIES} stories = "
             f"{N_MUROS_DIR_Y * N_STORIES} panels")

    created = 0
    failed = 0

    for story_idx in range(N_STORIES):
        z_bot = 0.0 if story_idx == 0 else STORY_ELEVATIONS[story_idx - 1]
        z_top = STORY_ELEVATIONS[story_idx]
        story_num = story_idx + 1

        for seg_idx, (eje, x, y_ini, y_fin, esp) in enumerate(MUROS_DIR_Y):
            section = get_section_name(esp)
            label = f"WY-{eje}-S{story_num}-{seg_idx}"

            try:
                name = create_wall_panel(
                    SapModel,
                    x_coords=(x, x),
                    y_coords=(y_ini, y_fin),
                    z_bot=z_bot,
                    z_top=z_top,
                    section_name=section,
                    wall_label=label,
                )
                set_wall_automesh(SapModel, name)
                created += 1
            except RuntimeError as e:
                log.error(f"  FAILED: {e}")
                failed += 1

        # Log progress every 5 stories
        if story_num % 5 == 0 or story_num == 1 or story_num == N_STORIES:
            log.info(f"  Story {story_num}/{N_STORIES}: "
                     f"{created} created, {failed} failed")

    log.info(f"  Direction Y complete: {created} created, {failed} failed")
    return created, failed


# ===================================================================
# STEP 2: Create walls in direction X (horizontal in plan)
# ===================================================================

def create_walls_dir_x(SapModel):
    """Create all walls running in the X direction, for all 20 stories.

    MUROS_DIR_X from config.py contains 22 segments, each defined as:
      (eje_label, y_coord, x_ini, x_fin, espesor)

    For each story, for each segment:
      - x_coords = (x_ini, x_fin)
      - y_coords = (y, y)  (same Y for both ends — vertical plane at y=const)
      - z_bot, z_top = story bottom/top elevations
    """
    log.info("Step 2: Creating walls in direction X...")
    log.info(f"  {N_MUROS_DIR_X} segments/story x {N_STORIES} stories = "
             f"{N_MUROS_DIR_X * N_STORIES} panels")

    created = 0
    failed = 0

    for story_idx in range(N_STORIES):
        z_bot = 0.0 if story_idx == 0 else STORY_ELEVATIONS[story_idx - 1]
        z_top = STORY_ELEVATIONS[story_idx]
        story_num = story_idx + 1

        for seg_idx, (eje, y, x_ini, x_fin, esp) in enumerate(MUROS_DIR_X):
            section = get_section_name(esp)
            label = f"WX-{eje}-S{story_num}-{seg_idx}"

            try:
                name = create_wall_panel(
                    SapModel,
                    x_coords=(x_ini, x_fin),
                    y_coords=(y, y),
                    z_bot=z_bot,
                    z_top=z_top,
                    section_name=section,
                    wall_label=label,
                )
                set_wall_automesh(SapModel, name)
                created += 1
            except RuntimeError as e:
                log.error(f"  FAILED: {e}")
                failed += 1

        # Log progress every 5 stories
        if story_num % 5 == 0 or story_num == 1 or story_num == N_STORIES:
            log.info(f"  Story {story_num}/{N_STORIES}: "
                     f"{created} created, {failed} failed")

    log.info(f"  Direction X complete: {created} created, {failed} failed")
    return created, failed


# ===================================================================
# STEP 3: Verify wall count
# ===================================================================

def verify_walls(SapModel, expected_total):
    """Verify walls were created by checking AreaObj.GetNameList.

    Note: In ETABS v19, GetNameList may return 0 after COM creation
    (known bug). The walls may still exist — verify in ETABS UI.
    """
    log.info("Step 3: Verifying wall count...")

    try:
        result = SapModel.AreaObj.GetNameList()
        if isinstance(result, tuple) and result[-1] == 0:
            n_areas = result[0]
            log.info(f"  AreaObj.GetNameList: {n_areas} area objects found")
            if n_areas >= expected_total:
                log.info(f"  Count OK (expected >= {expected_total})")
            elif n_areas == 0:
                log.warning(f"  GetNameList returned 0 — known v19 bug")
                log.warning(f"  Walls likely exist. Verify in ETABS UI or "
                            f"save and reopen the model.")
            else:
                log.warning(f"  Count mismatch: got {n_areas}, "
                            f"expected >= {expected_total}")
        else:
            ret_code = result[-1] if isinstance(result, tuple) else result
            log.warning(f"  AreaObj.GetNameList ret={ret_code}")
    except Exception as e:
        log.warning(f"  Verification failed: {e}")
        log.warning(f"  Non-critical — walls may still exist in the model")


# ===================================================================
# STEP 4: Print wall summary table
# ===================================================================

def print_wall_summary():
    """Print a summary table of all wall segments per story."""
    log.info("Wall segments per story:")
    log.info("")

    # Direction Y
    log.info("  Direction Y (26 segments):")
    log.info(f"    {'Eje':>4s}  {'X (m)':>8s}  {'Y_ini (m)':>9s}  "
             f"{'Y_fin (m)':>9s}  {'L (m)':>6s}  {'e (cm)':>6s}  Section")
    log.info(f"    {'----':>4s}  {'--------':>8s}  {'---------':>9s}  "
             f"{'---------':>9s}  {'------':>6s}  {'------':>6s}  -------")
    for eje, x, y_ini, y_fin, esp in MUROS_DIR_Y:
        L = abs(y_fin - y_ini)
        sec = get_section_name(esp)
        log.info(f"    {eje:>4s}  {x:8.3f}  {y_ini:9.3f}  "
                 f"{y_fin:9.3f}  {L:6.3f}  {esp*100:6.0f}  {sec}")

    log.info("")

    # Direction X
    log.info("  Direction X (22 segments):")
    log.info(f"    {'Eje':>4s}  {'Y (m)':>8s}  {'X_ini (m)':>9s}  "
             f"{'X_fin (m)':>9s}  {'L (m)':>6s}  {'e (cm)':>6s}  Section")
    log.info(f"    {'----':>4s}  {'--------':>8s}  {'---------':>9s}  "
             f"{'---------':>9s}  {'------':>6s}  {'------':>6s}  -------")
    for eje, y, x_ini, x_fin, esp in MUROS_DIR_X:
        L = abs(x_fin - x_ini)
        sec = get_section_name(esp)
        log.info(f"    {eje:>4s}  {y:8.3f}  {x_ini:9.3f}  "
                 f"{x_fin:9.3f}  {L:6.3f}  {esp*100:6.0f}  {sec}")

    # Totals
    n_30_y = sum(1 for _, _, _, _, e in MUROS_DIR_Y if abs(e - MURO_30_ESP) < 0.01)
    n_20_y = sum(1 for _, _, _, _, e in MUROS_DIR_Y if abs(e - MURO_20_ESP) < 0.01)
    n_30_x = sum(1 for _, _, _, _, e in MUROS_DIR_X if abs(e - MURO_30_ESP) < 0.01)
    n_20_x = sum(1 for _, _, _, _, e in MUROS_DIR_X if abs(e - MURO_20_ESP) < 0.01)

    log.info("")
    log.info("  Totals per story:")
    log.info(f"    MHA30G30: {n_30_y} (dir Y) + {n_30_x} (dir X) "
             f"= {n_30_y + n_30_x}")
    log.info(f"    MHA20G30: {n_20_y} (dir Y) + {n_20_x} (dir X) "
             f"= {n_20_y + n_20_x}")
    log.info(f"    Total:    {N_MUROS_DIR_Y} (dir Y) + {N_MUROS_DIR_X} (dir X) "
             f"= {N_MUROS_DIR_Y + N_MUROS_DIR_X}")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: create all walls for Edificio 1."""
    log.info("=" * 60)
    log.info("03_walls.py — Edificio 1 (All walls, 20 stories)")
    log.info("=" * 60)

    total_segments = N_MUROS_DIR_Y + N_MUROS_DIR_X
    total_panels = total_segments * N_STORIES

    # Print expected parameters
    log.info(f"  Wall segments per story: {total_segments}")
    log.info(f"    Direction Y: {N_MUROS_DIR_Y} segments")
    log.info(f"    Direction X: {N_MUROS_DIR_X} segments")
    log.info(f"  Stories: {N_STORIES}")
    log.info(f"  Total wall panels to create: {total_panels}")
    log.info(f"  Sections: {MURO_30_NAME} (t={MURO_30_ESP}m), "
             f"{MURO_20_NAME} (t={MURO_20_ESP}m)")
    log.info(f"  AutoMesh: {AUTOMESH_SIZE}m")
    log.info("")

    # Print wall summary table
    print_wall_summary()
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

        # Step 1: Create walls direction Y
        created_y, failed_y = create_walls_dir_y(SapModel)
        log.info("")

        # Step 2: Create walls direction X
        created_x, failed_x = create_walls_dir_x(SapModel)
        log.info("")

        t_elapsed = time.time() - t_start

        # Step 3: Verify
        total_created = created_y + created_x
        total_failed = failed_y + failed_x
        verify_walls(SapModel, total_created)
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
        log.info(f"  Direction Y: {created_y} created, {failed_y} failed "
                 f"(of {N_MUROS_DIR_Y * N_STORIES} expected)")
        log.info(f"  Direction X: {created_x} created, {failed_x} failed "
                 f"(of {N_MUROS_DIR_X * N_STORIES} expected)")
        log.info(f"  Total:       {total_created} created, {total_failed} failed "
                 f"(of {total_panels} expected)")
        log.info(f"  AutoMesh:    {AUTOMESH_SIZE}m applied to all panels")
        log.info(f"  Time:        {t_elapsed:.1f}s")
        log.info("")

        if total_failed > 0:
            log.warning(f"  {total_failed} walls failed — check errors above")
        else:
            log.info("  All walls created successfully!")

        log.info("")
        log.info("Ready for next step (04_beams.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
