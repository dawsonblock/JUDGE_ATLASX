# REPO_REALITY

## What Is Actually Implemented

### Core Strength Areas

#### Evidence Storage & Retrieval ✓
- Evidence snapshot model with version tracking
- Source registry with 26 registered sources
- Evidence query API (`/api/evidence/*`)
- Source-keyed evidence retrieval
- Evidence integrity checksums
- Audit trail for evidence modifications

#### Legal Document Ingestion ✓
- Backend ingestion pipeline (single active source: `justice_canada_laws_xml`)
- SQLAlchemy ORM models for legal instruments, sections, and relationships
- Alembic migrations for schema evolution
- Legal section versioning via `effective_date` and `repeal_date`
- Amendment tracking
- Repeal status tracking

#### Public API Boundaries ✓
- Anonymous public endpoints (`GET /api/evidence`, `GET /api/claims`)
- Authenticated routes (`POST /api/claims`, `PATCH /api/claims`)
- Admin-only routes (`POST /api/admin/*`)
- JWT-based auth with role enforcement
- RBAC checks on all mutable operations
- Public-safe/public-redacted filtering

#### Review & Publication Workflow ✓
- Claim entity model with status (pending/approved/rejected/disputed)
- Review assignment to admin/reviewer users
- Publish status control (internal/public_redacted/public_safe)
- Evidence requirement validation before approval
- Review notes and comment tracking
- Audit logging of all review actions

#### Testing & Quality Gates ✓
- Backend pytest suite (9 gate suites)
- Frontend typecheck, lint, test, build gates
- Docker runtime validation
- PostGIS integration tests
- Archive validation
- Source registry validation
- Path hygiene checks
- No-generated-files enforcement
- False-claim scanner

#### Proof & Deployment ✓
- Proof artifact generation (`make proof`)
- Release archive builder
- Archive validator
- Docker build pipeline
- postgres-gate integration testing
- Egress proxy proof
- Synthetic demo proof
- Proof freshness verification

---

### Partial/Limited Implementation

#### Memory System 🟡
- **Status**: Working but shallow
- **Implemented**: Claim storage, status tracking, confidence scoring
- **Missing**: 
  - Subject/predicate/object detail preservation
  - Match reason and salience tracking
  - Temporal query operators
  - Full evidence reference recovery
- **Scope**: Observation + status + confidence only
- **Risk**: Memory outputs lose source detail; derivatives only

#### AI/LLM Integration 🟡
- **Status**: Basic chat interface; no production-grade inference
- **Implemented**: 
  - Backend `/api/ai/chat` endpoint
  - Context window management
  - Role-based access control
- **Missing**:
  - Inference caching
  - Confidence calibration
  - Explanation generation
  - Contradiction detection
- **Scope**: Research-grade assistance only
- **Risk**: AI outputs are hypotheses; not authoritative

#### Live Map / Workflow Admin Routes 🟡
- **Status**: Experimental modules exist in tree but are unmounted
- **Implemented**: No mounted `live_map` or `workflow_admin` endpoints
- **Missing**:
  - Any future experimental route must pass auth boundary tests before mount
  - Explicit admin/source_admin enforcement for workflow control endpoints
  - Public filter bypass prevention tests for map-style admin switches
- **Scope**: Absent from active route registration
- **Risk**: Low in current state; rises if reintroduced without boundary tests

#### Event Origin Tracking 🟡
- **Status**: Partially implemented
- **Enum values**: RuntimeLoop, Evaluator, ClaimStore, ToolGate, ProofHarness
- **Missing**: 
  - External integration origins
  - Batch operation tracking
  - Schedule/cron tracking
- **Scope**: Covers internal operations only
- **Risk**: External source integrations not fully tracked

---

### Not Yet Implemented ❌

#### Bi-temporal Modeling
- No `valid_from`, `valid_to`, `tx_from`, `tx_to` fields
- No temporal query helpers
- No as-of queries
- Deferred to Phase 14

#### Advanced Memory Features
- No memory_records table (claim-table-only)
- No answer basis reconstruction
- No contradiction resolution
- No temporal memory queries
- Deferred to Phase 14

#### Multi-Region Deployment
- Single deployment only
- No failover
- No multi-region redundancy

#### Performance Optimization
- No query caching (except Redis session store)
- No pagination optimization
- No index materialization
- No pre-computed result caching

#### Advanced Search
- No full-text search on evidence text
- No semantic search
- No vector embeddings for document similarity
- No evidence inference graph

---

## Repo Reality Assessment

### Accuracy of Current Status Claims

| Claim | Accuracy | Notes |
|-------|----------|-------|
| "Alpha platform" | ✓ Accurate | Ready for research/review, not production deployment |
| "Not suitable for production deployment" | ✓ Accurate | Single deployment, no HA, no temporal support |
| "Evidence authoritative" | ✓ Accurate | Evidence snapshots are versioned and audited |
| "AI outputs derivative" | ✓ Accurate | No inference authority; hypotheses only |
| "Manual review required" | ✓ Accurate | Public publication requires approval |
| "Source coverage incomplete" | ✓ Accurate | 26 registered, 1 active ingestion |
| "Ingestion disabled by default" | ✓ Accurate | Sources must be explicitly enabled |
| "Legal correlations are hypotheses" | ✓ Accurate | No verdict authority; correlations are semantic links only |

### Gaps Between Documentation and Reality

| Gap | Severity | Status |
|-----|----------|--------|
| `REPO_INVENTORY.md` stale proof numbers | LOW | Will regenerate in Phase 11 |
| Memory system docs overstate capabilities | MEDIUM | Phase 14 will formalize temporal model |
| No hardening report (CODEX_MAIN_12) | MEDIUM | Will generate after Phase 13 |
| Live/admin routes not documented as unmounted | LOW | Phase 9 confirms decision |

---

## What Works Well

✓ **Evidence model**: Versioned, audited, queryable  
✓ **Public/private boundaries**: Enforced at API layer  
✓ **Review workflow**: Functional and tracked  
✓ **Proof infrastructure**: Comprehensive and automated  
✓ **Test coverage**: Main gates pass consistently  
✓ **Source registry**: Conservative and well-documented  
✓ **Docker deployment**: Validated and working  

---

## What Needs Work (Post-Alpha)

⏳ **Temporal queries**: No as-of support  
⏳ **Memory depth**: Shallow implementation  
⏳ **Event tracking**: Limited to internal operations  
⏳ **Performance**: No caching or optimization  
⏳ **Advanced features**: All deferred to Phase 14+  

---

## Configuration & Environment

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL (prod) / SQLite (test)
- **Frontend**: React/Next.js, Node 20 (target), TypeScript, Tailwind CSS
- **Database**: PostgreSQL 12+ with PostGIS for geospatial queries
- **Cache**: Redis for session storage (optional, not core)
- **Auth**: JWT with custom RBAC
- **Testing**: pytest, Vitest, Docker Compose for local integration

---

## Deployment Reality

- **Docker**: Multi-stage build, working
- **Compose**: Local dev environment validated
- **CI/CD**: GitHub Actions with 9 proof gates
- **Infrastructure**: Bicep/Terraform ready (not yet deployed)
- **Scaling**: Single deployment only; no horizontal scaling

---

**Current reality**: This is a working research platform with solid fundamentals but incomplete advanced features. Safe for alpha; not for production.
