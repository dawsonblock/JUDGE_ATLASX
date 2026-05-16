<!-- markdownlint-disable -->

# Runtime Dependency Graph

Generated: 2026-05-16 | Source: codebase exploration

## Request Lifecycle (FastAPI)

```
HTTP Request
  └── FastAPI (backend/app/main.py)
        ├── CORSMiddleware  (JTA_CORS_ORIGINS)
        ├── BaseHTTPMiddleware (max_request_size enforcement)
        ├── JWT validation middleware  (require_jwt / require_admin_review)
        ├── Rate-limit middleware  (slowapi, backend: memory | redis)
        └── Router dispatch (app/api/routes/__init__.py)
              ├── auth.py
              │     └── app.services.auth  →  app.models.user  →  DB
              ├── map.py / map_record.py
              │     └── app.services.map_service  →  app.models.*  →  DB + PostGIS
              ├── evidence.py / evidence_store.py
              │     └── app.services.evidence_integrity  →  SHA256 snapshots  →  DB
              ├── snapshots.py
              │     └── app.models.snapshot  →  DB
              ├── admin_review.py
              │     └── app.services.review_service  →  app.models.review_item  →  DB
              ├── admin_ingest.py / admin_ingestion.py
              │     └── app.ingestion.runner  →  ADAPTER_REGISTRY  →  External APIs
              ├── admin_sources.py
              │     └── app.models.source_registry  →  DB
              ├── graph.py
              │     └── app.services.graph_service  →  app.models.relationship  →  DB
              ├── admin_memory.py
              │     └── app.services.memory_service  →  DB
              ├── boundaries.py
              │     └── app.models.boundary  →  DB + PostGIS
              └── chat.py / ai_review.py / ai_correctness.py
                    └── AI gate (JTA_OLLAMA_ENABLED / NOT_RUNTIME sentinel)
```

## Service Layer Dependencies

```
app.services.evidence_integrity
  ├── app.models.snapshot (Snapshot, SnapshotContent)
  ├── hashlib.sha256
  └── IMMUTABLE_SNAPSHOT_FIELDS constant

app.services.review_service
  ├── app.models.review_item (ReviewItem)
  ├── app.policies.publication_policy (can_publish_entity, PUBLIC_REVIEW_STATUSES)
  └── DB session

app.services.map_service
  ├── app.models.entities (Judge, Case, Defendant, Event, CrimeAggregate, CrimeIncident)
  ├── app.models.source_registry (SourceRegistry)
  ├── app.policies.publication_policy (can_show_public_entity)
  └── PostGIS ST_* spatial queries

app.ingestion.runner
  ├── app.ingestion.source_adapter_factory (build_adapter, ADAPTER_REGISTRY)
  ├── app.ingestion.adapters (IngestionResult, ParsedRecord, CreatedRecord)
  ├── app.models.ingestion_run (IngestionRun, IngestionRunStatus)
  ├── app.models.review_item (ReviewItem) — creates review gate items
  ├── app.services.evidence_integrity — snapshot all records
  └── app.db.session

app.seed.source_registry
  ├── backend/app/ingestion/sources/canada_saskatchewan_sources.yaml
  ├── app.models.source_registry (SourceRegistry)
  └── validate_machine_ingest_source_spec() — contract enforcement
```

## Database Session Flow

```
backend/app/db/session.py
  ├── engine  (DATABASE_URL from JTA_DATABASE_URL)
  ├── SessionLocal  (per-request session via Depends(get_db))
  └── initialize_postgis()  — creates PostGIS extension if missing
```

## Startup Sequence

```
1. _validate_cors_origins()    — exits(1) on wildcard in production
2. _is_placeholder_secret()    — exits(1) on weak JWT secret in production
3. initialize_postgis()        — CREATE EXTENSION IF NOT EXISTS postgis
4. seed_source_registry()      — idempotent YAML → DB sync (if JTA_SEED_SOURCE_REGISTRY=true)
5. seed_sample_data()          — dev fixtures only (if JTA_AUTO_SEED=true)
6. APScheduler start           — if JTA_ENABLE_SCHEDULER=true
```
