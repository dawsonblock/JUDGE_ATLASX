"""Phase 3 regression — RelationshipEvidence review_status column + promotion helper.

Verifies:
1. RelationshipEvidence ORM has a review_status column with the correct default.
2. relationship_public_status() returns correct canonical statuses based on
   verification_status / relationship_status field combinations.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.models.entities import RelationshipEvidence
from app.policies.publication_policy import (
    OFFICIAL_POLICE_OPEN_DATA_REPORT,
    PENDING_REVIEW,
    REJECTED,
    VERIFIED_COURT_RECORD,
    relationship_public_status,
)


class TestRelationshipEvidenceColumn:
    def test_review_status_column_exists(self) -> None:
        assert "review_status" in RelationshipEvidence.__table__.c

    def test_review_status_default_is_pending_review(self) -> None:
        col = RelationshipEvidence.__table__.c["review_status"]
        assert col.default is not None
        assert col.default.arg == "pending_review"

    def test_review_status_server_default_is_pending_review(self) -> None:
        col = RelationshipEvidence.__table__.c["review_status"]
        assert col.server_default is not None
        assert col.server_default.arg == "pending_review"


class TestRelationshipPublicStatus:
    def _entity(
        self, *, verification_status: str | None, relationship_status: str | None
    ) -> MagicMock:
        e = MagicMock()
        e.verification_status = verification_status
        e.relationship_status = relationship_status
        return e

    def test_verified_and_approved_returns_verified_court_record(self) -> None:
        e = self._entity(verification_status="verified", relationship_status="approved")
        assert relationship_public_status(e) == VERIFIED_COURT_RECORD

    def test_verified_and_verified_relationship_returns_verified_court_record(self) -> None:
        e = self._entity(verification_status="verified", relationship_status="verified")
        assert relationship_public_status(e) == VERIFIED_COURT_RECORD

    def test_rejected_verification_returns_rejected(self) -> None:
        e = self._entity(verification_status="rejected", relationship_status="approved")
        assert relationship_public_status(e) == REJECTED

    def test_rejected_relationship_returns_rejected(self) -> None:
        e = self._entity(verification_status="reviewed", relationship_status="rejected")
        assert relationship_public_status(e) == REJECTED

    def test_reviewed_verification_returns_official_police_open_data(self) -> None:
        e = self._entity(verification_status="reviewed", relationship_status="pending")
        assert relationship_public_status(e) == OFFICIAL_POLICE_OPEN_DATA_REPORT

    def test_pending_verification_returns_pending_review(self) -> None:
        e = self._entity(verification_status="pending", relationship_status="pending")
        assert relationship_public_status(e) == PENDING_REVIEW

    def test_none_fields_return_pending_review(self) -> None:
        e = self._entity(verification_status=None, relationship_status=None)
        assert relationship_public_status(e) == PENDING_REVIEW
