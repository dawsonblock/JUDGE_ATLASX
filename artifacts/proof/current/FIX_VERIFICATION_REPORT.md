# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-26T20:25:25.616634+00:00
- commit_hash: f22ed8f3a52ae673031ee0886dea92387564956c
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
- archive_validation: PASS
- proof_freshness: PASS

## Release Blockers

- docker_runtime_preflight
- docker_smoke
- postgis_proof

## Canonical Artifacts

- artifacts/proof/current/release_gate.json
- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/CURRENT_PROOF.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/REPAIR_REPORT.md
