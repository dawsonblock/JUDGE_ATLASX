# RELEASE_READINESS

- generated_at_utc: 2026-05-15T07:24:58.369721+00:00
- overall_status: alpha-proof-pass
- production_ready: false
- release_recommendation: alpha-proof-pass
- archive_hash: 58f055d0bb56c4d69ebd6407ca6ad950b843b27f
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.14
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
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | b37c6dbf65566cc27820af5fe0de5997781559cea4b5e5a4219696855d2a89cf |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 23521d059c25b190b258a8ce55e430d97a1e103a8a7052c615187bffade3e5e2 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 02f7283ab6012eea4ed77e72de82d52e17a495e6d6eec4bdab67f07ee30bc5d4 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 34671b89396aa0f94852d60ff8e1c9ffa48b0e496f8205515a314b82e0ee727a |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 4555f74b23c5bbb85c0bff9b48ddfb4f76b924a307278348ff7464be6dc2816a |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | c45f3e197b1df8faf71ccfbb1cde8c83793ad0dd4e06faf8cf10bfe1493c3c73 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 6b07e5915f4e6c031cf04d6627800931c0fdc181f715e7032ccc5c9ff1f27b7b |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 6eb2369c4ce1c57d717ce60a109bd899f8230944bea29cd4f25361ae73d32153 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 90ead549d8e087042fd7a931db311382b329952554f73320504d9cdaec129e77 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | cdeee948673c188b83cb55b2384f978a44b292966bec02199d1271a03c941e7e |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 1aaabeefd07a61f2e5f39241277580ddbe158ff27c88271f2732e612208ffa33 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 7776e0dccb191ea8b622dd2cf437dfc9bb06749d3a4797a38cbb3c939d12d639 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 8cff4f691005e593c0470c2e3ddab9972bac301c4c982337a6114cd53e50ee28 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 4a3e6bc6a694ee17ded4f80a5c86a9e5e2f3a44f404c11e2bedbb25ab7a8d277 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 78ebbcc52598a48a739f08fbbc4ef958826f7b2d66cc8a5b365b473e71847020 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 0e80afc9bb82b4b8f0816b210c78499c88a92d59ea5305bf46bd4ac83a858420 |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 9d28148ff84484db6a8cdb544789e3ab2818fbfdb217575dbf65f6264e552a93 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 94eb2e330553d9bf8ec24a3669c6e32ee288fa0266ef0f7067ed0b117c89572e |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 6d8afe9c3d455f5441ac2735f40011f440525e5e95959106e6409460dfdde3a8 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | caf51c7f9ac952b909f0f506291b4e422e68ca938fc0e0c48fcba67cded1d02c |

## Remaining Blockers

- none

## Stale Or Misreported Claims

- none

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
