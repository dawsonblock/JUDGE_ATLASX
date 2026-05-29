# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-29T04:03:10.100234+00:00
- commit_hash: d0c67be8509754d370c3d2807bba0f54082ceb99
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
- archive_validation: PASS
- proof_freshness: PASS

## Release Blockers

- backend_pytest

## Canonical Artifacts

- artifacts/proof/current/release_gate.json
- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/REPAIR_REPORT.md
