<!-- markdownlint-disable -->

# legacy_disabled/us_ingestion_adapters/

US-only data adapters quarantined from the Canada-first production pipeline.

Each file in this directory has a `NOT_RUNTIME: bool = True` sentinel in its original location
(`backend/app/ingestion/` or `backend/app/ingestion/crime_sources/`) and is gated by a
`JTA_ENABLE_*` environment flag.

## Files

| File                | Original Path                                           | Gate Flag                     | Reason                                         |
| ------------------- | ------------------------------------------------------- | ----------------------------- | ---------------------------------------------- |
| `courtlistener.py`  | `backend/app/ingestion/courtlistener.py`                | `JTA_COURTLISTENER_API_TOKEN` | US CourtListener API; no Canadian equivalent   |
| `gdelt.py`          | `backend/app/ingestion/gdelt.py`                        | `JTA_GDELT_ENABLED`           | GDELT global news feed; secondary context only |
| `fbi_crime_data.py` | `backend/app/ingestion/crime_sources/fbi_crime_data.py` | `JTA_FBI_CRIME_ENABLED`       | US FBI crime statistics                        |

## Usage Policy

These adapters **must not** be loaded by:

- `app.ingestion.runner` (automatic scheduler)
- `app.ingestion.source_adapter_factory.ADAPTER_REGISTRY`
- Any background task without an explicit `JTA_ENABLE_*=true` flag

They may be loaded only by:

- Admin-only routes in `backend/app/api/routes/admin_ingest.py` (behind `JTA_ENABLE_ADMIN_IMPORTS`)
- Explicit developer / research scripts in `backend/scripts/` with documented justification

## Promotion Policy

If a Canadian equivalent of any adapter is built, the US version should be:

1. Removed from this directory
2. Replaced with a note pointing to the new Canadian adapter
3. The original `NOT_RUNTIME` sentinel in `backend/app/ingestion/` removed
