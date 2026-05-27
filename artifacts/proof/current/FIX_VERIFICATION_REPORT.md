# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-27T20:35:42.165058+00:00
- commit_hash: 06663bce861b92ec736fdebaadef7f86543baef5
- alpha_gate_passed: false

## Required Gate Signals

- backend_compile: PASS
- backend_import: PASS
- backend_pytest: PASS
- verify_evidence_store: PASS
- verify_audit_chain: PASS
- public_api_boundary: PASS
- frontend_node_gate: PASS
- frontend_contracts: PASS
- archive_validation: MISSING
- proof_freshness: PASS

## Release Blockers

- archive_validation
- check_proof_consistency
- check_proof_manifest
- required_proof_logs

## Canonical Artifacts

- artifacts/proof/current/release_gate.json
- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/REPAIR_REPORT.md
