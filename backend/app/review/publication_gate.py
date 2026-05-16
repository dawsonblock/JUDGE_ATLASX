"""Gate that must pass before any record can be set is_public=True."""

from __future__ import annotations

from app.models.entities import CrimeIncident, LegalInstrument, ReviewItem
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
