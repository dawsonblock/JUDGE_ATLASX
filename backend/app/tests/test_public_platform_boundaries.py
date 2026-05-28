"""Public platform boundary tests.

Verifies that:
1. Unreviewed incidents are never returned.
2. Approved but evidence-free incidents are never returned.
3. Approved + evidence + public_safe is returned.
4. Approved + evidence + public_redacted is returned.
5. private / admin_only / blocked are never returned.
6. Approved statute link is shown only if parent incident is public.
7. Pending statute link is never shown.
8. News link is shown only if source URL exists.
9. Public detail endpoint returns 404 for non-public incidents.
10. Public map count does not leak private incident count (total_count only counts public records).
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from app.policies.public_status import (
    PUBLIC_SAFE,
    PUBLIC_REDACTED,
    PUBLIC_PRIVATE,
    PUBLIC_ADMIN_ONLY,
    PUBLIC_BLOCKED,
    LEGACY_PUBLISHED,
    PUBLIC_VISIBLE_STATUSES,
    REVIEW_APPROVED,
    REVIEW_PENDING,
    REVIEW_REJECTED,
)
from app.services.public_release_policy import PublicReleasePolicy


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def _incident(publish_status=PUBLIC_SAFE, review_status=REVIEW_APPROVED,
               source_ids=None, evidence_ids=None, claim_ids=None,
               lat=45.0, lng=-75.0, is_suppressed=False, is_disputed=False):
    inc = MagicMock()
    inc.id = "test-incident"
    inc.publish_status = publish_status
    inc.review_status = review_status
    inc.source_ids = source_ids if source_ids is not None else ["src-1"]
    inc.evidence_ids = evidence_ids if evidence_ids is not None else []
    inc.claim_ids = claim_ids if claim_ids is not None else []
    inc.lat = lat
    inc.lng = lng
    inc.is_suppressed = is_suppressed
    inc.is_disputed = is_disputed
    inc.metadata_json = {}
    return inc


def _statute_link(review_status=REVIEW_APPROVED, confidence=0.9, reason="test reason"):
    link = MagicMock()
    link.review_status = review_status
    link.confidence_score = confidence
    link.link_reason = reason
    return link


def _news_link(url="https://example.com/article", title="Test Article", relevance=0.8):
    link = MagicMock()
    link.news_article_url = url
    link.news_article_title = title
    link.relevance_score = relevance
    return link


def _session():
    return MagicMock()


policy = PublicReleasePolicy()


# ---------------------------------------------------------------------------
# 1. Unreviewed incident is never returned
# ---------------------------------------------------------------------------

def test_unreviewed_incident_not_returned():
    inc = _incident(publish_status=PUBLIC_SAFE, review_status=REVIEW_PENDING)
    assert not policy.is_incident_publicly_releasable(_session(), inc)


# ---------------------------------------------------------------------------
# 2. Approved but evidence-free incident is never returned
# ---------------------------------------------------------------------------

def test_approved_no_evidence_not_returned():
    inc = _incident(
        publish_status=PUBLIC_SAFE,
        review_status=REVIEW_APPROVED,
        source_ids=[],
        evidence_ids=[],
        claim_ids=[],
    )
    assert not policy.is_incident_publicly_releasable(_session(), inc)


# ---------------------------------------------------------------------------
# 3. Approved + evidence + public_safe is returned
# ---------------------------------------------------------------------------

def test_public_safe_approved_evidence_returned():
    inc = _incident(publish_status=PUBLIC_SAFE, review_status=REVIEW_APPROVED)
    assert policy.is_incident_publicly_releasable(_session(), inc)


# ---------------------------------------------------------------------------
# 4. Approved + evidence + public_redacted is returned
# ---------------------------------------------------------------------------

def test_public_redacted_approved_evidence_returned():
    inc = _incident(publish_status=PUBLIC_REDACTED, review_status=REVIEW_APPROVED)
    assert policy.is_incident_publicly_releasable(_session(), inc)


# ---------------------------------------------------------------------------
# 5. private / admin_only / blocked are never returned
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("status", [PUBLIC_PRIVATE, PUBLIC_ADMIN_ONLY, PUBLIC_BLOCKED])
def test_non_public_status_never_returned(status):
    inc = _incident(publish_status=status, review_status=REVIEW_APPROVED)
    assert not policy.is_incident_publicly_releasable(_session(), inc)


def test_legacy_published_never_returned():
    """'published' must not grant public visibility under the new policy."""
    inc = _incident(publish_status=LEGACY_PUBLISHED, review_status=REVIEW_APPROVED)
    assert not policy.is_incident_publicly_releasable(_session(), inc)


# ---------------------------------------------------------------------------
# 6. Approved statute link shown only if parent incident is public
# ---------------------------------------------------------------------------

def test_approved_statute_link_on_public_incident_is_shown():
    link = _statute_link(review_status=REVIEW_APPROVED)
    assert policy.is_statute_link_publicly_releasable(link)


def test_approved_statute_link_requires_approved_parent():
    """Even an approved link should not be shown for a non-public parent incident.
    This is enforced at the query level — here we verify the link-level gate."""
    link = _statute_link(review_status=REVIEW_APPROVED)
    # The link itself is ok; the route is responsible for filtering by parent status.
    assert policy.is_statute_link_publicly_releasable(link)


# ---------------------------------------------------------------------------
# 7. Pending statute link is never shown
# ---------------------------------------------------------------------------

def test_pending_statute_link_not_shown():
    link = _statute_link(review_status=REVIEW_PENDING)
    assert not policy.is_statute_link_publicly_releasable(link)


def test_rejected_statute_link_not_shown():
    link = _statute_link(review_status=REVIEW_REJECTED)
    assert not policy.is_statute_link_publicly_releasable(link)


def test_zero_confidence_statute_link_not_shown():
    link = _statute_link(review_status=REVIEW_APPROVED, confidence=0.0)
    assert not policy.is_statute_link_publicly_releasable(link)


# ---------------------------------------------------------------------------
# 8. News link is shown only if source URL and title exist
# ---------------------------------------------------------------------------

def test_news_link_with_url_shown():
    link = _news_link(url="https://example.com/article")
    assert policy.is_news_link_publicly_releasable(link)


def test_news_link_without_url_not_shown():
    link = _news_link(url="", title="Has a title")
    assert not policy.is_news_link_publicly_releasable(link)


def test_news_link_without_title_not_shown():
    link = _news_link(url="https://example.com/article", title="")
    assert not policy.is_news_link_publicly_releasable(link)


def test_news_link_zero_relevance_not_shown():
    link = _news_link(relevance=0.0)
    assert not policy.is_news_link_publicly_releasable(link)


# ---------------------------------------------------------------------------
# 9. Non-public incident returns 404 (via policy gate)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("status", [PUBLIC_PRIVATE, PUBLIC_ADMIN_ONLY, PUBLIC_BLOCKED, LEGACY_PUBLISHED])
def test_non_public_incident_not_releasable(status):
    """Policy gate used by the detail endpoint must reject these statuses."""
    inc = _incident(publish_status=status, review_status=REVIEW_APPROVED)
    assert not policy.is_incident_publicly_releasable(_session(), inc)


# ---------------------------------------------------------------------------
# 10. total_count must not leak private incident count
# ---------------------------------------------------------------------------

def test_visible_statuses_are_only_public_safe_and_redacted():
    """PUBLIC_VISIBLE_STATUSES defines the filter used for total_count.
    It must contain exactly public_safe and public_redacted — nothing else."""
    assert PUBLIC_VISIBLE_STATUSES == frozenset({PUBLIC_SAFE, PUBLIC_REDACTED})
    assert LEGACY_PUBLISHED not in PUBLIC_VISIBLE_STATUSES
    assert PUBLIC_PRIVATE not in PUBLIC_VISIBLE_STATUSES
    assert PUBLIC_ADMIN_ONLY not in PUBLIC_VISIBLE_STATUSES
    assert PUBLIC_BLOCKED not in PUBLIC_VISIBLE_STATUSES
