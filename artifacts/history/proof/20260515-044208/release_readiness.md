# RELEASE_READINESS

- generated_at_utc: 2026-05-15T04:40:00.948527+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 16d6b61c15cc3785033a4c0435f2da1f81eb4e0d
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.9.7
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
| backend_import | FAIL | 1 | artifacts/proof/current/backend_import.log | dab659f06f79ad99905bfec9796af355dbd136132f5a28c7187cc6a518df1574 |
| backend_pytest | FAIL | 4 | artifacts/proof/current/backend_pytest.log | 25e97fabe0bf5ed5c75d22e9a7a6123b825328f54ddb8f6c0df72f5edededbbb |
| check_migrations | FAIL | 1 | artifacts/proof/current/check_migrations.log | 24181571dc19e6aec63d6ee572c93f0573f2eb238d03031d76a68b38c15b52c0 |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 02f7283ab6012eea4ed77e72de82d52e17a495e6d6eec4bdab67f07ee30bc5d4 |
| postgis_proof | FAIL | 1 | artifacts/proof/current/postgis_proof.log | 5edb13fdc8408d421ec33835245f5e720c5b34e85e2964400987d6a8bde35e3a |
| egress_proxy_proof | FAIL | 4 | artifacts/proof/current/egress_proxy_proof.log | df4ae2e455cc1f67c7378e3d31957847dfab0cc41be4766ec94acdd33411897f |
| demo_proof | FAIL | 1 | artifacts/proof/current/demo_proof.log | 262a51842a3a51b78c31301e415d7fb37cad5ef4573dd697f0d24b378a2c5b57 |
| validate_sources | FAIL | 1 | artifacts/proof/current/validate_sources.log | c1e03ec71edeb6ef7c2627ebf09dc035e2b10b5bdca9ce200f065bcd5d232a34 |
| verify_source_registry | FAIL | 2 | artifacts/proof/current/verify_source_registry.log | 3c734b711f5e84ded743f141ef038153631a654e5a7d8bff8e7ffa33ce17ff6a |
| source_registry_status | FAIL | 3 | artifacts/proof/current/source_registry_status.log | 8582ad2ff3e5069be02928321ff95cc429be55ce02b2262ecb1b67cc6e531e27 |
| prepare_proof_db | FAIL | 1 | artifacts/proof/current/prepare_proof_db.log | b8622fb1e3e9c211359faec01cc8bfd3a3c29ce2de27b002139326523992ef94 |
| verify_evidence_store | FAIL | 1 | artifacts/proof/current/verify_evidence_store.log | ec1a659e5e649469edb4f500b50196b65b64184e07b339ae8e07a5b6a33ac0c4 |
| verify_audit_chain | FAIL | 1 | artifacts/proof/current/verify_audit_chain.log | 59674b380e243e4e5f5305c19f28c5b630ccc2d2438b0597a6ec3ee117610e37 |
| auth_mutation_route_coverage | FAIL | 4 | artifacts/proof/current/auth_mutation_route_coverage.log | 25e97fabe0bf5ed5c75d22e9a7a6123b825328f54ddb8f6c0df72f5edededbbb |
| mutation_fail_closed_coverage | FAIL | 4 | artifacts/proof/current/mutation_fail_closed_coverage.log | 25e97fabe0bf5ed5c75d22e9a7a6123b825328f54ddb8f6c0df72f5edededbbb |
| frontend_node_gate | FAIL | 1 | artifacts/proof/current/frontend_node_gate.log | 20315d7633700c087490ffa770ecff19a3dc5a06788822f15dcbbf5a4adfffaf |
| frontend_install | BLOCKED | 1 | artifacts/proof/current/frontend_install.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_lint | BLOCKED | 1 | artifacts/proof/current/frontend_lint.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_typecheck | BLOCKED | 1 | artifacts/proof/current/frontend_typecheck.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_contracts | BLOCKED | 1 | artifacts/proof/current/frontend_contracts.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_build | BLOCKED | 1 | artifacts/proof/current/frontend_build.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| check_api_contracts | FAIL | 1 | artifacts/proof/current/check_api_contracts.log | 24cb32b8f2245fdb33ed496dd962ffaba53a96be06e8f41b85338c8ac168bcbd |
| repo_generated_files | FAIL | 1 | artifacts/proof/current/repo_generated_files.log | b05fe4711c489b0c88494dda83160de02bb2f7dc9bca2e73691d13281b0c1b49 |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 78ebbcc52598a48a739f08fbbc4ef958826f7b2d66cc8a5b365b473e71847020 |
| map_route_check | FAIL | 1 | artifacts/proof/current/map_route_check.log | b5e2d6513b368375dbabeb823089c3c2c93dc8a15715522bfea437c647bc5350 |
| public_api_boundary | FAIL | 4 | artifacts/proof/current/public_api_boundary.log | 25e97fabe0bf5ed5c75d22e9a7a6123b825328f54ddb8f6c0df72f5edededbbb |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 6cd1e3e58b79822fe1dcc6fdd62e597ad81395ae07704d459d089950ba10493e |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 99c9c848c8adf1342edfe8ed1fcd32e87eed2ac214ae90842d358bb511e42fb8 |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | c5612bb54402cb282ce0b57e65d5736a02a9987930bb6365e942f428dad53931 |

## Remaining Blockers

- required_gate_failed:check_false_claims
- required_gate_failed:backend_import
- required_gate_failed:backend_pytest
- required_gate_failed:check_migrations
- required_gate_failed:postgis_proof
- required_gate_failed:egress_proxy_proof
- required_gate_failed:demo_proof
- required_gate_failed:validate_sources
- required_gate_failed:verify_source_registry
- required_gate_failed:source_registry_status
- required_gate_failed:prepare_proof_db
- required_gate_failed:verify_evidence_store
- required_gate_failed:verify_audit_chain
- required_gate_failed:auth_mutation_route_coverage
- required_gate_failed:mutation_fail_closed_coverage
- required_gate_failed:frontend_node_gate
- required_gate_failed:frontend_install
- required_gate_failed:frontend_lint
- required_gate_failed:frontend_typecheck
- required_gate_failed:frontend_contracts
- required_gate_failed:frontend_build
- required_gate_failed:check_api_contracts
- required_gate_failed:repo_generated_files
- required_gate_failed:map_route_check
- required_gate_failed:public_api_boundary
- required_gate_failed:archive_validation
- node_major_mismatch:Expected Node 20.x, found Node v24.15.0
- archive_validation_not_pass

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
