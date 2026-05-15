"""Phase 1 regression — LegalInstrument.review_status ORM default.

The default must be the canonical sentinel "pending_review", NOT the legacy
ingestion-run sentinel "pending".  A wrong default would silently pass
pending-status records through publication gates that expect "pending_review".
"""

from __future__ import annotations

import pytest

from app.models.entities import LegalInstrument


def test_legal_instrument_review_status_default_is_pending_review() -> None:
    """ORM default for LegalInstrument.review_status must be 'pending_review'."""
    col = LegalInstrument.__table__.c["review_status"]
    assert col.default is not None, "review_status must have a column-level default"
    assert col.default.arg == "pending_review", (
        f"Expected default 'pending_review', got {col.default.arg!r}"
    )


def test_legal_instrument_review_status_server_default_is_pending_review() -> None:
    """Server default for LegalInstrument.review_status must be 'pending_review'."""
    col = LegalInstrument.__table__.c["review_status"]
    assert col.server_default is not None, "review_status must have a server_default"
    assert col.server_default.arg == "pending_review", (
        f"Expected server_default 'pending_review', got {col.server_default.arg!r}"
    )


def test_legal_instrument_review_status_default_is_not_legacy_pending() -> None:
    """ORM default must not be the legacy sentinel 'pending'."""
    col = LegalInstrument.__table__.c["review_status"]
    if col.default is not None:
        assert col.default.arg != "pending", (
            "review_status default must not be the legacy 'pending' sentinel"
        )
