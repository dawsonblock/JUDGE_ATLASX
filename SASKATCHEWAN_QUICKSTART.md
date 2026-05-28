# Saskatchewan Public Platform - Quick Start Guide

## 60-Second Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ with PostGIS
- Anthropic API key (for Claude AI linking)

### Step 1: Database (1 min)
```bash
cd backend
alembic upgrade head
```

### Step 2: Data & AI Processing (5 min)
```bash
# Run all deployment steps
python scripts/deploy_saskatchewan.py --all
```

This automatically:
- ✓ Verifies database
- ✓ Loads Saskatchewan laws
- ✓ Ingests sample Saskatoon crime data
- ✓ Generates statute links (AI)
- ✓ Creates public summaries (AI)

### Step 3: Start Servers (immediately)
```bash
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Step 4: Open Browser
Navigate to: **http://localhost:3000**

You'll see:
- **Landing page** with features and CTA
- **Crime map** showing Saskatoon incidents
- **Incident details** with statute links and explanations
- **Statutes browser** for searching laws

---

## What Gets Created

### Database Tables
- `statute_incident_links` - Links crimes to relevant Saskatchewan laws
- `incident_news_links` - Links crimes to news coverage
- Plus indices and constraints for performance

### Sample Data
- 8 Saskatoon crime incidents (from fixture)
- 3+ Saskatchewan statutes (Police Act, Correctional Services Act, etc.)
- AI-generated statute links (90%+ confidence)
- Plain-language explanations for public audiences

### Frontend Pages
| Page | URL | Purpose |
|------|-----|---------|
| Landing | `/` | Introduction & CTA |
| Map | `/public/map` | Interactive crime map |
| Incident Detail | `/public/incident/{id}` | Full incident + laws + news |
| Statutes | `/public/statutes` | Searchable statute browser |
| About | `/public/about` | Transparency & methodology |

---

## Troubleshooting

### "No incidents showing on map?"
1. Check: `python scripts/deploy_saskatchewan.py --step 3`
2. Verify: `SELECT COUNT(*) FROM geo_legal_events WHERE jurisdiction='Saskatchewan';`
3. If 0: Rerun ingestion step

### "AI links say 0 confidence?"
Set `ANTHROPIC_API_KEY`:
```bash
export ANTHROPIC_API_KEY=sk-...
python scripts/deploy_saskatchewan.py --step 4
```

### "Database connection refused?"
Check PostgreSQL:
```bash
psql -U postgres -d judge_atlas
\dt statute_incident_links
```

---

## Next: Expand the Platform

### Add More Saskatchewan Cities
1. Get crime data CSV from Regina/Winnipeg police
2. Create adapter in `backend/app/ingestion/crime_sources/`
3. Rerun `deploy_saskatchewan.py --step 3`

### Add News Articles
Manually link recent news:
```bash
# Use admin dashboard or API:
POST /api/admin/incident-news-link
```

### Enable Real-Time Updates
Set up daily ingestion cron:
```bash
# backend/scripts/ingest_saskatoon_daily.py
# Runs every morning to check for new crimes
```

### Collect User Feedback
- Analytics on which incidents users click
- Feedback form on explanations ("Was this helpful?")
- Track which statutes users search for

---

## Important: Legal & Privacy

- **Educational Only**: Not legal advice
- **No Tracking**: No cookies, no analytics
- **Privacy Protected**: Crime locations snap to city centroid
- **Transparent**: All data from official public sources
- **Disclaimers**: Clearly marked on every page

---

## Architecture

```
Backend (Python/FastAPI)
├── Database (PostgreSQL + PostGIS)
├── AI Services (Claude for linking & summarizing)
├── Public API (/api/public/*)
└── Admin Routes (/api/admin/*)

Frontend (Next.js)
├── Public Pages (/public/*)
├── Components (Map, Incident Detail, etc.)
└── API Client (Fetch from /api/public/*)
```

---

## Performance Tips

For large deployments:
1. **Cache API responses** - Add 1-hour cache to `/api/public/map/incidents`
2. **CDN for assets** - Use Vercel/Cloudflare for JS/CSS
3. **Batch AI processing** - Link statutes during off-hours
4. **Database indices** - Already included in migration

---

## Support

For issues:
1. Check logs: `tail -f backend/logs/app.log`
2. Test API: `curl http://localhost:8000/api/public/map/incidents`
3. Review docs: See `PUBLIC_PLATFORM_README.md` for full details
