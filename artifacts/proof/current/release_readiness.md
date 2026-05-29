# RELEASE_READINESS

- generated_at_utc: 2026-05-29T06:24:13.647838+00:00
- overall_status: alpha-proof-pass
- production_ready: false
- release_recommendation: alpha-proof-pass
- archive_hash: 14f8b7157d8d78ab0c84dd8e518ef4eca0e8478c
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
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | ef52f5f83bdd965c041c65e22c0119895113e37a9faf0f73842e4ad73fbec2db |
| backend_pytest_collect | PASS | 0 | artifacts/proof/current/backend_pytest_collect.log | 90e230f96a720c71a3186bdb55c092fb26ef3570b379b6042212eeb10b3edd18 |
| runtime_smoke | PASS | 0 | artifacts/proof/current/runtime_smoke.log | 561261d657b5b6b5bd99f9db4f716948b8a6188d16238c6259018c5ac421a7f3 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | d7c4c51dc1cb9dfc47677164295547643e91f030eac589bc07c098815cb27ef1 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 7db7b3b659a452708b9b7176ec71a4f0a235afbdccd76e5e53e9d883cfefdbbb |
| docker_smoke | PASS | 0 | artifacts/proof/current/docker_smoke.log | e4eb71116a5b4062e0c34c4bc78640398a7e08dfb76d4cce084487f1f9050ae0 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 0021540f0678c48f5c95499ab4d17d33634ab9851379bbf30d2a09f18dee3f2c |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 7022309231d9caad67f16d28c4627a35d5780c9c370608a55c987e8f9be315f4 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 5de510ce42797df8e127acf38025711918f2b55854ecaf8f51d8c3d81e29026e |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | d8eb48a84502174ba8d54f7d491815954bfd32c488bd4643046193309c3a6cde |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | a627028cae8dc77fd1985e05a14c9eb33197aebcd2791d1824866799fe8c86be |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 9de5b3b335fc86ba5393a6057ea00e0b8f311572434e1ed1e17f4df721c0fa25 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 8543a95c5b7f774db5d80c98a970296c482c13e608e7b0e2550f53f5d98aa989 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | d14f61a853f5d4f2b49932e04bc819a452c3d94029788fe69c2a6cdeb8ed377b |
| check_node_policy | PASS | 0 | artifacts/proof/current/check_node_policy.log | 7e85e2b7b48ea296e185ce24b37be147a91c5b0724af8f687c91aa19d5856fce |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 79c45e2f36695f8f728fccd4a155f367fe9dd7f76d137710ca4b5c8898dfbe45 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 20717c08bc4364d15080d2e825583ccb47fd229190e80dcb7642c193fb41af48 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 62f2619394ef3ce0bba725a155b89e41043ecc98ef7974bf814616cce3f2000b |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 39798d23c4446d3d60b08cb30d3115a9baeeeded0f0434dddee9a487463644b0 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| frontend_backend_route_contract | PASS | 0 | artifacts/proof/current/frontend_backend_route_contract.log | f3563209ec0dcbcbf599836f73236926eee160235914e0fe0e660e945c9042a0 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 1f136c767a6ec6bd6d527af249dd34271e19a2e1287eedd33fd8364bb9384137 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | c9bab79018cc60539b4fa5a6d6b6e291f3138327e6689b409cb60d8087b54092 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 4121f6f5e97b12082952b343c85b467e0fd313865272a16fdeb86b5fb0735b82 |
| canlii_staging_proof | PASS | 0 | artifacts/proof/current/canlii_staging_proof.log | d7c9393bb589559678b644f26519944ef1a69f81a771fdbd5fce0282bb665ab5 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 887701a9e3be9d4bdbb6c1cb6413b984a9bc5654b660f0017ae60a08b5bbe840 |
| single_proof_authority | PASS | 0 | artifacts/proof/current/single_proof_authority.log | 67de9d9d555d8a633cccb3b3fd168f55f5975ed306de95965f06666949cc4337 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | c6c445cfaa69949d25ab8fc4f24155fce51dbccbc290fc8171084663673f53f8 |
| proof_consistency_pytest | PASS | 0 | artifacts/proof/current/proof_consistency_pytest.log | e229541b306ca52d9ecce9c536c76cbe3da08c272aa8fdd2458d6f31a93e9481 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 385ee27208b9feb4f00ce23d77b6e09e432b9914fcdedf0f58dcc3f7c73ae07e |
| required_proof_logs | PASS | 0 | artifacts/proof/current/required_proof_logs.log | 545cb58a6f811600a22cd2843d2f16bca426298564052ebf72e65c4c158e82f3 |
| check_proof_manifest | PASS | 0 | artifacts/proof/current/check_proof_manifest.log | 02a5c925c7261eb8bd964a91c6442c19d3346172c9561eeed5476fc616df93d9 |
| check_no_local_paths_in_release_proof | PASS | 0 | artifacts/proof/current/check_no_local_paths_in_release_proof.log | 7ab4d071c63ecc123622b94a78dda4a32381a788cc2f318f840fe2f9e799c8e4 |
| check_proof_consistency | PASS | 0 | artifacts/proof/current/check_proof_consistency.log | 0a6ed516987c56172c896b5e5e4bae178cd6f9a2b53df2aa17bb118215f63a28 |
| release_gate | PASS | 0 | artifacts/proof/current/release_gate.log | 3d43a45c122a1fbddf9b8d3b558181669531d59c5081a32a7e79a47c22ff8f5b |

## Optional Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| static_guards | PASS | 0 | artifacts/proof/current/static_guards.log | 115a68267999528d3cc712acd354f443bc0db2bd743118066bb8d8f59c01ce65 |

## Remaining Blockers

- none

## Stale Or Misreported Claims

- none

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
