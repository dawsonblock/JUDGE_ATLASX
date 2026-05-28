"""Tests for LegalRiskLabeller."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.services.legal_risk_labeller import LegalRiskLabeller


def _event(title="", description="", crime_type="", id=1):
    ev = MagicMock()
    ev.id = id
    ev.title = title
    ev.description = description
    ev.crime_type = crime_type
    return ev


class TestLowRisk:
    def test_plain_incident_is_low_risk(self):
        label = LegalRiskLabeller.classify(_event(
            title="Theft from vehicle",
            description="Laptop stolen from parked car on Main St",
            crime_type="theft",
        ))
        assert label.level == "low"
        assert label.is_safe_to_publish
        assert not label.requires_human_approval

    def test_low_risk_has_no_redactions(self):
        label = LegalRiskLabeller.classify(_event(
            title="Break and enter",
            crime_type="break_and_enter",
        ))
        assert label.level == "low"
        assert label.redact_fields == []


class TestHighRisk:
    def test_publication_ban_phrase_triggers_high(self):
        label = LegalRiskLabeller.classify(_event(
            title="Trial with publication ban ordered",
            crime_type="assault",
        ))
        assert label.level == "high"
        assert label.requires_human_approval
        assert "exact_address" in label.redact_fields

    def test_youth_offender_phrase_triggers_high(self):
        label = LegalRiskLabeller.classify(_event(
            description="Youth offender appeared in court today",
        ))
        assert label.level == "high"

    def test_sexual_assault_crime_type_triggers_high(self):
        label = LegalRiskLabeller.classify(_event(
            title="Man charged",
            crime_type="sexual_assault",
        ))
        assert label.level == "high"
        assert not label.is_safe_to_publish

    def test_in_camera_hearing_triggers_high(self):
        label = LegalRiskLabeller.classify(_event(
            description="Proceedings held in camera due to sensitivity",
        ))
        assert label.level == "high"

    def test_high_risk_requires_human_approval(self):
        label = LegalRiskLabeller.classify(_event(
            title="YCJA hearing",
            crime_type="youth_offence",
        ))
        assert label.requires_human_approval


class TestMediumRisk:
    def test_ongoing_investigation_is_medium(self):
        label = LegalRiskLabeller.classify(_event(
            description="Police say this is an ongoing investigation.",
        ))
        assert label.level == "medium"
        assert not label.requires_human_approval
        assert "exact_address" in label.redact_fields

    def test_charges_stayed_is_medium(self):
        label = LegalRiskLabeller.classify(_event(
            title="Charges stayed against defendant",
        ))
        assert label.level == "medium"

    def test_domestic_violence_crime_type_is_medium(self):
        label = LegalRiskLabeller.classify(_event(
            crime_type="domestic_violence",
        ))
        assert label.level == "medium"

    def test_not_guilty_verdict_is_medium(self):
        label = LegalRiskLabeller.classify(_event(
            description="The jury returned a not guilty verdict.",
        ))
        assert label.level == "medium"


class TestUnknownRisk:
    def test_empty_event_is_unknown(self):
        label = LegalRiskLabeller.classify(_event())
        assert label.level == "unknown"
        assert label.requires_human_approval


class TestElevation:
    def test_high_beats_medium(self):
        # Both a medium phrase AND a high phrase present
        label = LegalRiskLabeller.classify(_event(
            description="ongoing investigation with publication ban issued",
        ))
        assert label.level == "high"

    def test_multiple_medium_phrases_stay_medium(self):
        label = LegalRiskLabeller.classify(_event(
            description="charges pending and bail conditions set",
        ))
        assert label.level == "medium"
