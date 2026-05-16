<!-- markdownlint-disable -->

# Dead Code Candidates

Generated: 2026-05-16 | Source: codebase exploration

## 1. Legacy US Adapters (Sprint B quarantine targets)

| File                | Path                                   | Reason                               | Status                                           |
| ------------------- | -------------------------------------- | ------------------------------------ | ------------------------------------------------ |
| `courtlistener.py`  | `backend/app/ingestion/`               | US-only, NOT_RUNTIME sentinel set    | Copy to `legacy_disabled/us_ingestion_adapters/` |
| `gdelt.py`          | `backend/app/ingestion/`               | NOT_RUNTIME sentinel set             | Copy to `legacy_disabled/us_ingestion_adapters/` |
| `fbi_crime_data.py` | `backend/app/ingestion/crime_sources/` | US FBI data, no NOT_RUNTIME sentinel | Add sentinel + copy                              |

## 2. Deprecated YAML Source Entries

| source_key                       | File                               | lifecycle_state | Action                                                            |
| -------------------------------- | ---------------------------------- | --------------- | ----------------------------------------------------------------- |
| `scc_judgments`                  | `canada_saskatchewan_sources.yaml` | `deprecated`    | Confirm `automation_status: deprecated`; move to archived section |
| `federal_court_canada_decisions` | `canada_saskatchewan_sources.yaml` | `deprecated`    | Confirm `automation_status: deprecated`; move to archived section |

## 3. Legacy Adapter ABC Hierarchy

| Class                    | File                                    | Status             | Reason                                                                                                     |
| ------------------------ | --------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------- |
| `SourceAdapter`          | `backend/app/ingestion/adapters.py:131` | Legacy placeholder | All real adapters now use `CanadianSourceAdapter`; only `CourtOpinionRSSAdapter` and `NewsAdapter` inherit |
| `CourtOpinionRSSAdapter` | `backend/app/ingestion/adapters.py:149` | Placeholder        | Returns empty lists; no concrete implementation wires into it                                              |
| `NewsAdapter`            | `backend/app/ingestion/adapters.py:159` | Placeholder        | Returns empty lists; news ingested via `crawlee_gov_news` / `crawlee_police_release` instead               |

## 4. AI / Semantic Stubs (NOT_IMPLEMENTED)

| Component           | Location                                            | Status                                                  |
| ------------------- | --------------------------------------------------- | ------------------------------------------------------- |
| `chat.py`           | `backend/app/api/routes/chat.py`                    | AI chat behind Ollama gate; never enabled in production |
| `ai_review.py`      | `backend/app/api/routes/ai_review.py`               | AI review gate; no persistent store wired               |
| `ai_correctness.py` | `backend/app/api/routes/ai_correctness.py`          | AI correctness scoring; stub                            |
| Embeddings support  | `backend/app/core/config.py` (`embeddings_enabled`) | Disabled by default; no production usage                |

## 5. Admin Memory Routes (partial stub)

| Component         | Location                                 | Status                                             |
| ----------------- | ---------------------------------------- | -------------------------------------------------- |
| `admin_memory.py` | `backend/app/api/routes/admin_memory.py` | Memory routes wired but memory service may be stub |

## 6. CourtListener Bulk Import

| Component                            | Location                                 | Status                                                                   |
| ------------------------------------ | ---------------------------------------- | ------------------------------------------------------------------------ |
| `courtlistener.py` (bulk)            | `backend/app/ingestion/courtlistener.py` | Large US-court bulk import; NOT_RUNTIME sentinel; no Canadian equivalent |
| `courtlistener_bulk_*` config fields | `backend/app/core/config.py`             | 5 config fields for a NOT_RUNTIME adapter                                |

## 7. Obsolete Route Files (audit flag — verify before removing)

| File                                      | Notes                                                  |
| ----------------------------------------- | ------------------------------------------------------ |
| `admin_ingest.py` vs `admin_ingestion.py` | Two files with overlapping purpose — may be duplicates |

---

## Recommended Actions

1. **Sprint B**: Copy + add NOT_RUNTIME to `fbi_crime_data.py`; add `# LEGACY` headers to all 3 in `legacy_disabled/us_ingestion_adapters/`
2. **Sprint B**: Add `@deprecated` docstrings to `SourceAdapter`, `CourtOpinionRSSAdapter`, `NewsAdapter`
3. **Sprint C**: Set `automation_status: deprecated` on 2 YAML entries above
4. **Post-v1**: Collapse `admin_ingest.py` + `admin_ingestion.py` if truly duplicate after confirming router mounts
5. **Post-v1**: Remove `courtlistener_bulk_*` config fields once CourtListener is fully quarantined
