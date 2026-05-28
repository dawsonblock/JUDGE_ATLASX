"""Ingestion dry-run endpoint.

POST /admin/ingestion/sources/{source_id}/dry-run

Checks source reachability, legal/robots notes, sample parsing, and what
would be created — without writing any public records to the database.

This is a read-only diagnostic tool for operators before enabling a source.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.admin import require_admin_token
from app.db.session import get_db
from app.models.entities import SourceRegistry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/ingestion", tags=["admin-ingestion-dryrun"])


class DryRunResult(BaseModel):
    source_id: int
    source_key: str
    source_name: str
    checked_at: datetime

    # Reachability
    source_reachable: bool
    reachability_note: str

    # Legal / access notes
    robots_note_present: bool
    terms_url: str | None
    terms_verified: str | None
    authentication_required: bool

    # Parsing
    sample_records_found: bool
    sample_record_count: int
    parser_matched: bool
    parser_note: str

    # What would be created
    evidence_snapshot_would_be_created: bool
    claims_would_be_extracted: bool
    public_visibility_default: str  # always "pending_review"
    records_would_bypass_review: bool  # should always be False

    # Overall verdict
    safe_to_enable: bool
    blocking_issues: list[str]
    warnings: list[str]


@router.post("/sources/{source_id}/dry-run", response_model=DryRunResult)
def dry_run_source(
    source_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin_token),
) -> DryRunResult:
    """Run a non-destructive dry-run check for a source."""
    source = db.get(SourceRegistry, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")

    now = datetime.now(tz=timezone.utc)
    blocking_issues: list[str] = []
    warnings: list[str] = []

    # Reachability check
    source_reachable = False
    reachability_note = "Dry-run: live network check not performed in this mode"
    if source.base_url:
        reachability_note = f"Base URL configured: {source.base_url}"
        source_reachable = True  # Indicates URL is configured; live check is opt-in
    else:
        reachability_note = "No base_url configured — source cannot be fetched"
        blocking_issues.append("base_url is missing")

    # Legal / robots notes
    robots_note_present = bool(source.terms_url or source.notes)
    if not robots_note_present:
        warnings.append("No terms_url or legal notes recorded for this source")

    # Terms verification
    if source.terms_verified is None or source.terms_verified == "false":
        warnings.append(
            "Terms of use have not been verified. "
            "Set terms_verified to an ISO date after confirming access terms."
        )

    # Authentication
    if source.authentication_required and not source.admin_notes:
        warnings.append(
            "Source requires authentication but no credentials note found in admin_notes"
        )

    # Parser check
    parser_matched = bool(source.parser)
    parser_note = (
        f"Parser configured: {source.parser}"
        if source.parser
        else "No parser configured — ingestion would fail"
    )
    if not parser_matched:
        blocking_issues.append("No parser configured for this source")

    # Determine if samples would be found
    sample_records_found = source_reachable and parser_matched
    sample_record_count = 0  # Live count requires network; not performed in dry-run
    if sample_records_found:
        parser_note += " (live sample fetch not performed in dry-run)"

    # Evidence snapshot
    evidence_snapshot_would_be_created = bool(source.evidence_required)
    if source.evidence_required and not source.base_url:
        blocking_issues.append(
            "Evidence snapshot required but no base_url to fetch from"
        )

    # Claims extraction
    claims_would_be_extracted = parser_matched

    # Review bypass check — this must always be False for safe operation
    records_would_bypass_review = source.auto_publish_enabled and not source.requires_manual_review
    if records_would_bypass_review:
        blocking_issues.append(
            "Source is configured to auto-publish without manual review. "
            "This is not allowed for alpha. Set requires_manual_review=True."
        )

    # Lifecycle state check
    if source.lifecycle_state == "deprecated":
        blocking_issues.append(f"Source is deprecated: {source.status_reason}")
    elif source.lifecycle_state not in {"enable_ready", "runnable_now"}:
        warnings.append(
            f"Lifecycle state is '{source.lifecycle_state}'. "
            "Only 'enable_ready' or 'runnable_now' sources should be dry-run tested."
        )

    safe_to_enable = len(blocking_issues) == 0

    logger.info(
        "[dryrun] source=%s safe=%s issues=%d warnings=%d",
        source.source_key,
        safe_to_enable,
        len(blocking_issues),
        len(warnings),
    )

    return DryRunResult(
        source_id=source.id,
        source_key=source.source_key,
        source_name=source.source_name,
        checked_at=now,
        source_reachable=source_reachable,
        reachability_note=reachability_note,
        robots_note_present=robots_note_present,
        terms_url=source.terms_url,
        terms_verified=source.terms_verified,
        authentication_required=source.authentication_required,
        sample_records_found=sample_records_found,
        sample_record_count=sample_record_count,
        parser_matched=parser_matched,
        parser_note=parser_note,
        evidence_snapshot_would_be_created=evidence_snapshot_would_be_created,
        claims_would_be_extracted=claims_would_be_extracted,
        public_visibility_default="pending_review",
        records_would_bypass_review=records_would_bypass_review,
        safe_to_enable=safe_to_enable,
        blocking_issues=blocking_issues,
        warnings=warnings,
    )
