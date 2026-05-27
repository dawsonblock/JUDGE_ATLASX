# JUDGE_ATLASX Comprehensive Repair Plan - Progress Report

**Date**: May 27, 2026  
**Status**: Phases 1-2 Complete, Phases 3-11 Planned

## Phases Completed ✅

### Phase 1: Public Platform Feature Flag ✅ COMPLETE
- **Objective**: Stop new public platform from breaking backend startup
- **Changes**:
  - Added `enable_public_platform: bool = False` to `backend/app/core/config.py`
  - Updated `backend/app/api/routes/__init__.py` with conditional lazy import
  - Added `JTA_ENABLE_PUBLIC_PLATFORM=false` to all 4 .env template files
- **Result**: Backend imports cleanly without public platform unless explicitly enabled
- **Commit**: `424fce8`

### Phase 2: Sync SQLAlchemy Conversion ✅ COMPLETE
- **Objective**: Convert public platform from async to repo's sync session model
- **Changes**:
  - Replaced `AsyncSession` with `Session` in `public_platform.py`
  - Changed `get_async_session` to `get_db` (matches app pattern)
  - Removed all `async def` and `await` keywords
  - Converted `public_release_policy.py` to sync
  - Added strict input validation (bbox, dates return HTTP 400 on error)
- **Result**: Public platform uses same sync SQLAlchemy as core app
- **Commit**: `7b2a359`

---

## Phases To Complete (Planned)

### Phase 3: Fix AI Service Boundary ⏳ PLANNED
**Problem**: Public AI services import Anthropic directly (not in dependencies, no LLM abstraction)  
**Solution**:
- Remove direct Anthropic imports from `public_crime_statute_linker.py` and `public_incident_explainer.py`
- Route through existing `backend/app/llm/provider.py` abstraction
- Create `backend/app/services/public_ai_suggestion_service.py`
- Ensure all AI output has `review_status="pending"` (never public by default)
- Add tests: `test_public_ai_boundary.py`, `test_public_ai_review_gate.py`

### Phase 4: Repair Alembic Migration Chain ⏳ PLANNED
**Problem**: Migration `20260527_0003` references wrong predecessor; missing FK/check constraints  
**Solution**:
- Update `down_revision = "20260522_0001"` (correct chain head)
- Add FK constraint: incident_id → geo_legal_events.id (CASCADE)
- Add check constraints: confidence_score ∈ [0,1], review_status ∈ {pending, approved, rejected, flagged}, relevance_score ∈ [0,1]
- Fix existing downgrade bugs in `20260520_0001`
- Tests: Verify upgrade/downgrade cycle works

### Phase 5: Fix Public Frontend Route Structure ⏳ PLANNED
**Problem**: Public UI in route group `(public)/` doesn't create `/public` paths; route collisions  
**Solution**:
- Move `frontend/app/(public)/` to `frontend/app/public/`
- Create missing routes:
  - `frontend/app/public/statute/[id]/page.tsx`
  - `frontend/app/public/methodology/page.tsx`
- Fix API calls: Add `frontend/lib/publicApi.ts` helper to set `NEXT_PUBLIC_API_BASE_URL`
- Build and typecheck to verify

### Phase 6: Align Public API Schemas ⏳ PLANNED
**Problem**: Schemas defined but responses return raw dicts with inconsistent names  
**Solution**:
- Add response_model to all endpoints: `@router.get(..., response_model=PublicMapIncidentsResponse)`
- Create missing schemas: `PublicStatutesSearchResponse`
- Generate TypeScript types in frontend matching backend schemas exactly
- Add contract tests: `test_public_platform_contracts.py`

### Phase 7: Repair Public Release Policy ⏳ PLANNED
**Problem**: Policy checks basics but misses legal/crime data requirements  
**Solution**:
- Add config: `public_min_confidence: float = 0.65`, `public_allowed_countries: list[str] = ["Canada"]`
- Require: country ∈ allowed list, confidence ≥ threshold, not juvenile/sealed/protected
- Add test cases: pending→hidden, no evidence→hidden, low confidence→hidden, non-Canada→hidden
- File: `test_public_release_policy.py`

### Phase 8: Fix Source/Public Status Vocabulary ⏳ PLANNED
**Problem**: Some docs still claim "production-ready"; misleading language  
**Solution**:
- Replace "production-ready" → "alpha-ready"
- Replace "100% Complete" → "core architecture complete, alpha proof candidate"
- Update docs: `PUBLIC_PLATFORM_README.md`, `docs/RELEASE_READINESS.md`, `docs/AI_LIMITATIONS.md`
- Run scripts: `check_false_claims.py`, `check_truth_claims.py --root .`

### Phase 9: Add Comprehensive Tests ⏳ PLANNED
**Test Files to Create**:
- `test_public_platform_flag.py` - Config imports without public_platform when disabled
- `test_public_platform_boundary.py` - Unpublished/pending/private incidents hidden
- `test_public_ai_boundary.py` - No live AI in GET routes, pending AI hidden
- `test_public_platform_migration_contract.py` - Migration integrity
- `frontend/tests/public-routes.contract.test.ts` - Routes exist, no collisions

**Key Assertions**:
- Default config: enable_public_platform == False
- Unpublished incidents never returned
- Pending-review AI suggestions never public
- Provider failures produce safe empty responses
- Migration FK/check constraints exist

### Phase 10: Regenerate Proof Artifacts ⏳ PLANNED
**Current Issues**:
- Tree hash mismatch (code changed, proof stale)
- Missing: backend_pytest.log, frontend_build.log, docker_smoke.log, runtime_smoke.log

**Process**:
1. Run local checks:
   ```bash
   python3 scripts/check_false_claims.py
   python3 scripts/check_source_keys.py
   python3 scripts/check_statuses.py
   ```

2. Backend verification:
   ```bash
   cd backend && python -m compileall -q app
   pytest -q app/tests
   ```

3. Frontend verification:
   ```bash
   cd frontend && npm run typecheck && npm run build
   ```

4. Regenerate proof:
   ```bash
   python3 scripts/regenerate_proof.py
   python3 scripts/check_proof_freshness.py
   ```

### Phase 11: Package Clean Archive ⏳ PLANNED
**After all proof gates pass**:
```bash
make release-package-proof-local
python3 scripts/validate_final_zip.py dist/JUDGE_ATLAS-main-final.zip
```

---

## Quick Reference: Acceptance Checks

### Phase 1 ✅
```bash
cd backend
python -m compileall -q app  # Should pass
python scripts/proof_backend_import.py  # Should pass
```

### Phase 2 ✅
```bash
cd backend
python -m compileall -q app  # Should pass (no AsyncSession errors)
```

### Phase 3 (Next)
```bash
cd backend
python scripts/proof_backend_import.py  # Check no direct Anthropic imports
pytest app/tests/test_public_ai_boundary.py -v
```

### Phase 4 (After Phase 3)
```bash
cd backend
alembic heads  # Should show single head
alembic upgrade head
alembic downgrade -1
alembic upgrade head  # Cycle should work
```

### Phase 5 (After Phase 4)
```bash
cd frontend
npm run typecheck  # No route collision errors
npm run build  # Should build successfully
```

### Final Gate (All Phases)
```bash
python3 scripts/check_false_claims.py  # PASS
python3 scripts/check_proof_freshness.py  # PASS
python3 scripts/verify_proof_hash_sync.py --root .  # PASS
```

---

## Target End State

| Layer | Target | Status |
|-------|--------|--------|
| **Backend** | FastAPI imports cleanly, public API feature-gated | ✅ Achieved |
| **Database** | Alembic chain valid, migrations work | ⏳ Phase 4 |
| **AI Services** | Routed through LLM abstraction, no direct imports | ⏳ Phase 3 |
| **Frontend** | Routes don't collide, /public/* paths work | ⏳ Phase 5 |
| **Public API** | Responses match schemas, review-gated | ⏳ Phase 6 |
| **Release Policy** | Strict rules, Canada-first, confidence threshold | ⏳ Phase 7 |
| **Documentation** | No false production-ready claims | ⏳ Phase 8 |
| **Tests** | Comprehensive coverage, all gates pass | ⏳ Phase 9 |
| **Proof** | Current tree hash matches artifacts | ⏳ Phase 10 |
| **Archive** | Clean final package ready for distribution | ⏳ Phase 11 |

---

## Commands to Continue

To proceed with Phase 3 (AI service boundary fix):

```bash
# 1. Check current Anthropic imports
grep -r "from anthropic import" backend/app/services/

# 2. Examine existing LLM abstraction
cat backend/app/llm/provider.py
cat backend/app/llm/reviewer_assistant.py

# 3. Create new suggestion service (stub for now)
cat > backend/app/services/public_ai_suggestion_service.py << 'EOF'
# To be implemented
EOF

# 4. Run import check
cd backend && python -m compileall -q app
python scripts/proof_backend_import.py
```

---

## Summary

**Completed**: Foundation stabilized (feature flag + sync conversion)  
**Status**: Ready to proceed with Phase 3  
**Risk**: Low - disabled by default until all phases pass  
**Next Step**: Remove direct Anthropic imports, route through LLM abstraction
