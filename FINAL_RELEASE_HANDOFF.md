# Final Release Handoff

This document is generated from the built archive and
canonical proof artifacts.
Manual edits are not authoritative.

## Authoritative Archive
- Path: dist/JUDGE_ATLAS-main-final.zip
- SHA-256: c1e54413f2ddad00815a3ed0c11ab49a03ee5ef3db86eed2bdf0e4c924f1123f

## Proof Anchors
- release_gate_path: artifacts/proof/current/release_gate.json
- release_gate_sha256: c075e760a1073eb7fe228d96040abeac9aedd6a9ccce91ca2d2cbd732c3b1529
- proof_manifest_path: artifacts/proof/current/proof_manifest.json
- proof_manifest_sha256: ac23ce8abaf4f34870e12b987a6135deee1167659b630b20edc862c6f33742fd
- required_log_index_path: artifacts/proof/current/required_log_index.json
- required_log_index_sha256: f216c5fac6c144b3e87179da737ed3fd494204d8d9122208f76c638343d10500

## Release Status
- release_classification: proof-blocked alpha proof snapshot
- alpha_gate_passed: false
- release_candidate: false
- production_ready: false
- proof_complete: false
- blocked_release_checks: ["docker_runtime_preflight", "docker_smoke", "postgis_proof"]

## Build Metadata
- generated_at_utc: 2026-05-27T02:43:11.124918+00:00
- git_commit: unknown
- python: 3.11.7
- node: v20.20.2
- npm: 10.8.2

## Notes
- This is a proof-blocked alpha proof snapshot.
- It is not ready for production deployment.
- Ship only the archive listed above.
- Validation must run against a fresh extraction
  of that archive.
