"""
Migration: Phase 3 - Ingestion Hardening (Adapter Contracts + Immutability Triggers)

This migration:
1. Creates source_adapter_contracts table (registry of parser_version schemas)
2. Adds trigger on source_snapshots to prevent UPDATE (immutability)
3. Adds trigger on audit_logs to prevent UPDATE and DELETE (append-only)
4. Creates indices for contract lookup and validation

Revision ID: 20260516_0003
Revises: 20260516_0002
Create Date: 2026-05-16 19:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '20260516_0003'
down_revision = '20260516_0002'
branch_labels = None
depends_on = None


def upgrade():
    """Apply Phase 3: Adapter contracts + immutability triggers."""
    
    # 1. Create source_adapter_contracts table
    op.create_table(
        'source_adapter_contracts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_key', sa.String(100), nullable=False, index=True),
        sa.Column('parser_version', sa.String(20), nullable=False, index=True),
        sa.Column('adapter_class', sa.String(120), nullable=False),
        sa.Column('schema_hash', sa.String(64), nullable=False),
        sa.Column('required_fields', postgresql.JSON(), nullable=True),
        sa.Column('output_types', postgresql.JSON(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, index=True, server_default='active'),
        sa.Column('deprecated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('successor_version', sa.String(20), nullable=True),
        sa.Column('validation_rules', postgresql.JSON(), nullable=True),
        sa.Column('documentation_url', sa.String(2048), nullable=True),
        sa.Column('created_by', sa.String(120), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )
    
    op.create_index(
        'ix_source_adapter_contracts_source_key_parser_version',
        'source_adapter_contracts',
        ['source_key', 'parser_version'],
        unique=True,
    )
    
    # 2. Create trigger function to prevent UPDATE on source_snapshots
    op.execute("""
    CREATE OR REPLACE FUNCTION prevent_source_snapshot_update()
    RETURNS TRIGGER AS $$
    BEGIN
        RAISE EXCEPTION 'SourceSnapshot is immutable: UPDATE not allowed (id=%)', OLD.id;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # 3. Create trigger on source_snapshots to enforce immutability
    op.execute("""
    CREATE TRIGGER source_snapshot_immutable_trigger
    BEFORE UPDATE ON source_snapshots
    FOR EACH ROW
    EXECUTE FUNCTION prevent_source_snapshot_update();
    """)
    
    # 4. Create trigger function to prevent UPDATE and DELETE on audit_logs
    op.execute("""
    CREATE OR REPLACE FUNCTION prevent_audit_log_modification()
    RETURNS TRIGGER AS $$
    BEGIN
        IF TG_OP = 'UPDATE' THEN
            RAISE EXCEPTION 'AuditLog is append-only: UPDATE not allowed (id=%)', OLD.id;
        ELSIF TG_OP = 'DELETE' THEN
            RAISE EXCEPTION 'AuditLog is append-only: DELETE not allowed (id=%)', OLD.id;
        END IF;
        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # 5. Create trigger on audit_logs to enforce append-only
    op.execute("""
    CREATE TRIGGER audit_log_append_only_trigger
    BEFORE UPDATE OR DELETE ON audit_logs
    FOR EACH ROW
    EXECUTE FUNCTION prevent_audit_log_modification();
    """)


def downgrade():
    """Rollback Phase 3: Adapter contracts + immutability triggers."""
    
    # Remove triggers
    op.execute("DROP TRIGGER IF EXISTS source_snapshot_immutable_trigger ON source_snapshots;")
    op.execute("DROP TRIGGER IF EXISTS audit_log_append_only_trigger ON audit_logs;")
    
    # Remove trigger functions
    op.execute("DROP FUNCTION IF EXISTS prevent_source_snapshot_update();")
    op.execute("DROP FUNCTION IF EXISTS prevent_audit_log_modification();")
    
    # Remove source_adapter_contracts table
    op.drop_index('ix_source_adapter_contracts_source_key_parser_version', table_name='source_adapter_contracts')
    op.drop_table('source_adapter_contracts')
