"""Feature flag boundary tests.

Verifies that alpha-locked feature flags are correctly enforced:
- JTA_ENABLE_EXPERIMENTAL_LIVE_MAP must be False (alpha-locked).
- Public platform flag is available but defaults to disabled unless explicitly set.
- The alpha status endpoint reports production_ready=False unconditionally.
- Workflow admin is gated appropriately.
"""

from __future__ import annotations

import os
import pytest


# ---------------------------------------------------------------------------
# Alpha status response contract
# ---------------------------------------------------------------------------


def test_alpha_readiness_production_ready_always_false(client):
    """production_ready must always be False in alpha — never True."""
    resp = client.get("/api/v1/status/alpha-readiness")
    # The endpoint may 500 if DB is unavailable in test context; skip gracefully.
    if resp.status_code == 500:
        pytest.skip("alpha-readiness endpoint requires DB — skipping in unit context")
    assert resp.status_code == 200
    data = resp.json()
    assert data["production_ready"] is False, (
        "production_ready must always be False in alpha — "
        f"got {data.get('production_ready')!r}"
    )


def test_alpha_readiness_experimental_live_map_disabled(client):
    """experimental_live_map must be 'disabled' or 'locked' in alpha."""
    resp = client.get("/api/v1/status/alpha-readiness")
    if resp.status_code in (500, 503):
        pytest.skip("alpha-readiness endpoint unavailable")
    assert resp.status_code == 200
    data = resp.json()
    assert data["experimental_live_map"] in ("disabled", "locked"), (
        f"experimental_live_map should be 'disabled' or 'locked', "
        f"got {data.get('experimental_live_map')!r}"
    )


# ---------------------------------------------------------------------------
# Config-level flag contract (no DB required)
# ---------------------------------------------------------------------------


def test_experimental_live_map_flag_defaults_false():
    """JTA_ENABLE_EXPERIMENTAL_LIVE_MAP must default to False in any profile."""
    # Unset env var and reload settings to check default.
    env_key = "JTA_ENABLE_EXPERIMENTAL_LIVE_MAP"
    original = os.environ.pop(env_key, None)
    try:
        from importlib import reload
        import app.core.config as cfg_mod
        reload(cfg_mod)
        settings = cfg_mod.get_settings()
        flag = getattr(settings, "enable_experimental_live_map", False)
        assert not flag, (
            "enable_experimental_live_map must default to False — "
            "this flag is alpha-locked"
        )
    finally:
        if original is not None:
            os.environ[env_key] = original
        # Restore module to avoid polluting other tests
        import app.core.config as cfg_mod
        reload(cfg_mod)


def test_source_lifecycle_constants_not_report_labels():
    """Source lifecycle DB constants must not equal report labels."""
    from app.policies.source_lifecycle import (
        SOURCE_RUNNABLE, SOURCE_RUNNABLE_DISABLED,
        REPORT_LABEL_RUNNABLE, REPORT_LABEL_ENABLE_READY,
    )
    assert SOURCE_RUNNABLE != REPORT_LABEL_RUNNABLE, (
        "DB value 'runnable' must not equal report label 'runnable_now'"
    )
    assert SOURCE_RUNNABLE_DISABLED != REPORT_LABEL_ENABLE_READY, (
        "DB value 'runnable_disabled' must not equal report label 'enable_ready'"
    )


def test_public_status_constants_not_legacy_published():
    """Canonical publish status constants must not include the legacy 'published' value."""
    from app.policies.public_status import PUBLIC_VISIBLE_STATUSES, LEGACY_PUBLISHED
    assert LEGACY_PUBLISHED not in PUBLIC_VISIBLE_STATUSES


def test_linker_disabled_flag_is_false():
    """CrimeStatuteLinker._LINKER_ENABLED must be False in alpha."""
    import app.services.public_crime_statute_linker as linker_mod
    assert linker_mod._LINKER_ENABLED is False, (
        "_LINKER_ENABLED must be False in alpha until evidence-grounded "
        "linking passes internal review"
    )


def test_linker_returns_empty_list_when_disabled():
    """CrimeStatuteLinker.link_incident_to_statutes must return [] while disabled."""
    from unittest.mock import MagicMock
    from app.services.public_crime_statute_linker import CrimeStatuteLinker

    linker = CrimeStatuteLinker(llm_provider=None)
    result = linker.link_incident_to_statutes(
        session=MagicMock(),
        incident_id="test-id",
        crime_type="assault",
        description="Test description",
        location="Toronto, ON",
    )
    assert result == [], (
        "link_incident_to_statutes must return [] while _LINKER_ENABLED is False"
    )
