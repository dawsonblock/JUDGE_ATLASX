# Runtime Boundaries

Canonical runtime boundary rules for alpha release.

## Allowed Runtime Surface

- `backend`
- `frontend`
- `docs`
- `deploy`
- `scripts`
- `tests`
- `artifacts/current`
- `tools`

## Explicitly Excluded From Runtime

- `external_reference`
- `artifacts/old`
- `artifacts/archive`
- `generated_logs`
- `tmp`
- `cache`
- old phase reports and duplicate status docs

## Enforcement

Validation command:

```bash
python3 scripts/validate_runtime_boundaries.py
```

This validator must pass in CI and proof execution.
