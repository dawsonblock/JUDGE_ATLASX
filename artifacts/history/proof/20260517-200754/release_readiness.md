# RELEASE_READINESS

- generated_at_utc: 2026-05-17T06:13:41.771068+00:00
- overall_status: alpha-proof-pass
- production_ready: false
- release_recommendation: alpha-proof-pass
- archive_hash: 9554109efba2b85785bb0ffd48cb918b78f17771
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
| check_false_claims | PASS | 0 | artifacts/proof/current/check_false_claims.log | cfb4d11f86760a5ca75365492872d7b272f784b0a8ed5be12e6aa4ee70567e4b |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | 8f6537cb7e3236306832e35ae185e1dcab93b5c124f4cf5380d460112fdaa3e2 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 24af56cc9417a83aac6f33ce20129f0fc430d6c8335ef618133aac99907ffc75 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 4b3422629a61752560e45a67923caa0b6d7024f6c094d38b2502e8c6907e050a |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 4c94fddaaf466b650ad37268238d19ba01c7a54cd5f51bee95bc4cab21c9c126 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 5acf1cb286e095bb5590de3939b91bf09465c986dd37d6a90d0f056bbc8b03b3 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 1437fafeec3728880ccae607718470279dd9b635e9bb3207249833835233f43b |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 68683c941f53fd55547c17b6a1b7a966702a2b51e89bd6832b00e772606b6b6e |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 566b533769efda184c621fadcbb3499a3de7b732897627c27b430e8565082bbb |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | ce75fe7a876fdb3f1ef137ef6ce8a6a6b03eea03e1e415e11f056520146c1137 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | ec8f978f344af50781b79858ffffa3f3da2a9df05cec23d593f532de427a37e9 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | a24f4940adc7597eeb444006b65dfb80f5a5adcb7d2b69c4d6322b7d429d911f |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 4da6afd155a16ecec95e3fc15909c120121302341ad3c037427a526273e53c63 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 29c955c125e4259b977ac94f44f7e6e7763d9a3463c0eee07b8be3115ccf5ae6 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 75920c1972c0db9e68cacefe8d25b4257c34010edf44288bd6c9e66128ff1d99 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 58b3f8dd1c4094dc2797c666bd407916dce63ab6deb182d7389c619d8eef1360 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 70b9802c3f798a2a035b7654978d7ed3436d20ab576ffc46b5c3cf0deec198ed |

## Remaining Blockers

- none

## Stale Or Misreported Claims

- none

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
