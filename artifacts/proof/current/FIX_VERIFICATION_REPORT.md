# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-21T23:27:33.941231+00:00
- commit_hash: 2dcfdef4375f9db04bd5a10d80a1b142440c03bb
- alpha_gate_passed: false

## Required Gate Signals

- backend_compile: PASS
- backend_import: PASS
- backend_pytest: FAIL
- verify_evidence_store: PASS
- verify_audit_chain: PASS
- public_api_boundary: FAIL
- frontend_node_gate: PASS
- frontend_contracts: PASS
- archive_validation: MISSING
- proof_freshness: PASS

## Release Blockers

- backend_pytest
- check_node_policy
- public_api_boundary

## Canonical Artifacts

- artifacts/proof/current/release_gate.json
- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/REPAIR_REPORT.md
