"""Update queue fields for Phase 3 hardening - Phase 14

Add additional production-grade fields to ingestion_queue_jobs:
- lease_expires_at: When the worker lease expires
- dead_lettered_at: When job was moved to dead-letter queue
- last_heartbeat_at: Last heartbeat timestamp from worker

Update dead_letter_queue_jobs table to match new schema:
- Rename source_key to source_id
- Add job_type field
- Rename failure_reason/error_message to final_error
- Rename original_job_data to payload_json
- Rename retry_count_at_failure to attempt_count
- Remove resolution fields (resolved, resolved_at, resolved_by, resolution_notes)

Revision ID: 20260519_0004
Revises: 20260519_0003
Create Date: 2026-05-19
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260519_0004'
down_revision = '20260519_0003'
branch_labels = None
depends_on = None


def upgrade():
    # Add new fields to ingestion_queue_jobs
    op.add_column('ingestion_queue_jobs', sa.Column('lease_expires_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('ingestion_queue_jobs', sa.Column('dead_lettered_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('ingestion_queue_jobs', sa.Column('last_heartbeat_at', sa.DateTime(timezone=True), nullable=True))
    
    # Update dead_letter_queue_jobs table
    # Rename source_key to source_id
    op.alter_column('dead_letter_queue_jobs', 'source_key', new_column_name='source_id')
    
    # Add new fields
    op.add_column('dead_letter_queue_jobs', sa.Column('job_type', sa.String(80), nullable=False, server_default='ingestion'))
    
    # Rename and consolidate error fields
    op.add_column('dead_letter_queue_jobs', sa.Column('final_error', sa.Text(), nullable=True))
    
    # Rename original_job_data to payload_json
    op.alter_column('dead_letter_queue_jobs', 'original_job_data', new_column_name='payload_json')
    
    # Rename retry_count_at_failure to attempt_count
    op.alter_column('dead_letter_queue_jobs', 'retry_count_at_failure', new_column_name='attempt_count')
    
    # Drop resolution fields
    op.drop_column('dead_letter_queue_jobs', 'resolved')
    op.drop_column('dead_letter_queue_jobs', 'resolved_at')
    op.drop_column('dead_letter_queue_jobs', 'resolved_by')
    op.drop_column('dead_letter_queue_jobs', 'resolution_notes')
    
    # Ensure dead_lettered_at is NOT NULL
    op.alter_column('dead_letter_queue_jobs', 'dead_lettered_at', nullable=False)


def downgrade():
    # Reverse changes to ingestion_queue_jobs
    op.drop_column('ingestion_queue_jobs', 'last_heartbeat_at')
    op.drop_column('ingestion_queue_jobs', 'dead_lettered_at')
    op.drop_column('ingestion_queue_jobs', 'lease_expires_at')
    
    # Reverse changes to dead_letter_queue_jobs
    # Make dead_lettered_at nullable again
    op.alter_column('dead_letter_queue_jobs', 'dead_lettered_at', nullable=True)
    
    # Add back resolution fields
    op.add_column('dead_letter_queue_jobs', sa.Column('resolution_notes', sa.Text(), nullable=True))
    op.add_column('dead_letter_queue_jobs', sa.Column('resolved_by', sa.String(120), nullable=True))
    op.add_column('dead_letter_queue_jobs', sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('dead_letter_queue_jobs', sa.Column('resolved', sa.Boolean(), nullable=False, server_default='false', index=True))
    
    # Rename back
    op.alter_column('dead_letter_queue_jobs', 'attempt_count', new_column_name='retry_count_at_failure')
    op.alter_column('dead_letter_queue_jobs', 'payload_json', new_column_name='original_job_data')
    
    # Drop final_error
    op.drop_column('dead_letter_queue_jobs', 'final_error')
    
    # Drop job_type
    op.drop_column('dead_letter_queue_jobs', 'job_type')
    
    # Rename source_id back to source_key
    op.alter_column('dead_letter_queue_jobs', 'source_id', new_column_name='source_key')
