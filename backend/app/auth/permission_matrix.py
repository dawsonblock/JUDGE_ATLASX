"""Role-based permission matrix for JUDGE_ATLASX.

Defines which actions each role may perform. This is the single source of
truth for authorisation checks across the application.

Roles
-----
  ``public``            – Unauthenticated public user (read-only, published records only)
  ``data_entry``        – Ingests and tags source records; no publish authority
  ``reviewer``          – Approves/rejects records; cannot ingest
  ``senior_reviewer``   – Reviewer + can override quarantine and approve high-risk records
  ``admin``             – Full access; can manage users, sources, and config
  ``system``            – Internal service-to-service calls (not human)

Usage
-----
    from app.auth.permission_matrix import can, Permission
    if not can(role="reviewer", action=Permission.APPROVE_RECORD):
        raise HTTPException(403, "Insufficient permissions")
"""

from __future__ import annotations

from enum import Enum
from typing import FrozenSet


class Permission(str, Enum):
    # Public read
    READ_PUBLISHED_INCIDENTS = "read_published_incidents"
    READ_PUBLISHED_STATUTES = "read_published_statutes"

    # Internal read
    READ_ALL_INCIDENTS = "read_all_incidents"
    READ_QUARANTINED_RUNS = "read_quarantined_runs"
    READ_SOURCE_REGISTRY = "read_source_registry"
    READ_AUDIT_LOG = "read_audit_log"

    # Ingestion
    TRIGGER_INGESTION = "trigger_ingestion"
    TRIGGER_DRY_RUN = "trigger_dry_run"
    RELEASE_QUARANTINE = "release_quarantine"

    # Review
    APPROVE_RECORD = "approve_record"
    REJECT_RECORD = "reject_record"
    APPROVE_HIGH_RISK_RECORD = "approve_high_risk_record"
    DISPUTE_RECORD = "dispute_record"

    # Source management
    ENABLE_SOURCE = "enable_source"
    DISABLE_SOURCE = "disable_source"
    EDIT_SOURCE_CONFIG = "edit_source_config"

    # Publishing
    PUBLISH_RECORD = "publish_record"
    SUPPRESS_RECORD = "suppress_record"
    MARK_RECORD_STALE = "mark_record_stale"

    # Administration
    MANAGE_USERS = "manage_users"
    MANAGE_FEATURE_FLAGS = "manage_feature_flags"
    VIEW_ALPHA_STATUS = "view_alpha_status"


# ---------------------------------------------------------------------------
# Role → permission mapping (immutable sets)
# ---------------------------------------------------------------------------

_MATRIX: dict[str, FrozenSet[Permission]] = {
    "public": frozenset(
        {
            Permission.READ_PUBLISHED_INCIDENTS,
            Permission.READ_PUBLISHED_STATUTES,
        }
    ),
    "data_entry": frozenset(
        {
            Permission.READ_PUBLISHED_INCIDENTS,
            Permission.READ_PUBLISHED_STATUTES,
            Permission.READ_ALL_INCIDENTS,
            Permission.READ_SOURCE_REGISTRY,
            Permission.TRIGGER_DRY_RUN,
            Permission.TRIGGER_INGESTION,
        }
    ),
    "reviewer": frozenset(
        {
            Permission.READ_PUBLISHED_INCIDENTS,
            Permission.READ_PUBLISHED_STATUTES,
            Permission.READ_ALL_INCIDENTS,
            Permission.READ_QUARANTINED_RUNS,
            Permission.READ_SOURCE_REGISTRY,
            Permission.APPROVE_RECORD,
            Permission.REJECT_RECORD,
            Permission.DISPUTE_RECORD,
            Permission.PUBLISH_RECORD,
            Permission.SUPPRESS_RECORD,
        }
    ),
    "senior_reviewer": frozenset(
        {
            Permission.READ_PUBLISHED_INCIDENTS,
            Permission.READ_PUBLISHED_STATUTES,
            Permission.READ_ALL_INCIDENTS,
            Permission.READ_QUARANTINED_RUNS,
            Permission.READ_SOURCE_REGISTRY,
            Permission.READ_AUDIT_LOG,
            Permission.APPROVE_RECORD,
            Permission.REJECT_RECORD,
            Permission.APPROVE_HIGH_RISK_RECORD,
            Permission.DISPUTE_RECORD,
            Permission.RELEASE_QUARANTINE,
            Permission.PUBLISH_RECORD,
            Permission.SUPPRESS_RECORD,
            Permission.MARK_RECORD_STALE,
            Permission.TRIGGER_DRY_RUN,
            Permission.VIEW_ALPHA_STATUS,
        }
    ),
    "admin": frozenset(Permission),  # All permissions
    "system": frozenset(
        {
            Permission.READ_ALL_INCIDENTS,
            Permission.TRIGGER_INGESTION,
            Permission.PUBLISH_RECORD,
            Permission.SUPPRESS_RECORD,
            Permission.MARK_RECORD_STALE,
            Permission.READ_QUARANTINED_RUNS,
            Permission.RELEASE_QUARANTINE,
        }
    ),
}


def can(role: str, action: Permission) -> bool:
    """Return True if ``role`` is allowed to perform ``action``.

    Unknown roles are treated as ``public`` (least privilege).
    """
    role_perms = _MATRIX.get(role, _MATRIX["public"])
    return action in role_perms


def get_permissions(role: str) -> FrozenSet[Permission]:
    """Return the full set of permissions for a role."""
    return _MATRIX.get(role, _MATRIX["public"])


def all_roles() -> list[str]:
    """Return all known role names."""
    return list(_MATRIX.keys())
