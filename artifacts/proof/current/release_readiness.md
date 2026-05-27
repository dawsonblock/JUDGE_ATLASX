# RELEASE_READINESS

- generated_at_utc: 2026-05-27T20:35:42.165058+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 06663bce861b92ec736fdebaadef7f86543baef5
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
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| check_dockerfile_copy_paths | PASS | 0 | artifacts/proof/current/check_dockerfile_copy_paths.log | 9cb5347afde90057ddc1a4fdcecd6ae1318290990ddadf2f5dfaeebf1e92eb2a |
| check_compose_auth_defaults | PASS | 0 | artifacts/proof/current/check_compose_auth_defaults.log | ce53c858a818dccbbd3685948e8ce1414dddb23714d77e259787b0ce79eceac9 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | ff048fbcb05f4b23e858a813501477214166d826b765b8ca1f6bba526c2b6e9c |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | 50af42294a061f60ac0dc3ddaa223b8f002e7cc4e4db7e5700192437b361facf |
| runtime_smoke | PASS | 0 | artifacts/proof/current/runtime_smoke.log | 561261d657b5b6b5bd99f9db4f716948b8a6188d16238c6259018c5ac421a7f3 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 805c580290f378348f1d13b2e9abb1221c71bc3e6ce8df7276068e40a8f32b2c |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | eab66fc4cb32d397c132fa9b200d20fecec69d2d8bca45891643a55d545383dd |
| docker_smoke | PASS | 0 | artifacts/proof/current/docker_smoke.log | 1279c68c632b3b71f35eec4becdb1cd457a37c3d960c159da308b681f473dcd2 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | cc24b86764eb82de46ad7bf992e24133a9424034edc13409460f2b05c38388c7 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | d26aa4e137784d6b17c5562bb9259474e6670d54b83e585781f3f94cfdbf69ed |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 5de510ce42797df8e127acf38025711918f2b55854ecaf8f51d8c3d81e29026e |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 67ac2c17616f1a62d9feb83d9fa9cc2da7fc9c66d468d48c3c493820037b917b |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | a627028cae8dc77fd1985e05a14c9eb33197aebcd2791d1824866799fe8c86be |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 83b6450d25662f9889ebd0ae74b02b98bbd16accf76a455184356c8922213c6b |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 19e95f03931508bcb63d5f1f276741db94fd3f8f0399d2690ed306a73c3ba6c7 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | d07a1be384f84d9d95b6d48bfc797264bdf209a84dca560c1775e944c8887ef5 |
| check_node_policy | PASS | 0 | artifacts/proof/current/check_node_policy.log | 4ac278efce24b13829768ac56e4c61c8e3a44e6168b2e384eba7e5cf0de08681 |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 79c45e2f36695f8f728fccd4a155f367fe9dd7f76d137710ca4b5c8898dfbe45 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | a289c645439e95fb6b676eb6d97d3f197ff737ebaf56b3a66bef1ef8ea52732b |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | c7a57e39f6ec74fa291a276eda6a631ac47499a5f34bf39f92bcd2a7d5f15bcd |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 01535818f0ff51d4029a4775616cd4189dcd24ea8e243799006c0b57f340d609 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| frontend_backend_route_contract | PASS | 0 | artifacts/proof/current/frontend_backend_route_contract.log | 0e8bab2771567bd799f27d1f1fe85abce2f828f3458cdc8bd1aeca100d8008ab |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 1f136c767a6ec6bd6d527af249dd34271e19a2e1287eedd33fd8364bb9384137 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | c9bab79018cc60539b4fa5a6d6b6e291f3138327e6689b409cb60d8087b54092 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 09a097be7424f54ef3b2ac124e66898292418d21711aa8aca3a772d0417592d5 |
| canlii_staging_proof | PASS | 0 | artifacts/proof/current/canlii_staging_proof.log | d7c9393bb589559678b644f26519944ef1a69f81a771fdbd5fce0282bb665ab5 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 5b1d1f8c12a471f8018aff3ac450b05d3bc90fa7e827014d6a499d69f392bcf9 |
| single_proof_authority | PASS | 0 | artifacts/proof/current/single_proof_authority.log | 67de9d9d555d8a633cccb3b3fd168f55f5975ed306de95965f06666949cc4337 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | fc0313f4d8e22e9451038a90d2896ac771889e558a2227534a500ba2cd657b5b |
| release_gate | PASS | 0 | artifacts/proof/current/release_gate.log | 0ce729567578d6518a605bef41730774ab089183acd3af9cf8101768073daaf9 |
| proof_consistency_pytest | FAIL | 1 | artifacts/proof/current/proof_consistency_pytest.log | missing |

## Optional Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| static_guards | PASS | 0 | artifacts/proof/current/static_guards.log | 115a68267999528d3cc712acd354f443bc0db2bd743118066bb8d8f59c01ce65 |

## Remaining Blockers

- archive_validation
- check_proof_consistency
- check_proof_manifest
- required_proof_logs

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
