"""Phase 8 regression — admin review queue includes 'legal_instrument'.

Verifies:
1. _review_statements() accepts 'legal_instrument' entity type.
2. The default requested_types in admin_review_queue includes 'legal_instrument'.
3. The admin review queue endpoint returns 200 with legal_instrument results.
"""

from __future__ import annotations

import inspect

import pytest
from fastapi.testclient import TestClient

from app.api.routes.admin_review import _review_statements, admin_review_queue


class TestReviewStatementsLegalInstrument:
    def test_legal_instrument_returns_statements_without_error(self) -> None:
        """_review_statements('legal_instrument', ...) must not raise HTTPException."""
        from fastapi import HTTPException
        try:
            data_stmt, count_stmt = _review_statements("legal_instrument", None, None)
        except HTTPException:
            pytest.fail(
                "_review_statements raised HTTPException for 'legal_instrument' — "
                "it must return valid SELECT statements"
            )
        assert data_stmt is not None
        assert count_stmt is not None

    def test_legal_instrument_with_review_status_filter(self) -> None:
        from fastapi import HTTPException
        try:
            data_stmt, count_stmt = _review_statements(
                "legal_instrument", "pending_review", None
            )
        except HTTPException:
            pytest.fail(
                "_review_statements raised HTTPException for 'legal_instrument' with status filter"
            )
        # Confirm the WHERE clause contains review_status
        compiled = str(data_stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "review_status" in compiled.lower()


class TestAdminReviewQueueDefaultTypes:
    def test_legal_instrument_in_default_source(self) -> None:
        """admin_review_queue source must include 'legal_instrument' in default requested_types."""
        src = inspect.getsource(admin_review_queue)
        assert '"legal_instrument"' in src, (
            "admin_review_queue must include 'legal_instrument' in default requested_types"
        )

    def test_default_includes_all_four_types(self) -> None:
        src = inspect.getsource(admin_review_queue)
        for entity_type in ("event", "crime_incident", "source", "legal_instrument"):
            assert f'"{entity_type}"' in src, (
                f"admin_review_queue default must include '{entity_type}'"
            )


class TestAdminReviewQueueEndpoint:
    def test_review_queue_returns_200_for_legal_instrument(
        self, client: TestClient, jwt_admin_headers: dict
    ) -> None:
        response = client.get(
            "/api/admin/review-queue?entity_type=legal_instrument",
            headers=jwt_admin_headers,
        )
        assert response.status_code == 200, (
            f"Expected 200 from admin review queue for legal_instrument, "
            f"got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert "items" in data
        assert "total_count" in data

    def test_review_queue_default_does_not_raise_for_legal_instrument(
        self, client: TestClient, jwt_admin_headers: dict
    ) -> None:
        """Default queue (no entity_type param) must succeed even though it now includes legal_instrument."""
        response = client.get(
            "/api/admin/review-queue",
            headers=jwt_admin_headers,
        )
        assert response.status_code == 200, (
            f"Default review queue returned {response.status_code}: {response.text}"
        )
