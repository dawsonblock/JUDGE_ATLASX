"""Public ingestion status endpoint.

GET /api/v1/status/ingestion — returns a summary of recent ingestion run
statuses so operators can confirm the pipeline is healthy without admin auth.
Only summary counts and status codes are exposed; no error message text
is included in the public response.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.core.config import get_settings
from app.core.runtime_profile import resolve_runtime_profile
from app.db.session import get_db
from app.ingestion.statuses import COMPLETED, COMPLETED_WITH_WARNINGS, FAILED, RUNNING
from app.models.entities import IngestionRun, SourceRegistry
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

router = APIRouter(tags=["status"])


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


class AlphaReadinessResponse(BaseModel):
    alpha_gate_passed: bool
    production_ready: bool
    proof_chain_complete: bool
    archive_self_verifying: bool
    runnable_sources: int
    total_sources: int
    evidence_store: str
    public_review_gate: str
    experimental_live_map: str
    workflow_admin: str
    storage_backend: str
    queue_backend: str
    rate_limit_backend: str
    warnings: list[str]


def _load_release_gate(root: Path) -> dict:
    release_gate_path = root / "artifacts/proof/current/release_gate.json"
    if not release_gate_path.exists():
        return {}
    try:
        data = json.loads(release_gate_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _check_exists(path_value: str | None) -> bool:
    if not path_value:
        return False
    try:
        return Path(path_value).expanduser().exists()
    except OSError:
        return False


@router.get("/api/v1/status/ingestion", response_model=IngestionStatusResponse)
@router.get("/status/ingestion", response_model=IngestionStatusResponse)
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


@router.get("/status/alpha-readiness", response_model=AlphaReadinessResponse)
@router.get("/api/v1/status/alpha-readiness", response_model=AlphaReadinessResponse)
def get_alpha_readiness(db: Session = Depends(get_db)) -> AlphaReadinessResponse:
    settings = get_settings()
    runtime_profile = resolve_runtime_profile(settings)

    repo_root = Path(__file__).resolve().parents[4]
    release_gate = _load_release_gate(repo_root)
    checks = release_gate.get("checks")
    check_items = checks if isinstance(checks, list) else []

    alpha_gate_passed = bool(release_gate.get("alpha_gate_passed", False))
    production_ready = bool(release_gate.get("production_ready", False))
    proof_chain_complete = bool(release_gate) and len(check_items) > 0

    archive_self_verifying = any(
        isinstance(item, dict)
        and item.get("name") == "archive_validation"
        and str(item.get("status", "")).upper() == "PASS"
        for item in check_items
    )

    total_sources = db.scalar(select(func.count(SourceRegistry.id))) or 0
    runnable_sources = db.scalar(
        select(func.count(SourceRegistry.id)).where(SourceRegistry.lifecycle_state == "runnable")
    ) or 0

    warnings: list[str] = []
    if not alpha_gate_passed:
        warnings.append("alpha_gate_not_passed")
    if production_ready:
        warnings.append("production_ready_true_requires_manual_verification")
    if not proof_chain_complete:
        warnings.append("proof_chain_incomplete")
    if not archive_self_verifying:
        warnings.append("archive_validation_not_verified")
    if runnable_sources == 0:
        warnings.append("no_runnable_sources")
    if not settings.evidence_store_required:
        warnings.append("evidence_store_not_required")
    if settings.enable_experimental_live_map:
        warnings.append("experimental_live_map_enabled")
    if settings.enable_workflow_admin:
        warnings.append("workflow_admin_enabled")

    evidence_store_ok = _check_exists(settings.evidence_store_root)
    if not evidence_store_ok:
        warnings.append("evidence_store_root_missing")

    return AlphaReadinessResponse(
        alpha_gate_passed=alpha_gate_passed,
        production_ready=production_ready,
        proof_chain_complete=proof_chain_complete,
        archive_self_verifying=archive_self_verifying,
        runnable_sources=int(runnable_sources),
        total_sources=int(total_sources),
        evidence_store="ok" if evidence_store_ok else "missing",
        public_review_gate="enabled" if settings.enable_admin_review else "disabled",
        experimental_live_map="enabled" if settings.enable_experimental_live_map else "disabled",
        workflow_admin="enabled" if settings.enable_workflow_admin else "disabled",
        storage_backend=settings.storage_backend,
        queue_backend=settings.ingestion_queue_backend,
        rate_limit_backend=settings.rate_limit_backend,
        warnings=warnings + [f"runtime_profile={runtime_profile.name}"],
    )
