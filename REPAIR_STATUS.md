# JUDGE_ATLASX Public Platform Repair Status

> [!WARNING]
> **STATUS:** Alpha-stage repair in progress. Code is functional but requires hardening before any deployment.
> **Authority**: This repair log. Do not deploy without completing hardening checklist.

## Phase 0: Baseline Capture ✅ Complete

Baseline failures documented:
- Import errors in public_platform.py (GeoLegalEvent incorrect import)
- Misplaced ORM fields in IncidentNewsLink (user session fields)
- Hardcoded status strings without canonical constants
- False production-ready claims in documentation

## Phase 1: Fix Import/Runtime Blockers ✅ Complete

**Step 1.1: Fixed GeoLegalEvent import** ✅
- File: `backend/app/api/routes/public_platform.py`
- Changed: Import from `geo_legal_event.py` instead of `entities.py`
- Removed duplicate `GeoLegalEventModel` alias

**Step 1.2: Removed misplaced ORM fields** ✅
- File: `backend/app/models/entities.py`
- Removed: `ip_hash` and `user` relationship from `IncidentNewsLink`
- These fields belong to `UserSession`, not news links

## Phase 2: Alembic Migration ✅ Verified

**Step 2.1: Migration chain linear** ✅
- File: `backend/alembic/versions/20260527_0003_public_platform_schema.py`
- Status: Correct `down_revision = '20260516_0002'`
- No accidental branch heads

## Phase 3: Fix Status Constants ✅ Complete

**Step 3.1: Created canonical status constants** ✅
- File: `backend/app/services/public_link_statuses.py` (NEW)
- Defines: `LINK_REVIEW_STATUS_PENDING`, `LINK_METHOD_MANUAL`, etc.

**Step 3.2: Replaced hardcoded strings** ✅
- File: `backend/app/services/public_crime_statute_linker.py`
  - Changed: `review_status="pending"` → `review_status=LINK_REVIEW_STATUS_PENDING`
- File: `backend/app/services/public_news_linker.py`
  - Changed: `link_method="manual"` → `link_method=LINK_METHOD_MANUAL`

## Phase 4: Fix False Claims ✅ In Progress

**Step 4.1: Updated documentation** ✅
- File: `README_PLATFORM.md`
  - Changed: "Production-Ready ✓" → "Alpha - Ready for Local Testing"
  - Changed: "100% Complete" → "Core architecture complete, subject to review"
  - Removed: Checkmark celebrations
  - Added: References to hardening requirements

**Step 4.2: Removed false claim files** ✅
- Deleted: `DEPLOYMENT_COMPLETE.txt` (false "ready for production")
- Deleted: `PLATFORM_IMPLEMENTATION_SUMMARY.md` (overstated completeness)

## Phase 5: Hardening ✅ 50% Complete

### 5.1: Public Release Policy Service ✅ Complete
- File: `backend/app/services/public_release_policy.py` (NEW)
- Implements: `is_incident_publicly_releasable()`
  * Requires: publish_status == published, review_status == approved
  * Requires: Has linked evidence (source_ids/evidence_ids/claim_ids)
  * Requires: Not suppressed/disputed, valid coordinates, no private metadata
- Implements: `is_statute_link_publicly_releasable()`
  * Requires: review_status == approved, confidence > 0, has reason
- Implements: `is_news_link_publicly_releasable()`
  * Requires: valid URL, title, positive relevance score

### 5.2: Response Serialization ✅ Complete
- File: `backend/app/api/schemas/public_schemas.py` (NEW)
- Created allowlisted response models:
  * PublicIncidentMapItem (map visualization, safe fields only)
  * PublicIncidentDetail (full incident, no private fields)
  * PublicStatuteLink (statute with link_reason and confidence)
  * PublicNewsLink (news with relevance score)
  * PublicIncidentWithLinks (incident + all links)
  * PublicMapIncidentsResponse (structured map response)
- Explicit allowlisting prevents exposure of:
  * raw_payload, scrape_metadata, private_notes
  * internal_review_notes, unreviewed AI summaries
  * internal_status, source_list, claim_ids (raw)

### 5.3: Public API Boundary ✅ Complete
- File: `backend/app/api/routes/public_platform.py`
- Updated map endpoint:
  * Filters incidents via PublicReleasePolicy.is_incident_publicly_releasable()
  * Returns PublicMapIncidentsResponse (schema-backed)
  * Counts approved statute links + news links
  * Never returns unapproved/unpublished/private incidents
- Imports now include policy + schemas

### 5.4: Negative Security Tests ✅ Complete
- File: `backend/app/tests/test_public_platform_boundary.py` (NEW)
- 15 incident visibility tests:
  * Unpublished incidents hidden ✓
  * Pending-review incidents hidden ✓
  * Rejected incidents hidden ✓
  * Incidents without evidence hidden ✓
  * Missing coordinates hidden ✓
  * Invalid coordinates hidden ✓
  * Suppressed incidents hidden ✓
  * Approved + published + evidence-linked = public ✓
- 3 statute link tests:
  * Pending links hidden ✓
  * Approved links public ✓
  * Zero confidence hidden ✓
- 3 news link tests:
  * No URL = hidden ✓
  * Zero relevance = hidden ✓
  * Valid = public ✓
- Tests prevent regression of security boundary

### 5.5: Frontend Validation (⏳ TODO - Next Phase)
- [ ] Coordinate validation guards in PublicCrimeMap.tsx
- [ ] Source badges (Reviewed Evidence, AI-Suggested, etc.)
- [ ] Hide pending-review items
- [ ] Label derivative summaries

### 5.6: Proof Artifacts (⏳ TODO - Final Phase)
- [ ] Regenerate from current tree after frontend complete
- [ ] Run: `python scripts/check_proof_consistency.py`
- [ ] Run: `python scripts/check_proof_freshness.py`
- [ ] Run: `python scripts/check_false_claims.py`
- [ ] All must PASS

## Current Gate State

```json
{
  "phase_1_imports_fixed": true,
  "phase_2_migrations_validated": true,
  "phase_3_status_constants": true,
  "phase_4_false_claims_removed": true,
  "phase_5_hardening_50_percent": true,
  "public_boundary_enforced": true,
  "security_tests_written": true,
  "code_compiles": "pending_test",
  "imports_work": "pending_test",
  "proof_artifacts_valid": false,
  "production_ready": false
}
```

**Status**: 50% of required hardening complete. Frontend validation and proof regeneration remaining.

---

## Files Changed in This Repair

**Phase 1-4 (Completed):**
1. ✅ `backend/app/api/routes/public_platform.py` - Import fix, endpoint hardening
2. ✅ `backend/app/models/entities.py` - Remove misplaced fields
3. ✅ `backend/app/services/public_crime_statute_linker.py` - Status constants
4. ✅ `backend/app/services/public_news_linker.py` - Status constants
5. ✅ `backend/app/services/public_link_statuses.py` - NEW: Canonical constants
6. ✅ `README_PLATFORM.md` - Corrected claims
7. ✅ Deleted: `DEPLOYMENT_COMPLETE.txt`
8. ✅ Deleted: `PLATFORM_IMPLEMENTATION_SUMMARY.md`

**Phase 5 (50% Complete):**
9. ✅ `backend/app/services/public_release_policy.py` - NEW: Release gate
10. ✅ `backend/app/api/schemas/public_schemas.py` - NEW: Allowlisted responses
11. ✅ `backend/app/tests/test_public_platform_boundary.py` - NEW: Security tests

**Still TODO:**
- Frontend: Add validation + badges
- Proof: Regenerate artifacts

---

## Next Action

**Phase 5.5: Frontend validation** (2 files)
1. Update `frontend/components/public/PublicCrimeMap.tsx`:
   - Add coordinate validation guards
   - Add source badges (Reviewed vs AI-Suggested vs News)
   - Skip invalid coordinates
   - Hide pending-review items

2. Update `frontend/app/(public)/incident/[id]/page.tsx`:
   - Label AI summaries as "derivative"
   - Show "Approved" badge for statute links
   - Show publication date for news links

Then Phase 5.6: Regenerate proof artifacts and verify
