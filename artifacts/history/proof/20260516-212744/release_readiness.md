# RELEASE_READINESS

- generated_at_utc: 2026-05-16T21:26:22.626127+00:00
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
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | 79438fa1da3a43ae65012d7fc2f9fbbf75e678c0486ec0e9eb52727d432a2892 |
| check_migrations | FAIL | 1 | artifacts/proof/current/check_migrations.log | 54be43380b7f89abd49343569455c7df6c197716bffc9acbf29e72a1156d908e |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | FAIL | 1 | artifacts/proof/current/postgis_proof.log | 8a1d3cfeed95be233ef4ba22bbe3a2bc326ca213d70579ac27b6029fee000321 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 0544b61e8f7f29d06fd9791311c0ed71ab539a19cd497e646f0927d4b67af803 |
| demo_proof | FAIL | 2 | artifacts/proof/current/demo_proof.log | 6a4b680a5425c16c63de588aac802c5d62df03ce23e90c63e2c26876b37dc409 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 5021562165d4dfaf864799884cd6e87f8f97ab93da5e21d6fb5c0dfba0876b2e |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | FAIL | 1 | artifacts/proof/current/prepare_proof_db.log | c39edd67eafbe6ca36f522357e0a157c20d805c620515d754fb2b2e63a6e0bb2 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 1179d0c8c1c56de20d4f917fd60915207780fa80305d5ffb0e8d31ff25adc9a1 |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 01ab2325e8e19ba0c1931aa6934d2f6222d47c828b058e1df0f21d98a6727a16 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | fa9cd0e25dcc1e230610463c80c04cc48c6c326debe3521403b94a8e7f25f4ae |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | a3743b2a379a4c611aab88f2dd4a717b1f18ae345d3b524353c6daddbbda95ef |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | d2f7d32baf0f1f29b1a8747f7979651012b9129abedc88173fb2b94d96e34cd3 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | ecd28d5ce2de2f64c5e78c8db49705f3c03eb097210beb4ba314e38e07175818 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | f22be5d40d7f70376f1085cfbce6102bad9d3133ec312701c0aabbb9ec0a7928 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 78ebbcc52598a48a739f08fbbc4ef958826f7b2d66cc8a5b365b473e71847020 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 8d32af7e6ae81285971fc29c48c9c9c136561740821a5ac076e2c359fdc77533 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | c57dee6f0110c9fb54e630d3361d7e67abeacbaef9aafc9aa5f4ab3f06120bc9 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 836f59db5bce0b7dfa9214237bec32d80bd6014b15de68a5fc967cb2e1b38cc8 |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | 28ce6890c2eccd21eb30eaa12bb2888c244cc0fb77acb65aeeedd6c2334705b3 |

## Remaining Blockers

- required_gate_failed:check_false_claims
- required_gate_failed:backend_pytest
- required_gate_failed:check_migrations
- required_gate_failed:postgis_proof
- required_gate_failed:demo_proof
- required_gate_failed:prepare_proof_db
- required_gate_failed:archive_validation
- node_major_mismatch:Expected Node 25.9.x, found Node v24.15.0
- archive_validation_not_pass

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
