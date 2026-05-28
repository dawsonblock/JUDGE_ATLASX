"""Alpha readiness status endpoint.

GET /api/v1/status/alpha-readiness

Returns a structured status report for the alpha.  No sensitive data is
included; this endpoint is intended for the admin status page and for
operators verifying the system before testing.
"""

from __future__ import annotations

import os
from pathlib import Path

from app.core.config import get_settings
from app.core.runtime_profile import get_active_profile, get_profile_warnings
from app.db.session import get_db
from app.models.entities import SourceRegistry
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/status", tags=["status"])


class AlphaReadinessResponse(BaseModel):
    alpha_gate_passed: bool
    production_ready: bool
    proof_chain_complete: bool
    archive_self_verifying: bool

    # Source coverage
    runnable_sources: int
    total_sources: int
    enable_ready_sources: int
    deprecated_sources: int

    # Infrastructure
    evidence_store: str  # "ok" | "missing" | "not_configured"
    storage_backend: str
    queue_backend: str
    rate_limit_backend: str

    # Feature gates
    public_review_gate: str  # "enabled" | "disabled"
    public_platform: str  # "enabled" | "disabled"
    experimental_live_map: str  # "enabled" | "disabled"
    workflow_admin: str  # "enabled" | "disabled"

    # Runtime profile
    runtime_profile: str

    # Warnings — never hidden
    warnings: list[str]


def _evidence_store_status(settings) -> str:
    root = settings.evidence_store_root
    if not root:
        return "not_configured"
    if Path(root).is_dir():
        return "ok"
    return "missing"


def _proof_chain_complete() -> bool:
    """Check if the proof manifest file exists and is non-empty."""
    candidates = [
        Path("CURRENT_PROOF.md"),
        Path("PROOF_STATUS.md"),
        Path("REPAIR_PROOF.json"),
    ]
    return any(p.exists() and p.stat().st_size > 0 for p in candidates)


@router.get("/alpha-readiness", response_model=AlphaReadinessResponse)
def get_alpha_readiness(db: Session = Depends(get_db)) -> AlphaReadinessResponse:
    """Return structured alpha readiness status for admin dashboard."""
    settings = get_settings()
    profile = get_active_profile()
    profile_warnings = get_profile_warnings(profile)

    # Source coverage from DB
    total_sources = db.scalar(select(func.count(SourceRegistry.id))) or 0
    runnable_sources = db.scalar(
        select(func.count(SourceRegistry.id)).where(
            SourceRegistry.lifecycle_state == "runnable_now"
        )
    ) or 0
    enable_ready_sources = db.scalar(
        select(func.count(SourceRegistry.id)).where(
            SourceRegistry.lifecycle_state == "enable_ready"
        )
    ) or 0
    deprecated_sources = db.scalar(
        select(func.count(SourceRegistry.id)).where(
            SourceRegistry.lifecycle_state == "deprecated"
        )
    ) or 0

    evidence_store = _evidence_store_status(settings)
    proof_chain = _proof_chain_complete()
    warnings: list[str] = list(profile_warnings)

    if evidence_store == "missing":
        warnings.append("Evidence store root is configured but directory does not exist.")
    if evidence_store == "not_configured":
        warnings.append("JTA_EVIDENCE_STORE_ROOT is not set. Evidence snapshots unavailable.")
    if runnable_sources == 0:
        warnings.append("No sources are currently runnable. Check source lifecycle states.")
    if not proof_chain:
        warnings.append("Proof manifest not found. Run: python3 scripts/generate_current_proof.py")

    # Alpha gate passes if review gate is enabled and evidence store is not broken
    public_review_gate_enabled = profile.public_review_gate_required
    alpha_gate_passed = (
        public_review_gate_enabled
        and evidence_store in {"ok", "not_configured"}
        and len([w for w in warnings if "FAIL" in w.upper()]) == 0
    )

    return AlphaReadinessResponse(
        alpha_gate_passed=alpha_gate_passed,
        production_ready=False,  # Never true at alpha
        proof_chain_complete=proof_chain,
        archive_self_verifying=proof_chain,
        runnable_sources=runnable_sources,
        total_sources=total_sources,
        enable_ready_sources=enable_ready_sources,
        deprecated_sources=deprecated_sources,
        evidence_store=evidence_store,
        storage_backend=settings.storage_backend,
        queue_backend=settings.ingestion_queue_backend,
        rate_limit_backend=settings.rate_limit_backend,
        public_review_gate="enabled" if public_review_gate_enabled else "disabled",
        public_platform="enabled" if settings.enable_public_platform else "disabled",
        experimental_live_map="enabled" if settings.enable_experimental_live_map else "disabled",
        workflow_admin="enabled" if settings.enable_workflow_admin else "disabled",
        runtime_profile=profile.name,
        warnings=warnings,
    )
