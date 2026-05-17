from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[3] / "scripts" / "validate_release_archive.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("validate_release_archive", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_zip(path: Path, files: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as zf:
        for name, text in files.items():
            zf.writestr(name, text)


def _valid_files(root: str = "JUDGE_ATLAS-main") -> dict[str, str]:
    prefix = f"{root}/"
    current_proof_md = (
        "# CURRENT_PROOF\n\n"
        "- generated_at_utc: 2026-05-17T21:55:21.805176+00:00\n"
        "- commit_hash: 3c703d2573821e41ef3fcea5034b028593028b88\n"
        "- alpha_gate_status: PASS\n"
        "- alpha_gate_passed: True\n"
        "- release_gate_check_count: 35\n"
        "- docker_available: True\n"
        "- postgis_proof_result: PASS\n"
        "- egress_proxy_proof_result: PASS\n"
        "- demo_proof_result: PASS\n"
        "- proof_freshness_result: PASS\n"
        "- proof_input_tree_hash: dc088dde49726c695658a2507e3b9ec2453b8b2c3f5fed7d25de1c2fa160aa99\n"
        "- proof_input_file_count: 100\n"
        "- egress_proxy_proof_log: artifacts/proof/current/egress_proxy_proof.log\n"
        "- demo_proof_log: artifacts/proof/current/demo_proof.log\n\n"
        "## Runtime Metadata\n\n"
        "- gate_runner_python_version: 3.11.7\n"
        "- gate_runner_python_executable: /Users/dawsonblock/.pyenv/versions/3.11.7/bin/python\n"
        "- backend_test_python_version: 3.11.7\n"
        "- backend_test_python_executable: /Users/dawsonblock/JUDGE_ATLASX/backend/.venv/bin/python\n"
        "- backend_required_python: >=3.11\n"
        "- node_version: v24.15.0\n"
        "- npm_version: 11.12.1\n"
        "- platform: macOS-26.2-arm64-arm-64bit\n"
        "- test_database_backend: sqlite\n"
        "- test_database_url_type: sqlite_file\n\n"
        "## Scope and Safety\n\n"
        "- Current status: proof-hardened alpha.\n"
        "- Not ready for production deployment.\n"
        "- Does not hold legal authority.\n"
        "- Evidence snapshots are authoritative; memory is derivative.\n"
        "- AI is reviewer assistance only.\n"
        "- Source ingestion is disabled by default unless explicitly enabled.\n"
        "- External folders are reference-only.\n"
        "- JWT mutation authority is current; legacy shared-token compatibility is deprecated.\n"
        "- make verify = local no-Docker quality checks.\n"
        "- make release-proof-local = Docker/PostGIS alpha release gate.\n"
        "- Current alpha release is blocked if Docker/PostGIS proof fails.\n"
        "- Docker/PostGIS proof passed in the current release gate.\n"
        "- Dedicated egress proxy proof passed in the current release gate.\n"
        "- Dedicated synthetic demo proof passed in the current release gate.\n"
        "- Proof freshness passed against the stored proof-input file list and tree hash.\n"
        "- Archive validation passed against the final distributable archive shape.\n"
        "- archive_validation_log: artifacts/proof/current/archive_validation.log\n"
        "- archive_validation_supported_shapes:\n"
        "  - JUDGE-main/\n"
        "  - */JUDGE-main/\n\n"
        "## Governance Status\n\n"
        "- legacy_shared_token_status: deprecated, removal plan documented\n"
        "- dependency_security_status: npm audit issues triaged for alpha; remediation plan documented\n\n"
        "## Current Proof Facts\n\n"
        "- backend pytest: 2790 passed, 19 skipped\n"
        "- backend import proof: PASS (95 routes)\n"
        "- frontend contracts: 48 passed\n"
        "- public API boundary: 33 passed\n"
        "- Docker runtime preflight: PASS\n"
        "- PostGIS proof: PASS\n"
        "- egress proxy proof: PASS\n"
        "- demo proof: PASS\n"
        "- mutation fail-closed coverage: PASS\n"
        "- Alembic migrations: 56\n\n"
        "## Failed Checks\n\n"
        "- none\n\n"
        "## Egress Proxy Coverage\n\n"
        "- Dedicated gate artifact: artifacts/proof/current/egress_proxy_proof.log.\n"
        "- Production startup proxy policy coverage: backend/app/tests/test_production_fetch_egress_policy.py.\n"
        "- Runtime proxy opener/wiring coverage: backend/app/tests/test_source_fetcher_proxy.py.\n"
        "- SSRF defense context coverage remains in backend/app/tests/test_source_fetcher_ssrf.py.\n\n"
        "## Canonical Artifacts\n\n"
        "- artifacts/proof/current/proof_manifest.json\n"
        "- artifacts/proof/current/release_gate.json\n"
        "- artifacts/proof/current/release_gate.log\n"
        "- artifacts/proof/current/docker_runtime_preflight.log\n"
        "- artifacts/proof/current/postgis_proof.log\n"
        "- artifacts/proof/current/egress_proxy_proof.log\n"
        "- artifacts/proof/current/demo_proof.log\n"
        "- artifacts/proof/current/proof_freshness.log\n"
        "- artifacts/proof/current/archive_validation.log\n"
        "- artifacts/proof/current/backend_import.log\n"
        "- artifacts/proof/current/backend_pytest.log\n"
        "- artifacts/proof/current/backend_proof_summary.json\n"
        "- artifacts/proof/current/frontend_proof_summary.json\n"
        "- artifacts/proof/current/frontend_node_gate.log\n"
        "- artifacts/proof/current/frontend_install.log\n"
        "- artifacts/proof/current/frontend_lint.log\n"
        "- artifacts/proof/current/frontend_typecheck.log\n"
        "- artifacts/proof/current/frontend_contracts.log\n"
        "- artifacts/proof/current/frontend_build.log\n"
        "- artifacts/proof/current/check_api_contracts.log\n"
        "- artifacts/proof/current/static_guards.log\n"
        "- artifacts/proof/current/map_route_check.log\n"
        "- artifacts/proof/current/public_api_boundary.log\n"
        "- artifacts/proof/current/mutation_fail_closed_coverage.log\n"
        "- artifacts/proof/current/source_registry_status.json\n"
        "- artifacts/proof/current/release_readiness.md\n"
        "- artifacts/proof/current/CURRENT_ALPHA_STATUS.md\n"
        "- artifacts/proof/current/SOURCE_REGISTRY_STATUS.md\n"
        "- artifacts/proof/current/PROOF_POLICY.md\n"
        "- artifacts/proof/current/REPAIR_REPORT.md\n"
    )
    return {
        prefix + "backend/app/main.py": "print('ok')\n",
        prefix + "frontend/package.json": "{}\n",
        prefix + "docs/README.md": "docs\n",
        prefix + "scripts/release_gate.py": "print('gate')\n",
        prefix + "artifacts/proof/current/CURRENT_PROOF.md": current_proof_md,
        prefix + "artifacts/proof/current/release_readiness.md": "current readiness\n",
        prefix + "artifacts/proof/current/release_gate.json": (
            '{"check_count": 35, "backend_pytest_passed": 2790, '
            '"backend_import_route_count": 95, "proof_input_file_count": 100}\n'
        ),
        prefix + "artifacts/proof/current/backend_proof_summary.json": '{"passed": 2790}\n',
        prefix + "artifacts/proof/current/frontend_proof_summary.json": '{"passed": 48}\n',
        prefix + "artifacts/proof/current/source_registry_status.json": '{"total_sources": 26}\n',
        prefix + "README.md": "repo readme\n",
        prefix + "STATUS.md": "Production ready: FALSE\n",
    }


def test_validate_release_archive_accepts_valid_archive(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "valid.zip"
    _write_zip(archive, _valid_files())

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is True
    assert report["top_level_roots"] == ["JUDGE_ATLAS-main"]


def test_validate_release_archive_rejects_wrong_root(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "wrong-root.zip"
    _write_zip(archive, _valid_files(root="JUDGE-main"))

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert "archive_root_mismatch:JUDGE-main!=JUDGE_ATLAS-main" in report["errors"]


def test_validate_release_archive_rejects_node_modules(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "node-modules.zip"
    files = _valid_files()
    files["JUDGE_ATLAS-main/frontend/node_modules/react/index.js"] = "module.exports = {}\n"
    _write_zip(archive, files)

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert any(error.startswith("forbidden_path:") for error in report["errors"])


def test_validate_release_archive_rejects_external_by_default(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "external.zip"
    files = _valid_files()
    files["JUDGE_ATLAS-main/external/reference/README.md"] = "external ref\n"
    _write_zip(archive, files)

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert any(error.startswith("forbidden_external_path:") for error in report["errors"])


def test_validate_release_archive_rejects_missing_current_proof_dir(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "missing-proof.zip"
    files = _valid_files()
    files.pop("JUDGE_ATLAS-main/artifacts/proof/current/CURRENT_PROOF.md")
    files.pop("JUDGE_ATLAS-main/artifacts/proof/current/release_readiness.md")
    _write_zip(archive, files)

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert "missing_required_directory:artifacts/proof/current/" in report["errors"] or any(
        error.startswith("missing_required_proof_file:") for error in report["errors"]
    )


def test_validate_release_archive_rejects_env_file(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "env.zip"
    files = _valid_files()
    files["JUDGE_ATLAS-main/.env"] = "SECRET=1\n"
    _write_zip(archive, files)

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert any(error.startswith("forbidden_secret_file:") for error in report["errors"])


def test_validate_release_archive_rejects_research_path(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "research.zip"
    files = _valid_files()
    files["JUDGE_ATLAS-main/research/crawlee-python-master/foo.py"] = "crawlee\n"
    _write_zip(archive, files)

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert any(error.startswith("forbidden_research_path:") for error in report["errors"])


def test_validate_release_archive_rejects_archive_validation_md(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "archive-val-md.zip"
    files = _valid_files()
    files["JUDGE_ATLAS-main/archive_validation.md"] = "validation output\n"
    _write_zip(archive, files)

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert any(
        error.startswith("forbidden_secret_file:") and "archive_validation.md" in error
        for error in report["errors"]
    )


def test_validate_release_archive_rejects_archive_validation_log(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "archive-val-log.zip"
    files = _valid_files()
    files["JUDGE_ATLAS-main/archive_validation.log"] = "log output\n"
    _write_zip(archive, files)

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert any(
        error.startswith("forbidden_secret_file:") and "archive_validation.log" in error
        for error in report["errors"]
    )


def test_validate_release_archive_rejects_trailing_whitespace_segment(tmp_path: Path) -> None:
    module = _load_module()
    archive = tmp_path / "whitespace-segment.zip"
    files = _valid_files()
    # "Research " (trailing space) is the canonical regression from the audit
    files["JUDGE_ATLAS-main/Research /crawlee-python-master/foo.py"] = "crawlee\n"
    _write_zip(archive, files)

    report = module.inspect_archive(archive, expected_root="JUDGE_ATLAS-main")

    assert report["valid"] is False
    assert any(error.startswith("whitespace_path_segment:") for error in report["errors"])