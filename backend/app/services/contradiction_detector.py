"""Contradiction detector for public record claims.

Detects when two ingested records from different sources make conflicting
factual claims about the same incident (e.g. different dates, different
crime types, different locations). Contradictions are flagged for human
review and are NEVER published to the public platform until resolved.

Usage
-----
    from app.services.contradiction_detector import ContradictionDetector
    report = ContradictionDetector(session).check(incident_id=42)
    if report.has_contradictions:
        # block publication, log for admin review
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.geo_legal_event import GeoLegalEvent

logger = logging.getLogger(__name__)

# Fields that, if they differ across sources for the same event,
# constitute a contradiction requiring human review.
CONTRADICTION_FIELDS: list[str] = [
    "occurred_at",
    "crime_type",
    "jurisdiction",
    "lat",
    "lng",
    "title",
]

# Tolerance for float comparisons (coordinates)
COORD_TOLERANCE = 0.0001  # ~10 m


@dataclass
class FieldContradiction:
    """A single field-level contradiction between two source claims."""

    field_name: str
    source_a: str
    value_a: Any
    source_b: str
    value_b: Any
    severity: str  # "blocking" | "advisory"


@dataclass
class ContradictionReport:
    """Full contradiction report for one incident."""

    incident_id: int | str
    checked_at: datetime
    has_contradictions: bool
    blocking_count: int
    advisory_count: int
    contradictions: list[FieldContradiction] = field(default_factory=list)

    @property
    def is_publication_blocked(self) -> bool:
        """True if this incident must NOT be published until resolved."""
        return self.blocking_count > 0


class ContradictionDetector:
    """Detect field-level contradictions between source claims for an incident.

    This operates on the *already-persisted* canonical GeoLegalEvent and
    checks its provenance metadata (source_key, parser_version) against
    sibling records that share the same external reference key.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def check(self, incident_id: int | str) -> ContradictionReport:
        """Run contradiction checks for a single incident.

        Args:
            incident_id: Primary key of the GeoLegalEvent to check.

        Returns:
            ContradictionReport describing any contradictions found.
        """
        event = self.session.get(GeoLegalEvent, incident_id)
        if event is None:
            logger.warning("[v0] ContradictionDetector: incident %s not found", incident_id)
            return ContradictionReport(
                incident_id=incident_id,
                checked_at=datetime.utcnow(),
                has_contradictions=False,
                blocking_count=0,
                advisory_count=0,
            )

        # Find sibling events: same external_ref_key but different source_key
        siblings = self._find_siblings(event)
        contradictions: list[FieldContradiction] = []

        for sibling in siblings:
            contradictions.extend(self._compare(event, sibling))

        blocking = [c for c in contradictions if c.severity == "blocking"]
        advisory = [c for c in contradictions if c.severity == "advisory"]

        report = ContradictionReport(
            incident_id=incident_id,
            checked_at=datetime.utcnow(),
            has_contradictions=bool(contradictions),
            blocking_count=len(blocking),
            advisory_count=len(advisory),
            contradictions=contradictions,
        )

        if report.has_contradictions:
            logger.warning(
                "[v0] Incident %s has %d blocking + %d advisory contradictions",
                incident_id,
                report.blocking_count,
                report.advisory_count,
            )

        return report

    def check_batch(self, incident_ids: list[int | str]) -> list[ContradictionReport]:
        """Run contradiction checks across multiple incidents."""
        return [self.check(iid) for iid in incident_ids]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_siblings(self, event: GeoLegalEvent) -> list[GeoLegalEvent]:
        """Find other GeoLegalEvents that share the same external_ref_key."""
        if not getattr(event, "external_ref_key", None):
            return []

        result = self.session.execute(
            select(GeoLegalEvent).where(
                GeoLegalEvent.external_ref_key == event.external_ref_key,
                GeoLegalEvent.id != event.id,
            )
        )
        return list(result.scalars().all())

    def _compare(
        self, canonical: GeoLegalEvent, sibling: GeoLegalEvent
    ) -> list[FieldContradiction]:
        """Compare two events field by field and return all contradictions."""
        contradictions: list[FieldContradiction] = []

        source_a = getattr(canonical, "source_key", "canonical")
        source_b = getattr(sibling, "source_key", "sibling")

        for field_name in CONTRADICTION_FIELDS:
            val_a = getattr(canonical, field_name, None)
            val_b = getattr(sibling, field_name, None)

            if val_a is None and val_b is None:
                continue

            differs = self._values_differ(field_name, val_a, val_b)
            if not differs:
                continue

            severity = self._classify_severity(field_name)
            contradictions.append(
                FieldContradiction(
                    field_name=field_name,
                    source_a=source_a,
                    value_a=val_a,
                    source_b=source_b,
                    value_b=val_b,
                    severity=severity,
                )
            )

        return contradictions

    def _values_differ(self, field_name: str, val_a: Any, val_b: Any) -> bool:
        """Compare two field values, using tolerance for floats."""
        if val_a is None or val_b is None:
            return val_a != val_b

        # Coordinate fields — allow small tolerance
        if field_name in ("lat", "lng"):
            try:
                return abs(float(val_a) - float(val_b)) > COORD_TOLERANCE
            except (TypeError, ValueError):
                pass

        # Datetime fields — compare date portion only
        if field_name == "occurred_at":
            if isinstance(val_a, datetime) and isinstance(val_b, datetime):
                return val_a.date() != val_b.date()

        return val_a != val_b

    @staticmethod
    def _classify_severity(field_name: str) -> str:
        """Classify a contradiction as blocking or advisory.

        Blocking contradictions prevent publication.
        Advisory contradictions are logged for review but do not block.
        """
        blocking_fields = {"crime_type", "occurred_at", "jurisdiction"}
        return "blocking" if field_name in blocking_fields else "advisory"
