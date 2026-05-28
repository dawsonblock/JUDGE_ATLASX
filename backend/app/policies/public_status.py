"""
Canonical public-release status constants for GeoLegalEvent.publish_status.

These are the authoritative DB-level values.  Import these constants instead
of hardcoding strings throughout the codebase.

publish_status values (GeoLegalEvent.publish_status):
    private              — not visible outside admin context
    admin_only           — visible to admin users only
    internal_published   — published internally, not cleared for public (post-migration
                           resting place for old "published" rows without approval)
    public_safe          — reviewed, approved, and cleared for full public display
    public_redacted      — approved for public display with sensitive fields redacted
    blocked              — blocked from publication (legal hold, dispute, etc.)

    LEGACY / INVALID (must not be written to new records):
    published            — pre-migration value.
                           Migration target (20260527_0004):
                             published + review=approved → public_safe
                             published + other review   → internal_published

review_status values (GeoLegalEvent.review_status, StatuteIncidentLink.review_status):
    needs_review    — awaiting human review
    approved        — approved by a human reviewer
    rejected        — rejected by a human reviewer
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# publish_status constants
# ---------------------------------------------------------------------------

PUBLIC_PRIVATE: str = "private"
PUBLIC_ADMIN_ONLY: str = "admin_only"
PUBLIC_INTERNAL_PUBLISHED: str = "internal_published"  # post-migration, not public
PUBLIC_SAFE: str = "public_safe"
PUBLIC_REDACTED: str = "public_redacted"
PUBLIC_BLOCKED: str = "blocked"

# All valid post-migration publish_status values.
ALL_PUBLISH_STATUSES: frozenset[str] = frozenset(
    {
        PUBLIC_PRIVATE,
        PUBLIC_ADMIN_ONLY,
        PUBLIC_INTERNAL_PUBLISHED,
        PUBLIC_SAFE,
        PUBLIC_REDACTED,
        PUBLIC_BLOCKED,
    }
)

# publish_status values that allow public API visibility.
PUBLIC_VISIBLE_STATUSES: frozenset[str] = frozenset({PUBLIC_SAFE, PUBLIC_REDACTED})

# publish_status values that are never visible in any public API.
NON_PUBLIC_STATUSES: frozenset[str] = frozenset(
    {PUBLIC_PRIVATE, PUBLIC_ADMIN_ONLY, PUBLIC_BLOCKED}
)

# Legacy value — must not be written to new records.
# Use for migration queries only.
LEGACY_PUBLISHED: str = "published"

# ---------------------------------------------------------------------------
# review_status constants
# ---------------------------------------------------------------------------

REVIEW_PENDING: str = "needs_review"
REVIEW_APPROVED: str = "approved"
REVIEW_REJECTED: str = "rejected"

ALL_REVIEW_STATUSES: frozenset[str] = frozenset(
    {REVIEW_PENDING, REVIEW_APPROVED, REVIEW_REJECTED}
)
