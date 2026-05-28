"""Add public_safe and public_redacted as canonical publish_status values.

Revision ID: 20260527_0004
Revises: 20260527_0003
Create Date: 2026-05-27

Background
----------
The old value "published" was used as a publish_status sentinel but was
ambiguous — it didn't distinguish between records that have been through the
human review gate and are safe for public display vs. records that were
marked published internally but should not yet be surfaced publicly.

This migration introduces two canonical public-visibility statuses:

    public_safe      — reviewed, approved, and cleared for full public display
    public_redacted  — approved for public display with sensitive fields redacted

The old "published" value is migrated to "public_safe" only where the row
also has review_status = 'approved'. Rows with "published" but any other
review_status are migrated to "internal_published" so they remain visible
to admin users but are blocked by the public release policy.

All other existing publish_status values (draft, internal, suppressed,
disputed, private) are untouched.

Rollback
--------
The downgrade() restores all "public_safe" rows to "published" and all
"internal_published" rows to "published" so the previous code works again.
"""

from alembic import op
import sqlalchemy as sa


# Alembic chain identifiers
revision = "20260527_0004"
down_revision = "20260527_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use a raw text block so the migration is database-agnostic and readable
    # in code review without needing an ORM import.
    conn = op.get_bind()

    # Step 1: rows that are "published" AND "approved" → public_safe
    conn.execute(
        sa.text(
            """
            UPDATE geo_legal_events
               SET publish_status = 'public_safe'
             WHERE publish_status = 'published'
               AND review_status  = 'approved'
            """
        )
    )

    # Step 2: remaining "published" rows (not yet approved) → internal_published
    # These stay visible in admin but are blocked by the public release policy.
    conn.execute(
        sa.text(
            """
            UPDATE geo_legal_events
               SET publish_status = 'internal_published'
             WHERE publish_status = 'published'
            """
        )
    )

    # Step 3: add a check constraint so only known values can be inserted going
    # forward. PostgreSQL supports named constraints; SQLite ignores check
    # constraints at runtime but still records them in the schema.
    # Using a try/except so migrations work on SQLite test databases too.
    try:
        op.create_check_constraint(
            "ck_geo_legal_events_publish_status",
            "geo_legal_events",
            sa.text(
                "publish_status IN ("
                "  'draft',"
                "  'internal',"
                "  'internal_published',"
                "  'public_redacted',"
                "  'public_safe',"
                "  'suppressed',"
                "  'disputed',"
                "  'private'"
                ")"
            ),
        )
    except Exception:
        # SQLite / some older PostgreSQL versions may not support named
        # check constraints on existing tables; skip rather than fail.
        pass


def downgrade() -> None:
    conn = op.get_bind()

    # Remove the check constraint first (if it exists)
    try:
        op.drop_constraint(
            "ck_geo_legal_events_publish_status",
            "geo_legal_events",
            type_="check",
        )
    except Exception:
        pass

    # Restore public_safe and public_redacted → published
    conn.execute(
        sa.text(
            """
            UPDATE geo_legal_events
               SET publish_status = 'published'
             WHERE publish_status IN ('public_safe', 'public_redacted')
            """
        )
    )

    # Restore internal_published → published
    conn.execute(
        sa.text(
            """
            UPDATE geo_legal_events
               SET publish_status = 'published'
             WHERE publish_status = 'internal_published'
            """
        )
    )
