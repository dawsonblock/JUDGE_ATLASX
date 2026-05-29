# JUDGE_ATLAS — PROOF CHAIN REPAIR ACTION CHECKLIST

**Status:** Deep extraction verdict identified 8 specific blockers  
**Classification:** Uploaded ZIP is source snapshot, not release archive  
**Next Step:** Execute these 8 priorities in order

---

## PRIORITY 1: Fix Upload Process ⚠️ BLOCKING

**Current State:** Uploaded ZIP is manually-zipped workspace, not `dist/JUDGE_ATLAS-main-final.zip`

**What To Do:**
- [ ] Locate packaging script: `scripts/build_release_archive.py` or `scripts/package_and_validate_release_archive.sh`
- [ ] Run packaging script locally
- [ ] Verify output is `dist/JUDGE_ATLAS-main-final.zip`
- [ ] Verify SHA-256 matches expected canonical hash (or document new hash)
- [ ] Upload ONLY the packaged archive, not workspace snapshots

**Command:**
```bash
bash scripts/package_and_validate_release_archive.sh
# OR
python3 scripts/build_release_archive.py --output dist/JUDGE_ATLAS-main-final.zip
```

**Success Criteria:**
- Output archive exists: `dist/JUDGE_ATLAS-main-final.zip`
- Archive is not a workspace snapshot
- Archive contains proof metadata

**Blocker Location:** `.gitignore` excludes `*.log` globally but packaging script should whitelist `artifacts/proof/current/*.log`

---

## PRIORITY 2: Fix Backend Pytest Failure ⚠️ BLOCKING

**Current State:** `backend_pytest` failed in batch 5; log missing

**What To Do:**
- [ ] Identify tests in batch 5 (spans memory_invalidation through public_graph_api_safety)
- [ ] Run failing batch to get exact traceback:
  ```bash
  cd backend/
  pytest app/tests/test_memory_invalidation.py -v
  pytest app/tests/test_*.py -k "memory or mutation or source or public" -v
  ```
- [ ] Fix failing test or code
- [ ] Regenerate proof logs:
  ```bash
  # Run your canonical proof pipeline
  # Output should be in artifacts/proof/current/
  ```
- [ ] Verify new `backend_pytest.log` is created
- [ ] Verify `backend_pytest_chunked_status.json` shows all batches PASS

**Success Criteria:**
- `pytest_passed` count is 404 or higher (at least one more than current)
- `backend_pytest_chunked_status.json` all batches PASS
- `backend_proof_summary.json` overall_status = PASS
- `backend_pytest.log` contains full test output

**Test Categories in Batch 5:**
- Memory invalidation
- Mutation/RBAC enforcement
- Source boundary validation
- Production preflight checks
- Public API safety
- Public graph security

---

## PRIORITY 3: Ensure All 53 Proof Logs in Archive ⚠️ BLOCKING

**Current State:** 0 of 53 referenced logs present in uploaded ZIP

**What To Do:**
- [ ] Review `.gitignore`:
  ```
  *.log               # This excludes all .log files
  artifacts/proof/current/*.log    # Verify this exception exists
  ```
- [ ] Ensure packaging script includes proof logs:
  ```bash
  # Inside packaging script, should have:
  # - Special handling for artifacts/proof/current/*.log
  # - Whitelist exception to .gitignore
  ```
- [ ] After packaging, verify logs are included:
  ```bash
  unzip -l dist/JUDGE_ATLAS-main-final.zip | grep ".log" | wc -l
  # Should be >= 53
  ```
- [ ] Verify proof manifest lists all logs:
  ```bash
  unzip -l dist/JUDGE_ATLAS-main-final.zip | grep proof_manifest.json
  cat artifacts/proof/current/proof_manifest.json | jq '.referenced_logs | length'
  # Should be 53
  ```

**Success Criteria:**
- `unzip -l dist/JUDGE_ATLAS-main-final.zip | grep ".log"` returns 53+ entries
- `artifacts/proof/current/release_gate.json` lists all logs
- `artifacts/proof/current/proof_manifest.json` lists all logs
- All listed logs exist in archive

**Files That Must Be Included:**
- `artifacts/proof/current/backend_pytest.log`
- `artifacts/proof/current/frontend_build.log`
- `artifacts/proof/current/docker_smoke.log`
- `artifacts/proof/current/runtime_smoke.log`
- `artifacts/proof/current/release_gate.log`
- `artifacts/proof/current/proof_consistency_pytest.log`
- (and 47 more)

---

## PRIORITY 4: Regenerate REPAIR_REPORT.md 🔴 REQUIRED

**Current State:** Missing from uploaded ZIP; packaging script requires it

**What To Do:**
- [ ] Locate canonical REPAIR_REPORT.md (should be in `artifacts/proof/current/`)
- [ ] If missing, create it with:
  - Summary of 22-step repair executed
  - Root causes fixed
  - Current proof state
  - Known remaining issues
- [ ] Ensure it's in the workspace before packaging
- [ ] After packaging, verify it's in archive:
  ```bash
  unzip -l dist/JUDGE_ATLAS-main-final.zip | grep REPAIR_REPORT.md
  ```

**Success Criteria:**
- `artifacts/proof/current/REPAIR_REPORT.md` exists before packaging
- Archive contains `artifacts/proof/current/REPAIR_REPORT.md`
- Content matches what was executed

---

## PRIORITY 5: Remove Stale Secondary Proof Files 🟡 CLEANUP

**Current State:** Local paths leaked in old files; old release claims present

**Files to Review/Remove:**
- [ ] `artifacts/proof/release_readiness.md` — contains `/Users/dawsonblock/...`
- [ ] `REPAIR_EXECUTION_STATUS.md` — contains local paths if not canonical
- [ ] Any other files in `artifacts/proof/` with old wording or local paths

**What To Do:**
1. For each file, check for:
   - [ ] Local absolute paths (`/Users/...`, `/home/...`)
   - [ ] Stale release claims (`production_ready: true`, `alpha_gate_passed: true`)
   - [ ] Outdated dates or repair references

2. If found:
   - [ ] Delete the file, OR
   - [ ] Move to `artifacts/proof/archive/`, OR
   - [ ] Regenerate under canonical path with correct content

3. After cleanup, audit all remaining files in `artifacts/proof/current/` for local paths:
   ```bash
   grep -r "/Users/" artifacts/proof/current/
   grep -r "/home/" artifacts/proof/current/
   # Should return 0 results
   ```

**Success Criteria:**
- No local absolute paths in released proof files
- No stale release claims
- All proof files dated recent or explicitly archived
- Packaging script validates no local paths before archiving

---

## PRIORITY 6: Fix required_log_index.json Generation 🟡 VALIDATION

**Current State:** Claims `"exists": true` but referenced logs are absent from archive

**What To Do:**
- [ ] Review `required_log_index.json` generation logic
- [ ] Add validation step:
  ```python
  # In generation code:
  # If logging "exists": true, verify files are in the packaged archive
  # Calculate hash against actual final archive
  # Set exists = false if any referenced file missing
  ```
- [ ] Make packaging fail if `exists: true` but files missing:
  ```bash
  # In packaging script:
  # Run check_required_proof_logs.py against final archive
  # Fail build if FAIL returned
  ```
- [ ] Update `required_log_index.json` format:
  - Keep `missing_required_logs` list current
  - Only set `exists: true` if all listed logs present
  - Add `validation_archive_sha256` to tie validation to specific archive

**Success Criteria:**
- `required_log_index.json` only says `exists: true` when all logs are present in archive
- Packaging script validates this before declaring success
- If `exists: true`, running validation tools on extracted archive confirms PASS

---

## PRIORITY 7: Fix archive_hash Naming 🟡 METADATA

**Current State:** Field labeled `archive_hash` contains 40-char commit hash, not SHA-256

**What To Do:**
- [ ] Locate `proof_manifest.json` generation
- [ ] Change field name:
  ```json
  // BEFORE:
  "archive_hash": "d0c67be8509754d370c3d2807bba0f54082ceb99"
  
  // AFTER:
  "archive_sha256": "2d35cf76cb23891443bc77596c9b63f43f7b15998b46d4e139fa5fb2cc9caf9e"
  
  // IF commit hash needed:
  "source_commit": "d0c67be8509754d370c3d2807bba0f54082ceb99"
  ```
- [ ] Add format validation in generation:
  ```python
  if len(archive_sha256) != 64:
    raise ValueError("archive_sha256 must be 64-char SHA-256, not " + len(archive_sha256))
  ```
- [ ] Update documentation/handoff files to use new field names
- [ ] Regenerate `proof_manifest.json` with correct hash

**Success Criteria:**
- `proof_manifest.json` uses `archive_sha256` (not `archive_hash`)
- `archive_sha256` value is 64 characters (real SHA-256)
- `archive_sha256` matches actual packaged archive hash
- If commit hash needed, stored under `source_commit`

**Example Correct Format:**
```json
{
  "archive_sha256": "2d35cf76cb23891443bc77596c9b63f43f7b15998b46d4e139fa5fb2cc9caf9e",
  "source_commit": "3845982",
  "release_date": "2026-05-29",
  "proof_count": 53
}
```

---

## PRIORITY 8: Remove Forbidden Directories 🟡 HYGIENE

**Current State:** `.trunk/` found in uploaded ZIP; forbidden for release archives

**What To Do:**
- [ ] Create `.buildarchiveignore` or update packaging script to exclude:
  - [ ] `.trunk/` — tool cache
  - [ ] `.idea/` — IDE config
  - [ ] `.vscode/settings.json` — editor config (keep extensions.json if exists)
  - [ ] `.DS_Store` — macOS metadata
  - [ ] `Thumbs.db` — Windows metadata
  - [ ] `*.swp`, `*~` — editor temp files
  - [ ] Build caches not needed for validation

- [ ] Update packaging script to exclude these:
  ```bash
  # In build_release_archive.py:
  def _is_excluded(path):
    forbidden = {'.trunk', '.idea', '.DS_Store', 'Thumbs.db'}
    return any(fb in path for fb in forbidden)
  ```

- [ ] After packaging, verify none present:
  ```bash
  unzip -l dist/JUDGE_ATLAS-main-final.zip | grep -E "\.trunk|\.idea|\.DS_Store|Thumbs"
  # Should return 0 results
  ```

**Success Criteria:**
- No `.trunk/` in archive
- No IDE/editor configs in archive
- No system metadata files in archive
- Packaging script excludes these by default

---

## VALIDATION COMMANDS (Run After Each Priority)

### After Priority 1 (Packaging):
```bash
unzip -l dist/JUDGE_ATLAS-main-final.zip | head -20
# Verify archive exists and contains expected root folder
```

### After Priority 2 (Backend Fix):
```bash
python3 scripts/check_required_proof_logs.py --root artifacts/
# Should return: PASS (not the uploaded ZIP, but current workspace)
```

### After Priority 3 (Proof Logs):
```bash
unzip -l dist/JUDGE_ATLAS-main-final.zip | grep ".log" | wc -l
# Should be >= 53
```

### After Priority 4 (REPAIR_REPORT):
```bash
unzip -l dist/JUDGE_ATLAS-main-final.zip | grep REPAIR_REPORT.md
# Should return 1 entry
```

### After Priority 5 (Cleanup):
```bash
unzip -p dist/JUDGE_ATLAS-main-final.zip artifacts/proof/current/release_readiness.md | grep "/Users/"
# Should return 0 results (file removed or cleaned)
```

### After Priority 6 (required_log_index):
```bash
python3 scripts/check_required_proof_logs.py --archive dist/JUDGE_ATLAS-main-final.zip
# Should return: PASS
```

### After Priority 7 (archive_hash):
```bash
unzip -p dist/JUDGE_ATLAS-main-final.zip artifacts/proof/current/proof_manifest.json | jq '.archive_sha256'
# Should return 64-char SHA-256, not 40-char commit hash
```

### After Priority 8 (Remove Forbidden):
```bash
unzip -l dist/JUDGE_ATLAS-main-final.zip | grep -E "\.trunk|\.idea|\.DS_Store"
# Should return 0 results
```

---

## EXECUTION ORDER

Execute in this order (dependencies exist):

```
1. Priority 1: Upload Process            (BLOCKING)
   ↓
2. Priority 2: Backend Pytest Fix         (BLOCKING)
   ↓
3. Priority 3: Include All Proof Logs     (BLOCKING)
   ↓
4. Priority 4: Regenerate REPAIR_REPORT   (REQUIRED)
   ↓
5. Priority 5: Remove Stale Files         (CLEANUP)
   ↓
6. Priority 6: Fix required_log_index     (VALIDATION)
   ↓
7. Priority 7: Fix archive_hash           (METADATA)
   ↓
8. Priority 8: Remove Forbidden Dirs      (HYGIENE)
   ↓
✅ FINAL: Package & Validate
```

---

## SUCCESS CRITERIA — FINAL VALIDATION

After completing all 8 priorities, the final archive should pass:

```bash
# Hash validation
shasum -a 256 dist/JUDGE_ATLAS-main-final.zip
# Should show canonical hash

# Proof logs
python3 scripts/check_required_proof_logs.py --archive dist/JUDGE_ATLAS-main-final.zip
# Result: PASS

# Proof consistency
python3 scripts/check_proof_consistency.py --archive dist/JUDGE_ATLAS-main-final.zip
# Result: PASS

# Proof manifest
python3 scripts/check_proof_manifest.py --archive dist/JUDGE_ATLAS-main-final.zip
# Result: PASS

# Gate status
unzip -p dist/JUDGE_ATLAS-main-final.zip artifacts/proof/current/release_gate.json | jq '.'
# Result: all referenced proof logs present in archive

# No forbidden files
unzip -l dist/JUDGE_ATLAS-main-final.zip | grep -E "\.trunk|\.idea|/Users/" 
# Result: 0 entries
```

---

## ESTIMATED TIMELINE

- **Priority 1-2 (Upload + Backend Fix):** 1-3 hours (depends on test debugging)
- **Priority 3-4 (Proof Logs + REPAIR_REPORT):** 30-60 minutes
- **Priority 5-8 (Cleanup, Validation, Metadata, Hygiene):** 30-45 minutes
- **Final Packaging & Validation:** 15-30 minutes

**Total estimated:** 3-5 hours for complete repair

---

## BLOCKERS REFERENCE

| ID | Priority | Blocker | Impact | Status |
|----|----|---------|--------|--------|
| 1 | 🔴 CRITICAL | Upload source snapshot instead of release archive | Breaks proof chain | Fix packaging process |
| 2 | 🔴 CRITICAL | backend_pytest failed (batch 5) | Fails release gate | Fix failing test |
| 3 | 🔴 CRITICAL | 53 proof logs missing from archive | Archive non-self-verifying | Include logs in packaging |
| 4 | 🟡 REQUIRED | REPAIR_REPORT.md missing | Packaging script fails | Regenerate file |
| 5 | 🟡 CLEANUP | Local paths in stale files | Leaks user environment | Remove/regenerate |
| 6 | 🟡 VALIDATION | required_log_index.json untrustworthy | Can't verify archive | Fix generation logic |
| 7 | 🟡 METADATA | archive_hash is commit hash not SHA-256 | Metadata inconsistent | Rename and fix |
| 8 | 🟡 HYGIENE | .trunk/ in archive | Not release-clean | Add to exclusions |

---

**Document Created:** 2026-05-29  
**Checkpoint:** All 8 blockers documented and actionable  
**Next Step:** Execute Priority 1 (Fix upload process)
