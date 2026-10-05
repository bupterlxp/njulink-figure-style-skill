#!/usr/bin/env python3
"""Generate a synthetic QA figure for the NJU-LINK style helpers.

This demo intentionally uses invented labels and values. It is a toolchain
smoke test, not a reproduction of any paper's data or figure.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from njulink_style import PASTELS, apply_style, draw_pipeline, heatmap, pastel_bars, radar, save_figure


def build_demo():
    apply_style()
    fig = plt.figure(figsize=(10.2, 6.2), constrained_layout=True)
    grid = fig.add_gridspec(2, 3, height_ratios=[1.05, 1.0], wspace=0.28, hspace=0.35)

    pipeline_ax = fig.add_subplot(grid[0, :])
    pipeline_ax.set_title("Synthetic evaluation pipeline", loc="left", pad=4)
    draw_pipeline(
        pipeline_ax,
        [
            {"label": "Source", "title": "Collect", "body": "documents\n+metadata"},
            {"label": "Filter", "title": "Normalize", "body": "deduplicate\n+quality"},
            {"label": "Model", "title": "Inspect", "body": "retrieve\n+reason"},
            {"label": "Audit", "title": "Score", "body": "human\n+check"},
            {"label": "Report", "title": "Release", "body": "metrics\n+limits"},
        ],
        x0=0.025,
        width=0.15,
        gap=0.035,
        y=0.25,
        height=0.44,
    )

    radar_ax = fig.add_subplot(grid[1, 0], projection="polar")
    radar_ax.set_title("Multi-axis comparison", loc="left", pad=16)
    radar(
        radar_ax,
        ["Recall", "Precision", "Robustness", "Cost", "Traceability", "Coverage"],
        {
            "Model A": [0.77, 0.70, 0.81, 0.55, 0.74, 0.68],
            "Model B": [0.65, 0.83, 0.69, 0.72, 0.61, 0.79],
            "Model C": [0.58, 0.62, 0.88, 0.77, 0.86, 0.63],
        },
    )

    bar_ax = fig.add_subplot(grid[1, 1])
    bar_ax.set_title("Category statistics", loc="left", pad=4)
    pastel_bars(
        bar_ax,
        ["Plan", "Search", "Extract", "Verify", "Report"],
        [34, 51, 43, 27, 18],
        annotate=True,
        color=PASTELS[0],
        rotation=25,
    )
    bar_ax.set_ylabel("count")

    heatmap_ax = fig.add_subplot(grid[1, 2])
    heatmap_ax.set_title("Error map", loc="left", pad=4)
    heatmap(
        heatmap_ax,
        np.array([[0.8, 0.2, 0.5], [0.3, 0.9, 0.4], [0.6, 0.4, 0.7]]),
        row_labels=["A", "B", "C"],
        col_labels=["x", "y", "z"],
        fmt=".1f",
    )

    return fig


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="./demo-output")
    args = parser.parse_args()
    fig = build_demo()
    outputs = save_figure(fig, Path(args.output_dir) / "njulink-style-demo")
    plt.close(fig)
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
