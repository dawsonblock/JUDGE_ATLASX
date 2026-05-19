# RELEASE_READINESS

- generated_at_utc: 2026-05-19T23:11:35.458622+00:00
- overall_status: alpha-proof-pass
- production_ready: false
- release_recommendation: alpha-proof-pass
- archive_hash: 6cf8570cff222c932dfb960dca31837d3a9d1c0d
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- gate_runner_node_version: v20.20.2
- frontend_node_gate_version: v20.20.2
- node_version: v20.20.2
- npm_version: 10.8.2

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
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 648664d413c1f209b0e804515fd113e10fe92eccb691542decbf3dad4a0a1f3c |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 9004c058488b161dcf9bc606f6e99defe3ccfbf584f349addbd9f4c60059a420 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 7238907ef99a4386e2c9bfd731ebab7777461f430a9f48ea78e2531e466c37b0 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 5de9f42e579164c0074526118de5f3ef733c9479f2e60507bfdd06a27a32b8de |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 8427643f82dcc6f52d65345969bb35a777b4625fd7fd9c0e665e54f9d794cfcd |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 08f9c6765cbe47b6872e4fab14ba7a7e5349ef84290b673908b991106a50845c |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 68683c941f53fd55547c17b6a1b7a966702a2b51e89bd6832b00e772606b6b6e |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 4411b877d5771fc1e4342c11d5cada44ce93ed7b3a6de21693ca4dcc3342143b |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | c65abdafdc4e14592a41b48937df3c77e307a5ac6624b005cef249e4529d3670 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | e67063c8ecfca49a834d6eb51293c4d1ea43d42f781cdae5afe9b9c9ea253068 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | decd7955258a2035abb0f1c685beb251b55f3d60fd9009da5a75afca52c212a8 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | a24f4940adc7597eeb444006b65dfb80f5a5adcb7d2b69c4d6322b7d429d911f |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 791d0d5487f0f619434520b5a4aab710da103fc6b959224b0180fe081b8049dc |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 4dabce1243e4eac792a59853c427fcf187bdb8f164cf23fbb01fd78e69a2e111 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | eba750aa870fdf59fb62e3df0c29ee42c98462022ba769f15ef90b1616be024c |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 29a7bbf4ff9f5b09e0768f60bed58f5ba78a8a6cbd5c19a875fb4b11318041ce |

## Remaining Blockers

- none

## Stale Or Misreported Claims

- none

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
