# Archive Validation

- validated_at_utc: 2026-05-26T06:50:50.903204+00:00
- archive: [REDACTED_LOCAL_PATH]/judge_atlas_archive.zip
- archive_sha256: 653b5643b71e8c496ca64006377653ec120da4d3e9530b1ca331d1cf5cd55cbf
- expected_root: JUDGE_ATLAS-main
- actual_root: JUDGE_ATLAS-main
- top_level_roots: JUDGE_ATLAS-main
- root_match: yes
- valid: FAIL
- compressed_size_bytes: 2043297
- uncompressed_size_bytes: 7776483

## Errors

- release_gate_not_alpha_passed
- release_gate_not_release_candidate

## Largest Files

| path | uncompressed | compressed |
|---|---:|---:|
| JUDGE_ATLAS-main/backend/uv.lock | 769811 | 238625 |
| JUDGE_ATLAS-main/frontend/package-lock.json | 393441 | 85051 |
| JUDGE_ATLAS-main/scripts/release_gate.py | 110371 | 20532 |
| JUDGE_ATLAS-main/backend/app/models/entities.py | 101799 | 16701 |
| JUDGE_ATLAS-main/artifacts/proof/current/release_gate.json | 88892 | 13325 |
| JUDGE_ATLAS-main/backend/app/memory/contradiction_engine.py | 48640 | 8977 |
| JUDGE_ATLAS-main/backend/app/ingestion/sources/canada_saskatchewan_sources.yaml | 48464 | 6929 |
| JUDGE_ATLAS-main/artifacts/proof/current/proof_manifest.json | 47573 | 6566 |
| JUDGE_ATLAS-main/backend/app/tests/test_api.py | 43536 | 7488 |
| JUDGE_ATLAS-main/backend/app/api/routes/admin_sources.py | 41311 | 8548 |
| JUDGE_ATLAS-main/backend/app/tests/test_ingestion_runtime.py | 38018 | 5725 |
| JUDGE_ATLAS-main/backend/app/tests/test_phase5_adaptive_retry.py | 35181 | 4174 |
| JUDGE_ATLAS-main/backend/app/tests/test_ai_reasoning.py | 30318 | 4943 |
| JUDGE_ATLAS-main/backend/app/ingestion/courtlistener_bulk_normalizer.py | 29758 | 5588 |
| JUDGE_ATLAS-main/backend/app/tests/test_admin_ingestion.py | 29007 | 4529 |
| JUDGE_ATLAS-main/backend/app/tests/test_graph_layer.py | 28216 | 4765 |
| JUDGE_ATLAS-main/artifacts/proof/current/source_registry_status.json | 27776 | 3325 |
| JUDGE_ATLAS-main/backend/app/seed/sample_data.py | 25376 | 4657 |
| JUDGE_ATLAS-main/backend/app/tests/test_memory_runtime.py | 24708 | 4490 |
| JUDGE_ATLAS-main/backend/app/workers/postgres_queue.py | 24147 | 4457 |

## Largest Top-Level Directories

| path | uncompressed |
|---|---:|
| backend | 5504065 |
| frontend | 859320 |
| scripts | 672007 |
| docs | 362763 |
| artifacts | 252219 |
| .github | 47320 |
| demo | 26537 |
| infra | 17264 |
| REPO_REALITY.md | 7941 |
| Makefile | 7808 |
| STUBS_AND_PLACEHOLDERS.md | 4683 |
| STATUS.md | 2477 |
| docker-compose.yml | 2372 |
| CURRENT_STATUS.md | 2035 |
| PROOF_STATUS.md | 1939 |
| README.md | 1910 |
| RELEASE_BLOCKERS.md | 1291 |
| RELEASE_MANIFEST.json | 1253 |
| Dockerfile.proof | 890 |
| deploy | 389 |
