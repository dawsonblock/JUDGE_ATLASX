"""
Public Platform API Routes

Public-facing API endpoints for the crime understanding platform.
These endpoints are unauthenticated and optimized for public access:

- GET /api/public/map/incidents - Get incidents for map visualization
- GET /api/public/incident/{id} - Get full incident details
- GET /api/public/statutes - Search and list statutes
- GET /api/public/statute/{id} - Get statute with linked incidents
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.geo_legal_event import GeoLegalEvent
from app.models.entities import (
    StatuteIncidentLink,
    IncidentNewsLink,
    LegalInstrument,
    LegalSection,
)
from app.services.public_release_policy import PublicReleasePolicy
from app.api.schemas.public_schemas import (
    PublicIncidentMapItem,
    PublicMapIncidentsResponse,
    PublicStatuteLink,
    PublicNewsLink,
    PublicIncidentWithLinks,
    PublicStatuteItem,
    ErrorResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/public", tags=["public"])


# ============================================================================
# Map Incidents Endpoint
# ============================================================================


@router.get("/map/incidents")
def get_map_incidents(
    bbox_min_lat: float = Query(-90, description="Bounding box min latitude"),
    bbox_min_lng: float = Query(-180, description="Bounding box min longitude"),
    bbox_max_lat: float = Query(90, description="Bounding box max latitude"),
    bbox_max_lng: float = Query(180, description="Bounding box max longitude"),
    date_from: str | None = Query(None, description="ISO date start (YYYY-MM-DD)"),
    date_to: str | None = Query(None, description="ISO date end (YYYY-MM-DD)"),
    crime_types: list[str] | None = Query(None, description="Filter by crime types"),
    jurisdictions: list[str] | None = Query(
        None, description="Filter by jurisdictions"
    ),
    limit: int = Query(500, ge=1, le=1000, description="Max results"),
    session: Session = Depends(get_db),
) -> dict:
    """
    Get crime incidents for map visualization.

    Returns incidents within a bounding box, with optional filtering by date,
    crime type, and jurisdiction. Optimized for map clustering.

    Query params:
    - bbox_min_lat, bbox_min_lng, bbox_max_lat, bbox_max_lng: Bounding box
    - date_from, date_to: Optional date range
    - crime_types: Filter by crime type (e.g., "assault", "theft")
    - jurisdictions: Filter by jurisdiction (e.g., "Ontario", "BC")
    - limit: Maximum incidents to return (default 500, max 1000)
    """
    logger.info(
        f"[v0] Map incidents request: bbox=({bbox_min_lat},{bbox_min_lng},"
        f"{bbox_max_lat},{bbox_max_lng})"
    )

    # Validate bounding box
    if bbox_min_lat > bbox_max_lat or bbox_min_lng > bbox_max_lng:
        raise HTTPException(status_code=400, detail="Invalid bounding box: min must be <= max")

    try:
        # Validate date formats early
        date_from_dt = None
        if date_from:
            try:
                date_from_dt = datetime.fromisoformat(date_from)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date_from format (use YYYY-MM-DD)")

        date_to_dt = None
        if date_to:
            try:
                date_to_dt = datetime.fromisoformat(date_to)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date_to format (use YYYY-MM-DD)")

        # Build query
        query = select(GeoLegalEvent).filter(
            and_(
                GeoLegalEvent.lat >= bbox_min_lat,
                GeoLegalEvent.lat <= bbox_max_lat,
                GeoLegalEvent.lng >= bbox_min_lng,
                GeoLegalEvent.lng <= bbox_max_lng,
                GeoLegalEvent.publish_status == "published",
            )
        )

        # Apply date filter
        if date_from_dt:
            query = query.filter(GeoLegalEvent.occurred_at >= date_from_dt)

        if date_to_dt:
            query = query.filter(GeoLegalEvent.occurred_at <= date_to_dt)

        # Apply crime type filter
        if crime_types:
            query = query.filter(GeoLegalEvent.event_type.in_(crime_types))

        # Apply jurisdiction filter
        if jurisdictions:
            query = query.filter(GeoLegalEvent.jurisdiction.in_(jurisdictions))

        query = query.limit(limit).order_by(GeoLegalEvent.occurred_at.desc())

        result = session.execute(query)
        incidents = result.scalars().all()

        # Filter to only publicly releasable incidents
        policy = PublicReleasePolicy()
        public_incidents = []
        for incident in incidents:
            if policy.is_incident_publicly_releasable(session, incident):
                public_incidents.append(incident)

        # Transform to response schema
        features = []
        for incident in public_incidents:
            # Count linked resources
            statute_result = session.execute(
                select(func.count(StatuteIncidentLink.id)).where(
                    StatuteIncidentLink.incident_id == incident.id,
                    StatuteIncidentLink.review_status == "approved",
                )
            )
            statute_count = statute_result.scalar() or 0

            news_result = session.execute(
                select(func.count(IncidentNewsLink.id)).where(
                    IncidentNewsLink.incident_id == incident.id
                )
            )
            news_count = news_result.scalar() or 0

            item = PublicIncidentMapItem(
                id=incident.id,
                title=incident.title,
                event_type=incident.event_type,
                lat=incident.lat,
                lng=incident.lng,
                location_name=incident.location_name,
                occurred_at=incident.occurred_at,
                jurisdiction=incident.jurisdiction,
                confidence=incident.confidence,
                evidence_count=statute_count + news_count,
            )
            features.append(item)

        logger.info(f"[v0] Returning {len(features)} publicly releasable incidents")
        return PublicMapIncidentsResponse(
            incidents=features,
            bbox_min_lat=bbox_min_lat,
            bbox_min_lng=bbox_min_lng,
            bbox_max_lat=bbox_max_lat,
            bbox_max_lng=bbox_max_lng,
            total_count=len(incidents),
            returned_count=len(features),
        )

    except Exception as e:
        logger.error(f"[v0] Error fetching map incidents: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching incidents")


# ============================================================================
# Incident Detail Endpoint
# ============================================================================


@router.get("/incident/{incident_id}")
def get_incident_detail(
    incident_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Get full details for a specific incident.

    Returns:
    - Basic incident information
    - Linked statutes with explanations
    - Related news articles
    - AI-generated public summary
    """
    logger.info(f"[v0] Fetching incident detail: {incident_id}")

    try:
        # Fetch incident
        result = session.execute(
            select(GeoLegalEvent).filter_by(id=incident_id)
        )
        incident = result.scalar()

        if not incident or incident.publish_status != "published":
            raise HTTPException(status_code=404, detail="Incident not found")

        # Fetch linked statutes
        statute_links_result = session.execute(
            select(StatuteIncidentLink)
            .filter_by(incident_id=incident_id, review_status="approved")
            .order_by(StatuteIncidentLink.confidence_score.desc())
        )
        statute_links = statute_links_result.scalars().all()

        statutes = []
        for link in statute_links:
            section_result = session.execute(
                select(LegalSection).filter_by(id=link.legal_section_id)
            )
            section = section_result.scalar()

            instrument_result = session.execute(
                select(LegalInstrument).filter_by(id=section.legal_instrument_id)
            )
            instrument = instrument_result.scalar()

            if section and instrument:
                statutes.append(
                    {
                        "section_id": section.id,
                        "section_label": section.section_label,
                        "marginal_note": section.marginal_note or "",
                        "text_excerpt": section.text[:300] if section.text else "",
                        "statute_title": instrument.title or instrument.short_title,
                        "citation": instrument.citation or "",
                        "relevance": link.link_reason,
                        "confidence": link.confidence_score,
                    }
                )

        # Fetch linked news
        news_result = session.execute(
            select(IncidentNewsLink)
            .filter_by(incident_id=incident_id)
            .order_by(IncidentNewsLink.published_date.desc())
            .limit(10)
        )
        news_links = news_result.scalars().all()

        news = [
            {
                "id": link.id,
                "title": link.news_article_title,
                "url": link.news_article_url,
                "publication": link.publication_name or "Unknown",
                "date": link.published_date.isoformat()
                if link.published_date
                else None,
                "excerpt": link.excerpt,
            }
            for link in news_links
        ]

        return {
            "id": incident_id,
            "title": incident.title,
            "type": incident.event_type,
            "description": incident.description,
            "public_summary": incident.public_summary,
            "location": incident.location_name,
            "lat": incident.lat,
            "lng": incident.lng,
            "jurisdiction": incident.jurisdiction,
            "occurred_at": incident.occurred_at.isoformat()
            if incident.occurred_at
            else None,
            "published_at": incident.published_at.isoformat()
            if incident.published_at
            else None,
            "statutes": statutes,
            "news": news,
            "confidence": incident.confidence,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[v0] Error fetching incident {incident_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching incident")


# ============================================================================
# Statutes Endpoint
# ============================================================================


@router.get("/statutes")
def search_statutes(
    search: str | None = Query(None, description="Search term"),
    sort_by: str = Query(
        "frequency", description="Sort: frequency, title, or recent"
    ),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Search and list Canadian statutes.

    Returns statutes with count of linked incidents.

    Query params:
    - search: Search in statute titles/citations
    - sort_by: frequency (most incidents), title (A-Z), or recent
    - limit: Results per page (default 50, max 200)
    - offset: For pagination
    """
    logger.info(f"[v0] Searching statutes: search={search}, sort_by={sort_by}")

    try:
        # Base query for Canadian federal statutes
        query = select(LegalInstrument).filter(
            and_(
                LegalInstrument.jurisdiction == "CA",
                LegalInstrument.public_visibility == "public",
            )
        )

        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (LegalInstrument.title.ilike(search_term))
                | (LegalInstrument.citation.ilike(search_term))
                | (LegalInstrument.short_title.ilike(search_term))
            )

        # Apply sorting
        if sort_by == "title":
            query = query.order_by(LegalInstrument.title)
        elif sort_by == "recent":
            query = query.order_by(LegalInstrument.last_amended_date.desc())
        else:  # frequency (default)
            # Join with statute_incident_links and count
            query = (
                query.outerjoin(StatuteIncidentLink)
                .group_by(LegalInstrument.id)
                .order_by(
                    func.count(StatuteIncidentLink.id).desc()
                )
            )

        # Paginate
        total_query = query.statement.with_only_columns(func.count())
        total = (session.execute(total_query)).scalar() or 0

        query = query.offset(offset).limit(limit)
        result = session.execute(query)
        statutes = result.scalars().unique().all()

        items = [
            {
                "id": statute.id,
                "title": statute.title or statute.short_title or "Unknown",
                "citation": statute.citation or "",
                "short_title": statute.short_title,
                "type": statute.instrument_type,
                "last_amended": statute.last_amended_date.isoformat()
                if statute.last_amended_date
                else None,
            }
            for statute in statutes
        ]

        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    except Exception as e:
        logger.error(f"[v0] Error searching statutes: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching statutes")


# ============================================================================
# Statute Detail Endpoint
# ============================================================================


@router.get("/statute/{statute_id}")
def get_statute_detail(
    statute_id: int,
    limit_incidents: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Get full details for a statute, including linked incidents.

    Returns:
    - Statute metadata (title, citation, text)
    - Sections and subsections
    - All linked incidents (paginated)
    """
    logger.info(f"[v0] Fetching statute detail: {statute_id}")

    try:
        # Fetch statute
        result = session.execute(
            select(LegalInstrument).filter_by(id=statute_id)
        )
        statute = result.scalar()

        if not statute or statute.public_visibility != "public":
            raise HTTPException(status_code=404, detail="Statute not found")

        # Fetch sections
        sections_result = session.execute(
            select(LegalSection).filter_by(legal_instrument_id=statute_id)
        )
        sections = sections_result.scalars().all()

        # Fetch linked incidents
        incidents_result = session.execute(
            select(StatuteIncidentLink)
            .filter_by(review_status="approved")
            .join(LegalSection)
            .filter(
                LegalSection.legal_instrument_id == statute_id
            )
            .order_by(StatuteIncidentLink.confidence_score.desc())
            .limit(limit_incidents)
        )
        incident_links = incidents_result.scalars().all()

        # Fetch incident details
        incidents = []
        for link in incident_links:
            incident_result = session.execute(
                select(GeoLegalEvent).filter_by(id=link.incident_id)
            )
            incident = incident_result.scalar()

            if incident:
                incidents.append(
                    {
                        "id": incident.id,
                        "title": incident.title,
                        "type": incident.event_type,
                        "location": incident.location_name,
                        "date": incident.occurred_at.isoformat()
                        if incident.occurred_at
                        else None,
                        "relevance": link.link_reason,
                    }
                )

        return {
            "id": statute_id,
            "title": statute.title or statute.short_title or "Unknown",
            "citation": statute.citation or "",
            "short_title": statute.short_title,
            "type": statute.instrument_type,
            "last_amended": statute.last_amended_date.isoformat()
            if statute.last_amended_date
            else None,
            "in_force_start": statute.in_force_start_date.isoformat()
            if statute.in_force_start_date
            else None,
            "sections_count": len(sections),
            "linked_incidents_count": len(incidents),
            "incidents": incidents,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[v0] Error fetching statute {statute_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching statute")
