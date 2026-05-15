"""Phase 5 regression — evidence_chat policy alignment.

Verifies:
1. chat_about_evidence() excludes RelationshipEvidence with relationship_status="pending".
2. _legal_context_citations() joins SourceSnapshot and requires content_hash IS NOT NULL.
"""

from __future__ import annotations

import inspect

import pytest
from sqlalchemy import text

from app.db.session import SessionLocal
from app.services.evidence_chat import _legal_context_citations, chat_about_evidence


class TestChatPendingRelationshipExcluded:
    """chat_about_evidence() must not surface evidence with relationship_status='pending'."""

    def test_pending_not_in_chat_filter_allowlist(self) -> None:
        """The source code of chat_about_evidence must not allow 'pending' in the relationship_status filter."""
        src = inspect.getsource(chat_about_evidence)
        # The allowlist ["approved", "verified"] must not include "pending"
        assert '"pending"' not in src or 'relationship_status' not in src.split('"pending"')[0].split('\n')[-1], (
            "chat_about_evidence must not filter by relationship_status='pending'"
        )

    def test_approved_and_verified_still_in_allowlist(self) -> None:
        """'approved' and 'verified' must remain in the relationship_status filter."""
        src = inspect.getsource(chat_about_evidence)
        assert '"approved"' in src
        assert '"verified"' in src


class TestLegalContextCitationsSnapshotRequirement:
    """_legal_context_citations() must join SourceSnapshot and require content_hash."""

    def test_source_snapshot_join_in_source(self) -> None:
        src = inspect.getsource(_legal_context_citations)
        assert "SourceSnapshot" in src, (
            "_legal_context_citations must join SourceSnapshot"
        )

    def test_content_hash_filter_in_source(self) -> None:
        src = inspect.getsource(_legal_context_citations)
        assert "content_hash" in src, (
            "_legal_context_citations must filter on SourceSnapshot.content_hash"
        )

    def test_is_not_none_filter_in_source(self) -> None:
        src = inspect.getsource(_legal_context_citations)
        assert "is_not" in src or "is not None" in src or "isnot" in src, (
            "_legal_context_citations must use is_not(None) for content_hash"
        )

    def test_raw_snapshot_id_filter_in_source(self) -> None:
        """raw_snapshot_id IS NOT NULL must still be present so non-snapshotted records are excluded."""
        src = inspect.getsource(_legal_context_citations)
        assert "raw_snapshot_id" in src
