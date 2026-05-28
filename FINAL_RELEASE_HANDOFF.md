# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: 326a1b5101e3678d4a9ba0e29444056b82a618c8eec1875d387913572df71e74

## Proof Anchors
- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: 789ae6422bec57b833e6b65b3190c60d3eecf20fddf6af36363b791471bce29f
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: 1ff336ccb8e12a29a3048dd445288772d65b21589192d067bc9e05aef09fa78c
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: b328709691688da16b923e9678070ad80ae2d9b393a608479ad0cdc8c7068034

## Release Status
- release_classification: proof-hardened alpha release candidate
- alpha_gate_passed: true
- release_candidate: true
- production_ready: false
- proof_complete: true
- blocked_release_checks: []

## Build Metadata
- generated_at_utc: 2026-05-28T20:02:59.380673+00:00
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
