"""GeoLegalEvent schema for normalized map-facing event layer.

This schema provides one normalized object that every map layer can render.
It abstracts over the underlying data models (Event, CrimeIncident, MemoryClaim, etc.)
to provide a consistent interface for the live map API.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class GeoLegalEvent(BaseModel):
    """Normalized legal event for map rendering.

    The map never renders raw scraped data directly. It renders only GeoLegalEvent
    rows derived from evidence-backed claims.
    """

    # Core identification
    id: str
    event_type: str

    # Content
    title: str
    description: str | None = None

    # Location
    lat: float | None = None
    lng: float | None = None
    location_name: str | None = None

    # Temporal
    occurred_at: datetime | None = None
    published_at: datetime | None = None

    # Geographic
    jurisdiction: str
    province: str | None = None
    country: str

    # Provenance links
    source_ids: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    claim_ids: list[str] = Field(default_factory=list)

    # Quality indicators
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_label: str  # e.g., "high", "medium", "low"
    review_status: str
    publish_status: str

    # Classification
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"from_attributes": True}


# Event types
EVENT_TYPES = [
    "court_event",
    "judge_event",
    "crime_event",
    "police_release",
    "news_event",
    "legislation_event",
    "statistical_event",
    "correction_event",
    "contradiction_event",
]

# Review statuses
REVIEW_STATUSES = [
    "raw",
    "parsed",
    "needs_review",
    "approved",
    "rejected",
    "superseded",
]

# Publish statuses
PUBLISH_STATUSES = [
    "private",
    "admin_only",
    "public_safe",
    "public_redacted",
    "blocked",
]

# Confidence labels
CONFIDENCE_LABELS = {
    (0.9, 1.0): "very_high",
    (0.7, 0.9): "high",
    (0.5, 0.7): "medium",
    (0.3, 0.5): "low",
    (0.0, 0.3): "very_low",
}


def get_confidence_label(confidence: float) -> str:
    """Get the confidence label for a given confidence score."""
    for (min_conf, max_conf), label in CONFIDENCE_LABELS.items():
        if min_conf <= confidence <= max_conf:
            return label
    return "very_low"
