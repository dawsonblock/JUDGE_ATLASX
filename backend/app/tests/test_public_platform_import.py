"""Smoke test: public_platform router must import cleanly with no undefined symbols.

Specifically verifies:
- No AsyncSession or get_async_session references remain in scope.
- All route functions use the sync Session / get_db dependency.
- The module-level import itself does not raise.
"""

from __future__ import annotations

import importlib
import inspect


def test_public_platform_imports():
    """The public_platform module must import without errors."""
    import app.api.routes.public_platform  # noqa: F401 — import is the test


def test_public_platform_no_async_session():
    """AsyncSession must not be imported or referenced in public_platform."""
    import app.api.routes.public_platform as pp

    # Check module's global namespace does not expose AsyncSession
    assert "AsyncSession" not in vars(pp), (
        "public_platform imports or exposes AsyncSession — "
        "all routes must use sync Session with get_db"
    )


def test_public_platform_no_get_async_session():
    """get_async_session must not be imported or referenced in public_platform."""
    import app.api.routes.public_platform as pp

    assert "get_async_session" not in vars(pp), (
        "public_platform imports or exposes get_async_session — "
        "all routes must use get_db"
    )


def test_public_platform_routes_are_sync():
    """All route handler functions in public_platform must be synchronous (not async def)."""
    import app.api.routes.public_platform as pp

    route_fn_names = [
        "get_map_incidents",
        "get_incident_detail",
        "search_statutes",
        "get_statute_detail",
    ]

    for name in route_fn_names:
        fn = getattr(pp, name, None)
        assert fn is not None, f"Expected route function {name!r} not found in public_platform"
        assert not inspect.iscoroutinefunction(fn), (
            f"Route {name!r} is async — all public_platform routes must be sync "
            "for the alpha (uses sync Session / get_db)"
        )
