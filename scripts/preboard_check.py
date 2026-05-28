#!/usr/bin/env python3
"""
Waveform Brain v1.0 — Local Pre-Board Check

Runs all non-Vivado checks that can be performed before implementation.

v0.16 correction:
  - Cleans generated compact-package artifacts before static/unit tests.
  - Runs tests before regenerating the reciprocal LUT and co-sim vectors.
  - Prevents test_compact_package.py from failing after generator execution.

This does not prove timing, CDC, or hardware behavior. It verifies that the
source tree is internally consistent, generated artifacts are reproducible, and
the known pre-board inputs exist.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "reports"
SUMMARY_JSON = REPORT_DIR / "preboard_local_summary.json"
SUMMARY_MD = REPORT_DIR / "preboard_local_summary.md"

GENERATED_ARTIFACTS = [
    "rtl/reciprocal_lut_w16_q24w25.mem",
    "reciprocal_lut_w16_q24w25.mem",
    "sim/gkp_cosim_vectors.hex",
    "register_map.json",
    "register_map.md",
    "register_map_issues.log",
    "cdc_crossing_suggestions.json",
    "cdc_crossing_suggestions.md",
]


def clean_generated_artifacts() -> None:
    for rel in GENERATED_ARTIFACTS:
        p = PROJECT_ROOT / rel
        if p.exists():
            p.unlink()


def run(cmd: list[str], *, required: bool = True, timeout: int = 120) -> dict:
    print("+", " ".join(cmd))
    try:
        proc = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        ok = proc.returncode == 0
        if not ok:
            print(proc.stdout)
        return {
            "cmd": cmd,
            "required": required,
            "returncode": proc.returncode,
            "pass": ok if required else True,
            "raw_pass": ok,
            "stdout_tail": "\n".join(proc.stdout.splitlines()[-25:]),
        }
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", errors="replace")
        out += f"\nTimed out after {timeout} seconds."
        print(out)
        return {
            "cmd": cmd,
            "required": required,
            "returncode": 124,
            "pass": False if required else True,
            "raw_pass": False,
            "stdout_tail": "\n".join(out.splitlines()[-25:]),
        }


def exists(rel: str) -> dict:
    p = PROJECT_ROOT / rel
    return {
        "path": rel,
        "exists": p.exists(),
        "size": p.stat().st_size if p.exists() else 0,
    }


def main() -> int:
    REPORT_DIR.mkdir(exist_ok=True)

    # Keep compact-package tests meaningful even if a previous local run left
    # generated artifacts behind.
    clean_generated_artifacts()

    checks = []
    files = []

    required_files = [
        "rtl/waveform_brain_axi4lite_cdc_top.v",
        "rtl/waveform_brain_cdc_wrapper.v",
        "rtl/axilite_regfile_full.v",
        "rtl/soft_weighting.v",
        "rtl/gkp_decoder.v",
        "rtl/poly_eval.v",
        "constraints/cdc_xpm_wrapper_constraints.xdc",
        "scripts/build_gate_cdc.tcl",
        "scripts/verify_cdc_constraints.tcl",
        "scripts/parse_cdc_report.py",
        "scripts/package_cdc_signoff.py",
        "scripts/implementation_gate.py",
        "scripts/package_vivado_signoff.py",
        "docs/PHASE1_SIGNOFF_SHEET.md",
        "docs/CDC_HARDENING_V14.md",
        "docs/PREBOARD_GATE_V15.md",
        "docs/BOARD_READY_TEMPLATE.md",
    ]

    for rel in required_files:
        files.append(exists(rel))

    # 1) Static/unit tests run while generated heavy artifacts are absent.
    checks.append(
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests"])
    )
    checks.append(run([sys.executable, "scripts/rtl_sanity_check.py"]))
    checks.append(run([sys.executable, "scripts/audit_rtl_arithmetic.py"]))

    # 2) Then prove generated artifacts are reproducible.
    checks.append(run([sys.executable, "scripts/generate_reciprocal_lut.py"]))
    checks.append(
        run(
            [
                sys.executable,
                "scripts/generate_gkp_cosim_vectors.py",
                "--count",
                "16",
            ]
        )
    )
    checks.append(run([sys.executable, "scripts/extract_register_map.py"]))
    checks.append(run([sys.executable, "scripts/analyze_cdc_crossings.py"]))

    # 3) Optional co-sim if Icarus exists. This is required only when the tools
    # are installed. Otherwise Vivado xsim can be used later.
    if shutil.which("iverilog") and shutil.which("vvp"):
        checks.append(
            run(
                [sys.executable, "scripts/run_gkp_cosim.py", "--count", "16"],
                required=True,
                timeout=180,
            )
        )
    else:
        checks.append(
            {
                "cmd": ["python3", "scripts/run_gkp_cosim.py"],
                "required": False,
                "returncode": 2,
                "pass": True,
                "raw_pass": False,
                "stdout_tail": (
                    "Skipped: iverilog/vvp not found. "
                    "Use Vivado xsim or install Icarus Verilog."
                ),
            }
        )

    file_pass = all(item["exists"] for item in files)
    check_pass = all(item["pass"] for item in checks)
    overall_pass = file_pass and check_pass

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(PROJECT_ROOT),
        "pass": overall_pass,
        "file_pass": file_pass,
        "check_pass": check_pass,
        "files": files,
        "checks": checks,
        "vivado_required_next": [
            "Vivado elaboration",
            "report_cdc",
            "report_clock_interaction",
            "report_timing_summary",
            "report_drc",
            "report_utilization",
            "Phase 1 sign-off sheet",
        ],
    }

    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# Local Pre-Board Check Summary",
        "",
        f"Timestamp UTC: `{summary['timestamp_utc']}`",
        "",
        f"Overall pass: **{overall_pass}**",
        f"File pass: **{file_pass}**",
        f"Check pass: **{check_pass}**",
        "",
        "## Required files",
        "",
        "| File | Exists | Size |",
        "|---|---:|---:|",
    ]
    for f in files:
        lines.append(f"| `{f['path']}` | {f['exists']} | {f['size']} |")

    lines += [
        "",
        "## Checks",
        "",
        "| Command | Required | Raw pass | Gate pass |",
        "|---|---:|---:|---:|",
    ]
    for c in checks:
        lines.append(
            (
                f"| `{' '.join(c['cmd'])}` | {c['required']} | "
                f"{c['raw_pass']} | {c['pass']} |"
            )
        )

    lines += [
        "",
        "## Next required Vivado gates",
        "",
        "- Vivado elaboration",
        "- CDC reports",
        "- Clock interaction report",
        "- Timing summary",
        "- DRC report",
        "- Utilization report",
        "- CDC sign-off package",
        "",
        "This local check does not authorize board testing.",
    ]

    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nWrote {SUMMARY_JSON}")
    print(f"Wrote {SUMMARY_MD}")
    print(f"\nLOCAL PRE-BOARD PASS: {overall_pass}")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
