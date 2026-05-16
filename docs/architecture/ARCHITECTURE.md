# Architecture

JUDGE_ATLASX alpha is an evidence-governed legal intelligence runtime with strict review and audit boundaries.

## Runtime Components

- `backend`: ingestion, evidence storage validation, review gates, publication policy, audit logs, auth/RBAC
- `frontend`: operational alpha surfaces only
- `scripts`: proof and boundary validation, release packaging
- `artifacts/current`: canonical proof and release manifests

## Boundary Rules

- runtime code must not import from `external_reference`
- archived experiments are non-runtime
- Docker/release surfaces must exclude reference bundles and caches

## Safety Rules

- evidence is authoritative
- AI and memory are derivative only
- no autonomous accusation/predictive policing semantics
