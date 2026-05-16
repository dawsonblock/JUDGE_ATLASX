<!-- markdownlint-disable -->

# Duplicate and Near-Duplicate Modules

Generated: 2026-05-16 | Source: codebase exploration

## 1. SCC Source Duplication

### Problem

The source registry YAML (`canada_saskatchewan_sources.yaml`) contains two SCC entries:

- `scc_judgments` — lifecycle_state: `deprecated`
- `scc_decisions` (or `scc_lexum_api`) — active entry

The adapter file is `backend/app/ingestion/source_adapters/scc_lexum_api.py`, which maps to the active entry. The deprecated `scc_judgments` source is never fetched by the adapter registry but remains in the YAML and in the DB after first seed.

**Resolution**: Sprint C — confirm `scc_judgments` has `automation_status: deprecated` and add `lifecycle_state: archived`.

---

## 2. Federal Court Canada Duplication

### Problem

Two YAML entries both reference Federal Court:

- `federal_court_canada_decisions` — lifecycle_state: `deprecated`
- `federal_court_canada` — active

Adapter file: `backend/app/ingestion/source_adapters/federal_court_html.py` (appears twice in YAML adapter listings per earlier audit).

**Resolution**: Sprint C — archive the deprecated entry; ensure adapter maps only to `federal_court_canada`.

---

## 3. `SourceAdapter` vs `CanadianSourceAdapter`

### Problem

Two abstract base classes coexist in `backend/app/ingestion/adapters.py`:

- `SourceAdapter` (line 131) — legacy ABC from original architecture
- `CanadianSourceAdapter` (line ~175) — production ABC; all 14 concrete adapters inherit from this

`SourceAdapter` is only inherited by two placeholder classes (`CourtOpinionRSSAdapter`, `NewsAdapter`) that return empty lists and have no production callers.

**Resolution**: Sprint D — add `BaseSourceAdapter = CanadianSourceAdapter` alias; Sprint B — add `@deprecated` docstrings to `SourceAdapter`/`CourtOpinionRSSAdapter`/`NewsAdapter`.

---

## 4. Admin Ingestion Route Duplication

### Problem

Two route files appear to cover overlapping admin ingestion functionality:

- `backend/app/api/routes/admin_ingest.py`
- `backend/app/api/routes/admin_ingestion.py`

Both are imported by the route aggregator. If they define routes at the same prefix without distinct tags, they produce duplicate OpenAPI operations.

**Resolution (post-v1)**: Audit both files for overlapping route paths; consolidate or give distinct prefixes with distinct OpenAPI tags.

---

## 5. Evidence Routes Duplication

### Problem

Two route files cover evidence:

- `backend/app/api/routes/evidence.py`
- `backend/app/api/routes/evidence_store.py`

These may be intentionally split (entity evidence panel vs. raw snapshot store), but should be verified to not overlap.

**Resolution**: Verify prefix tags during Sprint E evidence work; document the split in API docs.

---

## 6. Map Route Duplication

### Problem

Two map route files:

- `backend/app/api/routes/map.py`
- `backend/app/api/routes/map_record.py`

`map.py` likely handles aggregate/collection endpoints; `map_record.py` handles single record popups. Split is likely intentional but should be documented.

**Resolution**: Document intentional split in route_inventory.md (done).

---

## 7. `fetch_for_ingestion` vs direct `httpx` usage

### Problem

`backend/app/ingestion/http_client.py` (or equivalent) defines `fetch_for_ingestion()` as the safe, rate-limited HTTP fetcher for adapters. However, `courtlistener.py` uses direct `httpx` — documented in its module docstring as a known migration gap.

All 14 `source_adapters/` files should use `fetch_for_ingestion()` only.

**Resolution**: Verify each of the 14 adapters in `source_adapters/` uses `fetch_for_ingestion()` (not raw `httpx`). Track violations as issues.
