"""Reusable Matplotlib primitives for the NJU-LINK figure grammar.

The helpers deliberately draw an observable visual grammar rather than copying
source figures. They accept synthetic or user-owned data and keep the palette,
line weights, rounded cards, radar charts, and export settings consistent.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


INK = "#242424"
INK_MUTED = "#686868"
LINE = "#7F7F7F"
GRID = "#D8D8D8"
PAPER = "#FFFFFF"
PANEL = "#FAFAF8"
PASTELS = [
    "#57BDB5",
    "#85B9E2",
    "#B6A4D8",
    "#E5A1AF",
    "#F39A83",
    "#F4C6A5",
    "#E6C35C",
    "#A9C995",
]
STATUS = {"error": "#D95F5F", "success": "#58A889", "warning": "#E6C35C", "info": "#5B8CCB"}


def apply_style() -> None:
    """Apply portable defaults; call before creating the figure."""

    plt.rcParams.update(
        {
            "figure.facecolor": PAPER,
            "figure.edgecolor": PAPER,
            "savefig.facecolor": PAPER,
            "savefig.edgecolor": PAPER,
            "savefig.dpi": 300,
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
            "font.size": 8,
            "axes.titlesize": 10,
            "axes.titleweight": "semibold",
            "axes.labelsize": 8,
            "axes.labelcolor": INK,
            "axes.edgecolor": LINE,
            "axes.linewidth": 0.8,
            "axes.facecolor": PAPER,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "grid.alpha": 0.58,
            "xtick.color": INK_MUTED,
            "ytick.color": INK_MUTED,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "legend.frameon": False,
            "legend.fontsize": 7.5,
            "legend.handlelength": 1.8,
            "legend.handletextpad": 0.45,
            "lines.linewidth": 1.6,
            "lines.markersize": 4.0,
            "patch.linewidth": 0.8,
            "patch.edgecolor": LINE,
            "text.color": INK,
            "axes.prop_cycle": plt.cycler(color=PASTELS),
        }
    )


def pastel(index: int, alpha: float = 1.0) -> tuple[str, float]:
    """Return a stable categorical color, cycling through the pastel palette."""

    return PASTELS[index % len(PASTELS)], alpha


def add_card(
    ax: Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    facecolor: str = PAPER,
    edgecolor: str = LINE,
    alpha: float = 1.0,
    linestyle: str = "-",
    linewidth: float = 1.25,
    radius: float = 0.04,
    label: str | None = None,
    title: str | None = None,
    title_color: str = INK,
    zorder: int = 2,
) -> FancyBboxPatch:
    """Add a rounded modular card in axes coordinates."""

    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        transform=ax.transAxes,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        linestyle=linestyle,
        alpha=alpha,
        zorder=zorder,
    )
    ax.add_patch(patch)
    if label:
        ax.text(
            xy[0] + 0.018,
            xy[1] + height - 0.045,
            label,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=8.2,
            fontweight="semibold",
            color=title_color,
            zorder=zorder + 1,
        )
    if title:
        ax.text(
            xy[0] + 0.018,
            xy[1] + height - 0.09,
            title,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=7.4,
            color=INK_MUTED,
            zorder=zorder + 1,
        )
    return patch


def add_step_badge(
    ax: Axes,
    x: float,
    y: float,
    text: str,
    *,
    color: str = INK,
    radius: float = 0.022,
    fontsize: float = 7.4,
) -> None:
    """Draw the filled numbered circles used for pipeline stages."""

    # ``s`` is measured in points² while ``radius`` is expressed in axes
    # coordinates; the floor keeps small badges legible in narrow panels.
    size = max(26.0, (radius * 2600) ** 2 / 100)
    ax.scatter([x], [y], transform=ax.transAxes, s=size, c=[color], zorder=6)
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color=PAPER,
        zorder=7,
    )


def add_arrow(
    ax: Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = INK,
    linewidth: float = 1.5,
    linestyle: str = "-",
    mutation_scale: float = 10,
    connectionstyle: str = "arc3,rad=0",
) -> FancyArrowPatch:
    """Draw a compact filled arrow between two axes-coordinate points."""

    arrow = FancyArrowPatch(
        start,
        end,
        transform=ax.transAxes,
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=linewidth,
        linestyle=linestyle,
        color=color,
        connectionstyle=connectionstyle,
        shrinkA=3,
        shrinkB=3,
        zorder=5,
    )
    ax.add_patch(arrow)
    return arrow


def draw_pipeline(
    ax: Axes,
    stages: Sequence[Mapping[str, str]],
    *,
    y: float = 0.32,
    x0: float = 0.04,
    width: float = 0.15,
    height: float = 0.30,
    gap: float = 0.035,
    colors: Sequence[str] = PASTELS,
) -> None:
    """Draw a left-to-right rounded-card pipeline.

    Each stage mapping may contain ``label``, ``title``, and ``body``. The
    function intentionally leaves room for caller-provided icons or mini plots.
    """

    positions = []
    for i, stage in enumerate(stages):
        x = x0 + i * (width + gap)
        positions.append(x)
        color = colors[i % len(colors)]
        add_card(
            ax,
            (x, y),
            width,
            height,
            facecolor=color,
            edgecolor=color,
            alpha=0.18,
            # The pipeline header is drawn below so the badge has its own
            # horizontal slot and cannot collide with a long stage label.
            label=None,
            title=None,
            radius=0.035,
        )
        add_step_badge(ax, x + 0.028, y + height - 0.040, str(i + 1), color=color)
        label = stage.get("label", "")
        if label:
            ax.text(
                x + 0.060,
                y + height - 0.040,
                label,
                transform=ax.transAxes,
                ha="left",
                va="center",
                fontsize=7.4,
                fontweight="semibold",
                color=INK,
                zorder=7,
            )
        title = stage.get("title")
        if title:
            ax.text(
                x + 0.018,
                y + height - 0.092,
                title,
                transform=ax.transAxes,
                ha="left",
                va="top",
                fontsize=7.1,
                color=INK_MUTED,
                zorder=7,
            )
        body = stage.get("body", "")
        if body:
            ax.text(
                x + width / 2,
                y + height * 0.42,
                body,
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=7.1,
                color=INK,
                wrap=True,
                zorder=4,
            )
    for left, right in zip(positions, positions[1:]):
        add_arrow(ax, (left + width + 0.006, y + height / 2), (right - 0.006, y + height / 2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def radar(
    ax: Axes,
    labels: Sequence[str],
    series: Mapping[str, Sequence[float]],
    *,
    colors: Sequence[str] = PASTELS,
    ylim: tuple[float, float] = (0.0, 1.0),
    fill_alpha: float = 0.08,
    grid_ticks: int = 4,
) -> None:
    """Draw a pastel, lightly filled radar chart."""

    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(*ylim)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=7.1, color=INK)
    ax.set_yticks(np.linspace(ylim[0], ylim[1], grid_ticks + 1)[1:])
    ax.set_yticklabels([])
    ax.grid(color=GRID, linewidth=0.65, alpha=0.72)
    ax.spines["polar"].set_color(LINE)
    ax.spines["polar"].set_linewidth(0.75)
    for i, (name, values) in enumerate(series.items()):
        vals = list(values) + [values[0]]
        color = colors[i % len(colors)]
        ax.plot(angles, vals, color=color, linewidth=1.45, marker="o", markersize=2.8, label=name)
        ax.fill(angles, vals, color=color, alpha=fill_alpha, linewidth=0)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.34), ncol=min(4, len(series)), frameon=False)


def pastel_bars(
    ax: Axes,
    categories: Sequence[str],
    values: Sequence[float] | np.ndarray,
    *,
    labels: Sequence[str] | None = None,
    color: str | None = None,
    colors: Sequence[str] = PASTELS,
    width: float = 0.64,
    annotate: bool = False,
    rotation: float = 0,
) -> None:
    """Draw a clean pastel bar chart with optional value annotations."""

    arr = np.asarray(values)
    x = np.arange(len(categories))
    if arr.ndim == 1:
        bars = ax.bar(x, arr, width=width, color=color or colors[0], edgecolor="none")
        if annotate:
            for bar, value in zip(bars, arr):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value:g}", ha="center", va="bottom", fontsize=6.8, color=INK_MUTED)
    else:
        n = arr.shape[1]
        group_width = width
        bar_width = group_width / n
        for j in range(n):
            offset = (j - (n - 1) / 2) * bar_width
            bars = ax.bar(x + offset, arr[:, j], width=bar_width * 0.9, color=colors[j % len(colors)], edgecolor="none", label=labels[j] if labels else None)
            if annotate:
                for bar, value in zip(bars, arr[:, j]):
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value:g}", ha="center", va="bottom", fontsize=6.5, color=INK_MUTED)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=rotation, ha="right" if rotation else "center")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(LINE)
    ax.spines["bottom"].set_color(LINE)


def heatmap(
    ax: Axes,
    data: Sequence[Sequence[float]],
    *,
    row_labels: Sequence[str] | None = None,
    col_labels: Sequence[str] | None = None,
    cmap: str = "RdYlBu_r",
    annotate: bool = True,
    fmt: str = ".2f",
) -> None:
    """Draw a compact annotated heatmap with subtle cell boundaries."""

    arr = np.asarray(data, dtype=float)
    im = ax.imshow(arr, cmap=cmap, aspect="auto")
    ax.set_xticks(np.arange(arr.shape[1]))
    ax.set_yticks(np.arange(arr.shape[0]))
    if col_labels is not None:
        ax.set_xticklabels(col_labels, rotation=45, ha="right", fontsize=6.8)
    if row_labels is not None:
        ax.set_yticklabels(row_labels, fontsize=6.8)
    ax.set_xticks(np.arange(-0.5, arr.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, arr.shape[0], 1), minor=True)
    ax.grid(which="minor", color=PAPER, linewidth=0.55)
    ax.tick_params(which="minor", bottom=False, left=False)
    if annotate:
        midpoint = np.nanmean(arr)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                value = arr[i, j]
                if np.isnan(value):
                    continue
                ax.text(j, i, format(value, fmt), ha="center", va="center", fontsize=6.2, color=PAPER if value > midpoint else INK)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return im


def save_figure(fig: Figure, path: str | Path, *, formats: Iterable[str] = ("png", "pdf"), dpi: int = 300) -> list[Path]:
    """Save the same figure in raster and vector formats."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for ext in formats:
        out = target.with_suffix(f".{ext.lstrip('.')}")
        fig.savefig(out, dpi=dpi, bbox_inches="tight", pad_inches=0.09)
        saved.append(out)
    return saved
