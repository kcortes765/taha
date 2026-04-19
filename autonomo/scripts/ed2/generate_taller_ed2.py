"""
generate_taller_ed2.py - Genera informe oficial Ed.2 Parte 1.

Usa exclusivamente CSV/JSON reales del flujo oficial.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ed2_static_official import (
    RESULTS_DIR,
    ensure_informe_dir,
    read_csv,
    read_json,
    validate_required_results,
)


PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")


def main() -> int:
    missing = validate_required_results()
    if missing:
        print("Faltan resultados oficiales para generar informe:")
        for item in missing:
            print(f"  - {item}")
        return 1

    summary = read_json("ed2_summary.json")
    _, static_rows = read_csv("ed2_static_distribution.csv")
    _, drift_rows = read_csv("ed2_drift_envelope.csv")

    informe_dir = ensure_informe_dir()
    output_path = os.path.join(informe_dir, "resultados_ed2.md")

    lines = []
    lines.append("# Resultados Oficiales - Edificio 2 Parte 1")
    lines.append("")
    lines.append("## Resumen")
    lines.append(f"- W = {summary['W_total_tonf']:.3f} tonf")
    lines.append(f"- T* (X) = {summary['Tx_s']:.4f} s")
    lines.append(f"- Ty* = {summary['Ty_s']:.4f} s")
    lines.append(f"- Tz* = {summary['Tz_s']:.4f} s")
    lines.append(f"- Cx = {summary['Cx']:.5f}")
    lines.append(f"- Cy = {summary['Cy']:.5f}")
    lines.append(f"- Cmin = {summary['Cmin']:.5f}")
    lines.append(f"- Cmax = {summary['Cmax']:.5f}")
    lines.append(f"- Vdx = {summary['Vdx_tonf']:.3f} tonf")
    lines.append(f"- Vdy = {summary['Vdy_tonf']:.3f} tonf")
    lines.append(f"- Drift CM max = {summary.get('max_drift_cm', summary['max_drift']):.6f}")
    lines.append(f"- Drift punto max = {summary.get('max_drift_point', 0.0):.6f}")
    lines.append(f"- Exceso torsional max = {summary.get('max_drift_excess', 0.0):.6f}")
    lines.append(f"- Fuente pesos por piso = {summary.get('story_weight_source', 'unknown')}")
    lines.append(f"- Fuente drift CM = {summary.get('drift_cm_source', 'unknown')}")
    lines.append("")
    lines.append("## Fuerzas Por Piso")
    lines.append("")
    lines.append("| Story | z [m] | Wk [tonf] | Fx [tonf] | Fy [tonf] | ea [m] | MtX [tonf m] | MtY [tonf m] |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for row in static_rows:
        lines.append(
            f"| {row['story']} | {row['elevation_m']} | {row['weight_tonf']} | "
            f"{row['Fx_tonf']} | {row['Fy_tonf']} | {row['ea_m']} | "
            f"{row['MtX_tonf_m']} | {row['MtY_tonf_m']} |"
        )
    lines.append("")
    lines.append("## Drift")
    lines.append("")
    lines.append("| Story | z [m] | Drift CM X | Drift CM Y | Drift Max X | Drift Max Y | Exceso X | Exceso Y | Combo CM X | Combo CM Y | Combo Max X | Combo Max Y |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|")
    for row in drift_rows:
        lines.append(
            f"| {row['story']} | {row['elevation_m']} | {row['drift_x']} | {row['drift_y']} | "
            f"{row.get('max_drift_x', '')} | {row.get('max_drift_y', '')} | "
            f"{row.get('excess_x', '')} | {row.get('excess_y', '')} | "
            f"{row.get('governing_cm_combo_x', '')} | {row.get('governing_cm_combo_y', '')} | "
            f"{row.get('governing_combo_x', '')} | {row.get('governing_combo_y', '')} |"
        )
    lines.append("")

    plot_files = [
        "ed2_vz_mvolcante.png",
        "ed2_fuerzas_torsion.png",
        "ed2_drift_envelope.png",
        "ed2_modal_periods.png",
    ]
    existing_plots = [name for name in plot_files if os.path.exists(os.path.join(PLOTS_DIR, name))]
    if existing_plots:
        lines.append("## Graficos")
        lines.append("")
        for name in existing_plots:
            rel = os.path.join("..", "..", "results", "plots", name).replace("\\", "/")
            lines.append(f"![{name}]({rel})")
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")

    print(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
