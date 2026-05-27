# CURRENT_PROOF

- generated_at_utc: 2026-05-27T01:40:59.647028+00:00
- commit_hash: 764db500c29e6e97e0f50531322ca929774692a8
- alpha_gate_status: PASS
- alpha_gate_passed: true
- release_gate_check_count: 50
- docker_available: false
- postgis_proof_result: BLOCKED
- egress_proxy_proof_result: PASS
- demo_proof_result: PASS
- proof_freshness_result: PASS
- archive_validation_result: PASS
- proof_input_tree_hash: 1eed171c163af1185db4374a0c22b677f8f839e9e505df37e7c5ddc90409fad4
- proof_input_file_count: 1085
- egress_proxy_proof_log: artifacts/proof/current/egress_proxy_proof.log
- demo_proof_log: artifacts/proof/current/demo_proof.log

## Runtime Metadata

- gate_runner_python_version: 3.11.7
- gate_runner_python_executable: [REDACTED_LOCAL_PATH]
- backend_test_python_version: 3.11.7
- backend_test_python_executable: [REDACTED_LOCAL_PATH]/backend/.venv/bin/python
- backend_required_python: >=3.11
- node_version: v20.20.2
- npm_version: 10.8.2
- platform: macOS-26.2-arm64-arm-64bit
- test_database_backend: sqlite
- test_database_url_type: sqlite_file

## Scope and Safety

- Current status: proof-hardened alpha.
- Not ready for production deployment.
- Does not hold legal authority.
- Evidence snapshots are authoritative; memory is derivative.
- AI is reviewer assistance only.
- Source ingestion is disabled by default unless explicitly enabled.
- External folders are reference-only.
- JWT mutation authority is current; legacy shared-token compatibility is deprecated.
- make verify = local no-Docker quality checks.
- make release-proof-local = Docker/PostGIS alpha release gate.
- Current alpha release is blocked if Docker/PostGIS proof fails.
- Docker/PostGIS proof did not pass in the current release gate.
- Dedicated egress proxy proof passed in the current release gate.
- Dedicated synthetic demo proof passed in the current release gate.
- Proof freshness passed against the stored proof-input file list and tree hash.
- Archive validation passed against the final distributable archive shape.
- archive_validation_log: artifacts/proof/current/archive_validation.log
- archive_validation_supported_shapes:
  - JUDGE-main/
  - */JUDGE-main/

## Governance Status

- legacy_shared_token_status: deprecated, removal plan documented
- dependency_security_status: npm audit issues triaged for alpha; remediation plan documented

## Current Proof Facts

- backend pytest: 3454 passed, 2 skipped
- backend import proof: PASS (107 routes)
- frontend contracts: 49 passed
- public API boundary: 55 passed
- Docker runtime preflight: FAIL
- PostGIS proof: BLOCKED
- egress proxy proof: PASS
- demo proof: PASS
- CanLII staging proof: PASS
- mutation fail-closed coverage: PASS
- Alembic migrations: 72

## Blocked Checks

- docker_smoke: docker_runtime_preflight failed
- postgis_proof: docker_runtime_preflight failed

## Egress Proxy Coverage

- Dedicated gate artifact: artifacts/proof/current/egress_proxy_proof.log.
- Production startup proxy policy coverage: backend/app/tests/test_production_fetch_egress_policy.py.
- Runtime proxy opener/wiring coverage: backend/app/tests/test_source_fetcher_proxy.py.
- SSRF defense context coverage remains in backend/app/tests/test_source_fetcher_ssrf.py.

## Canonical Artifacts

- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/release_gate.json
- artifacts/proof/current/release_gate.log
- artifacts/proof/current/docker_runtime_preflight.log
- artifacts/proof/current/postgis_proof.log
- artifacts/proof/current/egress_proxy_proof.log
- artifacts/proof/current/demo_proof.log
- artifacts/proof/current/canlii_staging_proof.log
- artifacts/proof/current/proof_freshness.log
- artifacts/proof/current/archive_validation.log
- artifacts/proof/current/backend_import.log
- artifacts/proof/current/backend_pytest.log
- artifacts/proof/current/frontend_node_gate.log
- artifacts/proof/current/check_node_policy.log
- artifacts/proof/current/frontend_install.log
- artifacts/proof/current/frontend_lint.log
- artifacts/proof/current/frontend_typecheck.log
- artifacts/proof/current/frontend_contracts.log
- artifacts/proof/current/frontend_build.log
- artifacts/proof/current/check_api_contracts.log
- artifacts/proof/current/static_guards.log
- artifacts/proof/current/map_route_check.log
- artifacts/proof/current/public_api_boundary.log
- artifacts/proof/current/mutation_fail_closed_coverage.log
- artifacts/proof/current/proof_consistency_pytest.log
- artifacts/proof/current/single_proof_authority.log
- artifacts/proof/current/required_proof_logs.log
- artifacts/proof/current/source_registry_status.json
- artifacts/proof/current/release_readiness.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/SOURCE_REGISTRY_STATUS.md
- artifacts/proof/current/PROOF_POLICY.md
- artifacts/proof/current/REPAIR_REPORT.md
