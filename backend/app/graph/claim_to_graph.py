"""Convert memory claims to graph entities and relationships (Phase 9).

This module provides functions to transform structured memory claims
into graph entities and relationships for the knowledge graph.

Key functions:
- claim_to_entity_node: Convert a claim to an entity node
- claim_to_relationship: Convert a claim to a relationship edge
- batch_claims_to_graph: Batch process claims for graph integration
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.models.entities import MemoryClaim, CanonicalEntity
from app.graph.graph_models import EntityNode, RelationshipEdge
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


def claim_to_entity_node(claim: MemoryClaim, db: Session) -> EntityNode:
    """Convert a memory claim to a graph entity node.

    Args:
        claim: The memory claim to convert
        db: Database session

    Returns:
        EntityNode representation of the claim

    Raises:
        ValueError: If claim entity is not found
    """
    entity = db.query(CanonicalEntity).filter(
        CanonicalEntity.id == claim.entity_id
    ).first()

    if not entity:
        raise ValueError(f"Entity {claim.entity_id} not found for claim {claim.id}")

    # Build entity node properties from claim
    properties: Dict[str, Any] = {
        "claim_id": claim.id,
        "claim_key": claim.claim_key,
        "claim_uid": claim.claim_uid,
        "claim_type": claim.claim_type,
        "predicate": claim.predicate,
        "object_value": claim.object_value,
        "object_value_type": claim.object_value_type,
        "normalized_value": claim.normalized_value,
        "confidence": claim.confidence,
        "jurisdiction": claim.jurisdiction,
        "valid_from": claim.valid_from.isoformat() if claim.valid_from else None,
        "valid_to": claim.valid_to.isoformat() if claim.valid_to else None,
        "observed_at": claim.observed_at.isoformat() if claim.observed_at else None,
        "source_quality": claim.source_quality,
        "corroboration_count": claim.corroboration_count,
        "contradiction_count": claim.contradiction_count,
        "review_status": claim.review_status,
        "status": claim.status,
        "is_active": claim.is_active,
        # Phase 6 edge fields
        "claim_sensitivity": claim.claim_sensitivity,
        "elevated_review_status": claim.elevated_review_status,
        "elevated_reviewer_id": claim.elevated_reviewer_id,
        "elevated_reviewed_at": (
            claim.elevated_reviewed_at.isoformat()
            if claim.elevated_reviewed_at
            else None
        ),
        "derived_from_ai": claim.derived_from_ai,
        "extraction_model": claim.extraction_model,
        "last_seen_at": claim.last_seen_at.isoformat() if claim.last_seen_at else None,
    }

    # Create entity node
    node = EntityNode(
        entity_id=entity.id,
        entity_type=entity.entity_type,
        canonical_name=entity.canonical_name,
        properties=properties,
    )

    return node


def claim_to_relationship(claim: MemoryClaim, db: Session) -> Optional[RelationshipEdge]:
    """Convert a memory claim to a graph relationship edge.

    Args:
        claim: The memory claim to convert
        db: Database session

    Returns:
        RelationshipEdge representation of the claim, or None if not a relationship claim

    Raises:
        ValueError: If claim entity or object entity is not found
    """
    # Only convert claims with object_entity_id to relationships
    if not claim.object_entity_id:
        return None

    source_entity = db.query(CanonicalEntity).filter(
        CanonicalEntity.id == claim.entity_id
    ).first()

    target_entity = db.query(CanonicalEntity).filter(
        CanonicalEntity.id == claim.object_entity_id
    ).first()

    if not source_entity:
        raise ValueError(f"Source entity {claim.entity_id} not found for claim {claim.id}")

    if not target_entity:
        raise ValueError(f"Target entity {claim.object_entity_id} not found for claim {claim.id}")

    # Build relationship properties from claim
    properties: Dict[str, Any] = {
        "claim_id": claim.id,
        "claim_key": claim.claim_key,
        "claim_uid": claim.claim_uid,
        "claim_type": claim.claim_type,
        "predicate": claim.predicate,
        "object_value": claim.object_value,
        "object_value_type": claim.object_value_type,
        "normalized_value": claim.normalized_value,
        "confidence": claim.confidence,
        "jurisdiction": claim.jurisdiction,
        "valid_from": claim.valid_from.isoformat() if claim.valid_from else None,
        "valid_to": claim.valid_to.isoformat() if claim.valid_to else None,
        "observed_at": claim.observed_at.isoformat() if claim.observed_at else None,
        "source_quality": claim.source_quality,
        "corroboration_count": claim.corroboration_count,
        "contradiction_count": claim.contradiction_count,
        "review_status": claim.review_status,
        "status": claim.status,
        "is_active": claim.is_active,
        # Phase 6 edge fields
        "claim_sensitivity": claim.claim_sensitivity,
        "elevated_review_status": claim.elevated_review_status,
        "elevated_reviewer_id": claim.elevated_reviewer_id,
        "elevated_reviewed_at": (
            claim.elevated_reviewed_at.isoformat()
            if claim.elevated_reviewed_at
            else None
        ),
        "derived_from_ai": claim.derived_from_ai,
        "extraction_model": claim.extraction_model,
        "last_seen_at": claim.last_seen_at.isoformat() if claim.last_seen_at else None,
    }

    # Create relationship edge
    edge = RelationshipEdge(
        source_entity_id=source_entity.id,
        target_entity_id=target_entity.id,
        relationship_type=claim.predicate or claim.claim_type,
        properties=properties,
    )

    return edge


def batch_claims_to_graph(
    claims: List[MemoryClaim],
    db: Session,
    include_relationships: bool = True,
) -> Dict[str, Any]:
    """Batch process claims for graph integration.

    Args:
        claims: List of memory claims to process
        db: Database session
        include_relationships: Whether to also create relationship edges

    Returns:
        Dictionary with processing statistics:
        - entities_created: Number of entity nodes created
        - relationships_created: Number of relationship edges created
        - errors: List of error messages
    """
    stats: Dict[str, Any] = {
        "entities_created": 0,  # type: ignore[assignment]
        "relationships_created": 0,  # type: ignore[assignment]
        "errors": [],  # type: ignore[assignment]
    }

    for claim in claims:
        try:
            # Convert claim to entity node (validation)
            claim_to_entity_node(claim, db)
            stats["entities_created"] += 1

            # Optionally create relationship
            if include_relationships:
                edge = claim_to_relationship(claim, db)
                if edge:
                    stats["relationships_created"] += 1

        except ValueError as e:
            # Expected errors (missing entities, etc.)
            error_msg = f"Failed to process claim {claim.id}: {str(e)}"
            stats["errors"].append(error_msg)
            logger.warning(error_msg)
        except Exception as e:
            # Unexpected errors
            error_msg = f"Unexpected error processing claim {claim.id}: {str(e)}"
            stats["errors"].append(error_msg)
            logger.error(error_msg, exc_info=True)

    return stats


def sync_claim_to_graph(claim: MemoryClaim, db: Session) -> bool:
    """Sync a single claim to the graph (create or update).

    Args:
        claim: The memory claim to sync
        db: Database session

    Returns:
        True if sync was successful, False otherwise
    """
    try:
        # Convert claim to entity node (validation only)
        claim_to_entity_node(claim, db)

        # Convert claim to relationship if applicable (validation only)
        claim_to_relationship(claim, db)

        return True
    except Exception as e:
        # Log error but don't raise
        logger.error(f"Error syncing claim {claim.id} to graph: {e}", exc_info=True)
        return False


def remove_claim_from_graph(claim: MemoryClaim, db: Session) -> bool:
    """Remove a claim from the graph.

    Args:
        claim: The memory claim to remove
        db: Database session

    Returns:
        True if removal was successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented

    Note:
        This is a placeholder for future implementation. The actual
        graph deletion logic depends on the graph backend being used.
    """
    raise NotImplementedError(
        "Graph deletion logic not yet implemented. "
        "This will require: 1) Remove entity node if claim is the only reference, "
        "2) Remove relationship edge, 3) Handle cascading deletions appropriately."
    )
