# RELEASE_READINESS

- generated_at_utc: 2026-05-17T05:28:23.713753+00:00
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
| check_false_claims | PASS | 0 | artifacts/proof/current/check_false_claims.log | cfb4d11f86760a5ca75365492872d7b272f784b0a8ed5be12e6aa4ee70567e4b |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | f722c82c7def9e790c1676a4e1bdb4c064370a48071b37d54cf00c26ca8efd47 |
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | 280a6a0cc4b8b79f0a487cc5e97cbd7c36c0a0e0f7953de39a186f4132d2bfc0 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | FAIL | 1 | artifacts/proof/current/postgis_proof.log | bf9bf5cf9205ce13bd6f93d2137323bb5f37d9944db6c438ad7b0cd355f2c701 |
| egress_proxy_proof | FAIL | 1 | artifacts/proof/current/egress_proxy_proof.log | a68378810a48078fc66fb9b291298fba8fb3d619ea7204b91d8e7e71b75f11b0 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 333a6a576105c7eda85b90b1056ea1db8358fb534793f9c199f31d2396ae2491 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 3f71551b1ee04e799767b4f6c369e90f1a3386a3630c394b40f728d738b65164 |
| auth_mutation_route_coverage | FAIL | 1 | artifacts/proof/current/auth_mutation_route_coverage.log | 280a6a0cc4b8b79f0a487cc5e97cbd7c36c0a0e0f7953de39a186f4132d2bfc0 |
| mutation_fail_closed_coverage | FAIL | 1 | artifacts/proof/current/mutation_fail_closed_coverage.log | 280a6a0cc4b8b79f0a487cc5e97cbd7c36c0a0e0f7953de39a186f4132d2bfc0 |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 76ea0ac015cb9d9c288e4024304d32fba7a820308e1ff8824435bdda77abd1c2 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | cf73cc9d3ec494c8e8b87d942e8c36c15ee748b4620d82347852a61ed0f68a18 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | a24f4940adc7597eeb444006b65dfb80f5a5adcb7d2b69c4d6322b7d429d911f |
| check_api_contracts | FAIL | 1 | artifacts/proof/current/check_api_contracts.log | 8c8af47fa670772a62313d1e6fff77a730266fd6003a5a0ac5d317d226d88aa9 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 64b44871b811c0e727d8523ff51338f68993293de5ff9ab1d34287e46ce3c281 |
| map_route_check | FAIL | 1 | artifacts/proof/current/map_route_check.log | 707e94ad6a5784569796025b9ec6fb48f1f9047fd983aa29700e1bbbb6d468e7 |
| public_api_boundary | FAIL | 1 | artifacts/proof/current/public_api_boundary.log | 280a6a0cc4b8b79f0a487cc5e97cbd7c36c0a0e0f7953de39a186f4132d2bfc0 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 8db1735fc37585df0322392b14eece7220912680fdc957422bd00cca55fa2883 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 7ce6087f7d0c2a5c6dedac1ec0e8eac3ef2cdc0d4a5d6e2976226a767159dd79 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | f6391a9e4596e5b99363c348ee99cb1792b2817faf6a0d92439ccb5609778e88 |

## Remaining Blockers

- required_gate_failed:backend_pytest
- required_gate_failed:postgis_proof
- required_gate_failed:egress_proxy_proof
- required_gate_failed:auth_mutation_route_coverage
- required_gate_failed:mutation_fail_closed_coverage
- required_gate_failed:check_api_contracts
- required_gate_failed:map_route_check
- required_gate_failed:public_api_boundary

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
