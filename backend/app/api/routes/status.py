"""Public ingestion status endpoint.

GET /api/v1/status/ingestion — returns a summary of recent ingestion run
statuses so operators can confirm the pipeline is healthy without admin auth.
Only summary counts and status codes are exposed; no error message text
is included in the public response.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db.session import get_db
from app.ingestion.statuses import COMPLETED, COMPLETED_WITH_WARNINGS, FAILED, RUNNING
from app.models.entities import IngestionRun
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/status", tags=["status"])


class StatusBucket(BaseModel):
    status: str
    count: int


class IngestionStatusResponse(BaseModel):
    window_hours: int
    total_runs: int
    running: int
    completed: int
    completed_with_warnings: int
    failed: int
    other: int
    last_run_at: datetime | None
    buckets: list[StatusBucket]


@router.get("/ingestion", response_model=IngestionStatusResponse)
def get_ingestion_status(
    window_hours: int = Query(
        24, ge=1, le=168, description="Look-back window in hours"
    ),
    db: Session = Depends(get_db),
) -> IngestionStatusResponse:
    """Return ingestion run status summary for the last *window_hours* hours."""
    since = datetime.now(tz=timezone.utc) - timedelta(hours=window_hours)

    rows = db.execute(
        select(
            IngestionRun.status,
            func.count(IngestionRun.id).label("count"),
        )
        .where(IngestionRun.started_at >= since)
        .group_by(IngestionRun.status)
    ).all()

    bucket_map: dict[str, int] = {r.status: r.count for r in rows}
    total = sum(bucket_map.values())

    last_run_at = db.scalar(
        select(func.max(IngestionRun.started_at)).where(
            IngestionRun.started_at >= since
        )
    )

    known = {COMPLETED, COMPLETED_WITH_WARNINGS, FAILED, RUNNING}
    other = sum(v for k, v in bucket_map.items() if k not in known)

    return IngestionStatusResponse(
        window_hours=window_hours,
        total_runs=total,
        running=bucket_map.get(RUNNING, 0),
        completed=bucket_map.get(COMPLETED, 0),
        completed_with_warnings=bucket_map.get(COMPLETED_WITH_WARNINGS, 0),
        failed=bucket_map.get(FAILED, 0),
        other=other,
        last_run_at=last_run_at,
        buckets=[
            StatusBucket(status=k, count=v) for k, v in sorted(bucket_map.items())
        ],
    )
