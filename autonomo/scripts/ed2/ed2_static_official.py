"""
ed2_static_official.py - Canon operativo Ed.2 Parte 1 (metodo estatico).

Este modulo centraliza la logica oficial del flujo Ed.2 Parte 1 para que
guia UI, pipeline API, verificacion y generacion de entregables compartan
la misma base:

- Casos oficiales: Modal, EX, EY, TEX, TEY
- Combinaciones oficiales: C1-C7 con variantes explicitas +/- torsion
- Formulas NCh433/DS61 del metodo estatico
- Story weights y distribucion estatica por piso
- IO de archivos CSV/JSON del paquete `results/`

No depende de resultados sinteticos. Si faltan datos reales del modelo,
los consumidores deben fallar de forma clara.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import unicodedata
from typing import Dict, Iterable, List, Optional, Tuple

from config_ed2 import (
    AO_G,
    AREA_PLANTA,
    EA_STATIC_X,
    EA_STATIC_Y,
    G_ACCEL,
    GRID_X,
    GRID_Y,
    H_TOTAL,
    I_FACTOR,
    N_STORIES,
    S_SUELO,
    STORY_ELEVATIONS,
    STORY_HEIGHTS,
    STORY_NAMES,
    T_PRIME,
    N_SUELO,
    LOADS_AREA,
    RESULTS_DIR,
    INFORME_DIR,
    RUNTIME_ROOT,
    calc_C,
    calc_Cmax,
    calc_Cmin,
)

MODAL_CASE = "Modal"
EX_CASE = "EX"
EY_CASE = "EY"
TEX_CASE = "TEX"
TEY_CASE = "TEY"

SEISMIC_CASES = [EX_CASE, EY_CASE]
TORSION_CASES = [TEX_CASE, TEY_CASE]
OFFICIAL_CASES = [MODAL_CASE] + SEISMIC_CASES + TORSION_CASES
GRAVITY_CASES = ["PP", "TERP", "TERT", "SCP", "SCT"]

# Combinaciones oficiales del enunciado. Se expanden los sismicos para dejar
# explicitos el signo del sismo principal y el signo de la torsion accidental.
OFFICIAL_COMBINATIONS = {
    "C1": [(1.4, "PP"), (1.4, "TERP"), (1.4, "TERT")],
    "C2": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.6, "SCP"), (0.5, "SCT")],
    "C3": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (1.6, "SCT")],
    "C4_XP_TP": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (1.4, EX_CASE), (1.4, TEX_CASE)],
    "C4_XP_TN": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (1.4, EX_CASE), (-1.4, TEX_CASE)],
    "C4_XN_TP": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (-1.4, EX_CASE), (1.4, TEX_CASE)],
    "C4_XN_TN": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (-1.4, EX_CASE), (-1.4, TEX_CASE)],
    "C5_XP_TP": [(0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"), (1.4, EX_CASE), (1.4, TEX_CASE)],
    "C5_XP_TN": [(0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"), (1.4, EX_CASE), (-1.4, TEX_CASE)],
    "C5_XN_TP": [(0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"), (-1.4, EX_CASE), (1.4, TEX_CASE)],
    "C5_XN_TN": [(0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"), (-1.4, EX_CASE), (-1.4, TEX_CASE)],
    "C6_YP_TP": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (1.4, EY_CASE), (1.4, TEY_CASE)],
    "C6_YP_TN": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (1.4, EY_CASE), (-1.4, TEY_CASE)],
    "C6_YN_TP": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (-1.4, EY_CASE), (1.4, TEY_CASE)],
    "C6_YN_TN": [(1.2, "PP"), (1.2, "TERP"), (1.2, "TERT"), (1.0, "SCP"), (-1.4, EY_CASE), (-1.4, TEY_CASE)],
    "C7_YP_TP": [(0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"), (1.4, EY_CASE), (1.4, TEY_CASE)],
    "C7_YP_TN": [(0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"), (1.4, EY_CASE), (-1.4, TEY_CASE)],
    "C7_YN_TP": [(0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"), (-1.4, EY_CASE), (1.4, TEY_CASE)],
    "C7_YN_TN": [(0.9, "PP"), (0.9, "TERP"), (0.9, "TERT"), (-1.4, EY_CASE), (-1.4, TEY_CASE)],
}

# Combinaciones de servicio para drift: sismo principal +/- torsion accidental,
# sin factores LRFD, para revisar deformaciones por accion sismica con torsion.
OFFICIAL_DRIFT_COMBINATIONS = {
    "DRIFT_XP_TP": [(1.0, EX_CASE), (1.0, TEX_CASE)],
    "DRIFT_XP_TN": [(1.0, EX_CASE), (-1.0, TEX_CASE)],
    "DRIFT_XN_TP": [(-1.0, EX_CASE), (1.0, TEX_CASE)],
    "DRIFT_XN_TN": [(-1.0, EX_CASE), (-1.0, TEX_CASE)],
    "DRIFT_YP_TP": [(1.0, EY_CASE), (1.0, TEY_CASE)],
    "DRIFT_YP_TN": [(1.0, EY_CASE), (-1.0, TEY_CASE)],
    "DRIFT_YN_TP": [(-1.0, EY_CASE), (1.0, TEY_CASE)],
    "DRIFT_YN_TN": [(-1.0, EY_CASE), (-1.0, TEY_CASE)],
}

REQUIRED_RESULT_FILES = [
    "ed2_modal_seed.json",
    "ed2_modal_results.csv",
    "ed2_story_weights.csv",
    "ed2_story_weights_source.json",
    "ed2_static_seed.json",
    "ed2_torsion_application.json",
    "ed2_analysis_run.json",
    "ed2_story_drifts.csv",
    "ed2_drift_envelope.csv",
    "ed2_drift_service_summary.csv",
    "ed2_base_reactions.csv",
    "ed2_cm_cr_per_story.csv",
    "ed2_story_forces.csv",
    "ed2_story_forces_summary.csv",
    "ed2_static_distribution.csv",
    "ed2_summary.csv",
    "ed2_summary.json",
]


def ensure_results_dir() -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    return RESULTS_DIR


def ensure_informe_dir() -> str:
    os.makedirs(INFORME_DIR, exist_ok=True)
    return INFORME_DIR


def ensure_transfer_dir() -> str:
    path = os.path.join(RUNTIME_ROOT, "transfer")
    os.makedirs(path, exist_ok=True)
    return path


def safe_float(value, default=0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip().replace("%", "").replace(" ", "")
        if not text:
            return default
        text = text.replace(",", ".")
        return float(text)
    except (TypeError, ValueError):
        return default


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def write_csv(filename: str, headers: List[str], rows: Iterable[Iterable]) -> str:
    ensure_results_dir()
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(list(row))
    return path


def read_csv(filename: str) -> Tuple[List[str], List[Dict[str, str]]]:
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = [dict(row) for row in reader]
        return list(reader.fieldnames or []), rows


def write_json(filename: str, data) -> str:
    ensure_results_dir()
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
    return path


def read_json(filename: str):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_db_table(SapModel, table_key: str, group: str = "All") -> Tuple[Optional[List[str]], Optional[List[Dict[str, str]]]]:
    """Parse DatabaseTables.GetTableForDisplayArray with a tolerant strategy."""
    groups_to_try = []
    for candidate in [group, "", "All"]:
        if candidate not in groups_to_try:
            groups_to_try.append(candidate)

    result = None
    for current_group in groups_to_try:
        try:
            trial = SapModel.DatabaseTables.GetTableForDisplayArray(
                table_key, "", current_group, 1, [], 0, [],
            )
        except Exception:
            continue
        if isinstance(trial, (tuple, list)) and len(trial) >= 1:
            ret_code = trial[-1] if isinstance(trial[-1], int) else 0
            if ret_code == 0:
                result = trial
                break
        result = trial

    if not isinstance(result, (tuple, list)) or len(result) < 2:
        return None, None

    fields: Optional[List[str]] = None
    data: Optional[List[str]] = None

    # Explicit index patterns observed in different comtypes/CSI builds.
    for fields_idx, data_idx in [(4, 6), (2, 4), (3, 5)]:
        if len(result) <= data_idx:
            continue
        try:
            candidate_fields = [str(x) for x in result[fields_idx]]
            candidate_data = [str(x) for x in result[data_idx]]
        except TypeError:
            continue
        if candidate_fields and candidate_data and len(candidate_data) >= len(candidate_fields):
            fields = candidate_fields
            data = candidate_data
            break

    # Heuristic fallback closer to the older ETABS scripts: find a field-like
    # array and then the next sufficiently long array as flat data.
    if fields is None or data is None:
        for idx, item in enumerate(result):
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue
            try:
                candidate = [str(x) for x in item]
            except TypeError:
                continue
            first = candidate[0].strip().lower() if candidate else ""
            if not any(token in first for token in ["case", "mode", "story", "output", "name", "type"]):
                continue
            fields = candidate
            for next_item in result[idx + 1 :]:
                if not isinstance(next_item, (list, tuple)):
                    continue
                try:
                    candidate_data = [str(x) for x in next_item]
                except TypeError:
                    continue
                if len(candidate_data) >= len(fields):
                    data = candidate_data
                    break
            if fields and data:
                break

    arrays: List[List[str]] = []
    for item in result:
        if item is None or isinstance(item, (int, float, str)):
            continue
        try:
            arr = [str(x) for x in item]
        except TypeError:
            continue
        if arr:
            arrays.append(arr)

    def looks_like_fields(arr: List[str]) -> bool:
        if len(arr) < 2:
            return False
        non_numeric = 0
        for value in arr[: min(6, len(arr))]:
            token = value.strip()
            if not token:
                continue
            try:
                float(token.replace(",", "."))
            except ValueError:
                if len(token) < 60:
                    non_numeric += 1
        return non_numeric >= max(1, len(arr[: min(6, len(arr))]) // 2)

    if fields is None or data is None:
        for idx, arr in enumerate(arrays):
            if not looks_like_fields(arr):
                continue
            n_fields = len(arr)
            for arr2 in arrays[idx + 1 :]:
                if n_fields > 0 and len(arr2) % n_fields == 0:
                    fields = arr
                    data = arr2
                    break
            if fields and data:
                break

    if not fields or data is None:
        return None, None

    rows = []
    n_fields = len(fields)
    for offset in range(0, len(data), n_fields):
        chunk = data[offset : offset + n_fields]
        if len(chunk) != n_fields:
            continue
        rows.append({fields[i]: chunk[i] for i in range(n_fields)})
    return fields, rows


def _normalize_token(text: str) -> str:
    base = unicodedata.normalize("NFKD", str(text or ""))
    ascii_only = "".join(ch for ch in base if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", ascii_only.lower())


def _match_story_name(raw_story: str) -> str:
    token = _normalize_token(raw_story)
    for story_name in STORY_NAMES:
        if token == _normalize_token(story_name):
            return story_name
    return ""


def _story_from_z(z_value: float, tol: float = 0.05) -> str:
    for story_name, elevation in zip(STORY_NAMES, STORY_ELEVATIONS):
        if abs(z_value - elevation) <= tol:
            return story_name
    return ""


def _pick_field_by_tokens(
    fields: Iterable[str],
    exact_tokens: Iterable[str] = (),
    contains_tokens: Iterable[str] = (),
    exclude_tokens: Iterable[str] = (),
) -> Optional[str]:
    normalized = [(_normalize_token(field), field) for field in fields]
    excluded = {_normalize_token(token) for token in exclude_tokens}

    for exact in exact_tokens:
        target = _normalize_token(exact)
        for token, original in normalized:
            if token == target:
                return original

    for contains in contains_tokens:
        target = _normalize_token(contains)
        for token, original in normalized:
            if any(excluded_token and excluded_token in token for excluded_token in excluded):
                continue
            if target and target in token:
                return original
    return None


def list_available_tables(SapModel) -> List[Dict[str, str]]:
    """List available ETABS database tables with best-effort parsing."""
    try:
        result = SapModel.DatabaseTables.GetAvailableTables()
    except Exception:
        return []

    if not isinstance(result, (tuple, list)) or len(result) < 3:
        return []

    number = 0
    try:
        number = int(result[0])
    except Exception:
        number = 0

    keys = []
    names = []
    import_types = []

    for item in result[1:]:
        if isinstance(item, (tuple, list)):
            values = [str(x) for x in item]
            if not keys:
                keys = values
            elif not names:
                names = values
            elif not import_types:
                import_types = values

    count = max(number, len(keys), len(names))
    tables = []
    for idx in range(count):
        key = keys[idx] if idx < len(keys) else ""
        name = names[idx] if idx < len(names) else key
        import_type = import_types[idx] if idx < len(import_types) else ""
        if key or name:
            tables.append({
                "key": key,
                "name": name,
                "import_type": import_type,
            })
    return tables


def _collect_joint_lookup(SapModel) -> Dict[str, Dict[str, float]]:
    """Collect joint coordinates/story keyed by normalized labels.

    Uses both PointObj.GetNameList and the database table
    'Objects and Elements - Joints' to maximize compatibility with meshed
    point elements and internal joint labels.
    """
    lookup: Dict[str, Dict[str, float]] = {}

    def _store(alias: str, payload: Dict[str, float]) -> None:
        token = _normalize_token(alias)
        if not token:
            return
        lookup[token] = dict(payload)

    try:
        result = SapModel.PointObj.GetNameList()
        names = [str(name) for name in (result[1] if isinstance(result, (tuple, list)) and len(result) >= 2 else [])]
    except Exception:
        names = []

    for name in names:
        try:
            coord = SapModel.PointObj.GetCoordCartesian(name)
            x = float(coord[0])
            y = float(coord[1])
            z = float(coord[2])
        except Exception:
            continue
        story = _story_from_z(z)
        payload = {"name": name, "x": x, "y": y, "z": z, "story": story}
        _store(name, payload)

    fields, rows = parse_db_table(SapModel, "Objects and Elements - Joints")
    if not rows:
        return lookup

    fields = fields or []
    object_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["Object", "Obj"],
        contains_tokens=["object", "obj"],
    )
    element_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["Element", "Elm"],
        contains_tokens=["element", "elm"],
    )
    story_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["Story"],
        contains_tokens=["story"],
    )
    x_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["X", "GlobalX", "CoordX", "XCoord"],
        contains_tokens=["coordx", "globalx"],
        exclude_tokens=["ux", "xcm", "xcr"],
    )
    y_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["Y", "GlobalY", "CoordY", "YCoord"],
        contains_tokens=["coordy", "globaly"],
        exclude_tokens=["uy", "ycm", "ycr"],
    )
    z_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["Z", "GlobalZ", "CoordZ", "ZCoord"],
        contains_tokens=["coordz", "globalz"],
        exclude_tokens=["uz"],
    )

    for row in rows:
        x_raw = row.get(x_key, "") if x_key else ""
        y_raw = row.get(y_key, "") if y_key else ""
        z_raw = row.get(z_key, "") if z_key else ""
        if str(x_raw).strip() == "" or str(y_raw).strip() == "":
            continue

        x = safe_float(x_raw, 0.0)
        y = safe_float(y_raw, 0.0)
        z = safe_float(z_raw, 0.0)
        story = _match_story_name(str(row.get(story_key, ""))) if story_key else ""
        if not story:
            story = _story_from_z(z)
        payload = {
            "name": str(row.get(object_key or "", row.get(element_key or "", ""))).strip(),
            "x": x,
            "y": y,
            "z": z,
            "story": story,
        }
        for key_name in [object_key, element_key]:
            if not key_name:
                continue
            alias = str(row.get(key_name, "")).strip()
            if alias:
                _store(alias, payload)

    return lookup


def collect_joint_lookup(SapModel) -> Dict[str, Dict[str, float]]:
    return _collect_joint_lookup(SapModel)


def find_table_candidates(
    SapModel,
    exact_names: Iterable[str],
    keyword_groups: Iterable[Iterable[str]],
) -> List[str]:
    """Find ETABS table keys by exact or fuzzy name matching."""
    available = list_available_tables(SapModel)
    if not available:
        return list(exact_names)

    exact_normalized = {_normalize_token(name) for name in exact_names}
    seen = set()
    candidates: List[str] = []

    def add_candidate(key: str):
        token = _normalize_token(key)
        if key and token not in seen:
            seen.add(token)
            candidates.append(key)

    for table in available:
        hay = _normalize_token(table["key"] + " " + table["name"])
        if hay in exact_normalized:
            add_candidate(table["key"] or table["name"])

    for keywords in keyword_groups:
        normalized_keywords = [_normalize_token(word) for word in keywords]
        for table in available:
            hay = _normalize_token(table["key"] + " " + table["name"])
            if all(word in hay for word in normalized_keywords):
                add_candidate(table["key"] or table["name"])

    for name in exact_names:
        add_candidate(name)
    return candidates


def select_cases_for_output(SapModel, cases: Iterable[str]) -> None:
    try:
        SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    except Exception:
        pass
    for case in cases:
        try:
            SapModel.Results.Setup.SetCaseSelectedForOutput(case)
        except Exception:
            continue


def select_combos_for_output(SapModel, combos: Iterable[str]) -> None:
    try:
        SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    except Exception:
        pass
    for combo in combos:
        try:
            SapModel.Results.Setup.SetComboSelectedForOutput(combo)
        except Exception:
            continue


def get_story_index(story_name: str) -> int:
    try:
        return STORY_NAMES.index(story_name)
    except ValueError:
        return -1


def modal_directional_summary(modal_rows: List[Dict[str, str]]) -> Dict[str, Dict[str, float]]:
    """Choose T* in X/Y/Z from the mode with max modal participation in each direction."""
    best_x = {"period": 0.0, "mode": 0, "participation": -1.0}
    best_y = {"period": 0.0, "mode": 0, "participation": -1.0}
    best_rz = {"period": 0.0, "mode": 0, "participation": -1.0}

    for row in modal_rows:
        mode = int(safe_float(row.get("Mode", row.get("mode", "0")), 0))
        period = safe_float(row.get("Period", row.get("period", "0")), 0.0)
        ux = safe_float(row.get("UX", row.get("ux", "0")), 0.0)
        uy = safe_float(row.get("UY", row.get("uy", "0")), 0.0)
        rz = safe_float(row.get("RZ", row.get("rz", "0")), 0.0)
        if ux > 1:
            ux /= 100.0
        if uy > 1:
            uy /= 100.0
        if rz > 1:
            rz /= 100.0
        if period > 0 and ux > best_x["participation"]:
            best_x = {"period": period, "mode": mode, "participation": ux}
        if period > 0 and uy > best_y["participation"]:
            best_y = {"period": period, "mode": mode, "participation": uy}
        if period > 0 and rz > best_rz["participation"]:
            best_rz = {"period": period, "mode": mode, "participation": rz}

    return {"X": best_x, "Y": best_y, "RZ": best_rz}


def modal_first_three_summary(modal_rows: List[Dict[str, str]]) -> Dict[str, object]:
    ranked = sorted(
        modal_rows,
        key=lambda row: int(safe_float(row.get("Mode", row.get("mode", "0")), 0)),
    )[:3]

    first_three = []
    observed = set()
    for row in ranked:
        mode = int(safe_float(row.get("Mode", row.get("mode", "0")), 0))
        period = safe_float(row.get("Period", row.get("period", "0")), 0.0)
        ux = safe_float(row.get("UX", row.get("ux", "0")), 0.0)
        uy = safe_float(row.get("UY", row.get("uy", "0")), 0.0)
        rz = safe_float(row.get("RZ", row.get("rz", "0")), 0.0)
        if ux > 1:
            ux /= 100.0
        if uy > 1:
            uy /= 100.0
        if rz > 1:
            rz /= 100.0

        dominant = max(
            [("X", ux), ("Y", uy), ("RZ", rz)],
            key=lambda item: item[1],
        )[0]
        observed.add(dominant)
        first_three.append(
            {
                "mode": mode,
                "period": period,
                "dominant": dominant,
                "ux": ux,
                "uy": uy,
                "rz": rz,
            }
        )

    return {
        "first_three": first_three,
        "covers_xyz": observed == {"X", "Y", "RZ"},
    }


def extract_modal_rows_from_db(SapModel) -> List[Dict[str, str]]:
    table_names = [
        "Modal Participating Mass Ratios",
        "Modal Participation Mass Ratios",
        "Modal Participating Masses",
        "Modal Information",
        "Modal Periods And Frequencies",
    ]
    for table_name in table_names:
        fields, rows = parse_db_table(SapModel, table_name)
        if rows:
            normalized = []
            lower_map = {field.lower().strip(): field for field in (fields or [])}

            def _key(*candidates):
                for candidate in candidates:
                    for lower_name, original in lower_map.items():
                        if candidate in lower_name:
                            return original
                return None

            col_mode = _key("mode")
            col_period = _key("period")
            col_ux = _key("ux")
            col_uy = _key("uy")
            col_rz = _key("rz")
            col_sum_ux = _key("sumux", "sum ux")
            col_sum_uy = _key("sumuy", "sum uy")
            for row in rows:
                period = safe_float(row.get(col_period or "", "0"), 0.0)
                if period <= 0:
                    continue
                normalized.append({
                    "Mode": str(int(safe_float(row.get(col_mode or "", "0"), 0))),
                    "Period": f"{period:.6f}",
                    "UX": str(safe_float(row.get(col_ux or "", "0"), 0.0)),
                    "UY": str(safe_float(row.get(col_uy or "", "0"), 0.0)),
                    "RZ": str(safe_float(row.get(col_rz or "", "0"), 0.0)),
                    "SumUX": str(safe_float(row.get(col_sum_ux or "", "0"), 0.0)),
                    "SumUY": str(safe_float(row.get(col_sum_uy or "", "0"), 0.0)),
                })
            if normalized:
                return normalized
    return []


def compute_story_weights_analytic() -> List[Dict[str, float]]:
    """Approximate seismic weight at each floor from the official model definition.

    This is used to build the static force vector before the full seismic run.
    The extractor later contrasts this with real ETABS gravity/base-reaction data.
    """
    concrete_gamma = 2.5  # tonf/m3
    area = AREA_PLANTA

    beam_area_by_story = {
        "Story1": 0.50 * 0.70,
        "Story2": 0.50 * 0.70,
        "Story3": 0.45 * 0.70,
        "Story4": 0.45 * 0.70,
        "Story5": 0.45 * 0.70,
    }
    column_area_by_story = {
        "Story1": 0.70 * 0.70,
        "Story2": 0.70 * 0.70,
        "Story3": 0.65 * 0.65,
        "Story4": 0.65 * 0.65,
        "Story5": 0.65 * 0.65,
    }

    n_beams_per_story = 60
    beam_length = 6.5
    n_columns_per_story = 36

    floor_dead = []
    column_segment_weights = []
    for story_name, story_h in zip(STORY_NAMES, STORY_HEIGHTS):
        slab_weight = area * 0.17 * concrete_gamma
        beam_weight = n_beams_per_story * beam_length * beam_area_by_story[story_name] * concrete_gamma
        col_seg_weight = n_columns_per_story * story_h * column_area_by_story[story_name] * concrete_gamma
        column_segment_weights.append(col_seg_weight)

        super_dead = area * (LOADS_AREA["TERT"] if story_name == "Story5" else LOADS_AREA["TERP"])
        live_seismic = area * (LOADS_AREA["SCT"] if story_name == "Story5" else LOADS_AREA["SCP"]) * 0.25

        floor_dead.append({
            "story": story_name,
            "slab_weight": slab_weight,
            "beam_weight": beam_weight,
            "super_dead": super_dead,
            "live_seismic": live_seismic,
        })

    rows = []
    for i, story_name in enumerate(STORY_NAMES):
        col_contrib = 0.0
        if i >= 0:
            col_contrib += 0.5 * column_segment_weights[i]
        if i + 1 < len(column_segment_weights):
            col_contrib += 0.5 * column_segment_weights[i + 1]
        if i == len(column_segment_weights) - 1:
            col_contrib = 0.5 * column_segment_weights[i]

        dead_parts = floor_dead[i]
        total = (
            dead_parts["slab_weight"]
            + dead_parts["beam_weight"]
            + dead_parts["super_dead"]
            + dead_parts["live_seismic"]
            + col_contrib
        )
        rows.append({
            "story": story_name,
            "elevation_m": STORY_ELEVATIONS[i],
            "weight_tonf": total,
            "slab_weight_tonf": dead_parts["slab_weight"],
            "beam_weight_tonf": dead_parts["beam_weight"],
            "super_dead_tonf": dead_parts["super_dead"],
            "live_seismic_tonf": dead_parts["live_seismic"],
            "column_contrib_tonf": col_contrib,
        })
    return rows


def extract_story_weights_from_db(SapModel) -> Optional[List[Dict[str, float]]]:
    """Extract story weights from ETABS tables when available.

    Prefers explicit weight-like columns. If only translational masses are
    available, converts them to tonf multiplying by g.
    """
    table_names = [
        "Mass Summary by Story",
        "Story Mass Summary",
        "Mass Summary By Story",
        "Story Masses",
        "Masses by Story",
    ]
    table_candidates = find_table_candidates(
        SapModel,
        exact_names=table_names,
        keyword_groups=[
            ["mass", "story"],
            ["mass", "summary", "story"],
            ["story", "mass", "summary"],
            ["story", "masses"],
        ],
    )

    for table_name in table_candidates:
        fields, rows = parse_db_table(SapModel, table_name)
        if not rows:
            continue

        lower_map = {field.lower().strip(): field for field in (fields or [])}
        normalized_map = {_normalize_token(field): field for field in (fields or [])}
        story_name_map = {_normalize_token(name): name for name in STORY_NAMES}

        def _pick_story_key():
            for token, original in normalized_map.items():
                if "story" in token:
                    return original
            return None

        def _pick_weight_key():
            preferred = [
                "seismic weight",
                "weight",
                "story weight",
                "wt",
            ]
            for candidate in preferred:
                norm_candidate = _normalize_token(candidate)
                for token, original in normalized_map.items():
                    if norm_candidate in token:
                        return original
            return None

        def _pick_mass_keys():
            selected = []
            for candidate in [
                "ux mass",
                "uy mass",
                "uz mass",
                "mass x",
                "mass y",
                "mass z",
                "ux",
                "uy",
                "uz",
                "mass",
            ]:
                norm_candidate = _normalize_token(candidate)
                for token, original in normalized_map.items():
                    if norm_candidate in token and original not in selected:
                        selected.append(original)
            return selected

        story_key = _pick_story_key()
        if not story_key:
            continue

        weight_key = _pick_weight_key()
        mass_keys = _pick_mass_keys()

        parsed = []
        for row in rows:
            raw_story = str(row.get(story_key, "")).strip()
            story = story_name_map.get(_normalize_token(raw_story), raw_story)
            if story not in STORY_NAMES:
                continue

            weight_tonf = None
            if weight_key:
                weight_tonf = abs(safe_float(row.get(weight_key), 0.0))

            if (weight_tonf is None or weight_tonf <= 0.0) and mass_keys:
                masses = [abs(safe_float(row.get(key), 0.0)) for key in mass_keys]
                masses = [value for value in masses if value > 0.0]
                if masses:
                    weight_tonf = max(masses) * G_ACCEL

            if weight_tonf is None or weight_tonf <= 0.0:
                continue

            idx = STORY_NAMES.index(story)
            parsed.append({
                "story": story,
                "elevation_m": STORY_ELEVATIONS[idx],
                "weight_tonf": weight_tonf,
                "source_table": table_name,
                "source_field": weight_key or ",".join(mass_keys),
            })

        if len(parsed) == len(STORY_NAMES):
            parsed.sort(key=lambda item: item["elevation_m"])
            return parsed

    return None


def compute_static_distribution(tx: float, ty: float, story_weights: List[Dict[str, float]]) -> Dict[str, object]:
    cmin = calc_Cmin()
    cmax = calc_Cmax()
    cx_raw = calc_C(tx)
    cy_raw = calc_C(ty)
    cx = clamp(cx_raw, cmin, cmax)
    cy = clamp(cy_raw, cmin, cmax)
    w_total = sum(row["weight_tonf"] for row in story_weights)
    vx = cx * I_FACTOR * w_total
    vy = cy * I_FACTOR * w_total

    story_rows = sorted(story_weights, key=lambda item: item["elevation_m"])
    ak_terms = []
    z_prev = 0.0
    for row in story_rows:
        z_k = row["elevation_m"]
        ak = math.sqrt(max(0.0, 1.0 - z_prev / H_TOTAL)) - math.sqrt(max(0.0, 1.0 - z_k / H_TOTAL))
        akpk = ak * row["weight_tonf"]
        ak_terms.append((ak, akpk))
        z_prev = z_k

    sum_akpk = sum(term for _, term in ak_terms)
    rows_desc = []
    running_vx = 0.0
    running_vy = 0.0
    running_mx = 0.0
    running_my = 0.0

    story_with_terms = []
    for row, (ak, akpk) in zip(story_rows, ak_terms):
        factor = (akpk / sum_akpk) if sum_akpk else 0.0
        fx = vx * factor
        fy = vy * factor
        ea_x = EA_STATIC_X[row["story"]]
        ea_y = EA_STATIC_Y[row["story"]]
        mtx = fx * ea_x
        mty = fy * ea_y
        story_with_terms.append({
            **row,
            "Ak": ak,
            "AkPk_tonf": akpk,
            "Fx_tonf": fx,
            "Fy_tonf": fy,
            "ea_x_m": ea_x,
            "ea_y_m": ea_y,
            "MtX_tonf_m": mtx,
            "MtY_tonf_m": mty,
        })

    for row in sorted(story_with_terms, key=lambda item: item["elevation_m"], reverse=True):
        running_vx += row["Fx_tonf"]
        running_vy += row["Fy_tonf"]
        running_mx += row["Fx_tonf"] * row["elevation_m"]
        running_my += row["Fy_tonf"] * row["elevation_m"]
        rows_desc.append({
            "story": row["story"],
            "elevation_m": row["elevation_m"],
            "weight_tonf": row["weight_tonf"],
            "Ak": row["Ak"],
            "AkPk_tonf": row["AkPk_tonf"],
            "Fx_tonf": row["Fx_tonf"],
            "Fy_tonf": row["Fy_tonf"],
            "ea_x_m": row["ea_x_m"],
            "ea_y_m": row["ea_y_m"],
            "MtX_tonf_m": row["MtX_tonf_m"],
            "MtY_tonf_m": row["MtY_tonf_m"],
            "Vx_accum_tonf": running_vx,
            "Vy_accum_tonf": running_vy,
            "Mx_overturning_tonf_m": running_mx,
            "My_overturning_tonf_m": running_my,
        })

    rows = list(reversed(rows_desc))
    return {
        "W_total_tonf": w_total,
        "Tx_s": tx,
        "Ty_s": ty,
        "Cx": cx,
        "Cy": cy,
        "Cx_raw": cx_raw,
        "Cy_raw": cy_raw,
        "Cmin": cmin,
        "Cmax": cmax,
        "Vdx_tonf": vx,
        "Vdy_tonf": vy,
        "rows": rows,
    }


def export_static_distribution(static_data: Dict[str, object]) -> str:
    rows = static_data["rows"]
    return write_csv(
        "ed2_static_distribution.csv",
        [
            "story",
            "elevation_m",
            "weight_tonf",
            "Ak",
            "AkPk_tonf",
            "Fx_tonf",
            "Fy_tonf",
            "ea_x_m",
            "ea_y_m",
            "MtX_tonf_m",
            "MtY_tonf_m",
            "Vx_accum_tonf",
            "Vy_accum_tonf",
            "Mx_overturning_tonf_m",
            "My_overturning_tonf_m",
        ],
        [
            [
                row["story"],
                f"{row['elevation_m']:.3f}",
                f"{row['weight_tonf']:.3f}",
                f"{row['Ak']:.6f}",
                f"{row['AkPk_tonf']:.3f}",
                f"{row['Fx_tonf']:.3f}",
                f"{row['Fy_tonf']:.3f}",
                f"{row['ea_x_m']:.3f}",
                f"{row['ea_y_m']:.3f}",
                f"{row['MtX_tonf_m']:.3f}",
                f"{row['MtY_tonf_m']:.3f}",
                f"{row['Vx_accum_tonf']:.3f}",
                f"{row['Vy_accum_tonf']:.3f}",
                f"{row['Mx_overturning_tonf_m']:.3f}",
                f"{row['My_overturning_tonf_m']:.3f}",
            ]
            for row in rows
        ],
    )


def export_story_weights(weights: List[Dict[str, float]]) -> str:
    primary = write_csv(
        "ed2_story_weights.csv",
        [
            "story",
            "elevation_m",
            "weight_tonf",
            "slab_weight_tonf",
            "beam_weight_tonf",
            "super_dead_tonf",
            "live_seismic_tonf",
            "column_contrib_tonf",
            "source_table",
            "source_field",
        ],
        [
            [
                row["story"],
                f"{row['elevation_m']:.3f}",
                f"{row['weight_tonf']:.3f}",
                f"{row.get('slab_weight_tonf', 0.0):.3f}",
                f"{row.get('beam_weight_tonf', 0.0):.3f}",
                f"{row.get('super_dead_tonf', 0.0):.3f}",
                f"{row.get('live_seismic_tonf', 0.0):.3f}",
                f"{row.get('column_contrib_tonf', 0.0):.3f}",
                row.get("source_table", ""),
                row.get("source_field", ""),
            ]
            for row in weights
        ],
    )
    # Alias legacy para no romper consumidores antiguos del paquete.
    write_csv(
        "ed2_story_weights_analytic.csv",
        [
            "story",
            "elevation_m",
            "weight_tonf",
            "slab_weight_tonf",
            "beam_weight_tonf",
            "super_dead_tonf",
            "live_seismic_tonf",
            "column_contrib_tonf",
            "source_table",
            "source_field",
        ],
        [
            [
                row["story"],
                f"{row['elevation_m']:.3f}",
                f"{row['weight_tonf']:.3f}",
                f"{row.get('slab_weight_tonf', 0.0):.3f}",
                f"{row.get('beam_weight_tonf', 0.0):.3f}",
                f"{row.get('super_dead_tonf', 0.0):.3f}",
                f"{row.get('live_seismic_tonf', 0.0):.3f}",
                f"{row.get('column_contrib_tonf', 0.0):.3f}",
                row.get("source_table", ""),
                row.get("source_field", ""),
            ]
            for row in weights
        ],
    )
    return primary


def export_summary_csv(summary: Dict[str, float]) -> str:
    return write_csv(
        "ed2_summary.csv",
        ["metric", "value"],
        [[key, value] for key, value in summary.items()],
    )


def validate_required_results() -> List[str]:
    missing = []
    for filename in REQUIRED_RESULT_FILES:
        if not os.path.exists(os.path.join(RESULTS_DIR, filename)):
            missing.append(filename)
    return missing


def geometric_center() -> Tuple[float, float]:
    x = 0.5 * (min(GRID_X.values()) + max(GRID_X.values()))
    y = 0.5 * (min(GRID_Y.values()) + max(GRID_Y.values()))
    return x, y


def _extract_story_cm_from_table(SapModel) -> Dict[str, Dict[str, float]]:
    """Extract center of mass coordinates per story when ETABS exposes them."""
    table_names = [
        "Centers Of Mass And Rigidity",
        "Center Of Mass And Rigidity",
        "Centers of Mass and Rigidity",
    ]

    for table_name in table_names:
        fields, rows = parse_db_table(SapModel, table_name)
        if not rows:
            continue

        fields = fields or []
        story_key = _pick_field_by_tokens(fields, exact_tokens=["Story"], contains_tokens=["story"])
        xcm_key = _pick_field_by_tokens(
            fields,
            exact_tokens=["XCM", "X Center Mass", "CumX"],
            contains_tokens=["xcentermass", "xcm", "cumx"],
            exclude_tokens=["xcr"],
        )
        ycm_key = _pick_field_by_tokens(
            fields,
            exact_tokens=["YCM", "Y Center Mass", "CumY"],
            contains_tokens=["ycentermass", "ycm", "cumy"],
            exclude_tokens=["ycr"],
        )

        parsed = {}
        for row in rows:
            story = _match_story_name(str(row.get(story_key or "", "")))
            if story not in STORY_NAMES:
                continue
            xcm = safe_float(row.get(xcm_key or "", "0"), 0.0)
            ycm = safe_float(row.get(ycm_key or "", "0"), 0.0)
            parsed[story] = {"xcm": xcm, "ycm": ycm}
        if len(parsed) == len(STORY_NAMES):
            return parsed

    return {}


def _extract_story_cm_from_assembled_joint_masses(SapModel) -> Dict[str, Dict[str, float]]:
    """Derive story CM from nodal assembled masses when CM/CR table is absent."""
    fields, rows = parse_db_table(SapModel, "Assembled Joint Masses")
    if not rows:
        return {}

    fields = fields or []
    story_key = _pick_field_by_tokens(fields, exact_tokens=["Story"], contains_tokens=["story"])
    point_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["PointElm", "Joint", "Point", "Label", "UniqueName", "Name"],
        contains_tokens=["pointelm", "joint", "point", "label", "uniquename", "name"],
    )
    x_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["X", "CoordX", "GlobalX", "XCoord"],
        contains_tokens=["coordx", "globalx"],
        exclude_tokens=["ux", "xcm", "xcr", "massx"],
    )
    y_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["Y", "CoordY", "GlobalY", "YCoord"],
        contains_tokens=["coordy", "globaly"],
        exclude_tokens=["uy", "ycm", "ycr", "massy"],
    )
    z_key = _pick_field_by_tokens(
        fields,
        exact_tokens=["Z", "CoordZ", "GlobalZ", "ZCoord"],
        contains_tokens=["coordz", "globalz"],
        exclude_tokens=["uz", "massz"],
    )

    mass_keys: List[str] = []
    for candidate in [
        "UX Mass",
        "UY Mass",
        "UZ Mass",
        "Mass X",
        "Mass Y",
        "Mass Z",
        "U1",
        "U2",
        "U3",
        "UX",
        "UY",
        "UZ",
        "Mass",
    ]:
        field_name = _pick_field_by_tokens(
            fields,
            exact_tokens=[candidate],
            contains_tokens=[candidate],
            exclude_tokens=["coord", "global", "story", "joint", "point", "label", "name", "xcm", "ycm", "xcr", "ycr"],
        )
        if field_name and field_name not in mass_keys:
            mass_keys.append(field_name)

    if not mass_keys:
        return {}

    joint_lookup = _collect_joint_lookup(SapModel)
    accum = {
        story_name: {"mass": 0.0, "mx": 0.0, "my": 0.0, "point_count": 0}
        for story_name in STORY_NAMES
    }

    for row in rows:
        story = _match_story_name(str(row.get(story_key or "", "")))
        joint_name = str(row.get(point_key or "", "")).strip()
        joint_payload = joint_lookup.get(_normalize_token(joint_name), {})

        x_value = None
        y_value = None
        z_value = None
        if x_key and str(row.get(x_key, "")).strip() != "":
            x_value = safe_float(row.get(x_key), 0.0)
        if y_key and str(row.get(y_key, "")).strip() != "":
            y_value = safe_float(row.get(y_key), 0.0)
        if z_key and str(row.get(z_key, "")).strip() != "":
            z_value = safe_float(row.get(z_key), 0.0)

        if x_value is None and joint_payload:
            x_value = joint_payload.get("x")
        if y_value is None and joint_payload:
            y_value = joint_payload.get("y")
        if z_value is None and joint_payload:
            z_value = joint_payload.get("z")

        if not story and joint_payload:
            story = _match_story_name(str(joint_payload.get("story", "")))
        if not story and z_value is not None:
            story = _story_from_z(z_value)
        if story not in STORY_NAMES:
            continue
        if x_value is None or y_value is None:
            continue

        masses = [
            abs(safe_float(row.get(key), 0.0))
            for key in mass_keys
            if str(row.get(key, "")).strip() != ""
        ]
        masses = [value for value in masses if value > 0.0]
        if not masses:
            continue
        lumped_mass = max(masses)

        accum[story]["mass"] += lumped_mass
        accum[story]["mx"] += lumped_mass * x_value
        accum[story]["my"] += lumped_mass * y_value
        accum[story]["point_count"] += 1

    parsed = {}
    for story_name in STORY_NAMES:
        data = accum[story_name]
        if data["mass"] <= 0.0:
            continue
        parsed[story_name] = {
            "xcm": data["mx"] / data["mass"],
            "ycm": data["my"] / data["mass"],
            "point_count": data["point_count"],
            "lumped_mass": data["mass"],
        }

    if len(parsed) == len(STORY_NAMES):
        return parsed
    return {}


def extract_story_cm_data(SapModel) -> Dict[str, object]:
    cm_map = _extract_story_cm_from_table(SapModel)
    if len(cm_map) == len(STORY_NAMES):
        return {"cm_map": cm_map, "source": "cm_table"}

    cm_map = _extract_story_cm_from_assembled_joint_masses(SapModel)
    if len(cm_map) == len(STORY_NAMES):
        return {"cm_map": cm_map, "source": "assembled_joint_masses"}

    return {"cm_map": {}, "source": "missing"}


def extract_story_cm_from_db(SapModel) -> Dict[str, Dict[str, float]]:
    return extract_story_cm_data(SapModel)["cm_map"]


def extract_cm_cr_rows(SapModel) -> Tuple[List[Dict[str, float]], Dict[str, object]]:
    """Return CM/CR rows with explicit source metadata.

    If the ETABS build does not expose the CM/CR table, the function falls back
    to real CM from assembled joint masses and duplicates CM into CR placeholders
    so the package shape remains stable. The source metadata makes that fallback
    explicit for downstream verification/review.
    """
    table_names = [
        "Centers Of Mass And Rigidity",
        "Center Of Mass And Rigidity",
        "Centers of Mass and Rigidity",
    ]

    for table_name in table_names:
        fields, rows = parse_db_table(SapModel, table_name)
        if not rows:
            continue

        fields = fields or []
        story_key = _pick_field_by_tokens(fields, exact_tokens=["Story"], contains_tokens=["story"])
        xcm_key = _pick_field_by_tokens(fields, exact_tokens=["XCM", "X Center Mass", "CumX"], contains_tokens=["xcentermass", "xcm", "cumx"])
        ycm_key = _pick_field_by_tokens(fields, exact_tokens=["YCM", "Y Center Mass", "CumY"], contains_tokens=["ycentermass", "ycm", "cumy"])
        xcr_key = _pick_field_by_tokens(fields, exact_tokens=["XCR", "X Center Rigidity", "CenterRigidX"], contains_tokens=["xcenterrigidity", "xcr", "centerrigidx"])
        ycr_key = _pick_field_by_tokens(fields, exact_tokens=["YCR", "Y Center Rigidity", "CenterRigidY"], contains_tokens=["ycenterrigidity", "ycr", "centerrigidy"])

        parsed = []
        for row in rows:
            story = _match_story_name(str(row.get(story_key or "", "")))
            if story not in STORY_NAMES:
                continue
            xcm = safe_float(row.get(xcm_key or "", "0"), 0.0)
            ycm = safe_float(row.get(ycm_key or "", "0"), 0.0)
            xcr = safe_float(row.get(xcr_key or "", "0"), 0.0)
            ycr = safe_float(row.get(ycr_key or "", "0"), 0.0)
            parsed.append({
                "story": story,
                "xcm": xcm,
                "ycm": ycm,
                "xcr": xcr,
                "ycr": ycr,
                "ex": abs(xcm - xcr),
                "ey": abs(ycm - ycr),
                "source": "etabs_cm_table",
                "cr_available": 1,
            })

        if len(parsed) == len(STORY_NAMES):
            parsed.sort(key=lambda item: STORY_NAMES.index(item["story"]))
            return parsed, {"source": "etabs_cm_table", "cr_available": True}

    cm_data = extract_story_cm_data(SapModel)
    cm_map = cm_data["cm_map"]
    if len(cm_map) == len(STORY_NAMES):
        parsed = []
        for story in STORY_NAMES:
            xcm = float(cm_map[story]["xcm"])
            ycm = float(cm_map[story]["ycm"])
            parsed.append({
                "story": story,
                "xcm": xcm,
                "ycm": ycm,
                "xcr": xcm,
                "ycr": ycm,
                "ex": 0.0,
                "ey": 0.0,
                "source": "assembled_joint_masses_placeholder_cr",
                "cr_available": 0,
            })
        return parsed, {"source": "assembled_joint_masses_placeholder_cr", "cr_available": False}

    return [], {"source": "missing", "cr_available": False}


def _collect_story_points(SapModel) -> Dict[str, List[Dict[str, float]]]:
    try:
        result = SapModel.PointObj.GetNameList()
        names = [str(name) for name in (result[1] if isinstance(result, (tuple, list)) and len(result) >= 2 else [])]
    except Exception:
        return {}

    by_story: Dict[str, List[Dict[str, float]]] = {story: [] for story in STORY_NAMES}

    for name in names:
        try:
            coord = SapModel.PointObj.GetCoordCartesian(name)
            x = float(coord[0])
            y = float(coord[1])
            z = float(coord[2])
        except Exception:
            continue

        for story, elevation in zip(STORY_NAMES, STORY_ELEVATIONS):
            if abs(z - elevation) <= 0.05:
                by_story[story].append({"name": name, "x": x, "y": y, "z": z})
                break
    return by_story


def find_story_center_points(SapModel, per_story: int = 4) -> Dict[str, List[Dict[str, float]]]:
    """Find joints nearest to the real story CM from ETABS."""
    cm_map = extract_story_cm_from_db(SapModel)
    if len(cm_map) != len(STORY_NAMES):
        raise RuntimeError(
            "ETABS no expuso el CM por historia. El flujo oficial no acepta "
            "reemplazarlo por centro geometrico."
        )
    by_story = _collect_story_points(SapModel)
    selected: Dict[str, List[Dict[str, float]]] = {}

    for story, points in by_story.items():
        ref = cm_map[story]
        ranked = sorted(
            points,
            key=lambda item: math.hypot(item["x"] - ref["xcm"], item["y"] - ref["ycm"]),
        )
        selected[story] = ranked[:per_story]

    return selected


def find_story_torsion_points(SapModel, per_story: int = 4) -> Dict[str, List[Dict[str, float]]]:
    """Pick distributed joints per story to emulate a pure in-plane torque."""
    cm_map = extract_story_cm_from_db(SapModel)
    if len(cm_map) != len(STORY_NAMES):
        raise RuntimeError(
            "ETABS no expuso el CM por historia. El flujo oficial no acepta "
            "reemplazarlo por centro geometrico."
        )
    by_story = _collect_story_points(SapModel)
    selected: Dict[str, List[Dict[str, float]]] = {}

    for story, points in by_story.items():
        ref = cm_map[story]
        buckets: Dict[str, Optional[Tuple[float, Dict[str, float]]]] = {
            "PP": None,
            "PN": None,
            "NP": None,
            "NN": None,
        }
        ranked = []
        for point in points:
            dx = point["x"] - ref["xcm"]
            dy = point["y"] - ref["ycm"]
            radius = math.hypot(dx, dy)
            if radius <= 1e-3:
                continue
            key = ("P" if dx >= 0 else "N") + ("P" if dy >= 0 else "N")
            current = buckets[key]
            if current is None or radius > current[0]:
                buckets[key] = (radius, point)
            ranked.append((radius, point))

        picks = [item[1] for item in buckets.values() if item is not None]
        if len(picks) < min(per_story, 3):
            ranked.sort(key=lambda item: item[0], reverse=True)
            seen = {point["name"] for point in picks}
            for _, point in ranked:
                if point["name"] in seen:
                    continue
                picks.append(point)
                seen.add(point["name"])
                if len(picks) >= per_story:
                    break
        if not picks:
            picks = points[:per_story]
        selected[story] = picks[:per_story]

    return selected


def find_story_center_joints(SapModel, per_story: int = 4) -> Dict[str, List[str]]:
    """Backward-compatible wrapper that returns only joint names."""
    center_points = find_story_center_points(SapModel, per_story=per_story)
    return {story: [point["name"] for point in points] for story, points in center_points.items()}
