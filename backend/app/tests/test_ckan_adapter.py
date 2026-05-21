"""Focused CKAN adapter hardening tests."""

from __future__ import annotations

import json

from app.ingestion.schemas.ckan_crime_record import SCHEMA_VERSION
from app.ingestion.source_adapters.ckan_api import CKANApiAdapter


def _make_fetch_result(payload: dict):
    class _FetchResult:
        error = None
        raw_content = json.dumps(payload).encode("utf-8")
        http_status = 200
        content_type = "application/json"
        final_url = "https://open.canada.ca/api/3/action/datastore_search"

    return _FetchResult()


def test_ckan_parse_payload_contains_schema_and_review_only_markers() -> None:
    adapter = CKANApiAdapter(
        source_key="canada_open_data_crime",
        base_url="https://open.canada.ca",
        resource_id="rid",
        allowed_domains_json='["open.canada.ca"]',
        public_record_authority="official_statistics",
    )

    parsed = adapter.parse([{"incident_type": "Theft", "lat": 52.1, "lon": -106.6}])

    assert len(parsed) == 1
    payload = parsed[0].payload
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["ingestion_mode"] == "review_only"
    assert payload["parser_version"] == "ckan_api_v1"
    assert payload["public_record_authority"] == "official_statistics"
    assert payload["candidate_record_type"] == "CrimeIncident"


def test_ckan_run_creates_review_items_not_incidents() -> None:
    def _fetcher(url, allowed_domains, *, params=None, **kwargs):
        return _make_fetch_result(
            {
                "success": True,
                "result": {
                    "records": [{"_id": 1, "incident_type": "Theft"}],
                    "total": 1,
                },
            }
        )

    adapter = CKANApiAdapter(
        source_key="canada_open_data_crime",
        base_url="https://open.canada.ca",
        resource_id="rid",
        allowed_domains_json='["open.canada.ca"]',
        public_record_authority="official_statistics",
        fetcher=_fetcher,
    )

    result = adapter.run()

    assert result.errors == []
    assert result.created_records == []
    assert len(result.review_items) == 1
    assert result.review_items[0].payload["ingestion_mode"] == "review_only"


def test_ckan_parse_generates_deterministic_external_id_without_explicit_id() -> None:
    adapter = CKANApiAdapter(
        source_key="saskatoon_open_data_portal",
        base_url="https://opendata.saskatoon.ca",
        resource_id="rid",
        allowed_domains_json='["opendata.saskatoon.ca"]',
        public_record_authority="official_open_data",
    )

    row = {"incident_type": "Assault", "year": 2024}
    parsed_first = adapter.parse([row])[0]
    parsed_second = adapter.parse([row])[0]

    assert parsed_first.external_id.startswith("ckan-")
    assert parsed_first.external_id == parsed_second.external_id
