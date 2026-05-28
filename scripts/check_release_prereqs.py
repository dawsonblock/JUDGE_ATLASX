#!/usr/bin/env python3
"""Strict release prerequisite checks for Waveform Brain."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_REPORTS = [
    "reports/preboard_local_summary.json",
    "reports/preboard_local_summary.md",
    "reports/implementation_gate_summary.json",
    "reports/implementation_gate_summary.md",
    "reports/axilite_regfile_sim_summary.json",
    "reports/packer_axis_sim_summary.json",
    "reports/cdc_critical_summary.json",
    "reports/cdc_cell_match_summary.md",
    "reports/timing_summary.rpt",
    "reports/drc.rpt",
]

SIM_REPORTS = [
    "reports/axilite_regfile_sim_summary.json",
    "reports/packer_axis_sim_summary.json",
]


def fail(msg: str) -> int:
    print(f"release-prereq-fail: {msg}")
    return 1


def require_tools() -> int:
    missing = [tool for tool in ["iverilog", "vvp"] if shutil.which(tool) is None]
    if missing:
        return fail("missing simulator tools for release flow: " + ", ".join(missing))
    return 0


def require_reports() -> int:
    missing = [rel for rel in REQUIRED_REPORTS if not (PROJECT_ROOT / rel).exists()]
    if missing:
        print("release-prereq-fail: missing required reports:")
        for rel in missing:
            print(f"  {rel}")
        return 1
    return 0


def require_preboard_pass() -> int:
    path = PROJECT_ROOT / "reports/preboard_local_summary.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    if not bool(data.get("pass", False)):
        return fail("preboard_local_summary.json reports pass=false")

    checks = data.get("checks", [])
    cosim_checks = [
        item
        for item in checks
        if "scripts/run_gkp_cosim.py" in " ".join(item.get("cmd", []))
    ]
    if not cosim_checks:
        return fail("no run_gkp_cosim check found in preboard summary")

    latest = cosim_checks[-1]
    if not bool(latest.get("required", False)):
        return fail(
            "run_gkp_cosim was optional during preboard; " "release requires it"
        )
    if not bool(latest.get("raw_pass", False)):
        return fail("run_gkp_cosim did not pass in preboard summary")

    return 0


def require_implementation_pass() -> int:
    path = PROJECT_ROOT / "reports/implementation_gate_summary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not bool(data.get("pass", False)):
        return fail("implementation_gate_summary.json reports pass=false")
    return 0


def require_simulation_pass() -> int:
    for rel in SIM_REPORTS:
        path = PROJECT_ROOT / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        if not bool(data.get("pass", False)):
            return fail(f"{rel} reports pass=false")
    return 0


def main() -> int:
    for check in [
        require_tools,
        require_reports,
        require_preboard_pass,
        require_implementation_pass,
        require_simulation_pass,
    ]:
        rc = check()
        if rc != 0:
            return rc

    print("release-prereq-pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
