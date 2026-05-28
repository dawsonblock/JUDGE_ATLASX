"""
Canonical status constants for public platform linking tables.

These constants ensure consistent status values across statute/news linking
services and maintain a single source of truth.
"""

# StatuteIncidentLink and IncidentNewsLink review statuses
LINK_REVIEW_STATUS_PENDING = "pending"
LINK_REVIEW_STATUS_APPROVED = "approved"
LINK_REVIEW_STATUS_REJECTED = "rejected"
LINK_REVIEW_STATUS_FLAGGED = "flagged"

LINK_REVIEW_STATUSES = frozenset([
    LINK_REVIEW_STATUS_PENDING,
    LINK_REVIEW_STATUS_APPROVED,
    LINK_REVIEW_STATUS_REJECTED,
    LINK_REVIEW_STATUS_FLAGGED,
])

# Link method constants
LINK_METHOD_MANUAL = "manual"
LINK_METHOD_AI_MATCH = "ai_match"
LINK_METHOD_LOCATION_MATCH = "location_match"

LINK_METHODS = frozenset([
    LINK_METHOD_MANUAL,
    LINK_METHOD_AI_MATCH,
    LINK_METHOD_LOCATION_MATCH,
])
