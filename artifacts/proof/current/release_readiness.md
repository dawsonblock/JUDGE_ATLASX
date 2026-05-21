# RELEASE_READINESS

- generated_at_utc: 2026-05-21T00:39:37.718159+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 33b4ef99302778dddb0afd079f90beab9bfeef35
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- node_version: v25.9.0
- npm_version: 11.12.1

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
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | e429de281c0fa93c7a42d963c7d7fba554f4e1bcec89fe820486602337cd41dc |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | c06e4fa461ea71316a62d3413c6f561b7b34308c913e9b3fbb3842cbee3985cd |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 2f00ed1e1f571e0ba077b41c90c45cbcab937aefa69b749faa62513d9228f2bd |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | a59ee2a298043c7bdcaf780ddffb65d867ec1a8dc2f9692ccf150ef82b7e7bf4 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 343df55c50259d072f786bf3f35f110788d3b663e2aebfa2725a40081b893fc2 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 55fb1635e826dce58385e8c42e2694146895631e5cb64b4fd600ca1ceae74797 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| check_yaml_duplicate_keys | PASS | 0 | artifacts/proof/current/check_yaml_duplicate_keys.log | 88b52b46f87e415fc01b849aececd79f567ac8ea21f09f1d891a37eca7ddb06d |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 87ff32f707569db9b7bd2bbe68c4f701295831af775026eca71803e0273c577e |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 9babd9dfaea20969f8fa10dfbf1635cb79aec0012037bde38618213b5cf027c1 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | f4c61c0ac8f55c6c9a2d6c593731bf5f8c4a6c5bebbe514284fd4f899818f9e0 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | ffe2a4a341462d569b35e1e292ac1aa0fb4d5f4f8c0cc6d1855131d67100244c |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 3c0f4db7820ebf1923d54f9b493763ae6386af0f310195b3b1ddcd07a891eb14 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 4b456243d33d4f4a102ebe4d6785acf6f50894b664c463346cc21b84a4f9d4cd |
| frontend_typecheck | FAIL | 1 | artifacts/proof/current/frontend_typecheck.log | f637dfb4366601120be67c00c76aff187c008eca53ebc74ad5babd78b66a323f |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 4faf5612a6c72ca5480644b23d1bb1572158d8e279215c6e73f2785486b4455d |
| frontend_build | FAIL | 1 | artifacts/proof/current/frontend_build.log | 4068963a07b710d3328273027437834dbd45cd262ea6bf993e8139e3e569187a |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 08d740b77e2e85bd02a0e1c199f881bdfa49f829f414fe07fa49a592bf778486 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 9932c4a0f9fe9072136af39c3c8b07827153428e627e7d4d2385931a472edf56 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 1c077f50ec89b8612c876709b34e1d6151076af2e1da6182d2533196451b3dd4 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 1b6f73e2358996bfdd8896becd6b26deea2ccaed64ef3702c8395c728056cbc9 |

## Remaining Blockers

- required_gate_failed:frontend_typecheck
- required_gate_failed:frontend_build

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
