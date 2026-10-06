#!/usr/bin/env python3
"""NJU-LINK renditions of three Plot Is All You Need layouts.

All values are simulated; replace the explicitly named input arrays with data.
Layouts adapted from liouhai/plot-is-all-you-need (MIT, Copyright 2026 qc).
See licenses/plot-is-all-you-need-MIT.txt for attribution.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np
from scipy.stats import gaussian_kde

from njulink_style import INK, INK_MUTED, GRID, PASTELS, apply_style, save_figure


def raincloud(ax, groups, *, seed=2):
    """One numeric sample per observation, grouped by model; no aggregation loss."""
    rng = np.random.default_rng(seed)
    for x, (name, values) in enumerate(groups.items()):
        values = np.asarray(values, dtype=float)
        if len(values) < 2 or not np.isfinite(values).all() or np.ptp(values) == 0:
            raise ValueError("Each raincloud group needs at least two distinct finite observations.")
        colour = PASTELS[x % len(PASTELS)]
        span = np.ptp(values)
        yy = np.linspace(values.min() - 0.12 * span, values.max() + 0.12 * span, 200)
        dens = gaussian_kde(values)(yy)
        ax.fill_betweenx(yy, x + 0.04, x + 0.04 + dens / dens.max() * 0.34,
                         color=colour, alpha=0.65, linewidth=0.6, edgecolor=colour, zorder=2)
        ax.scatter(x - 0.08 - rng.random(len(values)) * 0.23, values,
                   s=7, color=colour, alpha=0.8, linewidths=0, zorder=3)
        median = np.median(values)
        ax.scatter([x + 0.04], [median], s=170, facecolor="white", edgecolor=INK,
                   linewidth=0.6, zorder=4)
        ax.text(x + 0.04, median, f"{median:.0f}", ha="center", va="center",
                fontsize=6.0, color=INK, zorder=5)
    ax.set_xticks(range(len(groups)), list(groups))
    ax.set_xlim(-0.55, len(groups) - 0.45)
    ax.set_ylabel("Task score (points)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Task-score distributions", loc="left", pad=8)


def ribbons(ax, periods, labels, percent):
    """Stack category shares; ribbons connect adjacent marginals, not flows."""
    percent = np.asarray(percent, dtype=float)
    if percent.shape != (len(labels), len(periods)):
        raise ValueError("Expected one row per component and one column per period.")
    if not np.isfinite(percent).all() or (percent < 0).any() or not np.allclose(percent.sum(axis=0), 100):
        raise ValueError("Each column must contain non-negative percentages summing to 100.")
    x, width = np.arange(len(periods)), 0.55
    top = np.cumsum(percent, axis=0)
    bottom = top - percent
    for i, label in enumerate(labels):
        colour = PASTELS[i % len(PASTELS)]
        ax.bar(x, percent[i], width, bottom=bottom[i], color=colour,
               edgecolor="white", linewidth=0.6, label=label, zorder=3)
        for j in range(len(periods) - 1):
            ax.fill_between([x[j] + width/2, x[j+1] - width/2],
                            [bottom[i, j], bottom[i, j+1]], [top[i, j], top[i, j+1]],
                            color=colour, alpha=0.24, linewidth=0, zorder=2)
        for j, value in enumerate(percent[i]):
            if value >= 10:
                ax.text(j, bottom[i, j] + value/2, f"{value:.0f}", ha="center",
                        va="center", fontsize=7, color=INK, zorder=4)
    ax.set_xticks(x, periods)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Task share (%)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=3, fontsize=7)
    ax.set_title("Composition across evaluation rounds", loc="left", pad=29)


def bubble_matrix(ax, names, values):
    """Show symmetric non-negative pair strengths with area proportional to value."""
    values = np.asarray(values, dtype=float)
    n = len(names)
    if values.shape != (n, n) or not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("Expected a finite, non-negative square strength matrix.")
    if not np.allclose(values, values.T) or not np.allclose(np.diag(values), 0):
        raise ValueError("Strength matrix must be symmetric with a zero diagonal.")
    maximum = float(values.max())
    if maximum <= 0:
        raise ValueError("At least one pair must have positive strength.")
    norm = Normalize(0, maximum)
    cmap = LinearSegmentedColormap.from_list("njulink_strength", ["#F3F7FB", PASTELS[1], "#376995"])
    i, j = np.triu_indices(n, 1)
    # Size is area in points squared; zero has zero area.
    sc = ax.scatter(j, i, s=220 * norm(values[i, j]), c=values[i, j], cmap=cmap,
                    norm=norm, edgecolors="#527080", linewidths=0.5, zorder=3)
    ax.set_xticks(range(n), names, rotation=38, ha="right")
    ax.set_yticks(range(n), names)
    ax.set_xlim(-0.55, n-0.45)
    ax.set_ylim(n-0.45, -0.55)
    ax.grid(axis="both", color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Pairwise interaction strength", loc="left", pad=8)
    # The unused triangle carries the shared area and colour key.
    legend_x, legend_y = 0.28, n - 2.0
    for k, fraction in enumerate([0.25, 0.5, 1.0]):
        x = legend_x + k * 0.95
        ax.scatter([x], [legend_y], s=220 * fraction, color=[cmap(fraction)],
                   edgecolors="#527080", linewidths=0.5, zorder=3)
        ax.text(x, legend_y + 0.72, f"{fraction * maximum:.1f}", ha="center", fontsize=6.5)
    ax.text(legend_x - 0.05, legend_y - 0.8, "Area + colour = strength", fontsize=6.5, color=INK_MUTED)
    return sc


def build_examples(output):
    output = Path(output)
    apply_style()
    rng = np.random.default_rng(2)
    # SIMULATED DATA: replace these arrays and labels for actual research.
    groups = {f"Agent {letter}": rng.normal(mean, 6.5, 70)
              for letter, mean in zip("ABCD", [58, 68, 73, 81])}
    periods = ["R1", "R2", "R3", "R4", "R5", "R6"]
    labels = ["Search", "Reason", "Verify"]
    percent = np.array([[45, 40, 34, 30, 28, 24], [35, 36, 40, 42, 44, 46],
                        [20, 24, 26, 28, 28, 30]], dtype=float)
    names = ["Plan", "Search", "Code", "Trace", "Verify", "Report"]
    upper = np.triu(rng.uniform(0.1, 1.0, (6, 6)), 1)
    strengths = upper + upper.T
    np.fill_diagonal(strengths, 0)
    strengths[0, 1] = strengths[1, 0] = 1.0
    recipes = [
        ("njulink-raincloud", lambda ax: raincloud(ax, groups), (5.4, 3.5)),
        ("njulink-ribbons", lambda ax: ribbons(ax, periods, labels, percent), (5.8, 3.5)),
        ("njulink-bubble", lambda ax: bubble_matrix(ax, names, strengths), (4.4, 4.0)),
    ]
    for name, draw, size in recipes:
        fig, ax = plt.subplots(figsize=size)
        draw(ax)
        fig.subplots_adjust(left=0.15, right=0.97, bottom=0.22, top=0.80)
        fig.text(0.98, 0.015, "SIMULATED DATA", ha="right", fontsize=7, color=INK_MUTED)
        paths = save_figure(fig, output/name, formats=("png", "pdf", "svg"))
        plt.close(fig)
        print(*paths, sep="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="figures/gallery-examples")
    args = parser.parse_args()
    build_examples(args.output_dir)
