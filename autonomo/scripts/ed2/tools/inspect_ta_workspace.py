"""
Filesystem-only audit for the ETABS Ed.2 workspace.

Use this on the university workstation or on any copied deploy folder to answer:
  - What folders are present under the workspace root?
  - Which folder looks like the active Ed.2 deploy?
  - Is there a real .edb model?
  - Are there raw CSV results?
  - Are there generated reports or plots without model evidence?
  - Does the deploy look older than the current repo baseline?
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


ROOT_DEFAULT = r"C:\Users\Civil\Documents\ta"

CORE_FILES = [
    "config_ed2.py",
    "01_init_model_ed2.py",
    "02_materials_sections_ed2.py",
    "03_columns_ed2.py",
    "04_beams_ed2.py",
    "05_slabs_ed2.py",
    "06_assignments_ed2.py",
    "07_loads_ed2.py",
    "08_seismic_ed2.py",
    "09_torsion_ed2.py",
    "10_combinations_ed2.py",
    "11_run_analysis_ed2.py",
    "12_extract_results_ed2.py",
    "run_pipeline_ed2.py",
]

ADVANCED_FILES = [
    "diag.py",
    "verify_ed2.py",
    "plot_results_ed2.py",
    "generate_taller_ed2.py",
]

RAW_RESULT_HINTS = [
    "ed2_modal_periods.csv",
    "ed2_drift_envelope.csv",
    "ed2_base_reactions.csv",
]

PLOT_CONSTANT_KEYS = ["W_TOTAL", "R_STAR", "V_DESIGN", "T1"]


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace")
    except OSError:
        return ""


def iso_mtime(path):
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")
    except OSError:
        return None


def relpath(path, base):
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def is_deploy_dir(path):
    if not path.is_dir():
        return False
    present = sum(1 for name in CORE_FILES if (path / name).exists())
    return (path / "config_ed2.py").exists() and present >= 6


def list_children(path):
    items = []
    if not path.exists():
        return items
    children = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    for child in children:
        items.append(
            {
                "name": child.name,
                "type": "dir" if child.is_dir() else "file",
                "mtime": iso_mtime(child),
            }
        )
    return items


def find_deploy_dirs(root):
    candidates = []
    if is_deploy_dir(root):
        candidates.append(root)
    if root.exists():
        for child in root.iterdir():
            if is_deploy_dir(child):
                candidates.append(child)
    return sorted(candidates, key=lambda p: p.name.lower())


def parse_plot_constants(plot_file):
    constants = {}
    if not plot_file.exists():
        return constants
    text = read_text(plot_file)
    for key in PLOT_CONSTANT_KEYS:
        match = re.search(r"^%s\s*=\s*([0-9.]+)" % re.escape(key), text, re.MULTILINE)
        if match:
            try:
                constants[key] = float(match.group(1))
            except ValueError:
                constants[key] = match.group(1)
    return constants


def detect_fallback_markers(generator_file):
    markers = []
    if not generator_file.exists():
        return markers
    text = read_text(generator_file).lower()
    checks = [
        ("computed_mode", "--computed" in text),
        ("estimate_drift", "estimando" in text or "estimate" in text),
        ("csv_or_compute", "csv + computed" in text or "csv+computed" in text),
    ]
    for name, present in checks:
        if present:
            markers.append(name)
    return markers


def summarize_deploy(deploy_dir, workspace_root):
    missing_core = [name for name in CORE_FILES if not (deploy_dir / name).exists()]
    missing_advanced = [name for name in ADVANCED_FILES if not (deploy_dir / name).exists()]

    models_dir = deploy_dir / "models"
    results_dir = deploy_dir / "results"
    plots_dir = results_dir / "plots"
    report_file = deploy_dir / "taller_ed2" / "informe" / "resultados_ed2.md"
    archive_dir = deploy_dir / "archive"

    edb_files = sorted(models_dir.rglob("*.edb")) if models_dir.exists() else []
    raw_csv_files = sorted(results_dir.glob("*.csv")) if results_dir.exists() else []
    plot_files = sorted(plots_dir.glob("*.png")) if plots_dir.exists() else []
    pipeline_logs = sorted(deploy_dir.glob("pipeline_ed2_*.log"))
    archive_snapshots = sorted([p for p in archive_dir.iterdir() if p.is_dir()]) if archive_dir.exists() else []

    plot_constants = parse_plot_constants(deploy_dir / "plot_results_ed2.py")
    fallback_markers = detect_fallback_markers(deploy_dir / "generate_taller_ed2.py")
    hint_hits = [name for name in RAW_RESULT_HINTS if (results_dir / name).exists()]

    findings = []
    if not edb_files:
        findings.append("No .edb found in models/.")
    if report_file.exists() and not edb_files:
        findings.append("Report package exists without model evidence.")
    if plot_files and not raw_csv_files:
        findings.append("Plots exist but results/ has no raw CSV files.")
    if missing_advanced:
        findings.append(
            "Deploy looks older than current repo baseline; missing: %s." % ", ".join(missing_advanced)
        )
    if plot_constants:
        findings.append("plot_results_ed2.py contains hardcoded reference constants.")
    if fallback_markers:
        findings.append("generate_taller_ed2.py can synthesize outputs when ETABS data is missing.")

    if edb_files and raw_csv_files and len(hint_hits) >= 2:
        validation_state = "validated_candidate"
    elif report_file.exists() or plot_files:
        validation_state = "generated_outputs_only"
    else:
        validation_state = "scripts_only"

    return {
        "path": str(deploy_dir),
        "path_relative": relpath(deploy_dir, workspace_root),
        "validation_state": validation_state,
        "missing_core": missing_core,
        "missing_advanced": missing_advanced,
        "models_dir_exists": models_dir.exists(),
        "results_dir_exists": results_dir.exists(),
        "report_exists": report_file.exists(),
        "report_path": relpath(report_file, workspace_root) if report_file.exists() else None,
        "edb_files": [relpath(p, workspace_root) for p in edb_files],
        "raw_csv_files": [relpath(p, workspace_root) for p in raw_csv_files],
        "raw_result_hint_hits": hint_hits,
        "plot_files": [relpath(p, workspace_root) for p in plot_files],
        "archive_snapshots": [relpath(p, workspace_root) for p in archive_snapshots],
        "pipeline_logs": [relpath(p, workspace_root) for p in pipeline_logs],
        "plot_constants": plot_constants,
        "fallback_markers": fallback_markers,
        "findings": findings,
    }


def summarize_workspace(root):
    exists = root.exists()
    deploy_dirs = find_deploy_dirs(root) if exists else []
    research_dirs = []
    zip_files = []
    if exists:
        for child in root.iterdir():
            if child.is_dir() and "research" in child.name.lower():
                research_dirs.append(child)
            if child.is_file() and child.suffix.lower() == ".zip":
                zip_files.append(child)

    return {
        "target_root": str(root),
        "exists": exists,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "children": list_children(root),
        "research_dirs": [relpath(p, root) for p in research_dirs],
        "zip_files": [relpath(p, root) for p in zip_files],
        "deploys": [summarize_deploy(p, root) for p in deploy_dirs],
    }


def to_markdown(data):
    lines = []
    lines.append("# Workspace Audit")
    lines.append("")
    lines.append("- Target root: `%s`" % data["target_root"])
    lines.append("- Timestamp: `%s`" % data["timestamp"])
    lines.append("- Exists: `%s`" % ("yes" if data["exists"] else "no"))
    lines.append("")

    if not data["exists"]:
        lines.append("The target path does not exist in this environment.")
        return "\n".join(lines)

    lines.append("## Root")
    if data["children"]:
        for item in data["children"]:
            lines.append("- `%s` (%s)" % (item["name"], item["type"]))
    else:
        lines.append("- Root is empty.")
    lines.append("")

    if data["research_dirs"]:
        lines.append("## Research")
        for entry in data["research_dirs"]:
            lines.append("- `%s`" % entry)
        lines.append("")

    if data["zip_files"]:
        lines.append("## Zip Files")
        for entry in data["zip_files"]:
            lines.append("- `%s`" % entry)
        lines.append("")

    lines.append("## Deploys")
    if not data["deploys"]:
        lines.append("- No Ed.2 deploy candidate was detected.")
        return "\n".join(lines)

    for deploy in data["deploys"]:
        lines.append("### `%s`" % deploy["path_relative"])
        lines.append("- Validation state: `%s`" % deploy["validation_state"])
        lines.append(
            "- Missing core files: `%s`"
            % (", ".join(deploy["missing_core"]) if deploy["missing_core"] else "none")
        )
        lines.append(
            "- Missing advanced files: `%s`"
            % (", ".join(deploy["missing_advanced"]) if deploy["missing_advanced"] else "none")
        )
        lines.append("- .edb files: `%d`" % len(deploy["edb_files"]))
        lines.append("- Raw CSV files: `%d`" % len(deploy["raw_csv_files"]))
        lines.append("- Plot PNG files: `%d`" % len(deploy["plot_files"]))
        lines.append("- Report exists: `%s`" % ("yes" if deploy["report_exists"] else "no"))
        lines.append("- Archive snapshots: `%d`" % len(deploy["archive_snapshots"]))
        if deploy["plot_constants"]:
            pairs = ", ".join("%s=%s" % (k, deploy["plot_constants"][k]) for k in sorted(deploy["plot_constants"]))
            lines.append("- Plot constants: `%s`" % pairs)
        if deploy["fallback_markers"]:
            lines.append("- Fallback markers: `%s`" % ", ".join(deploy["fallback_markers"]))
        if deploy["findings"]:
            lines.append("- Findings:")
            for finding in deploy["findings"]:
                lines.append("  - %s" % finding)
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit the Ed.2 workspace structure.")
    parser.add_argument("--path", default=ROOT_DEFAULT, help="Workspace root to inspect.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown.")
    parser.add_argument("--write-json", help="Optional JSON output file.")
    parser.add_argument("--write-markdown", help="Optional markdown output file.")
    args = parser.parse_args()

    root = Path(args.path)
    data = summarize_workspace(root)

    rendered = json.dumps(data, indent=2, ensure_ascii=True) if args.json else to_markdown(data)
    print(rendered)

    if args.write_json:
        Path(args.write_json).write_text(
            json.dumps(data, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
    if args.write_markdown:
        Path(args.write_markdown).write_text(to_markdown(data) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
