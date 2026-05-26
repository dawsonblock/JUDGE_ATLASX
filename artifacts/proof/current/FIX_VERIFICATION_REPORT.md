# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-26T08:42:25.230719+00:00
- commit_hash: 409b7137dfeb1594a1dca484e39d243d02bbda34
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
- archive_validation: FAIL
- proof_freshness: PASS

## Release Blockers

- docker_runtime_preflight
- docker_smoke
- postgis_proof
- archive_validation

## Canonical Artifacts

- artifacts/proof/current/release_gate.json
- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/REPAIR_REPORT.md
