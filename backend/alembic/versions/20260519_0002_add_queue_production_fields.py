"""Add production-grade queue fields and dead-letter table - Phase 14

Upgrade ingestion_queue_jobs with production-grade concurrency features:
- locked_by (worker identifier for row-level locks)
- locked_at (timestamp for stale lock recovery)
- idempotency_key (unique per source for deduplication)
- Unique constraint on (source_key, idempotency_key)

Create dead_letter_queue_jobs table for failed jobs:
- original_job_id (reference to failed job)
- source_key (source identifier)
- failure_reason (categorization of failure)
- error_message (detailed error)
- original_job_data (snapshot of job at failure)
- retry_count_at_failure (number of retries before DLQ)
- resolved (boolean for tracking resolution)
- resolved_at, resolved_by, resolution_notes (resolution tracking)

Revision ID: 20260519_0002
Revises: 20260519_0001
Create Date: 2026-05-19
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260519_0002'
down_revision = '20260519_0001'
branch_labels = None
depends_on = None


def upgrade():
    # Add production-grade fields to ingestion_queue_jobs
    op.add_column('ingestion_queue_jobs', sa.Column('locked_by', sa.String(120), nullable=True))
    op.add_column('ingestion_queue_jobs', sa.Column('locked_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('ingestion_queue_jobs', sa.Column('idempotency_key', sa.String(255), nullable=True))
    
    # Create indexes for new fields
    op.create_index(op.f('ix_ingestion_queue_jobs_locked_by'), 'ingestion_queue_jobs', ['locked_by'])
    op.create_index(op.f('ix_ingestion_queue_jobs_idempotency_key'), 'ingestion_queue_jobs', ['idempotency_key'])
    
    # Create unique constraint on (source_key, idempotency_key) for idempotency
    op.create_unique_constraint(
        'uq_ingestion_queue_jobs_source_key_idempotency_key',
        'ingestion_queue_jobs',
        ['source_key', 'idempotency_key']
    )
    
    # Create dead_letter_queue_jobs table
    op.create_table(
        'dead_letter_queue_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_job_id', sa.String(64), nullable=False),
        sa.Column('source_key', sa.String(120), nullable=False),
        sa.Column('failure_reason', sa.String(255), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('original_job_data', postgresql.JSON(), nullable=True),
        sa.Column('retry_count_at_failure', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('resolved', sa.Boolean(), nullable=False, server_default=False),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('resolved_by', sa.String(120), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dead_letter_queue_jobs_original_job_id'), 'dead_letter_queue_jobs', ['original_job_id'])
    op.create_index(op.f('ix_dead_letter_queue_jobs_source_key'), 'dead_letter_queue_jobs', ['source_key'])
    op.create_index(op.f('ix_dead_letter_queue_jobs_resolved'), 'dead_letter_queue_jobs', ['resolved'])


def downgrade():
    # Drop dead_letter_queue_jobs table
    op.drop_index(op.f('ix_dead_letter_queue_jobs_resolved'), table_name='dead_letter_queue_jobs')
    op.drop_index(op.f('ix_dead_letter_queue_jobs_source_key'), table_name='dead_letter_queue_jobs')
    op.drop_index(op.f('ix_dead_letter_queue_jobs_original_job_id'), table_name='dead_letter_queue_jobs')
    op.drop_table('dead_letter_queue_jobs')
    
    # Drop unique constraint
    op.drop_constraint('uq_ingestion_queue_jobs_source_key_idempotency_key', 'ingestion_queue_jobs', type_='unique')
    
    # Drop indexes for new fields
    op.drop_index(op.f('ix_ingestion_queue_jobs_idempotency_key'), table_name='ingestion_queue_jobs')
    op.drop_index(op.f('ix_ingestion_queue_jobs_locked_by'), table_name='ingestion_queue_jobs')
    
    # Drop production-grade fields from ingestion_queue_jobs
    op.drop_column('ingestion_queue_jobs', 'idempotency_key')
    op.drop_column('ingestion_queue_jobs', 'locked_at')
    op.drop_column('ingestion_queue_jobs', 'locked_by')
