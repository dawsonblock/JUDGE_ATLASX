#!/usr/bin/env python3
"""Compile and run AXI-Lite register file behavioral simulation."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=PROJECT_ROOT, text=True)
    return proc.returncode


def main() -> int:
    if shutil.which("iverilog") is None or shutil.which("vvp") is None:
        print(
            "ERROR: iverilog/vvp not found. "
            "Install Icarus Verilog or use Vivado xsim."
        )
        return 2

    build_dir = PROJECT_ROOT / "sim" / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    out = build_dir / "tb_axilite_regfile_full.vvp"
    rc = run(
        [
            "iverilog",
            "-g2012",
            "-Wall",
            "-o",
            str(out),
            "sim/tb_axilite_regfile_full.sv",
            "rtl/axilite_regfile_full.v",
        ]
    )
    if rc != 0:
        return rc

    return run(["vvp", str(out)])


if __name__ == "__main__":
    raise SystemExit(main())
