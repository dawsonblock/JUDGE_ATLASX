# PROOF_STATUS

## Current Proof Gate Status

| Check | Status | Log | Notes |
|-------|--------|-----|-------|
| Alpha gate | source-of-truth | artifacts/proof/current/release_gate.json | Canonical machine-readable gate output |
| Docker proof | ✓ PASS | artifacts/proof/current/docker_runtime_preflight.log | Container runtime verified |
| PostGIS proof | ✓ PASS | artifacts/proof/current/postgis_proof.log | Database integration verified |
| Egress proxy proof | ✓ PASS | artifacts/proof/current/egress_proxy_proof.log | Network boundaries validated |
| Demo proof | ✓ PASS | artifacts/proof/current/demo_proof.log | Synthetic scenario passed |
| Proof freshness | ✓ PASS | artifacts/proof/current/proof_freshness.log | Artifacts match tree state |
| Archive validation | ✓ PASS | artifacts/proof/current/archive_validation.log | Release archive format verified |
| Proof consistency | ✓ PASS | artifacts/proof/current/proof_consistency_pytest.log | release_gate/current proof docs aligned |

## Runtime Environment

- **Python version**: 3.11.7
- **Node version**: v20.20.2
- **npm version**: 10.8.2
- **Platform**: macOS-26.2-arm64
- **Database**: SQLite (test), PostgreSQL (PostGIS proof)
- **Docker**: Available and tested
- **production_ready**: false

## Proof Execution

All proof artifacts are stored under `artifacts/proof/current/` with timestamped run metadata.

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

---

**Canonical proof entry**: `artifacts/proof/current/CURRENT_PROOF.md`  
**Release readiness**: `artifacts/proof/current/release_readiness.md`
