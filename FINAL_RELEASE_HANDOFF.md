# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: 2d35cf76cb23891443bc77596c9b63f43f7b15998b46d4e139fa5fb2cc9caf9e

## Proof Anchors
- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: 42ff58cf9a6f15e56ed095b62c20f637d133f9bf98e0cac1876df16cd3d8315e
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: f5057063f8e5ad36e32d2d3aeaf93f66528028bd5d18cf0e8cae2be864760b82
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: ef0c81f189ce1b487afcd5b4a1cf594bde8f6ba627eff53f7b967ad42d8b0644

## Release Status
- release_classification: proof-blocked alpha proof snapshot
- alpha_gate_passed: false
- release_candidate: false
- production_ready: false
- proof_complete: false
- blocked_release_checks: ["backend_pytest"]

## Build Metadata
- created_at_utc: 2026-05-29T04:03:55.684763+00:00
- generated_at_utc: 2026-05-29T04:03:55.684763+00:00
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
