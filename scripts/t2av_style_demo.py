#!/usr/bin/env python3
"""Draw an independent T2AV-Compass-inspired figure grammar demo.

The figure uses synthetic values and invented labels. It demonstrates the
relationship between a radial comparison, explanatory distributions, and a
hierarchical sunburst without copying the source project's data or artwork.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Circle, Wedge

from njulink_style import INK, INK_MUTED, LINE, PASTELS, PAPER, apply_style, save_figure


HATCHES = ["///", "\\\\", "...", "xx", "--", "++"]


def _mix(color: str, amount: float) -> tuple[float, float, float]:
    rgb = np.array(to_rgb(color))
    return tuple(rgb * (1 - amount) + amount)


def _setup_font() -> None:
    # T2AV's public figures use a friendly hand-drawn display face. Keep it an
    # optional enhancement with a portable fallback for Linux/CI.
    plt.rcParams["font.family"] = ["Comic Sans MS", "Chalkboard", "DejaVu Sans"]


def draw_radial(ax: plt.Axes) -> None:
    labels = ["Text→Video", "Audio→Video", "Video→Audio", "V→Tech", "A→V", "Perceptual"]
    rng = np.random.default_rng(12)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    models = ["Model A", "Model B", "Model C", "Model D", "Model E", "Model F"]
    colors = PASTELS[:6]
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.23)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.grid(False)
    ax.spines["polar"].set_visible(False)
    for i, (angle, label) in enumerate(zip(angles, labels)):
        values = np.clip(0.60 + 0.33 * rng.random(6) + 0.05 * np.sin(i), 0.48, 0.98)
        # Six narrow bars per spoke create the radial “compass” rhythm.
        span = np.deg2rad(17)
        offsets = np.linspace(-span / 2, span / 2, len(values))
        for j, (value, offset) in enumerate(zip(values, offsets)):
            width = span / len(values) * 0.86
            bottom = 0.28
            ax.bar(
                angle + offset,
                value - bottom,
                bottom=bottom,
                width=width,
                color=colors[j],
                edgecolor=PAPER,
                linewidth=0.7,
                hatch=HATCHES[j],
                alpha=0.92,
                zorder=3,
            )
            ax.text(angle + offset, value + 0.035, f"{value:.2f}", fontsize=5.4,
                    ha="center", va="center", rotation=np.degrees(-angle - offset) + 90,
                    rotation_mode="anchor", color=INK, zorder=5)
        ax.plot([angle, angle], [0.28, 1.05], color=LINE, linewidth=0.55, alpha=0.4, zorder=1)
        ax.text(angle, 1.12, label, fontsize=6.7, fontweight="bold", ha="center", va="center",
                rotation=np.degrees(-angle), rotation_mode="anchor", color=INK)
    ax.add_patch(Circle((0.5, 0.5), 0.145, transform=ax.transAxes, facecolor=PAPER,
                        edgecolor=LINE, linewidth=1.0, zorder=10))
    ax.text(0, 0.035, "MULTI-\nMODAL", ha="center", va="center", fontsize=7.7,
            fontweight="bold", color=INK, zorder=11)
    ax.text(0.5, 0.435, "synthetic compass", transform=ax.transAxes,
            ha="center", va="center", fontsize=5.8, color=INK_MUTED, zorder=11)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c, hatch=h, ec=PAPER) for c, h in zip(colors, HATCHES)]
    ax.legend(handles, models, loc="lower center", bbox_to_anchor=(0.5, -0.18), ncol=3,
              fontsize=5.5, frameon=False, handlelength=1.2, columnspacing=0.8)
    ax.set_title("(a) Radial comparison", loc="left", pad=8, fontsize=9, fontweight="bold")


def draw_explanatory(ax: plt.Axes) -> None:
    inner = ax.get_subplotspec().subgridspec(2, 2, height_ratios=[1.2, 1.0], hspace=0.58, wspace=0.42)
    density = ax.figure.add_subplot(inner[0, :])
    bars_left = ax.figure.add_subplot(inner[1, 0])
    bars_right = ax.figure.add_subplot(inner[1, 1])
    ax.remove()

    x = np.linspace(0, 1, 300)
    curves = [
        (0.30, 0.12, PASTELS[3], "System A"),
        (0.48, 0.16, PASTELS[1], "System B"),
        (0.68, 0.13, PASTELS[0], "System C"),
    ]
    for mu, sigma, color, label in curves:
        y = np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
        y *= 0.018 / y.max()
        density.fill_between(x, y, color=color, alpha=0.32)
        density.plot(x, y, color=color, linewidth=1.5, label=label)
    density.set_title("(b) Prompt evidence distribution", loc="left", fontsize=8.4, fontweight="bold")
    density.set_xlabel("normalized prompt complexity", fontsize=6.3)
    density.set_ylabel("density", fontsize=6.3)
    density.tick_params(labelsize=5.8)
    density.legend(fontsize=5.8, frameon=False, loc="upper right")
    density.spines["top"].set_visible(False)
    density.spines["right"].set_visible(False)

    names = ["Alpha", "Beta", "Gamma", "Delta"]
    vals = [0.94, 0.82, 0.68, 0.54]
    bars_left.barh(np.arange(4), vals, color=[PASTELS[2], PASTELS[3], PASTELS[5], PASTELS[1]], height=0.54)
    bars_left.set_yticks(np.arange(4), names, fontsize=5.8)
    bars_left.set_xlim(0, 1.05)
    bars_left.set_xlabel("text alignment", fontsize=6.2)
    bars_left.invert_yaxis()
    bars_left.set_title("(c) Semantic coverage", loc="left", fontsize=8.1, fontweight="bold")
    bars_left.tick_params(axis="x", labelsize=5.6)
    bars_left.grid(axis="x", alpha=0.45)
    bars_left.grid(axis="y", visible=False)
    bars_left.spines["top"].set_visible(False)
    bars_left.spines["right"].set_visible(False)

    vals2 = [0.89, 0.76, 0.61, 0.43]
    bars_right.barh(np.arange(4), vals2, color=[PASTELS[0], PASTELS[4], PASTELS[6], PASTELS[1]], height=0.54)
    bars_right.set_yticks(np.arange(4), names, fontsize=5.8)
    bars_right.set_xlim(0, 1.05)
    bars_right.set_xlabel("audio grounding", fontsize=6.2)
    bars_right.invert_yaxis()
    bars_right.set_title("(d) Modality grounding", loc="left", fontsize=8.1, fontweight="bold")
    bars_right.tick_params(axis="x", labelsize=5.6)
    bars_right.grid(axis="x", alpha=0.45)
    bars_right.grid(axis="y", visible=False)
    bars_right.spines["top"].set_visible(False)
    bars_right.spines["right"].set_visible(False)


def draw_sunburst(ax: plt.Axes) -> None:
    # Three rings share the same parent angles; only the labels and tint change.
    groups = [("Alignment", PASTELS[1]), ("Realism", PASTELS[0]),
              ("Dynamics", PASTELS[3]), ("Knowledge", PASTELS[6])]
    children = ["Temporal", "Spatial", "Object", "Style", "Sound", "Motion", "Context", "Detail"]
    grandchildren = [
        "Short", "Long", "Local", "Global", "Fine", "Coarse", "Stable", "Shift",
        "Clear", "Dense", "Near", "Far", "Soft", "Hard", "Calm", "Burst",
    ]
    ax.set_aspect("equal")
    ax.axis("off")
    start = 90
    group_span = 360 / len(groups)
    for i, (name, color) in enumerate(groups):
        theta1 = start - (i + 1) * group_span
        theta2 = start - i * group_span
        ax.add_patch(Wedge((0, 0), 0.93, theta1, theta2, width=0.30,
                           facecolor=_mix(color, 0.17), edgecolor=PAPER, linewidth=1.0))
        angle = (theta1 + theta2) / 2
        r = 0.76
        ax.text(r * np.cos(np.deg2rad(angle)), r * np.sin(np.deg2rad(angle)), name,
                fontsize=6.4, ha="center", va="center", rotation=angle - 90,
                rotation_mode="anchor", fontweight="bold", color=INK)
        for j in range(2):
            child_index = i * 2 + j
            a1 = theta1 + j * group_span / 2
            a2 = theta1 + (j + 1) * group_span / 2
            ax.add_patch(Wedge((0, 0), 1.25, a1, a2, width=0.30,
                               facecolor=_mix(color, 0.36 + 0.07 * j), edgecolor=PAPER, linewidth=0.9))
            angle_child = (a1 + a2) / 2
            r_child = 1.08
            ax.text(r_child * np.cos(np.deg2rad(angle_child)), r_child * np.sin(np.deg2rad(angle_child)),
                    children[child_index], fontsize=5.5, ha="center", va="center",
                    rotation=angle_child - 90, rotation_mode="anchor", color=INK)
            for k in range(2):
                aa1 = a1 + k * group_span / 4
                aa2 = a1 + (k + 1) * group_span / 4
                ax.add_patch(Wedge((0, 0), 1.55, aa1, aa2, width=0.29,
                                   facecolor=_mix(color, 0.57 + 0.06 * k), edgecolor=PAPER, linewidth=0.8))
                angle_leaf = (aa1 + aa2) / 2
                r_leaf = 1.42
                ax.text(r_leaf * np.cos(np.deg2rad(angle_leaf)), r_leaf * np.sin(np.deg2rad(angle_leaf)),
                        grandchildren[child_index * 2 + k], fontsize=4.8, ha="center", va="center",
                        rotation=angle_leaf - 90, rotation_mode="anchor", color=INK)
    ax.add_patch(Circle((0, 0), 0.62, facecolor=PAPER, edgecolor=LINE, linewidth=1.0))
    ax.text(0, 0.05, "EVAL\nTAXONOMY", ha="center", va="center", fontsize=8.3,
            fontweight="bold", color=INK)
    ax.text(0, -0.23, "synthetic hierarchy", ha="center", va="center", fontsize=5.5, color=INK_MUTED)
    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-1.7, 1.7)
    ax.set_title("(e) Hierarchical overview", loc="left", fontsize=9, fontweight="bold", pad=4)


def build_demo() -> plt.Figure:
    apply_style()
    _setup_font()
    fig = plt.figure(figsize=(15.0, 6.5), facecolor=PAPER)
    outer = fig.add_gridspec(1, 3, width_ratios=[1.06, 1.18, 1.0], wspace=0.18, left=0.025, right=0.985, top=0.88, bottom=0.14)
    radial = fig.add_subplot(outer[0, 0], projection="polar")
    draw_radial(radial)
    explanatory = fig.add_subplot(outer[0, 1])
    draw_explanatory(explanatory)
    sunburst = fig.add_subplot(outer[0, 2])
    draw_sunburst(sunburst)
    fig.text(0.025, 0.955, "T2AV-COMPASS-INSPIRED FIGURE GRAMMAR", fontsize=13, fontweight="bold", color=INK)
    fig.text(0.025, 0.918, "Independent reimplementation · simulated data · invented labels", fontsize=8.3, color=INK_MUTED)
    fig.text(0.985, 0.035, "Visual structure study only; no source values, logos, or artwork reproduced.", ha="right", fontsize=6.6, color=INK_MUTED)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("./examples"))
    args = parser.parse_args()
    fig = build_demo()
    outputs = save_figure(fig, args.output_dir / "t2av-compass-style-demo", formats=("png", "pdf"), dpi=240)
    plt.close(fig)
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
