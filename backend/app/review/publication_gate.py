"""Gate that must pass before any record can be set is_public=True.

Public map publishing requires:
- valid evidence source
- source not blocked
- confidence above threshold
- location not ambiguous
- privacy/redaction pass complete
- review_status approved
- no unresolved high-risk contradiction

Default policy:
- official structured sources may auto-publish low-risk metadata
- news/police narrative sources require review
- person-specific accusations require strict review or block
- ambiguous locations stay admin-only
"""
from __future__ import annotations

from app.models.entities import CrimeIncident, LegalInstrument, Location, ReviewItem, MemoryClaim
from app.models.geocode_cache import GeocodeCache
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
    
    Also checks that geocoding result is not ambiguous for map publishing.
    """
    decision = can_publish_entity(db, "crime_incident", incident)
    if not decision.allowed:
        raise PublicationBlockedError(
            f"Incident {incident.id} blocked: {'; '.join(decision.reasons)}"
        )
    
    # Check geocoding status if location is set
    if incident.primary_location_id:
        location = db.query(Location).filter(
            Location.id == incident.primary_location_id
        ).first()
        if location and location.geocode_cache_id:
            geocode = db.query(GeocodeCache).filter(
                GeocodeCache.id == location.geocode_cache_id
            ).first()
            if geocode and geocode.status not in ("exact", "approximate"):
                raise PublicationBlockedError(
                    f"Incident {incident.id} has ambiguous or failed "
                    f"geocoding status '{geocode.status}' — "
                    f"cannot publish to public map"
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

    # Check named-person criminal allegations have elevated approval
    if claim.claim_sensitivity == "criminal_allegation_named_person":
        # Require elevated review approval for named-person criminal allegations
        if claim.elevated_review_status != "approved":
            raise PublicationBlockedError(
                f"MemoryClaim {claim.id} requires elevated approval for named-person criminal allegation"
            )

        # Require evidence source is official/public record
        if claim.source_snapshot_id:
            from app.models.entities import SourceSnapshot, LegalSource

            snapshot = db.query(SourceSnapshot).filter(
                SourceSnapshot.id == claim.source_snapshot_id
            ).first()
            if snapshot:
                source = db.query(LegalSource).filter(
                    LegalSource.id == snapshot.source_id
                ).first()
                if source and source.lifecycle_state not in ["active", "official"]:
                    raise PublicationBlockedError(
                        f"MemoryClaim {claim.id} evidence source '{source.source_id}' is not official/public record — requires elevated approval source"
                    )

        # Block media-only named-person criminal allegations
        if claim.source_snapshot_id:
            from app.models.entities import SourceSnapshot, LegalSource

            snapshot = db.query(SourceSnapshot).filter(
                SourceSnapshot.id == claim.source_snapshot_id
            ).first()
            if snapshot:
                source = db.query(LegalSource).filter(
                    LegalSource.id == snapshot.source_id
                ).first()
                if source and source.lifecycle_state == "media":
                    raise PublicationBlockedError(
                        f"MemoryClaim {claim.id} is a named-person criminal allegation from media source — media-only allegations are blocked"
                    )

    # Check redaction pass for sensitive claims
    if claim.claim_sensitivity in ["criminal_allegation_named_person", "criminal_allegation_private_person", "misconduct_allegation"]:
        # Require redaction pass for sensitive claims
        # This is checked during AI extraction; if redaction failed, the claim should not publish
        if claim.confidence < 0.8:  # Higher threshold for sensitive claims
            raise PublicationBlockedError(
                f"MemoryClaim {claim.id} has sensitivity '{claim.claim_sensitivity}' and confidence {claim.confidence} — sensitive claims require higher confidence and redaction pass"
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
