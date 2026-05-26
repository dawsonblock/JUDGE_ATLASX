# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive

- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: c1e54413f2ddad00815a3ed0c11ab49a03ee5ef3db86eed2bdf0e4c924f1123f

## Proof Anchors

- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: a2812784600d2c7ae7d8071ef6ca66524d2fe23a786ffce989b05170e7f48439
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: a644b4af2a6998428d92d149c07dafd921abb715dfa4e9755e91f2de941fc351
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: 4b471093e8069aa7b985673c762bdcd737b39054b8d2956bd294731030b6c83c

## Release Status

- release_classification: proof-blocked alpha proof snapshot
- alpha_gate_passed: false
- release_candidate: false
- production_ready: false
- proof_complete: false
- blocked_release_checks: ["docker_runtime_preflight", "docker_smoke", "postgis_proof", "archive_validation"]

## Build Metadata

- generated_at_utc: 2026-05-26T05:12:17.415740+00:00
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
