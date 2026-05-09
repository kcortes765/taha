"""
03_columns_ed2.py — Create 36 columns per story (6x6 grid) for Edificio 2.

Creates columns at every grid intersection (6 X-lines x 6 Y-lines = 36 per story).
Section assignment by story:
  - P1-P2: C70x70G25 (0.70 x 0.70 m)
  - P3-P5: C65x65G25 (0.65 x 0.65 m)

Each column spans from floor-bottom to floor-top elevation:
  Story1: z=0.00 to z=3.50  (h=3.50m)
  Story2: z=3.50 to z=6.50  (h=3.00m)
  Story3: z=6.50 to z=9.50  (h=3.00m)
  Story4: z=9.50 to z=12.50 (h=3.00m)
  Story5: z=12.50 to z=15.50 (h=3.00m)

Total: 36 columns x 5 stories = 180 columns.

Uses FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, Name, PropName, UserName) to place each
column as a vertical frame element. Name="" lets ETABS auto-assign the internal name.

Prerequisites:
  - ETABS (v19/v21) must be open with model (run 01 + 02 first)
  - comtypes installed
  - config_ed2.py in the same directory

Usage:
  python 03_columns_ed2.py

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
    N_STORIES, STORY_HEIGHTS, STORY_ELEVATIONS,
    COLUMN_POSITIONS, N_COLUMNS_PER_STORY,
    SECTIONS_BY_STORY, get_col_section,
    GRID_X_NAMES, GRID_Y_NAMES,
    N_COLUMNS_TOTAL,
)


# ===================================================================
# STEP 1: Create columns for all stories
# ===================================================================

def create_columns(SapModel):
    """Create 36 columns per story at every grid intersection.

    For each story, iterates over all 36 (x, y) positions and creates
    a vertical frame element from z_bottom to z_top using the appropriate
    section for that story.

    FrameObj.AddByCoord signature (com_signatures.md §6.1):
      ret = FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, Name, PropName, UserName, CSys)
      - (x1,y1,z1): bottom point (punto I)
      - (x2,y2,z2): top point (punto J)
      - Name: ref str — output name assigned by ETABS (pass "")
      - PropName: section name (str)
      - UserName: user-assigned name (str, "" for auto)
      - CSys: coordinate system (str, default "Global")
      Returns: (Name, ret) — ret=0 on success

    BUG FIX: The 7th parameter is Name (ref output), NOT PropName.
    Without passing "" for Name, col_section was being interpreted as Name
    and user_name as PropName — so columns were created with no real section.

    Column naming convention: C_S{story}_{col_index}
      e.g., C_S1_01 through C_S1_36 for Story 1
    """
    log.info("Step 1: Creating columns at all grid intersections...")

    total_created = 0
    FO = SapModel.FrameObj

    for story_idx in range(1, N_STORIES + 1):
        col_section = get_col_section(story_idx)

        # Calculate z_bottom and z_top for this story
        if story_idx == 1:
            z_bottom = 0.0
        else:
            z_bottom = STORY_ELEVATIONS[story_idx - 2]
        z_top = STORY_ELEVATIONS[story_idx - 1]

        log.info(f"  Story {story_idx}: section={col_section}, "
                 f"z={z_bottom:.2f} to {z_top:.2f} m")

        story_count = 0
        for col_idx, (x, y) in enumerate(COLUMN_POSITIONS, start=1):
            user_name = f"C_S{story_idx}_{col_idx:02d}"

            # FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, Name, PropName, UserName)
            # Name (param 7) is a ref/output string — pass "" so ETABS assigns it
            # PropName (param 8) is the section — col_section
            # UserName (param 9) is the user label — user_name
            result = FO.AddByCoord(
                x, y, z_bottom,      # bottom point (I)
                x, y, z_top,         # top point (J)
                "",                   # Name — ref output, ETABS assigns
                col_section,          # PropName — section name
                user_name,            # UserName — user label
            )

            # Parse return: [FrameName, ret] or (FrameName, ret)
            if isinstance(result, (tuple, list)) and len(result) >= 2:
                ret_code = result[-1]
            else:
                ret_code = result

            if ret_code != 0:
                log.error(f"    FAILED: {user_name} at ({x:.1f}, {y:.1f}) "
                          f"ret={ret_code}")
            else:
                story_count += 1

        total_created += story_count
        log.info(f"    Created {story_count}/{N_COLUMNS_PER_STORY} columns")

    log.info(f"  Total columns created: {total_created}/{N_COLUMNS_TOTAL}")
    return total_created


# ===================================================================
# STEP 2: Verify columns with FrameObj.GetNameList
# ===================================================================

def verify_columns(SapModel):
    """Verify column count using FrameObj.GetNameList.

    FrameObj.GetNameList signature (com_signatures.md §5.2):
      result = FrameObj.GetNameList()
      Returns: (NumberNames, MyName[], ret)
    """
    log.info("Step 2: Verifying columns with FrameObj.GetNameList...")

    FO = SapModel.FrameObj
    try:
        result = FO.GetNameList()
        if isinstance(result, (tuple, list)) and result[-1] == 0:
            n_frames = result[0]
            names = list(result[1]) if result[1] else []

            # Count only our column names (C_S*)
            col_names = [n for n in names if n.startswith("C_S")]
            n_cols = len(col_names)

            log.info(f"  Total frame objects: {n_frames}")
            log.info(f"  Column objects (C_S*): {n_cols}")
            log.info(f"  Expected columns: {N_COLUMNS_TOTAL}")

            if n_cols >= N_COLUMNS_TOTAL:
                log.info(f"  VERIFICATION OK: {n_cols} columns found")
            else:
                log.warning(f"  MISMATCH: expected {N_COLUMNS_TOTAL}, "
                            f"found {n_cols} column objects")
                # Show what we have per story
                for s in range(1, N_STORIES + 1):
                    s_cols = [n for n in col_names if n.startswith(f"C_S{s}_")]
                    log.info(f"    Story {s}: {len(s_cols)} columns")

            return n_cols
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
    """Print which section is assigned to each story."""
    log.info("  Section assignments:")
    for story_idx in range(1, N_STORIES + 1):
        col_sec = get_col_section(story_idx)
        log.info(f"    Story {story_idx}: {col_sec}")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: create and verify 180 columns."""
    log.info("=" * 60)
    log.info("03_columns_ed2.py — Edificio 2 (36 columns/story x 5 stories)")
    log.info("=" * 60)

    log.info(f"  Grid intersections per story: {N_COLUMNS_PER_STORY}")
    log.info(f"  Stories: {N_STORIES}")
    log.info(f"  Total columns: {N_COLUMNS_TOTAL}")
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

        # Step 1: Create columns
        n_created = create_columns(SapModel)
        log.info("")

        # Step 2: Verify
        n_verified = verify_columns(SapModel)
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
        log.info(f"  Columns created: {n_created}")
        log.info(f"  Columns verified: {n_verified}")
        log.info(f"  Expected: {N_COLUMNS_TOTAL}")
        print_section_summary()
        log.info("")

        if n_created == N_COLUMNS_TOTAL:
            log.info("All 180 columns created successfully.")
        else:
            log.warning(f"Created {n_created}/{N_COLUMNS_TOTAL} — check errors above.")

        log.info("")
        log.info("Ready for next step (04_beams_ed2.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
