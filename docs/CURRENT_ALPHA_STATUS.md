# CURRENT_ALPHA_STATUS

## Truth Statement

JUDGE_ATLASX is an evidence-governed Canadian legal intelligence alpha. Evidence is authoritative. AI and memory outputs are derivative only. All public-facing data requires human review approval and must be linked to an evidence snapshot. This is an alpha release, not a production legal authority.

- generated_at_utc: 2026-05-19T00:00:00.000000+00:00
- commit_hash: HEAD
- operational_posture: alpha
- production_ready: false
- alpha_gate_passed: true
- proof_freshness_result: PASS
- release_gate_check_count: 37
- postgis_proof_result: PASS
- egress_proxy_proof_result: PASS
- demo_proof_result: PASS

## Status

- This repository is in alpha proof-hardened posture.
- This repository is not approved for production deployment.
- Human review remains mandatory for public publication decisions.

## Phase 1-13 Completion Summary (2026-05-19)

All 13 phases of the repair plan have been completed:

**Phase 1: Graph Central**
- Fixed imports and entity fields in graph_central.py
- Added test_graph_central.py

**Phase 2: Risk Tiering**
- Fixed risk tiering logic thresholds
- Added test_risk_tiering.py

**Phase 3: Durable Contradiction System**
- Created memory_contradictions migration (20260518_0001_add_memory_contradictions.py)
- Upgraded contradiction_engine.py for durability with persistence
- Added test_memory_contradictions.py

**Phase 4: Publication Gate Enhancement**
- Updated publication_gate.py with contradiction checks
- Added validation for claim status, private-person allegations, source status
- Added test_publication_gate_contradictions.py

**Phase 5: Frontend Node Alignment**
- Aligned frontend Node version to 20 (.nvmrc)
- Downgraded @types/node to v20 (package.json)

**Phase 6: Ingestion Queue System**
- Created ingestion_jobs migration (20260519_0001_add_ingestion_queue_jobs.py)
- Implemented postgres_queue.py for durable job processing
- Added test_postgres_queue.py

**Phase 7: Source Registry Validation**
- Tightened source registry validation to require:
  - Adapter configuration for machine_ingest sources
  - Test fixtures for all sources
  - Deprecation policy for deprecated sources
  - Public status flag for public sources
  - Secret requirements for sources that need secrets

**Phase 8: E2E Evidence Pipeline**
- Added test_e2e_evidence_pipeline.py for end-to-end testing

**Phase 9: Claim-to-Graph Integration**
- Implemented claim_to_graph.py for graph entity/relationship conversion

**Phase 10: Reviewer Dashboard Routes**
- Added contradiction management routes to admin_review.py:
  - GET /api/admin/contradictions (list open contradictions)
  - GET /api/admin/contradictions/by-claim/{claim_id}
  - GET /api/admin/contradictions/by-entity/{entity_id}
  - POST /api/admin/contradictions/{contradiction_id}/resolve

**Phase 11: Source Enablement**
- Confirmed source registry supports one-at-a-time enablement
- Sources default to disabled (enabled_default: false)
- operator_next_step fields guide individual source activation

**Phase 12: Proof Regeneration**
- Implemented scripts/regenerate_proof.py for on-demand proof regeneration
- Supports --skip-db and --steps flags for selective regeneration

**Phase 13: CI Hard Gate**
- Added .github/workflows/hard-gate.yml for CI enforcement
- Runs proof regeneration, source validation, release gate verification

## Current Blockers

**Alpha Repair Blockers**: cleared

**Production Blockers** (active):
- Postgres queue production gate warning needs update (queue is alpha-hardened with worker-safe features)
- docs/runtime/INGESTION_SYSTEM.md is stale (lists sources that are disabled in source registry)
- claim_to_graph.py does not persist real graph edges to database
- remove_claim_from_graph() raises NotImplementedError instead of deactivate/hide behavior
- named-person allegation policy needs elevated approval path
- contradiction intelligence needs source-authority reasoning
- only one live source is enabled (justice_canada_laws_xml)
- no automated proof consistency check to prevent artifact disagreements

**Production Ready**: false
