# RELEASE_READINESS

- generated_at_utc: 2026-05-21T08:34:50.232008+00:00
- overall_status: alpha-proof-pass
- production_ready: false
- release_recommendation: alpha-proof-pass
- archive_hash: 756289219963a59c59a4e1b0295c5dab450e17a5
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
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 4f4e1b4c2d14e918e7e9fdf24b779bdb6c3a551e25449648f83168be56da5030 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | b75a97dbf33c6aab50ba7762ba9bc7bc0f215989dd1c1630755cbb1098ae5a82 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 4918fd9629e887aca459d8c33c179a466dc0c113dbf2b1749b313e603a8caf84 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 743654517f7ea1f6c252ab3360f1f4c30bd1d5873f342f6a3d0cabc699ad5a05 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 55fb1635e826dce58385e8c42e2694146895631e5cb64b4fd600ca1ceae74797 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 9cfda31acc3b863717079da3a921eb11a0e958c232be743ddab64bc53d1648ba |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 6e4c18ea642d609592a319bde752057ae36a0c464805ce057bd321d5673ddf7a |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 89d3ec78cb0fbd89b7737bfe3078876ad657c2c3b955758b5a26267a44a5d86b |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 44091516c6f7d278c9900d796163d45f95d1ad1819370ffeeaf887bc704f2e38 |
| check_node_policy | PASS | 0 | artifacts/proof/current/check_node_policy.log | b3f3ddcccb523f5bc6c15ebc81b3e697d939c9ccfd3fcdb7d13b34c1c5bf2f8c |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 79c45e2f36695f8f728fccd4a155f367fe9dd7f76d137710ca4b5c8898dfbe45 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 637a29bc305cdce655f31d7dd24ac3b08c01f7482afd5e99af78295a6caf878f |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 92b9f826b70495a44e1b6dce54ae7705d96e2ee1ed434ed412b82de16960db87 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | 7aa81e613784be4a0a2f28b43c04741a9b668f4fb39245d5fc28aafe5dcea65a |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | f492d0774b25a2915565da1f1888d5e5e9b9a6825d6eabbd3463f0e26f22e3cd |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 9c85cbfd94484f55bb0a7972f6e9a9778b3d64fb1deaf141becd980f70c6f687 |
| single_proof_authority | PASS | 0 | artifacts/proof/current/single_proof_authority.log | 67de9d9d555d8a633cccb3b3fd168f55f5975ed306de95965f06666949cc4337 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | b5ec131926cc8132aced9059667356253eb266cb2ad860a203aa999ef4659297 |
| proof_consistency_pytest | PASS | 0 | artifacts/proof/current/proof_consistency_pytest.log | 9b11cb2f3356aba2b6bea79c5002067b83ed8c2e96bb42b301fec1fe49fd2c79 |
| required_proof_logs | PASS | 0 | artifacts/proof/current/required_proof_logs.log | f1a485dd0d49f2e059e267a30bae6f839d36b274061f23655f6b8b6525f160c0 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | b791caa87908efe358b5f9f8d1d3b48d9ab4d167ea311a0c3059b77e23c686b7 |

## Remaining Blockers

- none

## Stale Or Misreported Claims

- none

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
