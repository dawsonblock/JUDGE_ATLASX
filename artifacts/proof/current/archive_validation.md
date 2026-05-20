# Archive Validation

- validated_at_utc: 2026-05-20T08:16:48.654894+00:00
- archive: /private/var/folders/xt/jh84t2kj6hl26tk5qx3m_28h0000gn/T/tmp.0uwxmSnNr8/judge_atlas_archive.zip
- archive_sha256: b95cadf264daf1c955590412aaeec615897f47bad1915fc9b4f4b56bc715d6b6
- expected_root: JUDGE_ATLAS-main
- actual_root: JUDGE_ATLAS-main
- top_level_roots: JUDGE_ATLAS-main
- root_match: yes
- valid: FAIL
- compressed_size_bytes: 2051999
- uncompressed_size_bytes: 7668222

## Errors

- missing_required_proof_file:artifacts/proof/current/FIX_VERIFICATION_REPORT.md

## Largest Files

| path | uncompressed | compressed |
|---|---:|---:|
| JUDGE_ATLAS-main/backend/uv.lock | 769811 | 238625 |
| JUDGE_ATLAS-main/frontend/package-lock.json | 389365 | 84278 |
| JUDGE_ATLAS-main/frontend/tsconfig.tsbuildinfo | 193656 | 59785 |
| JUDGE_ATLAS-main/backend/app/models/entities.py | 91264 | 14639 |
| JUDGE_ATLAS-main/scripts/release_gate.py | 78988 | 15262 |
| JUDGE_ATLAS-main/artifacts/proof/current/release_gate.json | 76039 | 11724 |
| JUDGE_ATLAS-main/backend/app/ingestion/sources/canada_saskatchewan_sources.yaml | 48034 | 6676 |
| JUDGE_ATLAS-main/backend/app/tests/test_api.py | 43068 | 7429 |
| JUDGE_ATLAS-main/backend/app/memory/contradiction_engine.py | 41951 | 7023 |
| JUDGE_ATLAS-main/backend/app/tests/test_ingestion_runtime.py | 38018 | 5725 |
| JUDGE_ATLAS-main/backend/app/api/routes/admin_sources.py | 35256 | 7270 |
| JUDGE_ATLAS-main/backend/app/tests/test_phase5_adaptive_retry.py | 35181 | 4174 |
| JUDGE_ATLAS-main/backend/app/tests/test_ai_reasoning.py | 30318 | 4943 |
| JUDGE_ATLAS-main/backend/app/ingestion/courtlistener_bulk_normalizer.py | 29758 | 5588 |
| JUDGE_ATLAS-main/backend/app/tests/test_admin_ingestion.py | 29153 | 4559 |
| JUDGE_ATLAS-main/backend/app/tests/test_graph_layer.py | 28216 | 4765 |
| JUDGE_ATLAS-main/artifacts/proof/current/source_registry_status.json | 27724 | 3225 |
| JUDGE_ATLAS-main/backend/app/seed/sample_data.py | 25376 | 4657 |
| JUDGE_ATLAS-main/backend/app/tests/test_memory_runtime.py | 24708 | 4490 |
| JUDGE_ATLAS-main/artifacts/proof/current/proof_manifest.json | 24322 | 4041 |

## Largest Top-Level Directories

| path | uncompressed |
|---|---:|
| backend | 5297305 |
| frontend | 1029382 |
| docs | 605044 |
| scripts | 474148 |
| artifacts | 149606 |
| .github | 35894 |
| demo | 26537 |
| infra | 17264 |
| Makefile | 9767 |
| REPO_REALITY.md | 7414 |
| STUBS_AND_PLACEHOLDERS.md | 4683 |
| PROOF_STATUS.md | 2533 |
| docker-compose.yml | 2483 |
| STATUS.md | 1864 |
| RELEASE_MANIFEST.json | 1152 |
| CURRENT_STATUS.md | 1075 |
| README.md | 1073 |
| RELEASE_BLOCKERS.md | 998 |
