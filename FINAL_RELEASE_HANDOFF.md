# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: c1e54413f2ddad00815a3ed0c11ab49a03ee5ef3db86eed2bdf0e4c924f1123f

## Proof Anchors
- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: 7f917e37666b8c47d30b86fcbe0ef3318de83c6e2f583aefb3efc726cc2dc76b
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: 108ba0dd85ad0830bdc8bc69067acd18df90ab55bf047dd22eb34be991eb6661
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: e1a0c4e7ab3f091389600c6f45dc9984b4e56a1cf5127ef3453ca9d17fa44a19

## Release Status
- release_classification: proof-blocked alpha proof snapshot
- alpha_gate_passed: false
- release_candidate: false
- production_ready: false
- proof_complete: false
- blocked_release_checks: ["backend_pytest", "docker_runtime_preflight", "docker_smoke", "postgis_proof"]

## Build Metadata
- generated_at_utc: 2026-05-27T01:30:31.597149+00:00
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
