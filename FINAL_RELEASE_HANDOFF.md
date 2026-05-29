# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: d9161d7d63fa12320a140c8e35b4175e84adfede6fd53a1ae1afa14f4bf86ba2

## Proof Anchors
- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: 9284e76affb8249ece258a54098606767a84b34c1540f17a8845b1f5237f290d
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: 28b902fea8dda03f2306fbeda1cc53518506f7814124b653adab053e86db44d1
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: 07b0767896166370379a5d34dbc1dbc54151cbc45a581876332be6e48e0bd4d0

## Release Status
- release_classification: proof-hardened alpha release candidate
- alpha_gate_passed: true
- release_candidate: true
- production_ready: false
- proof_complete: true
- blocked_release_checks: []

## Build Metadata
- created_at_utc: 2026-05-29T06:24:51.344149+00:00
- generated_at_utc: 2026-05-29T06:24:51.344149+00:00
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
