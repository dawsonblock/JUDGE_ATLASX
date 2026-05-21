# RELEASE_READINESS

- generated_at_utc: 2026-05-21T21:25:48.042970+00:00
- overall_status: alpha-proof-pass
- production_ready: false
- release_recommendation: alpha-proof-pass
- archive_hash: 9770cd702bd85ed7d02cb8968a23c2ffd9fdde09
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
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
| check_dockerfile_copy_paths | PASS | 0 | artifacts/proof/current/check_dockerfile_copy_paths.log | 9cb5347afde90057ddc1a4fdcecd6ae1318290990ddadf2f5dfaeebf1e92eb2a |
| check_compose_auth_defaults | PASS | 0 | artifacts/proof/current/check_compose_auth_defaults.log | ce53c858a818dccbbd3685948e8ce1414dddb23714d77e259787b0ce79eceac9 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | f722c82c7def9e790c1676a4e1bdb4c064370a48071b37d54cf00c26ca8efd47 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | b0761b01ced8c414c99e0802338dfaecf75bf8ea82a34c6d09551fe652b15331 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | a8a8d0b3f6a52f8df83420d348d302e98d78d80ed63f2967436e105f2d2d9024 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | db9c5b574c12645c0ac522c489442dfcabca6439dc8739e27e0a479dea69e842 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | aefb82fb561d75ae6773386388de6a7c6e7fd11aeb4acf9adb19d12f2ca2bcaf |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 55fb1635e826dce58385e8c42e2694146895631e5cb64b4fd600ca1ceae74797 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | efc185c12e6a2c70cf02813f77ee19d4d484c0e15fc22acb6685be54c8539405 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | c67480f47c8c84d86f2ba450902ace6b26225427ce1a47469fba58c37925e3a6 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 19e95f03931508bcb63d5f1f276741db94fd3f8f0399d2690ed306a73c3ba6c7 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | ce22630fc7c34a988df630b4a92fb58d299903bc888dd68e961f12bfa2af1024 |
| check_node_policy | PASS | 0 | artifacts/proof/current/check_node_policy.log | b3f3ddcccb523f5bc6c15ebc81b3e697d939c9ccfd3fcdb7d13b34c1c5bf2f8c |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 79c45e2f36695f8f728fccd4a155f367fe9dd7f76d137710ca4b5c8898dfbe45 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 2c548bc3008ece215d98ba7ef6f0a1cdd8d38d6e81ff474a4a6fb54704c791b9 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 6f8ab5136766e0ab803361812baaa84c9d56991bf5a1a89173c0566fef623b9b |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 7aa81e613784be4a0a2f28b43c04741a9b668f4fb39245d5fc28aafe5dcea65a |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 6bd8c8f340ac775773516aa9c51bfa4b3d3521f09568db52f3669c615bc5c4cd |
| canlii_staging_proof | PASS | 0 | artifacts/proof/current/canlii_staging_proof.log | d7c9393bb589559678b644f26519944ef1a69f81a771fdbd5fce0282bb665ab5 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 2bcb4dd6095570ecd12839f44d8147d159892f81c5f033a7748aed6b051ec169 |
| single_proof_authority | PASS | 0 | artifacts/proof/current/single_proof_authority.log | 67de9d9d555d8a633cccb3b3fd168f55f5975ed306de95965f06666949cc4337 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | a026290541b01f990932e208255ed0295bfd5064d3577b0f209670145b16d48e |
| proof_consistency_pytest | PASS | 0 | artifacts/proof/current/proof_consistency_pytest.log | 80cc2ecf12ffc8469e01131917b32ec0682eac22f6e92080be3e6d3a005b8aa8 |
| required_proof_logs | PASS | 0 | artifacts/proof/current/required_proof_logs.log | 2f370b5ef35ebfbdf81ea7ceb911be9769e9a64c21514a09b721a6c440e7b6e3 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 674e78e84170bc8f441b61b7148fe22a1e4d74821f2c906f1f3be36321222599 |

## Remaining Blockers

- none

## Stale Or Misreported Claims

- none

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
