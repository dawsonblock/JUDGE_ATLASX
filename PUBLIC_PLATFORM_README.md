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

## Next Steps: Saskatchewan Deployment

### Phase 1: Database & Data Ingestion (Weeks 1-2)

**Step 1.1: Apply Migration**
```bash
cd /vercel/share/v0-project/backend
alembic upgrade head
```

**Step 1.2: Load Saskatchewan Law Data**
The Saskatchewan provincial statutes are already configured in the system. Verify they're loaded:
```bash
# From backend directory
python -m app.ingestion.laws.canada_saskatchewan
```

Key Saskatchewan statutes loaded:
- Saskatchewan Police Act (S.S. 2018, c. P-15.2)
- Saskatchewan Correctional Services Act (S.S. 2012, c. C-37.1)
- Saskatchewan Victims of Crime Act (S.S. 1995, c. V-6)
- Plus criminal code provisions (federal)

**Step 1.3: Ingest Saskatoon Police Crime Data**
Saskatoon Police Service publishes crime map data via CSV export:
```bash
# Load the sample fixture to verify pipeline
python -c "
from app.ingestion.crime_sources.saskatoon import import_saskatoon_csv
from app.db.session import get_async_session
import io

# Test with sample CSV
with open('app/ingestion/crime_sources/fixtures/saskatoon_sample.csv', 'r') as f:
    import_saskatoon_csv(db_session, f)
"
```

Expected data in Saskatoon sample:
- Break and Enter
- Assault
- Theft from Vehicle
- Robbery
- Mischief
- Fraud
- Vehicle Theft
- Theft Over \$5000

**Coordinates**: All Saskatoon crimes snap to city centroid (52.1332, -106.6700) for privacy.

### Phase 2: AI Processing Pipeline (Weeks 2-3)

**Step 2.1: Generate Statute Links for Saskatoon Crimes**
```python
# scripts/populate_saskatchewan_statute_links.py
import asyncio
from sqlalchemy import select
from app.db.session import get_async_session
from app.models.entities import GeoLegalEvent, StatuteIncidentLink
from app.services.public_crime_statute_linker import CrimeStatuteLinker

async def populate_saskatchewan_links():
    linker = CrimeStatuteLinker()
    
    async with get_async_session() as session:
        # Find all Saskatoon incidents without statute links
        stmt = select(GeoLegalEvent).where(
            GeoLegalEvent.jurisdiction == "Saskatchewan",
            ~GeoLegalEvent.statute_links.any()
        )
        results = await session.execute(stmt)
        incidents = results.scalars().all()
        
        print(f"Processing {len(incidents)} Saskatoon incidents...")
        
        for incident in incidents:
            try:
                links = await linker.link_incident_to_statutes(
                    session=session,
                    incident_id=incident.id,
                    crime_type=incident.crime_type or "unknown",
                    description=incident.description or "",
                    location=incident.location_name or "Saskatoon, SK"
                )
                print(f"✓ {incident.title}: {len(links)} statute links")
            except Exception as e:
                print(f"✗ {incident.title}: {str(e)}")
        
        await session.commit()
        print("Statute linking complete!")

if __name__ == "__main__":
    asyncio.run(populate_saskatchewan_links())
```

Run it:
```bash
cd /vercel/share/v0-project/backend
python scripts/populate_saskatchewan_statute_links.py
```

**Step 2.2: Generate Public Summaries**
```python
# scripts/populate_saskatchewan_summaries.py
import asyncio
from sqlalchemy import select
from app.db.session import get_async_session
from app.models.entities import GeoLegalEvent
from app.services.public_incident_explainer import IncidentExplainer

async def populate_summaries():
    explainer = IncidentExplainer()
    
    async with get_async_session() as session:
        # Find all Saskatoon incidents without public summaries
        stmt = select(GeoLegalEvent).where(
            GeoLegalEvent.jurisdiction == "Saskatchewan",
            GeoLegalEvent.public_summary == None
        )
        results = await session.execute(stmt)
        incidents = results.scalars().all()
        
        print(f"Generating summaries for {len(incidents)} incidents...")
        
        for incident in incidents:
            try:
                summary = await explainer.generate_public_summary(
                    session=session,
                    incident_id=incident.id,
                    incident_title=incident.title,
                    crime_type=incident.crime_type or "crime",
                    description=incident.description or "",
                    location=incident.location_name or "Saskatoon, SK"
                )
                incident.public_summary = summary
                print(f"✓ {incident.title}")
            except Exception as e:
                print(f"✗ {incident.title}: {str(e)}")
        
        await session.commit()
        print("Summary generation complete!")

if __name__ == "__main__":
    asyncio.run(populate_summaries())
```

Run it:
```bash
cd /vercel/share/v0-project/backend
python scripts/populate_saskatchewan_summaries.py
```

**Step 2.3: Link News Articles (Manual)**
Populate Saskatchewan news sources for verification:
```python
# scripts/add_saskatchewan_news_links.py
import asyncio
from datetime import datetime
from app.db.session import get_async_session
from app.models.entities import IncidentNewsLink

# Sample Saskatchewan news sources
SASKATOON_NEWS_SOURCES = [
    ("StarPhoenix", "https://thestarphoenix.com"),
    ("Saskatoon News Now", "https://www.saskatoonnewsnow.com"),
    ("CBC Saskatchewan", "https://www.cbc.ca/news/canada/saskatchewan"),
    ("Global News Saskatoon", "https://globalnews.ca/news/saskatoon"),
]

async def add_sample_news_links():
    async with get_async_session() as session:
        # This is a placeholder - you'll manually add news articles
        # For each significant Saskatoon crime, search for news coverage
        
        print("To manually add news links:")
        print("1. Search Saskatchewan news for recent crime coverage")
        print("2. Match incident IDs to articles")
        print("3. Use the API endpoint or admin dashboard to link them")
        print("\nExample:")
        print("POST /api/admin/incident-news-link")
        print("{")
        print('  "incident_id": "sask-crime-001",')
        print('  "article_title": "Police Investigate Assault in Downtown Saskatoon",')
        print('  "article_url": "https://thestarphoenix.com/...",')
        print('  "publication_name": "StarPhoenix",')
        print('  "published_date": "2026-05-27",')
        print('  "excerpt": "Saskatoon police responded to..."')
        print("}")

if __name__ == "__main__":
    asyncio.run(add_sample_news_links())
```

### Phase 3: Frontend Testing (Week 3)

**Step 3.1: Start Development Servers**
```bash
# Terminal 1: Backend
cd /vercel/share/v0-project/backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd /vercel/share/v0-project/frontend
npm run dev
```

**Step 3.2: Test Public Map**
1. Navigate to `http://localhost:3000/`
2. Click "Explore Crime Map" or go to `/public/map`
3. Verify Saskatoon incidents appear on map
4. Test filters:
   - Date range: Last 90 days
   - Crime types: Assault, Theft, etc.
   - Jurisdiction: Saskatchewan

**Step 3.3: Test Incident Detail**
1. Click on a marker on the map
2. Verify detail page shows:
   - Crime type, date, location
   - Public summary (AI-generated explanation)
   - Related statutes with explanations
   - News articles (if available)

**Step 3.4: Test Statutes Browser**
1. Navigate to `/public/statutes`
2. Search for "Saskatchewan Police Act"
3. Verify results show related incidents
4. Test sorting: by frequency, title, amendment date

### Phase 4: Production Deployment (Week 4)

**Step 4.1: Configure Production Database**
```bash
# Set up PostgreSQL with PostGIS extension in production
# Migration automatically creates all necessary tables and indexes
DATABASE_URL=postgresql://user:pass@prod-db:5432/judge_atlas_public
alembic upgrade head
```

**Step 4.2: Deploy Backend**
```bash
# Build Docker image
docker build -t judge-atlas-backend:v1 backend/
docker push your-registry/judge-atlas-backend:v1

# Deploy with environment variables
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgresql://...
ENVIRONMENT=production
```

**Step 4.3: Deploy Frontend**
```bash
cd frontend
npm run build
vercel deploy --prod
```

**Step 4.4: Enable Monitoring**
- Track API response times for `/api/public/*` endpoints
- Monitor AI API costs (Claude statute linking)
- Set up alerts for failed incidents (missing statute links)

### Phase 5: Ongoing Maintenance (Ongoing)

**Daily**:
- Monitor for new Saskatoon Police crime data
- Run ingestion pipeline automatically
- Process new incidents through AI services

**Weekly**:
- Review flagged statute links from users
- Update news article links
- Check data quality metrics

**Monthly**:
- Analyze user engagement (map views, clicks, etc.)
- Gather feedback on explanations
- Fine-tune AI prompts based on patterns

**Quarterly**:
- Expand to other Saskatchewan cities (Regina, etc.)
- Add more provincial law sources
- Consider adding civil legislation alongside criminal

## Saskatchewan-Specific Considerations

### Data Privacy
- Crime coordinates snap to city centroid (not precise location)
- No victim/accused names included
- No sensitive personal information
- Complies with Saskatchewan's public records policies

### Legal Accuracy
- All statute citations verified against official Saskatchewan King's Printer versions
- AI explanations reviewed by legal staff before publication
- Clear disclaimers: "Educational only, not legal advice"
- Links to official statute text for verification

### Community Engagement
- Partner with Saskatchewan Law Foundation
- Solicit feedback from civil rights organizations
- Work with Saskatoon Police Service on accuracy
- Consider educational partnerships with universities

## Advanced: Real-Time Ingestion

For future phases, set up real-time crime feeds:

```python
# Monitor Saskatoon Police API for new incidents
# Each new incident automatically:
# 1. Gets statute links (via AI service)
# 2. Gets public summary
# 3. Appears on public map within 5 minutes

# Requires:
# - Saskatoon Police data feed webhook
# - Job queue (Celery/RQ)
# - Real-time WebSocket updates to frontend
```

## Troubleshooting

**No incidents showing on map?**
1. Verify ingestion: Check `geo_legal_events` table has Saskatoon records
2. Check filters: Verify date range and jurisdictions match
3. Check API: Test `/api/public/map/incidents?bbox=...`

**Statute links showing 0 confidence?**
1. AI service may have failed - check logs
2. Run: `python scripts/populate_saskatchewan_statute_links.py` again
3. Review AI prompts in `public_crime_statute_linker.py`

**Performance issues?**
1. Add database indexes: Already included in migration
2. Enable caching in API: Add `Cache-Control` headers
3. Reduce map clustering threshold at high zoom levels

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
