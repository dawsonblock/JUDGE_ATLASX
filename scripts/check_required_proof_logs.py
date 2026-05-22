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
DEFAULT_REQUIRED_PROOF_FILES = (
    "artifacts/proof/current/CURRENT_PROOF.md",
    "artifacts/proof/current/CURRENT_ALPHA_STATUS.md",
    "artifacts/proof/current/SOURCE_REGISTRY_STATUS.md",
    "artifacts/proof/current/source_registry_status.json",
    "artifacts/proof/current/release_gate.json",
    "artifacts/proof/current/proof_manifest.json",
    "artifacts/proof/current/FIX_VERIFICATION_REPORT.md",
    "artifacts/proof/current/release_readiness.md",
    "artifacts/proof/current/PROOF_POLICY.md",
)


def check_required_proof_logs(repo_root: Path) -> tuple[list[str], int, int]:
    """Return missing log paths plus referenced/present totals.

    Reads ``artifacts/proof/current/release_gate.json`` and inspects every
    entry in the ``checks`` array for a ``log_path`` field.  Also checks the
    top-level ``logs`` map as a secondary source.

    Args:
        repo_root: Repository root directory.

    Returns:
        Tuple of ``(missing_paths, referenced_total, present_total)``.
    """
    gate_json = repo_root / "artifacts" / "proof" / "current" / "release_gate.json"
    if not gate_json.exists():
        print(f"ERROR: release_gate.json not found at {gate_json}", file=sys.stderr)
        missing_paths = [str(gate_json.relative_to(repo_root))]
        return missing_paths, len(missing_paths), 0

    try:
        payload = json.loads(gate_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: failed to parse release_gate.json: {exc}", file=sys.stderr)
        return ["release_gate.json:parse_error"], 1, 0

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

    referenced_total = len(seen)
    present_total = referenced_total - len(missing)
    return sorted(missing), referenced_total, present_total


def _missing_required_proof_files(repo_root: Path) -> list[str]:
    missing: list[str] = []
    for rel_path in DEFAULT_REQUIRED_PROOF_FILES:
        if not (repo_root / rel_path).exists():
            missing.append(rel_path)
    return sorted(missing)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root")
    parser.add_argument(
        "--strict-required-files",
        action="store_true",
        help=(
            "Also fail if canonical proof files required by archive packaging are missing"
        ),
    )
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    missing, referenced_total, present_total = check_required_proof_logs(repo_root)
    missing_required_files: list[str] = []
    if args.strict_required_files:
        missing_required_files = _missing_required_proof_files(repo_root)

    if missing or missing_required_files:
        print(
            "REQUIRED_PROOF_LOGS: FAIL "
            f"({len(missing)} missing of {referenced_total} referenced)"
        )
        print(
            "REQUIRED_PROOF_LOGS: DEBUG "
            f"present={present_total} missing={len(missing)} referenced={referenced_total}"
        )
        if referenced_total > 0:
            percentage = (present_total / referenced_total) * 100.0
            print(f"REQUIRED_PROOF_LOGS: DEBUG present_ratio={percentage:.1f}%")
        for path in missing:
            abs_path = repo_root / path
            if abs_path.exists():
                size = abs_path.stat().st_size
                print(f"  MISSING: {path} (exists_on_disk size={size} bytes)")
            else:
                print(f"  MISSING: {path}")

        if missing_required_files:
            print(
                "REQUIRED_PROOF_LOGS: DEBUG "
                f"missing_required_files={len(missing_required_files)}"
            )
            for path in missing_required_files:
                print(f"  MISSING_REQUIRED_FILE: {path}")
        return 1

    print(
        "REQUIRED_PROOF_LOGS: PASS "
        f"({present_total} referenced logs present)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
