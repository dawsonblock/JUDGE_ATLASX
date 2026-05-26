# RELEASE_READINESS

- generated_at_utc: 2026-05-26T20:25:25.616634+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: f22ed8f3a52ae673031ee0886dea92387564956c
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- node_version: v20.20.2
- npm_version: 10.8.2

## Required Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| check_no_pyc | PASS | 0 | artifacts/proof/current/check_no_pyc.log | a846f2e3cfab43e1b94af70247e6dff79ec62b983961a207185d87595b1b7ff6 |
| check_false_claims | PASS | 0 | artifacts/proof/current/check_false_claims.log | 8c882684eaade150d76d26e289c110f776b307c04d132c6aa33949aff87c7bc1 |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| check_dockerfile_copy_paths | PASS | 0 | artifacts/proof/current/check_dockerfile_copy_paths.log | 9cb5347afde90057ddc1a4fdcecd6ae1318290990ddadf2f5dfaeebf1e92eb2a |
| check_compose_auth_defaults | PASS | 0 | artifacts/proof/current/check_compose_auth_defaults.log | ce53c858a818dccbbd3685948e8ce1414dddb23714d77e259787b0ce79eceac9 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | ff048fbcb05f4b23e858a813501477214166d826b765b8ca1f6bba526c2b6e9c |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | b5409e2a52e4b96662c82b82dbf8e58fb1deb5387c82ca205874b9e5ceb612e4 |
| runtime_smoke | PASS | 0 | artifacts/proof/current/runtime_smoke.log | 561261d657b5b6b5bd99f9db4f716948b8a6188d16238c6259018c5ac421a7f3 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 78f2878f140ba391b613cb69097d5e57214466fdb2c13eb707d9a96c394573ad |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | FAIL | 1 | artifacts/proof/current/docker_runtime_preflight.log | 04a270ee30be9659917e4ad3b4dd3f6b7d0fc4bf4101788e46a803a622281046 |
| docker_smoke | BLOCKED | 1 | artifacts/proof/current/docker_smoke.log | c6593ad24f69d3c07a62c0aa26fba3a8e0b9cc02d0fde1d040db17258fd57c2c |
| postgis_proof | BLOCKED | 1 | artifacts/proof/current/postgis_proof.log | 161e3405df71182f2be5bc8d5b88e4558cb8779029700e68c4a76192e027b0c8 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | bd74d374ab5ba487ebc8648e683dc7aa0ee5c84ca583fa38e8c8d2efaee9e694 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 5de510ce42797df8e127acf38025711918f2b55854ecaf8f51d8c3d81e29026e |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 105df9202756cec134efb874bb81bf4dc284ebc9c0bb59461e1c55559f1a0323 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | a627028cae8dc77fd1985e05a14c9eb33197aebcd2791d1824866799fe8c86be |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 26cdea43192fd1aa37ad18acc300576164cbd2d9c37a252cef089d097e8d29a3 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 19e95f03931508bcb63d5f1f276741db94fd3f8f0399d2690ed306a73c3ba6c7 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | ffe2a4a341462d569b35e1e292ac1aa0fb4d5f4f8c0cc6d1855131d67100244c |
| check_node_policy | PASS | 0 | artifacts/proof/current/check_node_policy.log | 4ac278efce24b13829768ac56e4c61c8e3a44e6168b2e384eba7e5cf0de08681 |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 79c45e2f36695f8f728fccd4a155f367fe9dd7f76d137710ca4b5c8898dfbe45 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | b0e5086ba04618d003e44509199cbb6efd4e84d9a96e4290da4569f004d5443b |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 3e04dc15522f11a1f59137bcc907ec4f02f45d0bd6bb04d56c9fe10e3cf8c319 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 47aef45e83089014d566914acdaa079f5d71d7fd00cb88ef943bd86c97608dd7 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 1f136c767a6ec6bd6d527af249dd34271e19a2e1287eedd33fd8364bb9384137 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | c9bab79018cc60539b4fa5a6d6b6e291f3138327e6689b409cb60d8087b54092 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 4933e94c833a8e70359faff33aa488fba9a1a211d748d06f97e791ee85a9de9a |
| canlii_staging_proof | PASS | 0 | artifacts/proof/current/canlii_staging_proof.log | d7c9393bb589559678b644f26519944ef1a69f81a771fdbd5fce0282bb665ab5 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | a1d23945ef259b5aa4dafaa470459f2bdfdb222fea00c33064eec8ae14be72af |
| single_proof_authority | PASS | 0 | artifacts/proof/current/single_proof_authority.log | 67de9d9d555d8a633cccb3b3fd168f55f5975ed306de95965f06666949cc4337 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 0235daa16973b2b5ffe5aa1498c0fc21d21cb0ee94213549fce81211aec7a31e |
| proof_consistency_pytest | PASS | 0 | artifacts/proof/current/proof_consistency_pytest.log | dce821e26b65efde885da85ddc85e756e7332d437815e8f90fbe1933be0c87b8 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | bac6fa6edea8c106db4302e1934a7172331c9183bd9fcd3332c7b1a0398835a8 |
| required_proof_logs | PASS | 0 | artifacts/proof/current/required_proof_logs.log | 271becbf8942bdc9867c3fe07d72be2877c9315cf3bb8638a5ee98a5a676d68a |
| check_proof_manifest | PASS | 0 | artifacts/proof/current/check_proof_manifest.log | 02a5c925c7261eb8bd964a91c6442c19d3346172c9561eeed5476fc616df93d9 |
| check_proof_consistency | PASS | 0 | artifacts/proof/current/check_proof_consistency.log | 6e38050568d728730b225be05ff8f9d14db9401316b0ec49e4b1aba262369e13 |
| check_no_local_paths_in_release_proof | PASS | 0 | artifacts/proof/current/check_no_local_paths_in_release_proof.log | 7ab4d071c63ecc123622b94a78dda4a32381a788cc2f318f840fe2f9e799c8e4 |
| release_gate | PASS | 0 | artifacts/proof/current/release_gate.log | 1d95670d640c93e9b08e74656432e3b801887174fbbc5d742021d8e9e33148b7 |

## Optional Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| static_guards | PASS | 0 | artifacts/proof/current/static_guards.log | 115a68267999528d3cc712acd354f443bc0db2bd743118066bb8d8f59c01ce65 |

## Remaining Blockers

- required_gate_failed:docker_runtime_preflight
- required_gate_failed:docker_smoke
- required_gate_failed:postgis_proof
- docker_runtime_preflight
- docker_smoke
- postgis_proof

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
