# Source Registry

This document is the canonical policy reference for source governance in alpha.

## Allowed Source States

- `machine_ingest`
- `portal_reference`
- `manual_upload`
- `disabled_stub`
- `deprecated`

## Machine Ingest Requirements

A source may be `machine_ingest` only when all requirements hold:

- adapter exists in runtime adapter registry
- adapter provides real raw snapshot bytes
- adapter provides fetch URL
- parser version matches registry
- source key matches registry
- replay test exists
- parser contract test exists

## Publication Guardrails

- no public claim without linked evidence snapshot and review state
- evidence is authoritative
- AI/memory outputs are derivative only

See coverage matrix at `docs/source-governance/COVERAGE_MATRIX.md`.
