# RELEASE_READINESS

- generated_at_utc: 2026-05-26T06:50:46.546565+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 0c8e0e5eb4705bc5e0144859e0154f9e4f8ae17a
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
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 18c6c3bd6dbeae56be3fd21a8c1ce8d43790392c499ed7a8f34396af6fb1c8f5 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | FAIL | 1 | artifacts/proof/current/docker_runtime_preflight.log | 281c9ac27f157a2a3dab85290471aacfc284373bb0f2541708d3f4f65445ac94 |
| docker_smoke | FAIL | 1 | artifacts/proof/current/docker_smoke.log | 6d2beac9921add811d164c694a212eb05da3515426ed1fed167d816fd3f81dd0 |
| postgis_proof | BLOCKED | 1 | artifacts/proof/current/postgis_proof.log | 20d252c24174576e18993ddeed557e9eb469ec52d0a574aff6c0f1a26edac3b1 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 3b2c9c3be1521f0ca06efcfe988546df90bfb034b79c967f0fd091bb7c389f3d |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 5de510ce42797df8e127acf38025711918f2b55854ecaf8f51d8c3d81e29026e |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | f800872165cfdb4fdcd278a3c6b3d7b6ffb4a7673d7e26fef70cb7ae10066dfc |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | a627028cae8dc77fd1985e05a14c9eb33197aebcd2791d1824866799fe8c86be |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | aaa7b6ea086edd383ee4f93e6838a42af84fafeb55137319f95026f090146cf3 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | f4c61c0ac8f55c6c9a2d6c593731bf5f8c4a6c5bebbe514284fd4f899818f9e0 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | ffe2a4a341462d569b35e1e292ac1aa0fb4d5f4f8c0cc6d1855131d67100244c |
| check_node_policy | FAIL | 1 | artifacts/proof/current/check_node_policy.log | 3e512d05b34f0df76fd2a6c3f4243ad316a6b93cb99f649770bae202f63039f1 |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 79c45e2f36695f8f728fccd4a155f367fe9dd7f76d137710ca4b5c8898dfbe45 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | e8835a9bddda60d5b78555664bbc7c5b8a8abe387e2182b8c58f07a07146085f |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 5aa7d6acb789a468f0e175055d35f909642533472cb2fd2862efaa4803ac0aba |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 47aef45e83089014d566914acdaa079f5d71d7fd00cb88ef943bd86c97608dd7 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 1f136c767a6ec6bd6d527af249dd34271e19a2e1287eedd33fd8364bb9384137 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | c9bab79018cc60539b4fa5a6d6b6e291f3138327e6689b409cb60d8087b54092 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | e76eabfb437e199a4a8e3b93e697cd304876daba195da0af999bc7506b7db325 |
| canlii_staging_proof | PASS | 0 | artifacts/proof/current/canlii_staging_proof.log | d7c9393bb589559678b644f26519944ef1a69f81a771fdbd5fce0282bb665ab5 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 9cb7432d5a0a117f92bd971e36b1462bfa9386c378fbbefd54050336f4dd5974 |
| single_proof_authority | PASS | 0 | artifacts/proof/current/single_proof_authority.log | 67de9d9d555d8a633cccb3b3fd168f55f5975ed306de95965f06666949cc4337 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 42f6b681cf72304f282c1dd292199d052e2d0fc9cf7a60a9ded42d4a891fbf5c |
| proof_consistency_pytest | PASS | 0 | artifacts/proof/current/proof_consistency_pytest.log | b6c7ffc9d80c78da811cf4c0f8da9b1721c6b323b8ab236716f7a65a8887a1ff |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | 0beeb4c197cad3cbc7a6925b59b327d8a23e53a34e6a3bb92816283275754e79 |
| required_proof_logs | PASS | 0 | artifacts/proof/current/required_proof_logs.log | 271becbf8942bdc9867c3fe07d72be2877c9315cf3bb8638a5ee98a5a676d68a |
| check_proof_manifest | PASS | 0 | artifacts/proof/current/check_proof_manifest.log | 02a5c925c7261eb8bd964a91c6442c19d3346172c9561eeed5476fc616df93d9 |
| check_no_local_paths_in_release_proof | PASS | 0 | artifacts/proof/current/check_no_local_paths_in_release_proof.log | 7ab4d071c63ecc123622b94a78dda4a32381a788cc2f318f840fe2f9e799c8e4 |
| release_gate | PASS | 0 | artifacts/proof/current/release_gate.log | c313634cc26bb873d17c7e4e37106c8166c32b77f0d0f75e733c3d07cd99ad1d |

## Optional Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| static_guards | PASS | 0 | artifacts/proof/current/static_guards.log | 115a68267999528d3cc712acd354f443bc0db2bd743118066bb8d8f59c01ce65 |

## Remaining Blockers

- required_gate_failed:docker_runtime_preflight
- required_gate_failed:docker_smoke
- required_gate_failed:postgis_proof
- required_gate_failed:check_node_policy
- required_gate_failed:archive_validation
- archive_validation_not_pass
- docker_runtime_preflight
- docker_smoke
- postgis_proof
- check_node_policy
- archive_validation

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
