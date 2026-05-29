# Production Preflight

- generated_at: 2026-05-29T01:25:38.772114+00:00
- checks_total: 10
- checks_passed: 2
- checks_failed: 8
- production_preflight_passed: false

## Checks

## Environment Sources

- app_env: JTA_APP_ENV
- backup_policy: unset
- cors_origins: unset
- database_url: unset
- evidence_store_root: unset
- jwt_secret_key: unset
- redis_url: unset

- FAIL production_environment_selected: JTA_APP_ENV=development
- FAIL strong_jwt_secret: JTA_JWT_SECRET_KEY must be set and >= 32 chars, non-default
- PASS legacy_admin_token_disabled: JTA_ENABLE_LEGACY_ADMIN_TOKEN must be false in production
- FAIL redis_rate_limit_configured: JTA_REDIS_URL must be configured
- FAIL evidence_store_root_configured: JTA_EVIDENCE_STORE_ROOT=unset
- FAIL cors_allowlist_not_wildcard: JTA_CORS_ORIGINS=unset
- FAIL egress_proxy_configured: JTA_FETCH_EGRESS_PROXY required unless JTA_ALLOW_DIRECT_FETCH_IN_NON_PROD=true
- FAIL database_url_configured: JTA_DATABASE_URL must be set
- PASS debug_mode_disabled: DEBUG must be false
- FAIL backup_policy_configured: JTA_BACKUP_POLICY must be documented/configured
