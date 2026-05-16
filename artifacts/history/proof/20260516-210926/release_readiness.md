# RELEASE_READINESS

- generated_at_utc: 2026-05-16T21:07:37.560100+00:00
- overall_status: blocked
- production_ready: false
- release_recommendation: blocked
- archive_hash: 505a93ea012837a27127931590a7a12820366133
- platform: macOS-26.2-arm64-arm-64bit
- python_version: 3.11.7
- node_version: v24.15.0
- npm_version: 11.12.1

## Required Proof Gates

| gate | status | exit_code | log | sha256 |
|---|---|---:|---|---|
| check_no_pyc | PASS | 0 | artifacts/proof/current/check_no_pyc.log | a846f2e3cfab43e1b94af70247e6dff79ec62b983961a207185d87595b1b7ff6 |
| check_false_claims | FAIL | 1 | artifacts/proof/current/check_false_claims.log | 4b8b482333948d6c4789e3011704e0077d7dbc27e63f6230fa324d720718a2e3 |
| check_source_keys | PASS | 0 | artifacts/proof/current/check_source_keys.log | 5a19cc9f9747d78ac73bb6e54323386b8a32b69079e204630f249748b6ffb39c |
| check_statuses | PASS | 0 | artifacts/proof/current/check_statuses.log | c5a1e374a12383ff2f924e70bd72bb2ba7210c803d1bba658765034a41a5b256 |
| check_no_direct_ingestion_network_clients | PASS | 0 | artifacts/proof/current/check_no_direct_ingestion_network_clients.log | ab01be057c4e3b265f8f9cc13a4ab4a145abca00913b61d7adf7116dbb1dca58 |
| check_source_registry_docs | FAIL | 1 | artifacts/proof/current/check_source_registry_docs.log | 156488c31d461920b2f20d6ef3e7458b6a5a37b9f1e323ac2c1b4cd2dd2ed9be |
| check_external_boundaries | PASS | 0 | artifacts/proof/current/check_external_boundaries.log | da039530a33bf730b0cc264637a3196b2212a42c42e24f50edcb6f1090c41b62 |
| backend_compile | PASS | 0 | artifacts/proof/current/backend_compile.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| backend_import | PASS | 0 | artifacts/proof/current/backend_import.log | f722c82c7def9e790c1676a4e1bdb4c064370a48071b37d54cf00c26ca8efd47 |
| backend_pytest | FAIL | 1 | artifacts/proof/current/backend_pytest.log | 02b55943bbcca8cab307a0d9027924f54ec5ab77b8c0832c84b174db6e609f63 |
| check_migrations | FAIL | 1 | artifacts/proof/current/check_migrations.log | 54be43380b7f89abd49343569455c7df6c197716bffc9acbf29e72a1156d908e |
| docker_runtime_preflight | PASS | 0 | artifacts/proof/current/docker_runtime_preflight.log | c309bbd87451e3f32452f819b1fafa809889d9728fead3ed2fb248b352d07ac9 |
| postgis_proof | FAIL | 1 | artifacts/proof/current/postgis_proof.log | 4506b95c5ae3ac51c05380d45a7205b43d8f4814981d67dbcc7e56770fdc4c72 |
| egress_proxy_proof | PASS | 0 | artifacts/proof/current/egress_proxy_proof.log | 0544b61e8f7f29d06fd9791311c0ed71ab539a19cd497e646f0927d4b67af803 |
| demo_proof | FAIL | 2 | artifacts/proof/current/demo_proof.log | 6a4b680a5425c16c63de588aac802c5d62df03ce23e90c63e2c26876b37dc409 |
| validate_sources | PASS | 0 | artifacts/proof/current/validate_sources.log | 4d734d90bf04c25a04d4752d5067c94dc51e963876cfc4f61bbf698de63c27ba |
| verify_source_registry | PASS | 0 | artifacts/proof/current/verify_source_registry.log | 2f9559115fbea52733da77b8e493acb355bc4c153fb71fdee450ba6baeef205e |
| source_registry_status | PASS | 0 | artifacts/proof/current/source_registry_status.log | 194970ce6494bacb9547233e7de0514c90912785c4df32ef959b72adb486e805 |
| prepare_proof_db | FAIL | 1 | artifacts/proof/current/prepare_proof_db.log | c39edd67eafbe6ca36f522357e0a157c20d805c620515d754fb2b2e63a6e0bb2 |
| verify_evidence_store | FAIL | 1 | artifacts/proof/current/verify_evidence_store.log | 23b4c067dec6b1ab124dc035846ee1fb2cb14346c140caea749cd737500cb028 |
| verify_audit_chain | FAIL | 1 | artifacts/proof/current/verify_audit_chain.log | f1617b86a5054e95ba1d0038e126533534d4a0badb9814c202dd719199a36f83 |
| auth_mutation_route_coverage | PASS | 0 | artifacts/proof/current/auth_mutation_route_coverage.log | 68683c941f53fd55547c17b6a1b7a966702a2b51e89bd6832b00e772606b6b6e |
| mutation_fail_closed_coverage | PASS | 0 | artifacts/proof/current/mutation_fail_closed_coverage.log | a3743b2a379a4c611aab88f2dd4a717b1f18ae345d3b524353c6daddbbda95ef |
| frontend_node_gate | PASS | 0 | artifacts/proof/current/frontend_node_gate.log | d82414c1d9dc6d5a72459d42f65920186da05770c9e8c0dd70833906ec6813db |
| frontend_install | PASS | 0 | artifacts/proof/current/frontend_install.log | 7776e0dccb191ea8b622dd2cf437dfc9bb06749d3a4797a38cbb3c939d12d639 |
| frontend_lint | PASS | 0 | artifacts/proof/current/frontend_lint.log | 9d79910829d5abcf1161f85f3d57cc9c745d1edd5734a88fee634c9913b368e8 |
| frontend_typecheck | PASS | 0 | artifacts/proof/current/frontend_typecheck.log | 701338e1389ab6284419cba533b353099f6b47658b930e128a8627a7a2d6d6e7 |
| frontend_contracts | PASS | 0 | artifacts/proof/current/frontend_contracts.log | 8f15e244c3c64e1432035fb5c7a8fe9bf67fd1f907ab751c29bf7e2a5d6a573e |
| frontend_build | PASS | 0 | artifacts/proof/current/frontend_build.log | f22be5d40d7f70376f1085cfbce6102bad9d3133ec312701c0aabbb9ec0a7928 |
| check_api_contracts | PASS | 0 | artifacts/proof/current/check_api_contracts.log | f6750f8d64797a660c9122c245fa0ae38eb689dd8023b7fef1d0481e4ab86216 |
| repo_generated_files | FAIL | 1 | artifacts/proof/current/repo_generated_files.log | 89debbe2a577ae6914ee67a02a4aa5341b0b26d3b0fa9e5773b4b86292d7ed78 |
| check_npm_audit_triage | FAIL | 1 | artifacts/proof/current/check_npm_audit_triage.log | a7c49d8a9ae38f847a8d6c1f3b07e531c17b1300dee00689d298a2b6f826aa6a |
| map_route_check | PASS | 0 | artifacts/proof/current/map_route_check.log | 3f2c0fb18144134952224494bc6690cde35213914ff5880a8eed0b5ca519e30f |
| public_api_boundary | PASS | 0 | artifacts/proof/current/public_api_boundary.log | 1f9efd854b1ce46c541f6186d52d641b3825867401b4f1d59c95677245fb4ac1 |
| proof_freshness | PASS | 0 | artifacts/proof/current/proof_freshness.log | 72367522b57be0defb94290b19ceb8034c015e505aa682aa9cd7dba8f955b1c2 |
| release_readiness_generation | PASS | 0 | artifacts/proof/current/release_readiness.md | b5527c76c8ec8e2fba224ff8992711ab8e3a2bcefddff41c1f4fa180dbf66668 |
| archive_validation | FAIL | 1 | artifacts/proof/current/archive_validation.log | 976be3dc8b06749f769ad977cefe5cf72d532cdc1425c5fde141322d984cca97 |

## Remaining Blockers

- required_gate_failed:check_false_claims
- required_gate_failed:check_source_registry_docs
- required_gate_failed:backend_pytest
- required_gate_failed:check_migrations
- required_gate_failed:postgis_proof
- required_gate_failed:demo_proof
- required_gate_failed:prepare_proof_db
- required_gate_failed:verify_evidence_store
- required_gate_failed:verify_audit_chain
- required_gate_failed:repo_generated_files
- required_gate_failed:check_npm_audit_triage
- required_gate_failed:archive_validation
- node_major_mismatch:Expected Node 25.9.x, found Node v24.15.0
- archive_validation_not_pass

## Stale Or Misreported Claims

- readiness is blocked due to failed/missing required proof evidence

## Next Repair Action

- Resolve any required failed gate and rerun scripts/release_gate.py.
