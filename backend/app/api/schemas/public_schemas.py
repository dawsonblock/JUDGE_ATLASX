"""
Public API Response Schemas

These schemas enforce strict allowlisting of fields for public endpoints.
Never return raw ORM objects; always use these schemas for serialization.

This prevents accidental exposure of private fields, raw payloads, internal
review notes, unreviewed AI outputs, or other sensitive data.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PublicIncidentMapItem(BaseModel):
    """Incident as it appears on the interactive map."""

    id: str = Field(..., description="Incident ID")
    title: str = Field(..., description="Incident title")
    event_type: Optional[str] = Field(None, description="Type of event")
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    location_name: Optional[str] = Field(None, description="Human-readable location")
    occurred_at: Optional[datetime] = Field(None, description="When the incident occurred")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction (e.g., 'Saskatchewan')")
    confidence: float = Field(..., description="Confidence score (0-1)")
    evidence_count: int = Field(
        default=0, description="Number of linked evidence items"
    )


class PublicIncidentDetail(BaseModel):
    """Full incident detail with statute and news links."""

    id: str
    title: str
    event_type: Optional[str]
    description: Optional[str]
    public_summary: Optional[str] = Field(
        None,
        description="AI-generated summary (derivative, not authoritative)",
    )
    lat: float
    lng: float
    location_name: Optional[str]
    occurred_at: Optional[datetime]
    jurisdiction: Optional[str]
    province: Optional[str]
    country: str
    confidence: float
    confidence_label: str


class PublicStatuteLink(BaseModel):
    """Link between an incident and a statute."""

    statute_id: int = Field(..., description="Legal section ID")
    statute_title: str = Field(..., description="Statute title")
    statute_citation: Optional[str] = Field(None, description="Citation (e.g., 'S.S. 2018, c. P-15.2')")
    section_label: Optional[str] = Field(None, description="Section number")
    link_reason: str = Field(..., description="Why this statute is relevant")
    confidence_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score (0-1)",
    )
    ai_model_version: str = Field(..., description="AI model that generated this link")


class PublicNewsLink(BaseModel):
    """Link between an incident and a news article."""

    article_title: str
    article_url: str
    publication_name: Optional[str]
    published_date: Optional[datetime]
    excerpt: Optional[str]
    relevance_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Relevance score (0-1)",
    )


class PublicIncidentWithLinks(PublicIncidentDetail):
    """Incident detail with statute and news links."""

    statute_links: list[PublicStatuteLink] = Field(
        default=[], description="Related statutes"
    )
    news_links: list[PublicNewsLink] = Field(
        default=[], description="Related news articles"
    )


class PublicStatuteItem(BaseModel):
    """Statute as it appears in statute browser."""

    id: int
    title: str
    citation: Optional[str]
    jurisdiction: str
    short_description: Optional[str]
    incident_count: int = Field(
        default=0, description="Number of linked incidents"
    )


class PublicStatuteDetail(BaseModel):
    """Full statute detail with sections and linked incidents."""

    id: int
    title: str
    citation: Optional[str]
    jurisdiction: str
    full_text: Optional[str]
    sections: list[dict] = Field(
        default=[], description="Statute sections"
    )


class PublicMapIncidentsResponse(BaseModel):
    """Response for /api/public/map/incidents endpoint."""

    incidents: list[PublicIncidentMapItem]
    bbox_min_lat: float
    bbox_min_lng: float
    bbox_max_lat: float
    bbox_max_lng: float
    total_count: int
    returned_count: int


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    detail: Optional[str] = None
    status_code: int
