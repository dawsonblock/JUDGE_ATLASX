# RELEASE_READINESS

- generated_at_utc: 2026-05-17T08:55:28.354160+00:00
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
| check_false_claims | PASS | 0 | artifacts/proof/current/check_false_claims.log | ef04562ae44d2a4e2489ef39646502a7b42c83f212cb7679c6ab98e035db955e |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | 90d607d6e74723b8807a06f5ae2f0d53c8da5049d6cfbb35d6f7beb95d307a05 |
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | a251c76fabbbcf352a97fbbdd66160c23d13d0819bfc862df8181d617d2e4ed0 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | a473cdc61d6b502afc353d713f0596f1c453db14633ed97dc6217e8adc819a3d |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 246b3ba88bfbee21846622942dfabba83a40212420e87b3b03fd0be67f1afd8e |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 67a564a860075fa28159bb2a61ddef2872d476620a00cabc0b7238eed6fdaee0 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 880797ab78071bebda41affb0efc5353721a144059f2b9c3d83c158a9de9eade |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 6247e9c2c22e07e4ff750860496d6141cec724e2c30f38fb46adf79b3261dafb |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | bfb94aa3bce5e5c9a8e413d4c0b8cbbecf5444cc553dd49310e15bc548c86a10 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | a3743b2a379a4c611aab88f2dd4a717b1f18ae345d3b524353c6daddbbda95ef |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | cf248cb9bdce2c50524b7b90b4e365dcb83e780b3f805d38d1924df0668cb7a5 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 7ad07003b1adf4017ba90f6afb3eaec45a9acc084a9ed0a8b92d8ec203750754 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | f22be5d40d7f70376f1085cfbce6102bad9d3133ec312701c0aabbb9ec0a7928 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 6cefc62f18ffb2e57b9a64cb51e299efdcc71600f09b187538d9a83b064ba233 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 64b44871b811c0e727d8523ff51338f68993293de5ff9ab1d34287e46ce3c281 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 5f9c22925db71c7d43f30bbdb10ca204726ce6a99a76d29314dfa1b0251eca54 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | da5acad76c3598dde4356584ba4f3cc8ed765edc6327bd5dc3960df1a2ffa30b |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 4b0ff4c71af188e28701fe71ce0e0203a89ff451053f1f0d209daf40564022ed |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | ff60ad5d60319b6976b2a01b5a3cb650514498a0c64fd407468bc262cd6bd107 |

## Remaining Blockers

- required_gate_failed:backend_pytest

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
