# PROOF_STATUS

## Current Proof Gate Status

- Alpha gate: see artifacts/proof/current/release_gate.json.
- Release readiness: see artifacts/proof/current/release_readiness.md.
- Current proof summary: see artifacts/proof/current/CURRENT_PROOF.md.
- Individual log files are evidence artifacts, not manual status claims.

## Authority Notes

- Canonical machine truth is artifacts/proof/current/release_gate.json.
- This file summarizes proof state and must not override release_gate.json.
- Proof gate PASS, if present in canonical artifacts, indicates alpha proof-check completion only.
- production_ready remains false unless explicitly changed in canonical artifacts.
- Production-ready=false until all production gates pass.

## Runtime Environment

- **Python version**: 3.11.7
- **Node version**: v20.20.2
- **npm version**: 10.8.2
- **Platform**: macOS-26.2-arm64
- **Database**: SQLite (test), PostgreSQL (PostGIS proof)
- **Docker**: See canonical proof logs for the current run state.
- **production_ready**: false

## Proof Execution

All proof artifacts are stored under `artifacts/proof/current/` with timestamped run metadata.
Do not infer PASS from this file; read the canonical gate and current-proof outputs.

**Required proof commands:**

```bash
python3 scripts/check_path_hygiene.py
python3 scripts/check_no_generated_files.py --root .
python3 scripts/check_false_claims.py
python3 scripts/check_source_registry_docs.py
python3 scripts/check_proof_consistency.py
python3 scripts/check_proof_freshness.py
```

**Regenerate proof:**

```bash
make proof
```

## Canonical Policy

- Current release truth is derived from `artifacts/proof/current/release_gate.json`.
- Historical counts and phase narratives are non-authoritative if they conflict with canonical artifacts.
- Canonical repository posture is summarized in `STATUS.md`.

## Status Matrix

- authority: artifacts/proof/current/release_gate.json
- alpha_ready: true
- production_ready: false
- public_release_safe: false
- ingestion_coverage: 1/26 runnable sources (from canonical source-registry proof)
- AI_answering_enabled: true (derivative, evidence-cited alpha mode)
- workflow_admin_enabled: false (gated/experimental)
- live_map_enabled: false (gated)

---

**Canonical proof entry**: `artifacts/proof/current/CURRENT_PROOF.md`  
**Release readiness**: `artifacts/proof/current/release_readiness.md`
