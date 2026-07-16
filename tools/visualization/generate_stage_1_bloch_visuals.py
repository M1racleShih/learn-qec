"""Regenerate the reusable Stage 1 Bloch-sphere learning visuals with QuTiP.

Run with:
    uv run --project tools/visualization \
        python tools/visualization/generate_stage_1_bloch_visuals.py

The script intentionally keeps single-qubit geometry and multi-qubit
correlations in separate visual regions. A Bloch sphere can show a single
qubit's local state, but cannot by itself show Bell-pair correlations.
"""

from __future__ import annotations

import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
OUTPUT_DIR = (
    PROJECT_ROOT / "docs" / "learning" / "01-minimum-quantum-knowledge" / "assets"
)

os.environ.setdefault("MPLCONFIGDIR", str(SCRIPT_DIR / ".matplotlib"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
from qutip import Bloch  # noqa: E402


INK = "#0f172a"
MUTED = "#475569"
GRID = "#94a3b8"
BLUE = "#2563eb"
BLUE_LIGHT = "#dbeafe"
ORANGE = "#ea580c"
ORANGE_LIGHT = "#ffedd5"
GREEN = "#16a34a"
GREEN_LIGHT = "#dcfce7"
RED = "#dc2626"
RED_LIGHT = "#fee2e2"
PURPLE = "#7c3aed"
PURPLE_LIGHT = "#f3e8ff"
CANVAS = "#f8fafc"
CARD = "#ffffff"


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "DejaVu Sans"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
        }
    )


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
    zorder: int = 0,
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
            zorder=zorder,
        )
    )


def add_arrow(
    fig: plt.Figure,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = ORANGE,
    linewidth: float = 2.5,
    connectionstyle: str = "arc3",
) -> None:
    fig.add_artist(
        FancyArrowPatch(
            start,
            end,
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=linewidth,
            color=color,
            connectionstyle=connectionstyle,
            zorder=4,
        )
    )


def draw_bloch(
    fig: plt.Figure,
    position: list[float],
    *,
    vectors: list[list[float]] | None = None,
    vector_colors: list[str] | None = None,
    trajectories: list[tuple[np.ndarray, str]] | None = None,
    center_color: str | None = None,
    view: list[float] | None = None,
) -> None:
    ax = fig.add_axes(position, projection="3d", zorder=2)
    sphere = Bloch(fig=fig, axes=ax, view=view or [-58, 24])
    sphere.sphere_color = BLUE_LIGHT
    sphere.sphere_alpha = 0.09
    sphere.frame_color = GRID
    sphere.frame_alpha = 0.22
    sphere.frame_width = 0.8
    sphere.axis_color = "#64748b"
    sphere.axis_width = 1.0
    sphere.vector_width = 5
    sphere.vector_mutation = 18
    sphere.font_color = INK
    sphere.font_size = 12
    sphere.xlabel = ["+X", "−X"]
    sphere.ylabel = ["+Y", "−Y"]
    sphere.zlabel = [r"$|0\rangle$", r"$|1\rangle$"]

    if vectors:
        sphere.add_vectors(vectors, colors=vector_colors)
    for trajectory, color in trajectories or []:
        sphere.add_points(
            trajectory,
            meth="l",
            colors=[color],
            alpha=0.95,
            linewidth=3.0,
        )
    if center_color:
        sphere.add_points(
            np.array([0.0, 0.0, 0.0]),
            colors=[center_color],
            alpha=1.0,
            s=95,
        )
    sphere.render()


def save_figure(fig: plt.Figure, stem: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / stem
    svg_path = output.with_suffix(".svg")
    fig.savefig(svg_path, facecolor=CANVAS)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(output.with_suffix(".png"), dpi=180, facecolor=CANVAS)
    plt.close(fig)
    print(f"Generated {output.with_suffix('.svg')}")
    print(f"Generated {output.with_suffix('.png')}")


def add_measurement_row(
    fig: plt.Figure,
    x: float,
    y: float,
    width: float,
    *,
    source: str,
    result: str,
    color: str,
    fill: str,
) -> None:
    add_card(
        fig,
        x,
        y,
        width,
        0.052,
        facecolor=fill,
        edgecolor=color,
        linewidth=1.2,
        radius=0.009,
    )
    fig.text(
        x + 0.025,
        y + 0.026,
        source,
        ha="left",
        va="center",
        fontsize=13.5,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        x + width - 0.025,
        y + 0.026,
        result,
        ha="right",
        va="center",
        fontsize=13,
        color=color,
    )


def generate_basis_figure() -> None:
    fig = plt.figure(figsize=(16, 10), facecolor=CANVAS)
    fig.text(
        0.5,
        0.966,
        "Bloch Sphere：Z basis 与 X basis 是两组不同方向",
        ha="center",
        va="center",
        fontsize=26,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.5,
        0.931,
        "状态方向与 measurement axis 对齐时结果确定；垂直时结果 50/50",
        ha="center",
        va="center",
        fontsize=15,
        color=MUTED,
    )

    add_card(fig, 0.04, 0.50, 0.92, 0.395, edgecolor="#93c5fd")
    fig.text(
        0.065,
        0.865,
        "1 · 球面上的四个纯态，以及一个 classical mixture",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#1d4ed8",
    )

    positions = [0.025, 0.22, 0.415, 0.61, 0.805]
    sphere_y = 0.575
    sphere_w = 0.17
    sphere_h = 0.235
    states = [
        (r"$|0\rangle$", "Z 轴北极", [[0, 0, 1]], [RED], None),
        (r"$|1\rangle$", "Z 轴南极", [[0, 0, -1]], [RED], None),
        (r"$|+\rangle$", "X 轴 +X 端", [[1, 0, 0]], [BLUE], None),
        (r"$|-\rangle$", "X 轴 −X 端", [[-1, 0, 0]], [BLUE], None),
        ("50/50 mixture", "球心：没有纯态方向", None, None, PURPLE),
    ]
    for x, (title, subtitle, vectors, colors, center_color) in zip(
        positions, states, strict=True
    ):
        draw_bloch(
            fig,
            [x, sphere_y, sphere_w, sphere_h],
            vectors=vectors,
            vector_colors=colors,
            center_color=center_color,
        )
        fig.text(
            x + sphere_w / 2,
            0.825,
            title,
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
            color=INK,
        )
        fig.text(
            x + sphere_w / 2,
            0.535,
            subtitle,
            ha="center",
            va="center",
            fontsize=12.5,
            color=MUTED,
        )

    fig.text(
        0.89,
        0.845,
        r"它不是 $|+\rangle$",
        ha="center",
        va="center",
        fontsize=12.5,
        color=PURPLE,
    )

    add_card(fig, 0.045, 0.09, 0.44, 0.365, edgecolor="#fdba74")
    add_card(fig, 0.515, 0.09, 0.44, 0.365, edgecolor="#93c5fd")
    fig.text(
        0.07,
        0.425,
        "2 · Z measurement：询问北极还是南极",
        ha="left",
        va="center",
        fontsize=17,
        fontweight="bold",
        color="#9a3412",
    )
    fig.text(
        0.54,
        0.425,
        "3 · X measurement：询问 +X 端还是 −X 端",
        ha="left",
        va="center",
        fontsize=17,
        fontweight="bold",
        color="#1d4ed8",
    )

    add_measurement_row(
        fig,
        0.07,
        0.335,
        0.39,
        source=r"输入 $|0\rangle$",
        result="bit 0 / +1：确定",
        color="#9a3412",
        fill=ORANGE_LIGHT,
    )
    add_measurement_row(
        fig,
        0.07,
        0.268,
        0.39,
        source=r"输入 $|1\rangle$",
        result="bit 1 / −1：确定",
        color="#9a3412",
        fill=ORANGE_LIGHT,
    )
    add_measurement_row(
        fig,
        0.07,
        0.201,
        0.39,
        source=r"输入 $|+\rangle$ 或 $|-\rangle$",
        result="bit 0/1：各 50%",
        color="#9a3412",
        fill="#fff7ed",
    )

    add_measurement_row(
        fig,
        0.54,
        0.335,
        0.39,
        source=r"输入 $|+\rangle$",
        result="+1：确定",
        color="#1d4ed8",
        fill=BLUE_LIGHT,
    )
    add_measurement_row(
        fig,
        0.54,
        0.268,
        0.39,
        source=r"输入 $|-\rangle$",
        result="−1：确定",
        color="#1d4ed8",
        fill=BLUE_LIGHT,
    )
    add_measurement_row(
        fig,
        0.54,
        0.201,
        0.39,
        source=r"输入 $|0\rangle$ 或 $|1\rangle$",
        result="+1/−1：各 50%",
        color="#1d4ed8",
        fill="#eff6ff",
    )

    fig.text(
        0.5,
        0.125,
        "basis 是测量方向，不是给同一个状态换名字。",
        ha="center",
        va="center",
        fontsize=15,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.5,
        0.055,
        r"真正的 $|+\rangle$ 位于 +X；随机制备 $|0\rangle$/$|1\rangle$ 的 mixture 位于球心。",
        ha="center",
        va="center",
        fontsize=12,
        color=MUTED,
    )

    save_figure(fig, "bloch-sphere-z-x-basis")


def add_pauli_summary_row(
    fig: plt.Figure,
    y: float,
    *,
    error: str,
    color: str,
    fill: str,
    local_effect: str,
    changed_info: str,
    check_effect: str,
) -> None:
    add_card(
        fig,
        0.07,
        y,
        0.86,
        0.063,
        facecolor=fill,
        edgecolor=color,
        linewidth=1.1,
        radius=0.007,
    )
    fig.text(0.105, y + 0.0315, error, ha="center", va="center", fontsize=16, fontweight="bold", color=color)
    fig.text(0.205, y + 0.0315, local_effect, ha="left", va="center", fontsize=13, color=INK)
    fig.text(0.50, y + 0.0315, changed_info, ha="center", va="center", fontsize=13, color=INK)
    fig.text(0.785, y + 0.0315, check_effect, ha="center", va="center", fontsize=13, color=INK)


def generate_pauli_figure() -> None:
    fig = plt.figure(figsize=(16, 11), facecolor=CANVAS)
    fig.text(
        0.5,
        0.966,
        "Pauli X、Y、Z：绕对应 Bloch axis 旋转 180°",
        ha="center",
        va="center",
        fontsize=26,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.5,
        0.931,
        "先看单 Qubit 的旋转，再看它会翻转哪一种 QEC relationship check",
        ha="center",
        va="center",
        fontsize=15,
        color=MUTED,
    )

    add_card(fig, 0.04, 0.47, 0.92, 0.425, edgecolor="#cbd5e1")
    fig.text(
        0.065,
        0.866,
        "1 · 三种 Pauli error 的几何动作",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color=INK,
    )

    theta = np.linspace(0, np.pi, 80)
    x_path = np.vstack([np.zeros_like(theta), -np.sin(theta), np.cos(theta)])
    z_path = np.vstack([np.cos(theta), np.sin(theta), np.zeros_like(theta)])
    y_path = np.vstack([np.sin(theta), np.zeros_like(theta), np.cos(theta)])

    panels = [
        (
            0.07,
            "Pauli X",
            "绕 X 轴：Z 北极 ↔ Z 南极",
            [[0, 0, 1], [0, 0, -1]],
            x_path,
            BLUE,
            r"$|0\rangle \leftrightarrow |1\rangle$",
            "Z measurement 结果会变",
        ),
        (
            0.39,
            "Pauli Z",
            "绕 Z 轴：+X 端 ↔ −X 端",
            [[1, 0, 0], [-1, 0, 0]],
            z_path,
            RED,
            r"$|+\rangle \leftrightarrow |-\rangle$",
            "X measurement 结果会变",
        ),
        (
            0.71,
            "Pauli Y",
            "绕 Y 轴：同时改变 X、Z 方向",
            [[0, 0, 1], [0, 0, -1]],
            y_path,
            PURPLE,
            "bit 与 phase 两类关系都变",
            "XX、ZZ 两类 check 都可能报警",
        ),
    ]
    for x, title, subtitle, vectors, path, color, state_change, info_change in panels:
        fig.text(
            x + 0.11,
            0.825,
            title,
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
            color=color,
        )
        fig.text(
            x + 0.11,
            0.795,
            subtitle,
            ha="center",
            va="center",
            fontsize=12.5,
            color=MUTED,
        )
        draw_bloch(
            fig,
            [x, 0.555, 0.22, 0.23],
            vectors=vectors,
            vector_colors=["#64748b", color],
            trajectories=[(path, color)],
        )
        fig.text(
            x + 0.11,
            0.525,
            state_change,
            ha="center",
            va="center",
            fontsize=13.5,
            fontweight="bold",
            color=color,
        )
        fig.text(
            x + 0.11,
            0.495,
            info_change,
            ha="center",
            va="center",
            fontsize=12,
            color=MUTED,
        )

    add_card(fig, 0.045, 0.08, 0.91, 0.345, edgecolor="#cbd5e1")
    fig.text(
        0.07,
        0.396,
        "2 · 从 Bloch rotation 到 QEC syndrome",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color=INK,
    )
    fig.text(0.105, 0.357, "Error", ha="center", va="center", fontsize=13, fontweight="bold", color=MUTED)
    fig.text(0.205, 0.357, "单 Qubit 变化", ha="left", va="center", fontsize=13, fontweight="bold", color=MUTED)
    fig.text(0.50, 0.357, "被改变的信息", ha="center", va="center", fontsize=13, fontweight="bold", color=MUTED)
    fig.text(0.785, 0.357, "对应的 relationship check", ha="center", va="center", fontsize=13, fontweight="bold", color=MUTED)

    add_pauli_summary_row(
        fig,
        0.278,
        error="X",
        color=BLUE,
        fill="#eff6ff",
        local_effect=r"$|0\rangle \leftrightarrow |1\rangle$",
        changed_info="Z result 翻转",
        check_effect="ZZ 翻转（anticommute）",
    )
    add_pauli_summary_row(
        fig,
        0.202,
        error="Z",
        color=RED,
        fill="#fff7ed",
        local_effect=r"$|+\rangle \leftrightarrow |-\rangle$",
        changed_info="X result 翻转",
        check_effect="XX 翻转（anticommute）",
    )
    add_pauli_summary_row(
        fig,
        0.126,
        error="Y",
        color=PURPLE,
        fill="#faf5ff",
        local_effect="同时具有 X、Z 两类作用",
        changed_info="X、Z result 都会翻转",
        check_effect="与该 Qubit 相交的 XX、ZZ check 都翻转",
    )
    fig.text(
        0.5,
        0.047,
        "旋转轴上的状态留在同一个 Bloch 点；这里关注的是 measurement 结果与 relationship check 是否改变。",
        ha="center",
        va="center",
        fontsize=11.5,
        color=MUTED,
    )

    save_figure(fig, "pauli-rotations-bloch-sphere")


def add_bell_relation_card(
    fig: plt.Figure,
    x: float,
    *,
    title: str,
    outcomes: str,
    forbidden: str,
    relation: str,
    color: str,
    fill: str,
) -> None:
    add_card(
        fig,
        x,
        0.285,
        0.40,
        0.18,
        facecolor=fill,
        edgecolor=color,
        linewidth=1.5,
        radius=0.012,
    )
    fig.text(x + 0.20, 0.425, title, ha="center", va="center", fontsize=17, fontweight="bold", color=color)
    fig.text(x + 0.20, 0.385, outcomes, ha="center", va="center", fontsize=15, fontweight="bold", color=INK)
    fig.text(x + 0.20, 0.348, forbidden, ha="center", va="center", fontsize=12.5, color=MUTED)
    fig.text(x + 0.20, 0.312, relation, ha="center", va="center", fontsize=14, fontweight="bold", color=color)


def generate_bell_figure() -> None:
    fig = plt.figure(figsize=(16, 10), facecolor=CANVAS)
    fig.text(
        0.5,
        0.966,
        r"Bell Pair $|\Phi^+\rangle$：单独看在球心，联合看关系确定",
        ha="center",
        va="center",
        fontsize=26,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.5,
        0.931,
        "Bloch Sphere 描述单 Qubit；Entanglement 必须从 A、B 的联合统计中观察",
        ha="center",
        va="center",
        fontsize=15,
        color=MUTED,
    )

    add_card(fig, 0.04, 0.50, 0.92, 0.395, edgecolor="#c4b5fd")
    fig.text(
        0.065,
        0.865,
        "1 · 分别只看 A 或 B",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color=PURPLE,
    )
    fig.text(
        0.065,
        0.835,
        "球心表示没有任何单独的 X、Y、Z 偏向：测量结果都是随机的。",
        ha="left",
        va="center",
        fontsize=13.5,
        color=MUTED,
    )

    draw_bloch(fig, [0.12, 0.555, 0.25, 0.235], center_color=BLUE)
    draw_bloch(fig, [0.63, 0.555, 0.25, 0.235], center_color=RED)
    fig.text(0.245, 0.805, "Qubit A alone", ha="center", va="center", fontsize=16, fontweight="bold", color=BLUE)
    fig.text(0.755, 0.805, "Qubit B alone", ha="center", va="center", fontsize=16, fontweight="bold", color=RED)
    fig.text(0.245, 0.525, "Bloch vector 在球心", ha="center", va="center", fontsize=13, color=MUTED)
    fig.text(0.755, 0.525, "Bloch vector 在球心", ha="center", va="center", fontsize=13, color=MUTED)

    add_card(
        fig,
        0.405,
        0.655,
        0.19,
        0.085,
        facecolor=PURPLE_LIGHT,
        edgecolor=PURPLE,
        linewidth=1.5,
        radius=0.012,
        zorder=5,
    )
    fig.text(0.5, 0.711, "信息在关系里", ha="center", va="center", fontsize=15, fontweight="bold", color=PURPLE, zorder=6)
    fig.text(0.5, 0.681, "不是 A/B 的独立箭头", ha="center", va="center", fontsize=11.5, color=MUTED, zorder=6)
    add_arrow(fig, (0.385, 0.697), (0.405, 0.697), color=PURPLE, linewidth=2.0)
    add_arrow(fig, (0.615, 0.697), (0.595, 0.697), color=PURPLE, linewidth=2.0)

    fig.text(
        0.5,
        0.49,
        "2 · 把 A、B 的结果放在一起比较",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color=INK,
    )
    add_bell_relation_card(
        fig,
        0.07,
        title="两边都做 Z measurement",
        outcomes="00 或 11，各 50%",
        forbidden="不会出现 01、10",
        relation="ZZ = +1：结果始终相同",
        color="#b91c1c",
        fill="#fff7ed",
    )
    add_bell_relation_card(
        fig,
        0.53,
        title="两边都做 X measurement",
        outcomes="++ 或 −−，各 50%",
        forbidden="不会出现 +−、−+",
        relation="XX = +1：结果始终相同",
        color="#1d4ed8",
        fill="#eff6ff",
    )

    add_card(fig, 0.045, 0.075, 0.91, 0.16, edgecolor="#cbd5e1")
    fig.text(
        0.07,
        0.207,
        "3 · 为什么只看 Bloch Sphere 还不够",
        ha="left",
        va="center",
        fontsize=17,
        fontweight="bold",
        color=INK,
    )
    fig.text(0.16, 0.169, "State", ha="center", va="center", fontsize=12.5, fontweight="bold", color=MUTED)
    fig.text(0.39, 0.169, "A/B 单独的球", ha="center", va="center", fontsize=12.5, fontweight="bold", color=MUTED)
    fig.text(0.62, 0.169, "Z relationship", ha="center", va="center", fontsize=12.5, fontweight="bold", color=MUTED)
    fig.text(0.83, 0.169, "X relationship", ha="center", va="center", fontsize=12.5, fontweight="bold", color=MUTED)

    add_card(fig, 0.075, 0.112, 0.85, 0.043, facecolor=PURPLE_LIGHT, edgecolor="#ddd6fe", linewidth=1.0, radius=0.005)
    fig.text(0.16, 0.1335, "Bell Pair", ha="center", va="center", fontsize=12.5, fontweight="bold", color=PURPLE)
    fig.text(0.39, 0.1335, "都在球心", ha="center", va="center", fontsize=12.5, color=INK)
    fig.text(0.62, 0.1335, "始终相同", ha="center", va="center", fontsize=12.5, color=INK)
    fig.text(0.83, 0.1335, "始终相同", ha="center", va="center", fontsize=12.5, color=INK)

    add_card(fig, 0.075, 0.061, 0.85, 0.043, facecolor="#f8fafc", edgecolor="#e2e8f0", linewidth=1.0, radius=0.005)
    fig.text(0.16, 0.0825, "Classical 00/11 mixture", ha="center", va="center", fontsize=11.5, fontweight="bold", color=MUTED)
    fig.text(0.39, 0.0825, "也都在球心", ha="center", va="center", fontsize=12, color=INK)
    fig.text(0.62, 0.0825, "始终相同", ha="center", va="center", fontsize=12, color=INK)
    fig.text(0.83, 0.0825, "相同/不同各 50%", ha="center", va="center", fontsize=12, color=INK)

    fig.text(
        0.5,
        0.025,
        "结论：单 Qubit Bloch Sphere 相同，不代表 two-qubit correlation 相同；必须测量 relationship。",
        ha="center",
        va="center",
        fontsize=11.5,
        color=MUTED,
    )

    save_figure(fig, "bell-pair-correlations")


def main() -> None:
    configure_matplotlib()
    generate_basis_figure()
    generate_pauli_figure()
    generate_bell_figure()


if __name__ == "__main__":
    main()
