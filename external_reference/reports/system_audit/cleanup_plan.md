<!-- markdownlint-disable -->

# Cleanup Plan

Generated: 2026-05-16 | Prioritized from audit findings

## Priority 1 — Safety / Correctness (Sprint B)

| #   | Action                                                                                    | File(s)                                                 | Risk if Skipped                                               |
| --- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------- |
| 1.1 | Add `NOT_RUNTIME: bool = True` sentinel to `fbi_crime_data.py`                            | `backend/app/ingestion/crime_sources/fbi_crime_data.py` | US-only adapter may load unconditionally                      |
| 1.2 | Add `# LEGACY: NOT_RUNTIME` header block to courtlistener.py, gdelt.py, fbi_crime_data.py | Same 3 files                                            | Runtime confusion about intent                                |
| 1.3 | Copy all 3 legacy files to `legacy_disabled/us_ingestion_adapters/`                       | `legacy_disabled/` (new dir)                            | Historical context lost when originals are eventually removed |
| 1.4 | Set `JTA_ENABLE_LEGACY_ADMIN_TOKEN=false` in docker-compose.yml                           | `docker-compose.yml`                                    | Staging deploys accidentally enable deprecated auth           |

## Priority 2 — Data Integrity (Sprint C)

| #   | Action                                                                                    | File(s)                               | Risk if Skipped                                        |
| --- | ----------------------------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------ |
| 2.1 | Add 7 spec-required fields to all 26 YAML source entries                                  | `canada_saskatchewan_sources.yaml`    | Source registry lacks provenance metadata              |
| 2.2 | Set `automation_status: deprecated` on `scc_judgments` + `federal_court_canada_decisions` | Same YAML                             | Deprecated entries may be picked up by adapter factory |
| 2.3 | Update `validate_machine_ingest_source_spec()` to enforce new fields                      | `backend/app/seed/source_registry.py` | New fields silently skipped on seed                    |

## Priority 3 — API Contracts (Sprint D + E + F)

| #   | Action                                                                                      | File(s)                                         | Risk if Skipped                                    |
| --- | ------------------------------------------------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------- |
| 3.1 | Add `healthcheck()`, `snapshot()`, `normalize()` default methods to `CanadianSourceAdapter` | `backend/app/ingestion/adapters.py`             | Adapters lack standard interface                   |
| 3.2 | Add `detect_orphaned_snapshots()` + `get_evidence_chain()` to `evidence_integrity.py`       | `backend/app/services/evidence_integrity.py`    | No way to find evidence leaks                      |
| 3.3 | Create `IngestionState` enum + `ingestion_state_for_review_status()`                        | `backend/app/policies/ingestion_state.py` (new) | Review status → ingestion status mapping is ad-hoc |

## Priority 4 — Configuration Safety (Sprint H)

| #   | Action                                                           | File(s)                          | Risk if Skipped                             |
| --- | ---------------------------------------------------------------- | -------------------------------- | ------------------------------------------- |
| 4.1 | Startup warn if `jwt_auth_enabled=False` in production           | `backend/app/main.py`            | Silent unauthenticated admin access         |
| 4.2 | Startup error if `rate_limit_backend=redis` and `redis_url=None` | `backend/app/main.py`            | Runtime crash on first rate-limited request |
| 4.3 | Startup warn if `evidence_store_root=None` in production         | `backend/app/main.py`            | Evidence snapshots silently dropped         |
| 4.4 | Create `.env.production.example`                                 | `.env.production.example` (new)  | No canonical production config reference    |
| 4.5 | Create `docs/config_reference.md`                                | `docs/config_reference.md` (new) | Admin flags undocumented                    |

## Priority 5 — Frontend / UI (Sprint G)

| #   | Action                                                                 | File(s)                     | Risk if Skipped                      |
| --- | ---------------------------------------------------------------------- | --------------------------- | ------------------------------------ |
| 5.1 | ✅ Completed: moved to canonical `MapWorkspace.tsx` under `/map/`      | `frontend/app/map/`         | Confusing `map-v2` URL in production |
| 5.2 | ✅ Completed: `/map/page.tsx` now renders canonical workspace directly | `frontend/app/map/page.tsx` | Double redirect                      |
| 5.3 | Create `frontend/app/records/[id]/page.tsx`                            | New file                    | No public record detail page         |

## Priority 6 — New Endpoints (Sprint I)

| #   | Action                                      | File(s)                         | Risk if Skipped                       |
| --- | ------------------------------------------- | ------------------------------- | ------------------------------------- |
| 6.1 | Add `GET /api/v1/sources/coverage` endpoint | New route in `admin_sources.py` | No programmatic source health summary |
| 6.2 | Add `GET /api/v1/status/ingestion` endpoint | New route                       | No system-wide ingestion health       |

## Priority 7 — Release (Sprint J)

| #   | Action                         | File(s)    | Risk if Skipped                  |
| --- | ------------------------------ | ---------- | -------------------------------- |
| 7.1 | Add `make release-zip` target  | `Makefile` | No reproducible release artifact |
| 7.2 | Run `make verify`              | CI         | Accumulated lint/test drift      |
| 7.3 | Create final validation report | `reports/` | No documented release gate       |

## Post-v1 (Not Blocking)

| #   | Action                                                              | Notes                                 |
| --- | ------------------------------------------------------------------- | ------------------------------------- |
| P.1 | Collapse `admin_ingest.py` + `admin_ingestion.py`                   | Overlapping route files               |
| P.2 | Remove `courtlistener_bulk_*` config fields from `config.py`        | Dead config for a quarantined adapter |
| P.3 | Audit all 14 source_adapters for `fetch_for_ingestion()` compliance | Should not use raw `httpx`            |
| P.4 | Consolidate `evidence.py` + `evidence_store.py` if routes overlap   | Verify prefix split                   |
