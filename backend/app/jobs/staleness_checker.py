"""Staleness checker job for public platform records.

Marks GeoLegalEvents as stale when they have not been refreshed by a source
within the expected freshness window. Stale records are hidden from the public
platform until re-confirmed by a fresh ingestion run.

Each SourceRegistry entry has a ``freshness_window_days`` field. If the source
has not produced a new IngestionRun referencing a record within that window,
the record is marked stale.

Run via:
    python -m app.jobs.staleness_checker          # one-shot check
    # or from your scheduler/cron/Celery beat task
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.geo_legal_event import GeoLegalEvent

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# Default freshness window when source does not specify one
DEFAULT_FRESHNESS_WINDOW_DAYS = 30

# Publish status values
PUBLISH_STATUS_PUBLISHED = "published"
PUBLISH_STATUS_STALE = "stale"


@dataclass
class StalenessReport:
    """Summary of a staleness check run."""

    checked_at: datetime
    total_checked: int
    newly_stale: int
    already_stale: int
    still_fresh: int
    stale_ids: list[int]


def run_staleness_check(session: Session, dry_run: bool = False) -> StalenessReport:
    """Check all published incidents for staleness and mark them accordingly.

    Args:
        session: SQLAlchemy session.
        dry_run: If True, compute but do not commit any changes.

    Returns:
        StalenessReport with counts and affected IDs.
    """
    now = datetime.now(timezone.utc)
    logger.info("[v0] Starting staleness check at %s (dry_run=%s)", now.isoformat(), dry_run)

    # Load all published events
    result = session.execute(
        select(GeoLegalEvent).where(
            GeoLegalEvent.publish_status.in_([PUBLISH_STATUS_PUBLISHED, PUBLISH_STATUS_STALE])
        )
    )
    events: list[GeoLegalEvent] = list(result.scalars().all())

    newly_stale: list[int] = []
    already_stale: list[int] = []
    still_fresh: list[int] = []

    for event in events:
        freshness_days = _get_freshness_window(event)
        cutoff = now - timedelta(days=freshness_days)

        last_seen = _get_last_seen(event)
        is_currently_stale = getattr(event, "publish_status", None) == PUBLISH_STATUS_STALE

        if last_seen is None or last_seen < cutoff:
            # Record is stale
            if is_currently_stale:
                already_stale.append(event.id)
            else:
                newly_stale.append(event.id)
                logger.info(
                    "[v0] Marking incident %s stale (last_seen=%s, cutoff=%s)",
                    event.id,
                    last_seen,
                    cutoff,
                )
                if not dry_run:
                    event.publish_status = PUBLISH_STATUS_STALE  # type: ignore[assignment]
        else:
            still_fresh.append(event.id)
            # If it was stale before but is now fresh, restore it
            if is_currently_stale and not dry_run:
                event.publish_status = PUBLISH_STATUS_PUBLISHED  # type: ignore[assignment]

    if not dry_run:
        session.commit()
        logger.info("[v0] Committed staleness updates: %d newly stale", len(newly_stale))
    else:
        logger.info("[v0] Dry-run: would mark %d as stale", len(newly_stale))

    return StalenessReport(
        checked_at=now,
        total_checked=len(events),
        newly_stale=len(newly_stale),
        already_stale=len(already_stale),
        still_fresh=len(still_fresh),
        stale_ids=newly_stale,
    )


def _get_freshness_window(event: GeoLegalEvent) -> int:
    """Return the freshness window in days for an event.

    Tries to read from the event's linked source; falls back to default.
    """
    # If the event has a source_key attribute, we could look up the source
    # For now use the default — this will be expanded when source FK is added
    return DEFAULT_FRESHNESS_WINDOW_DAYS


def _get_last_seen(event: GeoLegalEvent) -> datetime | None:
    """Return the most recent time this incident was confirmed by a source run.

    Uses updated_at as a proxy for last confirmation.
    """
    val = getattr(event, "updated_at", None) or getattr(event, "created_at", None)
    if val is None:
        return None
    # Ensure timezone-aware
    if isinstance(val, datetime) and val.tzinfo is None:
        val = val.replace(tzinfo=timezone.utc)
    return val


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run staleness check on published incidents")
    parser.add_argument("--dry-run", action="store_true", help="Do not commit changes")
    args = parser.parse_args()

    with SessionLocal() as db:
        report = run_staleness_check(db, dry_run=args.dry_run)

    print(f"Staleness check complete at {report.checked_at.isoformat()}")
    print(f"  Checked:      {report.total_checked}")
    print(f"  Newly stale:  {report.newly_stale}")
    print(f"  Already stale:{report.already_stale}")
    print(f"  Still fresh:  {report.still_fresh}")
    if report.stale_ids:
        print(f"  Stale IDs:   {report.stale_ids}")
