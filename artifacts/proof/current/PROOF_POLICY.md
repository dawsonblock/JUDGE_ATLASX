# PROOF_POLICY

- generated_at_utc: 2026-05-15T04:43:28.908943+00:00
- commit_hash: 16d6b61c15cc3785033a4c0435f2da1f81eb4e0d

## Canonical Current Artifacts

- Canonical proof output location is artifacts/proof/current/.
- release_gate.json is the machine-readable source of truth for gate state.
- CURRENT_PROOF.md and release_readiness.md are derived summaries from release_gate.json.
- CURRENT_ALPHA_STATUS.md and SOURCE_REGISTRY_STATUS.md are generated per run from the same gate payload.

## History And Retention

- Historical sidecars are archived to artifacts/proof/history/.
- artifacts/proof/current/ represents only the latest authoritative run.

## Truth Boundaries

- Release recommendation is blocked on any required failed or missing check.
- Operational posture remains alpha; production readiness is false.
- Evidence snapshots are authoritative; memory is derivative and non-authoritative.
