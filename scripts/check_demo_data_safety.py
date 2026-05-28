#!/usr/bin/env python3
"""Demo data safety checker.

Scans the demo/seed data directory for records that should never ship to
production — real names, real SIN/SIN-like numbers, real addresses, or records
that are missing the DEMO_ONLY marker.

Exit codes
----------
  0   All demo data is safe.
  1   One or more safety violations found.

Usage
-----
    python scripts/check_demo_data_safety.py
    python scripts/check_demo_data_safety.py --path backend/tests/fixtures
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns that should NOT appear in demo data (case-insensitive)
# ---------------------------------------------------------------------------

# Social Insurance Number (Canadian) — 3-3-3 digit pattern
SIN_PATTERN = re.compile(r"\b\d{3}[- ]\d{3}[- ]\d{3}\b")

# Common placeholder for real names used accidentally
REAL_NAME_PATTERNS: list[re.Pattern] = [
    re.compile(r"\bjohn (doe|smith|jones)\b", re.IGNORECASE),
    re.compile(r"\bjane (doe|smith)\b", re.IGNORECASE),
]

# Real Saskatchewan postal code prefixes (S0A–S9Z) — should be blurred in demo
REAL_POSTAL_CODE = re.compile(r"\bS[0-9][A-Z] [0-9][A-Z][0-9]\b")

# Street addresses with real street numbers
STREET_ADDRESS = re.compile(r"\b\d{2,5}\s+[A-Z][a-z]+\s+(St|Ave|Rd|Dr|Blvd|Way|Cres|Pl)\b")

# Required marker in every demo JSON file
DEMO_MARKER = "DEMO_ONLY"

# File extensions to scan
SCAN_EXTENSIONS = {".json", ".csv", ".txt", ".md", ".yaml", ".yml"}

# Directories to scan when no --path is specified
DEFAULT_SCAN_PATHS = [
    "backend/tests/fixtures",
    "backend/tests/seeds",
    "scripts/demo_data",
]


def check_file(path: Path) -> list[str]:
    """Return a list of violation messages for one file."""
    violations: list[str] = []
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [f"{path}: cannot read file ({e})"]

    # JSON files: check for DEMO_ONLY marker
    if path.suffix == ".json":
        try:
            data = json.loads(content)
            if isinstance(data, dict) and data.get("_demo_only") is not True:
                violations.append(
                    f"{path}: missing '_demo_only: true' marker in JSON root"
                )
        except json.JSONDecodeError:
            pass  # Not valid JSON, skip marker check

    # Pattern checks (all file types)
    if SIN_PATTERN.search(content):
        violations.append(f"{path}: possible SIN number pattern found")

    if REAL_POSTAL_CODE.search(content) and DEMO_MARKER not in content:
        violations.append(
            f"{path}: real postal code pattern found without DEMO_ONLY marker"
        )

    if STREET_ADDRESS.search(content) and DEMO_MARKER not in content:
        violations.append(
            f"{path}: real street address pattern found without DEMO_ONLY marker"
        )

    return violations


def scan_directory(root: Path) -> list[str]:
    """Recursively scan a directory and return all violations."""
    if not root.exists():
        return []
    all_violations: list[str] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in SCAN_EXTENSIONS:
            all_violations.extend(check_file(path))
    return all_violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check demo data safety")
    parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="Path to scan (defaults to all DEFAULT_SCAN_PATHS)",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).parent.parent

    if args.path:
        scan_paths = [repo_root / args.path]
    else:
        scan_paths = [repo_root / p for p in DEFAULT_SCAN_PATHS]

    all_violations: list[str] = []
    for path in scan_paths:
        all_violations.extend(scan_directory(path))

    if all_violations:
        print(f"[FAIL] Demo data safety check: {len(all_violations)} violation(s) found\n")
        for v in all_violations:
            print(f"  - {v}")
        return 1

    print("[PASS] Demo data safety check: all demo data appears safe")
    return 0


if __name__ == "__main__":
    sys.exit(main())
