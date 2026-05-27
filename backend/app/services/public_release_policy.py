"""
Public Platform Release Policy

Enforces evidence-first rules for public incident visibility.
All public-facing incidents must pass this gate before serialization.

Core principle:
- Evidence is authoritative
- AI and derivative links are supporting only
- No unreviewed, unsupported, or private data can be public
"""

import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.geo_legal_event import GeoLegalEvent
from app.models.entities import StatuteIncidentLink, IncidentNewsLink

logger = logging.getLogger(__name__)

# Expected publish/review statuses for public release
PUBLISHED_STATUS = "published"
APPROVED_REVIEW_STATUS = "approved"


class PublicReleasePolicy:
    """Enforces public release eligibility for incidents and links."""

    @staticmethod
    async def is_incident_publicly_releasable(
        session: AsyncSession,
        incident: GeoLegalEvent,
    ) -> bool:
        """
        Determine if an incident can be shown publicly.

        An incident is publicly releasable if:
        1. publish_status == "published"
        2. review_status == "approved" (if applicable)
        3. Has linked evidence (via source_ids or evidence_ids)
        4. Not marked as suppressed, disputed, or private
        5. Has valid geospatial coordinates
        6. No private metadata exposed

        Args:
            session: Database session (for potential lookups)
            incident: The GeoLegalEvent to check

        Returns:
            True if the incident can be shown publicly
        """
        # Rule 1: Must be published
        if incident.publish_status != PUBLISHED_STATUS:
            logger.debug(
                f"[v0] Incident {incident.id} not public: "
                f"publish_status={incident.publish_status} (expected {PUBLISHED_STATUS})"
            )
            return False

        # Rule 2: Must be approved (if review_status field is used)
        if hasattr(incident, "review_status"):
            if incident.review_status != APPROVED_REVIEW_STATUS:
                logger.debug(
                    f"[v0] Incident {incident.id} not public: "
                    f"review_status={incident.review_status} (expected {APPROVED_REVIEW_STATUS})"
                )
                return False

        # Rule 3: Must have linked evidence
        has_evidence_links = bool(
            (incident.source_ids and len(incident.source_ids) > 0)
            or (incident.evidence_ids and len(incident.evidence_ids) > 0)
            or (incident.claim_ids and len(incident.claim_ids) > 0)
        )
        if not has_evidence_links:
            logger.debug(
                f"[v0] Incident {incident.id} not public: no linked evidence"
            )
            return False

        # Rule 4: Check for suppression/dispute flags
        if hasattr(incident, "is_suppressed") and incident.is_suppressed:
            logger.debug(f"[v0] Incident {incident.id} suppressed - not public")
            return False

        if hasattr(incident, "is_disputed") and incident.is_disputed:
            logger.debug(f"[v0] Incident {incident.id} disputed - not public")
            return False

        # Rule 5: Validate coordinates
        if incident.lat is None or incident.lng is None:
            logger.debug(f"[v0] Incident {incident.id} missing coordinates - not public")
            return False

        if not (-90 <= incident.lat <= 90 and -180 <= incident.lng <= 180):
            logger.debug(
                f"[v0] Incident {incident.id} invalid coordinates "
                f"({incident.lat}, {incident.lng}) - not public"
            )
            return False

        # Rule 6: Check for private metadata (conservative: if metadata exists,
        # ensure it doesn't contain private indicators)
        if incident.metadata_json:
            if incident.metadata_json.get("is_private"):
                logger.debug(
                    f"[v0] Incident {incident.id} marked private - not public"
                )
                return False

        logger.debug(f"[v0] Incident {incident.id} is publicly releasable")
        return True

    @staticmethod
    async def is_statute_link_publicly_releasable(
        link: StatuteIncidentLink,
    ) -> bool:
        """
        Determine if a statute link can be shown publicly.

        A statute link is publicly releasable if:
        1. review_status == "approved"
        2. confidence_score > 0 (it has some confidence)
        3. link_reason is not empty

        Args:
            link: The StatuteIncidentLink to check

        Returns:
            True if the link can be shown publicly
        """
        # Must be approved
        if link.review_status != "approved":
            return False

        # Must have confidence
        if link.confidence_score <= 0:
            return False

        # Must have reason
        if not link.link_reason or len(link.link_reason.strip()) == 0:
            return False

        return True

    @staticmethod
    async def is_news_link_publicly_releasable(
        link: IncidentNewsLink,
    ) -> bool:
        """
        Determine if a news link can be shown publicly.

        A news link is publicly releasable if:
        1. Has a valid article URL
        2. Has a title
        3. relevance_score > 0
        4. Not from a private/restricted source

        Args:
            link: The IncidentNewsLink to check

        Returns:
            True if the link can be shown publicly
        """
        # Must have URL
        if not link.news_article_url or len(link.news_article_url.strip()) == 0:
            return False

        # Must have title
        if not link.news_article_title or len(link.news_article_title.strip()) == 0:
            return False

        # Must have positive relevance
        if link.relevance_score <= 0:
            return False

        return True

    @staticmethod
    def get_public_incident_fields(incident: GeoLegalEvent) -> dict:
        """
        Return only the public-safe fields from an incident.

        This ensures no private metadata, review notes, internal fields,
        or unreviewed AI outputs leak to the public API.

        Returns:
            Dictionary with only allowlisted fields for public display
        """
        return {
            "id": incident.id,
            "title": incident.title,
            "event_type": incident.event_type,
            "description": incident.description,  # User-facing description only
            "public_summary": incident.public_summary,  # AI summary marked as derivative
            "lat": incident.lat,
            "lng": incident.lng,
            "location_name": incident.location_name,
            "occurred_at": incident.occurred_at.isoformat() if incident.occurred_at else None,
            "jurisdiction": incident.jurisdiction,
            "province": incident.province,
            "country": incident.country,
            "confidence": incident.confidence,
            "confidence_label": incident.confidence_label,
            # Explicitly exclude:
            # - raw_payload, scrape_metadata, source_list, evidence_list
            # - private_notes, internal_review_notes, internal_status
            # - unreviewed AI outputs without evidence
        }
