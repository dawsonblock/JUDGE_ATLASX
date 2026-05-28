#!/usr/bin/env python3
"""
Run the GKP decoder RTL/golden co-simulation harness.

Requires Icarus Verilog with SystemVerilog support (`iverilog` and `vvp`).
If the tools are not installed, this script exits with code 2 and explains what
is missing. It is intentionally optional because Vivado simulation may be used
instead.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(cmd, *, cwd: Path) -> int:
    print("+", " ".join(str(c) for c in cmd))
    proc = subprocess.run(cmd, cwd=cwd, text=True)
    return proc.returncode


def main() -> int:
    parser_desc = "Run GKP decoder co-simulation."
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument(
        "--vectors",
        type=Path,
        default=PROJECT_ROOT / "sim" / "gkp_cosim_vectors.hex",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=64,
    )
    parser.add_argument(
        "--profile",
        choices=["default", "edge"],
        default="default",
        help="Vector profile when generating vectors.",
    )
    parser.add_argument(
        "--use-existing-vectors",
        action="store_true",
        help="Skip vector generation and use --vectors as-is.",
    )
    args = parser.parse_args()

    if shutil.which("iverilog") is None or shutil.which("vvp") is None:
        print(
            "ERROR: iverilog/vvp not found. "
            "Install Icarus Verilog or run this harness in Vivado simulator."
        )
        return 2

    build = PROJECT_ROOT / "sim" / "build"
    build.mkdir(parents=True, exist_ok=True)

    if not args.use_existing_vectors:
        # Generate vectors.
        rc = run(
            [
                sys.executable,
                "scripts/generate_gkp_cosim_vectors.py",
                "--out",
                str(args.vectors),
                "--count",
                str(args.count),
                "--profile",
                args.profile,
            ],
            cwd=PROJECT_ROOT,
        )
        if rc != 0:
            return rc
    elif not args.vectors.exists():
        print(f"ERROR: vector file does not exist: {args.vectors}")
        return 2

    # Generate the reciprocal ROM if the compact source package
    # does not contain it.
    rom_src = PROJECT_ROOT / "rtl" / "reciprocal_lut_w16_q24w25.mem"
    if not rom_src.exists():
        rc = run(
            [sys.executable, "scripts/generate_reciprocal_lut.py"],
            cwd=PROJECT_ROOT,
        )
        if rc != 0:
            return rc

    # $readmemh in soft_weighting.v uses the default ROM filename. Make a copy
    # in the project root for simulator working-directory compatibility.
    rom_dst = PROJECT_ROOT / "reciprocal_lut_w16_q24w25.mem"
    if not rom_dst.exists() or rom_dst.read_bytes() != rom_src.read_bytes():
        rom_dst.write_bytes(rom_src.read_bytes())

    out = build / "gkp_cosim.vvp"
    sources = [
        "sim/tb_gkp_decoder_cosim.sv",
        "rtl/gkp_decoder.v",
        "rtl/poly_eval.v",
        "rtl/soft_weighting.v",
    ]

    rc = run(
        ["iverilog", "-g2012", "-Wall", "-o", str(out)] + sources,
        cwd=PROJECT_ROOT,
    )
    if rc != 0:
        return rc

    rc = run(
        ["vvp", str(out), f"+VECTORS={args.vectors}"],
        cwd=PROJECT_ROOT,
    )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
