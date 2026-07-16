"""Generate the Stage 1 visual for an X error flipping a ZZ check.

The figure deliberately separates two ideas:

1. A Bloch sphere explains the local, single-qubit action of an X error.
2. A relation panel explains how that local change flips a two-qubit ZZ check.

Run with:
    uv run --project tools/visualization \
        python tools/visualization/generate_x_error_zz_bloch.py
"""

from __future__ import annotations

import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
OUTPUT_STEM = (
    PROJECT_ROOT
    / "docs"
    / "learning"
    / "01-minimum-quantum-knowledge"
    / "assets"
    / "x-error-flips-zz-bloch"
)

# Matplotlib otherwise tries to write under ~/.config, which is undesirable for
# a repository-local, reproducible tool.
os.environ.setdefault("MPLCONFIGDIR", str(SCRIPT_DIR / ".matplotlib"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
from qutip import Bloch  # noqa: E402


INK = "#0f172a"
MUTED = "#475569"
BLUE = "#2563eb"
BLUE_LIGHT = "#dbeafe"
ORANGE = "#ea580c"
ORANGE_LIGHT = "#ffedd5"
GREEN = "#16a34a"
GREEN_LIGHT = "#dcfce7"
RED = "#dc2626"
RED_LIGHT = "#fee2e2"
CANVAS = "#f8fafc"
CARD = "#ffffff"


def add_card(
    fig: plt.Figure,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    facecolor: str = CARD,
    edgecolor: str = "#cbd5e1",
    linewidth: float = 1.5,
    radius: float = 0.014,
) -> None:
    fig.add_artist(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle=f"round,pad=0.008,rounding_size={radius}",
            transform=fig.transFigure,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            zorder=0,
        )
    )


def add_figure_arrow(
    fig: plt.Figure,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = ORANGE,
    linewidth: float = 2.6,
) -> None:
    fig.add_artist(
        FancyArrowPatch(
            start,
            end,
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=20,
            linewidth=linewidth,
            color=color,
            zorder=4,
        )
    )


def draw_bloch(
    fig: plt.Figure,
    position: list[float],
    vectors: list[list[float]],
    colors: list[str],
    *,
    trajectory: np.ndarray | None = None,
) -> None:
    ax = fig.add_axes(position, projection="3d", zorder=2)
    sphere = Bloch(fig=fig, axes=ax, view=[-58, 24])
    sphere.sphere_color = BLUE_LIGHT
    sphere.sphere_alpha = 0.09
    sphere.frame_color = "#94a3b8"
    sphere.frame_alpha = 0.22
    sphere.frame_width = 0.8
    sphere.axis_color = "#64748b"
    sphere.axis_width = 1.0
    sphere.vector_width = 5
    sphere.vector_mutation = 18
    sphere.font_color = INK
    sphere.font_size = 13
    sphere.xlabel = ["+X", "−X"]
    sphere.ylabel = ["+Y", "−Y"]
    sphere.zlabel = [r"$|0\rangle$", r"$|1\rangle$"]
    sphere.add_vectors(vectors, colors=colors)
    if trajectory is not None:
        sphere.add_points(
            trajectory,
            meth="l",
            colors=[ORANGE],
            alpha=0.95,
            linewidth=3.2,
        )
    sphere.render()


def add_relation_row(
    fig: plt.Figure,
    y: float,
    *,
    before: str,
    after: str,
    change: str,
) -> None:
    add_card(
        fig,
        0.08,
        y,
        0.29,
        0.076,
        facecolor=GREEN_LIGHT,
        edgecolor=GREEN,
        linewidth=1.7,
        radius=0.012,
    )
    add_card(
        fig,
        0.63,
        y,
        0.29,
        0.076,
        facecolor=RED_LIGHT,
        edgecolor=RED,
        linewidth=1.7,
        radius=0.012,
    )
    center_y = y + 0.038
    fig.text(
        0.225,
        center_y + 0.013,
        before,
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.225,
        center_y - 0.017,
        "A、B 相同  →  ZZ = +1",
        ha="center",
        va="center",
        fontsize=14,
        color="#166534",
    )
    fig.text(
        0.775,
        center_y + 0.013,
        after,
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.775,
        center_y - 0.017,
        "A、B 不同  →  ZZ = −1",
        ha="center",
        va="center",
        fontsize=14,
        color="#991b1b",
    )
    add_figure_arrow(fig, (0.395, center_y), (0.605, center_y))
    fig.text(
        0.5,
        center_y + 0.024,
        "X error on A",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#9a3412",
    )
    fig.text(
        0.5,
        center_y - 0.024,
        change,
        ha="center",
        va="center",
        fontsize=12.5,
        color=MUTED,
    )


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "DejaVu Sans"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
        }
    )

    fig = plt.figure(figsize=(16, 11), facecolor=CANVAS)
    fig.text(
        0.5,
        0.966,
        "为什么单个 X error 会把 ZZ 从 +1 翻成 −1？",
        ha="center",
        va="center",
        fontsize=27,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.5,
        0.931,
        "先看单个 Qubit 的几何变化，再看两个 Qubit 的关系变化",
        ha="center",
        va="center",
        fontsize=15.5,
        color=MUTED,
    )

    # Step 1: local single-qubit geometry.
    add_card(fig, 0.045, 0.51, 0.91, 0.385, edgecolor="#93c5fd")
    fig.text(
        0.07,
        0.867,
        "Step 1 · X error 对 A 做了什么？",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#1d4ed8",
    )
    fig.text(
        0.07,
        0.837,
        "在 Bloch Sphere 上，X error 等于绕 X 轴旋转 180°。",
        ha="left",
        va="center",
        fontsize=14,
        color=MUTED,
    )

    sphere_y = 0.565
    sphere_w = 0.22
    sphere_h = 0.245
    draw_bloch(
        fig,
        [0.075, sphere_y, sphere_w, sphere_h],
        [[0, 0, 1]],
        [BLUE],
    )

    theta = np.linspace(0, np.pi, 80)
    rotation_path = np.vstack(
        [np.zeros_like(theta), -np.sin(theta), np.cos(theta)]
    )
    draw_bloch(
        fig,
        [0.39, sphere_y, sphere_w, sphere_h],
        [[0, 0, 1], [0, 0, -1]],
        [BLUE, ORANGE],
        trajectory=rotation_path,
    )
    draw_bloch(
        fig,
        [0.705, sphere_y, sphere_w, sphere_h],
        [[0, 0, -1]],
        [ORANGE],
    )

    fig.text(0.185, 0.815, "A：错误前", ha="center", fontsize=15, fontweight="bold")
    fig.text(0.5, 0.815, "X error 的旋转过程", ha="center", fontsize=15, fontweight="bold")
    fig.text(0.815, 0.815, "A：错误后", ha="center", fontsize=15, fontweight="bold")
    fig.text(
        0.185,
        0.535,
        r"Z 轴北极：$|0\rangle$",
        ha="center",
        fontsize=14,
        color=BLUE,
    )
    fig.text(0.5, 0.535, "蓝色起点 → 橙色终点", ha="center", fontsize=14, color=MUTED)
    fig.text(
        0.815,
        0.535,
        r"Z 轴南极：$|1\rangle$",
        ha="center",
        fontsize=14,
        color=ORANGE,
    )
    add_figure_arrow(fig, (0.305, 0.685), (0.375, 0.685))
    add_figure_arrow(fig, (0.62, 0.685), (0.69, 0.685))

    # Step 2: two-qubit relationship. This is intentionally separate because a
    # single Bloch sphere does not encode Bell-pair correlations.
    add_card(fig, 0.045, 0.075, 0.91, 0.405, edgecolor="#cbd5e1")
    fig.text(
        0.07,
        0.452,
        "Step 2 · ZZ 只比较 A、B 的 Z 结果是否相同",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.07,
        0.422,
        "X 只翻转 A；B 没动，所以原本相同的两个结果必然变得不同。",
        ha="left",
        va="center",
        fontsize=14,
        color=MUTED,
    )

    add_relation_row(
        fig,
        0.295,
        before="错误前：A=0，B=0",
        after="错误后：A=1，B=0",
        change="A：0 → 1；B：保持 0",
    )
    add_relation_row(
        fig,
        0.185,
        before="错误前：A=1，B=1",
        after="错误后：A=0，B=1",
        change="A：1 → 0；B：保持 1",
    )

    add_card(
        fig,
        0.18,
        0.101,
        0.64,
        0.052,
        facecolor=BLUE_LIGHT,
        edgecolor="#60a5fa",
        linewidth=1.5,
        radius=0.011,
    )
    fig.text(
        0.5,
        0.127,
        "一个 Z 结果被翻转：相同 → 不同，因此 ZZ：+1 → −1",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#1e40af",
    )
    fig.text(
        0.5,
        0.045,
        "说明：Bloch Sphere 展示单 Qubit 的旋转；下方关系图展示 ZZ。它不直接表示 Bell Pair 的纠缠。",
        ha="center",
        va="center",
        fontsize=11.5,
        color="#64748b",
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    fig.savefig(svg_path, facecolor=CANVAS)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(OUTPUT_STEM.with_suffix(".png"), dpi=180, facecolor=CANVAS)
    plt.close(fig)

    print(f"Generated {OUTPUT_STEM.with_suffix('.svg')}")
    print(f"Generated {OUTPUT_STEM.with_suffix('.png')}")


if __name__ == "__main__":
    main()
