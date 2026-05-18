"""Tests for risk-tiered review system (Phase 10).

Tests risk tier calculation and review requirements.
"""

import pytest

from app.models.entities import MemoryClaim, CanonicalEntity
from app.review.risk_tier import (
    calculate_claim_risk_tier,
    get_review_requirements,
    can_auto_approve,
    calculate_entity_risk_tier,
    batch_calculate_risk_tiers,
)
from app.db.session import SessionLocal


class TestRiskTierCalculation:
    """Test risk tier calculation logic."""

    def test_low_confidence_high_risk(self, db_session):
        """Test that low confidence claims are high risk."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        claim = MemoryClaim(
            claim_key="test_claim_1",
            claim_type="test",
            entity_id=entity.id,
            claim_value="Test value",
            confidence=0.2,
            contradiction_count=0,
            corroboration_count=0,
        )
        db_session.add(claim)
        db_session.commit()

        risk_tier = calculate_claim_risk_tier(claim.id, db_session)
        assert risk_tier in ["high", "critical"]

    def test_high_confidence_low_risk(self, db_session):
        """Test that high confidence claims are low risk."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        claim = MemoryClaim(
            claim_key="test_claim_1",
            claim_type="test",
            entity_id=entity.id,
            claim_value="Test value",
            confidence=0.9,
            contradiction_count=0,
            corroboration_count=2,
        )
        db_session.add(claim)
        db_session.commit()

        risk_tier = calculate_claim_risk_tier(claim.id, db_session)
        assert risk_tier in ["low", "medium"]

    def test_contradictions_increase_risk(self, db_session):
        """Test that contradictions increase risk tier."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        claim = MemoryClaim(
            claim_key="test_claim_1",
            claim_type="test",
            entity_id=entity.id,
            claim_value="Test value",
            confidence=0.7,
            contradiction_count=3,
            corroboration_count=1,
        )
        db_session.add(claim)
        db_session.commit()

        risk_tier = calculate_claim_risk_tier(claim.id, db_session)
        assert risk_tier in ["high", "critical"]

    def test_lack_of_evidence_increases_risk(self, db_session):
        """Test that lack of evidence increases risk tier."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        claim = MemoryClaim(
            claim_key="test_claim_1",
            claim_type="test",
            entity_id=entity.id,
            claim_value="Test value",
            confidence=0.7,
            contradiction_count=0,
            corroboration_count=0,
        )
        db_session.add(claim)
        db_session.commit()

        risk_tier = calculate_claim_risk_tier(claim.id, db_session)
        assert risk_tier in ["medium", "high"]


class TestReviewRequirements:
    """Test review requirements per risk tier."""

    def test_critical_tier_requirements(self):
        """Test that critical tier requires review and evidence."""
        requirements = get_review_requirements("critical")
        assert requirements["requires_review"] is True
        assert requirements["requires_evidence"] is True
        assert requirements["auto_approve"] is False

    def test_high_tier_requirements(self):
        """Test that high tier requires review and evidence."""
        requirements = get_review_requirements("high")
        assert requirements["requires_review"] is True
        assert requirements["requires_evidence"] is True
        assert requirements["auto_approve"] is False

    def test_medium_tier_requirements(self):
        """Test that medium tier requires review but not evidence."""
        requirements = get_review_requirements("medium")
        assert requirements["requires_review"] is True
        assert requirements["requires_evidence"] is False
        assert requirements["auto_approve"] is False

    def test_low_tier_requirements(self):
        """Test that low tier allows auto-approval."""
        requirements = get_review_requirements("low")
        assert requirements["requires_review"] is False
        assert requirements["requires_evidence"] is False
        assert requirements["auto_approve"] is True


class TestAutoApproval:
    """Test auto-approval logic."""

    def test_low_risk_can_auto_approve(self, db_session):
        """Test that low risk claims can be auto-approved."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        claim = MemoryClaim(
            claim_key="test_claim_1",
            claim_type="test",
            entity_id=entity.id,
            claim_value="Test value",
            confidence=0.9,
            contradiction_count=0,
            corroboration_count=2,
        )
        db_session.add(claim)
        db_session.commit()

        assert can_auto_approve(claim.id, db_session) is True

    def test_high_risk_cannot_auto_approve(self, db_session):
        """Test that high risk claims cannot be auto-approved."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        claim = MemoryClaim(
            claim_key="test_claim_1",
            claim_type="test",
            entity_id=entity.id,
            claim_value="Test value",
            confidence=0.3,
            contradiction_count=2,
            corroboration_count=0,
        )
        db_session.add(claim)
        db_session.commit()

        assert can_auto_approve(claim.id, db_session) is False


class TestEntityRiskTier:
    """Test entity-level risk tier calculation."""

    def test_entity_risk_based_on_claims(self, db_session):
        """Test that entity risk is based on its claims."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        # Add low risk claim
        claim1 = MemoryClaim(
            claim_key="test_claim_1",
            claim_type="test",
            entity_id=entity.id,
            claim_value="Test value",
            confidence=0.9,
            contradiction_count=0,
            corroboration_count=2,
        )
        db_session.add(claim1)
        db_session.commit()

        risk_tier = calculate_entity_risk_tier(entity.id, db_session)
        assert risk_tier in ["low", "medium"]

    def test_entity_risk_max_of_claims(self, db_session):
        """Test that entity risk is the maximum of its claims."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        # Add high risk claim
        claim1 = MemoryClaim(
            claim_key="test_claim_1",
            claim_type="test",
            entity_id=entity.id,
            claim_value="Test value",
            confidence=0.3,
            contradiction_count=2,
            corroboration_count=0,
        )
        db_session.add(claim1)
        db_session.commit()

        risk_tier = calculate_entity_risk_tier(entity.id, db_session)
        assert risk_tier in ["high", "critical"]

    def test_batch_calculate_risk_tiers(self, db_session):
        """Test batch calculation of risk tiers."""
        entity = CanonicalEntity(
            entity_type="person",
            name="John Doe",
            jurisdiction="CA",
        )
        db_session.add(entity)
        db_session.commit()

        # Add multiple claims
        for i in range(3):
            claim = MemoryClaim(
                claim_key=f"test_claim_{i}",
                claim_type="test",
                entity_id=entity.id,
                claim_value=f"Test value {i}",
                confidence=0.7,
                contradiction_count=0,
                corroboration_count=1,
            )
            db_session.add(claim)
        db_session.commit()

        risk_tiers = batch_calculate_risk_tiers(entity.id, db_session)
        assert len(risk_tiers) == 3
        for claim_id, tier in risk_tiers.items():
            assert tier in ["low", "medium", "high", "critical"]


@pytest.fixture
def db_session():
    """Create a database session for testing."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
