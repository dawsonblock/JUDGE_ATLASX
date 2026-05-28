"""
Tests for the publish_status migration logic (20260527_0004).

These tests verify the migration's UPDATE logic using in-process SQLite
without requiring a live PostgreSQL connection.  They do NOT run Alembic
directly — instead they replicate the exact SQL from the migration and
assert the expected outcome.

Run:  pytest backend/app/tests/test_publish_status_migration.py -v
"""

import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.policies.public_status import (
    PUBLIC_SAFE,
    PUBLIC_REDACTED,
    PUBLIC_INTERNAL_PUBLISHED,
    PUBLIC_VISIBLE_STATUSES,
    LEGACY_PUBLISHED,
    REVIEW_APPROVED,
    REVIEW_PENDING,
    REVIEW_REJECTED,
    ALL_PUBLISH_STATUSES,
)


# ---------------------------------------------------------------------------
# SQLite in-memory fixture table
# ---------------------------------------------------------------------------

DDL = """
CREATE TABLE geo_legal_events (
    id             TEXT PRIMARY KEY,
    publish_status TEXT NOT NULL,
    review_status  TEXT NOT NULL
)
"""

SEED = [
    # Rows that should become public_safe
    ("pub-approved-1", "published", "approved"),
    ("pub-approved-2", "published", "approved"),
    # Rows that should become internal_published
    ("pub-pending-1", "published", "needs_review"),
    ("pub-rejected-1", "published", "rejected"),
    # Rows with other publish_status values — must be untouched
    ("draft-1", "draft", "needs_review"),
    ("suppressed-1", "suppressed", "approved"),
    ("disputed-1", "disputed", "needs_review"),
    ("private-1", "private", "needs_review"),
    # Rows already using new values — must be untouched
    ("safe-1", "public_safe", "approved"),
    ("redacted-1", "public_redacted", "approved"),
]

MIGRATION_STEP_1 = """
UPDATE geo_legal_events
   SET publish_status = 'public_safe'
 WHERE publish_status = 'published'
   AND review_status  = 'approved'
"""

MIGRATION_STEP_2 = """
UPDATE geo_legal_events
   SET publish_status = 'internal_published'
 WHERE publish_status = 'published'
"""


@pytest.fixture()
def conn():
    """Provide a SQLite in-memory connection seeded with test rows."""
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as c:
        c.execute(text(DDL))
        c.executemany(
            "INSERT INTO geo_legal_events VALUES (?, ?, ?)", SEED
        )
        c.commit()
        yield c


def run_migration(conn) -> None:
    conn.execute(text(MIGRATION_STEP_1))
    conn.execute(text(MIGRATION_STEP_2))
    conn.commit()


def fetch(conn, id_: str) -> str:
    row = conn.execute(
        text("SELECT publish_status FROM geo_legal_events WHERE id = :id"),
        {"id": id_},
    ).fetchone()
    assert row is not None, f"Row {id_!r} not found"
    return row[0]


# ---------------------------------------------------------------------------
# Migration correctness tests
# ---------------------------------------------------------------------------


class TestPublishedPlusApprovedBecomesPublicSafe:
    def test_first_approved_row(self, conn):
        run_migration(conn)
        assert fetch(conn, "pub-approved-1") == PUBLIC_SAFE

    def test_second_approved_row(self, conn):
        run_migration(conn)
        assert fetch(conn, "pub-approved-2") == PUBLIC_SAFE

    def test_result_is_in_public_visible_statuses(self, conn):
        run_migration(conn)
        assert fetch(conn, "pub-approved-1") in PUBLIC_VISIBLE_STATUSES


class TestPublishedWithoutApprovalBecomesInternalPublished:
    def test_pending_review_row(self, conn):
        run_migration(conn)
        assert fetch(conn, "pub-pending-1") == PUBLIC_INTERNAL_PUBLISHED

    def test_rejected_row(self, conn):
        run_migration(conn)
        assert fetch(conn, "pub-rejected-1") == PUBLIC_INTERNAL_PUBLISHED

    def test_internal_published_not_in_public_visible(self, conn):
        run_migration(conn)
        assert fetch(conn, "pub-pending-1") not in PUBLIC_VISIBLE_STATUSES


class TestUntouchedRows:
    """Rows with other publish_status values must not change."""

    def test_draft_untouched(self, conn):
        run_migration(conn)
        assert fetch(conn, "draft-1") == "draft"

    def test_suppressed_untouched(self, conn):
        run_migration(conn)
        assert fetch(conn, "suppressed-1") == "suppressed"

    def test_disputed_untouched(self, conn):
        run_migration(conn)
        assert fetch(conn, "disputed-1") == "disputed"

    def test_private_untouched(self, conn):
        run_migration(conn)
        assert fetch(conn, "private-1") == "private"

    def test_already_public_safe_untouched(self, conn):
        run_migration(conn)
        assert fetch(conn, "safe-1") == PUBLIC_SAFE

    def test_already_public_redacted_untouched(self, conn):
        run_migration(conn)
        assert fetch(conn, "redacted-1") == PUBLIC_REDACTED


class TestNoLegacyPublishedRemains:
    def test_zero_published_rows_after_migration(self, conn):
        run_migration(conn)
        count = conn.execute(
            text(
                "SELECT COUNT(*) FROM geo_legal_events "
                "WHERE publish_status = :ps"
            ),
            {"ps": LEGACY_PUBLISHED},
        ).scalar()
        assert count == 0, "No rows should retain the legacy 'published' status"


class TestDowngradeMigration:
    """Verify the downgrade SQL restores the pre-migration state."""

    DOWNGRADE_1 = """
        UPDATE geo_legal_events
           SET publish_status = 'published'
         WHERE publish_status IN ('public_safe', 'public_redacted')
    """
    DOWNGRADE_2 = """
        UPDATE geo_legal_events
           SET publish_status = 'published'
         WHERE publish_status = 'internal_published'
    """

    def test_downgrade_restores_approved_rows(self, conn):
        run_migration(conn)
        conn.execute(text(self.DOWNGRADE_1))
        conn.execute(text(self.DOWNGRADE_2))
        conn.commit()
        assert fetch(conn, "pub-approved-1") == LEGACY_PUBLISHED

    def test_downgrade_restores_pending_rows(self, conn):
        run_migration(conn)
        conn.execute(text(self.DOWNGRADE_1))
        conn.execute(text(self.DOWNGRADE_2))
        conn.commit()
        assert fetch(conn, "pub-pending-1") == LEGACY_PUBLISHED

    def test_downgrade_preserves_other_statuses(self, conn):
        run_migration(conn)
        conn.execute(text(self.DOWNGRADE_1))
        conn.execute(text(self.DOWNGRADE_2))
        conn.commit()
        assert fetch(conn, "draft-1") == "draft"
        assert fetch(conn, "suppressed-1") == "suppressed"


class TestPublicStatusConstants:
    """Smoke-test the policy module constants used throughout the codebase."""

    def test_public_safe_in_visible_set(self):
        assert PUBLIC_SAFE in PUBLIC_VISIBLE_STATUSES

    def test_public_redacted_in_visible_set(self):
        assert PUBLIC_REDACTED in PUBLIC_VISIBLE_STATUSES

    def test_internal_published_not_visible(self):
        assert PUBLIC_INTERNAL_PUBLISHED not in PUBLIC_VISIBLE_STATUSES

    def test_legacy_published_not_visible(self):
        assert LEGACY_PUBLISHED not in PUBLIC_VISIBLE_STATUSES

    def test_all_publish_statuses_complete(self):
        # internal_published must be in the full set
        assert PUBLIC_INTERNAL_PUBLISHED in ALL_PUBLISH_STATUSES

    def test_visible_is_subset_of_all(self):
        assert PUBLIC_VISIBLE_STATUSES.issubset(ALL_PUBLISH_STATUSES)
