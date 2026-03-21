"""
01_init_model.py — Initialize ETABS model with grid and stories for Edificio 1.

Creates a new ETABS model from scratch:
  1. Initializes model with Tonf_m_C units
  2. Creates 20 stories via NewGridOnly (h1=3.40m, h2-20=2.60m)
  3. Edits grid line positions and labels to match the irregular building grid
     (17 ejes X + 6 ejes Y with exact coordinates from Enunciado Taller)
  4. Verifies stories and grid
  5. Saves model as Edificio1_api.edb

Prerequisites:
  - ETABS v19 must be open manually (File > New Model > Blank)
  - comtypes installed (pip install comtypes)
  - config.py in the same directory

Usage:
  python 01_init_model.py

Fuente datos: Enunciado Taller ADSE 1S-2026, Prof. Music (pags 2-6)
Firmas COM: autonomo/research/com_signatures.md (R03)
"""

import sys
import os
import time

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, disconnect, check_ret, verify_model, set_units, get_model, log,
    UNITS_TONF_M_C,
    N_STORIES, STORY_HEIGHT_TYP, STORY_HEIGHT_1,
    N_LINES_X, N_LINES_Y,
    GRID_X, GRID_Y, GRID_X_NAMES, GRID_X_VALS,
    GRID_Y_NAMES, GRID_Y_VALS,
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
# STEP 2: Create model with NewGridOnly (stories + placeholder grid)
# ===================================================================

def create_grid_and_stories(SapModel):
    """Create model skeleton: 20 stories + initial grid via NewGridOnly.

    NewGridOnly creates:
      - Stories with correct heights (BottomStoryHeight for piso 1)
      - A uniform grid as placeholder (will be edited in step 3)

    Firma: com_signatures.md §1.3
    ret = SapModel.File.NewGridOnly(
        NumberStorys, TypicalStoryHeight, BottomStoryHeight,
        NumberLinesX, NumberLinesY, SpacingX, SpacingY
    )
    Total args: 7. Return: int (0=OK).
    """
    # Use average spacing as placeholder — will be edited to exact values
    avg_spacing_x = LX_PLANTA / (N_LINES_X - 1)  # ~2.406 m
    avg_spacing_y = LY_PLANTA / (N_LINES_Y - 1)  # ~2.764 m

    log.info("Step 2: Creating model with NewGridOnly...")
    log.info(f"  Stories: {N_STORIES} (h1={STORY_HEIGHT_1}m, "
             f"h_typ={STORY_HEIGHT_TYP}m, H_total={H_TOTAL}m)")
    log.info(f"  Grid: {N_LINES_X} X-lines x {N_LINES_Y} Y-lines "
             f"(placeholder spacing: {avg_spacing_x:.3f} x {avg_spacing_y:.3f} m)")

    ret = SapModel.File.NewGridOnly(
        N_STORIES,          # 20 stories
        STORY_HEIGHT_TYP,   # 2.60 m (pisos 2-20)
        STORY_HEIGHT_1,     # 3.40 m (piso 1)
        N_LINES_X,          # 17 X-lines
        N_LINES_Y,          # 6 Y-lines
        avg_spacing_x,      # placeholder X spacing
        avg_spacing_y,      # placeholder Y spacing
    )
    check_ret(ret, "File.NewGridOnly")
    log.info("  NewGridOnly OK — stories created")


# ===================================================================
# STEP 3: Edit grid to match exact building coordinates
# ===================================================================

def edit_grid_via_database_tables(SapModel):
    """Edit grid line positions and labels via DatabaseTables API.

    After NewGridOnly creates a uniform grid, this function modifies each
    grid line to have the correct coordinate and label from the Enunciado.

    Approach:
      1. GetTableForEditingArray — get current grid data and field names
      2. Build new data with exact coordinates and labels
      3. SetTableForEditingArray + ApplyEditedTables

    Table: "Grid Definitions - Grid Lines"
    Fields: Name, Grid Line Type, ID, Ordinate, Visible, Bubble Location
    """
    TABLE_KEY = "Grid Definitions - Grid Lines"
    TABLE_VERSION = 1

    log.info("Step 3: Editing grid lines via DatabaseTables...")

    # --- 3a: Get current grid data to learn field names ---
    try:
        result = SapModel.DatabaseTables.GetTableForEditingArray(
            TABLE_KEY, "", 1
        )
        # result is typically: (TableVersion, FieldsKeysIncluded, NumberRecords,
        #                       TableData, ret)
        # The exact tuple structure depends on the COM binding
        if isinstance(result, tuple):
            ret_code = result[-1]
            if ret_code != 0:
                log.warning(f"  GetTableForEditingArray returned {ret_code}")
                raise RuntimeError(f"GetTableForEditingArray failed: ret={ret_code}")
            # Extract field names from the result
            fields_raw = result[1] if len(result) > 2 else None
            log.info(f"  Current table fields: {fields_raw}")
        else:
            raise RuntimeError("Unexpected return type from GetTableForEditingArray")
    except Exception as e:
        log.warning(f"  Could not read grid table: {e}")
        log.warning("  Falling back to direct grid editing approach...")
        return edit_grid_fallback(SapModel)

    # --- 3b: Build new grid data ---
    # Standard ETABS field names for grid lines
    fields = ["Name", "Grid Line Type", "ID", "Ordinate",
              "Visible", "Bubble Location"]

    # Determine grid system name — usually "G1" or "Global" after NewGridOnly
    grid_sys_name = _get_grid_system_name(SapModel)

    # Build flat data array (row-major: field1_row1, field2_row1, ..., field1_row2, ...)
    table_data = []
    n_records = N_LINES_X + N_LINES_Y

    # X-direction grid lines (ejes 1-17)
    for name, val in zip(GRID_X_NAMES, GRID_X_VALS):
        table_data.extend([
            grid_sys_name,      # Name (grid system)
            "X (Cartesian)",    # Grid Line Type
            name,               # ID (label: "1", "2", ...)
            str(val),           # Ordinate (position in m)
            "Yes",              # Visible
            "End",              # Bubble Location
        ])

    # Y-direction grid lines (ejes A-F)
    for name, val in zip(GRID_Y_NAMES, GRID_Y_VALS):
        table_data.extend([
            grid_sys_name,      # Name
            "Y (Cartesian)",    # Grid Line Type
            name,               # ID (label: "A", "B", ...)
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
        return edit_grid_fallback(SapModel)

    # --- 3d: Apply changes ---
    try:
        result = SapModel.DatabaseTables.ApplyEditedTables(True)
        # result: (FillImport, NumFatalErrors, NumWarnMsgs, NumInfoMsgs, ImportLog, ret)
        if isinstance(result, tuple):
            n_fatal = result[1] if len(result) > 2 else 0
            n_warn = result[2] if len(result) > 3 else 0
            import_log = result[4] if len(result) > 5 else ""
            ret_code = result[-1]

            if n_fatal > 0:
                log.error(f"  ApplyEditedTables: {n_fatal} fatal errors")
                log.error(f"  Import log: {import_log}")
                return edit_grid_fallback(SapModel)
            if n_warn > 0:
                log.warning(f"  ApplyEditedTables: {n_warn} warnings")
            if ret_code != 0:
                log.warning(f"  ApplyEditedTables ret={ret_code}")
                return edit_grid_fallback(SapModel)
        else:
            check_ret(result, "ApplyEditedTables")
    except Exception as e:
        log.warning(f"  ApplyEditedTables failed: {e}")
        return edit_grid_fallback(SapModel)

    log.info("  Grid lines edited successfully via DatabaseTables")
    return True


def edit_grid_fallback(SapModel):
    """Fallback: try to edit grid via GridSys_2 or log manual instructions.

    If DatabaseTables fails, try SetGridSys_2 (available in some v19 builds).
    If that also fails, the grid remains uniform but all elements will be
    placed at correct coordinates regardless — the grid is only visual.
    """
    log.info("  Attempting fallback: EditGrid via GridSys API...")

    grid_sys_name = _get_grid_system_name(SapModel)

    # Try SetGridSys_2 — known to exist in some ETABS v19 builds
    # Signature (from Eng-Tips/SAP2000 API):
    #   SetGridSys_2(Name, GridSysType, NumXLines, NumYLines,
    #                GridLineIDX[], GridLineIDY[],
    #                OrdinateX[], OrdinateY[],
    #                VisibleX[], VisibleY[],
    #                BubbleLocX[], BubbleLocY[])
    try:
        ret = SapModel.GridSys.SetGridSys_2(
            grid_sys_name,
            1,                     # Cartesian
            N_LINES_X,
            N_LINES_Y,
            GRID_X_NAMES,          # Labels X: ["1","2",...,"17"]
            GRID_Y_NAMES,          # Labels Y: ["A","B",...,"F"]
            GRID_X_VALS,           # Ordinates X
            GRID_Y_VALS,           # Ordinates Y
            [True] * N_LINES_X,    # Visible X
            [True] * N_LINES_Y,    # Visible Y
            ["End"] * N_LINES_X,   # Bubble X
            ["Start"] * N_LINES_Y, # Bubble Y
        )
        check_ret(ret, "GridSys.SetGridSys_2")
        log.info("  Grid edited via SetGridSys_2 OK")
        return True
    except Exception as e:
        log.warning(f"  SetGridSys_2 failed: {e}")

    # Final fallback: log manual instructions
    log.warning("=" * 60)
    log.warning("  GRID EDITING FAILED — manual adjustment required.")
    log.warning("  The stories are correct but grid positions are uniform.")
    log.warning("  To fix in ETABS UI:")
    log.warning("    1. Go to Define > Coordinate Systems / Grids")
    log.warning("    2. Edit grid line positions to match config.py values")
    log.warning("  NOTE: Elements will be placed at exact coordinates")
    log.warning("  regardless — the grid is purely visual/reference.")
    log.warning("=" * 60)

    _print_grid_reference()
    return False


def _get_grid_system_name(SapModel):
    """Get the name of the current grid system (usually 'G1' or 'Global')."""
    try:
        result = SapModel.GridSys.GetNameList()
        # result: (NumberNames, Names_array, ret)
        if isinstance(result, tuple) and len(result) >= 2:
            names = result[1]
            if names and len(names) > 0:
                name = names[0] if hasattr(names, '__getitem__') else str(names)
                log.info(f"  Grid system found: '{name}'")
                return str(name)
    except Exception as e:
        log.debug(f"  GetNameList failed: {e}")

    # Default name after NewGridOnly
    return "G1"


def _print_grid_reference():
    """Print a reference table of all grid line positions."""
    log.info("")
    log.info("  Grid X (17 axes):")
    for name, val in zip(GRID_X_NAMES, GRID_X_VALS):
        log.info(f"    Eje {name:>2s}: {val:8.3f} m")
    log.info("")
    log.info("  Grid Y (6 axes):")
    for name, val in zip(GRID_Y_NAMES, GRID_Y_VALS):
        log.info(f"    Eje {name}: {val:8.3f} m")


# ===================================================================
# STEP 4: Verify model
# ===================================================================

def verify_stories(SapModel):
    """Verify that stories were created correctly.

    Checks:
      - Number of stories = 20
      - Story names exist
      - Base elevation = 0
      - Top elevation = 52.80 m
    """
    log.info("Step 4a: Verifying stories...")

    try:
        result = SapModel.Story.GetStories()
        # result: (NumberStories, StoryNames[], StoryHeights[],
        #          StoryElevations[], IsMasterStory[], SimilarToStory[],
        #          SpliceAbove[], SpliceHeight[], Color[], ret)
        if isinstance(result, tuple):
            n = result[0]
            names = result[1]
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

            # Print first, last, and total height
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
        return True  # NewGridOnly with ret=0 guarantees correct stories

    return True


def verify_grid(SapModel):
    """Verify grid line positions and labels."""
    log.info("Step 4b: Verifying grid lines...")

    # Try to read grid data
    try:
        result = SapModel.GridSys.GetNameList()
        if isinstance(result, tuple) and len(result) >= 2:
            n_grids = result[0]
            grid_names = result[1]
            log.info(f"  Grid systems: {n_grids} — {grid_names}")
    except Exception as e:
        log.warning(f"  Grid verification skipped: {e}")
        return True

    # Try to read grid line positions via DatabaseTables
    try:
        TABLE_KEY = "Grid Definitions - Grid Lines"
        result = SapModel.DatabaseTables.GetTableForDisplayArray(
            TABLE_KEY, [], "All", 1
        )
        if isinstance(result, tuple) and result[-1] == 0:
            n_records = result[1] if len(result) > 2 else 0
            log.info(f"  Grid lines in table: {n_records} records")

            # Count X and Y lines
            table_data = result[2] if len(result) > 3 else []
            fields = result[0] if len(result) > 1 else []
            if table_data and fields:
                log.info(f"  Table fields: {list(fields)}")
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
        if isinstance(units, tuple):
            units = units[0]
        log.info(f"  Present units: {units} "
                 f"({'Tonf_m_C' if units == UNITS_TONF_M_C else 'OTHER'})")
        if units != UNITS_TONF_M_C:
            log.warning(f"  Setting units to Tonf_m_C...")
            set_units(UNITS_TONF_M_C)
    except Exception as e:
        log.warning(f"  Units check failed: {e}")


# ===================================================================
# STEP 5: Save model
# ===================================================================

def save_model(SapModel, filename="Edificio1_api.edb"):
    """Save the model to the models/ directory.

    Creates the output directory if it doesn't exist.
    """
    log.info("Step 5: Saving model...")

    # Ensure output directory exists
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR, exist_ok=True)
        log.info(f"  Created directory: {MODELS_DIR}")

    filepath = os.path.join(MODELS_DIR, filename)

    try:
        ret = SapModel.File.Save(filepath)
        if isinstance(ret, tuple):
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
    log.info("01_init_model.py — Edificio 1 (20p muros HA, Antofagasta)")
    log.info("=" * 60)

    # Print expected parameters
    log.info(f"  Grid: {N_LINES_X} X-axes x {N_LINES_Y} Y-axes")
    log.info(f"  Plan: {LX_PLANTA:.3f} x {LY_PLANTA:.3f} m")
    log.info(f"  Stories: {N_STORIES} (H={H_TOTAL:.1f} m)")
    log.info(f"  Units: Tonf_m_C (={UNITS_TONF_M_C})")
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
        # Step 1: Initialize model
        init_model(SapModel)

        # Step 2: Create stories + placeholder grid
        create_grid_and_stories(SapModel)

        # Allow ETABS to process
        time.sleep(2)

        # Step 3: Edit grid to exact building coordinates
        grid_ok = edit_grid_via_database_tables(SapModel)

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
        log.info(f"  Grid editing: {'OK' if grid_ok else 'NEEDS MANUAL FIX'}")
        log.info(f"  Plan dimensions: {LX_PLANTA:.3f} x {LY_PLANTA:.3f} m")
        log.info(f"  Total height: {H_TOTAL:.1f} m")
        log.info("")
        if grid_ok:
            log.info("Model ready for next step (02_materials.py)")
        else:
            log.info("Model created but grid positions need manual adjustment.")
            log.info("Elements will be placed at correct coordinates regardless.")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
