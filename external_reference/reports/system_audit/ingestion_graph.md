<!-- markdownlint-disable -->

# Ingestion Pipeline Graph

Generated: 2026-05-16 | Source: codebase exploration

## Full Pipeline

```
canada_saskatchewan_sources.yaml
  │
  ├── seed_source_registry()  →  SourceRegistry table (DB)
  │
  └── build_adapter(source_key, settings)
        └── source_adapter_factory.py
              ├── ADAPTER_REGISTRY  (from source_adapters/__init__.py)
              │     ├── laws_justice_xml      → LawsJusticeXmlAdapter
              │     ├── canlii_api            → CanLIIApiAdapter
              │     ├── federal_court_html    → FederalCourtHtmlAdapter
              │     ├── scc_lexum_api         → SccLexumApiAdapter
              │     ├── ckan_api              → CkanApiAdapter
              │     ├── crawlee_gov_news      → CrawleeGovNewsAdapter
              │     ├── crawlee_police_release→ CrawleePoliceReleaseAdapter
              │     ├── saskatoon_csv         → SaskatoonCsvAdapter
              │     ├── saskatoon_police_csv  → SaskatoonPoliceCsvAdapter
              │     ├── sk_courts_html        → SkCourtsHtmlAdapter
              │     ├── sk_legislature_html   → SkLegislatureHtmlAdapter
              │     └── statscan_table        → StatscanTableAdapter
              │
              └── adapter.run()
                    ├── adapter.fetch()       →  HTTP / file / API call
                    ├── adapter.validate_record_contract()  →  ContractViolationError
                    ├── adapter.parse()       →  ParsedRecord
                    └── persistence layer
                          ├── ReviewItem created (if requires_manual_review=true)
                          ├── evidence snapshot  →  evidence_integrity.py (SHA256)
                          └── IngestionResult(records_created, errors, run_id)
```

## Adapter Contract (CanadianSourceAdapter)

```python
class CanadianSourceAdapter(ABC):
    source_key: str                   # must match YAML source_key
    def fetch(self) -> list[RawRecord]
    def parse(self, raw: RawRecord) -> ParsedRecord
    def validate_record_contract(self, record: ParsedRecord) -> None  # raises ContractViolationError
    def run(self, db, settings, run_id) -> IngestionResult
```

## Data Contracts

```
RawRecord
  ├── payload: dict
  ├── source_url: str
  └── fetched_at: datetime

ParsedRecord
  ├── source_name: str
  ├── source_quality: str  (primary | secondary_context | aggregate)
  ├── raw: dict
  └── entity_refs: list[EntityRef]

IngestionResult
  ├── records_created: list[CreatedRecord]
  ├── review_items: list[CreatedReviewItem]
  ├── legal_instruments: list[CreatedLegalInstrument]
  ├── errors: list[str]
  └── success: bool  (property — True if no errors)
```

## Source Lifecycle States (as of audit)

| lifecycle_state     | Count | Description                          |
| ------------------- | ----- | ------------------------------------ |
| `runnable`          | 1     | Has adapter, enabled by default      |
| `runnable_disabled` | 5     | Has adapter, disabled pending config |
| `portal_reference`  | 8     | Manual portal — no adapter yet       |
| `disabled_stub`     | 4     | Adapter planned, not built           |
| `deprecated`        | 3     | Superseded — do not use              |
| `manual_reference`  | 3     | Manual data entry only               |

## Deprecated Sources (to archive)

| source_key                       | Superseded by          | Action                                                            |
| -------------------------------- | ---------------------- | ----------------------------------------------------------------- |
| `scc_judgments`                  | `scc_decisions`        | Mark `automation_status: deprecated`, `lifecycle_state: archived` |
| `federal_court_canada_decisions` | `federal_court_canada` | Mark `automation_status: deprecated`, `lifecycle_state: archived` |

## Missing Spec Fields (Sprint C target)

All 26 YAML entries are missing these 7 fields:

- `confidence_class` — quality tier (high / medium / low / unclassified)
- `retention_policy` — data retention period or policy reference
- `canonical_url` — stable, human-readable URL for the source homepage
- `evidence_required` — bool — whether records require evidence snapshot
- `terms_verified` — bool + date — whether ToS compliance has been confirmed
- `authentication_required` — bool — whether API key is required
- `rate_limit_policy` — max requests/day or "unrestricted"
