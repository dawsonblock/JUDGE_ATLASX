"""Parser version enforcement service.

Validates that every ingestion run's declared ``parser_version`` matches the
active contract stored in ``SourceAdapterContract``. A mismatch means the
adapter code has changed without a corresponding contract update, which is a
signal that parsed records may not conform to the expected schema.

Behaviour on mismatch
---------------------
- Run is quarantined automatically.
- Admin is notified via the audit log.
- Public platform does NOT receive any records from the run.

Usage
-----
    from app.services.parser_version_enforcer import ParserVersionEnforcer
    result = ParserVersionEnforcer(session).validate(
        source_key="justice_canada_laws_xml",
        declared_version="1.0",
    )
    if not result.is_valid:
        raise QuarantineException(result.reason)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import SourceAdapterContract

logger = logging.getLogger(__name__)


@dataclass
class VersionValidationResult:
    """Result of a parser version check."""

    source_key: str
    declared_version: str
    expected_version: str | None
    is_valid: bool
    reason: str


class ParserVersionEnforcer:
    """Validates parser versions against registered adapter contracts."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def validate(self, source_key: str, declared_version: str) -> VersionValidationResult:
        """Check that a declared parser version matches the active contract.

        Args:
            source_key: The source registry key (e.g. "justice_canada_laws_xml").
            declared_version: Version string declared by the adapter (e.g. "1.0").

        Returns:
            VersionValidationResult describing whether the version is valid.
        """
        contract = self._get_active_contract(source_key)

        if contract is None:
            logger.warning(
                "[v0] ParserVersionEnforcer: no active contract for source_key=%s", source_key
            )
            return VersionValidationResult(
                source_key=source_key,
                declared_version=declared_version,
                expected_version=None,
                is_valid=False,
                reason=f"No active contract registered for source '{source_key}'. "
                       "Register a contract before ingesting.",
            )

        if declared_version != contract.parser_version:
            logger.error(
                "[v0] Parser version mismatch for %s: declared=%s expected=%s",
                source_key,
                declared_version,
                contract.parser_version,
            )
            return VersionValidationResult(
                source_key=source_key,
                declared_version=declared_version,
                expected_version=contract.parser_version,
                is_valid=False,
                reason=(
                    f"Parser version mismatch: adapter declared '{declared_version}' "
                    f"but contract expects '{contract.parser_version}'. "
                    "Update the contract or revert the adapter change."
                ),
            )

        return VersionValidationResult(
            source_key=source_key,
            declared_version=declared_version,
            expected_version=contract.parser_version,
            is_valid=True,
            reason="Parser version matches active contract.",
        )

    def validate_or_raise(self, source_key: str, declared_version: str) -> None:
        """Validate and raise ValueError on mismatch.

        Convenience wrapper for use in ingestion pipeline.
        """
        result = self.validate(source_key, declared_version)
        if not result.is_valid:
            raise ValueError(result.reason)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_active_contract(self, source_key: str) -> SourceAdapterContract | None:
        """Fetch the active (non-deprecated) contract for a source key."""
        return self.session.execute(
            select(SourceAdapterContract).where(
                SourceAdapterContract.source_key == source_key,
                SourceAdapterContract.status == "active",
            )
        ).scalar_one_or_none()
