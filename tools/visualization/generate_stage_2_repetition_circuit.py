"""Generate the Stage 2 repetition-code circuit with Qiskit.

Run with:
    uv run --project tools/visualization \
        python tools/visualization/generate_stage_2_repetition_circuit.py
"""

from __future__ import annotations

import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
OUTPUT_DIR = PROJECT_ROOT / "docs" / "learning" / "02-general-qec" / "assets"

os.environ.setdefault("MPLCONFIGDIR", str(SCRIPT_DIR / ".matplotlib"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from qiskit import QuantumCircuit  # noqa: E402


def build_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(3, 1)

    # Prepare |+00>.
    circuit.h(0)

    # Encode: Q1 controls Q2, then Q3.
    circuit.cx(0, 1)
    circuit.cx(0, 2)

    # Undo the encoding in reverse order.
    circuit.cx(0, 2)
    circuit.cx(0, 1)

    # X-basis measurement of Q1: H followed by a standard Z readout.
    circuit.h(0)
    circuit.measure(0, 0)

    return circuit


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "three-qubit-encode-decode"

    figure = build_circuit().draw(
        output="mpl",
        fold=-1,
        idle_wires=True,
        scale=1.5,
    )
    figure.savefig(
        output.with_suffix(".svg"),
        bbox_inches="tight",
        pad_inches=0.05,
        facecolor="white",
    )
    figure.savefig(
        output.with_suffix(".png"),
        bbox_inches="tight",
        pad_inches=0.05,
        dpi=300,
        facecolor="white",
    )
    plt.close(figure)

    print(f"Generated {output.with_suffix('.svg')}")
    print(f"Generated {output.with_suffix('.png')}")


if __name__ == "__main__":
    main()
