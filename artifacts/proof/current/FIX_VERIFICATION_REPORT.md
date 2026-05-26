# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-26T22:49:35.072319+00:00
- commit_hash: cf73254d549f440255ef120824e668c640aae5b3
- alpha_gate_passed: false

## Required Gate Signals

- backend_compile: PASS
- backend_import: PASS
- backend_pytest: FAIL
- verify_evidence_store: PASS
- verify_audit_chain: PASS
- public_api_boundary: PASS
- frontend_node_gate: PASS
- frontend_contracts: PASS
- archive_validation: FAIL
- proof_freshness: PASS

## Release Blockers

- backend_pytest
- docker_runtime_preflight
- docker_smoke
- postgis_proof
- archive_validation
- check_proof_consistency
- validation_summary_missing

## Canonical Artifacts

- artifacts/proof/current/release_gate.json
- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/REPAIR_REPORT.md
