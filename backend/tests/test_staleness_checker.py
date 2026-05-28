"""Tests for the staleness checker job."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.jobs.staleness_checker import (
    DEFAULT_FRESHNESS_WINDOW_DAYS,
    PUBLISH_STATUS_PUBLISHED,
    PUBLISH_STATUS_STALE,
    StalenessReport,
    _get_last_seen,
    run_staleness_check,
)


def _make_event(
    id: int = 1,
    publish_status: str = PUBLISH_STATUS_PUBLISHED,
    updated_at: datetime | None = None,
) -> MagicMock:
    ev = MagicMock()
    ev.id = id
    ev.publish_status = publish_status
    ev.updated_at = updated_at
    ev.created_at = updated_at
    return ev


class TestGetLastSeen:
    def test_returns_updated_at_when_set(self):
        ev = _make_event(updated_at=datetime(2024, 6, 1, tzinfo=timezone.utc))
        result = _get_last_seen(ev)
        assert result == datetime(2024, 6, 1, tzinfo=timezone.utc)

    def test_returns_none_when_no_timestamps(self):
        ev = MagicMock()
        ev.updated_at = None
        ev.created_at = None
        result = _get_last_seen(ev)
        assert result is None

    def test_makes_naive_datetime_timezone_aware(self):
        ev = _make_event(updated_at=datetime(2024, 6, 1))  # naive
        result = _get_last_seen(ev)
        assert result is not None
        assert result.tzinfo is not None


class TestRunStalenessCheck:
    def _make_session(self, events: list) -> MagicMock:
        session = MagicMock()
        session.execute.return_value.scalars.return_value.all.return_value = events
        return session

    def test_fresh_events_are_not_marked_stale(self):
        fresh_time = datetime.now(timezone.utc) - timedelta(days=5)
        ev = _make_event(id=1, updated_at=fresh_time)
        session = self._make_session([ev])

        report = run_staleness_check(session, dry_run=True)

        assert report.still_fresh == 1
        assert report.newly_stale == 0
        assert ev.publish_status == PUBLISH_STATUS_PUBLISHED

    def test_old_events_are_marked_stale(self):
        stale_time = datetime.now(timezone.utc) - timedelta(days=DEFAULT_FRESHNESS_WINDOW_DAYS + 5)
        ev = _make_event(id=2, updated_at=stale_time)
        session = self._make_session([ev])

        report = run_staleness_check(session, dry_run=True)

        assert report.newly_stale == 1
        assert 2 in report.stale_ids

    def test_dry_run_does_not_commit(self):
        stale_time = datetime.now(timezone.utc) - timedelta(days=60)
        ev = _make_event(id=3, updated_at=stale_time)
        session = self._make_session([ev])

        run_staleness_check(session, dry_run=True)

        session.commit.assert_not_called()

    def test_non_dry_run_commits(self):
        fresh_time = datetime.now(timezone.utc) - timedelta(days=1)
        ev = _make_event(id=4, updated_at=fresh_time)
        session = self._make_session([ev])

        run_staleness_check(session, dry_run=False)

        session.commit.assert_called_once()

    def test_already_stale_events_counted_separately(self):
        stale_time = datetime.now(timezone.utc) - timedelta(days=60)
        ev = _make_event(id=5, publish_status=PUBLISH_STATUS_STALE, updated_at=stale_time)
        session = self._make_session([ev])

        report = run_staleness_check(session, dry_run=True)

        assert report.already_stale == 1
        assert report.newly_stale == 0

    def test_no_events_returns_zero_report(self):
        session = self._make_session([])

        report = run_staleness_check(session, dry_run=True)

        assert report.total_checked == 0
        assert report.newly_stale == 0
        assert report.stale_ids == []

    def test_event_with_no_timestamp_is_marked_stale(self):
        ev = _make_event(id=6, updated_at=None)
        ev.created_at = None
        session = self._make_session([ev])

        report = run_staleness_check(session, dry_run=True)

        assert report.newly_stale == 1
