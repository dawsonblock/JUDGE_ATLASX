# Final Release Handoff

This document is generated from the built archive and canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: 11e22eb97bb75a542f8bc1fe9cd41e37816c4beb96bef1f5920a0b598a022d63

## Proof Anchors
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- required_log_index_path: artifacts/proof/current/required_log_index.json
- release_gate_path: artifacts/proof/current/release_gate.json

## Release Status
- release_classification: proof-hardened alpha release candidate
- alpha_gate_passed: true (if all validators pass from extraction)
- release_candidate: true (if all validators pass from extraction)
- production_ready: false (by design for alpha)
- self_verifying: true (archive proves itself)

## Distributable Archive
- Path: dist/JUDGE_ATLAS-main-final-distributable.zip
- Contains: JUDGE_ATLAS-main-final.zip + metadata
- Verification: Extract and run scripts/check_proof_consistency.py --root .

## Notes
- This is a proof-hardened alpha release candidate.
- It is NOT ready for production deployment.
- Ship ONLY: dist/JUDGE_ATLAS-main-final-distributable.zip
- Do NOT ship working-directory archives.
