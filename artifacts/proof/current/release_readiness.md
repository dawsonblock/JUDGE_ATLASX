# RELEASE_READINESS

- generated_at_utc: 2026-05-19T22:07:06.258025+00:00
- overall_status: alpha-proof-pass
- production_ready: false
- release_recommendation: alpha-proof-pass
- archive_hash: 1f28e795d0c9c6deae74f3931a8eb5184b976008
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- gate_runner_node_version: v20.20.2
- frontend_node_gate_version: v20.20.2
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
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | 8f6537cb7e3236306832e35ae185e1dcab93b5c124f4cf5380d460112fdaa3e2 |
| backend_pytest | PASS | 0 | artifacts/proof/current/backend_pytest.log | dbf1cbcb40943beefa9a7cdd0f14cd0a0614ff6f0a70291da4a99cbcfecdc817 |
| check_migrations | PASS | 0 | artifacts/proof/current/check_migrations.log | b1a31ef1e482457fd1c47ac213cc98d199e78f8051acc81264a305cf629b66bf |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 9004c058488b161dcf9bc606f6e99defe3ccfbf584f349addbd9f4c60059a420 |
| postgis_proof | PASS | 0 | artifacts/proof/current/postgis_proof.log | 5a9724ffc36c3fd526959a905da517c5ab17e068bfd95ee51e6f3615d2a81c99 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | f6c972f79ca0a589639c7ce06cfb1201e71498acebe3841a464ef8601d0b4289 |
| demo_proof | PASS | 0 | artifacts/proof/current/demo_proof.log | 327cc313bcd037a966775bd5b877b5c4a84265a7f7755c41ef3db78ee82b2e94 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 05e3e24875d7cd0a58447a3c0ca8b1a16553787e11d30b4fdc9d3446a6ccfca8 |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | PASS | 0 | artifacts/proof/current/prepare_proof_db.log | ef6779db88eeffa32551cb68ca12147f76837d1ef139b9e8d67f668940f260d5 |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 7b693f37394b451d76dd236d9668d34a5e48b67f48dee151954763083deca20f |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | f3e09744c103cc8112533b0db8ad182026393a32af6ee9fd69ac18a4888c1b65 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 19e95f03931508bcb63d5f1f276741db94fd3f8f0399d2690ed306a73c3ba6c7 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 566b533769efda184c621fadcbb3499a3de7b732897627c27b430e8565082bbb |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | c65abdafdc4e14592a41b48937df3c77e307a5ac6624b005cef249e4529d3670 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | fb100198bb1b4bb1a9b4a4cd7b6e4334b410483b7ba7f0e105b922c45b58ee61 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | a092a4c8be3cf894b61a7a1b26b8fd746085f10500a8c94dd07f89ecfb544f3a |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | a24f4940adc7597eeb444006b65dfb80f5a5adcb7d2b69c4d6322b7d429d911f |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 9dc4e7eea5a5e96cd6ffc6ef8d27793275b71d18f69711a757d9bd58be2a49fd |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 65633723f387e649e8f04e59614f0d295c0466a5a9554780b1947b1236826052 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | 644c53a8b63701ebb8f8c8b9d109a4f055ade496c5b92277d9763443dd5c3eb2 |
| archive_validation | PASS | 0 | artifacts/proof/current/archive_validation.log | 1e8550d0eea99a7509a7990ac52204d0d28911f5fc7159985d392705991e8eaa |

## Remaining Blockers

- none

## Stale Or Misreported Claims

- none

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
