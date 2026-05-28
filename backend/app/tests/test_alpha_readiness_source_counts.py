from __future__ import annotations

from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.models.entities import SourceRegistry


client = TestClient(app)


def _make_source(source_key: str, lifecycle_state: str) -> SourceRegistry:
    return SourceRegistry(
        source_key=source_key,
        source_name=f"Source {source_key}",
        source_type="test",
        lifecycle_state=lifecycle_state,
        source_class="machine_ingest",
        is_active=lifecycle_state == "runnable",
        automation_status="machine_ready_enabled" if lifecycle_state == "runnable" else "machine_ready_disabled",
    )


def test_alpha_readiness_source_lifecycle_counts() -> None:
    keys = [
        "alpha-count-runnable",
        "alpha-count-enable-ready",
        "alpha-count-deprecated",
        "alpha-count-disabled-stub",
        "alpha-count-portal-reference",
    ]

    with SessionLocal() as db:
        db.query(SourceRegistry).filter(SourceRegistry.source_key.in_(keys)).delete(
            synchronize_session=False
        )
        db.add_all(
            [
                _make_source("alpha-count-runnable", "runnable"),
                _make_source("alpha-count-enable-ready", "runnable_disabled"),
                _make_source("alpha-count-deprecated", "deprecated"),
                _make_source("alpha-count-disabled-stub", "disabled_stub"),
                _make_source("alpha-count-portal-reference", "portal_reference"),
            ]
        )
        db.commit()

    try:
        response = client.get("/api/v1/status/alpha-readiness")
        assert response.status_code == 200
        payload = response.json()

        assert payload["runnable_sources"] >= 1
        assert payload["enable_ready_sources"] >= 1
        assert payload["deprecated_sources"] >= 1
    finally:
        with SessionLocal() as db:
            db.query(SourceRegistry).filter(SourceRegistry.source_key.in_(keys)).delete(
                synchronize_session=False
            )
            db.commit()
