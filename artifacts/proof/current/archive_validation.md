# Archive Validation

- validated_at_utc: 2026-05-26T20:25:31.606015+00:00
- archive: [REDACTED_LOCAL_PATH]/judge_atlas_archive.zip
- archive_sha256: 52fc4dd13782a0e5a0fff4d739e3bc4102bba10f1b3a090074951c34ac274392
- expected_root: JUDGE_ATLAS-main
- actual_root: JUDGE_ATLAS-main
- top_level_roots: JUDGE_ATLAS-main
- root_match: yes
- valid: PASS
- compressed_size_bytes: 2047750
- uncompressed_size_bytes: 7802223

## Errors

- none

## Warnings

- release_gate_not_alpha_passed
- release_gate_not_release_candidate

## Largest Files

| path | uncompressed | compressed |
|---|---:|---:|
| JUDGE_ATLAS-main/backend/uv.lock | 769811 | 238625 |
| JUDGE_ATLAS-main/frontend/package-lock.json | 393441 | 85051 |
| JUDGE_ATLAS-main/scripts/release_gate.py | 111933 | 20796 |
| JUDGE_ATLAS-main/backend/app/models/entities.py | 101799 | 16701 |
| JUDGE_ATLAS-main/artifacts/proof/current/release_gate.json | 88824 | 13301 |
| JUDGE_ATLAS-main/backend/app/memory/contradiction_engine.py | 48640 | 8977 |
| JUDGE_ATLAS-main/backend/app/ingestion/sources/canada_saskatchewan_sources.yaml | 48464 | 6929 |
| JUDGE_ATLAS-main/artifacts/proof/current/proof_manifest.json | 47526 | 6543 |
| JUDGE_ATLAS-main/backend/app/tests/test_api.py | 43536 | 7488 |
| JUDGE_ATLAS-main/backend/app/api/routes/admin_sources.py | 41311 | 8548 |
| JUDGE_ATLAS-main/backend/app/tests/test_ingestion_runtime.py | 38018 | 5725 |
| JUDGE_ATLAS-main/backend/app/tests/test_phase5_adaptive_retry.py | 35181 | 4174 |
| JUDGE_ATLAS-main/backend/app/tests/test_ai_reasoning.py | 30318 | 4943 |
| JUDGE_ATLAS-main/backend/app/ingestion/courtlistener_bulk_normalizer.py | 29758 | 5588 |
| JUDGE_ATLAS-main/backend/app/tests/test_admin_ingestion.py | 29007 | 4529 |
| JUDGE_ATLAS-main/backend/app/tests/test_graph_layer.py | 28216 | 4765 |
| JUDGE_ATLAS-main/artifacts/proof/current/source_registry_status.json | 27776 | 3324 |
| JUDGE_ATLAS-main/backend/app/seed/sample_data.py | 25376 | 4657 |
| JUDGE_ATLAS-main/backend/app/tests/test_memory_runtime.py | 24708 | 4490 |
| JUDGE_ATLAS-main/backend/app/workers/postgres_queue.py | 24147 | 4457 |

## Largest Top-Level Directories

| path | uncompressed |
|---|---:|
| backend | 5511073 |
| frontend | 859320 |
| scripts | 697772 |
| docs | 362743 |
| artifacts | 244800 |
| .github | 47338 |
| demo | 26537 |
| infra | 17264 |
| REPO_REALITY.md | 7941 |
| Makefile | 7808 |
| STUBS_AND_PLACEHOLDERS.md | 4683 |
| docker-compose.yml | 2496 |
| STATUS.md | 2471 |
| CURRENT_STATUS.md | 2031 |
| PROOF_STATUS.md | 1941 |
| README.md | 1910 |
| RELEASE_MANIFEST.json | 1525 |
| RELEASE_BLOCKERS.md | 1291 |
| Dockerfile.proof | 890 |
| deploy | 389 |
