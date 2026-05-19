# RELEASE_READINESS

- generated_at_utc: 2026-05-17T20:10:27.099024+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 703cc67defe1ce64d5627219f2f4373e20ce08e2
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- gate_runner_node_version: v24.15.0
- frontend_node_gate_version: v25.9.0
- node_version: v24.15.0
- npm_version: 11.12.1

## Required Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| check_no_pyc | PASS | 0 | artifacts/proof/current/check_no_pyc.log | a846f2e3cfab43e1b94af70247e6dff79ec62b983961a207185d87595b1b7ff6 |
| check_false_claims | PASS | 0 | artifacts/proof/current/check_false_claims.log | ef04562ae44d2a4e2489ef39646502a7b42c83f212cb7679c6ab98e035db955e |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | FAIL | 1 | artifacts/proof/current/backend_import.log | 0a8e31eae2e395f494747d547389b12ccaf6225949fa094047d32edec3a964d9 |
| backend_pytest | FAIL | 4 | artifacts/proof/current/backend_pytest.log | 377e1354102293f874137765668721b6054ac2e44a25436718889fc491bcd16e |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | FAIL | 1 | artifacts/proof/current/postgis_proof.log | 6b18e64d9ce53a3e065c35ff61e35c7c602e8dbddedb0b225d1e2b87eaf027ab |
| egress_proxy_proof | FAIL | 4 | artifacts/proof/current/egress_proxy_proof.log | 8104bf9142e2e739b956ed2da14fcb7016268e1021d98bce7194e74a23bc6688 |
| demo_proof | FAIL | 1 | artifacts/proof/current/demo_proof.log | 38dd8eeb75ca7fa4e36ba434599e4ff59bd3c30055af7a39a8d2d45327103598 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 3820300463904ab2a898dc404dfce688ea323dff2d53f4d5557a15a9fb53c3ae |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 880797ab78071bebda41affb0efc5353721a144059f2b9c3d83c158a9de9eade |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 2a93e8b02701655b79484371793ca80791eda6c088863dd68202d0a0df19165f |
| auth_mutation_route_coverage | FAIL | 4 | artifacts/proof/current/auth_mutation_route_coverage.log | 377e1354102293f874137765668721b6054ac2e44a25436718889fc491bcd16e |
| mutation_fail_closed_coverage | FAIL | 4 | artifacts/proof/current/mutation_fail_closed_coverage.log | 377e1354102293f874137765668721b6054ac2e44a25436718889fc491bcd16e |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 3a6038526bd672a50e98cb06131bb7e1017015fd28922e16bbd84ea2a90eaddf |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 1ed9c03c2050691ece07b6b9f96bc9b573d14de5fa19a27d684d6d8f595accde |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | a24f4940adc7597eeb444006b65dfb80f5a5adcb7d2b69c4d6322b7d429d911f |
| check_api_contracts | FAIL | 1 | artifacts/proof/current/check_api_contracts.log | d361118566a59d167c2bd7834fda71083835910f4d5877064b5dc2c38eacc21e |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 6cefc62f18ffb2e57b9a64cb51e299efdcc71600f09b187538d9a83b064ba233 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 4da6afd155a16ecec95e3fc15909c120121302341ad3c037427a526273e53c63 |
| map_route_check | FAIL | 1 | artifacts/proof/current/map_route_check.log | e0fa1b76d58aedcc158a19058332034c978fbd626c101082396263b05feb296b |
| public_api_boundary | FAIL | 4 | artifacts/proof/current/public_api_boundary.log | 377e1354102293f874137765668721b6054ac2e44a25436718889fc491bcd16e |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | d61619aec0e56798ea9da3efe15673b4059b1d1a5533a6665bbebc88155f0da4 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | c26303814a993d326ec307cdc6c857bedae29edd5978a34749f9ce9b4b0e22b0 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | d7cf01ef78f52fc1aa01b9edce87a7ef883200dd9663df9270b55b2184781705 |

## Remaining Blockers

- required_gate_failed:backend_import
- required_gate_failed:backend_pytest
- required_gate_failed:postgis_proof
- required_gate_failed:egress_proxy_proof
- required_gate_failed:demo_proof
- required_gate_failed:auth_mutation_route_coverage
- required_gate_failed:mutation_fail_closed_coverage
- required_gate_failed:check_api_contracts
- required_gate_failed:map_route_check
- required_gate_failed:public_api_boundary

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
