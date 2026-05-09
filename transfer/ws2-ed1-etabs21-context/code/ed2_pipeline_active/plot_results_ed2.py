"""
plot_results_ed2.py - Graficos oficiales Ed.2 Parte 1.

Genera graficos solo desde resultados reales ya extraidos.
"""

import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ed2_static_official import RESULTS_DIR, read_csv, read_json, validate_required_results


PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")


def ensure_plots_dir() -> None:
    os.makedirs(PLOTS_DIR, exist_ok=True)


def to_float(rows, key):
    return [float(str(row[key]).replace(",", ".")) for row in rows]


def save_plot(fig, filename):
    ensure_plots_dir()
    path = os.path.join(PLOTS_DIR, filename)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_shear_and_overturning():
    _, rows = read_csv("ed2_static_distribution.csv")
    stories = [row["story"] for row in rows]
    z = to_float(rows, "elevation_m")
    vx = to_float(rows, "Vx_accum_tonf")
    vy = to_float(rows, "Vy_accum_tonf")
    mx = to_float(rows, "Mx_overturning_tonf_m")
    my = to_float(rows, "My_overturning_tonf_m")

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    axes[0].plot(vx, z, marker="o", label="Vx(z)")
    axes[0].plot(vy, z, marker="s", label="Vy(z)")
    axes[0].set_xlabel("Corte acumulado [tonf]")
    axes[0].set_ylabel("Elevacion [m]")
    axes[0].set_title("V(z)")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(mx, z, marker="o", label="Mx(z)")
    axes[1].plot(my, z, marker="s", label="My(z)")
    axes[1].set_xlabel("Momento volcamiento [tonf m]")
    axes[1].set_ylabel("Elevacion [m]")
    axes[1].set_title("Mvolcante(z)")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    return save_plot(fig, "ed2_vz_mvolcante.png")


def plot_story_forces_and_torsion():
    _, rows = read_csv("ed2_static_distribution.csv")
    stories = [row["story"] for row in rows]
    fx = to_float(rows, "Fx_tonf")
    fy = to_float(rows, "Fy_tonf")
    mtx = to_float(rows, "MtX_tonf_m")
    mty = to_float(rows, "MtY_tonf_m")

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    axes[0].bar(stories, fx, label="Fx")
    axes[0].bar(stories, fy, alpha=0.7, label="Fy")
    axes[0].set_title("Fuerzas por piso")
    axes[0].set_ylabel("tonf")
    axes[0].grid(True, axis="y", alpha=0.3)
    axes[0].legend()

    axes[1].bar(stories, mtx, label="MtX")
    axes[1].bar(stories, mty, alpha=0.7, label="MtY")
    axes[1].set_title("Torsion accidental por piso")
    axes[1].set_ylabel("tonf m")
    axes[1].grid(True, axis="y", alpha=0.3)
    axes[1].legend()
    return save_plot(fig, "ed2_fuerzas_torsion.png")


def plot_drifts():
    summary = read_json("ed2_summary.json")
    _, rows = read_csv("ed2_drift_envelope.csv")
    stories = [row["story"] for row in rows]
    dx = to_float(rows, "drift_x")
    dy = to_float(rows, "drift_y")
    ex = to_float(rows, "excess_x")
    ey = to_float(rows, "excess_y")
    limit_cm = float(summary.get("drift_limit_cm", summary["drift_limit"]))
    limit_excess = float(summary.get("drift_limit_point", 0.001))

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    axes[0].plot(dx, stories, marker="o", label="Drift CM X")
    axes[0].plot(dy, stories, marker="s", label="Drift CM Y")
    axes[0].axvline(limit_cm, color="r", linestyle="--", label="Limite CM")
    axes[0].set_xlabel("Drift")
    axes[0].set_ylabel("Story")
    axes[0].set_title("Condicion 1 - Drift CM")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(ex, stories, marker="o", label="Exceso X")
    axes[1].plot(ey, stories, marker="s", label="Exceso Y")
    axes[1].axvline(limit_excess, color="r", linestyle="--", label="Limite exceso")
    axes[1].set_xlabel("Drift")
    axes[1].set_ylabel("Story")
    axes[1].set_title("Condicion 2 - Exceso torsional")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    return save_plot(fig, "ed2_drift_envelope.png")


def plot_modal_periods():
    _, rows = read_csv("ed2_modal_results.csv")
    modes = [int(float(row["Mode"])) for row in rows[:10]]
    periods = [float(row["Period"]) for row in rows[:10]]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(modes, periods)
    ax.set_xlabel("Modo")
    ax.set_ylabel("Periodo [s]")
    ax.set_title("Periodos modales")
    ax.grid(True, axis="y", alpha=0.3)
    return save_plot(fig, "ed2_modal_periods.png")


def main() -> int:
    missing = validate_required_results()
    if missing:
        print("Faltan resultados oficiales para graficar:")
        for item in missing:
            print(f"  - {item}")
        return 1

    outputs = [
        plot_shear_and_overturning(),
        plot_story_forces_and_torsion(),
        plot_drifts(),
        plot_modal_periods(),
    ]
    print("Graficos generados:")
    for path in outputs:
        print(f"  - {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
