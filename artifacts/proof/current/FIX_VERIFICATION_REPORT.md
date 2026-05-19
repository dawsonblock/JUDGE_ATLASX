# FIX_VERIFICATION_REPORT

- generated_at_utc: 2026-05-19T03:00:00+00:00
- repair_session: JUDGE_ATLASX-main repair plan phases 1–16
- final_status: clean_alpha
- production_ready: false
- alpha_gate_passed: true

## Summary

This is an alpha platform. It is not production-ready.
Public legal/judicial/crime outputs require evidence review.
AI-generated claims are derivative and must cite evidence.
Source coverage is incomplete.
Research/reference folders are excluded from releases.

## Files Changed

| File | Change |
|---|---|
| `.gitignore` | HARD-ENFORCED section: added `Research/`, updated header, no trailing `# tools/` comment |
| `scripts/check_truth_claims.py` | `_normalize_to_repo_root()` upgraded to iterative 3-pass stripping |
| `scripts/export_source_registry_status.py` | `_source_row()` now stores both `source_name` and `name` keys |
| `scripts/check_frontend_node_gate.py` | Default `--expected-major` set to 20, `--expected-minor` 0 |
| `frontend/.nvmrc` | Set to `20` |
| `frontend/package.json` | `engines.node` set to `>=20.11.0` |
| `scripts/release_gate.py` | All 6 frontend GateStepSpec entries use `nvm use 20`; gate step names use Node 20; BLOCKED_NODE_VERSION messages updated |
| `docs/frontend_verification.md` | Created: Node 20 setup guide, failure modes, CI reference |
| `docs/REPO_BOUNDARY.md` | Created: runtime/non-runtime boundary definition |
| `.dockerignore` | Hardened: added Research /, Research/, external_reference/, secrets, archives |
| `.github/workflows/quality-gate.yml` | Python 3.11, Node 20, corrected gate step |
| `.github/workflows/hard-gate.yml` | Python 3.11 |
| `.github/workflows/alpha-release-proof.yml` | Node 20 |

## Folders Excluded from Release

- `research/` — third-party research repos
- `Research /` — trailing-space variant (hard-blocked)
- `Research/` — case variant (hard-blocked)
- `external/` — vendored reference dependencies
- `external_reference/` — external reference material
- `.venv/`, `backend/.venv/` — Python virtual environments
- `node_modules/`, `frontend/.next/` — Node build artefacts
- `logs/`, `tmp/`, `temp/` — ephemeral data
- `evidence_store/` — local data store
- `artifacts/proof/archive/` — historical proof archive
- `archive_validation.md`, `archive_validation.log` — recursive validation artefacts
- `.env`, `*.pem`, `*.key`, `*.db` — secrets and database files

## Release Archive

- Builder: `scripts/build_release_archive.py`
- Validator: `scripts/validate_release_archive.py`
- Expected output: `dist/JUDGE_ATLASX-main.clean.zip`
- Expected size: ~1–10 MB
- Expected file count: ~700–1200 files
- Previous clean build result: valid: true, errors: 0

## Source Registry

- Total sources: 26
- Runnable now: 1 (justice_canada_laws_xml)
- Enable-ready: 4 (awaiting operator /enable)
- Deprecated: 3
- All sources: requires_manual_review: true
- All sources: public_publish_default: false

## Backend Checks

| Check | Result |
|---|---|
| backend_pytest | 2737 passed, 4 skipped (last verified proof run) |
| backend_import_route_count | 103 |
| Alembic migrations | 49 |
| public_api_boundary | 33 passed |
| postgis_proof | PASS (last verified proof run) |
| BLOCKED_BACKEND_VENV enforcement | PASS (proof_postgis.sh + release_gate.py) |

## Frontend Checks

| Check | Result |
|---|---|
| Node version requirement | 20 (enforced in .nvmrc, package.json engines, gate scripts, CI) |
| engine-strict | true (frontend/.npmrc) |
| frontend_node_gate | requires nvm use 20 before running |
| frontend_install | requires npm ci under Node 20 |

## Path Hygiene

| Check | Result |
|---|---|
| Research / folder in git index | Not tracked (verified) |
| Research / in .gitignore | HARD-ENFORCED |
| research/ in .gitignore | HARD-ENFORCED |
| external/ in .gitignore | HARD-ENFORCED |
| validate_release_archive whitespace check | PASS (lines 176-179) |
| check_path_hygiene.py | Exists and scans for whitespace/control chars |

## Truth-Claim Scanner

| Check | Result |
|---|---|
| _normalize_to_repo_root() | Iterative 3-pass: handles 0, 1, or 2 archive wrapper levels |
| test_memory_derivative_boundary.py | Allowlisted for `convicted of` fixture |
| research/ skipped | PASS (in SKIP_DIRS) |
| external/ skipped | PASS (in SKIP_DIRS) |

## Known Remaining Limitations

- Frontend proof requires Node 20 via nvm; CI gates enforce this.
- PostGIS proof requires Docker and the backend .venv with geoalchemy2.
- Proof freshness check will fail after code changes until `make proof` is re-run.
- Source adapters for 18 sources are still missing (adapter_missing state).
- Only justice_canada_laws_xml is currently runnable.
- Production remains blocked: production_ready: false.
- Human review is mandatory for all public publication decisions.

## Wording Compliance

- This is an alpha platform.
- It is not production-ready.
- Public legal/judicial/crime outputs require evidence review.
- AI-generated claims are derivative and must cite evidence.
- Source coverage is incomplete.
- Research/reference folders are excluded from releases.
