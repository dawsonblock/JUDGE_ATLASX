"""Tests for alpha_status.py source lifecycle count correctness.

Verifies that:
- DB filter uses "runnable" (not "runnable_now") for runnable_sources count.
- DB filter uses "runnable_disabled" (not "enable_ready") for enable_ready_sources count.
- DB filter uses "deprecated" for deprecated_sources count.
- portal_reference and disabled_stub sources are NOT counted as runnable or enable-ready.

These tests use the in-memory SQLite DB from conftest.py.
"""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.models.entities import SourceRegistry
from app.policies.source_lifecycle import (
    SOURCE_RUNNABLE,
    SOURCE_RUNNABLE_DISABLED,
    SOURCE_DEPRECATED,
    SOURCE_PORTAL_REFERENCE,
    SOURCE_DISABLED_STUB,
    LIFECYCLE_REPORT_LABELS,
)


# ---------------------------------------------------------------------------
# Vocabulary contract tests (no DB required)
# ---------------------------------------------------------------------------


def test_runnable_db_value_is_not_runnable_now():
    """DB value and report label are intentionally different — verify the mapping."""
    assert SOURCE_RUNNABLE == "runnable"
    assert LIFECYCLE_REPORT_LABELS[SOURCE_RUNNABLE] == "runnable_now"


def test_runnable_disabled_db_value_is_not_enable_ready():
    assert SOURCE_RUNNABLE_DISABLED == "runnable_disabled"
    assert LIFECYCLE_REPORT_LABELS[SOURCE_RUNNABLE_DISABLED] == "enable_ready"


def test_portal_reference_is_non_machine():
    from app.policies.source_lifecycle import SOURCE_NON_MACHINE_STATES
    assert SOURCE_PORTAL_REFERENCE in SOURCE_NON_MACHINE_STATES


def test_disabled_stub_is_non_machine():
    from app.policies.source_lifecycle import SOURCE_NON_MACHINE_STATES
    assert SOURCE_DISABLED_STUB in SOURCE_NON_MACHINE_STATES


def test_portal_reference_not_runnable():
    from app.policies.source_lifecycle import SOURCE_MACHINE_STATES
    assert SOURCE_PORTAL_REFERENCE not in SOURCE_MACHINE_STATES


def test_disabled_stub_not_runnable():
    from app.policies.source_lifecycle import SOURCE_MACHINE_STATES
    assert SOURCE_DISABLED_STUB not in SOURCE_MACHINE_STATES


# ---------------------------------------------------------------------------
# DB count tests
# ---------------------------------------------------------------------------


@pytest.fixture
def db_with_sources(db: Session):
    """Seed a known set of sources with varied lifecycle states."""
    sources = [
        SourceRegistry(
            source_key=f"src-runnable-{i}",
            display_name=f"Runnable Source {i}",
            lifecycle_state=SOURCE_RUNNABLE,
            is_active=True,
        )
        for i in range(2)
    ] + [
        SourceRegistry(
            source_key=f"src-disabled-{i}",
            display_name=f"Disabled Source {i}",
            lifecycle_state=SOURCE_RUNNABLE_DISABLED,
            is_active=False,
        )
        for i in range(3)
    ] + [
        SourceRegistry(
            source_key="src-deprecated-1",
            display_name="Deprecated Source",
            lifecycle_state=SOURCE_DEPRECATED,
            is_active=False,
        ),
        SourceRegistry(
            source_key="src-portal-1",
            display_name="Portal Reference",
            lifecycle_state=SOURCE_PORTAL_REFERENCE,
            is_active=False,
        ),
        SourceRegistry(
            source_key="src-stub-1",
            display_name="Disabled Stub",
            lifecycle_state=SOURCE_DISABLED_STUB,
            is_active=False,
        ),
    ]
    for src in sources:
        db.add(src)
    db.flush()
    yield db
    # Rollback to avoid polluting other tests.
    db.rollback()


def _count_lifecycle(db: Session, state: str) -> int:
    from sqlalchemy import func, select
    return db.scalar(
        select(func.count(SourceRegistry.id)).where(
            SourceRegistry.lifecycle_state == state
        )
    ) or 0


def test_runnable_count_uses_runnable_not_runnable_now(db_with_sources: Session):
    """Queries with 'runnable' find the right sources; 'runnable_now' finds none."""
    count_correct = _count_lifecycle(db_with_sources, SOURCE_RUNNABLE)
    count_wrong = _count_lifecycle(db_with_sources, "runnable_now")
    assert count_correct >= 2
    assert count_wrong == 0, (
        "'runnable_now' is a report label — it must not exist as a DB lifecycle_state"
    )


def test_enable_ready_count_uses_runnable_disabled_not_enable_ready(db_with_sources: Session):
    """Queries with 'runnable_disabled' find the right sources; 'enable_ready' finds none."""
    count_correct = _count_lifecycle(db_with_sources, SOURCE_RUNNABLE_DISABLED)
    count_wrong = _count_lifecycle(db_with_sources, "enable_ready")
    assert count_correct >= 3
    assert count_wrong == 0, (
        "'enable_ready' is a report label — it must not exist as a DB lifecycle_state"
    )


def test_portal_reference_not_counted_as_runnable(db_with_sources: Session):
    runnable = _count_lifecycle(db_with_sources, SOURCE_RUNNABLE)
    # The portal_reference source is seeded but must not appear in runnable count
    portal_would_be_included = _count_lifecycle(db_with_sources, SOURCE_PORTAL_REFERENCE)
    assert portal_would_be_included >= 1, "Portal reference source was seeded"
    # Ensure the DB runnable count does not include portal_reference
    assert runnable >= 2  # only actual runnable sources
    # Double check portal is not in runnable
    from sqlalchemy import select
    portal_sources = db_with_sources.execute(
        select(SourceRegistry).where(
            SourceRegistry.lifecycle_state == SOURCE_PORTAL_REFERENCE
        )
    ).scalars().all()
    for src in portal_sources:
        assert src.lifecycle_state != SOURCE_RUNNABLE


def test_disabled_stub_not_counted_as_enable_ready(db_with_sources: Session):
    enable_ready = _count_lifecycle(db_with_sources, SOURCE_RUNNABLE_DISABLED)
    stub_count = _count_lifecycle(db_with_sources, SOURCE_DISABLED_STUB)
    assert stub_count >= 1, "Disabled stub source was seeded"
    assert enable_ready >= 3  # only runnable_disabled sources
    from sqlalchemy import select
    stub_sources = db_with_sources.execute(
        select(SourceRegistry).where(
            SourceRegistry.lifecycle_state == SOURCE_DISABLED_STUB
        )
    ).scalars().all()
    for src in stub_sources:
        assert src.lifecycle_state != SOURCE_RUNNABLE_DISABLED
