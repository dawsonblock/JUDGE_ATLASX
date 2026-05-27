# Production Deployment: Saskatchewan Public Platform

## Overview

This guide covers deploying the JUDGE ATLAS Saskatchewan public crime understanding platform to production.

**Estimated Time**: 4-6 hours
**Complexity**: Medium
**Cost**: ~$200-500/month (depends on traffic & AI API usage)

---

## Infrastructure Requirements

### Compute
- **Backend**: 2 CPU, 4GB RAM (Cloud Run, ECS, or Kubernetes)
- **Frontend**: Vercel (recommended) or similar CDN + static hosting
- **Database**: Managed PostgreSQL (AWS RDS, Google Cloud SQL, Azure)
  - Minimum: 2 CPU, 4GB RAM, 100GB storage
  - Enable PostGIS extension
  - Daily automated backups

### Network
- CDN for static assets (Vercel, Cloudflare)
- SSL/TLS certificates (auto-renewed)
- Rate limiting on public API
- DDoS protection

### Services
- Anthropic API key (for Claude AI services)
- Email provider (SendGrid, Mailgun) for alerts
- Monitoring/Logging (Sentry, CloudWatch, Stackdriver)

---

## Step 1: Prepare Database

### 1.1 Create Managed Database
Using Google Cloud SQL (recommended):
```bash
# Create instance
gcloud sql instances create judge-atlas-prod \
  --database-version=POSTGRES_14 \
  --tier=db-custom-2-4096 \
  --region=us-central1 \
  --backup-start-time=02:00 \
  --backup-location=us

# Enable PostGIS extension
gcloud sql connect judge-atlas-prod
  > CREATE EXTENSION postgis;
  > CREATE EXTENSION postgis_topology;
```

### 1.2 Create Database & User
```sql
CREATE DATABASE judge_atlas_prod;
CREATE USER app_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE judge_atlas_prod TO app_user;
```

### 1.3 Run Migrations
```bash
export DATABASE_URL="postgresql://app_user:pass@cloud-sql-ip/judge_atlas_prod"
cd backend
alembic upgrade head

# Verify tables
psql $DATABASE_URL -c "\dt"
# Should show: statute_incident_links, incident_news_links, etc.
```

---

## Step 2: Prepare Backend

### 2.1 Build Docker Image
```dockerfile
# Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/app ./app
COPY backend/alembic ./alembic
COPY backend/alembic.ini .

ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build & push:
```bash
docker build -f Dockerfile.backend -t judge-atlas-backend:v1 .
docker tag judge-atlas-backend:v1 gcr.io/PROJECT_ID/judge-atlas-backend:v1
docker push gcr.io/PROJECT_ID/judge-atlas-backend:v1
```

### 2.2 Set Environment Variables
```bash
# Production .env (Cloud Run secrets manager)
DATABASE_URL=postgresql://app_user:pass@cloud-sql-ip/judge_atlas_prod
ANTHROPIC_API_KEY=sk-...
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://judge-atlas-sask.ca,https://www.judge-atlas-sask.ca
API_MAX_REQUESTS=1000
API_WINDOW_SECONDS=60
```

### 2.3 Deploy Backend
Using Google Cloud Run:
```bash
gcloud run deploy judge-atlas-backend \
  --image=gcr.io/PROJECT_ID/judge-atlas-backend:v1 \
  --platform=managed \
  --region=us-central1 \
  --memory=2Gi \
  --cpu=2 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=$DATABASE_URL,ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
```

Verify:
```bash
curl https://judge-atlas-backend-xxx.a.run.app/health
```

---

## Step 3: Prepare Frontend

### 3.1 Build Next.js App
```bash
cd frontend

# Create production environment
cat > .env.production << EOF
NEXT_PUBLIC_API_URL=https://judge-atlas-backend-xxx.a.run.app
NEXT_PUBLIC_SITE_NAME=Judge Atlas Saskatchewan
EOF

npm run build
npm run export  # Static export for CDN
```

### 3.2 Deploy to Vercel (Recommended)
```bash
# Connect repo & deploy
vercel --prod \
  --env NEXT_PUBLIC_API_URL=https://judge-atlas-backend-xxx.a.run.app

# Automatic deployments on git push to main
```

Or deploy to your own CDN:
```bash
# Upload build output to S3/CloudStorage
aws s3 sync ./out s3://judge-atlas-frontend --delete
```

---

## Step 4: Populate Data

### 4.1 Load Saskatchewan Laws
```bash
python backend/scripts/deploy_saskatchewan.py --step 2
```

### 4.2 Ingest Saskatoon Police Data
```bash
python backend/scripts/deploy_saskatchewan.py --step 3
```

### 4.3 Generate Statute Links (Batch Job)
```bash
# Run as Cloud Task (scheduled job)
python backend/scripts/deploy_saskatchewan.py --step 4
```

Expected time: ~2 minutes per 100 incidents with Anthropic API

### 4.4 Generate Public Summaries
```bash
python backend/scripts/deploy_saskatchewan.py --step 5
```

---

## Step 5: Configure DNS & SSL

### 5.1 Register Domain
Register `judge-atlas-sask.ca` (or similar)

### 5.2 Point DNS to Frontend
If using Vercel:
```
CNAME: judge-atlas-sask.ca -> cname.vercel-dns.com
```

If using S3 + CloudFront:
```
CNAME: judge-atlas-sask.ca -> d111111abcdef8.cloudfront.net
```

### 5.3 SSL Certificate
- Vercel: Auto-provisioned
- CloudFront: Use AWS Certificate Manager (free)
- Self-hosted: Let's Encrypt (Certbot)

---

## Step 6: Setup Monitoring & Logging

### 6.1 Backend Logging
Using Google Cloud Logging:
```python
# app/logger.py
import logging
from google.cloud import logging as cloud_logging

logger = cloud_logging.Client().logger("judge-atlas-backend")

# All logs automatically sent to Cloud Logging
```

### 6.2 Error Tracking
Using Sentry:
```python
# app/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="https://xxxx@sentry.io/xxxx",
    environment="production",
)
```

### 6.3 Performance Monitoring
```bash
# Add to Cloud Run
gcloud run deploy judge-atlas-backend \
  --update-env-vars ENABLE_PROFILER=true
```

---

## Step 7: Setup Daily Data Ingestion

### 7.1 Create Scheduled Job
Using Google Cloud Scheduler:
```bash
# Check Saskatoon Police for new crimes daily at 2 AM
gcloud scheduler jobs create pubsub ingest-saskatoon-daily \
  --schedule="0 2 * * *" \
  --time-zone="America/Denver" \
  --topic=ingest-saskatoon \
  --message-body='{"source":"saskatoon_police"}'
```

### 7.2 Create Cloud Function to Process
```python
# functions/ingest_daily.py
def ingest_saskatoon(request):
    """Cloud Function triggered by Pub/Sub."""
    from app.ingestion.crime_sources.saskatoon import import_saskatoon_csv
    from app.services.public_crime_statute_linker import CrimeStatuteLinker
    
    # 1. Download latest CSV from Saskatoon Police
    # 2. Ingest new incidents
    # 3. Run AI linking on new crimes
    # 4. Generate summaries
    
    return {"status": "complete"}
```

---

## Step 8: Setup Backups & Disaster Recovery

### 8.1 Database Backups
```bash
# Google Cloud SQL handles automated backups
# Retention: 7 days (paid), 35 days with backup service

# Manual backup
gcloud sql backups create \
  --instance=judge-atlas-prod \
  --description="Pre-launch backup"
```

### 8.2 Frontend Backup
```bash
# Vercel automatically maintains version history
# Rollback to previous deployment:
vercel rollback
```

### 8.3 Test Recovery
Monthly: Restore backup to staging database and test

---

## Step 9: Performance Optimization

### 9.1 API Caching
```python
# app/api/routes/public_platform.py
@router.get("/api/public/map/incidents")
def get_incidents(
    bbox: str,
    cache_control = Header("Cache-Control: max-age=3600")
):
    """Cache map incidents for 1 hour."""
```

### 9.2 Frontend Caching
```javascript
// next.config.js
module.exports = {
  headers: [
    {
      source: '/api/:path*',
      headers: [
        { key: 'Cache-Control', value: 'max-age=3600' },
      ],
    },
  ],
}
```

### 9.3 Database Query Optimization
All done in migration (indices on: `incident_id`, `confidence_score`, `published_date`)

---

## Step 10: Security Hardening

### 10.1 Environment Variables (Secrets Manager)
```bash
# Never commit API keys
gcloud secrets create ANTHROPIC_API_KEY --data-file=- < key.txt
```

### 10.2 Rate Limiting
```python
# app/middleware.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("100/hour")
@router.get("/api/public/map/incidents")
def get_incidents():
    pass
```

### 10.3 CORS Configuration
```python
# Only allow from production domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://judge-atlas-sask.ca"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

---

## Cost Estimation (Monthly)

| Service | Size | Cost |
|---------|------|------|
| Cloud SQL (PostgreSQL) | 2 CPU, 4GB, 100GB | $150 |
| Cloud Run (Backend) | 2 CPU, 2GB, ~10k req/day | $50-150 |
| Vercel (Frontend) | Static, ~1M/month views | $20-100 |
| Anthropic API (Claude) | ~500k tokens/month | $50 |
| CloudFlare CDN | ~1GB/day | $25 |
| Monitoring (Sentry) | <1M events | $29 |
| **Total** | | **~$320-450** |

---

## Launch Checklist

- [ ] Database migrated and verified
- [ ] Saskatchewan laws loaded
- [ ] Sample Saskatoon data ingested
- [ ] AI services tested and working
- [ ] Backend deployed and healthy
- [ ] Frontend deployed and DNS working
- [ ] SSL certificate valid
- [ ] Monitoring & logging configured
- [ ] Daily ingestion scheduled
- [ ] Backups tested
- [ ] Rate limiting enabled
- [ ] CORS configured
- [ ] Legal disclaimers reviewed
- [ ] Privacy policy published
- [ ] Stakeholders notified

---

## Post-Launch

### Day 1
- Monitor error logs
- Check API response times
- Verify daily ingestion runs
- Gather initial user feedback

### Week 1
- Analyze user engagement (map clicks, searches)
- Check AI link quality
- Monitor costs
- Iterate on explanations

### Month 1
- Expand to Regina/other Saskatchewan cities
- Add more news sources
- Optimize slow queries
- Plan next features

---

## Troubleshooting

### Backend Errors
```bash
gcloud run logs read judge-atlas-backend --limit 50
```

### Database Issues
```bash
gcloud sql connect judge-atlas-prod
\dt  # List tables
SELECT COUNT(*) FROM geo_legal_events;
```

### Frontend Not Updating
```bash
# Check deployment
vercel ls
vercel inspect  # See current build
```

---

## Support & Contact

- **Issues**: Open GitHub issue or Sentry alert
- **Questions**: Contact team
- **Feedback**: User feedback form on about page
