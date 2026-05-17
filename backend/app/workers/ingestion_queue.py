"""Ingestion queue backend selector facade.

This module keeps the existing public import path while routing queue access
to the configured backend implementation.
"""
from __future__ import annotations

import threading
from app.core.config import get_settings
from app.workers.inprocess_queue import InProcessIngestionQueue
from app.workers.postgres_queue import PostgresIngestionQueue
from app.workers.queue_backend import IngestionJobRecord, IngestionQueueBackend, JobState


# Module-level singleton queue
_QUEUE: IngestionQueueBackend | None = None
_QUEUE_BACKEND: str | None = None
_QUEUE_LOCK = threading.Lock()


def _build_backend(backend: str) -> IngestionQueueBackend:
    if backend == "inprocess":
        return InProcessIngestionQueue()
    if backend == "postgres":
        return PostgresIngestionQueue()
    raise ValueError(
        "Unsupported ingestion queue backend: "
        f"{backend}. Allowed: inprocess, postgres"
    )


def get_ingestion_queue(settings=None) -> IngestionQueueBackend:
    """Return the process-wide ingestion queue singleton for active backend."""
    global _QUEUE, _QUEUE_BACKEND
    backend = (settings or get_settings()).ingestion_queue_backend
    if _QUEUE is None or _QUEUE_BACKEND != backend:
        with _QUEUE_LOCK:
            if _QUEUE is None or _QUEUE_BACKEND != backend:
                _QUEUE = _build_backend(backend)
                _QUEUE_BACKEND = backend
    return _QUEUE


def _reset_ingestion_queue_for_tests() -> None:
    """Reset singleton queue instance for deterministic backend tests."""
    global _QUEUE, _QUEUE_BACKEND
    with _QUEUE_LOCK:
        _QUEUE = None
        _QUEUE_BACKEND = None


__all__ = [
    "InProcessIngestionQueue",
    "IngestionJobRecord",
    "IngestionQueueBackend",
    "JobState",
    "get_ingestion_queue",
]
