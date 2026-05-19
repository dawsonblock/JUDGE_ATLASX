"""Public API safety checks (Phase 11).

Tests ensuring public endpoints never expose unsafe data.
"""

import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.entities import (
    Case,
    Court,
    Defendant,
    Event,
    EventDefendant,
    Judge,
    LegalSource,
    Location,
)
from app.services.constants import PUBLIC_REVIEW_STATUSES


client = TestClient(app)


@pytest.fixture
def db_session():
    """Create a test database session."""
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def setup_test_data(db_session: Session):
    """Create test data for safety checks."""
    # Create court
    court = Court(
        name="Test Court",
        jurisdiction="CA-ON",
        court_level="superior",
    )
    db_session.add(court)
    db_session.flush()

    # Create location
    location = Location(
        city="Toronto",
        province_state="Ontario",
        country="Canada",
        latitude=43.6532,
        longitude=-79.3832,
    )
    db_session.add(location)
    db_session.flush()

    # Create judge
    judge = Judge(
        name="Test Judge",
        court_id=court.id,
        cl_person_id="TEST-JUDGE-001",
    )
    db_session.add(judge)
    db_session.flush()

    # Create case
    case = Case(
        case_number="TEST-2024-001",
        filed_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        court_id=court.id,
    )
    db_session.add(case)
    db_session.flush()

    # Create defendant
    defendant = Defendant(
        anonymized_id="DEF-001",
    )
    db_session.add(defendant)
    db_session.flush()

    # Create legal source
    source = LegalSource(
        source_id="TEST-SOURCE-001",
        source_name="Test Source",
        source_type="court_record",
        public_visibility=True,
        review_status="approved",
    )
    db_session.add(source)
    db_session.flush()

    # Create public event (should be visible)
    public_event = Event(
        event_id="EVT-PUBLIC-001",
        case_id=case.id,
        court_id=court.id,
        judge_id=judge.id,
        primary_location_id=location.id,
        event_type="hearing",
        decision_date=datetime(2024, 1, 15, tzinfo=timezone.utc),
        public_visibility=True,
        review_status="approved",
    )
    db_session.add(public_event)
    db_session.flush()

    # Link defendant to public event
    event_defendant = EventDefendant(
        event_id=public_event.id,
        defendant_id=defendant.id,
    )
    db_session.add(event_defendant)
    db_session.flush()

    # Create private event (should NOT be visible)
    private_event = Event(
        event_id="EVT-PRIVATE-001",
        case_id=case.id,
        court_id=court.id,
        judge_id=judge.id,
        primary_location_id=location.id,
        event_type="hearing",
        decision_date=datetime(2024, 1, 20, tzinfo=timezone.utc),
        public_visibility=False,
        review_status="approved",
    )
    db_session.add(private_event)
    db_session.flush()

    # Create pending review event (should NOT be visible)
    pending_event = Event(
        event_id="EVT-PENDING-001",
        case_id=case.id,
        court_id=court.id,
        judge_id=judge.id,
        primary_location_id=location.id,
        event_type="hearing",
        decision_date=datetime(2024, 1, 25, tzinfo=timezone.utc),
        public_visibility=True,
        review_status="pending_review",
    )
    db_session.add(pending_event)
    db_session.flush()

    # Create private source (should NOT be visible)
    private_source = LegalSource(
        source_id="TEST-SOURCE-PRIVATE",
        source_name="Private Source",
        source_type="court_record",
        public_visibility=False,
        review_status="approved",
    )
    db_session.add(private_source)
    db_session.flush()

    db_session.commit()

    return {
        "court": court,
        "location": location,
        "judge": judge,
        "case": case,
        "defendant": defendant,
        "source": source,
        "public_event": public_event,
        "private_event": private_event,
        "pending_event": pending_event,
        "private_source": private_source,
    }


def test_list_events_excludes_private_events(setup_test_data):
    """Public /api/events endpoint must not expose events with public_visibility=False."""
    response = client.get("/api/events")
    assert response.status_code == 200
    
    events = response.json()
    event_ids = [e["event_id"] for e in events]
    
    # Public event should be visible
    assert "EVT-PUBLIC-001" in event_ids
    
    # Private event should NOT be visible
    assert "EVT-PRIVATE-001" not in event_ids
    
    # Pending review event should NOT be visible
    assert "EVT-PENDING-001" not in event_ids


def test_get_event_returns_404_for_private_event(setup_test_data):
    """Public /api/events/{event_id} endpoint must return 404 for private events."""
    response = client.get("/api/events/EVT-PRIVATE-001")
    assert response.status_code == 404


def test_get_event_returns_404_for_pending_review_event(setup_test_data):
    """Public /api/events/{event_id} endpoint must return 404 for pending review events."""
    response = client.get("/api/events/EVT-PENDING-001")
    assert response.status_code == 404


def test_list_judges_excludes_judges_without_public_events(setup_test_data, db_session: Session):
    """Public /api/judges endpoint must not expose judges without public events."""
    # Add a judge with no public events
    court = setup_test_data["court"]
    private_judge = Judge(
        name="Private Judge",
        court_id=court.id,
        cl_person_id="PRIVATE-JUDGE-001",
    )
    db_session.add(private_judge)
    db_session.commit()
    
    response = client.get("/api/judges")
    assert response.status_code == 200
    
    judges = response.json()
    judge_names = [j["name"] for j in judges]
    
    # Test judge (with public event) should be visible
    assert "Test Judge" in judge_names
    
    # Private judge (without public events) should NOT be visible
    assert "Private Judge" not in judge_names


def test_get_judge_returns_404_for_judge_without_public_events(setup_test_data, db_session: Session):
    """Public /api/judges/{judge_id} endpoint must return 404 for judges without public events."""
    court = setup_test_data["court"]
    private_judge = Judge(
        name="Private Judge",
        court_id=court.id,
        cl_person_id="PRIVATE-JUDGE-001",
    )
    db_session.add(private_judge)
    db_session.commit()
    
    response = client.get(f"/api/judges/{private_judge.id}")
    assert response.status_code == 404


def test_list_cases_excludes_cases_without_public_events(setup_test_data, db_session: Session):
    """Public /api/cases endpoint must not expose cases without public events."""
    # Add a case with no public events
    court = setup_test_data["court"]
    private_case = Case(
        case_number="PRIVATE-2024-001",
        filed_date=datetime(2024, 2, 1, tzinfo=timezone.utc),
        court_id=court.id,
    )
    db_session.add(private_case)
    db_session.commit()
    
    response = client.get("/api/cases")
    assert response.status_code == 200
    
    cases = response.json()
    case_numbers = [c["case_number"] for c in cases]
    
    # Test case (with public event) should be visible
    assert "TEST-2024-001" in case_numbers
    
    # Private case (without public events) should NOT be visible
    assert "PRIVATE-2024-001" not in case_numbers


def test_get_case_returns_404_for_case_without_public_events(setup_test_data, db_session: Session):
    """Public /api/cases/{case_id} endpoint must return 404 for cases without public events."""
    court = setup_test_data["court"]
    private_case = Case(
        case_number="PRIVATE-2024-001",
        filed_date=datetime(2024, 2, 1, tzinfo=timezone.utc),
        court_id=court.id,
    )
    db_session.add(private_case)
    db_session.commit()
    
    response = client.get(f"/api/cases/{private_case.id}")
    assert response.status_code == 404


def test_list_sources_excludes_private_sources(setup_test_data):
    """Public /api/sources endpoint must not expose sources with public_visibility=False."""
    response = client.get("/api/sources")
    assert response.status_code == 200
    
    sources = response.json()
    source_ids = [s["source_id"] for s in sources]
    
    # Public source should be visible
    assert "TEST-SOURCE-001" in source_ids
    
    # Private source should NOT be visible
    assert "TEST-SOURCE-PRIVATE" not in source_ids


def test_get_source_returns_404_for_private_source(setup_test_data):
    """Public /api/sources/{source_id} endpoint must return 404 for private sources."""
    response = client.get("/api/sources/TEST-SOURCE-PRIVATE")
    assert response.status_code == 404


def test_get_defendant_anonymizes_personal_data(setup_test_data):
    """Public /api/defendants/{defendant_id} endpoint must not expose personal data."""
    defendant_id = setup_test_data["defendant"].id
    response = client.get(f"/api/defendants/{defendant_id}")
    assert response.status_code == 200
    
    data = response.json()
    
    # Should only return anonymized data
    assert "id" in data
    assert "anonymized_id" in data
    assert "display_label" in data
    assert data["display_label"] == data["anonymized_id"]
    
    # Should include warning about no personal location tracking
    assert "warning" in data
    assert "No personal location tracking" in data["warning"]


def test_get_defendant_returns_404_for_defendant_without_public_events(setup_test_data, db_session: Session):
    """Public /api/defendants/{defendant_id} endpoint must return 404 for defendants without public events."""
    # Add a defendant with no public events
    private_defendant = Defendant(
        anonymized_id="DEF-PRIVATE-001",
    )
    db_session.add(private_defendant)
    db_session.commit()
    
    response = client.get(f"/api/defendants/{private_defendant.id}")
    assert response.status_code == 404


def test_defendant_timeline_excludes_private_events(setup_test_data):
    """Public /api/defendants/{defendant_id}/timeline endpoint must not expose private events."""
    defendant_id = setup_test_data["defendant"].id
    response = client.get(f"/api/defendants/{defendant_id}/timeline")
    assert response.status_code == 200
    
    events = response.json()
    event_ids = [e["event_id"] for e in events]
    
    # Public event should be visible
    assert "EVT-PUBLIC-001" in event_ids
    
    # Private event should NOT be visible
    assert "EVT-PRIVATE-001" not in event_ids
    
    # Pending review event should NOT be visible
    assert "EVT-PENDING-001" not in event_ids


def test_case_timeline_excludes_private_events(setup_test_data):
    """Public /api/cases/{case_id}/timeline endpoint must not expose private events."""
    case_id = setup_test_data["case"].id
    response = client.get(f"/api/cases/{case_id}/timeline")
    assert response.status_code == 200
    
    events = response.json()
    event_ids = [e["event_id"] for e in events]
    
    # Public event should be visible
    assert "EVT-PUBLIC-001" in event_ids
    
    # Private event should NOT be visible
    assert "EVT-PRIVATE-001" not in event_ids
    
    # Pending review event should NOT be visible
    assert "EVT-PENDING-001" not in event_ids


def test_judge_events_excludes_private_events(setup_test_data):
    """Public /api/judges/{judge_id}/events endpoint must not expose private events."""
    judge_id = setup_test_data["judge"].id
    response = client.get(f"/api/judges/{judge_id}/events")
    assert response.status_code == 200
    
    events = response.json()
    event_ids = [e["event_id"] for e in events]
    
    # Public event should be visible
    assert "EVT-PUBLIC-001" in event_ids
    
    # Private event should NOT be visible
    assert "EVT-PRIVATE-001" not in event_ids
    
    # Pending review event should NOT be visible
    assert "EVT-PENDING-001" not in event_ids


def test_all_non_public_review_statuses_are_filtered(setup_test_data, db_session: Session):
    """Public endpoints must filter all non-public review statuses."""
    case = setup_test_data["case"]
    court = setup_test_data["court"]
    judge = setup_test_data["judge"]
    location = setup_test_data["location"]
    
    # Create events with each non-public review status
    non_public_statuses = ["pending", "rejected", "needs_info", "draft"]
    
    for idx, status in enumerate(non_public_statuses):
        event = Event(
            event_id=f"EVT-{status.upper()}-001",
            case_id=case.id,
            court_id=court.id,
            judge_id=judge.id,
            primary_location_id=location.id,
            event_type="hearing",
            decision_date=datetime(2024, idx + 2, 1, tzinfo=timezone.utc),
            public_visibility=True,
            review_status=status,
        )
        db_session.add(event)
    
    db_session.commit()
    
    response = client.get("/api/events")
    assert response.status_code == 200
    
    events = response.json()
    event_ids = [e["event_id"] for e in events]
    
    # All non-public status events should NOT be visible
    for status in non_public_statuses:
        assert f"EVT-{status.upper()}-001" not in event_ids
    
    # Only approved public event should be visible
    assert "EVT-PUBLIC-001" in event_ids


def test_public_endpoints_never_expose_internal_fields(setup_test_data):
    """Public endpoints must never expose internal database fields."""
    response = client.get("/api/events/EVT-PUBLIC-001")
    assert response.status_code == 200
    
    event = response.json()
    
    # Check that internal fields are not exposed
    assert "id" not in event  # Internal database ID
    assert "internal_notes" not in event
    assert "audit_log" not in event
    
    # Only public-safe fields should be present
    assert "event_id" in event
    assert "event_type" in event
    assert "decision_date" in event
