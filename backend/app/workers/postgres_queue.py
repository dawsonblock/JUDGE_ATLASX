"""PostgreSQL-backed ingestion queue backend placeholder.

This module provides the backend shape only. A real implementation is required
before enabling this backend in production.
"""
from __future__ import annotations

from app.workers.queue_backend import IngestionJobRecord, JobState


class PostgresIngestionQueue:
    """Queue backend interface stub for a future Postgres worker queue."""

    def __init__(self, dsn: str | None = None) -> None:
        self._dsn = dsn

    def _not_implemented(self) -> None:
        raise NotImplementedError(
            "Postgres ingestion queue backend is a placeholder. "
            "Implement durable queue semantics before use."
        )

    def enqueue(self, source_key: str) -> str:
        self._not_implemented()

    def run_next(self) -> IngestionJobRecord | None:
        self._not_implemented()

    def run_job(self, job_id: str) -> IngestionJobRecord | None:
        self._not_implemented()

    def get_status(self, job_id: str) -> IngestionJobRecord | None:
        self._not_implemented()

    def list_jobs(self, state: JobState | None = None) -> list[IngestionJobRecord]:
        self._not_implemented()

    def pending_count(self) -> int:
        self._not_implemented()
