# Archive Validation

- validated_at_utc: 2026-05-17T21:55:26.472394+00:00
- archive: /private/var/folders/xt/jh84t2kj6hl26tk5qx3m_28h0000gn/T/tmp.gNF2iYoI0R/judge_atlas_archive.zip
- archive_sha256: 44e022a727a38f18d870029a2d5241da86985ee2e7eb0b3cd2f0230aa33e6eaa
- expected_root: JUDGE_ATLAS-main
- actual_root: JUDGE_ATLAS-main
- top_level_roots: JUDGE_ATLAS-main
- root_match: yes
- valid: FAIL
- compressed_size_bytes: 1796862
- uncompressed_size_bytes: 6540432

## Errors

- proof_count_mismatch:release_gate_check_count=35 not found in CURRENT_PROOF.md

## Largest Files

| path | uncompressed | compressed |
|---|---:|---:|
| JUDGE_ATLAS-main/backend/uv.lock | 769811 | 238625 |
| JUDGE_ATLAS-main/frontend/package-lock.json | 357395 | 75752 |
| JUDGE_ATLAS-main/frontend/tsconfig.tsbuildinfo | 148225 | 44796 |
| JUDGE_ATLAS-main/backend/app/models/entities.py | 75663 | 11985 |
| JUDGE_ATLAS-main/scripts/release_gate.py | 73751 | 14278 |
| JUDGE_ATLAS-main/artifacts/proof/current/release_gate.json | 67162 | 10536 |
| JUDGE_ATLAS-main/backend/app/ingestion/sources/canada_saskatchewan_sources.yaml | 44787 | 6232 |
| JUDGE_ATLAS-main/backend/app/tests/test_api.py | 43068 | 7429 |
| JUDGE_ATLAS-main/backend/app/tests/test_ingestion_runtime.py | 38018 | 5725 |
| JUDGE_ATLAS-main/backend/app/api/routes/admin_sources.py | 35256 | 7270 |
| JUDGE_ATLAS-main/backend/app/tests/test_phase5_adaptive_retry.py | 35181 | 4174 |
| JUDGE_ATLAS-main/backend/app/tests/test_ai_reasoning.py | 30318 | 4943 |
| JUDGE_ATLAS-main/backend/app/ingestion/courtlistener_bulk_normalizer.py | 29758 | 5588 |
| JUDGE_ATLAS-main/backend/app/tests/test_admin_ingestion.py | 29153 | 4559 |
| JUDGE_ATLAS-main/backend/app/tests/test_graph_layer.py | 28216 | 4765 |
| JUDGE_ATLAS-main/artifacts/proof/current/source_registry_status.json | 27707 | 3209 |
| JUDGE_ATLAS-main/backend/app/seed/sample_data.py | 25376 | 4657 |
| JUDGE_ATLAS-main/backend/app/tests/test_memory_runtime.py | 24708 | 4490 |
| JUDGE_ATLAS-main/backend/app/tests/test_serializer_contracts.py | 24032 | 4726 |
| JUDGE_ATLAS-main/backend/app/tests/test_evidence_runtime.py | 23712 | 3905 |

## Largest Top-Level Directories

| path | uncompressed |
|---|---:|
| backend | 4433593 |
| frontend | 847391 |
| docs | 585562 |
| scripts | 450567 |
| artifacts | 142400 |
| .github | 29006 |
| demo | 26537 |
| infra | 17264 |
| Makefile | 4438 |
| docker-compose.yml | 1894 |
| RELEASE_MANIFEST.json | 955 |
| README.md | 825 |
