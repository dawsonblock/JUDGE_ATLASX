# RELEASE_READINESS

- generated_at_utc: 2026-05-21T03:02:47.447031+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: f52e5a08758e41da613f4af98207544ad51fac93
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- node_version: v24.15.0
- npm_version: 11.12.1

## Required Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| check_no_pyc | PASS | 0 | artifacts/proof/current/check_no_pyc.log | a846f2e3cfab43e1b94af70247e6dff79ec62b983961a207185d87595b1b7ff6 |
| check_false_claims | PASS | 0 | artifacts/proof/current/check_false_claims.log | cfb4d11f86760a5ca75365492872d7b272f784b0a8ed5be12e6aa4ee70567e4b |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | f722c82c7def9e790c1676a4e1bdb4c064370a48071b37d54cf00c26ca8efd47 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | a1881ae76453b39c85292fa2ffaf9e60b655c988c34498eeec12bdcca7d26936 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | missing |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | missing |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | missing |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | missing |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | missing |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | missing |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | missing |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | missing |
| prepare_proof_db | FAIL | 1 | artifacts/proof/current/prepare_proof_db.log | missing |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 1179d0c8c1c56de20d4f917fd60915207780fa80305d5ffb0e8d31ff25adc9a1 |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | d6afe0d26bccad88e4e056fedddd8cc4319ef8a9fd7e4e2b6690d3d329236d3d |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 68683c941f53fd55547c17b6a1b7a966702a2b51e89bd6832b00e772606b6b6e |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | ce22630fc7c34a988df630b4a92fb58d299903bc888dd68e961f12bfa2af1024 |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 1aaabeefd07a61f2e5f39241277580ddbe158ff27c88271f2732e612208ffa33 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 3e80d310857178d82f4e368cc0bbc8cd94e671e4c32375ad818e0cc46f344d01 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 73855124fc285c86baa23c579d9a0cc07bee3a5f095a6b77ef8fa6453aeb11bd |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 7aa81e613784be4a0a2f28b43c04741a9b668f4fb39245d5fc28aafe5dcea65a |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 26637ef0dc1d70375ad0cf4847d42a82c9add4f92f36883652626b2550aadac5 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | fe29ab3e3dd26691cf8a9c321c8ab10e780d24b62fa0fc67bd4289823a749f7c |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 25a0f916b5b54858c77993005e7309b1041e7977a8b87f74c1330202048a66b7 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | c911332c65578ff8b9353b82e7e68e9067f4e8b3efbfc9da2b5b81e50108c500 |

## Remaining Blockers

- missing_log:docker_runtime_preflight:artifacts/proof/current/docker_runtime_preflight.log
- missing_log_sha256:docker_runtime_preflight
- missing_log:postgis_proof:artifacts/proof/current/postgis_proof.log
- missing_log_sha256:postgis_proof
- missing_log:egress_proxy_proof:artifacts/proof/current/egress_proxy_proof.log
- missing_log_sha256:egress_proxy_proof
- missing_log:demo_proof:artifacts/proof/current/demo_proof.log
- missing_log_sha256:demo_proof
- missing_log:validate_sources:artifacts/proof/current/validate_sources.log
- missing_log_sha256:validate_sources
- missing_log:check_yaml_duplicate_keys:artifacts/proof/current/check_yaml_duplicate_keys.log
- missing_log_sha256:check_yaml_duplicate_keys
- missing_log:verify_source_registry:artifacts/proof/current/verify_source_registry.log
- missing_log_sha256:verify_source_registry
- missing_log:source_registry_status:artifacts/proof/current/source_registry_status.log
- missing_log_sha256:source_registry_status
- required_gate_failed:prepare_proof_db
- missing_log:prepare_proof_db:artifacts/proof/current/prepare_proof_db.log
- missing_log_sha256:prepare_proof_db

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
