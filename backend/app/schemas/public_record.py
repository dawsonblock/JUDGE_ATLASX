"""Public record response schema.

Every public legal/incident response must include evidence basis metadata.
Naked claims (records without evidence_snapshot_id and review attribution)
must not be returned via the public API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator


class EvidenceBasis(BaseModel):
    """Evidence metadata that must accompany every public record."""

    evidence_snapshot_id: str = Field(
        description="Opaque identifier of the archived evidence snapshot"
    )
    evidence_url: str | None = Field(
        None,
        description="URL to the evidence snapshot (admin-only; redacted in public API)",
    )
    source_id: str = Field(description="Source registry key")
    source_type: str = Field(description="Type of the originating source")
    captured_at: datetime = Field(description="When the evidence snapshot was captured")
    last_verified_at: datetime | None = Field(
        None, description="When the evidence was last re-verified"
    )
    sha256_hash: str | None = Field(
        None, description="SHA-256 hash of the captured source material"
    )
    storage_backend: str | None = Field(
        None, description="Where the snapshot is stored (local, minio, azure_blob)"
    )


class RecordLimitation(BaseModel):
    """A limitation or caveat that applies to this record."""

    code: str = Field(description="Machine-readable limitation code, e.g. 'stale_data'")
    message: str = Field(description="Human-readable limitation message")
    severity: str = Field(
        "warning",
        description="'info', 'warning', or 'error'",
    )


class PublicRecord(BaseModel):
    """Base schema for every public-facing legal or incident record.

    All public API responses must inherit from or compose this schema.
    The evidence_basis field is always required; naked claims are forbidden.
    """

    id: str = Field(description="Stable public record identifier")
    record_type: str = Field(
        description="Type of record, e.g. 'legislation', 'court_outcome', 'crime_incident'"
    )
    summary: str = Field(
        description=(
            "Neutral, source-attributed summary of the record. "
            "Must not use language that implies guilt or draws legal conclusions."
        )
    )
    review_status: str = Field(
        "approved",
        description="Must be 'approved' for public records",
    )
    evidence_basis: EvidenceBasis = Field(
        description="Evidence metadata — required for all public records"
    )
    limitations: list[RecordLimitation] = Field(
        default_factory=list,
        description="Limitations or caveats that apply to this record",
    )
    legal_risk_label: str | None = Field(
        None,
        description="Risk label: 'low', 'medium', 'high', 'restricted'",
    )

    # Reviewer attribution (anonymized for public API)
    reviewer_attributed: bool = Field(
        False,
        description="Whether a human reviewer attributed this record",
    )

    # Optional extended fields
    extra: dict[str, Any] = Field(
        default_factory=dict,
        description="Record-type-specific fields",
    )

    @model_validator(mode="after")
    def enforce_approved_status(self) -> "PublicRecord":
        """Public records must always have review_status='approved'."""
        if self.review_status != "approved":
            raise ValueError(
                f"Public records must have review_status='approved', got {self.review_status!r}. "
                "Unreviewed records must not be returned via the public API."
            )
        return self

    @model_validator(mode="after")
    def enforce_reviewer_attribution(self) -> "PublicRecord":
        """Public records must have been reviewed by a human."""
        if not self.reviewer_attributed:
            raise ValueError(
                "Public records must have reviewer_attributed=True. "
                "Ensure a human reviewer has approved this record before publishing."
            )
        return self
