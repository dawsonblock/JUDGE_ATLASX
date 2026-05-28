# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: 640c89b5c47c4629dd5b9b5c7929e002b8839b26e6a90f417b33684a2b02f4d1

## Proof Anchors
- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: 5604615c8904e0219e3a677b6446482b7a94a496f71673f82dd7c72154761b09
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: 2d0286bc7c1f87a4aea3cbb60f55b0c7648c7962e1b7a5f155e1b9d119c459bc
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: 484bf62cb033db22083c1a1bbb53e6d2e13bae0fd15c34fb5da8d33c8c77e50b

## Release Status
- release_classification: proof-hardened alpha release candidate
- alpha_gate_passed: true
- release_candidate: true
- production_ready: false
- proof_complete: true
- blocked_release_checks: []

## Build Metadata
- created_at_utc: 2026-05-28T22:09:07.947503+00:00
- generated_at_utc: 2026-05-28T22:09:07.947503+00:00
- git_commit: unknown
- python: unknown
- node: unknown
- npm: unknown

## Notes
- This is a proof-hardened alpha release candidate.
- It is not ready for production deployment.
- Ship only the archive listed above.
- Validation must run against a fresh extraction
  of that archive.
- `release_gate.json` is only valid as a proof artifact when every
  log path it references exists inside `artifacts/proof/current/`
  at packaging time. Do not ship manually zipped working trees.
