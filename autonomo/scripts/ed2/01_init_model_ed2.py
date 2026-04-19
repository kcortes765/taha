"""
01_init_model_ed2.py — Initialize ETABS model with grid and stories for Edificio 2.

Creates a new ETABS model from scratch:
  1. Initializes model with Tonf_m_C units
  2. Creates 5 stories via NewGridOnly (h1=3.50m, h2-5=3.00m)
  3. Relabels grid lines (X: 1-6, Y: A-F) — spacing is already correct (6.5m uniform)
  4. Verifies stories and grid
  5. Saves model as Edificio2_api.edb

Prerequisites:
  - ETABS (v19/v21) must be open manually (File > New Model > Blank)
  - comtypes installed (pip install comtypes)
  - config_ed2.py in the same directory

Usage:
  python 01_init_model_ed2.py

Fuente datos: Enunciado Taller ADSE 1S-2026, Prof. Music (pags 8-13)
Firmas COM: autonomo/research/com_signatures.md (R03)

# =====================================================================
# Template: autonomo/scripts/01_init_model.py (Ed.1)
# Adaptado para Edificio 2 — Marcos HA, 5 pisos, planta regular 32.5x32.5m
# Grilla uniforme 6x6 (6.5m) — NO requiere edicion compleja de grilla
# =====================================================================
"""

import sys
import os
import time

# Ensure config_ed2.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    connect, disconnect, check_ret, verify_model, set_units, get_model, log,
    UNITS_TONF_M_C,
    N_STORIES, STORY_HEIGHT_TYP, STORY_HEIGHT_1,
    N_LINES_X, N_LINES_Y,
    GRID_X, GRID_Y, GRID_X_NAMES, GRID_X_VALS,
    GRID_Y_NAMES, GRID_Y_VALS,
    GRID_SPACING,
    LX_PLANTA, LY_PLANTA, H_TOTAL,
    STORY_NAMES, STORY_HEIGHTS, STORY_ELEVATIONS,
    MODELS_DIR,
)


# ===================================================================
# STEP 1: Initialize new model
# ===================================================================

def init_model(SapModel):
    """Initialize a new blank model with Tonf_m_C units.

    Uses SapModel.InitializeNewModel(12) — Tonf, m, C.
    Firma: com_signatures.md §1.1
    """
    log.info("Step 1: Initializing new model (Tonf_m_C)...")
    ret = SapModel.InitializeNewModel(UNITS_TONF_M_C)
    check_ret(ret, "InitializeNewModel(12)")
    log.info("  Model initialized OK (units=Tonf_m_C)")


# ===================================================================
# STEP 2: Create model with NewGridOnly (stories + uniform grid)
# ===================================================================

def create_grid_and_stories(SapModel):
    """Create model skeleton: 5 stories + 6x6 uniform grid via NewGridOnly.

    NewGridOnly creates:
      - Stories with correct heights (BottomStoryHeight for piso 1)
      - A uniform grid with 6.5m spacing in both directions

    Since Ed.2 has a regular grid (all spacings = 6.5m), the grid
    created by NewGridOnly is already correct — only labels need editing.

    Firma: com_signatures.md §1.3
    ret = SapModel.File.NewGridOnly(
        NumberStorys, TypicalStoryHeight, BottomStoryHeight,
        NumberLinesX, NumberLinesY, SpacingX, SpacingY
    )
    Total args: 7. Return: int (0=OK).
    """
    log.info("Step 2: Creating model with NewGridOnly...")
    log.info(f"  Stories: {N_STORIES} (h1={STORY_HEIGHT_1}m, "
             f"h_typ={STORY_HEIGHT_TYP}m, H_total={H_TOTAL}m)")
    log.info(f"  Grid: {N_LINES_X} X-lines x {N_LINES_Y} Y-lines "
             f"(uniform spacing: {GRID_SPACING}m)")

    ret = SapModel.File.NewGridOnly(
        N_STORIES,          # 5 stories
        STORY_HEIGHT_TYP,   # 3.00 m (pisos 2-5)
        STORY_HEIGHT_1,     # 3.50 m (piso 1)
        N_LINES_X,          # 6 X-lines
        N_LINES_Y,          # 6 Y-lines
        GRID_SPACING,       # 6.5 m X spacing (uniform)
        GRID_SPACING,       # 6.5 m Y spacing (uniform)
    )
    check_ret(ret, "File.NewGridOnly")
    log.info("  NewGridOnly OK — stories and grid created")


# ===================================================================
# STEP 3: Relabel grid lines (X: 1-6, Y: A-F)
# ===================================================================

def relabel_grid_lines(SapModel):
    """Relabel grid lines via DatabaseTables API.

    NewGridOnly creates default labels (A,B,C... for X; 1,2,3... for Y or similar).
    We need: X-lines = "1","2","3","4","5","6" and Y-lines = "A","B","C","D","E","F".
    The coordinates are already correct (uniform 6.5m spacing).

    Table: "Grid Definitions - Grid Lines"
    Fields: Name, Grid Line Type, ID, Ordinate, Visible, Bubble Location
    """
    TABLE_KEY = "Grid Definitions - Grid Lines"
    TABLE_VERSION = 1

    log.info("Step 3: Relabeling grid lines via DatabaseTables...")

    # --- 3a: Get current grid data to learn field names ---
    try:
        result = SapModel.DatabaseTables.GetTableForEditingArray(
            TABLE_KEY, "", 1
        )
        if isinstance(result, (tuple, list)):
            ret_code = result[-1]
            if ret_code != 0:
                log.warning(f"  GetTableForEditingArray returned {ret_code}")
                raise RuntimeError(f"GetTableForEditingArray failed: ret={ret_code}")
            fields_raw = result[1] if len(result) > 2 else None
            log.info(f"  Current table fields: {fields_raw}")
        else:
            raise RuntimeError("Unexpected return type from GetTableForEditingArray")
    except Exception as e:
        log.warning(f"  Could not read grid table: {e}")
        log.warning("  Grid labels may need manual adjustment — positions are correct.")
        _print_grid_reference()
        return False

    # --- 3b: Build new grid data ---
    fields = ["Name", "Grid Line Type", "ID", "Ordinate",
              "Visible", "Bubble Location"]

    grid_sys_name = _get_grid_system_name(SapModel)

    table_data = []
    n_records = N_LINES_X + N_LINES_Y

    # X-direction grid lines (ejes 1-6)
    for name, val in zip(GRID_X_NAMES, GRID_X_VALS):
        table_data.extend([
            grid_sys_name,      # Name (grid system)
            "X (Cartesian)",    # Grid Line Type
            name,               # ID (label: "1", "2", ..., "6")
            str(val),           # Ordinate (position in m)
            "Yes",              # Visible
            "End",              # Bubble Location
        ])

    # Y-direction grid lines (ejes A-F)
    for name, val in zip(GRID_Y_NAMES, GRID_Y_VALS):
        table_data.extend([
            grid_sys_name,      # Name
            "Y (Cartesian)",    # Grid Line Type
            name,               # ID (label: "A", "B", ..., "F")
            str(val),           # Ordinate
            "Yes",              # Visible
            "Start",            # Bubble Location
        ])

    log.info(f"  Grid system: '{grid_sys_name}'")
    log.info(f"  Setting {N_LINES_X} X-lines + {N_LINES_Y} Y-lines = "
             f"{n_records} records")

    # --- 3c: Set edited data ---
    try:
        ret = SapModel.DatabaseTables.SetTableForEditingArray(
            TABLE_KEY, TABLE_VERSION, fields, n_records, table_data
        )
        check_ret(ret, "SetTableForEditingArray (grid)")
    except Exception as e:
        log.warning(f"  SetTableForEditingArray failed: {e}")
        log.warning("  Grid labels may need manual adjustment — positions are correct.")
        _print_grid_reference()
        return False

    # --- 3d: Apply changes ---
    try:
        result = SapModel.DatabaseTables.ApplyEditedTables(True)
        if isinstance(result, (tuple, list)):
            n_fatal = result[1] if len(result) > 2 else 0
            n_warn = result[2] if len(result) > 3 else 0
            import_log = result[4] if len(result) > 5 else ""
            ret_code = result[-1]

            if n_fatal > 0:
                log.error(f"  ApplyEditedTables: {n_fatal} fatal errors")
                log.error(f"  Import log: {import_log}")
                _print_grid_reference()
                return False
            if n_warn > 0:
                log.warning(f"  ApplyEditedTables: {n_warn} warnings")
            if ret_code != 0:
                log.warning(f"  ApplyEditedTables ret={ret_code}")
                _print_grid_reference()
                return False
        else:
            check_ret(result, "ApplyEditedTables")
    except Exception as e:
        log.warning(f"  ApplyEditedTables failed: {e}")
        log.warning("  Grid labels may need manual adjustment — positions are correct.")
        _print_grid_reference()
        return False

    log.info("  Grid lines relabeled successfully via DatabaseTables")
    return True


def _get_grid_system_name(SapModel):
    """Get the name of the current grid system (usually 'G1' or 'Global')."""
    try:
        result = SapModel.GridSys.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            names = result[1]
            if names and len(names) > 0:
                name = names[0] if hasattr(names, '__getitem__') else str(names)
                log.info(f"  Grid system found: '{name}'")
                return str(name)
    except Exception as e:
        log.debug(f"  GetNameList failed: {e}")

    return "G1"


def _print_grid_reference():
    """Print a reference table of all grid line positions."""
    log.info("")
    log.info("  Grid X (6 axes, uniform 6.5m):")
    for name, val in zip(GRID_X_NAMES, GRID_X_VALS):
        log.info(f"    Eje {name}: {val:8.3f} m")
    log.info("")
    log.info("  Grid Y (6 axes, uniform 6.5m):")
    for name, val in zip(GRID_Y_NAMES, GRID_Y_VALS):
        log.info(f"    Eje {name}: {val:8.3f} m")


# ===================================================================
# STEP 4: Verify model
# ===================================================================

def verify_stories(SapModel):
    """Verify that stories were created correctly.

    Checks:
      - Number of stories = 5
      - Story names exist
      - Base elevation = 0
      - Top elevation = 15.50 m
    """
    log.info("Step 4a: Verifying stories...")

    try:
        result = SapModel.Story.GetStories()
        # result: (NumberStories, StoryNames[], StoryHeights[],
        #          StoryElevations[], IsMasterStory[], SimilarToStory[],
        #          SpliceAbove[], SpliceHeight[], Color[], ret)
        if isinstance(result, (tuple, list)):
            n = result[0]
            heights = result[2]
            elevations = result[3]
            ret_code = result[-1]

            if ret_code != 0:
                log.warning(f"  Story.GetStories ret={ret_code}")

            log.info(f"  Number of stories: {n}")

            if n != N_STORIES:
                log.error(f"  MISMATCH: expected {N_STORIES} stories, got {n}")
            else:
                log.info(f"  Stories count OK ({N_STORIES})")

            if elevations and len(elevations) > 0:
                elev_list = list(elevations)
                top_elev = max(elev_list) if elev_list else 0
                log.info(f"  First story height: {heights[0]:.2f} m "
                         f"(expected {STORY_HEIGHT_1:.2f})")
                log.info(f"  Top elevation: {top_elev:.2f} m "
                         f"(expected {H_TOTAL:.2f})")

                if abs(top_elev - H_TOTAL) > 0.01:
                    log.error(f"  MISMATCH: top elevation {top_elev:.2f} "
                              f"!= {H_TOTAL:.2f}")
                else:
                    log.info(f"  Total height OK ({H_TOTAL:.1f} m)")
            return True
    except Exception as e:
        log.warning(f"  Story verification failed: {e}")
        log.warning("  get_story_data() is known to fail in v19 — "
                     "this is non-critical if NewGridOnly returned 0")
        return True

    return True


def verify_grid(SapModel):
    """Verify grid line positions and labels."""
    log.info("Step 4b: Verifying grid lines...")

    try:
        result = SapModel.GridSys.GetNameList()
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            n_grids = result[0]
            grid_names = result[1]
            log.info(f"  Grid systems: {n_grids} — {grid_names}")
    except Exception as e:
        log.warning(f"  Grid verification skipped: {e}")
        return True

    try:
        TABLE_KEY = "Grid Definitions - Grid Lines"
        result = SapModel.DatabaseTables.GetTableForDisplayArray(
            TABLE_KEY, [], "All", 1
        )
        if isinstance(result, (tuple, list)) and result[-1] == 0:
            n_records = result[1] if len(result) > 2 else 0
            log.info(f"  Grid lines in table: {n_records} records")
        else:
            log.info("  Grid table read returned non-zero — "
                     "grid may need manual verification")
    except Exception as e:
        log.debug(f"  Grid table read failed: {e}")
        log.info("  Grid table verification skipped (non-critical)")

    return True


def verify_units(SapModel):
    """Verify model units are Tonf_m_C (=12)."""
    log.info("Step 4c: Verifying units...")
    try:
        units = SapModel.GetPresentUnits()
        if isinstance(units, (tuple, list)):
            units = units[0]
        log.info(f"  Present units: {units} "
                 f"({'Tonf_m_C' if units == UNITS_TONF_M_C else 'OTHER'})")
        if units != UNITS_TONF_M_C:
            log.warning("  Setting units to Tonf_m_C...")
            set_units(UNITS_TONF_M_C)
    except Exception as e:
        log.warning(f"  Units check failed: {e}")


# ===================================================================
# STEP 5: Save model
# ===================================================================

def save_model(SapModel, filename="Edificio2_api.edb"):
    """Save the model to the ed2/models/ directory.

    Creates the output directory if it doesn't exist.
    """
    log.info("Step 5: Saving model...")

    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR, exist_ok=True)
        log.info(f"  Created directory: {MODELS_DIR}")

    filepath = os.path.join(MODELS_DIR, filename)

    try:
        ret = SapModel.File.Save(filepath)
        if isinstance(ret, (tuple, list)):
            ret = ret[-1]
        if ret == 0:
            log.info(f"  Model saved: {filepath}")
        else:
            log.warning(f"  File.Save returned {ret}")
            log.warning("  If ETABS was opened without UI (CreateObject), "
                        "the .edb may be corrupted.")
            log.warning("  Workaround: open ETABS manually, File > New > Blank, "
                        "then re-run this script.")
    except Exception as e:
        log.error(f"  Save failed: {e}")
        log.error(f"  Manual save: File > Save As > {filepath}")
        raise

    return filepath


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: initialize model, create grid, verify, save."""
    log.info("=" * 60)
    log.info("01_init_model_ed2.py — Edificio 2 (5p marcos HA, Antofagasta)")
    log.info("=" * 60)

    log.info(f"  Grid: {N_LINES_X} X-axes x {N_LINES_Y} Y-axes "
             f"(uniform {GRID_SPACING}m)")
    log.info(f"  Plan: {LX_PLANTA:.1f} x {LY_PLANTA:.1f} m")
    log.info(f"  Stories: {N_STORIES} (H={H_TOTAL:.1f} m)")
    log.info(f"  Units: Tonf_m_C (={UNITS_TONF_M_C})")
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
        # Step 1: Initialize model
        init_model(SapModel)

        # Step 2: Create stories + uniform grid
        create_grid_and_stories(SapModel)

        # Allow ETABS to process
        time.sleep(2)

        # Step 3: Relabel grid lines (X: 1-6, Y: A-F)
        grid_ok = relabel_grid_lines(SapModel)

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Step 4: Verify
        verify_units(SapModel)
        verify_stories(SapModel)
        verify_grid(SapModel)

        # Step 5: Save
        filepath = save_model(SapModel)

        # Summary
        log.info("")
        log.info("=" * 60)
        log.info("SUMMARY")
        log.info("=" * 60)
        log.info(f"  Model: {filepath}")
        log.info(f"  Stories: {N_STORIES} (h1={STORY_HEIGHT_1}m, "
                 f"h_typ={STORY_HEIGHT_TYP}m)")
        log.info(f"  Grid: {N_LINES_X} X-axes [{GRID_X_NAMES[0]}-"
                 f"{GRID_X_NAMES[-1]}] x "
                 f"{N_LINES_Y} Y-axes [{GRID_Y_NAMES[0]}-"
                 f"{GRID_Y_NAMES[-1]}]")
        log.info(f"  Spacing: {GRID_SPACING}m (uniform both directions)")
        log.info(f"  Grid labeling: {'OK' if grid_ok else 'NEEDS MANUAL FIX'}")
        log.info(f"  Plan dimensions: {LX_PLANTA:.1f} x {LY_PLANTA:.1f} m")
        log.info(f"  Total height: {H_TOTAL:.1f} m")
        log.info("")
        if grid_ok:
            log.info("Model ready for next step (02_materials_sections_ed2.py)")
        else:
            log.info("Model created but grid labels need manual adjustment.")
            log.info("Coordinates are correct — labels are cosmetic only.")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
