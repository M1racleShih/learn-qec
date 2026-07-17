"""Generate the Stage 2 Z-parity-check circuit with Qiskit.

Run with:
    uv run --project tools/visualization \
        python tools/visualization/generate_stage_2_parity_check_circuit.py
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
from qiskit import (  # noqa: E402
    AncillaRegister,
    ClassicalRegister,
    QuantumCircuit,
    QuantumRegister,
)


def build_circuit() -> QuantumCircuit:
    data = QuantumRegister(2, "data")
    ancilla = AncillaRegister(1, "ancilla")
    check = ClassicalRegister(1, "check")
    circuit = QuantumCircuit(data, ancilla, check)

    circuit.reset(ancilla[0])
    circuit.cx(data[0], ancilla[0])
    circuit.cx(data[1], ancilla[0])
    circuit.measure(ancilla[0], check[0])

    return circuit


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "zz-parity-check-circuit"

    figure = build_circuit().draw(
        output="mpl",
        fold=-1,
        idle_wires=True,
        cregbundle=False,
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
