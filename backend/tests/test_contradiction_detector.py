"""Tests for ContradictionDetector.

These tests use simple MagicMock objects so they run without a real database.
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.services.contradiction_detector import (
    ContradictionDetector,
    ContradictionReport,
    FieldContradiction,
)


def _make_event(
    id: int = 1,
    source_key: str = "source_a",
    external_ref_key: str = "ref-001",
    crime_type: str = "assault",
    occurred_at: datetime | None = None,
    jurisdiction: str = "SK",
    lat: float = 52.1,
    lng: float = -106.7,
    title: str = "Test Incident",
) -> MagicMock:
    ev = MagicMock()
    ev.id = id
    ev.source_key = source_key
    ev.external_ref_key = external_ref_key
    ev.crime_type = crime_type
    ev.occurred_at = occurred_at or datetime(2024, 1, 15, tzinfo=timezone.utc)
    ev.jurisdiction = jurisdiction
    ev.lat = lat
    ev.lng = lng
    ev.title = title
    return ev


class TestContradictionDetectorNoSiblings:
    def test_no_external_ref_key_returns_clean(self):
        session = MagicMock()
        event = _make_event()
        event.external_ref_key = None
        session.get.return_value = event

        detector = ContradictionDetector(session)
        report = detector.check(incident_id=1)

        assert not report.has_contradictions
        assert report.blocking_count == 0
        assert report.advisory_count == 0

    def test_no_siblings_returns_clean(self):
        session = MagicMock()
        event = _make_event()
        session.get.return_value = event
        # Simulate empty sibling query
        session.execute.return_value.scalars.return_value.all.return_value = []

        detector = ContradictionDetector(session)
        report = detector.check(incident_id=1)

        assert not report.has_contradictions
        assert not report.is_publication_blocked

    def test_missing_incident_returns_clean(self):
        session = MagicMock()
        session.get.return_value = None

        detector = ContradictionDetector(session)
        report = detector.check(incident_id=999)

        assert not report.has_contradictions
        assert report.incident_id == 999


class TestContradictionDetectorBlocking:
    def _setup(self, canonical_kwargs: dict, sibling_kwargs: dict):
        canonical = _make_event(id=1, **canonical_kwargs)
        sibling = _make_event(id=2, **sibling_kwargs)

        session = MagicMock()
        session.get.return_value = canonical
        session.execute.return_value.scalars.return_value.all.return_value = [sibling]
        return ContradictionDetector(session)

    def test_crime_type_mismatch_is_blocking(self):
        detector = self._setup(
            {"crime_type": "assault"},
            {"crime_type": "murder", "source_key": "source_b"},
        )
        report = detector.check(1)
        assert report.has_contradictions
        assert report.blocking_count >= 1
        assert report.is_publication_blocked

    def test_jurisdiction_mismatch_is_blocking(self):
        detector = self._setup(
            {"jurisdiction": "SK"},
            {"jurisdiction": "AB", "source_key": "source_b"},
        )
        report = detector.check(1)
        assert report.blocking_count >= 1

    def test_date_mismatch_across_days_is_blocking(self):
        detector = self._setup(
            {"occurred_at": datetime(2024, 1, 15, tzinfo=timezone.utc)},
            {
                "occurred_at": datetime(2024, 1, 20, tzinfo=timezone.utc),
                "source_key": "source_b",
            },
        )
        report = detector.check(1)
        assert report.blocking_count >= 1

    def test_date_same_day_different_hour_is_not_blocking(self):
        """Same date, different time: not a blocking contradiction."""
        detector = self._setup(
            {"occurred_at": datetime(2024, 1, 15, 8, 0, tzinfo=timezone.utc)},
            {
                "occurred_at": datetime(2024, 1, 15, 22, 0, tzinfo=timezone.utc),
                "source_key": "source_b",
            },
        )
        report = detector.check(1)
        # occurred_at checks date only, so same day → no contradiction
        crime_type_contradictions = [
            c for c in report.contradictions if c.field_name == "occurred_at"
        ]
        assert len(crime_type_contradictions) == 0


class TestContradictionDetectorAdvisory:
    def _setup(self, canonical_kwargs: dict, sibling_kwargs: dict):
        canonical = _make_event(id=1, **canonical_kwargs)
        sibling = _make_event(id=2, **sibling_kwargs)
        session = MagicMock()
        session.get.return_value = canonical
        session.execute.return_value.scalars.return_value.all.return_value = [sibling]
        return ContradictionDetector(session)

    def test_title_mismatch_is_advisory_only(self):
        detector = self._setup(
            {"title": "Incident on Main St"},
            {"title": "Incident near Central Park", "source_key": "source_b"},
        )
        report = detector.check(1)
        assert report.has_contradictions
        assert report.advisory_count >= 1
        assert report.blocking_count == 0
        assert not report.is_publication_blocked

    def test_coordinate_mismatch_within_tolerance_is_clean(self):
        """Small coordinate difference (< 10m) should not flag."""
        detector = self._setup(
            {"lat": 52.1000, "lng": -106.7000},
            {"lat": 52.10001, "lng": -106.70001, "source_key": "source_b"},
        )
        report = detector.check(1)
        coord_contradictions = [
            c for c in report.contradictions if c.field_name in ("lat", "lng")
        ]
        assert len(coord_contradictions) == 0

    def test_coordinate_mismatch_beyond_tolerance_is_advisory(self):
        """Large coordinate difference (> 10m) should flag as advisory."""
        detector = self._setup(
            {"lat": 52.1, "lng": -106.7},
            {"lat": 52.5, "lng": -107.0, "source_key": "source_b"},
        )
        report = detector.check(1)
        coord_contradictions = [
            c for c in report.contradictions if c.field_name in ("lat", "lng")
        ]
        assert len(coord_contradictions) >= 1
        assert all(c.severity == "advisory" for c in coord_contradictions)


class TestContradictionDetectorBatch:
    def test_check_batch_returns_one_report_per_id(self):
        session = MagicMock()
        session.get.return_value = None  # All missing → clean reports

        detector = ContradictionDetector(session)
        reports = detector.check_batch([1, 2, 3])

        assert len(reports) == 3
        assert all(isinstance(r, ContradictionReport) for r in reports)
        assert all(not r.has_contradictions for r in reports)
