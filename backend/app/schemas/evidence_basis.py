"""Evidence basis schema helpers.

Re-exports EvidenceBasis and related types from public_record for
convenience, and provides builders for constructing evidence basis
objects from ORM entities.
"""

from __future__ import annotations

from app.schemas.public_record import EvidenceBasis, RecordLimitation

__all__ = [
    "EvidenceBasis",
    "RecordLimitation",
    "evidence_basis_from_snapshot",
]


def evidence_basis_from_snapshot(snapshot: object) -> EvidenceBasis:
    """Build an EvidenceBasis from a SourceSnapshot ORM instance.

    Uses getattr with safe defaults so this works even if the snapshot
    schema has not been fully migrated.
    """
    return EvidenceBasis(
        evidence_snapshot_id=str(getattr(snapshot, "id", "unknown")),
        evidence_url=None,  # Redacted from public API; admin-only
        source_id=str(getattr(snapshot, "source_key", "unknown")),
        source_type=str(getattr(snapshot, "source_type", "unknown")),
        captured_at=getattr(snapshot, "captured_at", None)
        or getattr(snapshot, "created_at", None),
        last_verified_at=getattr(snapshot, "last_verified_at", None),
        sha256_hash=getattr(snapshot, "content_hash", None),
        storage_backend=getattr(snapshot, "storage_backend", None),
    )
