<!-- markdownlint-disable -->

# Future Architecture

Status: NOT_IMPLEMENTED — planning document only

This document describes capabilities that are explicitly **not present** in the current codebase.
None of the systems below are operational. This document is a planning reference for post-v1 development.

---

## 1. Semantic Search

**Status**: NOT_IMPLEMENTED  
**Config gate**: `JTA_EMBEDDINGS_ENABLED=true` (defaults False; heavy torch dependency)

### Planned

- Sentence-transformer embeddings (`all-MiniLM-L6-v2` or similar) over canonical entity text
- pgvector extension on PostgreSQL for vector similarity search
- Hybrid retrieval: BM25 keyword score + cosine similarity re-rank
- Expose via `GET /api/v1/search/semantic?q=...`

### Dependencies Not Yet Present

- `pgvector` PostgreSQL extension
- `sentence-transformers` Python package (guarded by feature flag)
- Embedding generation pipeline (batch + incremental)
- Vector index maintenance (incremental rebuild on new records)

### Constraints

- Embeddings must be regenerated after any canonical text normalization change
- Source-tier filtering must be applied before embedding search (no unsourced results)
- Output must include provenance metadata (which source, which snapshot, confidence score)

---

## 2. AI-Assisted Review

**Status**: NOT_IMPLEMENTED (stub routes exist in `ai_review.py`, `ai_correctness.py`, `chat.py`)  
**Config gate**: `JTA_OLLAMA_ENABLED=true` (defaults False)

### Planned

- Local LLM (via Ollama) for:
  - Suggesting review decisions on queued items
  - Flagging potential PII in ingested records
  - Confidence scoring on entity resolution
- AI suggestions must be displayed as suggestions only, never auto-applied
- All AI decisions must be logged with model version + prompt hash for audit trail

### Hard Constraints (from AI_BOUNDARY_RULES.md)

- AI cannot create, modify, or delete legal records
- AI cannot make publication decisions
- AI outputs are advisory only and require human review confirmation
- AI subsystem operates in a read-only context; no write access to case/judge/defendant tables

---

## 3. Graph Intelligence

**Status**: Partial infrastructure (graph routes exist); intelligence layer NOT_IMPLEMENTED

### Planned

- Multi-hop relationship traversal (judge → cases → defendants → related entities)
- Influence/centrality scoring for judge and case networks
- Timeline anomaly detection (statistically unusual sentencing patterns)
- Expose via enhanced `GET /api/v1/graph/entity/{type}/{id}/subgraph?depth=N`

### Current State

- Basic graph routes exist (`graph.py`) with entity edge queries
- No scoring, traversal algorithms, or anomaly detection implemented
- `enable_public_relationship_arcs` gate exists but requires policy sign-off

---

## 4. Cross-Jurisdiction Expansion (Beyond Saskatchewan / Federal Canada)

**Status**: NOT_IMPLEMENTED  
**Current scope**: Saskatchewan + Federal Canada sources only

### Planned Expansion (requires new source registrations + ToS verification)

- Ontario courts (CanLII + Ontario Court of Justice)
- British Columbia courts
- Alberta Queen's Bench
- Federal administrative tribunals

### Requirements Before Expansion

- Each new province requires its own `confidence_class` + `terms_verified` entries
- Separate rate-limit policy per jurisdiction
- Policy review for cross-provincial PII handling differences
- Separate `retention_policy` if provincial law differs from federal baseline

---

## 5. Public Correction and Takedown System

**Status**: NOT_IMPLEMENTED  
**Reference**: `docs/CORRECTION_AND_TAKEDOWN.md`

### Planned

- Public web form for individuals to submit correction requests
- Admin review queue for takedown/correction requests (separate from ingestion review)
- Formal response timeline (target: 14 business days per `docs/CORRECTION_AND_TAKEDOWN.md`)
- Audit log of all correction/takedown decisions

### Current Gap

- No correction request model or table exists
- Admin review queue (`admin_review.py`) handles ingestion review only
- No external-facing correction form in the frontend

---

## 6. Real-Time Ingestion (Event-Driven)

**Status**: NOT_IMPLEMENTED  
**Current model**: Polling via APScheduler (`JTA_ENABLE_SCHEDULER`)

### Planned

- Webhook receivers for sources that support push (e.g., CKAN DCAT feeds)
- Message queue (Redis Streams or similar) for fan-out to multiple consumers
- Near-real-time evidence snapshot creation on new record receipt

### Constraint

- APScheduler polling approach is correct for v1; real-time is post-v1 only

---

## 7. Multi-Tenant / Organization Accounts

**Status**: NOT_IMPLEMENTED  
**Current model**: Single-admin JWT with first-admin bootstrap

### Not Planned for v1

- Organization-scoped data views
- Role-based access control beyond admin/non-admin
- API keys per organization

---

## Implementation Policy

> Features listed in this document **must not** be implemented piecemeal without:
>
> 1. A corresponding entry in `COMPLETION_CHECKLIST.md`
> 2. A policy review for any feature that touches publication decisions or PII
> 3. A sprint plan approved before coding begins
>
> Partial stubs for unimplemented features **must** carry a `NOT_IMPLEMENTED` comment at module top level.
