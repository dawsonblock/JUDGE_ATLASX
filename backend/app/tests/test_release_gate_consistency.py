"""Test consistency between canonical proof artifacts derived from release_gate.json."""

import json
from pathlib import Path

import pytest


@pytest.fixture
def repo_root():
    """Return the repository root directory."""
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def release_gate_path(repo_root):
    """Return path to release_gate.json."""
    return repo_root / "artifacts" / "proof" / "current" / "release_gate.json"


@pytest.fixture
def current_proof_path(repo_root):
    """Return path to CURRENT_PROOF.md."""
    return repo_root / "artifacts" / "proof" / "current" / "CURRENT_PROOF.md"


@pytest.fixture
def repair_report_path(repo_root):
    """Return path to REPAIR_REPORT.md."""
    return repo_root / "artifacts" / "proof" / "current" / "REPAIR_REPORT.md"


@pytest.fixture
def release_gate_json(release_gate_path):
    """Load and return release_gate.json as dict."""
    if not release_gate_path.exists():
        pytest.skip(f"release_gate.json not found at {release_gate_path}")
    return json.loads(release_gate_path.read_text(encoding="utf-8"))


@pytest.fixture
def current_proof_md(current_proof_path):
    """Load and return CURRENT_PROOF.md as string."""
    if not current_proof_path.exists():
        pytest.skip(f"CURRENT_PROOF.md not found at {current_proof_path}")
    return current_proof_path.read_text(encoding="utf-8")


def test_current_proof_md_exists(current_proof_path):
    """Test that CURRENT_PROOF.md exists in artifacts/proof/current."""
    assert current_proof_path.exists(), f"CURRENT_PROOF.md missing at {current_proof_path}"


def test_repair_report_md_exists(repair_report_path):
    """Test that REPAIR_REPORT.md exists in artifacts/proof/current."""
    assert repair_report_path.exists(), f"REPAIR_REPORT.md missing at {repair_report_path}"


def test_release_gate_json_alpha_gate_passed_matches_current_proof(
    release_gate_json, current_proof_md
):
    """Test that release_gate.json alpha_gate_passed matches CURRENT_PROOF.md."""
    # Extract alpha_gate_passed from release_gate.json
    alpha_gate_passed = release_gate_json.get("alpha_gate_passed")
    assert alpha_gate_passed is not None, "release_gate.json missing alpha_gate_passed"

    # Extract alpha_gate_passed from CURRENT_PROOF.md
    normalized = current_proof_md.lower()
    assert "- alpha_gate_passed: true" in normalized or "- alpha_gate_passed: false" in normalized, \
        "CURRENT_PROOF.md missing alpha_gate_passed line"

    if alpha_gate_passed:
        assert "- alpha_gate_passed: true" in normalized, \
            "CURRENT_PROOF.md alpha_gate_passed does not match release_gate.json (expected True)"
    else:
        assert "- alpha_gate_passed: false" in normalized, \
            "CURRENT_PROOF.md alpha_gate_passed does not match release_gate.json (expected False)"


def test_release_gate_json_archive_validation_result_matches_current_proof(
    release_gate_json, current_proof_md
):
    """Test that release_gate.json archive_validation_result matches CURRENT_PROOF.md."""
    # Extract archive_validation_result from release_gate.json
    archive_validation_result = release_gate_json.get("archive_validation_result")
    assert archive_validation_result is not None, "release_gate.json missing archive_validation_result"

    normalized = current_proof_md.lower()

    # Preferred explicit key in CURRENT_PROOF.md.
    if "- archive_validation_result:" in normalized:
        expected_line = f"- archive_validation_result: {archive_validation_result}".lower()
        assert expected_line in normalized, \
            f"CURRENT_PROOF.md archive_validation_result does not match release_gate.json (expected {expected_line})"
        return

    # Backward-compatible proof format fallback.
    if archive_validation_result == "PASS":
        assert "archive validation passed against the final distributable archive shape." in normalized, \
            "CURRENT_PROOF.md archive validation prose does not match release_gate.json (expected PASS)"
    else:
        assert "archive validation has not yet been recorded for this run." in normalized, \
            "CURRENT_PROOF.md archive validation prose does not match release_gate.json (expected non-PASS)"


def test_release_gate_json_check_count_matches_current_proof(
    release_gate_json, current_proof_md
):
    """Test that release_gate.json check_count matches CURRENT_PROOF.md."""
    # Extract check_count from release_gate.json
    check_count = release_gate_json.get("check_count")
    assert check_count is not None, "release_gate.json missing check_count"

    # Extract check_count from CURRENT_PROOF.md
    assert "- release_gate_check_count:" in current_proof_md, \
        "CURRENT_PROOF.md missing release_gate_check_count line"
    
    expected_line = f"- release_gate_check_count: {check_count}"
    assert expected_line in current_proof_md, \
        f"CURRENT_PROOF.md release_gate_check_count does not match release_gate.json (expected {expected_line})"


def test_release_gate_json_log_paths_exist(release_gate_json, repo_root, current_proof_path):
    """Test that all paths in release_gate.json logs exist."""
    logs = release_gate_json.get("logs", {})
    assert logs, "release_gate.json missing logs field"

    if current_proof_path.exists():
        current_proof_text = current_proof_path.read_text(encoding="utf-8").lower()
        if "- status: in_progress" in current_proof_text:
            pytest.skip("current proof is still being assembled")
    
    missing_paths = []
    for key, path in logs.items():
        full_path = repo_root / path
        if not full_path.exists():
            missing_paths.append(f"{key}: {path}")
    
    assert not missing_paths, f"Missing log paths:\n" + "\n".join(missing_paths)


def test_release_gate_json_logs_stay_under_canonical_proof_tree(release_gate_json):
    """Test that release gate logs do not point back to legacy proof mirrors."""
    logs = release_gate_json.get("logs", {})
    assert logs, "release_gate.json missing logs field"

    check_names = {
        check.get("name")
        for check in release_gate_json.get("checks", [])
        if isinstance(check, dict)
    }

    legacy_paths = []
    for key, path in logs.items():
        normalized = str(path).replace("\\", "/")
        if normalized.startswith("artifacts/current/"):
            legacy_paths.append(f"{key}: {path}")

    if "single_proof_authority" not in check_names and legacy_paths:
        pytest.skip("release_gate.json predates canonical-only proof migration")

    assert not legacy_paths, "Legacy proof mirror paths remain in release_gate.json logs:\n" + "\n".join(legacy_paths)


def test_proof_input_file_list_excludes_cache_files(release_gate_json):
    """Test that proof_input_file_list does not include cache files."""
    proof_input_file_list = release_gate_json.get("proof_input_file_list", [])
    if not proof_input_file_list:
        pytest.skip("release_gate.json missing proof_input_file_list (stale/incomplete artifact)")
    
    cache_files = [
        f for f in proof_input_file_list
        if any(pattern in f for pattern in [
            ".pytest_cache",
            "__pycache__",
            "node_modules",
            ".next",
        ])
    ]
    
    assert not cache_files, f"proof_input_file_list contains cache files:\n" + "\n".join(cache_files)


def test_proof_manifest_exists_in_canonical_proof_tree(repo_root, release_gate_json):
    """Test that the canonical proof manifest exists alongside release_gate.json."""
    proof_manifest_path = repo_root / "artifacts" / "proof" / "current" / "proof_manifest.json"
    assert proof_manifest_path.exists(), f"proof_manifest.json missing at {proof_manifest_path}"

    proof_manifest = json.loads(proof_manifest_path.read_text(encoding="utf-8"))
    manifest_alpha_gate = proof_manifest.get("release_gate", {}).get("alpha_gate_passed")
    if manifest_alpha_gate is not None:
        assert manifest_alpha_gate == release_gate_json.get("alpha_gate_passed")
