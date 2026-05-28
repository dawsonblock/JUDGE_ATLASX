"""Legal-risk labelling for public platform records.

Attaches a ``legal_risk_level`` label to each GeoLegalEvent before it is
shown on the public platform. The label drives UI warnings and filtering:

  ``low``      – No known publication restrictions. Safe to show.
  ``medium``   – Involves a publication ban, ongoing trial, or youth offender.
                  Show with warning. Some fields must be redacted.
  ``high``     – Active ban, sub-judice, or identified victim. Must NOT be
                  published without explicit human approval.
  ``unknown``  – Insufficient data to classify. Treat as high.

This module contains RULE-BASED classification only. No LLM is involved.
Rules are deterministic and auditable. Add new rules in ``RULES`` below.

Usage
-----
    from app.services.legal_risk_labeller import LegalRiskLabeller
    label = LegalRiskLabeller.classify(event)
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

RiskLevel = str  # "low" | "medium" | "high" | "unknown"


@dataclass
class RiskLabel:
    """Result of a risk classification."""

    level: RiskLevel
    reasons: list[str]
    redact_fields: list[str]
    requires_human_approval: bool

    @property
    def is_safe_to_publish(self) -> bool:
        return self.level == "low" and not self.requires_human_approval


# ---------------------------------------------------------------------------
# Pattern-based risk rules
# ---------------------------------------------------------------------------

# Phrases in title/description that elevate to HIGH risk
HIGH_RISK_PHRASES: list[str] = [
    "publication ban",
    "sub judice",
    "youth offender",
    "young offender",
    "young person",
    "ycja",                  # Youth Criminal Justice Act
    "in camera",
    "victim identity",
    "complainant identity",
    "witness protection",
    "identity of the victim",
    "identity of the complainant",
    "sexual assault",        # Complainant identity often protected
    "sexual offence",
]

# Phrases that elevate to MEDIUM risk (warning shown, some fields redacted)
MEDIUM_RISK_PHRASES: list[str] = [
    "ongoing investigation",
    "charges pending",
    "not guilty",
    "acquitted",
    "charges stayed",
    "bail conditions",
    "publication restrictions",
    "sealing order",
    "mental health tribunal",
    "not criminally responsible",
]

# Crime types that always require at least MEDIUM labelling
HIGH_RISK_CRIME_TYPES: set[str] = {
    "sexual_assault",
    "sexual_offence",
    "child_exploitation",
    "human_trafficking",
}

MEDIUM_RISK_CRIME_TYPES: set[str] = {
    "domestic_violence",
    "stalking",
    "witness_intimidation",
    "youth_offence",
}

# Fields to redact per risk level
REDACT_FOR_HIGH: list[str] = ["exact_address", "victim_name", "complainant_name", "witness_name"]
REDACT_FOR_MEDIUM: list[str] = ["exact_address"]


class LegalRiskLabeller:
    """Classify the legal risk level of a GeoLegalEvent for public display."""

    @classmethod
    def classify(cls, event: Any) -> RiskLabel:
        """Run all rules and return the highest applicable risk label.

        Args:
            event: Any object with attributes: title, description, crime_type.
                   Missing attributes are treated as empty strings.
        """
        reasons: list[str] = []
        level: RiskLevel = "low"

        title = str(getattr(event, "title", "") or "").lower()
        description = str(getattr(event, "description", "") or "").lower()
        crime_type = str(getattr(event, "crime_type", "") or "").lower().replace(" ", "_")
        combined_text = f"{title} {description}"

        # --- Crime type rules ---
        if crime_type in HIGH_RISK_CRIME_TYPES:
            level = cls._elevate(level, "high")
            reasons.append(f"Crime type '{crime_type}' triggers high-risk protection.")

        elif crime_type in MEDIUM_RISK_CRIME_TYPES:
            level = cls._elevate(level, "medium")
            reasons.append(f"Crime type '{crime_type}' requires a publication warning.")

        # --- Phrase rules ---
        for phrase in HIGH_RISK_PHRASES:
            if phrase in combined_text:
                level = cls._elevate(level, "high")
                reasons.append(f"High-risk phrase detected: '{phrase}'")
                break  # One match is enough to trigger high

        if level != "high":
            for phrase in MEDIUM_RISK_PHRASES:
                if phrase in combined_text:
                    level = cls._elevate(level, "medium")
                    reasons.append(f"Medium-risk phrase detected: '{phrase}'")
                    break

        # --- Unknown data rule ---
        if not title and not description and not crime_type:
            level = "unknown"
            reasons.append("Insufficient data to classify risk level.")

        # --- Compute redaction and approval requirements ---
        redact_fields: list[str] = []
        requires_human_approval = False

        if level in ("high", "unknown"):
            redact_fields = REDACT_FOR_HIGH.copy()
            requires_human_approval = True
        elif level == "medium":
            redact_fields = REDACT_FOR_MEDIUM.copy()

        if not reasons:
            reasons.append("No risk indicators found; classified as low risk.")

        label = RiskLabel(
            level=level,
            reasons=reasons,
            redact_fields=redact_fields,
            requires_human_approval=requires_human_approval,
        )

        if level != "low":
            logger.info(
                "[v0] LegalRiskLabeller: event=%s level=%s reasons=%s",
                getattr(event, "id", "?"),
                level,
                reasons,
            )

        return label

    @staticmethod
    def _elevate(current: RiskLevel, candidate: RiskLevel) -> RiskLevel:
        """Return the higher of two risk levels."""
        order = {"low": 0, "medium": 1, "high": 2, "unknown": 3}
        return current if order.get(current, 0) >= order.get(candidate, 0) else candidate
