"""Add geocode_cache_id foreign key to locations table.

Adds a foreign key column to link locations to cached geocoding results.
This enables tracking the geocoding status and quality for each location.

Revision ID: 20260520_0003
Revises: 20260520_0002
Create Date: 2026-05-20
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260520_0003'
down_revision = '20260520_0002'
branch_labels = None
depends_on = None


def upgrade():
    # Add geocode_cache_id column to locations table
    op.add_column(
        'locations',
        sa.Column('geocode_cache_id', sa.Integer(), nullable=True)
    )
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_locations_geocode_cache_id',
        'locations',
        'geocode_cache',
        ['geocode_cache_id'],
        ['id']
    )
    
    # Create index for faster lookups
    op.create_index(
        'idx_locations_geocode_cache_id',
        'locations',
        ['geocode_cache_id']
    )


def downgrade():
    # Drop index
    op.drop_index('idx_locations_geocode_cache_id', table_name='locations')
    
    # Drop foreign key constraint
    op.drop_constraint(
        'fk_locations_geocode_cache_id',
        'locations',
        type_='foreignkey'
    )
    
    # Drop column
    op.drop_column('locations', 'geocode_cache_id')
