# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: 81742f38c587c170bfdd2246dcbb8ee83d1b0568ea5647618507b6faa9b3c659

## Proof Anchors
- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: 1758cb9e1db3460cf4a4188786942db1b00d59a8853f48c72f06b1cab359eae9
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: 5da664f7c02a5fe7d52da3ba88ba0864d5ff98982855b961bae44f14a54c3bcb
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: 87ab2e6aeb7e0184cddc57d43a4fe2e2e06db92eb48522351af816458136aee1

## Release Status
- release_classification: proof-blocked alpha proof snapshot
- alpha_gate_passed: false
- release_candidate: false
- production_ready: false
- proof_complete: false
- blocked_release_checks: ["check_no_pyc", "backend_pytest", "repo_generated_files"]

## Build Metadata
- created_at_utc: 2026-05-29T02:01:29.212736+00:00
- generated_at_utc: 2026-05-29T16:00:00+00:00
- git_commit: unknown
- python: unknown
- node: unknown
- npm: unknown

## Notes
- This is a proof-blocked alpha proof snapshot.
- It is not ready for production deployment.
- Ship only the archive listed above.
- Validation must run against a fresh extraction
  of that archive.
- `release_gate.json` is only valid as a proof artifact when every
  log path it references exists inside `artifacts/proof/current/`
  at packaging time. Do not ship manually zipped working trees.
