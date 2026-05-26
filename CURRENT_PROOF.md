# CURRENT_PROOF

- generated_at_utc: 2026-05-26T21:53:59.055462+00:00
- commit_hash: 438c99a1f17e32e1ed8ba93e1cc7e799a84e8030
- alpha_gate_status: BLOCKED
- alpha_gate_passed: false
- release_gate_check_count: 37
- docker_available: false
- postgis_proof_result: UNKNOWN
- egress_proxy_proof_result: UNKNOWN
- demo_proof_result: UNKNOWN
- proof_freshness_result: UNKNOWN
- archive_validation_result: UNKNOWN
- proof_input_tree_hash: 10b763e7e0d18795aefda45dcb02cf5f13d14d9d0b7269e33d1682bb0b1fd6af
- proof_input_file_count: 1085
- egress_proxy_proof_log: unknown
- demo_proof_log: unknown

## Runtime Metadata

- gate_runner_python_version: 3.11.7
- gate_runner_python_executable: [REDACTED_LOCAL_PATH]
- backend_test_python_version: 3.11.7
- backend_test_python_executable: [REDACTED_LOCAL_PATH]
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
- Dedicated egress proxy proof did not pass in the current release gate.
- Dedicated synthetic demo proof did not pass in the current release gate.
- Proof freshness did not pass against the stored proof-input file list and tree hash.
- Archive validation has not yet been recorded for this run.
- archive_validation_log: unknown
- archive_validation_supported_shapes:
  - JUDGE-main/
  - */JUDGE-main/

## Governance Status

- legacy_shared_token_status: unknown
- dependency_security_status: unknown

## Failed Checks

- archive_validation
- docker_runtime_preflight
- docker_smoke
- postgis_proof

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
