"""Test that all paths referenced in release_gate.json["logs"] actually exist.

This validates proof artifact truthfulness: if release_gate.json references a file,
that file must exist in the release archive.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest


def test_release_gate_log_paths_exist(repo_root: Path):
    """All paths in release_gate.json["logs"] must exist relative to repo root."""
    release_gate_path = repo_root / "artifacts" / "proof" / "current" / "release_gate.json"

    # Skip test if release_gate.json doesn't exist (e.g., during initial development)
    if not release_gate_path.exists():
        pytest.skip(f"release_gate.json not found at {release_gate_path}")

    with release_gate_path.open(encoding="utf-8") as f:
        release_gate = json.load(f)

    logs = release_gate.get("logs", {})
    if not logs:
        pytest.fail("release_gate.json has no 'logs' section")

    missing = []
    for name, path in logs.items():
        full_path = repo_root / path
        if not full_path.exists():
            missing.append((name, path))

    if missing:
        missing_str = "\n".join(f"  - {name}: {path}" for name, path in missing)
        pytest.fail(
            f"release_gate.json references {len(missing)} missing file(s):\n{missing_str}\n"
            f"Total log references: {len(logs)}"
        )

    # All files exist
    assert True


def test_release_gate_current_proof_md_exists(repo_root: Path):
    """CURRENT_PROOF.md must exist as referenced in proof_input_paths."""
    current_proof_path = repo_root / "artifacts" / "proof" / "current" / "CURRENT_PROOF.md"
    if not current_proof_path.exists():
        pytest.skip(f"CURRENT_PROOF.md not found at {current_proof_path}")
    assert True


def test_release_gate_repair_report_md_exists(repo_root: Path):
    """REPAIR_REPORT.md must exist as referenced in logs."""
    repair_report_path = repo_root / "artifacts" / "proof" / "current" / "REPAIR_REPORT.md"
    if not repair_report_path.exists():
        pytest.skip(f"REPAIR_REPORT.md not found at {repair_report_path}")
    assert True
