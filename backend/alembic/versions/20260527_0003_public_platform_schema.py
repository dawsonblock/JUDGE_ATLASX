"""
Migration: Public Platform Schema

This migration creates the database schema for the public crime understanding platform:
1. Add public_summary field to geo_legal_events for AI-generated plain-language summaries
2. Create statute_incident_links table to link crimes to Canadian statutes
3. Create incident_news_links table to link crimes to news articles

These tables enable the public platform to show citizens:
- Where crimes occur (on map)
- Which laws are relevant (statute links)
- News coverage of incidents (news links)

Revision ID: 20260527_0003
Revises: 20260522_0001
Create Date: 2026-05-27 12:00:00

"""
from alembic import op
import sqlalchemy as sa

revision = '20260527_0003'
down_revision = '20260522_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add public_summary field to geo_legal_events
    op.add_column(
        'geo_legal_events',
        sa.Column(
            'public_summary',
            sa.Text(),
            nullable=True,
            comment='AI-generated plain-English summary for public viewing'
        ),
    )

    # Create statute_incident_links table
    op.create_table(
        'statute_incident_links',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('incident_id', sa.String(64), nullable=False, index=True),
        sa.Column('legal_section_id', sa.Integer(), nullable=False, index=True),
        sa.Column(
            'link_reason',
            sa.Text(),
            nullable=False,
            comment='AI-generated explanation of statute relevance'
        ),
        sa.Column(
            'confidence_score',
            sa.Float(),
            nullable=False,
            server_default='0.5',
            comment='Confidence score (0-1) for statute relevance'
        ),
        sa.Column(
            'ai_model_version',
            sa.String(50),
            nullable=False,
            comment='AI model that generated this link'
        ),
        sa.Column(
            'review_status',
            sa.String(20),
            nullable=False,
            server_default='pending',
            index=True,
            comment='enum: pending, approved, rejected, flagged'
        ),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(
            ['legal_section_id'],
            ['legal_sections.id'],
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'incident_id',
            'legal_section_id',
            name='uq_statute_incident_links_incident_section'
        ),
    )
    op.create_index(
        'idx_statute_incident_links_incident_id',
        'statute_incident_links',
        ['incident_id']
    )
    op.create_index(
        'idx_statute_incident_links_legal_section_id',
        'statute_incident_links',
        ['legal_section_id']
    )
    op.create_index(
        'idx_statute_incident_links_confidence_score',
        'statute_incident_links',
        ['confidence_score']
    )

    # Create incident_news_links table
    op.create_table(
        'incident_news_links',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('incident_id', sa.String(64), nullable=False, index=True),
        sa.Column(
            'news_article_title',
            sa.String(500),
            nullable=False,
            comment='Title of news article'
        ),
        sa.Column(
            'news_article_url',
            sa.String(2048),
            nullable=False,
            comment='URL to news article'
        ),
        sa.Column(
            'publication_name',
            sa.String(255),
            nullable=True,
            comment='e.g., CBC News, The Globe and Mail'
        ),
        sa.Column(
            'published_date',
            sa.Date(),
            nullable=True,
            index=True,
            comment='Date article was published'
        ),
        sa.Column(
            'relevance_score',
            sa.Float(),
            nullable=False,
            server_default='0.5',
            index=True,
            comment='Relevance score (0-1)'
        ),
        sa.Column(
            'excerpt',
            sa.Text(),
            nullable=True,
            comment='Brief excerpt from article'
        ),
        sa.Column(
            'link_method',
            sa.String(50),
            nullable=False,
            server_default='manual',
            comment='How link was established (manual, ai_match, etc.)'
        ),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'incident_id',
            'news_article_url',
            name='uq_incident_news_links_incident_url'
        ),
    )
    op.create_index(
        'idx_incident_news_links_incident_id',
        'incident_news_links',
        ['incident_id']
    )
    op.create_index(
        'idx_incident_news_links_relevance_score',
        'incident_news_links',
        ['relevance_score']
    )
    op.create_index(
        'idx_incident_news_links_published_date',
        'incident_news_links',
        ['published_date']
    )


def downgrade() -> None:
    op.drop_index('idx_incident_news_links_published_date', table_name='incident_news_links')
    op.drop_index('idx_incident_news_links_relevance_score', table_name='incident_news_links')
    op.drop_index('idx_incident_news_links_incident_id', table_name='incident_news_links')
    op.drop_table('incident_news_links')

    op.drop_index('idx_statute_incident_links_confidence_score', table_name='statute_incident_links')
    op.drop_index('idx_statute_incident_links_legal_section_id', table_name='statute_incident_links')
    op.drop_index('idx_statute_incident_links_incident_id', table_name='statute_incident_links')
    op.drop_table('statute_incident_links')

    op.drop_column('geo_legal_events', 'public_summary')
