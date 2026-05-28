"""Tests for the canonical public status contract.

Verifies that:
- PUBLIC_VISIBLE_STATUSES contains exactly public_safe and public_redacted.
- Non-public statuses (private, admin_only, blocked) are never in PUBLIC_VISIBLE_STATUSES.
- The legacy "published" value is NOT in PUBLIC_VISIBLE_STATUSES.
- PublicReleasePolicy.is_incident_publicly_releasable uses the canonical constants.
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from app.policies.public_status import (
    PUBLIC_SAFE,
    PUBLIC_REDACTED,
    PUBLIC_PRIVATE,
    PUBLIC_ADMIN_ONLY,
    PUBLIC_BLOCKED,
    LEGACY_PUBLISHED,
    PUBLIC_VISIBLE_STATUSES,
    NON_PUBLIC_STATUSES,
    REVIEW_APPROVED,
    REVIEW_PENDING,
    REVIEW_REJECTED,
)
from app.services.public_release_policy import PublicReleasePolicy


# ---------------------------------------------------------------------------
# Constant contract
# ---------------------------------------------------------------------------


def test_public_safe_is_visible():
    assert PUBLIC_SAFE in PUBLIC_VISIBLE_STATUSES


def test_public_redacted_is_visible():
    assert PUBLIC_REDACTED in PUBLIC_VISIBLE_STATUSES


def test_private_is_not_visible():
    assert PUBLIC_PRIVATE not in PUBLIC_VISIBLE_STATUSES


def test_admin_only_is_not_visible():
    assert PUBLIC_ADMIN_ONLY not in PUBLIC_VISIBLE_STATUSES


def test_blocked_is_not_visible():
    assert PUBLIC_BLOCKED not in PUBLIC_VISIBLE_STATUSES


def test_legacy_published_is_not_visible():
    """'published' is a legacy value that must never grant public visibility."""
    assert LEGACY_PUBLISHED not in PUBLIC_VISIBLE_STATUSES


def test_visible_statuses_are_exactly_two():
    assert PUBLIC_VISIBLE_STATUSES == frozenset({PUBLIC_SAFE, PUBLIC_REDACTED})


def test_non_public_statuses_contain_private_admin_blocked():
    assert NON_PUBLIC_STATUSES == frozenset(
        {PUBLIC_PRIVATE, PUBLIC_ADMIN_ONLY, PUBLIC_BLOCKED}
    )


def test_visible_and_non_public_are_disjoint():
    assert PUBLIC_VISIBLE_STATUSES.isdisjoint(NON_PUBLIC_STATUSES)


# ---------------------------------------------------------------------------
# PublicReleasePolicy contract
# ---------------------------------------------------------------------------


def _make_incident(**kwargs):
    """Return a minimal mock GeoLegalEvent with valid defaults for public release."""
    incident = MagicMock()
    incident.id = "test-incident-1"
    incident.publish_status = kwargs.get("publish_status", PUBLIC_SAFE)
    incident.review_status = kwargs.get("review_status", REVIEW_APPROVED)
    incident.source_ids = kwargs.get("source_ids", ["src-1"])
    incident.evidence_ids = kwargs.get("evidence_ids", [])
    incident.claim_ids = kwargs.get("claim_ids", [])
    incident.lat = kwargs.get("lat", 45.4215)
    incident.lng = kwargs.get("lng", -75.6972)
    # Suppress / dispute flags
    incident.is_suppressed = kwargs.get("is_suppressed", False)
    incident.is_disputed = kwargs.get("is_disputed", False)
    incident.metadata_json = kwargs.get("metadata_json", {})
    return incident


def _session():
    return MagicMock()


def test_public_safe_approved_evidence_is_releasable():
    incident = _make_incident(publish_status=PUBLIC_SAFE, review_status=REVIEW_APPROVED)
    assert PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)


def test_public_redacted_approved_evidence_is_releasable():
    incident = _make_incident(publish_status=PUBLIC_REDACTED, review_status=REVIEW_APPROVED)
    assert PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)


def test_private_is_not_releasable():
    incident = _make_incident(publish_status=PUBLIC_PRIVATE, review_status=REVIEW_APPROVED)
    assert not PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)


def test_admin_only_is_not_releasable():
    incident = _make_incident(publish_status=PUBLIC_ADMIN_ONLY, review_status=REVIEW_APPROVED)
    assert not PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)


def test_blocked_is_not_releasable():
    incident = _make_incident(publish_status=PUBLIC_BLOCKED, review_status=REVIEW_APPROVED)
    assert not PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)


def test_legacy_published_is_not_releasable():
    """Legacy 'published' must NOT grant public visibility under the new policy."""
    incident = _make_incident(publish_status=LEGACY_PUBLISHED, review_status=REVIEW_APPROVED)
    assert not PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)


def test_unapproved_review_not_releasable():
    incident = _make_incident(publish_status=PUBLIC_SAFE, review_status=REVIEW_PENDING)
    assert not PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)


def test_rejected_review_not_releasable():
    incident = _make_incident(publish_status=PUBLIC_SAFE, review_status=REVIEW_REJECTED)
    assert not PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)


def test_no_evidence_not_releasable():
    incident = _make_incident(
        publish_status=PUBLIC_SAFE,
        review_status=REVIEW_APPROVED,
        source_ids=[],
        evidence_ids=[],
        claim_ids=[],
    )
    assert not PublicReleasePolicy.is_incident_publicly_releasable(_session(), incident)
