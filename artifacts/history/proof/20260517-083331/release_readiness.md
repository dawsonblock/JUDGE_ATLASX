# RELEASE_READINESS

- generated_at_utc: 2026-05-17T08:32:07.169980+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 71f864da654f020bd6c2917557c35e1fc88ab50e
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- node_version: v24.15.0
- npm_version: 11.12.1

## Required Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| check_no_pyc | PASS | 0 | artifacts/proof/current/check_no_pyc.log | a846f2e3cfab43e1b94af70247e6dff79ec62b983961a207185d87595b1b7ff6 |
| check_false_claims | FAIL | 1 | artifacts/proof/current/check_false_claims.log | 90b093bf3fc9b60c053ad49d2cdfe5595fdde1bafc713eead49e0e9ae7ffccc3 |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | FAIL | 1 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | 20c89096311e8a8e2ab5eaaa870d94ea7ec84c5beee7d05d12adb5f0fa841da3 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | FAIL | 1 | artifacts/proof/current/check_external_boundaries.log | 6aeda0e8f969c4341a302e5cf7b32a8c7e4641e818523af9a707cb0ab95593d5 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | 90d607d6e74723b8807a06f5ae2f0d53c8da5049d6cfbb35d6f7beb95d307a05 |
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | 9425f032eae6d7ec0c50f02d3a468d0af0cbeb594ec9495e34ec998305c72005 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | e1065f41501785ea15a5a7f75563648bbacbe4621ce5b8c159300b6c6d9ed115 |
| egress_proxy_proof | FAIL | 1 | artifacts/proof/current/egress_proxy_proof.log | 3c884260628bdbd7c2956f2fa31b61f0ad8e2db3182ad8a340b0478c45d71912 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 22e7bf3bc97340963e950595cb2bff748a6c447d3ed2ba5be08ac98f358686ac |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 880797ab78071bebda41affb0efc5353721a144059f2b9c3d83c158a9de9eade |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 4893061efde69444b67edc67250c5956d68cb1ae0884844eb5cefffe32a0fe11 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | e8b12eb9c14e20ba6d6f42d6a6564099a0106363b2d2c716df325fb3a6e8b6f6 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | a3743b2a379a4c611aab88f2dd4a717b1f18ae345d3b524353c6daddbbda95ef |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 7776e0dccb191ea8b622dd2cf437dfc9bb06749d3a4797a38cbb3c939d12d639 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 24a693a73f32f4e560e7c2947deab9f33cc5babe11841d08c45501abd9e5d05f |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | f22be5d40d7f70376f1085cfbce6102bad9d3133ec312701c0aabbb9ec0a7928 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 6cefc62f18ffb2e57b9a64cb51e299efdcc71600f09b187538d9a83b064ba233 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 64b44871b811c0e727d8523ff51338f68993293de5ff9ab1d34287e46ce3c281 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | FAIL | 2 | artifacts/proof/current/public_api_boundary.log | 5025336cfdba0a5594150b7e9e252d512aefd82d38283280e120e7a2c9233438 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 47fc6178a3101eddfd11cef334d35365e93322d076f8732e3d372aa25d68f9de |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | f3596fd904fb81db0b201fa003404853ff29937cd08a9343805626656ac9d95b |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | a0e28fab06b75336d037d3679bc016290cc78b2bfeb2b3ea22aa647dd713f9a1 |

## Remaining Blockers

- required_gate_failed:check_false_claims
- required_gate_failed:check_no_direct_ingestion_network_clients
- required_gate_failed:check_external_boundaries
- required_gate_failed:backend_pytest
- required_gate_failed:egress_proxy_proof
- required_gate_failed:public_api_boundary
- required_gate_failed:archive_validation
- archive_validation_not_pass

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
