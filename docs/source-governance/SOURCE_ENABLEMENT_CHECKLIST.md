# Source Enablement Checklist (Disabled-Ready Sources)

This checklist is for enablement planning only. It does not auto-enable any source.

Current verified counts must remain unchanged during this checklist phase:

- total_sources: 26
- runnable_now: 1
- enable_ready: 5

All five sources below are intentionally disabled in alpha and require explicit governance sign-off before enablement.

## Global Preconditions (Required For Any Enablement)

- Confirm legal terms of use permit machine ingestion and local evidence retention.
- Confirm source endpoint availability and stable fetch behavior over multiple runs.
- Run adapter contract tests and source-specific replay/fixture tests.
- Run one dry ingestion that preserves raw evidence snapshot bytes.
- Verify review queue payload quality and citation/evidence binding quality.
- Regenerate proof artifacts and verify source registry truth table consistency.
- Obtain documented approval from release/security/governance owners.
- Enable exactly one source at a time, never as a bulk toggle.

## Source-Specific Checklist

### `scc_decisions`

- [ ] Endpoint reachable and stable over repeated fetch windows.
- [ ] Terms reviewed for ingest/caching/republication constraints.
- [ ] Adapter contract + replay tests green.
- [ ] Dry run evidence snapshot captured and indexed.
- [ ] Governance approval documented for alpha scope expansion.

### `federal_court_canada`

- [ ] Endpoint reachable and stable over repeated fetch windows.
- [ ] Terms reviewed for ingest/caching/republication constraints.
- [ ] Adapter contract + replay tests green.
- [ ] Dry run evidence snapshot captured and indexed.
- [ ] Governance approval documented for alpha scope expansion.

### `sk_courts_qb_decisions`

- [ ] Endpoint reachable and stable over repeated fetch windows.
- [ ] Terms reviewed for ingest/caching/republication constraints.
- [ ] Adapter contract + replay tests green.
- [ ] Dry run evidence snapshot captured and indexed.
- [ ] Governance approval documented for alpha scope expansion.

### `sk_courts_ca_decisions`

- [ ] Endpoint reachable and stable over repeated fetch windows.
- [ ] Terms reviewed for ingest/caching/republication constraints.
- [ ] Adapter contract + replay tests green.
- [ ] Dry run evidence snapshot captured and indexed.
- [ ] Governance approval documented for alpha scope expansion.

### `sk_legislature_hansard`

- [ ] Endpoint reachable and stable over repeated fetch windows.
- [ ] Terms reviewed for ingest/caching/republication constraints.
- [ ] Adapter contract + replay tests green.
- [ ] Dry run evidence snapshot captured and indexed.
- [ ] Governance approval documented for alpha scope expansion.

## Non-Goals (Alpha Integrity)

- No production-readiness claim is implied by this checklist.
- No source is enabled automatically.
- Evidence, review, and publication guardrails remain unchanged.
