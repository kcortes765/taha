"""
import_ui_exports_ed2.py - Importa exports UI de ETABS Ed.2 al paquete local.

Uso:
  python import_ui_exports_ed2.py --source-dir C:\\ruta\\ui_exports_ed2
  python import_ui_exports_ed2.py --zip C:\\ruta\\ui_exports_ed2.zip

Salida principal en `results/`:
- ed2_ui_base_reactions.csv
- ed2_ui_story_forces_bottom.csv
- ed2_ui_joint_drifts.csv
- ed2_ui_story_drifts.csv
- ed2_ui_story_max_over_avg_drifts.csv
- ed2_ui_static_distribution.csv
- ed2_ui_drift_envelope.csv
- ed2_ui_summary.json
- ui_exports_raw/<timestamp>/... (copia cruda de los archivos fuente)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - runtime guard only
    raise SystemExit("Falta pandas. Instala con: pip install pandas openpyxl") from exc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import GRID_X, GRID_Y, RESULTS_DIR, STORY_ELEVATIONS, STORY_NAMES


REQUIRED_FILES = [
    "Base Reactions.xlsx",
    "Joint Drifts.xlsx",
    "Story Drifts.xlsx",
    "Story Forces.xlsx",
    "Story Max Over Avg Drifts.xlsx",
]

OPTIONAL_FILES = [
    "ed2_ui_summary.md",
    "CM_CR.xlsx",
    "Modal Periods And Frequencies.xlsx",
    "Modal Participating Mass Ratios.xlsx",
]

X_CASES = ["DRIFT_XP_TP", "DRIFT_XP_TN", "DRIFT_XN_TP", "DRIFT_XN_TN"]
Y_CASES = ["DRIFT_YP_TP", "DRIFT_YP_TN", "DRIFT_YN_TP", "DRIFT_YN_TN"]
DRIFT_CASES = X_CASES + Y_CASES
STORY_ORDER = {name: idx + 1 for idx, name in enumerate(STORY_NAMES)}
STORY_ELEVATION_MAP = {name: elev for name, elev in zip(STORY_NAMES, STORY_ELEVATIONS)}


def geometric_center():
    return 0.5 * (min(GRID_X.values()) + max(GRID_X.values())), 0.5 * (min(GRID_Y.values()) + max(GRID_Y.values()))


def clean_text(value) -> str:
    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def safe_float(value, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        text = str(value).strip()
        if not text:
            return default
        return float(text.replace(",", "."))
    except (TypeError, ValueError):
        return default


def ensure_results_dir() -> Path:
    path = Path(RESULTS_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_csv(path: Path, headers: Iterable[str], rows: Iterable[Iterable]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(list(headers))
        for row in rows:
            writer.writerow(list(row))


def load_etabs_table(path: Path, sheet_name=0) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=sheet_name, header=None)
    raw = raw.dropna(how="all").reset_index(drop=True)

    header_idx: Optional[int] = None
    for idx in range(min(12, len(raw))):
        row = [clean_text(x) for x in raw.iloc[idx].tolist()]
        if any(token in row for token in ["Output Case", "Story", "Label", "Direction", "Diaphragm"]):
            header_idx = idx
            break
    if header_idx is None:
        raise RuntimeError(f"No pude detectar encabezado ETABS en {path}")

    cols = [clean_text(x) for x in raw.iloc[header_idx].tolist()]
    df = raw.iloc[header_idx + 2 :].copy().reset_index(drop=True)  # salta fila de unidades
    df.columns = cols
    df = df.loc[:, [c for c in df.columns if c and c.lower() != "nan"]]
    return df


def _numeric_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[col] = out[col].apply(safe_float)
    return out


def _copy_raw_inputs(source_dir: Path, results_dir: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = results_dir / "ui_exports_raw" / stamp
    target.mkdir(parents=True, exist_ok=True)

    for name in REQUIRED_FILES + OPTIONAL_FILES:
        src = source_dir / name
        if src.exists():
            shutil.copy2(src, target / name)
    return target


def _extract_zip(zip_path: Path) -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="ed2_ui_import_"))
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(temp_dir)
    return temp_dir


def _resolve_source(args) -> Path:
    if args.source_dir:
        source_dir = Path(args.source_dir).expanduser().resolve()
        if not source_dir.is_dir():
            raise FileNotFoundError(f"Source dir no encontrado: {source_dir}")
        return source_dir
    zip_path = Path(args.zip).expanduser().resolve()
    if not zip_path.is_file():
        raise FileNotFoundError(f"Zip no encontrado: {zip_path}")
    return _extract_zip(zip_path)


def _check_required_files(source_dir: Path) -> None:
    missing = [name for name in REQUIRED_FILES if not (source_dir / name).exists()]
    if missing:
        raise FileNotFoundError(
            "Faltan exports UI requeridos:\n" + "\n".join(f"  - {name}" for name in missing)
        )


def _load_source_tables(source_dir: Path) -> Dict[str, pd.DataFrame]:
    return {
        "base_reactions": load_etabs_table(source_dir / "Base Reactions.xlsx", "Base Reactions"),
        "joint_drifts": load_etabs_table(source_dir / "Joint Drifts.xlsx", "Joint Drifts"),
        "story_drifts": load_etabs_table(source_dir / "Story Drifts.xlsx", "Story Drifts"),
        "story_forces": load_etabs_table(source_dir / "Story Forces.xlsx", "Story Forces"),
        "story_max_avg": load_etabs_table(source_dir / "Story Max Over Avg Drifts.xlsx", "Story Max Over Avg Drifts"),
    }


def _prepare_base_reactions(df: pd.DataFrame) -> pd.DataFrame:
    df = _numeric_columns(df, ["FX", "FY", "FZ", "MX", "MY", "MZ"])
    return df[df["Output Case"].astype(str).isin(["EX", "EY", "TEX", "TEY"])].copy()


def _prepare_story_forces(df: pd.DataFrame) -> pd.DataFrame:
    df = _numeric_columns(df, ["P", "VX", "VY", "T", "MX", "MY"])
    out = df[
        df["Output Case"].astype(str).isin(["EX", "EY"]) &
        df["Location"].astype(str).str.upper().eq("BOTTOM")
    ].copy()
    out["_story_n"] = out["Story"].map(STORY_ORDER)
    out = out.sort_values(["Output Case", "_story_n"])
    return out


def _prepare_joint_drifts(df: pd.DataFrame) -> pd.DataFrame:
    df = _numeric_columns(df, ["Label", "Unique Name", "Disp X", "Disp Y", "Drift X", "Drift Y"])
    out = df[df["Output Case"].astype(str).isin(DRIFT_CASES)].copy()
    out["_story_n"] = out["Story"].map(STORY_ORDER)
    return out.sort_values(["Output Case", "_story_n", "Label"])


def _prepare_story_drifts(df: pd.DataFrame) -> pd.DataFrame:
    df = _numeric_columns(df, ["Label", "Drift", "X", "Y", "Z"])
    out = df[df["Output Case"].astype(str).isin(DRIFT_CASES)].copy()
    out["_story_n"] = out["Story"].map(STORY_ORDER)
    return out.sort_values(["Output Case", "_story_n", "Direction", "Label"])


def _prepare_story_max_avg(df: pd.DataFrame) -> pd.DataFrame:
    df = _numeric_columns(df, ["Max Drift", "Avg Drift", "Ratio"])
    out = df[df["Output Case"].astype(str).isin(DRIFT_CASES)].copy()
    out["_story_n"] = out["Story"].map(STORY_ORDER)
    return out.sort_values(["Output Case", "_story_n", "Direction"])


def _static_distribution_from_story_forces(sf: pd.DataFrame) -> List[Dict[str, float]]:
    by_case = {}
    for case in ["EX", "EY"]:
        subset = sf[sf["Output Case"] == case].copy()
        subset = subset.sort_values("_story_n")
        by_case[case] = {row["Story"]: row for _, row in subset.iterrows()}

    rows: List[Dict[str, float]] = []
    for idx, story in enumerate(STORY_NAMES):
        current_ex = by_case["EX"][story]
        current_ey = by_case["EY"][story]
        next_story = STORY_NAMES[idx + 1] if idx + 1 < len(STORY_NAMES) else None

        next_vx = abs(by_case["EX"][next_story]["VX"]) if next_story else 0.0
        next_vy = abs(by_case["EY"][next_story]["VY"]) if next_story else 0.0
        next_tx = abs(by_case["EX"][next_story]["T"]) if next_story else 0.0
        next_ty = abs(by_case["EY"][next_story]["T"]) if next_story else 0.0

        vx_accum = abs(current_ex["VX"])
        vy_accum = abs(current_ey["VY"])
        tx_accum = abs(current_ex["T"])
        ty_accum = abs(current_ey["T"])

        rows.append(
            {
                "story": story,
                "elevation_m": STORY_ELEVATION_MAP[story],
                "Fx_story_tonf": vx_accum - next_vx,
                "Fy_story_tonf": vy_accum - next_vy,
                "MtX_story_tonf_m": tx_accum - next_tx,
                "MtY_story_tonf_m": ty_accum - next_ty,
                "Vx_accum_tonf": vx_accum,
                "Vy_accum_tonf": vy_accum,
                "Mx_overturning_tonf_m": abs(current_ey["MX"]),
                "My_overturning_tonf_m": abs(current_ex["MY"]),
                "T_from_EX_tonf_m": tx_accum,
                "T_from_EY_tonf_m": ty_accum,
            }
        )
    return rows


def _drift_envelope_from_ui(jd: pd.DataFrame, sm: pd.DataFrame) -> Dict[str, object]:
    jd_agg = (
        jd.groupby(["Output Case", "Story"], dropna=False)
        .agg({"Drift X": "max", "Drift Y": "max"})
        .reset_index()
    )

    x_story = jd_agg[jd_agg["Output Case"].isin(X_CASES)].groupby("Story", dropna=False)["Drift X"].max().reset_index()
    y_story = jd_agg[jd_agg["Output Case"].isin(Y_CASES)].groupby("Story", dropna=False)["Drift Y"].max().reset_index()

    x_story["_story_n"] = x_story["Story"].map(STORY_ORDER)
    y_story["_story_n"] = y_story["Story"].map(STORY_ORDER)
    x_story = x_story.sort_values("_story_n")
    y_story = y_story.sort_values("_story_n")

    x_sm = sm[sm["Output Case"].isin(X_CASES) & sm["Direction"].astype(str).eq("X")].copy()
    y_sm = sm[sm["Output Case"].isin(Y_CASES) & sm["Direction"].astype(str).eq("Y")].copy()
    x_sm = x_sm.groupby("Story", dropna=False).agg({"Max Drift": "max", "Avg Drift": "max", "Ratio": "max"}).reset_index()
    y_sm = y_sm.groupby("Story", dropna=False).agg({"Max Drift": "max", "Avg Drift": "max", "Ratio": "max"}).reset_index()
    x_sm["_story_n"] = x_sm["Story"].map(STORY_ORDER)
    y_sm["_story_n"] = y_sm["Story"].map(STORY_ORDER)
    x_sm = x_sm.sort_values("_story_n")
    y_sm = y_sm.sort_values("_story_n")
    x_sm["Delta(Max-Avg)"] = x_sm["Max Drift"] - x_sm["Avg Drift"]
    y_sm["Delta(Max-Avg)"] = y_sm["Max Drift"] - y_sm["Avg Drift"]

    rows = []
    for story in STORY_NAMES:
        x_row = x_story[x_story["Story"] == story].iloc[0]
        y_row = y_story[y_story["Story"] == story].iloc[0]
        x2 = x_sm[x_sm["Story"] == story].iloc[0]
        y2 = y_sm[y_sm["Story"] == story].iloc[0]
        rows.append(
            {
                "story": story,
                "elevation_m": STORY_ELEVATION_MAP[story],
                "drift_x": float(x_row["Drift X"]),
                "drift_y": float(y_row["Drift Y"]),
                "max_drift_x": float(x2["Max Drift"]),
                "avg_drift_x": float(x2["Avg Drift"]),
                "excess_x": float(x2["Delta(Max-Avg)"]),
                "ratio_x": float(x2["Ratio"]),
                "max_drift_y": float(y2["Max Drift"]),
                "avg_drift_y": float(y2["Avg Drift"]),
                "excess_y": float(y2["Delta(Max-Avg)"]),
                "ratio_y": float(y2["Ratio"]),
            }
        )

    gov_x = max(rows, key=lambda item: item["drift_x"])
    gov_y = max(rows, key=lambda item: item["drift_y"])
    gov_excess_x = max(rows, key=lambda item: item["excess_x"])
    gov_excess_y = max(rows, key=lambda item: item["excess_y"])
    gov_ratio_x = max(rows, key=lambda item: item["ratio_x"])
    gov_ratio_y = max(rows, key=lambda item: item["ratio_y"])

    return {
        "rows": rows,
        "governing": {
            "drift_x": gov_x,
            "drift_y": gov_y,
            "excess_x": gov_excess_x,
            "excess_y": gov_excess_y,
            "ratio_x": gov_ratio_x,
            "ratio_y": gov_ratio_y,
        },
    }


def _optional_modal_import(source_dir: Path, results_dir: Path) -> Optional[Dict[str, object]]:
    period_path = source_dir / "Modal Periods And Frequencies.xlsx"
    mass_path = source_dir / "Modal Participating Mass Ratios.xlsx"
    if not period_path.exists() or not mass_path.exists():
        return None

    periods = load_etabs_table(period_path, "Modal Periods And Frequencies")
    masses = load_etabs_table(mass_path, "Modal Participating Mass Ratios")
    periods = _numeric_columns(periods, ["Mode", "Period", "Frequency", "CircFreq", "Eigenvalue"])
    masses = _numeric_columns(masses, ["Mode", "Period", "UX", "UY", "UZ", "SumUX", "SumUY", "SumUZ", "RX", "RY", "RZ", "SumRX", "SumRY", "SumRZ"])

    merged = periods.merge(masses, on=["Case", "Mode", "Period"], how="left", suffixes=("", "_mass"))
    path = results_dir / "ed2_ui_modal_periods.csv"
    cols = [col for col in ["Case", "Mode", "Period", "Frequency", "UX", "UY", "SumUX", "SumUY", "RZ", "SumRZ"] if col in merged.columns]
    merged[cols].to_csv(path, index=False, encoding="utf-8")
    return {"file": str(path), "rows": len(merged)}


def _write_outputs(
    results_dir: Path,
    raw_copy_dir: Path,
    source_dir: Path,
    br: pd.DataFrame,
    sf: pd.DataFrame,
    jd: pd.DataFrame,
    sd: pd.DataFrame,
    sm: pd.DataFrame,
    static_rows: List[Dict[str, float]],
    drift_data: Dict[str, object],
    modal_info: Optional[Dict[str, object]],
) -> Dict[str, str]:
    outputs: Dict[str, str] = {}

    base_path = results_dir / "ed2_ui_base_reactions.csv"
    br[["Output Case", "FX", "FY", "MZ", "MX", "MY"]].to_csv(base_path, index=False, encoding="utf-8")
    outputs["base_reactions"] = str(base_path)

    sf_path = results_dir / "ed2_ui_story_forces_bottom.csv"
    sf[["Story", "Output Case", "Location", "VX", "VY", "T", "MX", "MY"]].to_csv(sf_path, index=False, encoding="utf-8")
    outputs["story_forces_bottom"] = str(sf_path)

    jd_path = results_dir / "ed2_ui_joint_drifts.csv"
    jd[["Story", "Label", "Unique Name", "Output Case", "Disp X", "Disp Y", "Drift X", "Drift Y"]].to_csv(jd_path, index=False, encoding="utf-8")
    outputs["joint_drifts"] = str(jd_path)

    sd_path = results_dir / "ed2_ui_story_drifts.csv"
    sd[["Story", "Output Case", "Direction", "Drift", "Label", "X", "Y", "Z"]].to_csv(sd_path, index=False, encoding="utf-8")
    outputs["story_drifts"] = str(sd_path)

    sm_path = results_dir / "ed2_ui_story_max_over_avg_drifts.csv"
    sm[["Story", "Output Case", "Direction", "Max Drift", "Avg Drift", "Ratio"]].to_csv(sm_path, index=False, encoding="utf-8")
    outputs["story_max_avg"] = str(sm_path)

    static_path = results_dir / "ed2_ui_static_distribution.csv"
    write_csv(
        static_path,
        [
            "story",
            "elevation_m",
            "Fx_story_tonf",
            "Fy_story_tonf",
            "MtX_story_tonf_m",
            "MtY_story_tonf_m",
            "Vx_accum_tonf",
            "Vy_accum_tonf",
            "Mx_overturning_tonf_m",
            "My_overturning_tonf_m",
            "T_from_EX_tonf_m",
            "T_from_EY_tonf_m",
        ],
        [
            [
                row["story"],
                f"{row['elevation_m']:.3f}",
                f"{row['Fx_story_tonf']:.6f}",
                f"{row['Fy_story_tonf']:.6f}",
                f"{row['MtX_story_tonf_m']:.6f}",
                f"{row['MtY_story_tonf_m']:.6f}",
                f"{row['Vx_accum_tonf']:.6f}",
                f"{row['Vy_accum_tonf']:.6f}",
                f"{row['Mx_overturning_tonf_m']:.6f}",
                f"{row['My_overturning_tonf_m']:.6f}",
                f"{row['T_from_EX_tonf_m']:.6f}",
                f"{row['T_from_EY_tonf_m']:.6f}",
            ]
            for row in static_rows
        ],
    )
    outputs["static_distribution"] = str(static_path)

    drift_path = results_dir / "ed2_ui_drift_envelope.csv"
    write_csv(
        drift_path,
        [
            "story",
            "elevation_m",
            "drift_x",
            "drift_y",
            "max_drift_x",
            "avg_drift_x",
            "excess_x",
            "ratio_x",
            "max_drift_y",
            "avg_drift_y",
            "excess_y",
            "ratio_y",
        ],
        [
            [
                row["story"],
                f"{row['elevation_m']:.3f}",
                f"{row['drift_x']:.6f}",
                f"{row['drift_y']:.6f}",
                f"{row['max_drift_x']:.6f}",
                f"{row['avg_drift_x']:.6f}",
                f"{row['excess_x']:.6f}",
                f"{row['ratio_x']:.3f}",
                f"{row['max_drift_y']:.6f}",
                f"{row['avg_drift_y']:.6f}",
                f"{row['excess_y']:.6f}",
                f"{row['ratio_y']:.3f}",
            ]
            for row in drift_data["rows"]
        ],
    )
    outputs["drift_envelope"] = str(drift_path)

    xcg, ycg = geometric_center()
    cmcr_path = results_dir / "ed2_ui_cm_cr_proxy.csv"
    write_csv(
        cmcr_path,
        ["story", "xcm", "ycm", "xcr", "ycr", "ex", "ey", "source"],
        [[story, f"{xcg:.3f}", f"{ycg:.3f}", f"{xcg:.3f}", f"{ycg:.3f}", "0.000", "0.000", "geometric_center_proxy"] for story in STORY_NAMES],
    )
    outputs["cm_cr_proxy"] = str(cmcr_path)

    summary = {
        "source": "etabs_ui_export",
        "source_dir": str(source_dir),
        "raw_copy_dir": str(raw_copy_dir),
        "base_reactions": {
            row["Output Case"]: {
                "FX": safe_float(row["FX"]),
                "FY": safe_float(row["FY"]),
                "MZ": safe_float(row["MZ"]),
                "MX": safe_float(row["MX"]),
                "MY": safe_float(row["MY"]),
            }
            for _, row in br.iterrows()
        },
        "drift_limit_cm": 0.002,
        "drift_limit_point": 0.001,
        "geometric_center_proxy": {"x": xcg, "y": ycg},
        "governing": drift_data["governing"],
        "checks": {
            "drift_x_le_0_002": drift_data["governing"]["drift_x"]["drift_x"] <= 0.002,
            "drift_y_le_0_002": drift_data["governing"]["drift_y"]["drift_y"] <= 0.002,
            "excess_x_le_0_001": drift_data["governing"]["excess_x"]["excess_x"] <= 0.001,
            "excess_y_le_0_001": drift_data["governing"]["excess_y"]["excess_y"] <= 0.001,
        },
        "modal_info": modal_info or {"available": False},
    }
    summary_path = results_dir / "ed2_ui_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)
    outputs["summary_json"] = str(summary_path)

    source_summary_md = source_dir / "ed2_ui_summary.md"
    if source_summary_md.exists():
        copied_summary_md = results_dir / "ed2_ui_summary.md"
        shutil.copy2(source_summary_md, copied_summary_md)
        outputs["summary_md"] = str(copied_summary_md)

    manifest_path = results_dir / "ed2_ui_import_manifest.json"
    manifest = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_dir": str(source_dir),
        "raw_copy_dir": str(raw_copy_dir),
        "required_files": REQUIRED_FILES,
        "optional_files_present": [name for name in OPTIONAL_FILES if (source_dir / name).exists()],
        "outputs": outputs,
    }
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    outputs["manifest"] = str(manifest_path)

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source-dir", help="Carpeta con exports UI de ETABS")
    group.add_argument("--zip", help="Zip con exports UI de ETABS")
    args = parser.parse_args()

    source_dir = _resolve_source(args)
    _check_required_files(source_dir)
    results_dir = ensure_results_dir()
    raw_copy_dir = _copy_raw_inputs(source_dir, results_dir)
    tables = _load_source_tables(source_dir)

    br = _prepare_base_reactions(tables["base_reactions"])
    sf = _prepare_story_forces(tables["story_forces"])
    jd = _prepare_joint_drifts(tables["joint_drifts"])
    sd = _prepare_story_drifts(tables["story_drifts"])
    sm = _prepare_story_max_avg(tables["story_max_avg"])

    static_rows = _static_distribution_from_story_forces(sf)
    drift_data = _drift_envelope_from_ui(jd, sm)
    modal_info = _optional_modal_import(source_dir, results_dir)

    outputs = _write_outputs(results_dir, raw_copy_dir, source_dir, br, sf, jd, sd, sm, static_rows, drift_data, modal_info)

    print("UI import completado:")
    for key, value in outputs.items():
        print(f"  - {key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
