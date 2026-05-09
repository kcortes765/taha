"""
04_beams_ed2.py — Create 60 beams per story (30 dir X + 30 dir Y) for Edificio 2.

Creates frame objects for every beam using FrameObj.AddByCoord.
Section assignment by story:
  - P1-P2: V50x70G25 (0.50 x 0.70 m)
  - P3-P5: V45x70G25 (0.45 x 0.70 m)

Beam layout per story:
  - Direction X: 6 rows (axes A-F) x 5 spans = 30 beams
  - Direction Y: 6 columns (axes 1-6) x 5 spans = 30 beams
  - Total: 60 beams/story

Beams are placed at the TOP elevation of each story (slab level).
Beams are NORMAL (NOT inverted) — Cardinal Point = Top Center (8).
StiffTransform=True required because CP≠10 (offset from centroid to top face).

Total: 60 beams x 5 stories = 300 beams.

Prerequisites:
  - ETABS (v19/v21) must be open with model (run 01 + 02 + 03 first)
  - comtypes installed
  - config_ed2.py in the same directory

Usage:
  python 04_beams_ed2.py

Units: Tonf, m, C (eUnits=12) throughout.
COM signatures verified against: autonomo/research/com_signatures.md (R03)
Sources: Enunciado Taller ADSE 1S-2026, pags 8-9
"""

import sys
import os

# Ensure config_ed2.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
    N_STORIES, STORY_ELEVATIONS,
    VIGAS_DIR_X, VIGAS_DIR_Y,
    N_VIGAS_X_PER_STORY, N_VIGAS_Y_PER_STORY,
    N_VIGAS_PER_STORY, N_VIGAS_TOTAL,
    get_viga_section,
    VIGA_CARDINAL_POINT, CP_CENTROID,
    GRID_X_NAMES, GRID_Y_NAMES,
)


# ===================================================================
# STEP 1: Create beams for all stories
# ===================================================================

def create_beams(SapModel):
    """Create 60 beams per story at every grid span.

    For each story, creates:
      - 30 X-direction beams (horizontal, along rows A-F)
      - 30 Y-direction beams (vertical, along columns 1-6)

    Beams are placed at z = story top elevation (slab level).

    FrameObj.AddByCoord signature (com_signatures.md section 5.1):
      ret = FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, Name, PropName)
      Returns: (FrameName, ret) -- ret=0 on success

    Beam naming convention:
      VX_S{story}_{idx:02d}  for X-direction beams
      VY_S{story}_{idx:02d}  for Y-direction beams

    Returns:
        int -- total number of beams successfully created
    """
    log.info("Step 1: Creating beams at all grid spans...")

    total_created = 0
    FO = SapModel.FrameObj

    for story_idx in range(1, N_STORIES + 1):
        viga_section = get_viga_section(story_idx)
        z_elev = STORY_ELEVATIONS[story_idx - 1]

        log.info(f"  Story {story_idx}: section={viga_section}, z={z_elev:.2f} m")

        story_count = 0

        # --- X-direction beams: 30 per story ---
        # VIGAS_DIR_X = [(y, x_ini, x_fin), ...] — 30 items
        for beam_idx, (y, x_ini, x_fin) in enumerate(VIGAS_DIR_X, start=1):
            user_name = f"VX_S{story_idx}_{beam_idx:02d}"

            result = FO.AddByCoord(
                x_ini, y, z_elev,     # Point I (start)
                x_fin, y, z_elev,     # Point J (end)
                "",                    # Name (ETABS assigns)
                viga_section,          # PropName
                user_name,             # UserName
            )

            if isinstance(result, (tuple, list)):
                ret_code = result[-1]
            else:
                ret_code = result

            if ret_code != 0:
                log.error(f"    FAILED: {user_name} at y={y:.1f} "
                          f"x=[{x_ini:.1f},{x_fin:.1f}] ret={ret_code}")
            else:
                story_count += 1

        # --- Y-direction beams: 30 per story ---
        # VIGAS_DIR_Y = [(x, y_ini, y_fin), ...] — 30 items
        for beam_idx, (x, y_ini, y_fin) in enumerate(VIGAS_DIR_Y, start=1):
            user_name = f"VY_S{story_idx}_{beam_idx:02d}"

            result = FO.AddByCoord(
                x, y_ini, z_elev,     # Point I (start)
                x, y_fin, z_elev,     # Point J (end)
                "",                    # Name (ETABS assigns)
                viga_section,          # PropName
                user_name,             # UserName
            )

            if isinstance(result, (tuple, list)):
                ret_code = result[-1]
            else:
                ret_code = result

            if ret_code != 0:
                log.error(f"    FAILED: {user_name} at x={x:.1f} "
                          f"y=[{y_ini:.1f},{y_fin:.1f}] ret={ret_code}")
            else:
                story_count += 1

        total_created += story_count
        log.info(f"    Created {story_count}/{N_VIGAS_PER_STORY} beams "
                 f"({N_VIGAS_X_PER_STORY} X + {N_VIGAS_Y_PER_STORY} Y)")

    log.info(f"  Total beams created: {total_created}/{N_VIGAS_TOTAL}")
    return total_created


# ===================================================================
# STEP 2: Verify beams with FrameObj.GetNameList
# ===================================================================

def verify_beams(SapModel):
    """Verify beam count using FrameObj.GetNameList.

    Counts frames with names starting with VX_ or VY_ (our beams).
    Also reports total frame count (includes columns C_S*).

    FrameObj.GetNameList signature (com_signatures.md section 5.2):
      result = FrameObj.GetNameList()
      Returns: (NumberNames, MyName[], ret)
    """
    log.info("Step 2: Verifying beams with FrameObj.GetNameList...")

    FO = SapModel.FrameObj
    try:
        result = FO.GetNameList()
        if isinstance(result, (tuple, list)) and result[-1] == 0:
            n_frames = result[0]
            names = list(result[1]) if result[1] else []

            # Count beams by prefix
            vx_names = [n for n in names if n.startswith("VX_")]
            vy_names = [n for n in names if n.startswith("VY_")]
            col_names = [n for n in names if n.startswith("C_S")]
            n_beams = len(vx_names) + len(vy_names)

            log.info(f"  Total frame objects: {n_frames}")
            log.info(f"  Column objects (C_S*): {len(col_names)}")
            log.info(f"  Beam objects X (VX_*): {len(vx_names)}")
            log.info(f"  Beam objects Y (VY_*): {len(vy_names)}")
            log.info(f"  Total beams: {n_beams}")
            log.info(f"  Expected beams: {N_VIGAS_TOTAL}")

            if n_beams >= N_VIGAS_TOTAL:
                log.info(f"  VERIFICATION OK: {n_beams} beams found")
            else:
                log.warning(f"  MISMATCH: expected {N_VIGAS_TOTAL}, "
                            f"found {n_beams} beam objects")
                # Show per story
                for s in range(1, N_STORIES + 1):
                    s_vx = [n for n in vx_names if n.startswith(f"VX_S{s}_")]
                    s_vy = [n for n in vy_names if n.startswith(f"VY_S{s}_")]
                    log.info(f"    Story {s}: {len(s_vx)} X + {len(s_vy)} Y "
                             f"= {len(s_vx) + len(s_vy)} beams")

            return n_beams
        else:
            log.warning(f"  GetNameList returned non-zero")
            return 0
    except Exception as e:
        log.warning(f"  Verification failed: {e}")
        return 0


# ===================================================================
# STEP 3: Print summary of section assignments
# ===================================================================

def print_section_summary():
    """Print which beam section is assigned to each story."""
    log.info("  Beam section assignments:")
    for story_idx in range(1, N_STORIES + 1):
        viga_sec = get_viga_section(story_idx)
        log.info(f"    Story {story_idx}: {viga_sec}")
    log.info(f"  Cardinal Point: {VIGA_CARDINAL_POINT} "
             f"({'TopCenter' if VIGA_CARDINAL_POINT == 8 else 'Centroid' if VIGA_CARDINAL_POINT == CP_CENTROID else 'Other'})")
    log.info(f"  Beams are NORMAL (not inverted) — CP=8 TopCenter")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: create and verify 300 beams."""
    log.info("=" * 60)
    log.info("04_beams_ed2.py — Edificio 2 (60 beams/story x 5 stories)")
    log.info("=" * 60)

    log.info(f"  Beams per story: {N_VIGAS_PER_STORY} "
             f"({N_VIGAS_X_PER_STORY} X + {N_VIGAS_Y_PER_STORY} Y)")
    log.info(f"  Stories: {N_STORIES}")
    log.info(f"  Total beams: {N_VIGAS_TOTAL}")
    print_section_summary()
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

        # Step 1: Create beams
        n_created = create_beams(SapModel)
        log.info("")

        # Step 2: Verify
        n_verified = verify_beams(SapModel)
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
        log.info(f"  Beams created: {n_created}")
        log.info(f"  Beams verified: {n_verified}")
        log.info(f"  Expected: {N_VIGAS_TOTAL}")
        print_section_summary()
        log.info("")

        if n_created == N_VIGAS_TOTAL:
            log.info("All 300 beams created successfully.")
        else:
            log.warning(f"Created {n_created}/{N_VIGAS_TOTAL} — check errors above.")

        log.info("")
        log.info("Ready for next step (05_slabs_ed2.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
