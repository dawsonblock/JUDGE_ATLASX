# Alpha Deployment

This is the canonical alpha deployment reference.

## Preconditions

- runtime boundaries pass
- proof command passes
- release zip validates cleanly

## Commands

```bash
make proof
make build-clean-release
make validate-release-zip
```

## Output Artifacts

- `artifacts/current/PROOF_REPORT.md`
- `artifacts/current/PROOF_MANIFEST.json`
- `artifacts/current/RELEASE_MANIFEST.json`
- `JUDGE_ATLASX-alpha-clean.zip`
