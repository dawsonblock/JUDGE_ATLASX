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
        self._stale_lock_threshold_seconds = 300  # 5 minutes
        self._worker_id = f"worker-{uuid.uuid4()}"

    def enqueue_job(self, source_key: str, idempotency_key: Optional[str] = None) -> str:
        """Enqueue a source for ingestion with optional idempotency key."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            # Check for existing job with same idempotency key
            if idempotency_key:
                existing = db.query(IngestionQueueJob).filter(
                    IngestionQueueJob.source_key == source_key,
                    IngestionQueueJob.idempotency_key == idempotency_key
                ).first()
                if existing:
                    logger.info(
                        "Job with idempotency_key %s already exists: %s",
                        idempotency_key, existing.job_id
                    )
                    return existing.job_id

            job_id = str(uuid.uuid4())
            job = IngestionQueueJob(
                job_id=job_id,
                source_key=source_key,
                state=JobState.PENDING.value,
                enqueued_at=datetime.now(timezone.utc),
                idempotency_key=idempotency_key,
            )
            db.add(job)
            db.commit()

            logger.info(
                "Enqueued ingestion job %s for source %s (idempotency_key=%s)",
                job_id, source_key, idempotency_key
            )
            return job_id
        except Exception as exc:
            db.rollback()
            logger.error("Failed to enqueue job: %s", exc)
            raise
        finally:
            db.close()

    def lease_next_job(self, worker_id: str, lease_seconds: int = 300) -> Optional[str]:
        """Lease the next pending job with row-level locking."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob
            from sqlalchemy import text

            # Recover stale locks first
            self.recover_stale_jobs()

            now = datetime.now(timezone.utc).timestamp()
            lease_expires = datetime.now(timezone.utc).timestamp() + lease_seconds

            # Use SELECT FOR UPDATE SKIP LOCKED for safe concurrent job acquisition
            job = db.execute(
                text("""
                    SELECT id FROM ingestion_queue_jobs
                    WHERE state = :pending_state
                    AND (retry_after IS NULL OR retry_after <= :now)
                    AND (locked_by IS NULL OR lease_expires_at IS NULL OR lease_expires_at <= :now)
                    ORDER BY enqueued_at
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                """),
                {
                    "pending_state": JobState.PENDING.value,
                    "now": now,
                }
            ).fetchone()

            if not job:
                return None

            # Load the full job object
            job_obj = db.query(IngestionQueueJob).filter_by(id=job[0]).first()
            if not job_obj:
                return None

            # Acquire lock
            job_obj.locked_by = worker_id
            job_obj.locked_at = datetime.now(timezone.utc)
            job_obj.lease_expires_at = datetime.fromtimestamp(lease_expires, tz=timezone.utc)
            job_obj.state = JobState.RUNNING.value
            job_obj.started_at = datetime.now(timezone.utc)
            db.commit()

            logger.info(
                "Leased job %s to worker %s (expires at %s)",
                job_obj.job_id, worker_id, job_obj.lease_expires_at
            )
            return job_obj.job_id
        except Exception as exc:
            logger.error("Failed to lease next job: %s", exc)
            db.rollback()
            return None
        finally:
            db.close()

    def recover_stale_jobs(self) -> None:
        """Recover locks that have exceeded the lease expiration."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            now = datetime.now(timezone.utc)

            stale_jobs = db.query(IngestionQueueJob).filter(
                IngestionQueueJob.state == JobState.RUNNING.value,
                IngestionQueueJob.lease_expires_at.isnot(None),
                IngestionQueueJob.lease_expires_at < now
            ).all()

            for job in stale_jobs:
                logger.warning(
                    "Recovering stale lock on job %s (locked_by=%s, lease_expires_at=%s)",
                    job.job_id, job.locked_by, job.lease_expires_at
                )
                job.state = JobState.PENDING.value
                job.locked_by = None
                job.locked_at = None
                job.lease_expires_at = None
                job.retry_count = (job.retry_count or 0) + 1

            if stale_jobs:
                db.commit()
                logger.info("Recovered %d stale jobs", len(stale_jobs))
        finally:
            db.close()

    def heartbeat_job(self, job_id: str, worker_id: str) -> bool:
        """Update heartbeat timestamp for a leased job."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            job = db.query(IngestionQueueJob).filter_by(job_id=job_id).first()
            if not job:
                logger.warning("Job %s not found for heartbeat", job_id)
                return False

            if job.locked_by != worker_id:
                logger.warning(
                    "Job %s is not leased by worker %s (locked_by=%s)",
                    job_id, worker_id, job.locked_by
                )
                return False

            job.last_heartbeat_at = datetime.now(timezone.utc)
            db.commit()
            return True
        except Exception as exc:
            logger.error("Failed to heartbeat job %s: %s", job_id, exc)
            db.rollback()
            return False
        finally:
            db.close()

    def complete_job(self, job_id: str, worker_id: str, result: dict) -> bool:
        """Mark a leased job as completed."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            job = db.query(IngestionQueueJob).filter_by(job_id=job_id).first()
            if not job:
                logger.warning("Job %s not found for completion", job_id)
                return False

            if job.locked_by != worker_id:
                logger.warning(
                    "Job %s is not leased by worker %s (locked_by=%s)",
                    job_id, worker_id, job.locked_by
                )
                return False

            job.finished_at = datetime.now(timezone.utc)
            job.result = result
            job.state = JobState.COMPLETED.value
            job.locked_by = None
            job.locked_at = None
            job.lease_expires_at = None
            job.run_id = result.get("run_id")
            job.records_fetched = result.get("records_fetched", 0)
            job.review_items = result.get("review_items", 0)
            job.created_records = result.get("created_records", 0)
            job.raw_snapshot_preserved = result.get("raw_snapshot_preserved", False)
            db.commit()

            logger.info(
                "Job %s completed by worker %s (run_id=%s, records=%d)",
                job_id, worker_id, job.run_id, job.records_fetched
            )
            return True
        except Exception as exc:
            logger.error("Failed to complete job %s: %s", job_id, exc)
            db.rollback()
            return False
        finally:
            db.close()

    def fail_job(self, job_id: str, worker_id: str, error: str) -> bool:
        """Mark a leased job as failed, with retry or DLQ handling."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob

            job = db.query(IngestionQueueJob).filter_by(job_id=job_id).first()
            if not job:
                logger.warning("Job %s not found for failure", job_id)
                return False

            if job.locked_by != worker_id:
                logger.warning(
                    "Job %s is not leased by worker %s (locked_by=%s)",
                    job_id, worker_id, job.locked_by
                )
                return False

            job.error = error
            job.retry_count = (job.retry_count or 0) + 1

            # Check if we should retry
            if job.retry_count < self._max_retries:
                job.state = JobState.PENDING.value
                job.retry_after = datetime.now(timezone.utc).timestamp() + self._retry_delay_seconds
                job.locked_by = None
                job.locked_at = None
                job.lease_expires_at = None
                db.commit()
                logger.info(
                    "Job %s failed by worker %s, scheduled for retry (attempt %d)",
                    job_id, worker_id, job.retry_count
                )
            else:
                job.state = JobState.FAILED.value
                job.finished_at = datetime.now(timezone.utc)
                job.locked_by = None
                job.locked_at = None
                job.lease_expires_at = None
                job.dead_lettered_at = datetime.now(timezone.utc)
                db.commit()

                # Move to dead-letter queue
                self.move_to_dead_letter(job_id)
                logger.error(
                    "Job %s failed after %d retries by worker %s, moved to DLQ",
                    job_id, job.retry_count, worker_id
                )

            return True
        except Exception as exc:
            logger.error("Failed to fail job %s: %s", job_id, exc)
            db.rollback()
            return False
        finally:
            db.close()

    def run_job(self, job_id: str) -> Optional[IngestionJobRecord]:
        """Run a specific job by ID (legacy method for compatibility)."""
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
                job.locked_by = None
                job.locked_at = None
                db.commit()
                logger.info("Job %s scheduled for retry (attempt %d)", job_id, job.retry_count)
            else:
                job.state = JobState.FAILED.value
                job.finished_at = datetime.now(timezone.utc)
                job.error = f"Max retries exceeded: {str(exc)}"
                job.locked_by = None
                job.locked_at = None
                db.commit()
                
                # Move to dead-letter queue
                self._move_to_dead_letter_queue(job, db)
                logger.error("Job %s failed after %d retries, moved to DLQ", job_id, job.retry_count)

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

    def move_to_dead_letter(self, job_id: str) -> bool:
        """Move a failed job to dead-letter queue."""
        db = SessionLocal()

        try:
            from app.models.entities import IngestionQueueJob, DeadLetterQueueJob

            job = db.query(IngestionQueueJob).filter_by(job_id=job_id).first()
            if not job:
                logger.warning("Job %s not found for DLQ", job_id)
                return False

            dlq_job = DeadLetterQueueJob(
                original_job_id=job.job_id,
                source_id=job.source_key,
                job_type="ingestion",
                payload_json={
                    "job_id": job.job_id,
                    "source_key": job.source_key,
                    "retry_count": job.retry_count,
                    "enqueued_at": job.enqueued_at.isoformat() if job.enqueued_at else None,
                },
                final_error=job.error,
                attempt_count=job.retry_count or 0,
                dead_lettered_at=datetime.now(timezone.utc),
            )
            db.add(dlq_job)
            db.commit()
            logger.info("Moved job %s to dead-letter queue", job.job_id)
            return True
        except Exception as exc:
            logger.error("Failed to move job %s to DLQ: %s", job_id, exc)
            db.rollback()
            return False
        finally:
            db.close()
