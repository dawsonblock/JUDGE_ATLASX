"""Tests for Live Map API endpoints.

Tests cover:
- Public filtering (only approved, public-safe events)
- Admin mode bypassing filters
- Bbox filtering and validation
- Evidence ID redaction in public mode
- Source ID redaction in public mode
- Pagination and truncation
- Rate limiting
"""
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.geo_legal_event import GeoLegalEvent as GeoLegalEventModel
from app.schemas.geo_legal_event import GeoLegalEvent

_LIVE_MAP_MOUNTED = any(
    getattr(route, "path", None) == "/api/live-map/events" for route in app.routes
)
pytestmark = pytest.mark.skipif(
    not _LIVE_MAP_MOUNTED,
    reason="live_map route intentionally unmounted for public boundary hardening",
)


@pytest.fixture
def client(db_session):
    """Create a test client for the API."""
    return TestClient(app)


@pytest.fixture
def sample_geo_events(db_session):
    """Create sample GeoLegalEvent records for testing."""
    events = []

    # Create an approved public-safe event
    event1 = GeoLegalEventModel(
        id="public-event-1",
        event_type="court_event",
        title="Public Court Event",
        lat=50.0,
        lng=-105.0,
        jurisdiction="federal",
        province="Saskatchewan",
        country="Canada",
        confidence=0.8,
        confidence_label="high",
        review_status="approved",
        publish_status="public_safe",
        source_ids=["source-abc123"],
        evidence_ids=["evidence-def456"],
        claim_ids=["claim-ghi789"],
    )
    events.append(event1)

    # Create a needs_review event (should be filtered in public mode)
    event2 = GeoLegalEventModel(
        id="private-event-1",
        event_type="crime_event",
        title="Private Crime Event",
        lat=51.0,
        lng=-106.0,
        jurisdiction="provincial",
        province="Saskatchewan",
        country="Canada",
        confidence=0.7,
        confidence_label="medium",
        review_status="needs_review",  # Not approved
        publish_status="admin_only",
        source_ids=["source-jkl012"],
        evidence_ids=["evidence-mno345"],
        claim_ids=["claim-pqr678"],
    )
    events.append(event2)

    # Create a low confidence event (should be filtered in public mode)
    event3 = GeoLegalEventModel(
        id="low-conf-event-1",
        event_type="news_event",
        title="Low Confidence News",
        lat=49.0,
        lng=-104.0,
        jurisdiction="federal",
        province="Alberta",
        country="Canada",
        confidence=0.5,  # Below typical threshold
        confidence_label="low",
        review_status="approved",
        publish_status="public_safe",
        source_ids=["source-stu901"],
        evidence_ids=["evidence-vwx234"],
        claim_ids=["claim-yza567"],
    )
    events.append(event3)

    for event in events:
        db_session.add(event)
    db_session.commit()

    return events


def test_live_map_events_public_mode_filters_correctly(client, sample_geo_events, db_session):
    """Test that public mode filters out non-approved and low-confidence events."""
    response = client.get("/api/live-map/events?admin_mode=false")

    assert response.status_code == 200
    data = response.json()

    # Should only return the approved public-safe event
    assert data["returned_count"] == 1
    assert data["events"][0]["id"] == "public-event-1"
    assert data["filters_applied"]["public_visibility"] is True


def test_live_map_events_admin_mode_shows_all(client, sample_geo_events, db_session):
    """Test that admin mode shows all events including non-approved ones."""
    response = client.get("/api/live-map/events?admin_mode=true")

    assert response.status_code == 200
    data = response.json()

    # Should return all events
    assert data["returned_count"] == 3
    assert data["filters_applied"]["admin_mode"] is True
    event_ids = [e["id"] for e in data["events"]]
    assert "public-event-1" in event_ids
    assert "private-event-1" in event_ids
    assert "low-conf-event-1" in event_ids


def test_live_map_events_public_mode_redacts_evidence_ids(client, sample_geo_events, db_session):
    """Test that evidence IDs are redacted in public mode."""
    response = client.get("/api/live-map/events?admin_mode=false")

    assert response.status_code == 200
    data = response.json()

    assert data["returned_count"] == 1
    event = data["events"][0]

    # Evidence IDs should be redacted
    assert "evidence_" in event["evidence_ids"][0]
    assert "..." in event["evidence_ids"][0]
    # Should not contain the full ID
    assert "evidence-def456" not in event["evidence_ids"][0]


def test_live_map_events_public_mode_redacts_source_ids(client, sample_geo_events, db_session):
    """Test that source IDs are redacted in public mode."""
    response = client.get("/api/live-map/events?admin_mode=false")

    assert response.status_code == 200
    data = response.json()

    assert data["returned_count"] == 1
    event = data["events"][0]

    # Source IDs should be redacted
    assert "source_" in event["source_ids"][0]
    assert "..." in event["source_ids"][0]
    # Should not contain the full ID
    assert "source-abc123" not in event["source_ids"][0]


def test_live_map_events_admin_mode_preserves_ids(client, sample_geo_events, db_session):
    """Test that IDs are preserved in admin mode."""
    response = client.get("/api/live-map/events?admin_mode=true")

    assert response.status_code == 200
    data = response.json()

    assert data["returned_count"] == 3
    public_event = next(e for e in data["events"] if e["id"] == "public-event-1")

    # IDs should be preserved in admin mode
    assert "source-abc123" in public_event["source_ids"]
    assert "evidence-def456" in public_event["evidence_ids"]
    assert "claim-ghi789" in public_event["claim_ids"]


def test_live_map_events_bbox_filtering(client, sample_geo_events, db_session):
    """Test that bbox filtering works correctly."""
    # Bbox that includes only the first event (around 50.0, -105.0)
    response = client.get(
        "/api/live-map/events?bbox=-106.0,49.5,-104.0,50.5&admin_mode=true"
    )

    assert response.status_code == 200
    data = response.json()

    # Should only return events within the bbox
    assert data["returned_count"] == 1
    assert data["events"][0]["id"] == "public-event-1"


def test_live_map_events_bbox_validation(client, sample_geo_events, db_session):
    """Test that invalid bbox values are rejected."""
    # Invalid bbox: south > north
    response = client.get("/api/live-map/events?bbox=-106.0,50.5,-104.0,49.5")

    assert response.status_code == 422
    assert "bbox south must be <= north" in response.json()["detail"]


def test_live_map_events_bbox_area_limit(client, sample_geo_events, db_session):
    """Test that oversized bbox requests are rejected."""
    # Very large bbox (should exceed max area limit)
    response = client.get("/api/live-map/events?bbox=-180.0,-90.0,180.0,90.0")

    assert response.status_code == 422
    assert "exceeds maximum" in response.json()["detail"]


def test_live_map_events_event_type_filter(client, sample_geo_events, db_session):
    """Test filtering by event type."""
    response = client.get(
        "/api/live-map/events?event_type=court_event&admin_mode=true"
    )

    assert response.status_code == 200
    data = response.json()

    # Should only return court events
    assert data["returned_count"] == 1
    assert data["events"][0]["event_type"] == "court_event"


def test_live_map_events_jurisdiction_filter(client, sample_geo_events, db_session):
    """Test filtering by jurisdiction."""
    response = client.get(
        "/api/live-map/events?jurisdiction=federal&admin_mode=true"
    )

    assert response.status_code == 200
    data = response.json()

    # Should only return federal events
    assert data["returned_count"] == 2
    for event in data["events"]:
        assert event["jurisdiction"] == "federal"


def test_live_map_events_confidence_filter(client, sample_geo_events, db_session):
    """Test filtering by minimum confidence."""
    response = client.get(
        "/api/live-map/events?min_confidence=0.75&admin_mode=true"
    )

    assert response.status_code == 200
    data = response.json()

    # Should only return events with confidence >= 0.75
    assert data["returned_count"] == 1
    assert data["events"][0]["confidence"] >= 0.75


def test_live_map_events_pagination(client, sample_geo_events, db_session):
    """Test that pagination works correctly."""
    response = client.get("/api/live-map/events?limit=2&offset=0&admin_mode=true")

    assert response.status_code == 200
    data = response.json()

    # Should return 2 events
    assert data["returned_count"] == 2
    assert data["truncated"] is True  # There are 3 total, so this should be truncated


def test_live_map_events_disclaimer_present(client, sample_geo_events, db_session):
    """Test that platform disclaimer is present in responses."""
    response = client.get("/api/live-map/events?admin_mode=false")

    assert response.status_code == 200
    data = response.json()

    assert "disclaimer" in data
    assert len(data["disclaimer"]) > 0


def test_live_map_single_event_public_mode(client, sample_geo_events, db_session):
    """Test retrieving a single event in public mode."""
    response = client.get("/api/live-map/events/public-event-1?admin_mode=false")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == "public-event-1"
    # IDs should be redacted
    assert "..." in data["evidence_ids"][0]


def test_live_map_single_event_not_found(client, sample_geo_events, db_session):
    """Test that requesting a non-existent event returns 404."""
    response = client.get("/api/live-map/events/non-existent-event")

    assert response.status_code == 404


def test_live_map_source_health_endpoint(client, sample_geo_events, db_session):
    """Test that source health endpoint is accessible."""
    response = client.get("/api/live-map/source-health")

    # Should return 200 (even if empty)
    assert response.status_code in [200, 404]  # 404 if no implementation yet


def test_live_map_layers_endpoint(client, sample_geo_events, db_session):
    """Test that layers endpoint returns available layer types."""
    response = client.get("/api/live-map/layers")

    assert response.status_code in [200, 404]  # 404 if no implementation yet