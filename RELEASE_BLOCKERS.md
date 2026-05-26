# RELEASE_BLOCKERS

## Alpha Gate Status

- Source-of-truth blocker state is defined by artifacts/proof/current/release_gate.json.
- Source-of-truth readiness narrative is defined by artifacts/proof/current/release_readiness.md.
- Canonical status file is STATUS.md.
- Canonical current proof summary is artifacts/proof/current/CURRENT_PROOF.md.
- Alpha gate pass/fail is not a production readiness claim.

## Current Blocker Policy

- Treat release_gate.json as the only authoritative blocker source.
- Treat release_readiness.md as the only authoritative blocker narrative.
- Manual summaries in this file must never mark phases PASS unless the canonical artifacts say so for the current run.
- If artifacts/proof/current/release_gate.json and this file disagree, the gate wins.

## Deferred by Plan (Non-Blocking)

- Phase 14 bi-temporal foundation remains deferred until after clean-alpha gate completion.

## Status Assertion

- release_status: derive from artifacts/proof/current/release_gate.json
- production_ready: false
- operational_posture: alpha

## Interpretation

- Current alpha release state must be read from the canonical gate artifacts for the current run.
- Deferred scope items are non-blocking only when the current canonical gate artifacts say the alpha gate passed.
