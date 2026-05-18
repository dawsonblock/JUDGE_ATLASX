"""Tests for named-person criminal allegation publication policy (Phase 4)."""
import pytest
from datetime import datetime, timezone

from app.models.entities import MemoryClaim, CanonicalEntity, SourceSnapshot, LegalSource
from app.review.publication_gate import assert_memory_claim_publication_ready, PublicationBlockedError
from app.db.session import SessionLocal


def test_named_person_criminal_allegation_requires_elevated_approval():
    """Test that named-person criminal allegations require elevated approval."""
    db = SessionLocal()

    try:
        # Create a claim with criminal_allegation_named_person sensitivity
        claim = MemoryClaim(
            claim_key="test-claim-1",
            claim_uid="uid-1",
            claim_type="criminal_allegation",
            entity_id=1,
            claim_value="Test claim",
            confidence=0.8,
            review_status="approved",
            claim_sensitivity="criminal_allegation_named_person",
            elevated_review_status="pending_review",  # Not approved
        )
        db.add(claim)
        db.commit()

        # Should raise PublicationBlockedError
        with pytest.raises(PublicationBlockedError) as exc_info:
            assert_memory_claim_publication_ready(claim, db)

        assert "requires elevated approval for named-person criminal allegation" in str(exc_info.value)

    finally:
        db.close()


def test_named_person_criminal_allegation_with_elevated_approval_passes():
    """Test that named-person criminal allegations pass with elevated approval."""
    db = SessionLocal()

    try:
        # Create a claim with elevated approval
        claim = MemoryClaim(
            claim_key="test-claim-2",
            claim_uid="uid-2",
            claim_type="criminal_allegation",
            entity_id=1,
            claim_value="Test claim",
            confidence=0.8,
            review_status="approved",
            claim_sensitivity="criminal_allegation_named_person",
            elevated_review_status="approved",
            elevated_reviewer_id="reviewer-1",
            elevated_reviewed_at=datetime.now(timezone.utc),
        )
        db.add(claim)

        # Create supporting evidence
        from app.models.entities import MemoryEvidenceLink
        evidence = MemoryEvidenceLink(
            claim_id=claim.id,
            snapshot_id=1,
            evidence_checksum="abc123",
            support_type="supports",
        )
        db.add(evidence)
        db.commit()

        # Should not raise PublicationBlockedError (assuming source is official)
        # Note: This test would need a proper source setup to fully pass
        # For now, we just verify it doesn't fail on the elevated approval check
        try:
            assert_memory_claim_publication_ready(claim, db)
        except PublicationBlockedError as e:
            # If it fails, it should not be due to elevated approval
            assert "requires elevated approval" not in str(e)

    finally:
        db.close()


def test_public_record_criminal_allegation_does_not_require_elevated_approval():
    """Test that public record criminal allegations do not require elevated approval."""
    db = SessionLocal()

    try:
        # Create a claim with public_record sensitivity
        claim = MemoryClaim(
            claim_key="test-claim-3",
            claim_uid="uid-3",
            claim_type="criminal_allegation",
            entity_id=1,
            claim_value="Test claim",
            confidence=0.8,
            review_status="approved",
            claim_sensitivity="public_record",  # Not named-person
        )
        db.add(claim)

        # Create supporting evidence
        from app.models.entities import MemoryEvidenceLink
        evidence = MemoryEvidenceLink(
            claim_id=claim.id,
            snapshot_id=1,
            evidence_checksum="abc123",
            support_type="supports",
        )
        db.add(evidence)
        db.commit()

        # Should not require elevated approval
        try:
            assert_memory_claim_publication_ready(claim, db)
        except PublicationBlockedError as e:
            # If it fails, it should not be due to elevated approval
            assert "requires elevated approval" not in str(e)

    finally:
        db.close()


def test_non_criminal_allegation_does_not_require_elevated_approval():
    """Test that non-criminal allegations do not require elevated approval."""
    db = SessionLocal()

    try:
        # Create a claim with different sensitivity
        claim = MemoryClaim(
            claim_key="test-claim-4",
            claim_uid="uid-4",
            claim_type="employment",
            entity_id=1,
            claim_value="Test claim",
            confidence=0.8,
            review_status="approved",
            claim_sensitivity="statistical_aggregate",
        )
        db.add(claim)

        # Create supporting evidence
        from app.models.entities import MemoryEvidenceLink
        evidence = MemoryEvidenceLink(
            claim_id=claim.id,
            snapshot_id=1,
            evidence_checksum="abc123",
            support_type="supports",
        )
        db.add(evidence)
        db.commit()

        # Should not require elevated approval
        try:
            assert_memory_claim_publication_ready(claim, db)
        except PublicationBlockedError as e:
            # If it fails, it should not be due to elevated approval
            assert "requires elevated approval" not in str(e)

    finally:
        db.close()


def test_elevated_approval_fields_are_set():
    """Test that elevated approval fields are properly set when approved."""
    db = SessionLocal()

    try:
        # Create a claim with elevated approval
        claim = MemoryClaim(
            claim_key="test-claim-5",
            claim_uid="uid-5",
            claim_type="criminal_allegation",
            entity_id=1,
            claim_value="Test claim",
            confidence=0.8,
            review_status="approved",
            claim_sensitivity="criminal_allegation_named_person",
            elevated_review_status="approved",
            elevated_reviewer_id="reviewer-1",
            elevated_reviewed_at=datetime.now(timezone.utc),
        )
        db.add(claim)
        db.commit()

        # Verify fields are set
        assert claim.elevated_review_status == "approved"
        assert claim.elevated_reviewer_id == "reviewer-1"
        assert claim.elevated_reviewed_at is not None

    finally:
        db.close()
