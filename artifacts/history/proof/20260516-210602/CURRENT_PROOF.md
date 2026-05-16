# CURRENT_PROOF

- generated_at_utc: 2026-05-15T07:24:58.369721+00:00
- commit_hash: 5758506700958171c3bd2a736a289b508467f7d7
- alpha_gate_status: PASS
- alpha_gate_passed: true
- release_gate_check_count: 37
- docker_available: true
- postgis_proof_result: PASS
- egress_proxy_proof_result: PASS
- demo_proof_result: PASS
- proof_freshness_result: PASS
- proof_input_tree_hash: c05c14150bf6842334c49556718cdaa0793dbc697184c381d8c76681380571e3
- proof_input_file_count: 804
- egress_proxy_proof_log: artifacts/proof/current/egress_proxy_proof.log
- demo_proof_log: artifacts/proof/current/demo_proof.log

## Runtime Metadata

- gate_runner_python_version: 3.11.14
- gate_runner_python_executable: /Users/dawsonblock/Downloads/JUDGE_ATLAS-main 2/backend/.venv/bin/python3
- backend_test_python_version: 3.11.14
- backend_test_python_executable: /Users/dawsonblock/Downloads/JUDGE_ATLAS-main 2/backend/.venv/bin/python
- backend_required_python: >=3.11
- node_version: v20.20.2
- npm_version: 10.8.2
- platform: macOS-26.2-arm64-arm-64bit
- test_database_backend: sqlite
- test_database_url_type: sqlite_file

## Scope and Safety

- Current status: proof-hardened alpha.
- Not ready for production deployment.
- Does not hold legal authority.
- Evidence snapshots are authoritative; memory is derivative.
- AI is reviewer assistance only.
- Source ingestion is disabled by default unless explicitly enabled.
- External folders are reference-only.
- JWT mutation authority is current; legacy shared-token compatibility is deprecated.
- make verify = local no-Docker quality checks.
- make release-proof-local = Docker/PostGIS alpha release gate.
- Current alpha release is blocked if Docker/PostGIS proof fails.
- Docker/PostGIS proof passed in the current release gate.
- Dedicated egress proxy proof passed in the current release gate.
- Dedicated synthetic demo proof passed in the current release gate.
- Proof freshness passed against the stored proof-input file list and tree hash.
- Archive validation passed against the final distributable archive shape.
- archive_validation_log: artifacts/proof/current/archive_validation.log
- archive_validation_supported_shapes:
  - JUDGE-main/
  - */JUDGE-main/

## Governance Status

- legacy_shared_token_status: deprecated, removal plan documented
- dependency_security_status: npm audit issues triaged for alpha; remediation plan documented

## Current Proof Facts

- backend pytest: 2801 passed, 4 skipped
- backend import proof: PASS (103 routes)
- frontend contracts: 38 passed
- public API boundary: 33 passed
- Docker runtime preflight: PASS
- PostGIS proof: PASS
- egress proxy proof: PASS
- demo proof: PASS
- mutation fail-closed coverage: PASS
- Alembic migrations: 49

## Egress Proxy Coverage

- Dedicated gate artifact: artifacts/proof/current/egress_proxy_proof.log.
- Production startup proxy policy coverage: backend/app/tests/test_production_fetch_egress_policy.py.
- Runtime proxy opener/wiring coverage: backend/app/tests/test_source_fetcher_proxy.py.
- SSRF defense context coverage remains in backend/app/tests/test_source_fetcher_ssrf.py.

## Canonical Artifacts

- artifacts/proof/current/proof_manifest.json
- artifacts/proof/current/release_gate.json
- artifacts/proof/current/release_gate.log
- artifacts/proof/current/docker_runtime_preflight.log
- artifacts/proof/current/postgis_proof.log
- artifacts/proof/current/egress_proxy_proof.log
- artifacts/proof/current/demo_proof.log
- artifacts/proof/current/proof_freshness.log
- artifacts/proof/current/archive_validation.log
- artifacts/proof/current/backend_import.log
- artifacts/proof/current/backend_pytest.log
- artifacts/proof/current/backend_proof_summary.json
- artifacts/proof/current/frontend_proof_summary.json
- artifacts/proof/current/frontend_node_gate.log
- artifacts/proof/current/frontend_install.log
- artifacts/proof/current/frontend_lint.log
- artifacts/proof/current/frontend_typecheck.log
- artifacts/proof/current/frontend_contracts.log
- artifacts/proof/current/frontend_build.log
- artifacts/proof/current/check_api_contracts.log
- artifacts/proof/current/static_guards.log
- artifacts/proof/current/map_route_check.log
- artifacts/proof/current/public_api_boundary.log
- artifacts/proof/current/mutation_fail_closed_coverage.log
- artifacts/proof/current/source_registry_status.json
- artifacts/proof/current/release_readiness.md
- artifacts/proof/current/CURRENT_ALPHA_STATUS.md
- artifacts/proof/current/SOURCE_REGISTRY_STATUS.md
- artifacts/proof/current/PROOF_POLICY.md
- artifacts/proof/current/REPAIR_REPORT.md

## Hardening Pass — Review Status Normalization (applied after commit 58f055d)

8 policy/data bugs fixed across 7 source files; 2 new Alembic migrations added.

| # | Bug | File | Fix |
|---|-----|------|-----|
| 1 | `LegalInstrument.review_status` ORM default was wrong ingestion sentinel `"pending"` | `entities.py` | Default changed to literal `"pending_review"` |
| 2 | Event evidence anchor did not verify linked source is reviewed AND public | `publication_policy.py` | Added `entity_review_status(source) in PUBLIC_REVIEW_STATUSES` + `entity_public_visibility(source)` checks |
| 3 | `RelationshipEvidence` had no `review_status` column; policy fell through to `None` | `entities.py` | Added `review_status` column; added `relationship_public_status()` helper |
| 4 | `is_publishable()` / `check_publication_safety()` had no deprecation notices | `publish_rules.py`, `ingestion/publish_rules.py` | Added `.. deprecated::` docstrings pointing to canonical policy functions |
| 5a | `_legal_context_citations()` did not verify `SourceSnapshot.content_hash IS NOT NULL` | `evidence_chat.py` | Added `SourceSnapshot` join + `content_hash.is_not(None)` filter |
| 5b | `chat_about_evidence()` allowed `relationship_status="pending"` | `evidence_chat.py` | Removed `"pending"` from allowlist |
| 6 | `ingestion_identity_hash` indexes were plain non-unique; NULLs broke idempotency | Migrations 0003 + 0004 | Partial unique indexes `WHERE ingestion_identity_hash IS NOT NULL` |
| 7 | `official_legislation` authority only allowed `ReviewItem`; blocked `LegalInstrument`/`LegalSection` | `ingestion/source_rules.py` | Expanded to `{SourceSnapshot, LegalInstrument, LegalSection, ReviewItem}` |
| 8 | `LegalInstrument` missing from admin review queue `_review_statements()` | `admin_review.py` | Added `"legal_instrument"` branch + added to default `requested_types` |
| 9 | `publicMapMarkerSchema.review_status` was `z.string()` — no enum validation | `frontend/lib/schemas/publicMap.ts` | Changed to `z.enum(CANONICAL_REVIEW_STATUSES)` with exported const array and type |
