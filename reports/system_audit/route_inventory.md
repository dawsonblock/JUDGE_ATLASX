<!-- markdownlint-disable -->

# Route Inventory

Generated: 2026-05-16 | Source: `backend/app/api/routes/` + `backend/app/main.py`

## FastAPI Routers

All routers are mounted via the single `router` aggregator in `backend/app/api/routes/__init__.py`
and registered with `app.include_router(router)` in `backend/app/main.py`.

### Authentication (`backend/app/api/routes/auth.py`)

| Method | Path                 | Auth Required      | Notes                 |
| ------ | -------------------- | ------------------ | --------------------- |
| POST   | `/api/auth/register` | first_admin_secret | Bootstrap first admin |
| POST   | `/api/auth/token`    | credentials        | Login — returns JWT   |
| GET    | `/me`                | JWT                | Current user info     |

### Cases & Defendants (`backend/app/api/routes/map.py` + `map_record.py`)

| Method | Path                                                 | Auth Required  | Notes                |
| ------ | ---------------------------------------------------- | -------------- | -------------------- |
| GET    | `/api/cases`                                         | None           | List cases           |
| GET    | `/api/cases/{case_id}`                               | None           | Case detail          |
| GET    | `/api/cases/{case_id}/timeline`                      | None           | Case events          |
| GET    | `/api/defendants/{defendant_id}`                     | None           | Defendant detail     |
| GET    | `/api/defendants/{defendant_id}/timeline`            | None           | Defendant events     |
| GET    | `/api/events`                                        | None           | Event list           |
| GET    | `/api/events/{event_id}`                             | None           | Event detail         |
| GET    | `/api/judges`                                        | None           | Judge list           |
| GET    | `/api/judges/{judge_id}`                             | None           | Judge detail         |
| GET    | `/api/judges/{judge_id}/events`                      | None           | Judge events         |
| GET    | `/api/map/events`                                    | rate_limit_map | Map-optimised events |
| GET    | `/api/map/crime-aggregates`                          | rate_limit_map | Crime aggregate pins |
| GET    | `/api/map/crime-incidents`                           | rate_limit_map | Crime incident pins  |
| GET    | `/api/map/relationship-arcs`                         | rate_limit_map | Arc overlays         |
| GET    | `/api/map/record/{record_type}/{record_id}`          | None           | Single record popup  |
| GET    | `/api/map/records/{record_type}/{record_id}/quality` | None           | Evidence quality     |

### Sources (`backend/app/api/routes/admin_sources.py`)

| Method | Path                       | Auth Required | Notes              |
| ------ | -------------------------- | ------------- | ------------------ |
| GET    | `/api/sources`             | None          | List all sources   |
| GET    | `/api/sources/{source_id}` | None          | Source detail      |
| GET    | `/{source_key}`            | None          | Source by key      |
| GET    | `/{source_key}/health`     | None          | Health metrics     |
| GET    | `/{source_key}/runs`       | None          | Ingestion run list |
| GET    | `/stats/by-source`         | None          | Per-source stats   |
| GET    | `/stats/daily`             | None          | Daily stats        |

### Ingestion Admin (`backend/app/api/routes/admin_ingest.py` + `admin_ingestion.py`)

| Method | Path                       | Auth Required | Notes                     |
| ------ | -------------------------- | ------------- | ------------------------- |
| GET    | `` (list)                  | admin         | List ingestion runs       |
| GET    | `/{run_id}`                | admin         | Run detail                |
| GET    | `/{run_id}/review-items`   | admin         | Items from run            |
| GET    | `/{run_id}/snapshots`      | admin         | Snapshots from run        |
| POST   | (trigger)                  | admin         | Trigger manual run        |
| GET    | `/courtlistener-bulk/runs` | admin         | CourtListener bulk status |

### Admin Review (`backend/app/api/routes/admin_review.py`)

| Method | Path                                | Auth Required        | Notes          |
| ------ | ----------------------------------- | -------------------- | -------------- |
| GET    | `/api/admin/review/items`           | require_admin_review | Queue          |
| GET    | `/api/admin/review/items/{item_id}` | require_admin_review | Item detail    |
| PATCH  | `/api/admin/review/items/{item_id}` | require_admin_review | Approve/reject |

### Evidence (`backend/app/api/routes/evidence.py` + `evidence_store.py`)

| Method | Path                                                   | Auth Required | Notes          |
| ------ | ------------------------------------------------------ | ------------- | -------------- |
| GET    | `/api/evidence/source-panel/{entity_type}/{entity_id}` | None          | Evidence panel |

### Snapshots (`backend/app/api/routes/snapshots.py`)

| Method | Path                      | Auth Required | Notes                |
| ------ | ------------------------- | ------------- | -------------------- |
| GET    | `/verify/{snapshot_id}`   | None          | Verify hash          |
| GET    | `/by-hash/{content_hash}` | None          | Lookup by hash       |
| GET    | `/unverified`             | None          | Unverified snapshots |
| GET    | `/{snapshot_id}`          | None          | Snapshot detail      |
| GET    | `/{snapshot_id}/linked`   | None          | Linked data          |
| GET    | `/{snapshot_id}/raw`      | None          | Raw content          |

### Graph (`backend/app/api/routes/graph.py`)

| Method | Path                                                    | Auth Required | Notes               |
| ------ | ------------------------------------------------------- | ------------- | ------------------- |
| GET    | `/entity/{entity_type}/{entity_id}`                     | None          | Entity node         |
| GET    | `/entity/{entity_type}/{entity_id}/edges`               | None          | Entity edges        |
| GET    | `/entity/{entity_type}/{entity_id}/related`             | None          | Related entities    |
| GET    | `/relationship/{from_type}/{from_id}/{to_type}/{to_id}` | None          | Relationship detail |

### Memory Admin (`backend/app/api/routes/admin_memory.py`)

| Method | Path                        | Auth Required | Notes               |
| ------ | --------------------------- | ------------- | ------------------- |
| GET    | `/claims`                   | admin         | Memory claims       |
| GET    | `/entity/{entity_id}/state` | admin         | Entity memory state |
| GET    | `/path`                     | admin         | Memory path query   |

### AI Routes (`backend/app/api/routes/ai_review.py` + `ai_correctness.py` + `chat.py`)

| Method | Path             | Auth Required | Notes                      |
| ------ | ---------------- | ------------- | -------------------------- |
| GET    | `/status`        | None          | AI subsystem status        |
| GET    | `/search/by-url` | None          | Lookup by source URL       |
| POST   | (chat endpoint)  | None          | AI chat (NOT_RUNTIME gate) |

### Public Events (`backend/app/api/routes/public_events.py`)

| Method | Path         | Auth Required                 | Notes               |
| ------ | ------------ | ----------------------------- | ------------------- |
| GET    | `/health`    | None                          | Health check        |
| POST   | (event post) | enable_public_event_post gate | Ingest public event |

### Quarantine (`backend/app/api/routes/admin_quarantine.py`)

| Method | Path | Auth Required | Notes            |
| ------ | ---- | ------------- | ---------------- |
| GET    | ``   | admin         | Quarantined runs |

### Boundaries (`backend/app/api/routes/boundaries.py`)

| Method | Path          | Auth Required | Notes                 |
| ------ | ------------- | ------------- | --------------------- |
| GET    | `/boundaries` | None          | Geographic boundaries |

---

## Next.js App Routes (`frontend/app/`)

| Route           | File                            | Status        | Notes                         |
| --------------- | ------------------------------- | ------------- | ----------------------------- |
| `/`             | `app/page.tsx`                  | Active        | Landing / redirect            |
| `/map`          | `app/map/page.tsx`              | Redirect stub | → `/map-v2` (Sprint G target) |
| `/map-v2`       | `app/map-v2/MapV2Workspace.tsx` | Active        | Primary map workspace         |
| `/sources`      | `app/sources/page.tsx`          | Active        | Source registry page          |
| `/records/[id]` | (not yet created)               | Missing       | Sprint G target               |
| `/admin/*`      | `app/admin/`                    | Partial       | Admin review UI               |

---

## Missing Endpoints (planned)

| Method | Path                       | Sprint   | Notes                        |
| ------ | -------------------------- | -------- | ---------------------------- |
| GET    | `/api/v1/sources/coverage` | Sprint I | Per-source ingestion status  |
| GET    | `/api/v1/status/ingestion` | Sprint I | System-wide ingestion health |
