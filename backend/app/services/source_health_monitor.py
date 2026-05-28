"""Source health monitoring service.

Computes health scores and status summaries for each SourceRegistry entry,
using recent IngestionRun history. Surfaces:
  - ``healthy``   – recent successful runs, error rate < threshold
  - ``degraded``  – elevated error rate or missed expected cadence
  - ``failing``   – all recent runs failed or no runs in window
  - ``unknown``   – not enough data to judge

Used by the admin status page and the alpha readiness endpoint to report
which sources are operationally ready for public platform inclusion.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.entities import IngestionRun, SourceRegistry
from app.ingestion.statuses import COMPLETED, COMPLETED_WITH_WARNINGS, FAILED, QUARANTINED

logger = logging.getLogger(__name__)

HealthStatus = Literal["healthy", "degraded", "failing", "unknown"]

# How far back to look when computing health
HEALTH_WINDOW_DAYS = 14

# How many recent runs to consider
HEALTH_SAMPLE_SIZE = 10

# Error rate thresholds
HEALTHY_MAX_ERROR_RATE = 0.05   # < 5 % errors → healthy
DEGRADED_MAX_ERROR_RATE = 0.25  # < 25 % errors → degraded; ≥ 25 % → failing


@dataclass
class SourceHealthSummary:
    """Health summary for one SourceRegistry entry."""

    source_key: str
    source_name: str
    status: HealthStatus
    last_successful_fetch: datetime | None
    last_error: str | None
    last_error_at: datetime | None
    recent_run_count: int
    error_rate: float  # 0.0 – 1.0
    parser_version: str | None
    is_public_platform_eligible: bool
    reason: str  # Human-readable explanation of current status


class SourceHealthMonitor:
    """Compute health summaries for all (or a subset of) sources."""

    def __init__(self, session: Session) -> None:
        self.session = session

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_all_summaries(self) -> list[SourceHealthSummary]:
        """Return health summaries for every active SourceRegistry entry."""
        sources = self.session.execute(
            select(SourceRegistry).order_by(SourceRegistry.source_name)
        ).scalars().all()
        return [self._summarise(src) for src in sources]

    def get_summary(self, source_key: str) -> SourceHealthSummary | None:
        """Return health summary for one source, or None if not found."""
        src = self.session.execute(
            select(SourceRegistry).where(SourceRegistry.source_key == source_key)
        ).scalar_one_or_none()
        return self._summarise(src) if src else None

    def get_public_eligible(self) -> list[SourceHealthSummary]:
        """Return only sources eligible for the public platform."""
        return [s for s in self.get_all_summaries() if s.is_public_platform_eligible]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _summarise(self, src: SourceRegistry) -> SourceHealthSummary:
        cutoff = datetime.now(timezone.utc) - timedelta(days=HEALTH_WINDOW_DAYS)

        recent_runs = self.session.execute(
            select(IngestionRun)
            .where(
                IngestionRun.source_name == src.source_name,
                IngestionRun.started_at >= cutoff,
            )
            .order_by(desc(IngestionRun.started_at))
            .limit(HEALTH_SAMPLE_SIZE)
        ).scalars().all()

        status, error_rate, reason = self._compute_status(src, recent_runs)
        eligible = self._is_eligible(src, status)

        return SourceHealthSummary(
            source_key=src.source_key,
            source_name=src.source_name,
            status=status,
            last_successful_fetch=src.last_successful_fetch,
            last_error=src.last_error,
            last_error_at=src.last_error_at,
            recent_run_count=len(recent_runs),
            error_rate=error_rate,
            parser_version=src.parser_version,
            is_public_platform_eligible=eligible,
            reason=reason,
        )

    def _compute_status(
        self,
        src: SourceRegistry,
        recent_runs: list[IngestionRun],
    ) -> tuple[HealthStatus, float, str]:
        if not src.is_active:
            return "unknown", 0.0, "Source is not active"

        if not recent_runs:
            if src.last_successful_fetch is None:
                return "unknown", 0.0, "No ingestion runs found"
            return "degraded", 0.0, f"No runs in last {HEALTH_WINDOW_DAYS} days"

        failed_statuses = {FAILED, QUARANTINED}
        failed_count = sum(1 for r in recent_runs if r.status in failed_statuses)
        error_rate = failed_count / len(recent_runs)

        if error_rate <= HEALTHY_MAX_ERROR_RATE:
            return "healthy", error_rate, "Recent runs completing successfully"
        elif error_rate <= DEGRADED_MAX_ERROR_RATE:
            return (
                "degraded",
                error_rate,
                f"Elevated error rate: {error_rate:.0%} of recent runs failed",
            )
        else:
            return (
                "failing",
                error_rate,
                f"High error rate: {error_rate:.0%} of recent runs failed",
            )

    @staticmethod
    def _is_eligible(src: SourceRegistry, status: HealthStatus) -> bool:
        """A source is eligible for the public platform when it is healthy
        and requires human review (i.e. not fully automated without review)."""
        return (
            status == "healthy"
            and src.is_active
            and bool(src.parser_version)
        )
