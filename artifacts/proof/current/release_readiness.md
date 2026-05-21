# RELEASE_READINESS

- generated_at_utc: 2026-05-21T00:19:41.923125+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: f7f430681d3ec98954fe86fb64414ececb00b641
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
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
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | e429de281c0fa93c7a42d963c7d7fba554f4e1bcec89fe820486602337cd41dc |
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | d46921ae161dd2f123dd387bfdb23e3b1f2b19d41c4b840372d8468cc051707b |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 2f00ed1e1f571e0ba077b41c90c45cbcab937aefa69b749faa62513d9228f2bd |
| postgis_proof | FAIL | 1 | artifacts/proof/current/postgis_proof.log | 05074a907b727cd76e83b1d6d68c4f491d892f309c9c7efa225b90ae64e91f73 |
| egress_proxy_proof | FAIL | 1 | artifacts/proof/current/egress_proxy_proof.log | cf914157f8930ddeb0d1ea7c7dda78191ab9ad77ce618a8cc90d0d9d8781dd78 |
| demo_proof | FAIL | 1 | artifacts/proof/current/demo_proof.log | 26b02dae11e0d26cb5b1244b8009602bd6c3a097b3b20af2591c5c7745aff1e1 |
| validate_sources | FAIL | 1 | artifacts/proof/current/validate_sources.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| check_yaml_duplicate_keys | FAIL | 1 | artifacts/proof/current/check_yaml_duplicate_keys.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| verify_source_registry | FAIL | 1 | artifacts/proof/current/verify_source_registry.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| source_registry_status | FAIL | 1 | artifacts/proof/current/source_registry_status.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| prepare_proof_db | FAIL | 1 | artifacts/proof/current/prepare_proof_db.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| verify_evidence_store | FAIL | 1 | artifacts/proof/current/verify_evidence_store.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| verify_audit_chain | FAIL | 1 | artifacts/proof/current/verify_audit_chain.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| auth_mutation_route_coverage | FAIL | 1 | artifacts/proof/current/auth_mutation_route_coverage.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| mutation_fail_closed_coverage | FAIL | 1 | artifacts/proof/current/mutation_fail_closed_coverage.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| frontend_node_gate | FAIL | 1 | artifacts/proof/current/frontend_node_gate.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| frontend_install | BLOCKED | 1 | artifacts/proof/current/frontend_install.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_lint | BLOCKED | 1 | artifacts/proof/current/frontend_lint.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_typecheck | BLOCKED | 1 | artifacts/proof/current/frontend_typecheck.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_contracts | BLOCKED | 1 | artifacts/proof/current/frontend_contracts.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| frontend_build | BLOCKED | 1 | artifacts/proof/current/frontend_build.log | 81e994d60d6eb291e23f2cbfcc54f0008a99563866c7214c6b862d5cb66decbc |
| check_api_contracts | FAIL | 1 | artifacts/proof/current/check_api_contracts.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| repo_generated_files | FAIL | 1 | artifacts/proof/current/repo_generated_files.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| check_npm_audit_triage | FAIL | 1 | artifacts/proof/current/check_npm_audit_triage.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| map_route_check | FAIL | 1 | artifacts/proof/current/map_route_check.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| public_api_boundary | FAIL | 1 | artifacts/proof/current/public_api_boundary.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| proof_freshness | FAIL | 1 | artifacts/proof/current/proof_freshness.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 1a7820a48227acb06b95ebb70a5d5d004e5c2fe05db6ac775bc81be062f80ce6 |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | d44df28e5dc80d80ffd30292a39250fe1bd369390c1797c6387ce947ed05d05b |

## Remaining Blockers

- required_gate_failed:backend_pytest
- required_gate_failed:postgis_proof
- required_gate_failed:egress_proxy_proof
- required_gate_failed:demo_proof
- required_gate_failed:validate_sources
- required_gate_failed:check_yaml_duplicate_keys
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
- required_gate_failed:check_npm_audit_triage
- required_gate_failed:map_route_check
- required_gate_failed:public_api_boundary
- required_gate_failed:proof_freshness
- required_gate_failed:archive_validation
- archive_validation_not_pass

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
