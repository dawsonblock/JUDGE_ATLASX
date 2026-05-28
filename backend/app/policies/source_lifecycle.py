"""
Canonical source lifecycle state constants for SourceRegistry.lifecycle_state.

These are the authoritative DB-level values.  Import these constants instead
of hardcoding strings.

IMPORTANT: DB values vs report labels are intentionally different:
    DB value         | Report / UI label
    ---------------- | -----------------
    runnable         | runnable_now
    runnable_disabled| enable_ready
    deprecated       | deprecated

Do NOT store "runnable_now" or "enable_ready" as lifecycle_state in the DB.
Do NOT use these report labels in SQLAlchemy filter expressions.

Machine states (automated ingest can act on these):
    runnable          — source is active and scheduled for ingest
    runnable_disabled — configured but disabled; can be enabled without code
    deprecated        — decommissioned; kept for historical reference

Non-machine states (ingest never acts on these):
    portal_reference  — link to an external portal; not a runnable ingest source
    disabled_stub     — placeholder; implementation not complete
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# DB-level lifecycle_state constants
# ---------------------------------------------------------------------------

SOURCE_RUNNABLE: str = "runnable"
SOURCE_RUNNABLE_DISABLED: str = "runnable_disabled"
SOURCE_DEPRECATED: str = "deprecated"
SOURCE_PORTAL_REFERENCE: str = "portal_reference"
SOURCE_DISABLED_STUB: str = "disabled_stub"

# All valid lifecycle_state values.
ALL_LIFECYCLE_STATES: frozenset[str] = frozenset(
    {
        SOURCE_RUNNABLE,
        SOURCE_RUNNABLE_DISABLED,
        SOURCE_DEPRECATED,
        SOURCE_PORTAL_REFERENCE,
        SOURCE_DISABLED_STUB,
    }
)

# States where the automated ingest runner can act on the source.
SOURCE_MACHINE_STATES: frozenset[str] = frozenset(
    {SOURCE_RUNNABLE, SOURCE_RUNNABLE_DISABLED, SOURCE_DEPRECATED}
)

# States that are reference/placeholder only (no ingest).
SOURCE_NON_MACHINE_STATES: frozenset[str] = frozenset(
    {SOURCE_PORTAL_REFERENCE, SOURCE_DISABLED_STUB}
)

# ---------------------------------------------------------------------------
# Report / UI label helpers
#
# Use these when building human-facing reports or API responses.
# Never use them as DB filter values.
# ---------------------------------------------------------------------------

REPORT_LABEL_RUNNABLE: str = "runnable_now"
REPORT_LABEL_ENABLE_READY: str = "enable_ready"
REPORT_LABEL_DEPRECATED: str = "deprecated"

# Map from DB value -> report label for display purposes.
LIFECYCLE_REPORT_LABELS: dict[str, str] = {
    SOURCE_RUNNABLE: REPORT_LABEL_RUNNABLE,
    SOURCE_RUNNABLE_DISABLED: REPORT_LABEL_ENABLE_READY,
    SOURCE_DEPRECATED: REPORT_LABEL_DEPRECATED,
    SOURCE_PORTAL_REFERENCE: "portal_reference",
    SOURCE_DISABLED_STUB: "disabled_stub",
}
