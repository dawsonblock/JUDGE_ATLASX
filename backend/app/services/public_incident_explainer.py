"""
Incident Explainer Service for Public Platform

This service generates plain-English explanations of crime incidents for
public understanding. It connects incidents to relevant laws and explains
why crimes matter in the context of those laws.

Usage:
    service = IncidentExplainer()
    summary = await service.generate_public_summary(
        incident_id="crime-12345",
        incident_title="Assault in Downtown Toronto",
        crime_type="assault",
        description="Two individuals involved in physical altercation",
        statute_links=[...] # Links to relevant statutes
    )
"""

import logging
from datetime import datetime

from anthropic import Anthropic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import StatuteIncidentLink, LegalSection, GeoLegalEvent
from app.models.geo_legal_event import GeoLegalEvent

logger = logging.getLogger(__name__)

client = Anthropic()


class IncidentExplainer:
    """Generates plain-language explanations of crimes for public understanding."""

    MODEL = "claude-3-5-sonnet-20241022"
    AI_MODEL_VERSION = "1.0"

    async def generate_public_summary(
        self,
        session: AsyncSession,
        incident_id: str,
        incident_title: str,
        crime_type: str,
        description: str,
        location: str,
        occurred_at: datetime | None = None,
    ) -> str:
        """
        Generate a plain-language public summary explaining an incident.

        Args:
            session: Database session
            incident_id: ID of the GeoLegalEvent
            incident_title: Title of the incident
            crime_type: Type of crime
            description: Description of what happened
            location: Where it occurred
            occurred_at: When it occurred

        Returns:
            Plain-language explanation for public viewing
        """
        logger.info(f"[v0] Generating public summary for incident {incident_id}")

        # Fetch linked statutes
        statute_links_result = await session.execute(
            select(StatuteIncidentLink).filter_by(incident_id=incident_id)
        )
        statute_links = statute_links_result.scalars().all()

        statute_context = []
        for link in statute_links[:5]:  # Top 5 most relevant
            section_result = await session.execute(
                select(LegalSection).filter_by(id=link.legal_section_id)
            )
            section = section_result.scalar()
            if section:
                statute_context.append(
                    {
                        "section_label": section.section_label,
                        "marginal_note": section.marginal_note or "",
                        "excerpt": section.text[:200] if section.text else "",
                        "link_reason": link.link_reason,
                    }
                )

        date_str = (
            occurred_at.strftime("%B %d, %Y") if occurred_at else "Unknown date"
        )

        prompt = self._build_explanation_prompt(
            incident_title=incident_title,
            crime_type=crime_type,
            description=description,
            location=location,
            date_str=date_str,
            statute_context=statute_context,
        )

        try:
            message = client.messages.create(
                model=self.MODEL,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )

            summary = message.content[0].text
            logger.debug(f"[v0] Generated summary:\n{summary[:300]}")

            # Save summary to database
            incident_result = await session.execute(
                select(GeoLegalEvent).filter_by(id=incident_id)
            )
            incident = incident_result.scalar()

            if incident:
                incident.public_summary = summary
                await session.commit()
                logger.info(f"[v0] Saved public summary for incident {incident_id}")

            return summary

        except Exception as e:
            logger.error(
                f"[v0] Error generating summary for incident {incident_id}: {str(e)}"
            )
            return ""

    def _build_explanation_prompt(
        self,
        incident_title: str,
        crime_type: str,
        description: str,
        location: str,
        date_str: str,
        statute_context: list,
    ) -> str:
        """Build prompt for Claude to explain incident in plain language."""

        statute_section = ""
        if statute_context:
            statute_section = "RELEVANT CANADIAN LAWS:\n"
            for statute in statute_context:
                statute_section += f"""
- Section {statute['section_label']}: {statute['marginal_note']}
  Why relevant: {statute['link_reason']}
  Text excerpt: {statute['excerpt']}...
"""

        return f"""You are a Canadian legal educator writing for the general public.
Your task is to explain a crime incident and connect it to relevant laws, helping citizens
understand why this crime matters and how it relates to Canadian law.

INCIDENT:
- Title: {incident_title}
- Type: {crime_type}
- Location: {location}
- Date: {date_str}
- Description: {description}

{statute_section}

WRITING GUIDELINES:
1. Use plain, accessible language (avoid legal jargon where possible)
2. Explain what happened in 2-3 sentences
3. Explain which laws are relevant and why
4. Help readers understand the severity and context
5. Be objective and educational, not sensational
6. Keep total length to 3-4 paragraphs

TONE: Informative, respectful, educational. You're helping citizens understand their legal system.

Write the public summary now (3-4 paragraphs, plain language)."""

    async def batch_generate_summaries(
        self,
        session: AsyncSession,
        incident_ids: list[str],
    ) -> dict[str, str]:
        """Generate summaries for multiple incidents. Returns dict of incident_id -> summary."""
        
        results = {}

        for incident_id in incident_ids:
            try:
                incident_result = await session.execute(
                    select(GeoLegalEvent).filter_by(id=incident_id)
                )
                incident = incident_result.scalar()

                if not incident:
                    logger.warning(f"[v0] Incident {incident_id} not found")
                    continue

                # Skip if already has summary
                if incident.public_summary:
                    results[incident_id] = incident.public_summary
                    continue

                summary = await self.generate_public_summary(
                    session=session,
                    incident_id=incident_id,
                    incident_title=incident.title,
                    crime_type=incident.event_type,
                    description=incident.description or "",
                    location=incident.location_name or "",
                    occurred_at=incident.occurred_at,
                )

                results[incident_id] = summary

            except Exception as e:
                logger.error(
                    f"[v0] Error generating summary for {incident_id}: {str(e)}"
                )
                continue

        return results
