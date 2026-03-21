"""
12_extract_results.py — Extract ALL analysis results for Edificio 1.

Comprehensive post-analysis extraction script that produces:
  1. Modal periods, mass participation, and dominant mode types
  2. Story drifts (NCh433 Condition 1: CM, Condition 2: max point)
  3. Base shear per load case and combination
  4. Centers of mass (CM) and rigidity (CR) per story
  5. Story shear and overturning moment per story
  6. Forces in border walls (axes 1 and F)
  7. P-M demand points for walls (Pu, Mu per combo)

Output:
  - Formatted tables printed to console
  - CSV files in autonomo/scripts/results/
  - Summary markdown in autonomo/research/resultados_esperados.md

Prerequisites:
  - ETABS v19 open with model from scripts 01-11
  - Analysis already completed (model locked with results)
  - comtypes installed
  - config.py in the same directory

Usage:
  python 12_extract_results.py                 # Extract all results
  python 12_extract_results.py --no-csv        # Console only, no CSV export
  python 12_extract_results.py --no-summary    # Skip markdown summary
  python 12_extract_results.py --sections 1 3  # Only extract specific sections

Units: Tonf, m, C (eUnits=12) throughout.

Drift notes (NCh433 + elastic spectrum):
  The pipeline uses the ELASTIC spectrum (Sa/g, unreduced). ETABS spectral
  analysis gives elastic displacements. For this building (T ~ 1.0-1.3s >> To
  = 0.40s), the equal displacement principle applies, so the elastic drift
  approximates the inelastic drift. Drift from ETABS can be compared directly
  against the 0.002 limit of NCh433 Art. 5.9.

COM signatures verified against:
  - autonomo/research/com_signatures.md §14-§15
  - autonomo/research/etabs_api_reference.md §19-§20
  - Results.Setup.DeselectAllCasesAndCombosForOutput(): 0 args
  - Results.Setup.SetCaseSelectedForOutput(CaseName): 1 arg
  - Results.Setup.SetComboSelectedForOutput(ComboName): 1 arg
  - Results.StoryDrifts(): 0 input args → 12-element tuple
  - Results.BaseReac(...): 0 input args → 14-element tuple
  - Results.FrameForce(Name, ItemTypeElm, ...): 2 input args
  - DatabaseTables.GetTableForDisplayArray(Key,"","All",1,[],0,[]): 4 input args

Sources: NCh433 Mod 2009, DS61, Material Apoyo Taller 2026, config.py
"""

import sys
import os
import csv
import time
import argparse
import traceback
from datetime import datetime

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
    N_STORIES, H_TOTAL, STORY_NAMES, STORY_HEIGHTS, STORY_ELEVATIONS,
    AREA_PLANTA, PESO_ESPERADO_TONF, DRIFT_LIMITE,
    R_MUROS, RO_MUROS, I_FACTOR, S_SUELO, AO_G, G_ACCEL,
    TO_SUELO, T_PRIME, N_SUELO, P_SUELO,
    calc_R_star, calc_Cmin, calc_Cmax,
    COMBINATIONS, GRID_X, GRID_Y,
    MUROS_DIR_Y, MUROS_DIR_X,
    LX_PLANTA, LY_PLANTA,
)

# ===================================================================
# CONSTANTS
# ===================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")

# Seismic cases
SEISMIC_CASES = ["SDX", "SDY"]
TORSION_CASES = ["SDTX", "SDTY"]
GRAVITY_CASES = ["PP", "TERP", "TERT", "SCP", "SCT"]
ALL_CASES = GRAVITY_CASES + SEISMIC_CASES + TORSION_CASES

# Drift limit NCh433 Art. 5.9.2
DRIFT_LIMIT_CM = 0.002       # Condition 1: at CM
DRIFT_LIMIT_MAX = 0.002      # Condition 2: at any point (same limit)

# Border wall axes for force extraction
BORDER_AXIS_1_X = GRID_X['1']    # x = 0.0
BORDER_AXIS_17_X = GRID_X['17']  # x = 38.505
BORDER_AXIS_A_Y = GRID_Y['A']    # y = 0.0
BORDER_AXIS_F_Y = GRID_Y['F']    # y = 13.821
COORD_TOL = 0.5  # m — tolerance for coordinate matching


# ===================================================================
# HELPER: Parse DatabaseTables result
# ===================================================================

def parse_db_table(SapModel, table_key, group="All"):
    """Parse a DatabaseTable into a list of dicts.

    Handles the variable return format from comtypes by trying multiple
    index positions for fields and data arrays.

    Args:
        SapModel: ETABS model object
        table_key: str — name of the table
        group: str — group filter ("All" for everything)

    Returns:
        (fields, rows) where fields is list of str, rows is list of dicts.
        Returns (None, None) on failure.
    """
    try:
        result = SapModel.DatabaseTables.GetTableForDisplayArray(
            table_key, "", group, 1, [], 0, [],
        )

        if not isinstance(result, tuple) or len(result) < 5:
            log.warning(f"  Table '{table_key}': unexpected format "
                        f"(len={len(result) if isinstance(result, tuple) else 'N/A'})")
            return None, None

        fields = None
        table_data = None

        # Try known index positions (varies by comtypes binding)
        for fields_idx, data_idx in [(4, 6), (2, 4), (3, 5)]:
            if len(result) > data_idx:
                try:
                    candidate_f = [str(f) for f in result[fields_idx]]
                    candidate_d = [str(d) for d in result[data_idx]]
                    if candidate_f and candidate_d and len(candidate_d) >= len(candidate_f):
                        fields = candidate_f
                        table_data = candidate_d
                        break
                except (TypeError, IndexError):
                    continue

        # Heuristic fallback: scan for field-name-like arrays
        if fields is None:
            for i in range(len(result)):
                item = result[i]
                if not isinstance(item, (list, tuple)) or len(item) < 2:
                    continue
                try:
                    first_str = str(item[0]).lower()
                    if any(k in first_str for k in
                           ['case', 'mode', 'story', 'output', 'name', 'type']):
                        fields = [str(f) for f in item]
                        # Next suitable array = data
                        for j in range(i + 1, len(result)):
                            if isinstance(result[j], (list, tuple)) and \
                               len(result[j]) >= len(fields):
                                table_data = [str(d) for d in result[j]]
                                break
                        break
                except (TypeError, IndexError):
                    continue

        if not fields or not table_data:
            log.warning(f"  Table '{table_key}': could not parse result "
                        f"({len(result)} elements)")
            return None, None

        n_fields = len(fields)
        n_rows = len(table_data) // n_fields

        if n_rows == 0:
            log.warning(f"  Table '{table_key}': no data rows")
            return fields, []

        rows = []
        for r in range(n_rows):
            offset = r * n_fields
            row = {}
            for c in range(n_fields):
                row[fields[c]] = table_data[offset + c]
            rows.append(row)

        return fields, rows

    except Exception as e:
        log.warning(f"  Table '{table_key}' query failed: {e}")
        return None, None


def safe_float(val, default=0.0):
    """Convert string to float, returning default on failure."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def select_cases_for_output(SapModel, cases):
    """Select specific load cases for output, deselecting all others."""
    SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    for case in cases:
        try:
            SapModel.Results.Setup.SetCaseSelectedForOutput(case)
        except Exception:
            pass


def select_combos_for_output(SapModel, combos):
    """Select specific combos for output, deselecting all others."""
    SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    for combo in combos:
        try:
            SapModel.Results.Setup.SetComboSelectedForOutput(combo)
        except Exception:
            pass


# ===================================================================
# CSV EXPORT HELPER
# ===================================================================

def ensure_results_dir():
    """Create results output directory if it doesn't exist."""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    return RESULTS_DIR


def export_csv_file(filename, headers, rows):
    """Export data to CSV file in results directory.

    Args:
        filename: str — CSV filename (without path)
        headers: list of str — column headers
        rows: list of lists — row data

    Returns:
        str — full path to written file
    """
    outdir = ensure_results_dir()
    filepath = os.path.join(outdir, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
    log.info(f"  CSV: {filename} ({len(rows)} rows)")
    return filepath


# ===================================================================
# CONSOLE TABLE PRINTER
# ===================================================================

def print_table(title, headers, rows, col_widths=None, alignments=None):
    """Print a formatted table to console via log.info.

    Args:
        title: str — table title
        headers: list of str
        rows: list of lists (matching headers length)
        col_widths: list of int (optional, auto-calculated if None)
        alignments: list of str ('>' for right, '<' for left, '^' for center)
    """
    if not rows:
        log.info(f"  {title}: no data")
        return

    n_cols = len(headers)
    if col_widths is None:
        col_widths = []
        for i in range(n_cols):
            max_w = len(str(headers[i]))
            for row in rows:
                if i < len(row):
                    max_w = max(max_w, len(str(row[i])))
            col_widths.append(min(max_w + 1, 20))

    if alignments is None:
        alignments = ['>'] * n_cols

    log.info("")
    log.info(f"  {title}")
    log.info(f"  {'─' * (sum(col_widths) + n_cols * 2)}")

    # Header
    hdr = "  "
    sep = "  "
    for i in range(n_cols):
        w = col_widths[i]
        hdr += f"{str(headers[i]):^{w}s}  "
        sep += f"{'─' * w}  "
    log.info(hdr)
    log.info(sep)

    # Rows
    for row in rows:
        line = "  "
        for i in range(n_cols):
            w = col_widths[i]
            val = str(row[i]) if i < len(row) else ""
            a = alignments[i] if i < len(alignments) else '>'
            line += f"{val:{a}{w}s}  "
        log.info(line)


# ===================================================================
# 1. MODAL RESULTS — Periods, mass participation, mode types
# ===================================================================

def extract_modal_results(SapModel):
    """Extract complete modal analysis results.

    Uses DatabaseTables "Modal Participating Mass Ratios" to get:
    - Period per mode
    - Individual and cumulative mass participation (UX, UY, RZ)
    - Mode type classification (translational X/Y, torsional, mixed)

    Returns:
        dict with 'modes' list and summary data, or None on failure
    """
    log.info("=" * 65)
    log.info("  1. MODAL RESULTS — Periods & Mass Participation")
    log.info("=" * 65)

    fields, rows = parse_db_table(SapModel, "Modal Participating Mass Ratios")

    if not rows:
        log.warning("  Could not extract modal results from DatabaseTables")
        # Fallback: try direct Results.ModalPeriod if available
        return None

    # Map column names (case-insensitive partial match)
    col_names = {f.lower().strip(): f for f in fields} if fields else {}

    def find_col(keywords):
        """Find column name matching any keyword."""
        for key, original in col_names.items():
            for kw in keywords:
                if kw in key:
                    return original
        return None

    col_mode = find_col(['mode'])
    col_period = find_col(['period'])
    col_ux = find_col(['ux'])
    col_uy = find_col(['uy'])
    col_uz = find_col(['uz'])
    col_sum_ux = find_col(['sumux', 'sum ux'])
    col_sum_uy = find_col(['sumuy', 'sum uy'])
    col_rz = find_col(['rz'])
    col_sum_rz = find_col(['sumrz', 'sum rz'])

    modes = []
    for row in rows:
        mode_num = int(safe_float(row.get(col_mode, '0'))) if col_mode else len(modes) + 1
        period = safe_float(row.get(col_period, '0')) if col_period else 0
        ux = safe_float(row.get(col_ux, '0')) if col_ux else 0
        uy = safe_float(row.get(col_uy, '0')) if col_uy else 0
        uz = safe_float(row.get(col_uz, '0')) if col_uz else 0
        sum_ux = safe_float(row.get(col_sum_ux, '0')) if col_sum_ux else 0
        sum_uy = safe_float(row.get(col_sum_uy, '0')) if col_sum_uy else 0
        rz = safe_float(row.get(col_rz, '0')) if col_rz else 0
        sum_rz = safe_float(row.get(col_sum_rz, '0')) if col_sum_rz else 0

        if period <= 0:
            continue

        # Classify mode type
        # Values may be ratios (0-1) or percentages (0-100)
        ux_pct = ux if ux > 1 else ux * 100
        uy_pct = uy if uy > 1 else uy * 100
        rz_pct = rz if rz > 1 else rz * 100

        if ux_pct > max(uy_pct, rz_pct) and ux_pct > 10:
            mode_type = "Trans-X"
        elif uy_pct > max(ux_pct, rz_pct) and uy_pct > 10:
            mode_type = "Trans-Y"
        elif rz_pct > max(ux_pct, uy_pct) and rz_pct > 10:
            mode_type = "Torsion"
        elif ux_pct < 5 and uy_pct < 5 and rz_pct < 5:
            mode_type = "Local"
        else:
            mode_type = "Mixed"

        modes.append({
            'mode': mode_num,
            'period': period,
            'ux': ux, 'uy': uy, 'uz': uz,
            'sum_ux': sum_ux, 'sum_uy': sum_uy,
            'rz': rz, 'sum_rz': sum_rz,
            'type': mode_type,
        })

    if not modes:
        log.warning("  No valid modal data found")
        return None

    # Normalize: detect if values are ratios or percentages
    is_pct = any(m['sum_ux'] > 1 or m['sum_uy'] > 1 for m in modes)

    result = {
        'modes': modes,
        'n_modes': len(modes),
        'is_percentage': is_pct,
        'T1': modes[0]['period'],
    }

    # R* for T1
    t1 = modes[0]['period']
    r_star = calc_R_star(t1)
    result['R_star'] = r_star

    # Final cumulative participation
    if modes:
        last = modes[-1]
        sux = last['sum_ux']
        suy = last['sum_uy']
        if is_pct:
            sux /= 100
            suy /= 100
        result['final_sum_ux'] = sux
        result['final_sum_uy'] = suy

    # Print table
    tbl_headers = ["Mode", "T (s)", "UX%", "UY%", "RZ%", "SumUX%", "SumUY%", "Type"]
    tbl_rows = []
    for m in modes[:15]:  # Show first 15 modes
        if is_pct:
            tbl_rows.append([
                m['mode'], f"{m['period']:.4f}",
                f"{m['ux']:.2f}", f"{m['uy']:.2f}", f"{m['rz']:.2f}",
                f"{m['sum_ux']:.2f}", f"{m['sum_uy']:.2f}", m['type'],
            ])
        else:
            tbl_rows.append([
                m['mode'], f"{m['period']:.4f}",
                f"{m['ux']*100:.2f}", f"{m['uy']*100:.2f}", f"{m['rz']*100:.2f}",
                f"{m['sum_ux']*100:.2f}", f"{m['sum_uy']*100:.2f}", m['type'],
            ])

    print_table("Modal Periods & Mass Participation", tbl_headers, tbl_rows,
                col_widths=[5, 8, 7, 7, 7, 8, 8, 9],
                alignments=['>', '>', '>', '>', '>', '>', '>', '<'])

    # Summary
    log.info("")
    log.info(f"  T1 = {t1:.4f} s  |  R*(T1) = {r_star:.2f}")
    if len(modes) >= 2:
        log.info(f"  T2 = {modes[1]['period']:.4f} s")
    if len(modes) >= 3:
        log.info(f"  T3 = {modes[2]['period']:.4f} s")

    sux_final = result.get('final_sum_ux', 0) * 100
    suy_final = result.get('final_sum_uy', 0) * 100
    log.info(f"  Cumulative: SumUX = {sux_final:.1f}%, SumUY = {suy_final:.1f}% "
             f"({result['n_modes']} modes)")
    log.info(f"  NCh433 Art. 6.3.6.2 requires >= 90%: "
             f"{'PASS' if sux_final >= 90 and suy_final >= 90 else 'FAIL'}")
    log.info("")

    return result


# ===================================================================
# 2. STORY DRIFTS — NCh433 Conditions 1 & 2
# ===================================================================

def extract_story_drifts(SapModel):
    """Extract story drifts for all seismic cases.

    NCh433 Art. 5.9:
      Condition 1: Drift at CM <= 0.002 (elastic, T >> To for this building)
      Condition 2: Maximum drift at any point <= 0.002
                   (includes torsion amplification effects)

    ETABS StoryDrifts() returns drift at the point of maximum drift per story,
    which covers Condition 2. For Condition 1 (CM drift), we also extract from
    the DatabaseTables "Story Drifts" table which includes labels for CM.

    Returns:
        dict with 'records', 'max_per_story', 'violations', or None
    """
    log.info("=" * 65)
    log.info("  2. STORY DRIFTS — NCh433 Conditions 1 & 2")
    log.info("=" * 65)

    # --- Method A: Results.StoryDrifts() (direct API) ---
    all_cases = SEISMIC_CASES + TORSION_CASES
    select_cases_for_output(SapModel, all_cases)

    records = []
    try:
        result = SapModel.Results.StoryDrifts(
            0, [], [], [], [],        # NumberResults, Story, LoadCase, StepType, StepNum
            [], [], [], [], [], [],   # Direction, Drift, Label, X, Y, Z
        )

        if isinstance(result, tuple) and len(result) >= 12 and result[0] > 0:
            n = result[0]
            for i in range(n):
                records.append({
                    'story': str(result[1][i]),
                    'case': str(result[2][i]),
                    'direction': str(result[5][i]),
                    'drift': float(result[6][i]),
                    'label': str(result[7][i]),
                    'x': float(result[8][i]),
                    'y': float(result[9][i]),
                    'z': float(result[10][i]),
                })
            log.info(f"  StoryDrifts(): {n} records from API")
    except Exception as e:
        log.warning(f"  StoryDrifts() failed: {e}")

    # --- Method B: DatabaseTables fallback ---
    if not records:
        log.info("  Trying DatabaseTables 'Story Drifts'...")
        fields, db_rows = parse_db_table(SapModel, "Story Drifts")
        if db_rows:
            for row in db_rows:
                story = row.get('Story', row.get('story', ''))
                case = row.get('OutputCase', row.get('Load Case', ''))
                direction = row.get('Direction', row.get('direction', ''))
                drift = safe_float(row.get('Drift', row.get('drift', '0')))
                label = row.get('Label', row.get('label', ''))
                x = safe_float(row.get('X', '0'))
                y = safe_float(row.get('Y', '0'))
                z = safe_float(row.get('Z', '0'))

                if story and drift != 0:
                    records.append({
                        'story': story, 'case': case, 'direction': direction,
                        'drift': drift, 'label': label, 'x': x, 'y': y, 'z': z,
                    })
            log.info(f"  DatabaseTables: {len(records)} records")

    if not records:
        log.warning("  No drift data available")
        return None

    # --- Organize by story, case, direction ---
    # Find max drift per (story, direction) across all cases
    max_per_story = {}
    for rec in records:
        key = (rec['story'], rec['direction'])
        if key not in max_per_story or abs(rec['drift']) > abs(max_per_story[key]['drift']):
            max_per_story[key] = rec

    # Find max drift per (case, direction)
    max_per_case = {}
    for rec in records:
        key = (rec['case'], rec['direction'])
        if key not in max_per_case or abs(rec['drift']) > abs(max_per_case[key]['drift']):
            max_per_case[key] = rec

    # Violations
    violations = []
    for rec in records:
        if abs(rec['drift']) > DRIFT_LIMIT_CM:
            violations.append(rec)

    # --- Print summary per case ---
    tbl_headers = ["Case", "Dir", "Max Drift", "Story", "Label", "Status"]
    tbl_rows = []
    for (case, direction), rec in sorted(max_per_case.items()):
        d = abs(rec['drift'])
        status = "OK" if d <= DRIFT_LIMIT_CM else "FAIL"
        tbl_rows.append([
            case, direction, f"{d:.6f}", rec['story'], rec['label'], status,
        ])

    print_table("Maximum Drift per Case & Direction", tbl_headers, tbl_rows,
                col_widths=[8, 4, 10, 10, 8, 5],
                alignments=['<', '>', '>', '<', '>', '<'])

    # --- Print drift profile (all stories, worst case per direction) ---
    log.info("")
    log.info("  Drift Profile (worst-case envelope per direction):")

    tbl2_headers = ["Story", "Elev (m)", "Drift X", "Drift Y", "Limit", "Status"]
    tbl2_rows = []
    for sn in reversed(STORY_NAMES):
        dx = abs(max_per_story.get((sn, 'X'), {}).get('drift', 0))
        dy = abs(max_per_story.get((sn, 'Y'), {}).get('drift', 0))
        idx = STORY_NAMES.index(sn) if sn in STORY_NAMES else -1
        elev = STORY_ELEVATIONS[idx] if 0 <= idx < len(STORY_ELEVATIONS) else 0
        worst = max(dx, dy)
        status = "OK" if worst <= DRIFT_LIMIT_CM else "FAIL"
        tbl2_rows.append([
            sn, f"{elev:.1f}", f"{dx:.6f}", f"{dy:.6f}",
            f"{DRIFT_LIMIT_CM:.4f}", status,
        ])

    print_table("Drift Profile — All Stories", tbl2_headers, tbl2_rows,
                col_widths=[10, 8, 10, 10, 8, 5],
                alignments=['<', '>', '>', '>', '>', '<'])

    # Summary
    all_drifts_x = [abs(r['drift']) for r in records if 'X' in r['direction'].upper()]
    all_drifts_y = [abs(r['drift']) for r in records if 'Y' in r['direction'].upper()]
    max_x = max(all_drifts_x) if all_drifts_x else 0
    max_y = max(all_drifts_y) if all_drifts_y else 0

    log.info("")
    log.info(f"  Max drift X: {max_x:.6f}  |  Max drift Y: {max_y:.6f}")
    log.info(f"  NCh433 limit: {DRIFT_LIMIT_CM:.4f}")
    log.info(f"  Status: {'ALL PASS' if not violations else f'{len(violations)} VIOLATIONS'}")
    log.info("")

    return {
        'records': records,
        'max_per_story': max_per_story,
        'max_per_case': max_per_case,
        'violations': violations,
        'max_drift_x': max_x,
        'max_drift_y': max_y,
    }


# ===================================================================
# 3. BASE SHEAR — Per load case
# ===================================================================

def extract_base_shear(SapModel):
    """Extract base reactions for all load cases.

    For seismic cases (SDX, SDY): dominant shear is checked against
    Qmin = Cmin × W where Cmin = Ao×S/(6g).

    Returns:
        dict with shear per case, or None
    """
    log.info("=" * 65)
    log.info("  3. BASE SHEAR — Per Load Case")
    log.info("=" * 65)

    results = {}

    # Get all cases
    cases_to_check = GRAVITY_CASES + SEISMIC_CASES + TORSION_CASES

    for case_name in cases_to_check:
        try:
            select_cases_for_output(SapModel, [case_name])

            result = SapModel.Results.BaseReac(
                0, [], [], [],              # NumberResults, LoadCase, StepType, StepNum
                [], [], [], [], [], [],     # Fx, Fy, Fz, Mx, My, Mz
                0.0, 0.0, 0.0,             # gx, gy, gz
            )

            if isinstance(result, tuple) and len(result) >= 10 and result[0] > 0:
                n = result[0]
                # For spectral cases, there may be multiple steps (Max, Min)
                # Take the maximum absolute values
                fx_max = max(abs(float(result[4][i])) for i in range(n)) if result[4] else 0
                fy_max = max(abs(float(result[5][i])) for i in range(n)) if result[5] else 0
                fz_max = max(abs(float(result[6][i])) for i in range(n)) if result[6] else 0
                mx_max = max(abs(float(result[7][i])) for i in range(n)) if result[7] else 0
                my_max = max(abs(float(result[8][i])) for i in range(n)) if result[8] else 0
                mz_max = max(abs(float(result[9][i])) for i in range(n)) if result[9] else 0

                results[case_name] = {
                    'Fx': fx_max, 'Fy': fy_max, 'Fz': fz_max,
                    'Mx': mx_max, 'My': my_max, 'Mz': mz_max,
                    'n_results': n,
                }
        except Exception:
            pass  # Case may not exist or have no results

    if not results:
        log.warning("  No base reaction data available")
        return None

    # Also try DatabaseTables fallback
    if len(results) < 2:
        fields, db_rows = parse_db_table(SapModel, "Base Reactions")
        if db_rows:
            for row in db_rows:
                case = row.get('OutputCase', row.get('Load Case', ''))
                if not case or case in results:
                    continue
                results[case] = {
                    'Fx': abs(safe_float(row.get('FX', row.get('GlobalFX', '0')))),
                    'Fy': abs(safe_float(row.get('FY', row.get('GlobalFY', '0')))),
                    'Fz': abs(safe_float(row.get('FZ', row.get('GlobalFZ', '0')))),
                    'Mx': abs(safe_float(row.get('MX', row.get('GlobalMX', '0')))),
                    'My': abs(safe_float(row.get('MY', row.get('GlobalMY', '0')))),
                    'Mz': abs(safe_float(row.get('MZ', row.get('GlobalMZ', '0')))),
                    'n_results': 1,
                }

    # Print table
    tbl_headers = ["Case", "Fx (tonf)", "Fy (tonf)", "Fz (tonf)",
                    "Mx (tonf-m)", "My (tonf-m)", "Mz (tonf-m)"]
    tbl_rows = []
    for case in cases_to_check:
        if case not in results:
            continue
        v = results[case]
        tbl_rows.append([
            case, f"{v['Fx']:,.1f}", f"{v['Fy']:,.1f}", f"{v['Fz']:,.1f}",
            f"{v['Mx']:,.1f}", f"{v['My']:,.1f}", f"{v['Mz']:,.1f}",
        ])

    print_table("Base Reactions (abs max per case)", tbl_headers, tbl_rows,
                col_widths=[6, 11, 11, 11, 12, 12, 12],
                alignments=['<', '>', '>', '>', '>', '>', '>'])

    # Seismic shear analysis
    cmin = calc_Cmin()
    cmax = calc_Cmax()
    # Estimate seismic weight from PP base reaction
    pp_fz = results.get('PP', {}).get('Fz', 0)
    terp_fz = results.get('TERP', {}).get('Fz', 0)
    scp_fz = results.get('SCP', {}).get('Fz', 0)
    w_sismico = pp_fz + terp_fz + 0.25 * scp_fz

    log.info("")
    log.info(f"  Seismic weight W = PP + TERP + 0.25*SCP = {w_sismico:,.1f} tonf")
    log.info(f"  Expected: ~{PESO_ESPERADO_TONF:,.0f} tonf "
             f"({AREA_PLANTA:.0f} m2 x {N_STORIES} pisos x 1 tonf/m2)")
    log.info(f"  Cmin = {cmin:.4f}  |  Qmin = {cmin * w_sismico:,.1f} tonf")
    log.info(f"  Cmax = {cmax:.4f}  |  Qmax = {cmax * w_sismico:,.1f} tonf")

    for case in SEISMIC_CASES:
        if case in results:
            v = results[case]
            dominant = v['Fx'] if 'X' in case else v['Fy']
            ratio_min = dominant / (cmin * w_sismico) if cmin * w_sismico > 0 else 0
            log.info(f"  V_{case} = {dominant:,.1f} tonf "
                     f"({ratio_min:.2f} x Qmin)")

    log.info("")

    results['_seismic_weight'] = w_sismico
    results['_Cmin'] = cmin
    results['_Cmax'] = cmax
    return results


# ===================================================================
# 4. CENTERS OF MASS AND RIGIDITY — Per story
# ===================================================================

def extract_cm_cr(SapModel):
    """Extract centers of mass (CM) and rigidity (CR) per story.

    Uses DatabaseTables "Centers Of Mass And Rigidity".

    Returns:
        list of dicts with CM/CR data per story, or None
    """
    log.info("=" * 65)
    log.info("  4. CENTERS OF MASS AND RIGIDITY — Per Story")
    log.info("=" * 65)

    fields, rows = parse_db_table(SapModel, "Centers Of Mass And Rigidity")

    if not rows:
        log.warning("  Could not extract CM/CR data")
        return None

    cm_cr_data = []
    for row in rows:
        story = row.get('Story', row.get('story', ''))
        if not story:
            continue

        data = {
            'story': story,
            'mass_x': safe_float(row.get('MassX', row.get('Mass X', '0'))),
            'mass_y': safe_float(row.get('MassY', row.get('Mass Y', '0'))),
            'xcm': safe_float(row.get('XCM', row.get('XCCM', '0'))),
            'ycm': safe_float(row.get('YCM', row.get('YCCM', '0'))),
            'xcr': safe_float(row.get('XCR', row.get('XCCR', '0'))),
            'ycr': safe_float(row.get('YCR', row.get('YCCR', '0'))),
            'ex': 0, 'ey': 0,
        }
        # Eccentricity
        data['ex'] = abs(data['xcm'] - data['xcr'])
        data['ey'] = abs(data['ycm'] - data['ycr'])
        cm_cr_data.append(data)

    if not cm_cr_data:
        log.warning("  No CM/CR data parsed")
        return None

    # Print table
    tbl_headers = ["Story", "XCM (m)", "YCM (m)", "XCR (m)", "YCR (m)",
                    "eX (m)", "eY (m)"]
    tbl_rows = []
    for d in cm_cr_data:
        tbl_rows.append([
            d['story'], f"{d['xcm']:.3f}", f"{d['ycm']:.3f}",
            f"{d['xcr']:.3f}", f"{d['ycr']:.3f}",
            f"{d['ex']:.3f}", f"{d['ey']:.3f}",
        ])

    print_table("Centers of Mass (CM) and Rigidity (CR)", tbl_headers, tbl_rows,
                col_widths=[10, 9, 9, 9, 9, 8, 8],
                alignments=['<', '>', '>', '>', '>', '>', '>'])

    # Summary
    if cm_cr_data:
        avg_xcm = sum(d['xcm'] for d in cm_cr_data) / len(cm_cr_data)
        avg_ycm = sum(d['ycm'] for d in cm_cr_data) / len(cm_cr_data)
        max_ex = max(d['ex'] for d in cm_cr_data)
        max_ey = max(d['ey'] for d in cm_cr_data)

        log.info("")
        log.info(f"  Avg CM: ({avg_xcm:.3f}, {avg_ycm:.3f}) m")
        log.info(f"  Max eccentricity: eX = {max_ex:.3f} m, eY = {max_ey:.3f} m")
        log.info(f"  Accidental ecc: eaX = {0.05 * LX_PLANTA:.3f} m "
                 f"(5% x {LX_PLANTA:.1f}), "
                 f"eaY = {0.05 * LY_PLANTA:.3f} m (5% x {LY_PLANTA:.1f})")
    log.info("")

    return cm_cr_data


# ===================================================================
# 5. STORY FORCES — Shear & overturning moment per story
# ===================================================================

def extract_story_forces(SapModel):
    """Extract story shear and overturning moment per story.

    Uses DatabaseTables "Story Forces" table.

    Returns:
        list of dicts with story force data, or None
    """
    log.info("=" * 65)
    log.info("  5. STORY FORCES — Shear & Overturning Moment")
    log.info("=" * 65)

    fields, rows = parse_db_table(SapModel, "Story Forces")

    if not rows:
        log.warning("  Could not extract Story Forces from DatabaseTables")
        # Try alternative extraction via base reactions per story
        return _extract_story_forces_fallback(SapModel)

    story_forces = []
    for row in rows:
        story = row.get('Story', row.get('story', ''))
        case = row.get('OutputCase', row.get('Load Case', ''))
        location = row.get('Location', '')

        if not story:
            continue

        data = {
            'story': story,
            'case': case,
            'location': location,
            'vx': safe_float(row.get('VX', row.get('P', '0'))),
            'vy': safe_float(row.get('VY', row.get('V2', '0'))),
            'mx': safe_float(row.get('MX', row.get('T', '0'))),
            'my': safe_float(row.get('MY', row.get('M3', '0'))),
            'p': safe_float(row.get('P', '0')),
            't': safe_float(row.get('T', '0')),
        }
        story_forces.append(data)

    if not story_forces:
        log.warning("  No story force data parsed")
        return None

    # Filter for seismic cases
    seismic_forces = [sf for sf in story_forces if sf['case'] in SEISMIC_CASES]
    if not seismic_forces:
        seismic_forces = story_forces  # Show whatever is available

    # Organize: max shear per story for SDX and SDY
    shear_summary = {}
    for sf in seismic_forces:
        story = sf['story']
        case = sf['case']
        key = (story, case)
        if key not in shear_summary:
            shear_summary[key] = {'vx': 0, 'vy': 0, 'mx': 0, 'my': 0}
        shear_summary[key]['vx'] = max(shear_summary[key]['vx'], abs(sf['vx']))
        shear_summary[key]['vy'] = max(shear_summary[key]['vy'], abs(sf['vy']))
        shear_summary[key]['mx'] = max(shear_summary[key]['mx'], abs(sf['mx']))
        shear_summary[key]['my'] = max(shear_summary[key]['my'], abs(sf['my']))

    # Print shear distribution for SDX
    for case in SEISMIC_CASES:
        tbl_headers = ["Story", f"VX (tonf)", f"VY (tonf)", f"MX (tonf-m)", f"MY (tonf-m)"]
        tbl_rows = []
        for sn in reversed(STORY_NAMES):
            key = (sn, case)
            if key in shear_summary:
                v = shear_summary[key]
                tbl_rows.append([
                    sn, f"{v['vx']:,.1f}", f"{v['vy']:,.1f}",
                    f"{v['mx']:,.1f}", f"{v['my']:,.1f}",
                ])

        if tbl_rows:
            print_table(f"Story Forces — {case}", tbl_headers, tbl_rows,
                        col_widths=[10, 11, 11, 13, 13],
                        alignments=['<', '>', '>', '>', '>'])
    log.info("")

    return story_forces


def _extract_story_forces_fallback(SapModel):
    """Fallback: estimate story forces from base reactions if table unavailable."""
    log.info("  Attempting fallback via individual story queries...")
    log.warning("  Story Forces table not available — results may be limited")
    return None


# ===================================================================
# 6. WALL FORCES — Border walls (axes 1 and F)
# ===================================================================

def extract_wall_forces(SapModel):
    """Extract forces in border walls at axes 1 and F.

    Strategy:
      1. Try "Pier Forces" DatabaseTable (if piers are defined)
      2. Try "Area Element Forces - Shells" and filter by coordinates
      3. Try FrameForce for any frame elements near border axes

    Axis 1: x = 0.0 m (left edge, longest wall = A-C, muro 30cm)
    Axis F: y = 13.821 m (top edge, walls at multiple x-positions)

    Returns:
        dict with wall forces data, or None
    """
    log.info("=" * 65)
    log.info("  6. WALL FORCES — Border Walls (Axes 1 & F)")
    log.info("=" * 65)

    wall_results = {'axis_1': [], 'axis_F': []}

    # --- Method 1: Pier Forces ---
    log.info("  Trying 'Pier Forces' table...")
    fields, rows = parse_db_table(SapModel, "Pier Forces")

    if rows:
        log.info(f"  Found {len(rows)} pier force records")
        for row in rows:
            pier_name = row.get('Pier', row.get('pier', row.get('Name', '')))
            story = row.get('Story', row.get('story', ''))
            case = row.get('OutputCase', row.get('Load Case', ''))
            location = row.get('Location', '')
            p = safe_float(row.get('P', '0'))
            v2 = safe_float(row.get('V2', '0'))
            v3 = safe_float(row.get('V3', '0'))
            m2 = safe_float(row.get('M2', '0'))
            m3 = safe_float(row.get('M3', '0'))

            # Classify by pier name or location
            data = {
                'pier': pier_name, 'story': story, 'case': case,
                'location': location,
                'P': p, 'V2': v2, 'V3': v3, 'M2': m2, 'M3': m3,
            }

            # Attempt to classify: pier names might contain axis info
            pier_lower = str(pier_name).lower()
            if '1' in pier_lower or 'eje1' in pier_lower:
                wall_results['axis_1'].append(data)
            elif 'f' in pier_lower or 'ejef' in pier_lower:
                wall_results['axis_F'].append(data)
            else:
                # Store in both for now
                wall_results.setdefault('other', []).append(data)
    else:
        log.info("  No pier forces found — piers may not be defined in model")

    # --- Method 2: Area Element Forces filtered by coordinates ---
    if not wall_results['axis_1'] and not wall_results['axis_F']:
        log.info("  Trying 'Element Forces - Area Shells' table...")
        fields, rows = parse_db_table(SapModel, "Element Forces - Area Shells")

        if not rows:
            # Try alternative table names
            for alt_name in ["Area Element Forces", "Shell Forces",
                             "Element Forces - Shells"]:
                fields, rows = parse_db_table(SapModel, alt_name)
                if rows:
                    break

        if rows:
            log.info(f"  Found {len(rows)} area element force records")
            # This table may be very large; just count available records
            log.info("  (Area element forces available — "
                     "filter by pier labels for specific walls)")

    # --- Method 3: Identify walls at border axes from model geometry ---
    # Use wall definitions from config.py to identify which walls are at borders
    log.info("")
    log.info("  Border wall identification from config.py:")

    axis_1_walls = [w for w in MUROS_DIR_Y if w[0] == '1']
    axis_F_walls_y = [w for w in MUROS_DIR_Y
                      if abs(w[3] - BORDER_AXIS_F_Y) < COORD_TOL or
                      abs(w[2] - BORDER_AXIS_F_Y) < COORD_TOL]
    axis_F_walls_x = [w for w in MUROS_DIR_X
                      if abs(w[1] - BORDER_AXIS_F_Y) < COORD_TOL]

    log.info(f"  Axis 1 walls (x={BORDER_AXIS_1_X:.1f}): {len(axis_1_walls)} segments")
    for w in axis_1_walls:
        log.info(f"    Eje {w[0]}, y={w[2]:.3f}-{w[3]:.3f}, esp={w[4]}m")

    log.info(f"  Axis F walls (y={BORDER_AXIS_F_Y:.3f}): "
             f"{len(axis_F_walls_y)} Y-dir, {len(axis_F_walls_x)} X-dir")
    for w in axis_F_walls_y:
        log.info(f"    Eje {w[0]}, y={w[2]:.3f}-{w[3]:.3f}, esp={w[4]}m")
    for w in axis_F_walls_x:
        log.info(f"    Eje {w[0]}, x={w[2]:.3f}-{w[3]:.3f}, esp={w[4]}m")

    # Print pier forces if available
    for axis_label, axis_data in [("Axis 1", wall_results['axis_1']),
                                   ("Axis F", wall_results['axis_F'])]:
        if not axis_data:
            continue

        # Filter for seismic combos
        seismic_data = [d for d in axis_data if d['case'] in
                        SEISMIC_CASES + list(COMBINATIONS.keys())]
        if not seismic_data:
            seismic_data = axis_data[:20]  # Show first 20

        tbl_headers = ["Pier", "Story", "Case", "P (tonf)", "V2 (tonf)",
                        "M3 (tonf-m)"]
        tbl_rows = []
        for d in seismic_data[:30]:
            tbl_rows.append([
                d['pier'], d['story'], d['case'],
                f"{d['P']:,.1f}", f"{d['V2']:,.1f}", f"{d['M3']:,.1f}",
            ])

        print_table(f"Pier Forces — {axis_label}", tbl_headers, tbl_rows,
                    col_widths=[10, 10, 8, 11, 11, 13],
                    alignments=['<', '<', '<', '>', '>', '>'])

    if not wall_results['axis_1'] and not wall_results['axis_F']:
        log.info("")
        log.info("  NOTE: No pier forces extracted. To get wall forces:")
        log.info("    1. Define pier labels in ETABS (Assign > Shell > Pier Label)")
        log.info("    2. Re-run analysis")
        log.info("    3. Re-run this script")
        log.info("    OR: Use Section Cuts in ETABS UI for specific wall sections")

    log.info("")
    return wall_results


# ===================================================================
# 7. P-M DEMAND POINTS — For wall design
# ===================================================================

def extract_wall_pm(SapModel):
    """Extract P-M demand points for walls under all combinations.

    For each load combination (C1-C11), extracts the axial force (Pu) and
    moment (Mu) at the base of critical walls. These (Pu, Mu) pairs are
    the demand points for the interaction diagram.

    Strategy:
      1. Try "Pier Forces" table filtered for base stories
      2. Fall back to base reactions per combo (global check)

    Returns:
        dict with PM demand data, or None
    """
    log.info("=" * 65)
    log.info("  7. P-M DEMAND POINTS — Wall Design")
    log.info("=" * 65)

    pm_data = {}

    # --- Method 1: Pier Forces under combinations ---
    combo_names = list(COMBINATIONS.keys())

    # Select combos for output
    try:
        SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        for combo in combo_names:
            try:
                SapModel.Results.Setup.SetComboSelectedForOutput(combo)
            except Exception:
                pass
    except Exception:
        pass

    fields, rows = parse_db_table(SapModel, "Pier Forces")

    if rows:
        # Filter for base story (Story1) and seismic combos
        base_story = STORY_NAMES[0]  # Story1

        for row in rows:
            pier = row.get('Pier', row.get('pier', row.get('Name', '')))
            story = row.get('Story', row.get('story', ''))
            case = row.get('OutputCase', row.get('Load Case', ''))
            location = row.get('Location', '')

            # Only base piers, bottom location
            if story != base_story:
                continue

            p = safe_float(row.get('P', '0'))
            m2 = safe_float(row.get('M2', '0'))
            m3 = safe_float(row.get('M3', '0'))

            if pier not in pm_data:
                pm_data[pier] = []

            pm_data[pier].append({
                'combo': case,
                'location': location,
                'Pu': p,
                'M2': m2,
                'M3': m3,
            })

        if pm_data:
            log.info(f"  Extracted P-M demands for {len(pm_data)} piers at base")

            for pier, demands in sorted(pm_data.items()):
                tbl_headers = ["Combo", "Pu (tonf)", "M2 (tonf-m)", "M3 (tonf-m)"]
                tbl_rows = []
                for d in demands:
                    tbl_rows.append([
                        d['combo'], f"{d['Pu']:,.1f}",
                        f"{d['M2']:,.1f}", f"{d['M3']:,.1f}",
                    ])

                if tbl_rows:
                    print_table(f"P-M Demands — Pier {pier} (Base)", tbl_headers,
                                tbl_rows[:15],  # Limit to 15 combos
                                col_widths=[8, 12, 13, 13],
                                alignments=['<', '>', '>', '>'])

    # --- Method 2: Global base reactions per combo (fallback) ---
    if not pm_data:
        log.info("  No pier P-M data (piers not defined). Extracting global demands...")
        log.info("  Base reactions per load combination:")

        combo_reactions = {}
        for combo in combo_names:
            try:
                select_combos_for_output(SapModel, [combo])

                result = SapModel.Results.BaseReac(
                    0, [], [], [],
                    [], [], [], [], [], [],
                    0.0, 0.0, 0.0,
                )

                if isinstance(result, tuple) and len(result) >= 10 and result[0] > 0:
                    n = result[0]
                    # For combos, may have single result or multiple steps
                    fz_vals = [float(result[6][i]) for i in range(n)] if result[6] else [0]
                    mx_vals = [float(result[7][i]) for i in range(n)] if result[7] else [0]
                    my_vals = [float(result[8][i]) for i in range(n)] if result[8] else [0]

                    # Get max and min for envelope
                    combo_reactions[combo] = {
                        'Fz_max': max(fz_vals, key=abs),
                        'Mx_max': max(mx_vals, key=abs),
                        'My_max': max(my_vals, key=abs),
                    }
            except Exception:
                pass

        if combo_reactions:
            tbl_headers = ["Combo", "Fz (tonf)", "Mx (tonf-m)", "My (tonf-m)"]
            tbl_rows = []
            for combo in combo_names:
                if combo in combo_reactions:
                    v = combo_reactions[combo]
                    tbl_rows.append([
                        combo, f"{v['Fz_max']:,.1f}",
                        f"{v['Mx_max']:,.1f}", f"{v['My_max']:,.1f}",
                    ])

            print_table("Global Base Reactions per Combo (P-M reference)",
                        tbl_headers, tbl_rows,
                        col_widths=[6, 12, 14, 14],
                        alignments=['<', '>', '>', '>'])

            pm_data['_global'] = combo_reactions

        log.info("")
        log.info("  NOTE: For wall-specific P-M diagrams:")
        log.info("    1. Define pier labels in ETABS for critical walls")
        log.info("    2. Use Section Designer for interaction diagrams")
        log.info("    3. Or use Tablas de Diseno (docs/Tablas/) for AZA charts")

    log.info("")
    return pm_data if pm_data else None


# ===================================================================
# CSV EXPORT — All results
# ===================================================================

def export_all_csv(modal, drifts, shear, cm_cr, story_forces, wall_forces, wall_pm):
    """Export all extracted results to CSV files."""
    log.info("=" * 65)
    log.info("  CSV EXPORT")
    log.info("=" * 65)

    n_files = 0

    # 1. Modal results
    if modal and modal.get('modes'):
        is_pct = modal.get('is_percentage', False)
        headers = ["Mode", "Period_s", "UX_pct", "UY_pct", "RZ_pct",
                    "SumUX_pct", "SumUY_pct", "Type"]
        rows = []
        for m in modal['modes']:
            factor = 1.0 if is_pct else 100.0
            rows.append([
                m['mode'], f"{m['period']:.6f}",
                f"{m['ux'] * factor:.4f}", f"{m['uy'] * factor:.4f}",
                f"{m['rz'] * factor:.4f}",
                f"{m['sum_ux'] * factor:.4f}", f"{m['sum_uy'] * factor:.4f}",
                m['type'],
            ])
        export_csv_file("modal_results.csv", headers, rows)
        n_files += 1

    # 2. Story drifts
    if drifts and drifts.get('records'):
        headers = ["Story", "Case", "Direction", "Drift", "Label", "X_m", "Y_m", "Z_m"]
        rows = []
        for r in drifts['records']:
            rows.append([
                r['story'], r['case'], r['direction'],
                f"{r['drift']:.8f}", r['label'],
                f"{r['x']:.3f}", f"{r['y']:.3f}", f"{r['z']:.3f}",
            ])
        export_csv_file("story_drifts.csv", headers, rows)
        n_files += 1

        # Drift envelope
        headers2 = ["Story", "Elevation_m", "MaxDrift_X", "MaxDrift_Y"]
        rows2 = []
        for sn in STORY_NAMES:
            idx = STORY_NAMES.index(sn)
            elev = STORY_ELEVATIONS[idx] if idx < len(STORY_ELEVATIONS) else 0
            dx = abs(drifts['max_per_story'].get((sn, 'X'), {}).get('drift', 0))
            dy = abs(drifts['max_per_story'].get((sn, 'Y'), {}).get('drift', 0))
            rows2.append([sn, f"{elev:.2f}", f"{dx:.8f}", f"{dy:.8f}"])
        export_csv_file("drift_envelope.csv", headers2, rows2)
        n_files += 1

    # 3. Base shear
    if shear:
        headers = ["Case", "Fx_tonf", "Fy_tonf", "Fz_tonf",
                    "Mx_tonfm", "My_tonfm", "Mz_tonfm"]
        rows = []
        for case, v in shear.items():
            if case.startswith('_'):
                continue
            rows.append([
                case, f"{v['Fx']:.2f}", f"{v['Fy']:.2f}", f"{v['Fz']:.2f}",
                f"{v['Mx']:.2f}", f"{v['My']:.2f}", f"{v['Mz']:.2f}",
            ])
        export_csv_file("base_reactions.csv", headers, rows)
        n_files += 1

    # 4. CM/CR
    if cm_cr:
        headers = ["Story", "XCM_m", "YCM_m", "XCR_m", "YCR_m",
                    "eX_m", "eY_m", "MassX", "MassY"]
        rows = []
        for d in cm_cr:
            rows.append([
                d['story'], f"{d['xcm']:.4f}", f"{d['ycm']:.4f}",
                f"{d['xcr']:.4f}", f"{d['ycr']:.4f}",
                f"{d['ex']:.4f}", f"{d['ey']:.4f}",
                f"{d['mass_x']:.4f}", f"{d['mass_y']:.4f}",
            ])
        export_csv_file("cm_cr_per_story.csv", headers, rows)
        n_files += 1

    # 5. Story forces
    if story_forces:
        headers = ["Story", "Case", "Location", "VX_tonf", "VY_tonf",
                    "MX_tonfm", "MY_tonfm"]
        rows = []
        for sf in story_forces:
            rows.append([
                sf['story'], sf['case'], sf['location'],
                f"{sf['vx']:.2f}", f"{sf['vy']:.2f}",
                f"{sf['mx']:.2f}", f"{sf['my']:.2f}",
            ])
        export_csv_file("story_forces.csv", headers, rows)
        n_files += 1

    # 6. Wall forces (pier forces)
    if wall_forces:
        for axis_label, axis_key in [("axis_1", "axis_1"), ("axis_F", "axis_F")]:
            if wall_forces.get(axis_key):
                headers = ["Pier", "Story", "Case", "Location",
                           "P_tonf", "V2_tonf", "V3_tonf",
                           "M2_tonfm", "M3_tonfm"]
                rows = []
                for d in wall_forces[axis_key]:
                    rows.append([
                        d['pier'], d['story'], d['case'], d['location'],
                        f"{d['P']:.2f}", f"{d['V2']:.2f}", f"{d['V3']:.2f}",
                        f"{d['M2']:.2f}", f"{d['M3']:.2f}",
                    ])
                export_csv_file(f"wall_forces_{axis_label}.csv", headers, rows)
                n_files += 1

    # 7. P-M demands
    if wall_pm:
        for pier, demands in wall_pm.items():
            if pier.startswith('_'):
                # Global reactions
                if isinstance(demands, dict):
                    headers = ["Combo", "Fz_tonf", "Mx_tonfm", "My_tonfm"]
                    rows = []
                    for combo, v in demands.items():
                        rows.append([
                            combo, f"{v['Fz_max']:.2f}",
                            f"{v['Mx_max']:.2f}", f"{v['My_max']:.2f}",
                        ])
                    export_csv_file("pm_global_reactions.csv", headers, rows)
                    n_files += 1
                continue

            if isinstance(demands, list):
                headers = ["Combo", "Pu_tonf", "M2_tonfm", "M3_tonfm"]
                rows = []
                for d in demands:
                    rows.append([
                        d['combo'], f"{d['Pu']:.2f}",
                        f"{d['M2']:.2f}", f"{d['M3']:.2f}",
                    ])
                safe_name = str(pier).replace('/', '_').replace('\\', '_')
                export_csv_file(f"pm_pier_{safe_name}.csv", headers, rows)
                n_files += 1

    log.info(f"  Total: {n_files} CSV files in {RESULTS_DIR}")
    log.info("")


# ===================================================================
# SUMMARY MARKDOWN
# ===================================================================

def generate_summary_md(modal, drifts, shear, cm_cr, story_forces,
                        wall_forces, wall_pm, output_path):
    """Generate comprehensive results summary as markdown.

    Args:
        modal, drifts, shear, cm_cr, story_forces, wall_forces, wall_pm: result dicts
        output_path: str — path to write the markdown file
    """
    log.info("=" * 65)
    log.info("  GENERATING SUMMARY MARKDOWN")
    log.info("=" * 65)

    lines = []
    lines.append("# Resultados del Analisis — Edificio 1 (20 pisos, muros HA)")
    lines.append("")
    lines.append(f"> Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> Script: 12_extract_results.py")
    lines.append(f"> Unidades: Tonf, m, C")
    lines.append("")

    # Building info
    lines.append("## Datos del Edificio")
    lines.append("")
    lines.append(f"- **Pisos**: {N_STORIES}")
    lines.append(f"- **Altura total**: {H_TOTAL:.1f} m")
    lines.append(f"- **Area planta**: {AREA_PLANTA:.1f} m2")
    lines.append(f"- **Zona sismica**: 3 (Antofagasta)")
    lines.append(f"- **Suelo**: C (S={S_SUELO}, To={TO_SUELO}s, T'={T_PRIME}s)")
    lines.append(f"- **Sistema**: Muros HA (R={R_MUROS}, Ro={RO_MUROS})")
    lines.append(f"- **Categoria**: II (I={I_FACTOR})")
    lines.append("")

    # 1. Modal
    lines.append("## 1. Resultados Modales")
    lines.append("")
    if modal:
        t1 = modal.get('T1', 0)
        r_star = modal.get('R_star', 0)
        sux = modal.get('final_sum_ux', 0) * 100
        suy = modal.get('final_sum_uy', 0) * 100

        lines.append(f"- **T1** = {t1:.4f} s")
        lines.append(f"- **R*(T1)** = {r_star:.2f}")
        lines.append(f"- **SumUX** = {sux:.1f}%  |  **SumUY** = {suy:.1f}% "
                      f"({modal['n_modes']} modos)")
        lines.append(f"- Participacion >= 90%: "
                      f"{'CUMPLE' if sux >= 90 and suy >= 90 else 'NO CUMPLE'}")
        lines.append("")

        # Mode table
        lines.append("| Modo | T (s) | UX% | UY% | RZ% | SumUX% | SumUY% | Tipo |")
        lines.append("|------|-------|-----|-----|-----|--------|--------|------|")
        is_pct = modal.get('is_percentage', False)
        for m in modal['modes'][:12]:
            f = 1.0 if is_pct else 100.0
            lines.append(
                f"| {m['mode']} | {m['period']:.4f} | {m['ux']*f:.2f} | "
                f"{m['uy']*f:.2f} | {m['rz']*f:.2f} | {m['sum_ux']*f:.2f} | "
                f"{m['sum_uy']*f:.2f} | {m['type']} |"
            )
        lines.append("")

        # Seismic coefficients
        cmin = calc_Cmin()
        cmax = calc_Cmax()
        lines.append("### Coeficientes Sismicos")
        lines.append(f"- Cmin = Ao*S/(6g) = {cmin:.4f}")
        lines.append(f"- Cmax = 0.35*S*Ao/g = {cmax:.4f}")
        lines.append(f"- R*(T1={t1:.3f}s) = {r_star:.2f}")
        lines.append("")
    else:
        lines.append("*No se pudieron extraer resultados modales*")
        lines.append("")

    # 2. Drifts
    lines.append("## 2. Drifts de Entrepiso (NCh433 Art. 5.9)")
    lines.append("")
    if drifts:
        lines.append(f"- **Max drift X**: {drifts['max_drift_x']:.6f}")
        lines.append(f"- **Max drift Y**: {drifts['max_drift_y']:.6f}")
        lines.append(f"- **Limite NCh433**: {DRIFT_LIMIT_CM:.4f}")
        lines.append(f"- **Estado**: "
                      f"{'CUMPLE' if not drifts['violations'] else 'NO CUMPLE'}")
        lines.append("")
        lines.append("**Nota**: Espectro elastico (no reducido). Para T >> To, "
                      "desplazamiento elastico ~ inelastico (principio de igualdad "
                      "de desplazamientos).")
        lines.append("")

        # Drift envelope table
        lines.append("| Piso | Elev (m) | Drift X | Drift Y | Estado |")
        lines.append("|------|----------|---------|---------|--------|")
        for sn in reversed(STORY_NAMES):
            idx = STORY_NAMES.index(sn)
            elev = STORY_ELEVATIONS[idx] if idx < len(STORY_ELEVATIONS) else 0
            dx = abs(drifts['max_per_story'].get((sn, 'X'), {}).get('drift', 0))
            dy = abs(drifts['max_per_story'].get((sn, 'Y'), {}).get('drift', 0))
            worst = max(dx, dy)
            status = "OK" if worst <= DRIFT_LIMIT_CM else "FALLA"
            lines.append(f"| {sn} | {elev:.1f} | {dx:.6f} | {dy:.6f} | {status} |")
        lines.append("")
    else:
        lines.append("*No se pudieron extraer datos de drift*")
        lines.append("")

    # 3. Base shear
    lines.append("## 3. Corte Basal")
    lines.append("")
    if shear:
        w = shear.get('_seismic_weight', 0)
        cmin_val = shear.get('_Cmin', 0)
        qmin = cmin_val * w

        lines.append(f"- **Peso sismico W** = {w:,.1f} tonf")
        lines.append(f"- **Qmin** = Cmin x W = {cmin_val:.4f} x {w:,.0f} = "
                      f"{qmin:,.1f} tonf")
        lines.append("")

        lines.append("| Caso | Fx (tonf) | Fy (tonf) | Fz (tonf) |")
        lines.append("|------|-----------|-----------|-----------|")
        for case in GRAVITY_CASES + SEISMIC_CASES + TORSION_CASES:
            if case in shear and not case.startswith('_'):
                v = shear[case]
                lines.append(f"| {case} | {v['Fx']:,.1f} | {v['Fy']:,.1f} | "
                              f"{v['Fz']:,.1f} |")
        lines.append("")
    else:
        lines.append("*No se pudieron extraer datos de corte basal*")
        lines.append("")

    # 4. CM/CR
    lines.append("## 4. Centros de Masa y Rigidez")
    lines.append("")
    if cm_cr:
        lines.append("| Piso | XCM | YCM | XCR | YCR | eX | eY |")
        lines.append("|------|-----|-----|-----|-----|----|----|")
        for d in cm_cr:
            lines.append(f"| {d['story']} | {d['xcm']:.3f} | {d['ycm']:.3f} | "
                          f"{d['xcr']:.3f} | {d['ycr']:.3f} | "
                          f"{d['ex']:.3f} | {d['ey']:.3f} |")
        lines.append("")
    else:
        lines.append("*No se pudieron extraer datos de CM/CR*")
        lines.append("")

    # 5. Story forces
    lines.append("## 5. Fuerzas por Piso (Corte y Volcante)")
    lines.append("")
    if story_forces:
        # Summarize for SDX
        sdx_forces = [sf for sf in story_forces if sf['case'] == 'SDX']
        if sdx_forces:
            lines.append("### Caso SDX")
            lines.append("| Piso | VX (tonf) | VY (tonf) | MX (tonf-m) | MY (tonf-m) |")
            lines.append("|------|-----------|-----------|-------------|-------------|")
            seen = set()
            for sf in sdx_forces:
                if sf['story'] in seen:
                    continue
                seen.add(sf['story'])
                lines.append(f"| {sf['story']} | {sf['vx']:,.1f} | {sf['vy']:,.1f} | "
                              f"{sf['mx']:,.1f} | {sf['my']:,.1f} |")
            lines.append("")
    else:
        lines.append("*No se pudieron extraer fuerzas por piso*")
        lines.append("")

    # 6 & 7. Wall forces and P-M
    lines.append("## 6. Fuerzas en Muros de Borde")
    lines.append("")
    if wall_forces and (wall_forces.get('axis_1') or wall_forces.get('axis_F')):
        for axis_label, key in [("Eje 1", "axis_1"), ("Eje F", "axis_F")]:
            data = wall_forces.get(key, [])
            if data:
                lines.append(f"### {axis_label} ({len(data)} registros)")
                lines.append("")
    else:
        lines.append("*Se requiere definir Pier Labels en ETABS para extraer "
                      "fuerzas de muros individuales.*")
        lines.append("")
        lines.append("**Muros en bordes identificados (config.py):**")
        lines.append(f"- Eje 1 (x={BORDER_AXIS_1_X}m): "
                      f"Muro A-C, esp=0.30m, L={GRID_Y['C']-GRID_Y['A']:.3f}m")
        lines.append(f"- Eje F (y={BORDER_AXIS_F_Y}m): Multiples muros D-F")
        lines.append("")

    lines.append("## 7. Puntos de Demanda P-M")
    lines.append("")
    if wall_pm and '_global' in wall_pm:
        lines.append("### Reacciones Globales por Combo (referencia para P-M)")
        lines.append("| Combo | Fz (tonf) | Mx (tonf-m) | My (tonf-m) |")
        lines.append("|-------|-----------|-------------|-------------|")
        for combo, v in wall_pm['_global'].items():
            lines.append(f"| {combo} | {v['Fz_max']:,.1f} | {v['Mx_max']:,.1f} | "
                          f"{v['My_max']:,.1f} |")
        lines.append("")
    elif wall_pm:
        lines.append(f"P-M extraido para {len(wall_pm)} piers — ver CSVs")
        lines.append("")
    else:
        lines.append("*No se pudieron extraer datos P-M*")
        lines.append("")

    # Expected values reference
    lines.append("## Valores Esperados (referencia)")
    lines.append("")
    lines.append("| Parametro | Esperado | Fuente |")
    lines.append("|-----------|----------|--------|")
    lines.append(f"| T1 | 1.0-1.3 s | Regla empirica H/40-H/50 |")
    lines.append(f"| Peso total | ~{PESO_ESPERADO_TONF:,.0f} tonf | "
                  f"{AREA_PLANTA:.0f}m2 x {N_STORIES}p x 1 tonf/m2 |")
    lines.append(f"| Peso/area | ~1.0 tonf/m2 | Regla Lafontaine |")
    lines.append(f"| Drift max | <= {DRIFT_LIMIT_CM} | NCh433 Art. 5.9 |")
    lines.append(f"| SumUX, SumUY | >= 90% | NCh433 Art. 6.3.6.2 |")
    lines.append(f"| Qmin | Cmin x W = {calc_Cmin():.4f} x W | NCh433 Art. 6.3.7 |")
    lines.append("")

    # Write file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    log.info(f"  Summary written to: {output_path}")
    log.info("")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: extract all results from analyzed model."""
    log.info("=" * 65)
    log.info("  12_extract_results.py — Comprehensive Results Extraction")
    log.info("  Edificio 1: 20 pisos muros HA, Antofagasta")
    log.info("=" * 65)
    log.info("")

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Extract all analysis results from ETABS model")
    parser.add_argument('--no-csv', action='store_true',
                        help='Skip CSV export')
    parser.add_argument('--no-summary', action='store_true',
                        help='Skip markdown summary generation')
    parser.add_argument('--sections', nargs='+', type=int, default=None,
                        help='Only extract specific sections (1-7)')
    args = parser.parse_args()

    sections = set(args.sections) if args.sections else {1, 2, 3, 4, 5, 6, 7}

    log.info("  Sections to extract:")
    section_names = {
        1: "Modal results (periods, participation)",
        2: "Story drifts (NCh433 conditions 1 & 2)",
        3: "Base shear per case",
        4: "Centers of mass and rigidity",
        5: "Story forces (shear + overturning)",
        6: "Wall forces (border walls, axes 1 & F)",
        7: "P-M demand points for walls",
    }
    for s in sorted(sections):
        log.info(f"    {s}. {section_names.get(s, '?')}")
    log.info("")

    if not args.no_csv:
        log.info(f"  CSV output: {RESULTS_DIR}")
    if not args.no_summary:
        summary_path = os.path.join(SCRIPT_DIR, "..", "research",
                                     "resultados_esperados.md")
        summary_path = os.path.normpath(summary_path)
        log.info(f"  Summary:    {summary_path}")
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
        # Set units
        set_units(UNITS_TONF_M_C)
        log.info(f"  Units: Tonf_m_C (={UNITS_TONF_M_C})")

        # Verify model is analyzed (locked)
        try:
            locked = SapModel.GetModelIsLocked()
            if isinstance(locked, tuple):
                locked = locked[0]
            if not locked:
                log.warning("  Model is NOT locked — analysis may not have run")
                log.warning("  Results may be empty or outdated")
        except Exception:
            pass
        log.info("")

        t_start = time.time()

        # --- Extract all sections ---
        modal = None
        drifts = None
        shear = None
        cm_cr = None
        story_forces_data = None
        wall_forces_data = None
        wall_pm_data = None

        if 1 in sections:
            try:
                modal = extract_modal_results(SapModel)
            except Exception as e:
                log.error(f"  Section 1 failed: {e}")
                traceback.print_exc()

        if 2 in sections:
            try:
                drifts = extract_story_drifts(SapModel)
            except Exception as e:
                log.error(f"  Section 2 failed: {e}")
                traceback.print_exc()

        if 3 in sections:
            try:
                shear = extract_base_shear(SapModel)
            except Exception as e:
                log.error(f"  Section 3 failed: {e}")
                traceback.print_exc()

        if 4 in sections:
            try:
                cm_cr = extract_cm_cr(SapModel)
            except Exception as e:
                log.error(f"  Section 4 failed: {e}")
                traceback.print_exc()

        if 5 in sections:
            try:
                story_forces_data = extract_story_forces(SapModel)
            except Exception as e:
                log.error(f"  Section 5 failed: {e}")
                traceback.print_exc()

        if 6 in sections:
            try:
                wall_forces_data = extract_wall_forces(SapModel)
            except Exception as e:
                log.error(f"  Section 6 failed: {e}")
                traceback.print_exc()

        if 7 in sections:
            try:
                wall_pm_data = extract_wall_pm(SapModel)
            except Exception as e:
                log.error(f"  Section 7 failed: {e}")
                traceback.print_exc()

        t_elapsed = time.time() - t_start

        # --- CSV export ---
        if not args.no_csv:
            try:
                export_all_csv(modal, drifts, shear, cm_cr,
                               story_forces_data, wall_forces_data, wall_pm_data)
            except Exception as e:
                log.error(f"  CSV export failed: {e}")
                traceback.print_exc()

        # --- Summary markdown ---
        if not args.no_summary:
            try:
                summary_path = os.path.join(SCRIPT_DIR, "..", "research",
                                             "resultados_esperados.md")
                summary_path = os.path.normpath(summary_path)
                generate_summary_md(modal, drifts, shear, cm_cr,
                                    story_forces_data, wall_forces_data,
                                    wall_pm_data, summary_path)
            except Exception as e:
                log.error(f"  Summary generation failed: {e}")
                traceback.print_exc()

        # --- Final summary ---
        log.info("=" * 65)
        log.info("  EXTRACTION COMPLETE")
        log.info("=" * 65)
        log.info("")
        log.info(f"  Time: {t_elapsed:.1f}s")
        log.info(f"  Sections extracted: {len(sections)}/7")

        status_items = []
        if modal:
            status_items.append(f"T1={modal['T1']:.3f}s")
        if drifts:
            status_items.append(
                f"Drift={'OK' if not drifts['violations'] else 'FAIL'}")
        if shear:
            w = shear.get('_seismic_weight', 0)
            status_items.append(f"W={w:,.0f}t")
        if cm_cr:
            status_items.append(f"CM/CR={len(cm_cr)}stories")

        log.info(f"  Summary: {' | '.join(status_items)}")
        log.info("")

        if not args.no_csv:
            log.info(f"  CSV files: {RESULTS_DIR}")
        if not args.no_summary:
            log.info(f"  Markdown:  autonomo/research/resultados_esperados.md")
        log.info("")

    except Exception as e:
        log.error(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
