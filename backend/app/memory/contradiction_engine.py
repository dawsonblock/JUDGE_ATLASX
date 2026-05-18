"""Contradiction engine for detecting conflicting claims.

Implements logic to detect contradictions between claims about the same entity.
Persist contradictions to database for durable tracking and review.
"""

import logging
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

from app.models.entities import (
    MemoryClaim,
    CanonicalEntity,
    MemoryContradiction,
    LegalSource,
)
from app.memory.source_authority import (
    get_source_authority_weight,
    calculate_authority_gap,
    should_supersede,
)

logger = logging.getLogger(__name__)


def detect_contradictions(
    entity_id: int, db: Session, persist: bool = True
) -> List[Dict[str, any]]:
    """Detect contradictions between claims for a given entity.

    Args:
        entity_id: ID of the entity to check
        db: Database session
        persist: Whether to persist contradictions to database

    Returns:
        List of contradiction dictionaries with details
    """
    # Get all active claims for the entity
    claims = (
        db.query(MemoryClaim)
        .filter(
            MemoryClaim.entity_id == entity_id,
            MemoryClaim.is_active == True,
            MemoryClaim.status == "active",
        )
        .all()
    )

    contradictions = []

    # Group claims by predicate
    claims_by_predicate: Dict[str, List[MemoryClaim]] = {}
    for claim in claims:
        predicate = claim.predicate or "unknown"
        if predicate not in claims_by_predicate:
            claims_by_predicate[predicate] = []
        claims_by_predicate[predicate].append(claim)

    # Check for contradictions within each predicate group
    for predicate, predicate_claims in claims_by_predicate.items():
        if len(predicate_claims) < 2:
            continue

        # Check for value contradictions
        for i, claim1 in enumerate(predicate_claims):
            for claim2 in predicate_claims[i + 1 :]:
                contradiction = _check_value_contradiction(claim1, claim2, db)
                if contradiction:
                    contradictions.append(contradiction)
                    if persist:
                        _persist_contradiction(contradiction, db)

        # Check for temporal contradictions
        for i, claim1 in enumerate(predicate_claims):
            for claim2 in predicate_claims[i + 1 :]:
                contradiction = _check_temporal_contradiction(claim1, claim2, db)
                if contradiction:
                    contradictions.append(contradiction)
                    if persist:
                        _persist_contradiction(contradiction, db)

    return contradictions


def _persist_contradiction(
    contradiction: Dict[str, any], db: Session
) -> Optional[MemoryContradiction]:
    """Persist a contradiction to the database.

    Args:
        contradiction: Contradiction dictionary
        db: Database session

    Returns:
        Created or existing MemoryContradiction, None if failed
    """
    # Check if contradiction already exists (prevent duplicates)
    # Check both orderings to account for claim_a_id/claim_b_id vs claim_b_id/claim_a_id
    claim1_id = contradiction["claim1_id"]
    claim2_id = contradiction["claim2_id"]
    conflict_type = contradiction["type"]

    existing = (
        db.query(MemoryContradiction)
        .filter(
            (
                (MemoryContradiction.claim_a_id == claim1_id)
                & (MemoryContradiction.claim_b_id == claim2_id)
            )
            | (
                (MemoryContradiction.claim_a_id == claim2_id)
                & (MemoryContradiction.claim_b_id == claim1_id)
            ),
            MemoryContradiction.conflict_type == conflict_type,
        )
        .first()
    )

    if existing:
        return existing

    # Calculate source authority weight for the contradiction
    claim1 = db.query(MemoryClaim).filter(MemoryClaim.id == claim1_id).first()
    claim2 = db.query(MemoryClaim).filter(MemoryClaim.id == claim2_id).first()

    source1 = None
    source2 = None
    if claim1 and claim1.source_id:
        source1 = db.query(LegalSource).filter(LegalSource.id == claim1.source_id).first()
    if claim2 and claim2.source_id:
        source2 = db.query(LegalSource).filter(LegalSource.id == claim2.source_id).first()

    weight1 = get_source_authority_weight(source1.source_type if source1 else None)
    weight2 = get_source_authority_weight(source2.source_type if source2 else None)
    # Use the higher authority weight for the contradiction
    authority_weight = max(weight1, weight2)

    # Create new contradiction record
    new_contradiction = MemoryContradiction(
        claim_a_id=claim1_id,
        claim_b_id=claim2_id,
        conflict_type=conflict_type,
        severity=contradiction.get("severity", "medium"),
        status="open",
        detected_by="system",
        detected_at=datetime.now(timezone.utc),
        source_authority_weight=authority_weight,
    )
    db.add(new_contradiction)

    try:
        # Increment contradiction counts on both claims
        if claim1:
            claim1.contradiction_count += 1
        else:
            logger.warning(
                "Claim %d not found when persisting contradiction",
                claim1_id
            )
        if claim2:
            claim2.contradiction_count += 1
        else:
            logger.warning(
                "Claim %d not found when persisting contradiction",
                claim2_id
            )

        db.commit()
        logger.info(
            "Persisted contradiction between claims %d and %d (type: %s, authority_weight: %.2f)",
            claim1_id,
            claim2_id,
            conflict_type,
            authority_weight,
        )

        return new_contradiction
    except IntegrityError:
        # Handle race condition where another process inserted the same contradiction
        db.rollback()
        # Query again to get the existing record
        existing = (
            db.query(MemoryContradiction)
            .filter(
                (
                    (MemoryContradiction.claim_a_id == claim1_id)
                    & (MemoryContradiction.claim_b_id == claim2_id)
                )
                | (
                    (MemoryContradiction.claim_a_id == claim2_id)
                    & (MemoryContradiction.claim_b_id == claim1_id)
                ),
                MemoryContradiction.conflict_type == conflict_type,
            )
            .first()
        )
        if existing:
            logger.info(
                "Contradiction already exists between claims %d and %d (type: %s)",
                claim1_id,
                claim2_id,
                conflict_type,
            )
            return existing
        logger.error(
            "Failed to find contradiction after IntegrityError rollback for claims %d and %d (type: %s)",
            claim1_id,
            claim2_id,
            conflict_type,
        )
        return None


def _calculate_severity(
    contradiction_type: str,
    claim1: MemoryClaim,
    claim2: MemoryClaim,
    db: Session,
) -> str:
    """Calculate contradiction severity based on multiple factors.

    Severity calculation considers:
    - Contradiction type (value vs temporal)
    - Source authority weight (higher authority = higher severity)
    - Confidence scores (higher confidence = higher severity)
    - Claim count (contradictions affecting more claims = higher severity)

    Args:
        contradiction_type: Type of contradiction (value_contradiction, temporal_contradiction)
        claim1: First claim
        claim2: Second claim
        db: Database session

    Returns:
        Severity level (low, medium, high, critical)
    """
    # Get source authority weights
    source1 = None
    source2 = None
    if claim1.source_snapshot_id:
        from app.models.entities import SourceSnapshot
        snapshot1 = db.query(SourceSnapshot).filter(
            SourceSnapshot.id == claim1.source_snapshot_id
        ).first()
        if snapshot1:
            source1 = db.query(LegalSource).filter(
                LegalSource.id == snapshot1.source_id
            ).first()
    if claim2.source_snapshot_id:
        from app.models.entities import SourceSnapshot
        snapshot2 = db.query(SourceSnapshot).filter(
            SourceSnapshot.id == claim2.source_snapshot_id
        ).first()
        if snapshot2:
            source2 = db.query(LegalSource).filter(
                LegalSource.id == snapshot2.source_id
            ).first()

    weight1 = get_source_authority_weight(source1.source_type if source1 else None)
    weight2 = get_source_authority_weight(source2.source_type if source2 else None)
    max_authority = max(weight1, weight2)

    # Base severity from contradiction type
    base_severity = {
        "value_contradiction": 0.5,
        "temporal_contradiction": 0.3,
    }.get(contradiction_type, 0.4)

    # Adjust by source authority (higher authority = higher severity)
    authority_factor = max_authority  # 0.0-1.0

    # Adjust by claim confidence (higher confidence = higher severity)
    confidence_factor = max(claim1.confidence or 0.5, claim2.confidence or 0.5)

    # Adjust by entity importance (critical entities = higher severity)
    entity_importance_factor = 1.0
    if claim1.entity_id:
        entity = db.query(CanonicalEntity).filter(CanonicalEntity.id == claim1.entity_id).first()
        if entity and entity.entity_type in ["person", "organization"]:
            entity_importance_factor = 1.2

    # Calculate final severity (0.0-1.0)
    final_severity = base_severity * authority_factor * confidence_factor * entity_importance_factor
    final_severity = min(final_severity, 1.0)  # Cap at 1.0

    # Map to severity levels
    if final_severity >= 0.8:
        return "critical"
    elif final_severity >= 0.5:
        return "high"
    elif final_severity >= 0.3:
        return "medium"
    else:
        return "low"


def _check_value_contradiction(
    claim1: MemoryClaim, claim2: MemoryClaim, db: Session
) -> Optional[Dict[str, any]]:
    """Check if two claims have contradictory values.

    Args:
        claim1: First claim
        claim2: Second claim

    Returns:
        Contradiction dict if found, None otherwise
    """
    # Skip if values are the same
    if claim1.normalized_value == claim2.normalized_value:
        return None

    # Skip if either claim lacks normalized value
    if not claim1.normalized_value or not claim2.normalized_value:
        return None

    # Check for explicit contradictions based on value type
    if claim1.object_value_type == "boolean" and claim2.object_value_type == "boolean":
        val1 = claim1.normalized_value.lower()
        val2 = claim2.normalized_value.lower()
        if (val1 == "true" and val2 == "false") or (val1 == "false" and val2 == "true"):
            severity = _calculate_severity("value_contradiction", claim1, claim2, db)
            return {
                "type": "value_contradiction",
                "claim1_id": claim1.id,
                "claim2_id": claim2.id,
                "predicate": claim1.predicate,
                "value1": claim1.normalized_value,
                "value2": claim2.normalized_value,
                "severity": severity,
            }

    # Check for numeric contradictions (significant difference)
    if claim1.object_value_type == "number" and claim2.object_value_type == "number":
        try:
            num1 = float(claim1.normalized_value)
            num2 = float(claim2.normalized_value)
            # If values differ by more than 10%, consider it a contradiction
            if num1 > 0 and abs(num1 - num2) / num1 > 0.1:
                severity = _calculate_severity("value_contradiction", claim1, claim2, db)
                return {
                    "type": "value_contradiction",
                    "claim1_id": claim1.id,
                    "claim2_id": claim2.id,
                    "predicate": claim1.predicate,
                    "value1": claim1.normalized_value,
                    "value2": claim2.normalized_value,
                    "severity": severity,
                }
        except (ValueError, TypeError):
            pass

    return None


def _check_temporal_contradiction(
    claim1: MemoryClaim, claim2: MemoryClaim, db: Session
) -> Optional[Dict[str, any]]:
    """Check if two claims have contradictory temporal validity.

    Args:
        claim1: First claim
        claim2: Second claim

    Returns:
        Contradiction dict if found, None otherwise
    """
    # Skip if either claim lacks temporal validity
    if not claim1.valid_from or not claim2.valid_from:
        return None

    # Check if validity periods don't overlap but should
    if claim1.valid_to and claim2.valid_from:
        if claim1.valid_to < claim2.valid_from:
            return None  # No overlap, not a contradiction

    # Check if claims have conflicting validity for the same time period
    if claim1.valid_from == claim2.valid_from:
        if claim1.normalized_value != claim2.normalized_value:
            severity = _calculate_severity("temporal_contradiction", claim1, claim2, db)
            return {
                "type": "temporal_contradiction",
                "claim1_id": claim1.id,
                "claim2_id": claim2.id,
                "predicate": claim1.predicate,
                "valid_from": str(claim1.valid_from),
                "value1": claim1.normalized_value,
                "value2": claim2.normalized_value,
                "severity": severity,
            }

    return None


def update_contradiction_counts(db: Session) -> int:
    """Update contradiction counts for all entities.

    Args:
        db: Database session

    Returns:
        Number of entities with contradictions
    """
    entities = db.query(CanonicalEntity).all()
    entities_with_contradictions = 0

    for entity in entities:
        contradictions = detect_contradictions(entity.id, db)
        contradiction_count = len(contradictions)

        # Update contradiction counts for all claims on this entity
        claims = (
            db.query(MemoryClaim)
            .filter(MemoryClaim.entity_id == entity.id)
            .all()
        )
        for claim in claims:
            claim.contradiction_count = contradiction_count

        if contradiction_count > 0:
            entities_with_contradictions += 1

    db.commit()
    logger.info(
        "Updated contradiction counts for %d entities",
        entities_with_contradictions,
    )

    return entities_with_contradictions


def resolve_contradiction(
    claim_id: int, resolution: str, db: Session
) -> bool:
    """Resolve a contradiction by marking the claim as superseded.

    Args:
        claim_id: ID of the claim to resolve
        resolution: Resolution type (supersede, invalidate, retain)
        db: Database session

    Returns:
        True if resolution succeeded, False otherwise
    """
    claim = db.query(MemoryClaim).filter(MemoryClaim.id == claim_id).first()
    if not claim:
        logger.warning("Claim %d not found for contradiction resolution", claim_id)
        return False

    if resolution == "supersede":
        claim.status = "superseded"
        claim.is_active = False
        claim.invalidation_reason = "Contradiction resolved by supersession"
        claim.invalidated_at = claim.updated_at
    elif resolution == "invalidate":
        claim.status = "invalid"
        claim.is_active = False
        claim.invalidation_reason = "Contradiction resolved by invalidation"
        claim.invalidated_at = claim.updated_at
    elif resolution == "retain":
        # Keep the claim active, update contradiction count
        pass
    else:
        logger.warning("Invalid resolution type: %s", resolution)
        return False

    db.commit()
    logger.info(
        "Resolved contradiction for claim %d with resolution: %s",
        claim_id,
        resolution,
    )

    # Update contradiction counts for the entity
    update_contradiction_counts(db)

    return True


def auto_supersede_by_authority(contradiction_id: int, db: Session) -> bool:
    """Automatically supersede lower-authority claim in a contradiction.

    If one claim has significantly higher source authority than the other,
    automatically supersede the lower-authority claim.

    Args:
        contradiction_id: ID of the contradiction record
        db: Database session

    Returns:
        True if supersession succeeded, False otherwise
    """
    contradiction = (
        db.query(MemoryContradiction)
        .filter(MemoryContradiction.id == contradiction_id)
        .first()
    )

    if not contradiction:
        logger.warning("Contradiction %d not found for auto-supersession", contradiction_id)
        return False

    # Get both claims
    claim_a = db.query(MemoryClaim).filter(
        MemoryClaim.id == contradiction.claim_a_id
    ).first()
    claim_b = db.query(MemoryClaim).filter(
        MemoryClaim.id == contradiction.claim_b_id
    ).first()

    if not claim_a or not claim_b:
        logger.warning("Claims not found for contradiction %d", contradiction_id)
        return False

    # Get source authority weights
    source_a = None
    source_b = None
    if claim_a.source_snapshot_id:
        from app.models.entities import SourceSnapshot
        snapshot_a = db.query(SourceSnapshot).filter(
            SourceSnapshot.id == claim_a.source_snapshot_id
        ).first()
        if snapshot_a:
            source_a = db.query(LegalSource).filter(
                LegalSource.id == snapshot_a.source_id
            ).first()
    if claim_b.source_snapshot_id:
        from app.models.entities import SourceSnapshot
        snapshot_b = db.query(SourceSnapshot).filter(
            SourceSnapshot.id == claim_b.source_snapshot_id
        ).first()
        if snapshot_b:
            source_b = db.query(LegalSource).filter(
                LegalSource.id == snapshot_b.source_id
            ).first()

    weight_a = get_source_authority_weight(source_a.source_type if source_a else None)
    weight_b = get_source_authority_weight(source_b.source_type if source_b else None)

    # Only auto-supersede if authority difference is significant (>0.3)
    authority_threshold = 0.3
    if abs(weight_a - weight_b) < authority_threshold:
        logger.info(
            "Authority difference too small for auto-supersesion: %.2f vs %.2f",
            weight_a, weight_b
        )
        return False

    # Determine which claim to supersede (lower authority)
    if weight_a > weight_b:
        claim_to_supersede = claim_b
        retained_claim = claim_a
    else:
        claim_to_supersede = claim_a
        retained_claim = claim_b

    # Supersede the lower-authority claim
    claim_to_supersede.status = "superseded"
    claim_to_supersede.is_active = False
    claim_to_supersede.invalidation_reason = f"Auto-superseded by higher-authority claim {retained_claim.id} (authority: {max(weight_a, weight_b):.2f} vs {min(weight_a, weight_b):.2f})"
    claim_to_supersede.invalidated_at = datetime.now(timezone.utc)
    claim_to_supersede.superseded_by_claim_id = retained_claim.id

    # Mark contradiction as resolved
    contradiction.status = "resolved"
    contradiction.resolved_at = datetime.now(timezone.utc)
    contradiction.resolution_note = f"Auto-resolved by authority-based supersession"

    db.commit()
    logger.info(
        "Auto-superseded claim %d by claim %d (authority: %.2f vs %.2f)",
        claim_to_supersede.id,
        retained_claim.id,
        weight_a,
        weight_b,
    )

    return True


def get_open_contradictions_by_claim(
    claim_id: int, db: Session
) -> List[MemoryContradiction]:
    """Get open contradictions for a specific claim.

    Args:
        claim_id: ID of the claim
        db: Database session

    Returns:
        List of open MemoryContradiction records
    """
    contradictions = (
        db.query(MemoryContradiction)
        .filter(
            (MemoryContradiction.claim_a_id == claim_id)
            | (MemoryContradiction.claim_b_id == claim_id),
            MemoryContradiction.status == "open",
        )
        .all()
    )
    return contradictions


def get_open_contradictions_by_entity(
    entity_id: int, db: Session
) -> List[MemoryContradiction]:
    """Get open contradictions for all claims on an entity.

    Args:
        entity_id: ID of the entity
        db: Database session

    Returns:
        List of open MemoryContradiction records
    """
    # Get all claims for the entity
    claim_ids = (
        db.query(MemoryClaim.id)
        .filter(MemoryClaim.entity_id == entity_id)
        .all()
    )
    claim_ids = [c[0] for c in claim_ids]

    if not claim_ids:
        return []

    # Get contradictions involving these claims
    contradictions = (
        db.query(MemoryContradiction)
        .filter(
            (MemoryContradiction.claim_a_id.in_(claim_ids))
            | (MemoryContradiction.claim_b_id.in_(claim_ids)),
            MemoryContradiction.status == "open",
        )
        .all()
    )
    return contradictions


def resolve_contradiction_record(
    contradiction_id: int,
    status: str,
    reviewer_id: int,
    resolution_note: str,
    db: Session,
) -> bool:
    """Resolve a contradiction record with reviewer action.

    Args:
        contradiction_id: ID of the contradiction record
        status: New status (resolved, false_positive, ignored)
        reviewer_id: ID of the reviewer
        resolution_note: Optional note about the resolution
        db: Database session

    Returns:
        True if resolution succeeded, False otherwise
    """
    contradiction = (
        db.query(MemoryContradiction)
        .filter(MemoryContradiction.id == contradiction_id)
        .first()
    )

    if not contradiction:
        logger.warning("Contradiction %d not found for resolution", contradiction_id)
        return False

    contradiction.status = status
    # Only set resolved_at for actual resolutions, not ignored
    if status != "ignored":
        contradiction.resolved_at = datetime.now(timezone.utc)
    contradiction.reviewer_id = reviewer_id
    contradiction.resolution_note = resolution_note
    contradiction.updated_at = datetime.now(timezone.utc)

    # Decrement contradiction counts on both claims
    claim_a = db.query(MemoryClaim).filter(
        MemoryClaim.id == contradiction.claim_a_id
    ).first()
    claim_b = db.query(MemoryClaim).filter(
        MemoryClaim.id == contradiction.claim_b_id
    ).first()

    if claim_a and claim_a.contradiction_count > 0:
        claim_a.contradiction_count -= 1
    if claim_b and claim_b.contradiction_count > 0:
        claim_b.contradiction_count -= 1

    db.commit()
    logger.info(
        "Resolved contradiction record %d with status: %s by reviewer %d",
        contradiction_id,
        status,
        reviewer_id,
    )

    return True
