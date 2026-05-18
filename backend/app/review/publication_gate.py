"""Gate that must pass before any record can be set is_public=True."""

from __future__ import annotations

from app.models.entities import CrimeIncident, LegalInstrument, ReviewItem, MemoryClaim
from app.policies.publication_policy import can_publish_entity, entity_public_visibility
from app.policies.state_model import (
    ReviewQueueDecision,
    normalize_review_queue_decision,
)
from sqlalchemy.orm import Session, object_session


class PublicationBlockedError(ValueError):
    """Raised when a record cannot be published due to unmet requirements."""


def assert_publication_ready(incident: CrimeIncident, db: Session) -> None:
    """Raise PublicationBlockedError if the incident may not be published.

    Domain entity publication means review_status + public visibility +
    evidence gate.  ReviewItem ``approved`` is not accepted here.
    """
    decision = can_publish_entity(db, "crime_incident", incident)
    if not decision.allowed:
        raise PublicationBlockedError(
            f"Incident {incident.id} blocked: {'; '.join(decision.reasons)}"
        )


def assert_review_item_publication_ready(item: ReviewItem) -> None:
    """Raise PublicationBlockedError if the ReviewItem has not been approved.

    ReviewItem uses a workflow ``status`` field (not ``review_status``), so
    this assert is intentionally separate from :func:`can_publish`.
    """
    if normalize_review_queue_decision(item.status) != ReviewQueueDecision.APPROVED:
        raise PublicationBlockedError(
            f"ReviewItem {item.id} status='{item.status}' — must be 'approved'"
        )
    if not item.source_snapshot_id:
        raise PublicationBlockedError(
            f"ReviewItem {item.id} has no source_snapshot_id — evidence link required"
        )


def assert_legal_instrument_publication_ready(
    instrument: LegalInstrument,
    db: Session | None = None,
) -> None:
    """Raise PublicationBlockedError if a legal instrument is not publication-ready.

    Delegates to the canonical policy.  ReviewItem ``approved`` is an
    internal workflow state and never a LegalInstrument.review_status.
    """
    db = db or object_session(instrument)
    if db is None:
        raise PublicationBlockedError(
            "LegalInstrument publication requires a database session"
        )
    decision = can_publish_entity(db, "legal_instrument", instrument)
    if not decision.allowed:
        raise PublicationBlockedError(
            f"LegalInstrument {instrument.id} blocked: {'; '.join(decision.reasons)}"
        )
    if not entity_public_visibility(instrument):
        raise PublicationBlockedError(
            f"LegalInstrument {instrument.id} public_visibility="
            f"'{instrument.public_visibility}' — must be 'public'"
        )


def assert_memory_claim_publication_ready(claim: MemoryClaim, db: Session) -> None:
    """Raise PublicationBlockedError if a memory claim is not publication-ready.

    Memory claims require:
    - review_status = approved
    - At least one supporting evidence link
    - Confidence above threshold (0.7)
    - No unresolved contradictions
    """
    # Check review status
    if claim.review_status != "approved":
        raise PublicationBlockedError(
            f"MemoryClaim {claim.id} review_status='{claim.review_status}' — must be 'approved'"
        )

    # Check evidence
    from app.models.entities import MemoryEvidenceLink

    supporting_evidence = (
        db.query(MemoryEvidenceLink)
        .filter(
            MemoryEvidenceLink.claim_id == claim.id,
            MemoryEvidenceLink.support_type == "supports",
        )
        .count()
    )
    if supporting_evidence == 0:
        raise PublicationBlockedError(
            f"MemoryClaim {claim.id} has no supporting evidence links"
        )

    # Check confidence
    if claim.confidence < 0.7:
        raise PublicationBlockedError(
            f"MemoryClaim {claim.id} confidence={claim.confidence} — must be >= 0.7"
        )

    # Check contradictions
    if claim.contradiction_count > 0:
        raise PublicationBlockedError(
            f"MemoryClaim {claim.id} has {claim.contradiction_count} unresolved contradictions"
        )
