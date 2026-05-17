# Dependency Remediation Plan (Frontend Audit)

## Scope

This plan converts alpha triage outcomes into explicit remediation tasks for frontend dependency vulnerabilities.

## Current State

- `npm audit` currently reports 10 vulnerabilities.
- Vulnerabilities are triaged for alpha scope in `docs/security/FRONTEND_SECURITY_TRIAGE.md`.
- Triage is not production remediation.

## Formal Alpha Exception Metadata

- reviewed_on: 2026-05-16
- review_due: 2026-06-30
- exception_expires_on: 2026-07-31
- exception_scope: alpha-only
- production_blocking: true while unresolved high vulnerabilities remain

## Production Gate Rule

No production-readiness claim is allowed while high vulnerabilities remain unresolved, unless a formal security exception is documented and approved.

## Remediation Task Matrix

| Package/Class | Severity | Dependency Path | Alpha Acceptance Reason | Affected Surface | Remediation Option | Owner | Review Due | Exception Expiry | Target Date/Release | Production Gate Status |
|---|---|---|---|---|---|---|---|---|---|---|
| glob | High | eslint-config-next -> @next/eslint-plugin-next -> glob | build-time toolchain only, no runtime CLI `--cmd` usage | lint/build tooling | upgrade via upstream Next.js ecosystem updates | security-review-alpha | 2026-06-30 | 2026-07-31 | before beta gate | blocked until remediated/exception |
| @next/eslint-plugin-next | High | transitive via eslint-config-next | build-time only | lint tooling | upgrade to patched upstream | security-review-alpha | 2026-06-30 | 2026-07-31 | before beta gate | blocked until remediated/exception |
| eslint-config-next | High | direct dev dependency | build-time only | lint tooling | upgrade to patched version | security-review-alpha | 2026-06-30 | 2026-07-31 | before beta gate | blocked until remediated/exception |
| next (runtime advisories set) | High | direct dependency | alpha deployment posture, restricted exposure controls | frontend server runtime | upgrade to patched Next.js release and re-verify exposure | security-review-alpha | 2026-06-30 | 2026-07-31 | before beta gate | blocked until remediated/exception |
| postcss | Moderate | transitive build dependency | build-time css processing only | build pipeline | upgrade transitives via lockfile refresh | security-review-alpha | 2026-06-30 | 2026-07-31 | next dependency refresh window | tracked |
| vitest | Moderate | dev test dependency | CI/local contracts only | test tooling | upgrade vitest and peer deps | security-review-alpha | 2026-06-30 | 2026-07-31 | next dependency refresh window | tracked |
| vite | Moderate | transitive via test/build tooling | tooling only | test/build tooling | upgrade vite ecosystem | security-review-alpha | 2026-06-30 | 2026-07-31 | next dependency refresh window | tracked |
| vite-node | Moderate | transitive via vitest | tooling only | test tooling | upgrade via vitest/vite updates | security-review-alpha | 2026-06-30 | 2026-07-31 | next dependency refresh window | tracked |
| esbuild | Moderate | transitive build dependency | tooling only | build tooling | pin/upgrade to patched range | security-review-alpha | 2026-06-30 | 2026-07-31 | next dependency refresh window | tracked |
| @vitest/mocker | Moderate | transitive via vitest | tooling only | test tooling | upgrade vitest stack | security-review-alpha | 2026-06-30 | 2026-07-31 | next dependency refresh window | tracked |

## Required Update Cadence

- Re-audit `npm audit` at least once per release cycle.
- Update this matrix when advisories change.
- Record remediation completion in PRs that bump dependencies.

## Notes

- This plan does not suppress findings.
- This plan does not imply production-readiness or legal authority.
