#!/usr/bin/env python3
"""Compile and run AXI-Stream packet packer stall simulation."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = PROJECT_ROOT / "reports" / "packer_axis_sim_summary.json"
REPORT_MD = PROJECT_ROOT / "reports" / "packer_axis_sim_summary.md"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def write_summary(*, passed: bool, returncode: int, output: str) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    stdout_tail = "\n".join(output.splitlines()[-40:])

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "sim": "packer_axis",
        "pass": passed,
        "returncode": returncode,
        "stdout_tail": stdout_tail,
    }
    REPORT_JSON.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )

    lines: list[str] = [
        "# AXI-Stream Packer Simulation Summary",
        "",
        f"Timestamp UTC: `{summary['timestamp_utc']}`",
        "",
        f"Pass: **{passed}**",
        f"Return code: `{returncode}`",
        "",
        "## Output tail",
        "",
        "```text",
        stdout_tail,
        "```",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if shutil.which("iverilog") is None or shutil.which("vvp") is None:
        msg = (
            "ERROR: iverilog/vvp not found. "
            "Install Icarus Verilog or use Vivado xsim."
        )
        print(msg)
        write_summary(passed=False, returncode=2, output=msg)
        return 2

    build_dir = PROJECT_ROOT / "sim" / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    out = build_dir / "tb_packer_axis_stall.vvp"
    compile_proc = run(
        [
            "iverilog",
            "-g2012",
            "-Wall",
            "-o",
            str(out),
            "sim/tb_packer_axis_stall.sv",
            "rtl/packer_axis.v",
        ]
    )
    print(compile_proc.stdout, end="")
    if compile_proc.returncode != 0:
        write_summary(
            passed=False,
            returncode=compile_proc.returncode,
            output=compile_proc.stdout,
        )
        return compile_proc.returncode

    run_proc = run(["vvp", str(out)])
    print(run_proc.stdout, end="")
    write_summary(
        passed=(run_proc.returncode == 0),
        returncode=run_proc.returncode,
        output=compile_proc.stdout + "\n" + run_proc.stdout,
    )
    return run_proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
