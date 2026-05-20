# RELEASE_READINESS

- generated_at_utc: 2026-05-20T01:43:35.184379+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: cac765bdf5964314a063c2486c7819ae8152a5cf
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
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | 3c91f250dda97ecfae0990f5e8dadf0c77e5b941392a7b60fbd1ed16cab8f666 |
| check_migrations | FAIL | 1 | artifacts/proof/current/check_migrations.log | 7a43e5916cc2cdffa5d277e8804ab26c7d540ea50a80e1aea0b8c287811754d2 |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | 9004c058488b161dcf9bc606f6e99defe3ccfbf584f349addbd9f4c60059a420 |
| postgis_proof | FAIL | 1 | artifacts/proof/current/postgis_proof.log | 91ffff81db1717a617493251aa8e10642654b6db5b54f6816361a9a65d9d5bd5 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 304de61e247d38990f9fecc066d227d57f45f5adc0593c052b6a74f6fd7a57a5 |
| demo_proof | FAIL | 1 | artifacts/proof/current/demo_proof.log | b2dbc91f6ad10a18728f74d0f3dcb6700219d2b497e7ab16e2090fdaa772a39f |
| validate_sources | FAIL | 1 | artifacts/proof/current/validate_sources.log | d52543c4f39605492cd3f16bc5a22a7476a1248961f166761d6384171c008b68 |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 51a033a57c01ccd45f33c15c9701c5559ad4545e1105a232f03a84c9da82fc7c |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | FAIL | 1 | artifacts/proof/current/prepare_proof_db.log | 9d18052aae771d7cd9e95302555234793fc217bbfa25dd90701a1368e698279f |
| verify_evidence_store | PASS | 0 | artifacts/proof/current/verify_evidence_store.log | 1179d0c8c1c56de20d4f917fd60915207780fa80305d5ffb0e8d31ff25adc9a1 |
| verify_audit_chain | PASS | 0 | artifacts/proof/current/verify_audit_chain.log | 01ab2325e8e19ba0c1931aa6934d2f6222d47c828b058e1df0f21d98a6727a16 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | bfb94aa3bce5e5c9a8e413d4c0b8cbbecf5444cc553dd49310e15bc548c86a10 |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | 566b533769efda184c621fadcbb3499a3de7b732897627c27b430e8565082bbb |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | c65abdafdc4e14592a41b48937df3c77e307a5ac6624b005cef249e4529d3670 |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | f440b647f033d86a8b86360390b49b5743f050f30cafc133947a534468ccd6a6 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 4b456243d33d4f4a102ebe4d6785acf6f50894b664c463346cc21b84a4f9d4cd |
| frontend_typecheck | FAIL | 1 | artifacts/proof/current/frontend_typecheck.log | 8d253fb37b7d4414f347e43dca15474c1ecb99d162dd9cbfc89cf978b8c5fe70 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 26bcda6f2f2e3a3c2c21fda708bc959cf45c2508d96bbc8a1bf0dc43a3c18d91 |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | ffe3d57b75f92ff3887eb80e401fd1227db312dc02abe794b9fc341e4e7beadb |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | PASS | 0 | artifacts/proof/current/repo_generated_files.log | 7e6ff97ad128bc573ab50f71262ff7561a2508747ada9b72abfa2fac77523dfd |
| check_npm_audit_triage | PASS | 0 | artifacts/proof/current/check_npm_audit_triage.log | 09470ee10bceef4b5371da2106a690e33d7d563a18a5dd2ccabfc2af0a29a331 |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | FAIL | 1 | artifacts/proof/current/public_api_boundary.log | b4ba867ebd641988b570bfa9833fce2d3d823b915fa1e96f5c40589b90ee0df5 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 6a78a0d35dd779835965c4d89dec0e6810d920b6213b09d5731d5ea8d944cd8e |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | df1ffda780ae57da3beff24f4c0e930313a408d1eb302b468858687130409f5d |

## Remaining Blockers

- missing_required_gate:archive_validation
- required_gate_failed:backend_pytest
- required_gate_failed:check_migrations
- required_gate_failed:postgis_proof
- required_gate_failed:demo_proof
- required_gate_failed:validate_sources
- required_gate_failed:prepare_proof_db
- required_gate_failed:frontend_typecheck
- required_gate_failed:public_api_boundary
- archive_validation_missing

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
