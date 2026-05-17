# RELEASE_READINESS

- generated_at_utc: 2026-05-17T22:54:49.369841+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 4552125671867e5ca006a46c611b43abaa575a8c
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
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | 90d607d6e74723b8807a06f5ae2f0d53c8da5049d6cfbb35d6f7beb95d307a05 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 7c75369b5f5fb1737b99fcee2aea0bead31487b1420c3019c960232cf9b91176 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 6938fe01995a02dbdb212dd25163677eac3740b7662b247934342530990595df |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 161e5da63e0ca6eefe0b6ce16961c83275ec2a900bcbcc6de8f9cfb477b9edda |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 633f8a6de0dee509dd7f719ffb24f8f381d3df658e8423b9902491b4c8dccf4b |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 880797ab78071bebda41affb0efc5353721a144059f2b9c3d83c158a9de9eade |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 044de313ea17e96551bd258b9ee5adc8f01899546418c9f30e6c1e921ede2848 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | e8b12eb9c14e20ba6d6f42d6a6564099a0106363b2d2c716df325fb3a6e8b6f6 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 2207aede3effc76057a2a3e57150b95838d002e9383df950aadd0fec45f590e8 |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 2669558a9088987cfe5c205eefcba1bbcc673363d1928d4184479c101a613d72 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | b4c5b5d48138d54e409a66e0e6a3f46bf79667be44ab3aed96ac85124771eab4 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | a24f4940adc7597eeb444006b65dfb80f5a5adcb7d2b69c4d6322b7d429d911f |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 6cefc62f18ffb2e57b9a64cb51e299efdcc71600f09b187538d9a83b064ba233 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 4da6afd155a16ecec95e3fc15909c120121302341ad3c037427a526273e53c63 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | d72d0f072498df436d98616d91e37d3596f77da870908df8bf77f6292853ecb2 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | ff44b9b99a347c90d2e309b72c86c24d83cf0c775e6a6230ae1a75548b2d864f |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 54cc66207a9e7e2768505377cfb68d383ec7e877f1b2162c20d239f489a50c80 |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | 687efd0f37113ede97ec323b170e36564a74a0f4ea1d04bf86a5563697e84cb6 |

## Remaining Blockers

- required_gate_failed:archive_validation
- archive_validation_not_pass

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
