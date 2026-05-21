# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-21T00:19:41.923125+00:00
- commit_hash: f7f430681d3ec98954fe86fb64414ececb00b641
- alpha_gate_passed: false

## Required Gate Signals

- backend_compile: PASS
- backend_import: PASS
- backend_pytest: FAIL
- verify_evidence_store: FAIL
- verify_audit_chain: FAIL
- public_api_boundary: FAIL
- frontend_node_gate: FAIL
- frontend_contracts: BLOCKED
- archive_validation: FAIL
- proof_freshness: FAIL

## Release Blockers

- backend_pytest
- postgis_proof
- egress_proxy_proof
- demo_proof
- validate_sources
- check_yaml_duplicate_keys
- verify_source_registry
- source_registry_status
- prepare_proof_db
- verify_evidence_store
- verify_audit_chain
- auth_mutation_route_coverage
- mutation_fail_closed_coverage
- frontend_node_gate
- frontend_install
- frontend_lint
- frontend_typecheck
- frontend_contracts
- frontend_build
- check_api_contracts
- repo_generated_files
- check_npm_audit_triage
- map_route_check
- public_api_boundary
- proof_freshness
- archive_validation

## Canonical Artifacts

- artifacts/proof/current/release_gate.json
- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/REPAIR_REPORT.md
