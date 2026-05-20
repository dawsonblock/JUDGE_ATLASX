# RELEASE_READINESS

- generated_at_utc: 2026-05-20T09:53:11.138269+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 864b006283e408703eb7f532a30fbc601f0deb63
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- gate_runner_node_version: v24.15.0
- frontend_node_gate_version: v20.20.2
- node_version: v24.15.0
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
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | 0e6617771aadfda0719574dc50692d1e216311b71f94f21b010577e79f6aee59 |
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | cd0b09cfae481a42fa11437283a501ca884649134d36e0c3c225b06ae7fbb0cb |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 57053ba53f9b373a9aee3f5840988f64cea880ee6fd37661155d06e63b88a9fd |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 96c43518dfb1c7c3d5e6106e0b62bc70ffbd70046922f35bb93fbcfda6a21c20 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 62a68c5d4a1f2842dc44f211ad23e10b01c799b43a78716db9b003f0cc3f702d |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 55fb1635e826dce58385e8c42e2694146895631e5cb64b4fd600ca1ceae74797 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | e655076a89bfef66144afde7a193ab721261301f9f7b08cc9df8de12ab520cae |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 2dc838b5340723e9ff63a2a6821236c94ee6678db285ea7a921153a9075fb733 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | bfb94aa3bce5e5c9a8e413d4c0b8cbbecf5444cc553dd49310e15bc548c86a10 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 566b533769efda184c621fadcbb3499a3de7b732897627c27b430e8565082bbb |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | 1aaabeefd07a61f2e5f39241277580ddbe158ff27c88271f2732e612208ffa33 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 2b3471d2baa6049c495aa7ebe7d2c2bd074e9db5e99aec85a274585a57b70ff6 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 4b456243d33d4f4a102ebe4d6785acf6f50894b664c463346cc21b84a4f9d4cd |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 62564e43f227325e6efcd36258a19e382725501b1e38f67aca13e40d8c0ac84b |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | ffe3d57b75f92ff3887eb80e401fd1227db312dc02abe794b9fc341e4e7beadb |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 72bfcab6c3e6778151bca44e8072a9b2603d1734eaacd177dfef1d76e2838ca0 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 26da4efb4a60e7807cd0a1839b314c47e2c33e8805e1a6c202a28a58caab06be |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 5c0e4ce117ffde555acbf71eadcd854960baf71584a6586d5314ce25360325a0 |

## Remaining Blockers

- missing_required_gate:archive_validation
- required_gate_failed:backend_pytest
- archive_validation_missing

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
