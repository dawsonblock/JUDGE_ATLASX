"""
Public Platform Boundary Tests

These tests verify that the public API enforces the evidence-first principles
and never leaks private data, unreviewed incidents, or unsupported claims.

CRITICAL: These negative tests are more important than happy-path tests.
Passing these means the system is safe for public use.
"""

import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.geo_legal_event import GeoLegalEvent
from app.models.entities import StatuteIncidentLink, IncidentNewsLink
from app.services.public_release_policy import PublicReleasePolicy


class TestPublicReleasePolicy:
    """Test the public release eligibility policy."""

    async def test_unpublished_incident_is_hidden(self, session: AsyncSession):
        """Unpublished incidents must never be public."""
        policy = PublicReleasePolicy()

        incident = GeoLegalEvent(
            id="test-unpublished",
            title="Test Incident",
            event_type="assault",
            jurisdiction="Saskatchewan",
            country="Canada",
            publish_status="draft",  # NOT published
            review_status="approved",
            confidence=0.8,
            confidence_label="high",
            lat=52.1332,
            lng=-106.6700,
            source_ids=["source-1"],
        )

        is_public = await policy.is_incident_publicly_releasable(session, incident)
        assert not is_public, "Unpublished incident must not be public"

    async def test_pending_review_incident_is_hidden(self, session: AsyncSession):
        """Pending-review incidents must not be public."""
        policy = PublicReleasePolicy()

        incident = GeoLegalEvent(
            id="test-pending-review",
            title="Test Incident",
            event_type="assault",
            jurisdiction="Saskatchewan",
            country="Canada",
            publish_status="published",
            review_status="pending",  # PENDING, not approved
            confidence=0.8,
            confidence_label="high",
            lat=52.1332,
            lng=-106.6700,
            source_ids=["source-1"],
        )

        is_public = await policy.is_incident_publicly_releasable(session, incident)
        assert not is_public, "Pending-review incident must not be public"

    async def test_rejected_incident_is_hidden(self, session: AsyncSession):
        """Rejected incidents must not be public."""
        policy = PublicReleasePolicy()

        incident = GeoLegalEvent(
            id="test-rejected",
            title="Test Incident",
            event_type="assault",
            jurisdiction="Saskatchewan",
            country="Canada",
            publish_status="published",
            review_status="rejected",  # REJECTED
            confidence=0.8,
            confidence_label="high",
            lat=52.1332,
            lng=-106.6700,
            source_ids=["source-1"],
        )

        is_public = await policy.is_incident_publicly_releasable(session, incident)
        assert not is_public, "Rejected incident must not be public"

    async def test_approved_published_with_evidence_is_public(
        self, session: AsyncSession
    ):
        """Approved, published incident with evidence CAN be public."""
        policy = PublicReleasePolicy()

        incident = GeoLegalEvent(
            id="test-public",
            title="Test Incident",
            event_type="assault",
            jurisdiction="Saskatchewan",
            country="Canada",
            publish_status="published",  # PUBLISHED
            review_status="approved",  # APPROVED
            confidence=0.8,
            confidence_label="high",
            lat=52.1332,  # Valid
            lng=-106.6700,  # Valid
            source_ids=["source-1"],  # HAS evidence
        )

        is_public = await policy.is_incident_publicly_releasable(session, incident)
        assert is_public, "Approved, published incident with evidence MUST be public"

    async def test_incident_without_evidence_is_hidden(self, session: AsyncSession):
        """Incidents without linked evidence must not be public."""
        policy = PublicReleasePolicy()

        incident = GeoLegalEvent(
            id="test-no-evidence",
            title="Test Incident",
            event_type="assault",
            jurisdiction="Saskatchewan",
            country="Canada",
            publish_status="published",
            review_status="approved",
            confidence=0.8,
            confidence_label="high",
            lat=52.1332,
            lng=-106.6700,
            source_ids=None,  # NO evidence
            evidence_ids=None,
            claim_ids=None,
        )

        is_public = await policy.is_incident_publicly_releasable(session, incident)
        assert not is_public, "Incident without evidence must not be public"

    async def test_incident_with_missing_coordinates_is_hidden(
        self, session: AsyncSession
    ):
        """Incidents with missing or invalid coordinates must not be public."""
        policy = PublicReleasePolicy()

        incident = GeoLegalEvent(
            id="test-no-coords",
            title="Test Incident",
            event_type="assault",
            jurisdiction="Saskatchewan",
            country="Canada",
            publish_status="published",
            review_status="approved",
            confidence=0.8,
            confidence_label="high",
            lat=None,  # MISSING
            lng=None,  # MISSING
            source_ids=["source-1"],
        )

        is_public = await policy.is_incident_publicly_releasable(session, incident)
        assert not is_public, "Incident without coordinates must not be public"

    async def test_incident_with_invalid_coordinates_is_hidden(
        self, session: AsyncSession
    ):
        """Incidents with out-of-range coordinates must not be public."""
        policy = PublicReleasePolicy()

        incident = GeoLegalEvent(
            id="test-bad-coords",
            title="Test Incident",
            event_type="assault",
            jurisdiction="Saskatchewan",
            country="Canada",
            publish_status="published",
            review_status="approved",
            confidence=0.8,
            confidence_label="high",
            lat=999.0,  # INVALID (must be -90 to 90)
            lng=-106.6700,
            source_ids=["source-1"],
        )

        is_public = await policy.is_incident_publicly_releasable(session, incident)
        assert not is_public, "Incident with invalid coordinates must not be public"

    async def test_suppressed_incident_is_hidden(self, session: AsyncSession):
        """Suppressed incidents must not be public."""
        policy = PublicReleasePolicy()

        incident = GeoLegalEvent(
            id="test-suppressed",
            title="Test Incident",
            event_type="assault",
            jurisdiction="Saskatchewan",
            country="Canada",
            publish_status="published",
            review_status="approved",
            confidence=0.8,
            confidence_label="high",
            lat=52.1332,
            lng=-106.6700,
            source_ids=["source-1"],
            metadata_json={"is_private": True},  # SUPPRESSED
        )

        is_public = await policy.is_incident_publicly_releasable(session, incident)
        assert not is_public, "Suppressed incident must not be public"


class TestPublicStatuteLink:
    """Test statute link eligibility."""

    async def test_pending_statute_link_is_hidden(self):
        """Pending-review statute links must not be public."""
        policy = PublicReleasePolicy()

        link = StatuteIncidentLink(
            id=1,
            incident_id="inc-1",
            legal_section_id=123,
            link_reason="This statute is relevant",
            confidence_score=0.8,
            ai_model_version="1.0",
            review_status="pending",  # PENDING
        )

        is_public = await policy.is_statute_link_publicly_releasable(link)
        assert not is_public, "Pending statute link must not be public"

    async def test_approved_statute_link_is_public(self):
        """Approved statute links can be public."""
        policy = PublicReleasePolicy()

        link = StatuteIncidentLink(
            id=1,
            incident_id="inc-1",
            legal_section_id=123,
            link_reason="This statute is relevant",
            confidence_score=0.8,  # Positive confidence
            ai_model_version="1.0",
            review_status="approved",  # APPROVED
        )

        is_public = await policy.is_statute_link_publicly_releasable(link)
        assert is_public, "Approved statute link MUST be public"

    async def test_statute_link_with_zero_confidence_is_hidden(self):
        """Statute links with zero confidence must not be public."""
        policy = PublicReleasePolicy()

        link = StatuteIncidentLink(
            id=1,
            incident_id="inc-1",
            legal_section_id=123,
            link_reason="This statute is relevant",
            confidence_score=0.0,  # ZERO confidence
            ai_model_version="1.0",
            review_status="approved",
        )

        is_public = await policy.is_statute_link_publicly_releasable(link)
        assert not is_public, "Zero-confidence link must not be public"


class TestPublicNewsLink:
    """Test news link eligibility."""

    async def test_news_link_with_invalid_url_is_hidden(self):
        """News links without valid URLs must not be public."""
        policy = PublicReleasePolicy()

        link = IncidentNewsLink(
            id=1,
            incident_id="inc-1",
            news_article_title="Article Title",
            news_article_url="",  # EMPTY URL
            relevance_score=0.8,
            link_method="manual",
        )

        is_public = await policy.is_news_link_publicly_releasable(link)
        assert not is_public, "News link without URL must not be public"

    async def test_news_link_with_zero_relevance_is_hidden(self):
        """News links with zero relevance must not be public."""
        policy = PublicReleasePolicy()

        link = IncidentNewsLink(
            id=1,
            incident_id="inc-1",
            news_article_title="Article Title",
            news_article_url="https://example.com/article",
            relevance_score=0.0,  # ZERO relevance
            link_method="manual",
        )

        is_public = await policy.is_news_link_publicly_releasable(link)
        assert not is_public, "Zero-relevance news link must not be public"

    async def test_valid_news_link_is_public(self):
        """Valid news links can be public."""
        policy = PublicReleasePolicy()

        link = IncidentNewsLink(
            id=1,
            incident_id="inc-1",
            news_article_title="Article Title",
            news_article_url="https://example.com/article",
            relevance_score=0.8,  # Positive relevance
            link_method="manual",
        )

        is_public = await policy.is_news_link_publicly_releasable(link)
        assert is_public, "Valid news link MUST be public"
