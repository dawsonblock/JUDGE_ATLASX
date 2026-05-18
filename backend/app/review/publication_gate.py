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
    - No open high/critical contradictions
    - Claim status is not disputed/rejected/superseded
    - Private-person allegations have review
    - Source is not deprecated/quarantined
    """
    # Check review status
    if claim.review_status != "approved":
        raise PublicationBlockedError(
            f"MemoryClaim {claim.id} review_status='{claim.review_status}' — must be 'approved'"
        )

    # Check claim status
    if claim.status in ["disputed", "rejected", "superseded", "invalid"]:
        raise PublicationBlockedError(
            f"MemoryClaim {claim.id} status='{claim.status}' — cannot publish disputed/rejected/superseded claims"
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

    # Check for open high/critical contradictions using durable system
    from app.memory.contradiction_engine import get_open_contradictions_by_claim

    open_contradictions = get_open_contradictions_by_claim(claim.id, db)
    high_critical_contradictions = [
        c for c in open_contradictions
        if c.severity in ["high", "critical"]
    ]

    if high_critical_contradictions:
        raise PublicationBlockedError(
            f"MemoryClaim {claim.id} has {len(high_critical_contradictions)} open high/critical contradictions"
        )

    # Check private-person allegations have review
    if claim.claim_type == "criminal_allegation":
        # Check if the claim involves a named private person
        if claim.object_entity_id:
            from app.models.entities import CanonicalEntity

            entity = db.query(CanonicalEntity).filter(
                CanonicalEntity.id == claim.object_entity_id
            ).first()
            if entity and entity.entity_type == "person":
                # Private person allegation requires explicit review approval
                # Note: review_status is already checked at line 86, so this block
                # only executes if review_status == "approved" from the outer check
                raise PublicationBlockedError(
                    f"MemoryClaim {claim.id} is a criminal allegation involving a named person - requires manual review approval"
                )

    # Check source status if available
    if claim.extraction_run_id:
        from app.models.entities import IngestionRun, LegalSource

        ingestion_run = db.query(IngestionRun).filter(
            IngestionRun.id == claim.extraction_run_id
        ).first()
        if ingestion_run:
            source = db.query(LegalSource).filter(
                LegalSource.id == ingestion_run.source_id
            ).first()
            if source and source.lifecycle_state in ["deprecated", "quarantined"]:
                raise PublicationBlockedError(
                    f"MemoryClaim {claim.id} source '{source.source_id}' is {source.lifecycle_state} — cannot publish"
                )
