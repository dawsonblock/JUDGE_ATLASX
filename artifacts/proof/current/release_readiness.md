# RELEASE_READINESS

- generated_at_utc: 2026-05-17T02:57:47.424592+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: d6a10e1657c723bf114c1e5984ea942ac893d51c
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
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | e14eb3a9186260a2e697a109f6e4699f0aec7baf9a96f9a4a8fadb3eb1b0dbe6 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 03f5085c020f71e0eb467aeee9670c957c6fa3009a9b745f4cd3f8775f887e7b |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 3c838f49a341458212b867bf286f3fcbd936be8ee6101135094781ef9a8d5f7a |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 9fc853b3f4935a705d1c30227cafdaf4599dd129d3219635eb54435e49a3849d |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 7071ab64d833b56839db5fe0b669bbcfbc0284d8acffaf7fc3395c5431e530cf |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | fa9cd0e25dcc1e230610463c80c04cc48c6c326debe3521403b94a8e7f25f4ae |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | a3743b2a379a4c611aab88f2dd4a717b1f18ae345d3b524353c6daddbbda95ef |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | d2f7d32baf0f1f29b1a8747f7979651012b9129abedc88173fb2b94d96e34cd3 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | c3e1727e26a6a9cd7cefb0fcec86e7f2ceaeec1fe8b918ec75756b46e890e23a |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | f22be5d40d7f70376f1085cfbce6102bad9d3133ec312701c0aabbb9ec0a7928 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 64b44871b811c0e727d8523ff51338f68993293de5ff9ab1d34287e46ce3c281 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | c2ce93a35e13cae61c124c36f881a4b3372084d5ec19edfc7ae8f112957d970d |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 05cffb72573faa2ad6eb2994f189b38f844792d231dfdc44f7e6ac0284744311 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 44b57872f8ae8fc1d3cd56658b535962902d56a000657cb34a753d0e827952f2 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 90f1addc86e015d9a89530638382dee9b5d4f766fecd691496070757592a0b0f |

## Remaining Blockers

- node_major_mismatch:Expected Node 25.9.x, found Node v24.15.0

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
