# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: 3397c2b54b889381534aa4aad053d0c6cf7aa39b94578d1462ad254017431645

## Proof Anchors
- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: 4371187a62347b33b5098615a12abad550b2d1d01ff4f7b885eb490b49b26b88
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: 0d520ac3a2c6f69037f3f5d01837d7bb97d3040e91de41d1b8762412bbba0a73
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: 957a5c4db7f68f6a00df9c177b4963bc86f5203e80952243eb6bbe7d83235025

## Release Status
- release_classification: proof-hardened alpha release candidate
- alpha_gate_passed: true
- release_candidate: true
- production_ready: false
- proof_complete: true
- blocked_release_checks: []

## Build Metadata
- generated_at_utc: 2026-05-28T20:31:39.576877+00:00
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
