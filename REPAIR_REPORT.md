# REPAIR_REPORT

- generated_at_utc: 2026-05-21T00:19:41.923125+00:00
- commit_hash: f7f430681d3ec98954fe86fb64414ececb00b641
- alpha_gate_passed: false

## Phase Results

- 1. Alpha Gate Truthfulness: FAIL (artifacts/proof/current/release_gate.json)
- 2. Canonical Proof Artifacts: PASS (artifacts/proof/current/CURRENT_PROOF.md)
- 3. Generated Alpha Status: PASS (artifacts/proof/current/CURRENT_ALPHA_STATUS.md)
- 4. Source Registry Governance: FAIL (artifacts/proof/current/source_registry_status.json)
- 5. Generated Source Registry Status: PASS (artifacts/proof/current/SOURCE_REGISTRY_STATUS.md)
- 6. Proof Policy Generated: PASS (artifacts/proof/current/PROOF_POLICY.md)
- 7. Evidence Store Integrity: FAIL (artifacts/proof/current/verify_evidence_store.log)
- 8. Audit Chain Integrity: FAIL (artifacts/proof/current/verify_audit_chain.log)
- 9. Justice XML Proof Coverage: FAIL (artifacts/proof/current/backend_pytest.log)
- 10. Public Review Gate Coverage: FAIL (artifacts/proof/current/public_api_boundary.log)
- 11. Derivative Memory Boundary Coverage: FAIL (artifacts/proof/current/public_api_boundary.log)
- 12. Frontend Node 25.9 Gate: FAIL (artifacts/proof/current/frontend_node_gate.log)
- 13. CI/Local Gate Parity Baseline: PASS (artifacts/proof/current/release_readiness.md)
- 14. Repair Report Generated: PASS (artifacts/proof/current/REPAIR_REPORT.md)

## Remaining Blockers

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
