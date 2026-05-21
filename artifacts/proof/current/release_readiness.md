# RELEASE_READINESS

- generated_at_utc: 2026-05-21T06:29:08.716136+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: ec0d0253ec855bfec9cda945fbee8c2f3a144cc4
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
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | f722c82c7def9e790c1676a4e1bdb4c064370a48071b37d54cf00c26ca8efd47 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 98dbca9d762dac013e3edc343338020ae11f21e7df9cab72391ef5472effb5b4 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 6d6c069411abb14a7b06221cbc746b8b8a3126b07f0b5678a9ddf28a35a36679 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | f7d920823ddc070bd9be6817e9d7dc96591fe95613eede304a312a943c237f6a |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | be249746679354c502b8b8854c430966c466bc16cff9935f201bc69afaf788eb |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 55fb1635e826dce58385e8c42e2694146895631e5cb64b4fd600ca1ceae74797 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | eb8ae548052c2912811c71484e10eb47a7667677bf6b3cdd77419c07d73c81fa |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 6d46f0d8c03dc6ba208f706cf319cc0f665fe7933dc3104c96d6fcda51c12759 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 19e95f03931508bcb63d5f1f276741db94fd3f8f0399d2690ed306a73c3ba6c7 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | ce22630fc7c34a988df630b4a92fb58d299903bc888dd68e961f12bfa2af1024 |
| check_node_policy | PASS | 0 | artifacts/proof/current/check_node_policy.log | a12ab616b1354b97e3f4584d9439874be22d679373efb54abb659c4e887036c8 |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 79c45e2f36695f8f728fccd4a155f367fe9dd7f76d137710ca4b5c8898dfbe45 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | a9747b048be3756cce54355e6d8fcdfe5cf285650dc1e85b0f065a61f6f291c2 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | f1dd0b97c4d6201ff834a2584248ccffe46852c69e496a2444b65f67b4f1372b |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 7aa81e613784be4a0a2f28b43c04741a9b668f4fb39245d5fc28aafe5dcea65a |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | f2059c1eb2c98dc3d8970b35e65f4b5e24baecd8966b9cd32316e28c4fd645a6 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 389c4d760d07945d6f770f0ad43e8fc54e7368e6f6a454393a9307ec70f74059 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | e7e8234e6d2dc1148d05ed9faa9b648ece1628a2b25b611297c4aafcb41bea24 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 4c4f665051b24b32e42a7e1fba4569f6f50be862f3357b2d08345d9e922ec08b |

## Remaining Blockers

- missing_required_gate:single_proof_authority

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
