<!-- markdownlint-disable -->

# Environment Variable Reference

Generated: 2026-05-16 | Source: `backend/app/core/config.py` (env*prefix=`JTA*`)

All variables use the prefix `JTA_`. Values in `.env` file override defaults.

## Core Application

| Variable           | Type | Default                       | Required in Prod          | Notes                                         |
| ------------------ | ---- | ----------------------------- | ------------------------- | --------------------------------------------- |
| `JTA_APP_NAME`     | str  | `JudgeTracker Atlas`          | No                        | Display name only                             |
| `JTA_APP_ENV`      | str  | `development`                 | Yes — set to `production` | Controls startup guard behaviour              |
| `JTA_DATABASE_URL` | str  | `sqlite:///./judgetracker.db` | Yes — PostgreSQL URL      | Must be PostgreSQL + PostGIS in prod          |
| `JTA_CORS_ORIGINS` | str  | `https://localhost:3000`      | Yes                       | Comma-separated; wildcard `*` blocked in prod |

## Authentication & Security

| Variable                              | Type | Default                       | Required in Prod   | Notes                                       |
| ------------------------------------- | ---- | ----------------------------- | ------------------ | ------------------------------------------- |
| `JTA_JWT_SECRET_KEY`                  | str  | `CHANGE-ME-BEFORE-PRODUCTION` | Yes                | Startup exits(1) if placeholder in prod     |
| `JTA_JWT_ALGORITHM`                   | str  | `HS256`                       | No                 |                                             |
| `JTA_JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | int  | `30`                          | No                 |                                             |
| `JTA_JWT_REFRESH_TOKEN_EXPIRE_DAYS`   | int  | `7`                           | No                 |                                             |
| `JTA_JWT_AUTH_ENABLED`                | bool | `False`                       | Yes — set `True`   | Admin/mutation routes require JWT when True |
| `JTA_FIRST_ADMIN_SECRET`              | str  | None                          | Yes (first deploy) | Bootstraps first admin user                 |
| `JTA_ADMIN_TOKEN`                     | str  | None                          | No                 | Legacy shared token — see deprecation note  |
| `JTA_ADMIN_REVIEW_TOKEN`              | str  | None                          | Conditional        | Required if `JTA_ENABLE_ADMIN_REVIEW=true`  |
| `JTA_ENABLE_LEGACY_ADMIN_TOKEN`       | bool | `False`                       | No — must be False | **DEPRECATED.** Never enable in production  |
| `JTA_ENFORCE_JWT_MUTATIONS`           | bool | `True`                        | Recommended True   | Rejects shared-token actors for mutations   |

## Feature Gates

| Variable                              | Type | Default | Required in Prod       | Notes                                         |
| ------------------------------------- | ---- | ------- | ---------------------- | --------------------------------------------- |
| `JTA_ENABLE_ADMIN_IMPORTS`            | bool | `False` | No                     | Gates GDELT/CourtListener admin import routes |
| `JTA_ENABLE_ADMIN_REVIEW`             | bool | `False` | Conditional            | Gates review queue endpoints                  |
| `JTA_ENABLE_PUBLIC_EVENT_POST`        | bool | `False` | No                     | Allows public POST of events                  |
| `JTA_ENABLE_SCHEDULER`                | bool | `False` | No                     | APScheduler background ingestion              |
| `JTA_ENABLE_PUBLIC_RELATIONSHIP_ARCS` | bool | `False` | No                     | Requires policy sign-off before enabling      |
| `JTA_AUTO_SEED`                       | bool | `False` | No — set False in prod | Dev fixtures only                             |
| `JTA_SEED_SOURCE_REGISTRY`            | bool | `True`  | Yes                    | YAML → DB source sync at startup              |

## Rate Limiting

| Variable                   | Type | Default  | Required in Prod | Notes                                                     |
| -------------------------- | ---- | -------- | ---------------- | --------------------------------------------------------- |
| `JTA_RATE_LIMIT_ENABLED`   | bool | `True`   | Yes              |                                                           |
| `JTA_RATE_LIMIT_BACKEND`   | str  | `memory` | Conditional      | `memory` or `redis`; if `redis`, `JTA_REDIS_URL` required |
| `JTA_RATE_LIMIT_PUBLIC`    | int  | `100`    | No               | Requests/minute for public endpoints                      |
| `JTA_RATE_LIMIT_ADMIN`     | int  | `30`     | No               | Requests/minute for admin endpoints                       |
| `JTA_RATE_LIMIT_MAP`       | int  | `60`     | No               | Requests/minute for map endpoints                         |
| `JTA_RATE_LIMIT_INGESTION` | int  | `10`     | No               | Requests/minute for ingestion endpoints                   |
| `JTA_REDIS_URL`            | str  | None     | Conditional      | Required if `JTA_RATE_LIMIT_BACKEND=redis`                |
| `JTA_TRUSTED_PROXY_IPS`    | str  | `""`     | Conditional      | Comma-separated; set if behind a proxy                    |

## Evidence Store

| Variable                         | Type | Default | Required in Prod | Notes                                 |
| -------------------------------- | ---- | ------- | ---------------- | ------------------------------------- |
| `JTA_EVIDENCE_STORE_ROOT`        | str  | None    | Recommended      | Directory for SHA256 snapshot blobs   |
| `JTA_EVIDENCE_STORE_REQUIRED`    | bool | `False` | Recommended True | Startup exits if store not reachable  |
| `JTA_EVIDENCE_STORE_PROBE_WRITE` | bool | `True`  | No               | Verifies store is writable at startup |

## External Data Sources

| Variable                  | Type | Default | Required in Prod | Notes                            |
| ------------------------- | ---- | ------- | ---------------- | -------------------------------- |
| `JTA_CANLII_API_KEY`      | str  | None    | Conditional      | Required for CanLII adapter      |
| `JTA_LEXUM_API_KEY`       | str  | None    | Conditional      | Required for SCC Lexum adapter   |
| `JTA_LAWS_XML_TARGET_IDS` | str  | `C-46`  | No               | Comma-sep Justice Canada XML IDs |
| `JTA_STATSCAN_ENABLED`    | bool | `False` | No               |                                  |
| `JTA_LOCAL_FEEDS_ENABLED` | bool | `False` | No               |                                  |
| `JTA_GEONAMES_USERNAME`   | str  | None    | Conditional      |                                  |

## Legacy / US Sources (should remain disabled in production)

| Variable                      | Type | Default | Notes                          |
| ----------------------------- | ---- | ------- | ------------------------------ |
| `JTA_FBI_CRIME_ENABLED`       | bool | `False` | US FBI data — NOT_RUNTIME      |
| `JTA_GDELT_ENABLED`           | bool | `False` | GDELT news — NOT_RUNTIME       |
| `JTA_COURTLISTENER_API_TOKEN` | str  | None    | CourtListener US — NOT_RUNTIME |

## AI / Semantic Features (disabled by default)

| Variable                 | Type | Default                  | Notes                         |
| ------------------------ | ---- | ------------------------ | ----------------------------- |
| `JTA_OLLAMA_ENABLED`     | bool | `False`                  | Local AI inference            |
| `JTA_OLLAMA_BASE_URL`    | str  | `http://localhost:11434` |                               |
| `JTA_OLLAMA_MODEL`       | str  | `mistral`                |                               |
| `JTA_EMBEDDINGS_ENABLED` | bool | `False`                  | sentence-transformers (heavy) |
| `JTA_EMBEDDINGS_MODEL`   | str  | `all-MiniLM-L6-v2`       |                               |

## Request Size Limits

| Variable                  | Type | Default            | Notes              |
| ------------------------- | ---- | ------------------ | ------------------ |
| `JTA_MAX_REQUEST_SIZE`    | int  | `10485760` (10 MB) | General API        |
| `JTA_MAX_CSV_UPLOAD_SIZE` | int  | `52428800` (50 MB) | CSV ingestion      |
| `JTA_MAX_CSV_ROWS`        | int  | `1000000`          | Hard row-count cap |

---

## Production Minimum Set

The following variables **must** be set before production deployment:

```bash
JTA_APP_ENV=production
JTA_DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/judgetracker
JTA_JWT_SECRET_KEY=<256-bit random>
JTA_JWT_AUTH_ENABLED=true
JTA_CORS_ORIGINS=https://yourdomain.com
JTA_SEED_SOURCE_REGISTRY=true
JTA_ENABLE_LEGACY_ADMIN_TOKEN=false
JTA_EVIDENCE_STORE_ROOT=/data/evidence
JTA_EVIDENCE_STORE_REQUIRED=true
```
