#!/usr/bin/env python3
"""Consistency checks for current proof artifacts.

This script validates that the canonical proof artifacts agree on core release
facts for the current tree.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_FILES = (
    "artifacts/proof/current/CURRENT_PROOF.md",
    "artifacts/proof/current/CURRENT_ALPHA_STATUS.md",
    "artifacts/proof/current/SOURCE_REGISTRY_STATUS.md",
    "artifacts/proof/current/source_registry_status.json",
    "artifacts/proof/current/release_gate.json",
    "artifacts/proof/current/proof_manifest.json",
    "artifacts/proof/current/FIX_VERIFICATION_REPORT.md",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _extract_bool_line(text: str, key: str) -> str | None:
    prefix = f"- {key}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip().lower()
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing_required_file:{rel}")

    if errors:
        print("PROOF CONSISTENCY: FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    release_gate = json.loads((root / "artifacts/proof/current/release_gate.json").read_text(encoding="utf-8"))
    current_alpha = _read_text(root / "artifacts/proof/current/CURRENT_ALPHA_STATUS.md")
    current_proof = _read_text(root / "artifacts/proof/current/CURRENT_PROOF.md")

    gate_alpha_passed = str(bool(release_gate.get("alpha_gate_passed", False))).lower()
    gate_prod_ready = str(bool(release_gate.get("production_ready", False))).lower()

    alpha_passed_md = _extract_bool_line(current_alpha, "alpha_gate_passed")
    prod_ready_md = _extract_bool_line(current_alpha, "production_ready")
    proof_alpha_passed_md = _extract_bool_line(current_proof, "alpha_gate_passed")

    if alpha_passed_md != gate_alpha_passed:
        errors.append("alpha_gate_passed_mismatch:CURRENT_ALPHA_STATUS_vs_release_gate")
    if prod_ready_md != gate_prod_ready:
        errors.append("production_ready_mismatch:CURRENT_ALPHA_STATUS_vs_release_gate")
    if proof_alpha_passed_md != gate_alpha_passed:
        errors.append("alpha_gate_passed_mismatch:CURRENT_PROOF_vs_release_gate")
    if gate_prod_ready != "false":
        errors.append("production_ready_must_be_false")

    if errors:
        print("PROOF CONSISTENCY: FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PROOF CONSISTENCY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
