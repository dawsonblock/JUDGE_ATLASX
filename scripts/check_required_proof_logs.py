#!/usr/bin/env python3
"""Verify that every log_path referenced in release_gate.json exists on disk.

This script reads ``artifacts/proof/current/release_gate.json`` and checks
that every log file recorded in ``checks[*].log_path`` is present on the
filesystem.  It exits 1 with a clear list of missing paths so the gate
cannot be marked PASS while evidence is absent.

Usage::

    python3 scripts/check_required_proof_logs.py
    python3 scripts/check_required_proof_logs.py --root /path/to/repo
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def check_required_proof_logs(repo_root: Path) -> list[str]:
    """Return a list of log_path values that are missing on disk.

    Reads ``artifacts/proof/current/release_gate.json`` and inspects every
    entry in the ``checks`` array for a ``log_path`` field.  Also checks the
    top-level ``logs`` map as a secondary source.

    Args:
        repo_root: Repository root directory.

    Returns:
        Sorted list of relative paths (strings) that do not exist on disk.
        Empty list means all referenced logs are present.
    """
    gate_json = repo_root / "artifacts" / "proof" / "current" / "release_gate.json"
    if not gate_json.exists():
        print(f"ERROR: release_gate.json not found at {gate_json}", file=sys.stderr)
        return [str(gate_json.relative_to(repo_root))]

    try:
        payload = json.loads(gate_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: failed to parse release_gate.json: {exc}", file=sys.stderr)
        return ["release_gate.json:parse_error"]

    missing: list[str] = []
    seen: set[str] = set()

    # Primary source: checks array (each entry has a log_path field)
    for entry in payload.get("checks", []):
        log_path = entry.get("log_path")
        if not log_path or not isinstance(log_path, str):
            continue
        if log_path in seen:
            continue
        seen.add(log_path)
        abs_path = repo_root / log_path
        if not abs_path.exists():
            missing.append(log_path)

    # Secondary source: top-level logs map
    for _check_name, log_path in payload.get("logs", {}).items():
        if not log_path or not isinstance(log_path, str):
            continue
        if log_path in seen:
            continue
        # Only enforce logs inside artifacts/proof/current/ — other paths
        # (docs, root files) are non-log artifacts and may vary per run.
        if not log_path.startswith("artifacts/proof/current/"):
            continue
        seen.add(log_path)
        abs_path = repo_root / log_path
        if not abs_path.exists():
            missing.append(log_path)

    return sorted(missing)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    missing = check_required_proof_logs(repo_root)

    gate_json = repo_root / "artifacts" / "proof" / "current" / "release_gate.json"
    if gate_json.exists():
        try:
            payload = json.loads(gate_json.read_text(encoding="utf-8"))
            total = len([
                e for e in payload.get("checks", []) if e.get("log_path")
            ])
        except (json.JSONDecodeError, OSError):
            total = 0
    else:
        total = 0

    if missing:
        print(f"REQUIRED_PROOF_LOGS: FAIL ({len(missing)} missing of {total} referenced)")
        for path in missing:
            print(f"  MISSING: {path}")
        return 1

    print(f"REQUIRED_PROOF_LOGS: PASS ({total} referenced logs present)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
