"""Public source coverage endpoint.

GET /api/v1/sources/coverage — returns aggregate coverage counts broken
down by country, jurisdiction, and source tier.  Only active sources are
included in the summary.
"""

from __future__ import annotations

from app.db.session import get_db
from app.models.entities import SourceRegistry
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/sources", tags=["sources"])


class CoverageItem(BaseModel):
    country: str | None
    jurisdiction: str | None
    source_tier: str
    count: int


class CoverageResponse(BaseModel):
    total_active_sources: int
    coverage: list[CoverageItem]


@router.get("/coverage", response_model=CoverageResponse)
def get_source_coverage(db: Session = Depends(get_db)) -> CoverageResponse:
    """Return aggregate source coverage counts for active sources only."""
    rows = db.execute(
        select(
            SourceRegistry.country,
            SourceRegistry.jurisdiction,
            SourceRegistry.source_tier,
            func.count(SourceRegistry.id).label("count"),
        )
        .where(SourceRegistry.is_active.is_(True))
        .group_by(
            SourceRegistry.country,
            SourceRegistry.jurisdiction,
            SourceRegistry.source_tier,
        )
        .order_by(
            SourceRegistry.country,
            SourceRegistry.jurisdiction,
            SourceRegistry.source_tier,
        )
    ).all()

    total = (
        db.scalar(
            select(func.count(SourceRegistry.id)).where(
                SourceRegistry.is_active.is_(True)
            )
        )
        or 0
    )

    return CoverageResponse(
        total_active_sources=total,
        coverage=[
            CoverageItem(
                country=r.country,
                jurisdiction=r.jurisdiction,
                source_tier=r.source_tier,
                count=r.count,
            )
            for r in rows
        ],
    )
