# Feature Flags

All feature flags default to `false` (disabled). They must be explicitly
enabled via environment variable. No code path is active unless its flag is set.

## JTA_ENABLE_PUBLIC_PLATFORM

Controls whether the public-facing `/public/*` frontend pages and
`/api/v1/public/*` backend routes are registered and reachable.

| Value | Effect |
|-------|--------|
| `false` (default) | Routes are not registered. All `/public/*` requests return 404. |
| `true` | Routes registered. Release policy enforced on every response. |

**Prerequisites before enabling:**
- Human reviewer has approved at least one incident via the admin review queue
- That incident has `publish_status = public_safe` or `public_redacted`
- At least one `StatuteIncidentLink` with `review_status = approved`
- Security team has reviewed `public_release_policy.py`
- Load test completed with representative Saskatchewan dataset

**Environment files to update:**
```
backend/.env
backend/.env.production
frontend/.env.local   (NEXT_PUBLIC_* values only, never secrets)
```

**How to enable locally for testing:**
```bash
# backend/.env
JTA_ENABLE_PUBLIC_PLATFORM=true
```
Then restart the backend. The `/api/v1/status/alpha-readiness` endpoint will
report `public_platform: "enabled"` when the flag is active.

---

## JTA_ENABLE_PUBLIC_REVIEW_GATE

Controls whether human approval is required before incidents appear on the
public map. When disabled, only `publish_status` filtering applies.

**This flag should always remain `true` in any non-developer environment.**

| Value | Effect |
|-------|--------|
| `false` | Review gate bypassed — for local development only. |
| `true` (recommended) | Only `review_status = approved` incidents visible publicly. |

---

## JTA_ENABLE_EXPERIMENTAL_LIVE_MAP

Controls the real-time crime feed overlay on the admin map view.
This feature is not yet stable and should not be enabled in production.

| Value | Effect |
|-------|--------|
| `false` (default) | Live map endpoint disabled. |
| `true` | WebSocket-based live crime feed active. |

---

## JTA_ENABLE_WORKFLOW_ADMIN

Controls the workflow administration UI and API endpoints used for
managing long-running ingestion pipelines.

| Value | Effect |
|-------|--------|
| `false` (default) | Workflow admin routes not registered. |
| `true` | Full workflow admin dashboard available. |

---

## Status Constants

All feature flags are reflected in the alpha readiness endpoint:

```
GET /api/v1/status/alpha-readiness
```

Each flag appears as `"enabled"` or `"disabled"` in the response.
See `backend/app/policies/public_status.py` for the canonical publish-status
values and `backend/app/policies/source_lifecycle.py` for source lifecycle
state constants.

---

## Adding a New Flag

1. Add `your_feature: bool = False` to `backend/app/core/config.py` with a
   `Field(alias="JTA_ENABLE_YOUR_FEATURE")`.
2. Add it to the `AlphaReadinessResponse` in `alpha_status.py`.
3. Add it to `frontend/types/alpha-status.ts`.
4. Document it in this file.
5. Add a test in `backend/app/tests/test_feature_flag_boundaries.py`.
