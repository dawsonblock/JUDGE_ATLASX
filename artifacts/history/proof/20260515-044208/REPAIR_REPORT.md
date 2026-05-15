# REPAIR_REPORT

- generated_at_utc: 2026-05-15T04:40:00.948527+00:00
- commit_hash: 16d6b61c15cc3785033a4c0435f2da1f81eb4e0d
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
- 12. Frontend Node 20 Gate: FAIL (artifacts/proof/current/frontend_node_gate.log)
- 13. CI/Local Gate Parity Baseline: PASS (artifacts/proof/current/release_readiness.md)
- 14. Repair Report Generated: PASS (artifacts/proof/current/REPAIR_REPORT.md)

## Remaining Blockers

- check_false_claims
- backend_import
- backend_pytest
- check_migrations
- postgis_proof
- egress_proxy_proof
- demo_proof
- validate_sources
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
- map_route_check
- public_api_boundary
- archive_validation
