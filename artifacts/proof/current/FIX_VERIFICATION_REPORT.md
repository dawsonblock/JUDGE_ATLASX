# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-21T20:59:11.234851+00:00
- commit_hash: 8046eaf25db783d96747a08661e0e8b6a6fdec95
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

- canlii_staging_proof
- archive_validation
- proof_consistency_pytest
- required_proof_logs

## Canonical Artifacts

- artifacts/proof/current/release_gate.json
- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/REPAIR_REPORT.md
