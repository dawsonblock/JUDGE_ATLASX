# RELEASE_READINESS

- generated_at_utc: 2026-05-17T08:38:05.420400+00:00
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
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | 5382271390c1bf666348ee08321697df7b5c4e9593305002170e8e2ad72ee7a2 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 7ef2084df91ba3468a82aeb9a911db5b9a493532b7c5ae628c5d5e1a702b35ca |
| egress_proxy_proof | FAIL | 1 | artifacts/proof/current/egress_proxy_proof.log | 6342f776f28699951317dba2b92768cb5a6e791e2330a0cee82326f34b700945 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 217db5cd4a41fcdd193eea652583851650ce7932cd63ecfc90203dfc4f9a3917 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 880797ab78071bebda41affb0efc5353721a144059f2b9c3d83c158a9de9eade |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 0135fa6acac9c43874685141d47e36bb82139557cc0579533326473467355e59 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | fa9cd0e25dcc1e230610463c80c04cc48c6c326debe3521403b94a8e7f25f4ae |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | a3743b2a379a4c611aab88f2dd4a717b1f18ae345d3b524353c6daddbbda95ef |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 7776e0dccb191ea8b622dd2cf437dfc9bb06749d3a4797a38cbb3c939d12d639 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 3e76acef2875704e9b29beb1f6cc42c0287fe5c4a04d94ff4dbf7e679cece981 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | f22be5d40d7f70376f1085cfbce6102bad9d3133ec312701c0aabbb9ec0a7928 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 6cefc62f18ffb2e57b9a64cb51e299efdcc71600f09b187538d9a83b064ba233 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 64b44871b811c0e727d8523ff51338f68993293de5ff9ab1d34287e46ce3c281 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 59d77d2deb8bcca5413a4b4740a1c9329837b599c707b7af2b131a263c7dbb6e |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | c1f08d44dd21439214b1ef228e02f33c69f528a43601d9762fb3645bb89c87a3 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | a0fa84258b609cecf2d7edf91c68aeadb881ed8f8632b03d34803fb399b16bbc |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | c208b8687dafc9db462fee9a94d52785327ebb933e1a165771990fa62cf525fd |

## Remaining Blockers

- required_gate_failed:backend_pytest
- required_gate_failed:egress_proxy_proof

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
