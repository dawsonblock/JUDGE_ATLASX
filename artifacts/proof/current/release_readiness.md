# RELEASE_READINESS

- generated_at_utc: 2026-05-15T04:43:28.908943+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 16d6b61c15cc3785033a4c0435f2da1f81eb4e0d
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- node_version: v24.15.0
- npm_version: 11.12.1

## Required Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| check_no_pyc | PASS | 0 | artifacts/proof/current/check_no_pyc.log | a846f2e3cfab43e1b94af70247e6dff79ec62b983961a207185d87595b1b7ff6 |
| check_false_claims | FAIL | 1 | artifacts/proof/current/check_false_claims.log | 143deb09d519413a1a35bb774b85ae7775d7ff1c1b6aaccc9e04c77fbc404137 |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | PASS | 0 | artifacts/proof/current/check_source_registry_docs.log | fe1b62e3c0b1bc448549dfe49a124455c9c01b1813f6d4e8effac96e238d35fe |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | b37c6dbf65566cc27820af5fe0de5997781559cea4b5e5a4219696855d2a89cf |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | 8bcb050bc473b6a2ca5ff96c77c2c2a0a95fc257fa53054941f89fd6327a435b |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 02f7283ab6012eea4ed77e72de82d52e17a495e6d6eec4bdab67f07ee30bc5d4 |
| postgis_proof | FAIL | 1 | artifacts/proof/current/postgis_proof.log | 09b6669b6735955a73ed79559e5855a2b49d5a8169e8a27040ed0b045b60efa4 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 1277d9b402205e139c94319b780be8ef03d6066b96f29b8fe20cf908d7c66f57 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | c45f3e197b1df8faf71ccfbb1cde8c83793ad0dd4e06faf8cf10bfe1493c3c73 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 12f833fa0cf117963231f1e74e641aeb4bf6276ac39ff568d07b4e1ad0d42750 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 77a0e2d638ea91634cbfd0af3c87ae083b42a7794058bd12449684d16509f971 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 17fdafa3eaa51e7919ed0afb180edd30b94eca9569a990788b6f9d08fddef954 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 2a33f1b9796dc79daaf7c12b0dc9bb6eac2670be1940cf23d0bb26cb49def682 |
| frontend_node_gate | FAIL | 1 | artifacts/proof/current/frontend_node_gate.log | 20315d7633700c087490ffa770ecff19a3dc5a06788822f15dcbbf5a4adfffaf |
| frontend_install | BLOCKED | 1 | artifacts/proof/current/frontend_install.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_lint | BLOCKED | 1 | artifacts/proof/current/frontend_lint.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_typecheck | BLOCKED | 1 | artifacts/proof/current/frontend_typecheck.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_contracts | BLOCKED | 1 | artifacts/proof/current/frontend_contracts.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_build | BLOCKED | 1 | artifacts/proof/current/frontend_build.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| check_api_contracts | FAIL | 1 | artifacts/proof/current/check_api_contracts.log | dd5d97b722153983c646bc1df5f820f95fe710923e6ff95cba9712a027d168a9 |
| repo_generated_files | FAIL | 1 | artifacts/proof/current/repo_generated_files.log | b05fe4711c489b0c88494dda83160de02bb2f7dc9bca2e73691d13281b0c1b49 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 78ebbcc52598a48a739f08fbbc4ef958826f7b2d66cc8a5b365b473e71847020 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 0e80afc9bb82b4b8f0816b210c78499c88a92d59ea5305bf46bd4ac83a858420 |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 45997782af1804d5beb32685ab78e1b300b9a89e6ce508fc843f4f00e7c0662d |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 6cd1e3e58b79822fe1dcc6fdd62e597ad81395ae07704d459d089950ba10493e |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 45122e8b3d98d31930f402fc584d6af36426c13c9ab40427e5f20ebb697b1e8c |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | 015ed50cf0ff7074aee9a78ecd7964d8087f75e64968cb997346a34ed8aab89f |

## Remaining Blockers

- required_gate_failed:check_false_claims
- required_gate_failed:postgis_proof
- required_gate_failed:frontend_node_gate
- required_gate_failed:frontend_install
- required_gate_failed:frontend_lint
- required_gate_failed:frontend_typecheck
- required_gate_failed:frontend_contracts
- required_gate_failed:frontend_build
- required_gate_failed:check_api_contracts
- required_gate_failed:repo_generated_files
- required_gate_failed:archive_validation
- node_major_mismatch:Expected Node 20.x, found Node v24.15.0
- archive_validation_not_pass

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
