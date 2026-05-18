"""Risk-tiered review system for prioritizing review tasks.

Implements risk tier calculation based on confidence, contradictions,
and evidence, with tier-based review requirements.
"""

import logging
from typing import Dict, Optional
from sqlalchemy.orm import Session

from app.models.entities import MemoryClaim, CanonicalEntity

logger = logging.getLogger(__name__)

# Risk tier thresholds
RISK_TIERS = {
    "critical": 0.0,  # High risk, requires immediate review
    "high": 0.3,  # High risk, requires review
    "medium": 0.6,  # Medium risk, requires review
    "low": 0.8,  # Low risk, may be auto-approved
}

# Review requirements per tier
REVIEW_REQUIREMENTS = {
    "critical": {"requires_review": True, "requires_evidence": True, "auto_approve": False},
    "high": {"requires_review": True, "requires_evidence": True, "auto_approve": False},
    "medium": {"requires_review": True, "requires_evidence": False, "auto_approve": False},
    "low": {"requires_review": False, "requires_evidence": False, "auto_approve": True},
}


def calculate_claim_risk_tier(claim_id: int, db: Session) -> str:
    """Calculate risk tier for a claim.

    Args:
        claim_id: ID of the claim
        db: Database session

    Returns:
        Risk tier: critical, high, medium, or low
    """
    claim = db.query(MemoryClaim).filter(MemoryClaim.id == claim_id).first()
    if not claim:
        logger.warning("Claim %d not found for risk tier calculation", claim_id)
        return "high"  # Default to high risk for unknown claims

    # Base risk from confidence (lower confidence = higher risk)
    confidence_risk = 1.0 - claim.confidence

    # Risk from contradictions
    contradiction_risk = min(0.3, (claim.contradiction_count or 0) * 0.1)

    # Risk from lack of evidence
    evidence_risk = 0.0
    if claim.corroboration_count == 0:
        evidence_risk = 0.2
    elif claim.corroboration_count == 1:
        evidence_risk = 0.1

    # Calculate total risk score
    total_risk = confidence_risk + contradiction_risk + evidence_risk
    total_risk = min(1.0, total_risk)  # Cap at 1.0

    # Determine tier
    if total_risk <= RISK_TIERS["low"]:
        tier = "low"
    elif total_risk <= RISK_TIERS["medium"]:
        tier = "medium"
    elif total_risk <= RISK_TIERS["high"]:
        tier = "high"
    else:
        tier = "critical"

    logger.debug(
        "Risk tier for claim %d: %s (confidence=%.2f, contradictions=%d, corroboration=%d)",
        claim_id,
        tier,
        claim.confidence,
        claim.contradiction_count,
        claim.corroboration_count,
    )

    return tier


def get_review_requirements(risk_tier: str) -> Dict[str, bool]:
    """Get review requirements for a risk tier.

    Args:
        risk_tier: Risk tier (critical, high, medium, low)

    Returns:
        Dictionary with review requirement flags
    """
    return REVIEW_REQUIREMENTS.get(risk_tier, REVIEW_REQUIREMENTS["high"])


def can_auto_approve(claim_id: int, db: Session) -> bool:
    """Check if a claim can be auto-approved based on risk tier.

    Args:
        claim_id: ID of the claim
        db: Database session

    Returns:
        True if auto-approval is allowed, False otherwise
    """
    risk_tier = calculate_claim_risk_tier(claim_id, db)
    requirements = get_review_requirements(risk_tier)
    return requirements["auto_approve"]


def calculate_entity_risk_tier(entity_id: int, db: Session) -> str:
    """Calculate risk tier for an entity based on its claims.

    Args:
        entity_id: ID of the entity
        db: Database session

    Returns:
        Risk tier: critical, high, medium, or low
    """
    claims = (
        db.query(MemoryClaim)
        .filter(
            MemoryClaim.entity_id == entity_id,
            MemoryClaim.is_active == True,
        )
        .all()
    )

    if not claims:
        return "low"

    # Calculate risk for each claim
    risk_scores = []
    for claim in claims:
        risk_tier = calculate_claim_risk_tier(claim.id, db)
        # Convert tier to numeric score
        tier_scores = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
        risk_scores.append(tier_scores.get(risk_tier, 0.75))

    # Entity risk is the maximum of its claims' risks
    max_risk = max(risk_scores) if risk_scores else 0.75

    # Convert back to tier
    if max_risk <= RISK_TIERS["low"]:
        return "low"
    elif max_risk <= RISK_TIERS["medium"]:
        return "medium"
    elif max_risk <= RISK_TIERS["high"]:
        return "high"
    else:
        return "critical"


def batch_calculate_risk_tiers(entity_id: int, db: Session) -> Dict[int, str]:
    """Calculate risk tiers for all claims on an entity.

    Args:
        entity_id: ID of the entity
        db: Database session

    Returns:
        Dictionary mapping claim IDs to risk tiers
    """
    claims = (
        db.query(MemoryClaim)
        .filter(
            MemoryClaim.entity_id == entity_id,
            MemoryClaim.is_active == True,
        )
        .all()
    )

    risk_tiers = {}
    for claim in claims:
        risk_tiers[claim.id] = calculate_claim_risk_tier(claim.id, db)

    logger.info("Calculated risk tiers for %d claims on entity %d", len(risk_tiers), entity_id)
    return risk_tiers
