# RELEASE_READINESS

- generated_at_utc: 2026-05-16T21:29:19.368787+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 505a93ea012837a27127931590a7a12820366133
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- node_version: v24.15.0
- npm_version: 11.12.1

## Required Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| check_no_pyc | PASS | 0 | artifacts/proof/current/check_no_pyc.log | a846f2e3cfab43e1b94af70247e6dff79ec62b983961a207185d87595b1b7ff6 |
| check_false_claims | FAIL | 1 | artifacts/proof/current/check_false_claims.log | 4b8b482333948d6c4789e3011704e0077d7dbc27e63f6230fa324d720718a2e3 |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | f722c82c7def9e790c1676a4e1bdb4c064370a48071b37d54cf00c26ca8efd47 |
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | c87870d5ac697a97fc7a36eaad714c04c2981fbf269ea41d5d31268d6201e10e |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 3c268dea191fad6151faa98090596b2db7df7b61382317442f4fe9d86ba454ed |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 4c902b4991741758682a4adf915346b3809a6328ab83b50b534f358606c8665a |
| demo_proof | FAIL | 2 | artifacts/proof/current/demo_proof.log | 6a4b680a5425c16c63de588aac802c5d62df03ce23e90c63e2c26876b37dc409 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 651eed225540ba3735fb31d50f3ff6f6bb5455e1d99710161df1aed0f2454d9f |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | FAIL | 1 | artifacts/proof/current/prepare_proof_db.log | 6298428fd9065fa04ae600af905e9c1d4234c323d8035bf40a99a4fd80436d31 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 1179d0c8c1c56de20d4f917fd60915207780fa80305d5ffb0e8d31ff25adc9a1 |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 01ab2325e8e19ba0c1931aa6934d2f6222d47c828b058e1df0f21d98a6727a16 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | bfb94aa3bce5e5c9a8e413d4c0b8cbbecf5444cc553dd49310e15bc548c86a10 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | a3743b2a379a4c611aab88f2dd4a717b1f18ae345d3b524353c6daddbbda95ef |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 2669558a9088987cfe5c205eefcba1bbcc673363d1928d4184479c101a613d72 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 39f3d22b9b7acdadf79047019330aedb97aef08f04c28795974fe213a1a2ab5c |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | f22be5d40d7f70376f1085cfbce6102bad9d3133ec312701c0aabbb9ec0a7928 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 78ebbcc52598a48a739f08fbbc4ef958826f7b2d66cc8a5b365b473e71847020 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 209307e872259f535750b98e14d022c9c00835928ab0303a56d537d77146362b |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 48c15c983a9ab4731ec1a7b10233d0ca5424eeec356ae683cfaf8df9af846fd1 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 4d0af0659edb985714a0403751d6fe0a56cfc4def762b295694915a9c9f75dd3 |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | 57481e1e80e02669c30ed92ac96a4584af9767c20668fa19ae6c94b69f683db0 |

## Remaining Blockers

- required_gate_failed:check_false_claims
- required_gate_failed:backend_pytest
- required_gate_failed:demo_proof
- required_gate_failed:prepare_proof_db
- required_gate_failed:archive_validation
- node_major_mismatch:Expected Node 25.9.x, found Node v24.15.0
- archive_validation_not_pass

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
