"""E2E test for evidence pipeline (Phase 8).

Tests the complete evidence pipeline from source ingestion through
to claim publication, including:
- Source ingestion and run tracking
- Evidence snapshot preservation
- Claim extraction and linking
- Evidence verification
- Publication gate validation
"""

import pytest
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.entities import (
    LegalSource,
    IngestionRun,
    SourceSnapshot,
    ReviewItem,
    MemoryClaim,
    MemoryEvidenceLink,
    CanonicalEntity,
)
from app.ingestion.automation_statuses import JobState
from app.review.publication_gate import (
    assert_memory_claim_publication_ready,
    PublicationBlockedError,
)
from app.db.session import SessionLocal


class TestEvidencePipelineE2E:
    """End-to-end test of the evidence pipeline."""

    def test_complete_evidence_pipeline(self, db_session):
        """Test the full evidence pipeline from ingestion to publication."""
        # Step 1: Create a legal source
        source = LegalSource(
            source_id="test_e2e_source",
            source_name="E2E Test Source",
            lifecycle_state="active",
        )
        db_session.add(source)
        db_session.commit()

        # Step 2: Create ingestion run
        run = IngestionRun(
            source_id=source.id,
            status=JobState.COMPLETED.value,
            started_at=datetime.now(timezone.utc),
            finished_at=datetime.now(timezone.utc),
        )
        db_session.add(run)
        db_session.commit()

        # Step 3: Create evidence snapshot
        snapshot = SourceSnapshot(
            run_id=run.id,
            snapshot_id="e2e_snapshot_1",
            source_id=source.id,
            snapshot_timestamp=datetime.now(timezone.utc),
            raw_content=b'{"test": "data"}',
            content_hash="abc123",
            preserved=True,
        )
        db_session.add(snapshot)
        db_session.commit()

        # Step 4: Create review item linked to snapshot
        review_item = ReviewItem(
            source_snapshot_id=snapshot.id,
            status="approved",
            item_type="case",
        )
        db_session.add(review_item)
        db_session.commit()

        # Step 5: Create canonical entity
        entity = CanonicalEntity(
            entity_type="person",
            canonical_name="E2E Test Judge",
        )
        db_session.add(entity)
        db_session.commit()

        # Step 6: Create memory claim
        claim = MemoryClaim(
            claim_key="e2e_claim_1",
            claim_type="role",
            entity_id=entity.id,
            claim_value="Judge",
            normalized_value="Judge",
            object_value_type="text",
            predicate="role",
            confidence=0.85,
            contradiction_count=0,
            review_status="approved",
            status="active",
            is_active=True,
            extraction_run_id=run.id,
        )
        db_session.add(claim)
        db_session.commit()

        # Step 7: Link claim to evidence
        evidence_link = MemoryEvidenceLink(
            claim_id=claim.id,
            snapshot_id=snapshot.id,
            support_type="supports",
            confidence=0.85,
            evidence_checksum="abc123",
        )
        db_session.add(evidence_link)
        db_session.commit()

        # Step 8: Verify publication gate passes
        assert_memory_claim_publication_ready(claim, db_session)

        # Step 9: Verify the complete chain
        assert snapshot.source_id == source.id
        assert snapshot.run_id == run.id
        assert review_item.source_snapshot_id == snapshot.id
        assert claim.extraction_run_id == run.id
        assert evidence_link.claim_id == claim.id
        assert evidence_link.snapshot_id == snapshot.id

    def test_evidence_pipeline_with_missing_snapshot(self, db_session):
        """Test that publication gate fails when evidence snapshot is missing."""
        source = LegalSource(
            source_id="test_e2e_source_2",
            source_name="E2E Test Source 2",
            lifecycle_state="active",
        )
        db_session.add(source)
        db_session.commit()

        run = IngestionRun(
            source_id=source.id,
            status=JobState.COMPLETED.value,
            started_at=datetime.now(timezone.utc),
            finished_at=datetime.now(timezone.utc),
        )
        db_session.add(run)
        db_session.commit()

        entity = CanonicalEntity(
            entity_type="person",
            canonical_name="E2E Test Judge 2",
        )
        db_session.add(entity)
        db_session.commit()

        claim = MemoryClaim(
            claim_key="e2e_claim_2",
            claim_type="role",
            entity_id=entity.id,
            claim_value="Judge",
            normalized_value="Judge",
            object_value_type="text",
            predicate="role",
            confidence=0.85,
            contradiction_count=0,
            review_status="approved",
            status="active",
            is_active=True,
            extraction_run_id=run.id,
        )
        db_session.add(claim)
        db_session.commit()

        # No evidence link - should fail publication gate
        with pytest.raises(PublicationBlockedError) as exc:
            assert_memory_claim_publication_ready(claim, db_session)
        assert "no supporting evidence links" in str(exc.value)

    def test_evidence_pipeline_with_deprecated_source(self, db_session):
        """Test that publication gate fails when source is deprecated."""
        source = LegalSource(
            source_id="test_e2e_source_3",
            source_name="E2E Test Source 3",
            lifecycle_state="deprecated",
        )
        db_session.add(source)
        db_session.commit()

        run = IngestionRun(
            source_id=source.id,
            status=JobState.COMPLETED.value,
            started_at=datetime.now(timezone.utc),
            finished_at=datetime.now(timezone.utc),
        )
        db_session.add(run)
        db_session.commit()

        snapshot = SourceSnapshot(
            run_id=run.id,
            snapshot_id="e2e_snapshot_3",
            source_id=source.id,
            snapshot_timestamp=datetime.now(timezone.utc),
            raw_content=b'{"test": "data"}',
            content_hash="abc123",
            preserved=True,
        )
        db_session.add(snapshot)
        db_session.commit()

        entity = CanonicalEntity(
            entity_type="person",
            canonical_name="E2E Test Judge 3",
        )
        db_session.add(entity)
        db_session.commit()

        claim = MemoryClaim(
            claim_key="e2e_claim_3",
            claim_type="role",
            entity_id=entity.id,
            claim_value="Judge",
            normalized_value="Judge",
            object_value_type="text",
            predicate="role",
            confidence=0.85,
            contradiction_count=0,
            review_status="approved",
            status="active",
            is_active=True,
            extraction_run_id=run.id,
        )
        db_session.add(claim)
        db_session.commit()

        evidence_link = MemoryEvidenceLink(
            claim_id=claim.id,
            snapshot_id=snapshot.id,
            support_type="supports",
            confidence=0.85,
            evidence_checksum="abc123",
        )
        db_session.add(evidence_link)
        db_session.commit()

        # Should fail due to deprecated source
        with pytest.raises(PublicationBlockedError) as exc:
            assert_memory_claim_publication_ready(claim, db_session)
        assert "deprecated" in str(exc.value)


@pytest.fixture
def db_session():
    """Create a database session for testing."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
