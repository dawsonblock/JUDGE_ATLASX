# Alpha Deployment

This is the canonical alpha deployment reference.

## Truth Statement

JUDGE_ATLASX is an evidence-governed Canadian legal intelligence alpha. Evidence is authoritative. AI and memory outputs are derivative only. All public-facing data requires human review approval and must be linked to an evidence snapshot. This is an alpha release, not a production legal authority.

The source registry is the authoritative source of truth for ingestion status. Only sources marked as "enabled_runnable" in the source registry are currently active.

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
