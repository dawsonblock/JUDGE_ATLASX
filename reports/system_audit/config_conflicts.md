<!-- markdownlint-disable -->

# Configuration Conflicts and Naming Mismatches

Generated: 2026-05-16 | Source: codebase exploration

## 1. `automation_status` Naming Mismatch

### Problem

The YAML spec in `canada_saskatchewan_sources.yaml` uses `automation_status` to describe whether a source is automatically ingested. However, the `lifecycle_state` field tracks active/deprecated state, and there is inconsistency between entries that use:

- `automation_status: runnable`
- `automation_status: portal_reference`
- `automation_status: disabled_stub`
- `lifecycle_state: deprecated` (some deprecated entries lack a corresponding `automation_status: deprecated`)

### Impact

`validate_machine_ingest_source_spec()` in `backend/app/seed/source_registry.py` may not enforce that deprecated lifecycle entries also carry `automation_status: deprecated`.

### Resolution (Sprint C)

- Ensure all `lifecycle_state: deprecated` entries also have `automation_status: deprecated`
- Add validation rule to `validate_machine_ingest_source_spec()`

---

## 2. `JTA_ENABLE_LEGACY_ADMIN_TOKEN` in docker-compose

### Problem

`docker-compose.yml` sets `JTA_ENABLE_LEGACY_ADMIN_TOKEN=true` (or equivalent legacy admin env var). This flag is explicitly documented as:

> DEPRECATED — disabled by default. Set to True only for local development. Never enable in production.

Leaving it in `docker-compose.yml` means a `docker-compose up` in staging or CI accidentally enables the deprecated auth path.

### Resolution (Sprint H)

- Remove or set to `false` in `docker-compose.yml`
- Add a comment referencing the deprecation notice in `config.py`
- Verify startup emits a `WARNING` when `enable_legacy_admin_token=true`

---

## 3. `JTA_JWT_AUTH_ENABLED` Default Is False

### Problem

`jwt_auth_enabled: bool = False` means the API ships with JWT auth disabled by default. Routes that check `require_jwt` may silently allow unauthenticated requests if the flag is not set to `true`.

### Impact

Any deployment that forgets to set `JTA_JWT_AUTH_ENABLED=true` exposes admin/review routes to unauthenticated callers.

### Resolution (Sprint H)

- Verify `require_jwt` middleware correctly rejects requests when `jwt_auth_enabled=False` vs. permitting them
- Add a startup `WARNING` if `app_env == "production"` and `jwt_auth_enabled == False`

---

## 4. YAML Field Name Mismatches vs. DB Model

### Problem

Several YAML fields do not have a 1:1 mapping to `SourceRegistry` model columns:

- YAML `rate_limit_policy` → no DB column yet
- YAML `confidence_class` → no DB column yet
- YAML `evidence_required` → no DB column yet
- YAML `terms_verified` → no DB column yet

These fields exist in the planned spec (see Sprint C) but are not yet in the schema.

### Resolution (Sprint C)

- Add fields to `canada_saskatchewan_sources.yaml` for all 26 entries
- Add corresponding columns to `SourceRegistry` model (or store as JSONB metadata)
- Update `validate_machine_ingest_source_spec()` to check all 7 new fields

---

## 5. `enable_admin_imports` vs. `enable_admin_review` vs. `require_admin_review`

### Problem

Three similar-sounding config flags with different scopes:

- `JTA_ENABLE_ADMIN_IMPORTS` — gates GDELT/CourtListener import routes
- `JTA_ENABLE_ADMIN_REVIEW` — gates the review queue UI endpoints
- `require_admin_review` — FastAPI dependency that checks the per-route token

The naming is confusing: `require_admin_review` is a function, not a config field, but it reads `admin_review_token`, not `enable_admin_review`.

### Resolution (Sprint H)

- Document the three flags in `docs/config_reference.md`
- Add a comment to `config.py` cross-referencing them

---

## 6. `rate_limit_backend` vs. `redis_url` Dependency Not Validated at Startup

### Problem

Setting `JTA_RATE_LIMIT_BACKEND=redis` without also setting `JTA_REDIS_URL` will cause a runtime crash when the first rate-limited request arrives, not at startup.

### Resolution (Sprint H)

- Add startup validation: if `rate_limit_backend == "redis"` and `redis_url is None`, log ERROR and either exit(1) or fall back to memory backend with a warning.

---

## 7. `evidence_store_root` Not Validated Unless `evidence_store_required=True`

### Problem

`JTA_EVIDENCE_STORE_ROOT` is silently ignored if not set and `JTA_EVIDENCE_STORE_REQUIRED=False`. This means evidence snapshots may be dropped silently in environments where the store path was forgotten.

### Resolution (Sprint H)

- Add startup `WARNING` if `evidence_store_root` is None and `app_env == "production"`
- Document expected production value in `.env.production.example`
