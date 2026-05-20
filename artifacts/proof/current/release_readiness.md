# RELEASE_READINESS

- generated_at_utc: 2026-05-20T10:42:54.773018+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: ba0b4c2b4f36f1761dff435c057666542dc31d77
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- gate_runner_node_version: v24.15.0
- frontend_node_gate_version: v20.20.2
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
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | 90ddbb4888a287c15ade23457303b0061ef54e01071bc4ed73ed0bed182ddb26 |
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | e4eae532a8ce6902e5b3bcf5b0c8934bd13193b833cccaab95ce1ca74873e449 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 9004c058488b161dcf9bc606f6e99defe3ccfbf584f349addbd9f4c60059a420 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 188822e8296ed18c35f93951d900297d70c40b83f4f202c4251df7af0fe84236 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | af2677b39a0b5a5fb61a417576ab1e52286fa14675175559d4c2b678b66a44f7 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 55fb1635e826dce58385e8c42e2694146895631e5cb64b4fd600ca1ceae74797 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 48a62072776480675e3ae339c5bb23b5a9f5e4cef790323cae6dc366027444e4 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 7f3afd65e2424264c6f748dccc29ad4ec50d8dbbec2719e1051e48c4ad3e7506 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | bfb94aa3bce5e5c9a8e413d4c0b8cbbecf5444cc553dd49310e15bc548c86a10 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 566b533769efda184c621fadcbb3499a3de7b732897627c27b430e8565082bbb |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 1aaabeefd07a61f2e5f39241277580ddbe158ff27c88271f2732e612208ffa33 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 2b3471d2baa6049c495aa7ebe7d2c2bd074e9db5e99aec85a274585a57b70ff6 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 4b456243d33d4f4a102ebe4d6785acf6f50894b664c463346cc21b84a4f9d4cd |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 491ef36b6f7a47ad3299d4f06dc79c579130dbc3defb3ae793f43ab99305d6b1 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | ffe3d57b75f92ff3887eb80e401fd1227db312dc02abe794b9fc341e4e7beadb |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | fb33afc4323d656fe8536c4b9d7df51c7f8a5e736e4cf24c3bfc98858ec6407f |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | af0c9307bf1a73a9c0358ea4c5b10b753a55d63655c0d2afc3ee008aa3172c93 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 3031fe756bf538b2f33c91c72bd2c59ce470b07883002928d5d7fbe30118f7dc |

## Remaining Blockers

- missing_required_gate:archive_validation
- required_gate_failed:backend_pytest
- archive_validation_missing

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
