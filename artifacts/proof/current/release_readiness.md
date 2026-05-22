# RELEASE_READINESS

- generated_at_utc: 2026-05-22T21:55:46.841046+00:00
- overall_status: alpha-proof-pass
- production_ready: false
- release_recommendation: alpha-proof-pass
- archive_hash: 515cdc3e1f867488f970628cf7b65af81f8d8d26
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
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | b5409e2a52e4b96662c82b82dbf8e58fb1deb5387c82ca205874b9e5ceb612e4 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | d8dc4f85c6a05cfca79b5ad181c38162b6830a88d4308bdfebfcb247c36e3cff |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 74fe61ae7e9b822ada6f5d696087ca103c44974c6d97481bd78c93940ddd1dda |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | f98359baee6afedf0dfb653c4dce92f55ebde8ee70bf99835a20436529353dd6 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 1e5779ad3cbfcb3e9b2dc7ff1327a97b30f93f452bcb7723117c3e45f683e87f |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | d4daf93a4255ba5763f141482a36011e9135c5bd214c08d9d6f7d90c5d8d6b29 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 60b65f2b4cfa01105cffcfb68278c9526b93d326e69cdd55114ddb13927d788a |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | a627028cae8dc77fd1985e05a14c9eb33197aebcd2791d1824866799fe8c86be |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 53bf154d8cb5fabe5ac63641f8e37da11df4ffd3b06bf5dbf08660560c8014bd |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 19e95f03931508bcb63d5f1f276741db94fd3f8f0399d2690ed306a73c3ba6c7 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | ffe2a4a341462d569b35e1e292ac1aa0fb4d5f4f8c0cc6d1855131d67100244c |
| check_node_policy | PASS | 0 | artifacts/proof/current/check_node_policy.log | 03219df2980f8d1bba4f607711fcb2df939804f35166a58f21ce085c296a589c |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 79c45e2f36695f8f728fccd4a155f367fe9dd7f76d137710ca4b5c8898dfbe45 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | a289c645439e95fb6b676eb6d97d3f197ff737ebaf56b3a66bef1ef8ea52732b |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 47873822fe2bb7dcf658a1aecbe521232ba1202510d21d3c958b4598014cd947 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 47aef45e83089014d566914acdaa079f5d71d7fd00cb88ef943bd86c97608dd7 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 1f136c767a6ec6bd6d527af249dd34271e19a2e1287eedd33fd8364bb9384137 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 2e16b5b8dae42c782612d0d00569294cb699e8e37531b669ae661b73c49b8f27 |
| canlii_staging_proof | PASS | 0 | artifacts/proof/current/canlii_staging_proof.log | d7c9393bb589559678b644f26519944ef1a69f81a771fdbd5fce0282bb665ab5 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | ca470e04660b7bcd29158c8cd48f9105c105ac8978807c74149bdd67fb4a9d71 |
| single_proof_authority | PASS | 0 | artifacts/proof/current/single_proof_authority.log | 67de9d9d555d8a633cccb3b3fd168f55f5975ed306de95965f06666949cc4337 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 114b7d571873e359dd50c413d7a7a67dd39929d9285228ff70ba98a1654d4549 |
| proof_consistency_pytest | PASS | 0 | artifacts/proof/current/proof_consistency_pytest.log | b6c7ffc9d80c78da811cf4c0f8da9b1721c6b323b8ab236716f7a65a8887a1ff |
| required_proof_logs | PASS | 0 | artifacts/proof/current/required_proof_logs.log | 62d8c2876e715bc853e01dc1a07e7c8216b908ebee94b18b8fa27935bb0d58de |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 5ce5a8fd561ac6f6ac04fe836033181543647718b3eeac4cd5cdda1101a39ddd |
| check_no_local_paths_in_release_proof | PASS | 0 | artifacts/proof/current/check_no_local_paths_in_release_proof.log | 7ab4d071c63ecc123622b94a78dda4a32381a788cc2f318f840fe2f9e799c8e4 |

## Remaining Blockers

- none

## Stale Or Misreported Claims

- none

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
