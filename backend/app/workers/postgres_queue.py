"""PostgreSQL-backed ingestion queue backend.

Provides durable queue semantics with health monitoring and retry logic.
"""
from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.workers.queue_backend import (
    IngestionJobRecord,
    JobState,
    QueueBackendCapabilities,
)
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


class PostgresIngestionQueue:
    """PostgreSQL-backed ingestion queue with durability and retry logic.

    Production-capable backend with health monitoring and automatic retries.
    """

    def __init__(self, dsn: Optional[str] = None) -> None:
        self._dsn = dsn
        self._capabilities = QueueBackendCapabilities(
            name="postgres",
            supports_production=True,
            implementation_status="production_ready",
        )
        self._max_retries = 3
        self._retry_delay_seconds = 60

    def enqueue(self, source_key: str) -> str:
        """Enqueue a source for ingestion."""
        job_id = str(uuid.uuid4())
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            job = IngestionQueueJob(
                job_id=job_id,
                source_key=source_key,
                state=JobState.PENDING.value,
                enqueued_at=datetime.now(timezone.utc),
            )
            db.add(job)
            db.commit()

            logger.info("Enqueued ingestion job %s for source %s", job_id, source_key)
            return job_id
        except Exception as exc:
            db.rollback()
            logger.error("Failed to enqueue job: %s", exc)
            raise
        finally:
            db.close()

    def run_next(self) -> Optional[IngestionJobRecord]:
        """Run the next pending job."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            now = datetime.now(timezone.utc).timestamp()
            job = (
                db.query(IngestionQueueJob)
                .filter(IngestionQueueJob.state == JobState.PENDING.value)
                .filter(
                    (IngestionQueueJob.retry_after.is_(None)) |
                    (IngestionQueueJob.retry_after <= now)
                )
                .order_by(IngestionQueueJob.enqueued_at)
                .first()
            )

            if not job:
                return None

            return self._run_job_internal(job.job_id, db)
        except Exception as exc:
            logger.error("Failed to run next job: %s", exc)
            return None
        finally:
            db.close()

    def run_job(self, job_id: str) -> Optional[IngestionJobRecord]:
        """Run a specific job by ID."""
        db = SessionLocal()

        try:
            return self._run_job_internal(job_id, db)
        except Exception as exc:
            logger.error("Failed to run job %s: %s", job_id, exc)
            return None
        finally:
            db.close()

    def _run_job_internal(self, job_id: str, db: Session) -> Optional[IngestionJobRecord]:
        """Internal job execution logic."""
        from app.models.entities import IngestionQueueJob
        from app.workers.jobs.ingestion_run import run_ingestion_job

        job = db.query(IngestionQueueJob).filter_by(job_id=job_id).first()
        if not job:
            logger.warning("Job %s not found", job_id)
            return None

        if job.state != JobState.PENDING.value:
            logger.info("Job %s is not in pending state: %s", job_id, job.state)
            return self._job_to_record(job)

        # Mark as running
        job.state = JobState.RUNNING.value
        job.started_at = datetime.now(timezone.utc)
        job.retry_count = (job.retry_count or 0) + 1
        db.commit()

        logger.info("Starting ingestion job %s for source %s", job_id, job.source_key)

        try:
            result = run_ingestion_job({"source_key": job.source_key})

            job.finished_at = datetime.now(timezone.utc)
            job.result = result

            if result.get("ok"):
                job.state = JobState.COMPLETED.value
                job.run_id = result.get("run_id")
                job.records_fetched = result.get("records_fetched", 0)
                job.review_items = result.get("review_items", 0)
                job.created_records = result.get("created_records", 0)
                job.raw_snapshot_preserved = result.get("raw_snapshot_preserved", False)
            else:
                job.state = JobState.FAILED.value
                job.error = result.get("message", "Unknown error")

            db.commit()

            logger.info(
                "Ingestion job %s finished: state=%s records=%d",
                job_id,
                job.state,
                job.records_fetched,
            )

            return self._job_to_record(job)

        except Exception as exc:
            logger.exception("Ingestion job %s failed with exception", job_id)

            # Check if we should retry
            if (job.retry_count or 0) < self._max_retries:
                job.state = JobState.PENDING.value
                job.error = f"Retryable error: {str(exc)}"
                job.retry_after = datetime.now(timezone.utc).timestamp() + self._retry_delay_seconds
                db.commit()
                logger.info("Job %s scheduled for retry (attempt %d)", job_id, job.retry_count)
            else:
                job.state = JobState.FAILED.value
                job.finished_at = datetime.now(timezone.utc)
                job.error = f"Max retries exceeded: {str(exc)}"
                db.commit()
                logger.error("Job %s failed after %d retries", job_id, job.retry_count)

            return self._job_to_record(job)

    def get_status(self, job_id: str) -> Optional[IngestionJobRecord]:
        """Get status of a specific job."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            job = db.query(IngestionQueueJob).filter_by(job_id=job_id).first()
            if not job:
                return None

            return self._job_to_record(job)
        finally:
            db.close()

    def list_jobs(self, state: Optional[JobState] = None) -> list[IngestionJobRecord]:
        """List jobs, optionally filtered by state."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            query = db.query(IngestionQueueJob)

            if state is not None:
                query = query.filter(IngestionQueueJob.state == state.value)

            jobs = query.order_by(IngestionQueueJob.enqueued_at.desc()).all()

            return [self._job_to_record(job) for job in jobs]
        finally:
            db.close()

    def pending_count(self) -> int:
        """Get count of pending jobs."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            return (
                db.query(IngestionQueueJob)
                .filter(IngestionQueueJob.state == JobState.PENDING.value)
                .count()
            )
        finally:
            db.close()

    def get_health_status(self) -> dict[str, any]:
        """Get queue health status."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            total_jobs = db.query(IngestionQueueJob).count()
            pending_jobs = (
                db.query(IngestionQueueJob)
                .filter(IngestionQueueJob.state == JobState.PENDING.value)
                .count()
            )
            running_jobs = (
                db.query(IngestionQueueJob)
                .filter(IngestionQueueJob.state == JobState.RUNNING.value)
                .count()
            )
            failed_jobs = (
                db.query(IngestionQueueJob)
                .filter(IngestionQueueJob.state == JobState.FAILED.value)
                .count()
            )

            # Get recent job completion rate
            recent_jobs = (
                db.query(IngestionQueueJob)
                .filter(IngestionQueueJob.finished_at.isnot(None))
                .order_by(IngestionQueueJob.finished_at.desc())
                .limit(100)
                .all()
            )

            completed_recent = sum(1 for job in recent_jobs if job.state == JobState.COMPLETED.value)
            completion_rate = completed_recent / len(recent_jobs) if recent_jobs else 1.0

            return {
                "total_jobs": total_jobs,
                "pending_jobs": pending_jobs,
                "running_jobs": running_jobs,
                "failed_jobs": failed_jobs,
                "completion_rate": completion_rate,
                "healthy": completion_rate >= 0.8 and running_jobs < 10,
            }
        finally:
            db.close()

    def _job_to_record(self, job) -> IngestionJobRecord:
        """Convert database job to record."""
        return IngestionJobRecord(
            job_id=job.job_id,
            source_key=job.source_key,
            state=JobState(job.state),
            enqueued_at=job.enqueued_at.timestamp() if job.enqueued_at else time.time(),
            started_at=job.started_at.timestamp() if job.started_at else None,
            finished_at=job.finished_at.timestamp() if job.finished_at else None,
            run_id=job.run_id,
            records_fetched=job.records_fetched or 0,
            review_items=job.review_items or 0,
            created_records=job.created_records or 0,
            raw_snapshot_preserved=job.raw_snapshot_preserved or False,
            error=job.error,
        )
