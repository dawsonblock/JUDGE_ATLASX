"""CKAN adapter review-payload schema contract."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

SCHEMA_VERSION = "ckan_crime_record_v1"


class CKANCrimeReviewPayload(BaseModel):
    """Normalized review payload produced by the CKAN adapter."""

    model_config = ConfigDict(extra="allow")

    source_key: str
    candidate_record_type: str
    external_id: str
    coordinate_precision: str
    raw: dict[str, Any]
    parser_version: str
    schema_version: str = SCHEMA_VERSION
    public_record_authority: str
    ingestion_mode: str = "review_only"
    source_url: str


def validate_ckan_row(row: Any) -> bool:
    """Return True when row is a non-empty object suitable for normalization."""
    return isinstance(row, dict) and bool(row)


def build_ckan_review_payload(
    *,
    source_key: str,
    candidate_record_type: str,
    external_id: str,
    coordinate_precision: str,
    raw: dict[str, Any],
    parser_version: str,
    public_record_authority: str,
    source_url: str,
) -> dict[str, Any]:
    """Build a validated review-only payload for CKAN-derived rows."""
    payload = CKANCrimeReviewPayload(
        source_key=source_key,
        candidate_record_type=candidate_record_type,
        external_id=external_id,
        coordinate_precision=coordinate_precision,
        raw=raw,
        parser_version=parser_version,
        public_record_authority=public_record_authority,
        source_url=source_url,
    )
    return payload.model_dump()
