"""Contradiction engine for detecting conflicting claims.

Implements logic to detect contradictions between claims about the same entity.
"""

import logging
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from app.models.entities import MemoryClaim, CanonicalEntity

logger = logging.getLogger(__name__)


def detect_contradictions(
    entity_id: int, db: Session
) -> List[Dict[str, any]]:
    """Detect contradictions between claims for a given entity.

    Args:
        entity_id: ID of the entity to check
        db: Database session

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
                contradiction = _check_value_contradiction(claim1, claim2)
                if contradiction:
                    contradictions.append(contradiction)

        # Check for temporal contradictions
        for i, claim1 in enumerate(predicate_claims):
            for claim2 in predicate_claims[i + 1 :]:
                contradiction = _check_temporal_contradiction(claim1, claim2)
                if contradiction:
                    contradictions.append(contradiction)

    return contradictions


def _check_value_contradiction(
    claim1: MemoryClaim, claim2: MemoryClaim
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
            return {
                "type": "value_contradiction",
                "claim1_id": claim1.id,
                "claim2_id": claim2.id,
                "predicate": claim1.predicate,
                "value1": claim1.normalized_value,
                "value2": claim2.normalized_value,
                "severity": "high",
            }

    # Check for numeric contradictions (significant difference)
    if claim1.object_value_type == "number" and claim2.object_value_type == "number":
        try:
            num1 = float(claim1.normalized_value)
            num2 = float(claim2.normalized_value)
            # If values differ by more than 10%, consider it a contradiction
            if num1 > 0 and abs(num1 - num2) / num1 > 0.1:
                return {
                    "type": "value_contradiction",
                    "claim1_id": claim1.id,
                    "claim2_id": claim2.id,
                    "predicate": claim1.predicate,
                    "value1": claim1.normalized_value,
                    "value2": claim2.normalized_value,
                    "severity": "medium",
                }
        except (ValueError, TypeError):
            pass

    return None


def _check_temporal_contradiction(
    claim1: MemoryClaim, claim2: MemoryClaim
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
            return {
                "type": "temporal_contradiction",
                "claim1_id": claim1.id,
                "claim2_id": claim2.id,
                "predicate": claim1.predicate,
                "valid_from": str(claim1.valid_from),
                "value1": claim1.normalized_value,
                "value2": claim2.normalized_value,
                "severity": "medium",
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
