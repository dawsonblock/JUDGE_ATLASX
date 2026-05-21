# PROOF_STATUS

## Current Proof Gate Status

| Check | Status | Log | Notes |
|-------|--------|-----|-------|
| Alpha gate | source-of-truth | artifacts/proof/current/release_gate.json | Canonical machine-readable gate output |
| Docker proof | ✓ PASS | artifacts/proof/current/docker_proof.log | Container runtime verified |
| PostGIS proof | ✓ PASS | artifacts/proof/current/postgis_proof.log | Database integration verified |
| Egress proxy proof | ✓ PASS | artifacts/proof/current/egress_proxy_proof.log | Network boundaries validated |
| Demo proof | ✓ PASS | artifacts/proof/current/demo_proof.log | Synthetic scenario passed |
| Proof freshness | ✓ PASS | artifacts/proof/current/proof_freshness.log | Artifacts match tree state |
| Archive validation | ✓ PASS | artifacts/proof/current/archive_validation.log | Release archive format verified |
| Proof consistency | ✓ PASS | scripts/check_proof_consistency.py | release_gate/current proof docs aligned |

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

## Known Blockers Resolved (Phase 1–5)

✓ No generated files (`__pycache__`, `*.pyc`)  
✓ No environment files (`.env.development` removed)  
✓ No proof history/logs in release archive  
✓ Root status docs created  
✓ Builder/validator contract aligned  

## Completion State (Phase 6–13)

- False-claim scanner hardening (Phase 6): complete
- Node version standardization to 20 (Phase 7): complete
- Python version standardization to 3.11 (Phase 8): complete
- Source registry regeneration (Phase 10): complete
- Proof freshness verification (Phase 11): complete
- Final archive validation (Phase 12): complete
- Status documents finalization (Phase 13): complete

---

**Canonical proof entry**: `artifacts/proof/current/CURRENT_PROOF.md`  
**Release readiness**: `artifacts/proof/current/release_readiness.md`
