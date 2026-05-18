"""Test fixture for sk_courts_qb_decisions source (Phase 8).

This file provides test fixtures for the Saskatchewan Courts QB Decisions source
adapter to enable testing of the ingestion pipeline.
"""

import pytest
from app.ingestion.source_adapters.sk_courts_html import SKCourtsHtmlAdapter


@pytest.fixture
def sk_courts_qb_decisions_adapter():
    """Create an SKCourtsHtmlAdapter instance for testing."""
    return SKCourtsHtmlAdapter(
        source_key="sk_courts_qb_decisions",
        base_url="https://sasklawcourts.ca/saskatchewan-court-decisions/",
        allowed_domains_json='["sasklawcourts.ca", "www.sasklawcourts.ca", "canlii.org", "www.canlii.org"]',
        public_record_authority="official_court_record",
    )


@pytest.fixture
def sk_courts_qb_decisions_mock_html():
    """Mock HTML content for Saskatchewan Courts decisions page."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Saskatchewan Court Decisions</title></head>
    <body>
        <h1>Saskatchewan Court Decisions</h1>
        <p>Decisions are published on CanLII:</p>
        <ul>
            <li><a href="https://www.canlii.org/en/sk/skkb/">Saskatchewan Court of King's Bench</a></li>
            <li><a href="https://www.canlii.org/en/sk/skca/">Saskatchewan Court of Appeal</a></li>
            <li><a href="https://www.canlii.org/en/sk/skpc/">Saskatchewan Provincial Court</a></li>
        </ul>
    </body>
    </html>
    """


@pytest.fixture
def sk_courts_qb_decisions_expected_records():
    """Expected parsed records from Saskatchewan Courts decisions page."""
    return [
        {
            "url": "https://www.canlii.org/en/sk/skkb/",
            "headline": "Saskatchewan Court of King's Bench",
        },
        {
            "url": "https://www.canlii.org/en/sk/skca/",
            "headline": "Saskatchewan Court of Appeal",
        },
        {
            "url": "https://www.canlii.org/en/sk/skpc/",
            "headline": "Saskatchewan Provincial Court",
        },
    ]


def test_sk_courts_qb_decisions_adapter_config(sk_courts_qb_decisions_adapter):
    """Test that the adapter is properly configured."""
    assert sk_courts_qb_decisions_adapter._source_key == "sk_courts_qb_decisions"
    assert sk_courts_qb_decisions_adapter._base_url == "https://sasklawcourts.ca/saskatchewan-court-decisions/"
    assert sk_courts_qb_decisions_adapter._public_record_authority == "official_court_record"


def test_sk_courts_qb_decisions_adapter_parse_html(
    sk_courts_qb_decisions_adapter,
    sk_courts_qb_decisions_mock_html,
    sk_courts_qb_decisions_expected_records,
):
    """Test that the adapter correctly parses Saskatchewan Courts HTML."""
    parsed = sk_courts_qb_decisions_adapter._parse_index_page(sk_courts_qb_decisions_mock_html)
    
    # Should extract CanLII links
    assert len(parsed) == 3
    assert parsed == sk_courts_qb_decisions_expected_records


def test_sk_courts_qb_decisions_adapter_parse_empty_html(sk_courts_qb_decisions_adapter):
    """Test that the adapter falls back to known court databases when no links found."""
    empty_html = "<html><body><p>No links here</p></body></html>"
    parsed = sk_courts_qb_decisions_adapter._parse_index_page(empty_html)
    
    # Should fall back to known court databases
    assert len(parsed) == 3
    assert parsed[0]["url"] == "https://www.canlii.org/en/sk/skkb/"
    assert parsed[1]["url"] == "https://www.canlii.org/en/sk/skca/"
    assert parsed[2]["url"] == "https://www.canlii.org/en/sk/skpc/"
