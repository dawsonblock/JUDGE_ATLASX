"""
News Article Linker Service for Public Platform

This service links crime incidents to relevant news articles, providing
citizens with news coverage context and verification of incidents.

Currently uses existing news_article_links data; can be extended to query
external news APIs (NewsAPI, etc.) in the future.

Usage:
    service = NewsIncidentLinker()
    links = await service.link_incident_to_news(
        incident_id="crime-12345",
        incident_title="Assault in Downtown Toronto",
        location="Toronto, ON",
        occurred_at=datetime(2026, 5, 27)
    )
"""

import logging
from datetime import datetime, timedelta

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import IncidentNewsLink

logger = logging.getLogger(__name__)


class NewsIncidentLinker:
    """Links crime incidents to news articles."""

    async def link_incident_to_news(
        self,
        session: AsyncSession,
        incident_id: str,
        incident_title: str,
        location: str,
        occurred_at: datetime | None = None,
        search_window_days: int = 30,
    ) -> list[dict]:
        """
        Link a crime incident to relevant news articles.

        Currently searches existing news_article_links data. In the future,
        could integrate with external news APIs (NewsAPI, etc.).

        Args:
            session: Database session
            incident_id: ID of the crime incident
            incident_title: Title of the incident
            location: Location of the incident
            occurred_at: When the incident occurred
            search_window_days: How many days before/after to search

        Returns:
            List of news article links with metadata
        """
        logger.info(f"[v0] Linking incident {incident_id} to news articles")

        links = []

        try:
            # Phase 1: Search existing news_article_links table
            # This is a placeholder for integration with existing news data
            # In a production system, this would query external news APIs

            # For now, log capability
            logger.info(
                f"[v0] News linking for {incident_id}: "
                f"Location={location}, Window={search_window_days} days"
            )

            # TODO: Implement actual news search:
            # 1. Query external news APIs (NewsAPI, etc.) with incident details
            # 2. Filter by location, date range, keywords
            # 3. Score relevance
            # 4. Persist to incident_news_links table

            # Placeholder: Return empty list until API integration
            return links

        except Exception as e:
            logger.error(
                f"[v0] Error linking incident {incident_id} to news: {str(e)}"
            )
            return []

    async def add_manual_news_link(
        self,
        session: AsyncSession,
        incident_id: str,
        article_title: str,
        article_url: str,
        publication_name: str | None = None,
        published_date: datetime | None = None,
        excerpt: str | None = None,
        relevance_score: float = 0.8,
    ) -> IncidentNewsLink | None:
        """
        Manually link a news article to an incident (for admin use).

        Args:
            session: Database session
            incident_id: ID of the crime incident
            article_title: Title of the news article
            article_url: URL to the article
            publication_name: Name of publication (optional)
            published_date: When article was published (optional)
            excerpt: Brief excerpt from article (optional)
            relevance_score: How relevant is this article (0-1)

        Returns:
            Created IncidentNewsLink or None if error
        """
        logger.info(
            f"[v0] Manually linking news to incident {incident_id}: {article_title}"
        )

        try:
            # Check if link already exists
            existing = await session.execute(
                select(IncidentNewsLink).filter(
                    and_(
                        IncidentNewsLink.incident_id == incident_id,
                        IncidentNewsLink.news_article_url == article_url,
                    )
                )
            )
            if existing.scalars().first():
                logger.info(f"[v0] Link already exists: {incident_id} -> {article_url}")
                return None

            # Create new link
            link = IncidentNewsLink(
                incident_id=incident_id,
                news_article_title=article_title,
                news_article_url=article_url,
                publication_name=publication_name,
                published_date=published_date.date() if published_date else None,
                excerpt=excerpt,
                relevance_score=relevance_score,
                link_method="manual",
            )

            session.add(link)
            await session.commit()

            logger.info(
                f"[v0] Created manual news link for incident {incident_id}"
            )
            return link

        except Exception as e:
            logger.error(
                f"[v0] Error creating manual news link for {incident_id}: {str(e)}"
            )
            await session.rollback()
            return None

    async def get_incident_news(
        self,
        session: AsyncSession,
        incident_id: str,
        limit: int = 10,
    ) -> list[dict]:
        """
        Fetch news articles linked to an incident.

        Args:
            session: Database session
            incident_id: ID of the crime incident
            limit: Maximum number of articles to return

        Returns:
            List of news article data
        """
        try:
            result = await session.execute(
                select(IncidentNewsLink)
                .filter_by(incident_id=incident_id)
                .order_by(IncidentNewsLink.published_date.desc())
                .limit(limit)
            )

            links = result.scalars().all()

            articles = [
                {
                    "id": link.id,
                    "title": link.news_article_title,
                    "url": link.news_article_url,
                    "publication": link.publication_name or "Unknown",
                    "published_date": link.published_date.isoformat()
                    if link.published_date
                    else None,
                    "excerpt": link.excerpt,
                    "relevance_score": link.relevance_score,
                }
                for link in links
            ]

            return articles

        except Exception as e:
            logger.error(
                f"[v0] Error fetching news for incident {incident_id}: {str(e)}"
            )
            return []
