# Public Crime Understanding Platform

## Overview

This is a separate public-facing platform built on top of JUDGE_ATLASX that helps Canadian citizens understand crime and law through an interactive, educational experience.

**Vision**: Citizens should be able to explore where crimes occur, understand which laws apply, and learn why specific crimes matter in the context of Canadian law.

## What Was Built

### Phase 1: Database Schema ✓
- **New Tables**:
  - `statute_incident_links` - Links crimes to relevant Canadian federal statutes
  - `incident_news_links` - Links crimes to news coverage
- **Extended Tables**:
  - Added `public_summary` field to `geo_legal_events` for AI-generated explanations
- **Migration**: `20260527_0003_public_platform_schema.py`

### Phase 2: AI Services ✓
Three Python services for automated intelligence:

1. **CrimeStatuteLinker** (`public_crime_statute_linker.py`)
   - Uses Claude AI to identify relevant Canadian statutes for each crime
   - Assigns confidence scores (0-1)
   - Generates explanations of why each statute is relevant
   - Handles batch processing and database persistence

2. **IncidentExplainer** (`public_incident_explainer.py`)
   - Generates 2-3 paragraph plain-language explanations for public audiences
   - Connects incidents to relevant laws and explains implications
   - Caches summaries in database to avoid repeated API calls
   - Supports batch generation for multiple incidents

3. **NewsIncidentLinker** (`public_news_linker.py`)
   - Links crimes to news articles for context and verification
   - Supports manual linking (for admin use)
   - Provides retrieval endpoints for incident news

### Phase 3: Public API Endpoints ✓
All endpoints are **unauthenticated** and optimized for public access:

**Map Data**:
- `GET /api/public/map/incidents` - Get incidents in bounding box with clustering
  - Filters: `date_from`, `date_to`, `crime_types[]`, `jurisdictions[]`
  - Returns GeoJSON-like format for map visualization

**Incident Details**:
- `GET /api/public/incident/{id}` - Full incident with statutes, news, and summary

**Statutes**:
- `GET /api/public/statutes` - Search/list Canadian statutes
  - Sort by: `frequency` (most incidents), `title` (A-Z), `recent` (amended date)
  - Supports full-text search
- `GET /api/public/statute/{id}` - Statute details with linked incidents

### Phase 4: Public Frontend ✓
Separate Next.js app in `frontend/app/(public)/`:

**Pages**:
1. **Landing Page** (`/`) - Hero, features, CTA
2. **Crime Map** (`/public/map`) - Interactive MapLibre map with filtering
   - Left sidebar with filters (date range, crime type, province/territory)
   - Incident clustering at different zoom levels
   - Click to view incident detail
3. **Incident Detail** (`/public/incident/[id]`) - 3-column layout:
   - Left: Basic facts (type, location, date, confidence)
   - Middle: Public summary + statute links with explanations
   - Right: News coverage
4. **Statutes Browser** (`/public/statutes`) - Searchable statute listing
   - Full-text search across statute titles/citations
   - Sort options: frequency, alphabetical, recently amended
   - Pagination
5. **About/Transparency** (`/public/about`) - Educational information
   - Mission statement
   - Data sources
   - How it works
   - Limitations and privacy policy

**Components**:
- `PublicCrimeMap.tsx` - MapLibre-based map with real-time incident loading
- Navigation and layout components

## Architecture

```
Backend (Python/FastAPI):
├── Models
│   ├── StatuteIncidentLink (statute_incident_links table)
│   └── IncidentNewsLink (incident_news_links table)
├── Services
│   ├── public_crime_statute_linker.py
│   ├── public_incident_explainer.py
│   └── public_news_linker.py
└── API Routes
    └── public_platform.py (/api/public/*)

Frontend (Next.js):
└── app/(public)/
    ├── page.tsx (Landing)
    ├── map/page.tsx (Map + Map component)
    ├── incident/[id]/page.tsx (Detail)
    ├── statutes/page.tsx (Browser)
    ├── about/page.tsx (About)
    └── components/public/PublicCrimeMap.tsx
```

## How to Use

### 1. Apply Database Migration
```bash
cd backend
alembic upgrade head
```

This creates the `statute_incident_links` and `incident_news_links` tables, and adds the `public_summary` field to `geo_legal_events`.

### 2. Run AI Linking Services

Link crimes to statutes (one-time or scheduled):
```python
from app.services.public_crime_statute_linker import CrimeStatuteLinker
from app.db.session import get_async_session

linker = CrimeStatuteLinker()
async with get_async_session() as session:
    links = await linker.link_incident_to_statutes(
        session=session,
        incident_id="crime-12345",
        crime_type="assault",
        description="Physical altercation in downtown",
        location="Toronto, ON"
    )
```

Generate public summaries:
```python
from app.services.public_incident_explainer import IncidentExplainer

explainer = IncidentExplainer()
async with get_async_session() as session:
    summary = await explainer.generate_public_summary(
        session=session,
        incident_id="crime-12345",
        incident_title="Assault in Downtown Toronto",
        crime_type="assault",
        description="...",
        location="Toronto, ON"
    )
```

Link news articles:
```python
from app.services.public_news_linker import NewsIncidentLinker

linker = NewsIncidentLinker()
async with get_async_session() as session:
    link = await linker.add_manual_news_link(
        session=session,
        incident_id="crime-12345",
        article_title="Police Respond to Assault in Downtown Core",
        article_url="https://...",
        publication_name="Toronto News",
        published_date=datetime.now()
    )
```

### 3. Access Public Platform

Frontend automatically connects to API at `/api/public/*`:
- Landing: `http://localhost:3000/`
- Map: `http://localhost:3000/public/map`
- Detail: `http://localhost:3000/public/incident/{id}`
- Statutes: `http://localhost:3000/public/statutes`
- About: `http://localhost:3000/public/about`

## Key Design Decisions

### 1. Separate Public UI from Admin Dashboard
- **Admin**: Procedural workflow (review, approve, reject)
- **Public**: Educational experience (explanation, context, learning)
- Different data visibility and UX patterns

### 2. AI-Powered Linking
- Automatically links all incidents to relevant statutes at scale
- Confidence scores let users judge reliability
- Starts with high-confidence links, improves over time
- Human review can flag problematic links

### 3. Plain Language + Statute Context
- Don't overwhelm public with dense legal text
- Show AI explanation of *why* statute matters *for this crime*
- Include news to validate relevance

### 4. No Authentication Required
- Anyone can explore the map and learn
- Democratizes access to legal understanding
- No tracking or data collection
- Public good, not monetized

## API Response Examples

### GET /api/public/map/incidents
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "id": "crime-12345",
      "title": "Assault in Downtown Toronto",
      "type": "assault",
      "lat": 43.6629,
      "lng": -79.3957,
      "location": "Downtown Toronto",
      "date": "2026-05-27T10:30:00",
      "jurisdiction": "Ontario"
    }
  ],
  "count": 1
}
```

### GET /api/public/incident/{id}
```json
{
  "id": "crime-12345",
  "title": "Assault in Downtown Toronto",
  "type": "assault",
  "public_summary": "This incident involves...",
  "statutes": [
    {
      "citation": "Criminal Code s. 267",
      "section_label": "267",
      "marginal_note": "Assault",
      "relevance": "This statute defines assault...",
      "confidence": 0.95
    }
  ],
  "news": [
    {
      "title": "Police Respond to Assault Downtown",
      "url": "https://...",
      "publication": "Toronto News"
    }
  ]
}
```

## Next Steps for Production

1. **Populate Data**:
   - Run AI services on existing incidents to generate links
   - Add news articles for context
   - Generate public summaries for all major incidents

2. **Enhance AI**:
   - Fine-tune Claude prompts based on user feedback
   - Add more sources (law enforcement, court data)
   - Implement real-time incident feeds

3. **Scale**:
   - Cache API responses for performance
   - Add CDN for static assets
   - Monitor AI API costs

4. **Community**:
   - Gather user feedback on explanations
   - Iterate on UI based on testing
   - Partner with legal education organizations

5. **Expand Jurisdictions**:
   - Currently built for Canadian federal law
   - Can expand to provincial/territorial law
   - Adapt for other countries

## Important Notes

- **Educational Only**: This is not legal advice
- **AI Explanations**: Generated by AI, may contain errors
- **Evidence-Based**: All data from official sources
- **Privacy**: No tracking, no accounts required
- **Public Good**: Free, accessible civic education tool

## Files Created

**Backend**:
- `/backend/app/models/entities.py` (StatuteIncidentLink, IncidentNewsLink)
- `/backend/app/models/geo_legal_event.py` (public_summary field)
- `/backend/app/services/public_crime_statute_linker.py`
- `/backend/app/services/public_incident_explainer.py`
- `/backend/app/services/public_news_linker.py`
- `/backend/app/api/routes/public_platform.py`
- `/backend/alembic/versions/20260527_0003_public_platform_schema.py`
- `/backend/app/api/routes/__init__.py` (updated)

**Frontend**:
- `/frontend/app/(public)/page.tsx`
- `/frontend/app/(public)/layout.tsx`
- `/frontend/app/(public)/map/page.tsx`
- `/frontend/app/(public)/incident/[id]/page.tsx`
- `/frontend/app/(public)/statutes/page.tsx`
- `/frontend/app/(public)/about/page.tsx`
- `/frontend/components/public/PublicCrimeMap.tsx`
