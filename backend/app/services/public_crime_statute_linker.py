"""
Crime-to-Statute Linking Service for Public Platform

This service uses an LLM (via abstracted provider) to automatically link crime 
incidents to relevant Canadian federal statutes. Each link includes a confidence 
score and explanation of why the statute is relevant to the specific crime.

Usage:
    service = CrimeStatuteLinker(llm_provider)
    links = service.link_incident_to_statutes(
        session=db_session,
        incident_id="crime-12345",
        crime_type="assault",
        description="Physical altercation...",
        location="Toronto, ON"
    )
"""

import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import LegalInstrument, LegalSection, StatuteIncidentLink
from app.db.session import get_db
from app.services.public_link_statuses import LINK_REVIEW_STATUS_PENDING
from app.llm.provider import LLMProvider
from app.llm.schemas import LLMRequest, TaskType

logger = logging.getLogger(__name__)


class CrimeStatuteLinker:
    """Links crimes to relevant Canadian statutes using an LLM provider."""

    AI_MODEL_VERSION = "1.0"

    def __init__(self, llm_provider: LLMProvider):
        """Initialize with an LLM provider.

        Args:
            llm_provider: Configured LLMProvider instance (e.g., OpenAI, Ollama)
        """
        self.llm = llm_provider
        logger.info(f"[v0] CrimeStatuteLinker initialized with {self.llm.provider_name}")

    def link_incident_to_statutes(
        self,
        session: Session,
        incident_id: str,
        crime_type: str,
        description: str,
        location: str,
        occurred_at: datetime | None = None,
    ) -> list[dict]:
        """
        Link a crime incident to relevant Canadian statutes.

        Args:
            session: Database session
            incident_id: ID of the GeoLegalEvent (crime incident)
            crime_type: Type of crime (e.g., "assault", "theft", "murder")
            description: Plain-language description of the incident
            location: Where the crime occurred
            occurred_at: When the crime occurred

        Returns:
            List of statute links with confidence scores and explanations
        """
        logger.info(
            f"[v0] Linking incident {incident_id} ({crime_type}) to Canadian statutes"
        )

        # Fetch all Canadian federal statutes from database
        result = session.execute(
            select(LegalInstrument).filter_by(jurisdiction="CA", public_visibility="public")
        )
        statutes = result.scalars().all()

        if not statutes:
            logger.warning("[v0] No Canadian statutes found in database")
            return []

        # Build statute reference list for AI
        statute_refs = []
        for statute in statutes[:50]:  # Limit to first 50 for token budget
            statute_refs.append(
                {
                    "id": statute.id,
                    "title": statute.title or statute.short_title or "Unknown",
                    "citation": statute.citation or "",
                    "sections": [
                        {
                            "id": section.id,
                            "label": section.section_label,
                            "title": section.marginal_note or "",
                        }
                        for section in statute.sections[:3]  # First 3 sections only
                    ],
                }
            )

        # Call Claude to identify relevant statutes
        prompt = self._build_linking_prompt(
            crime_type=crime_type,
            description=description,
            location=location,
            occurred_at=occurred_at,
            statute_refs=statute_refs,
        )

        try:
            message = client.messages.create(
                model=self.MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            logger.debug(f"[v0] Claude response:\n{response_text[:500]}")

            # Parse AI response and create database records
            links = await self._parse_and_persist_links(
                session=session,
                incident_id=incident_id,
                response_text=response_text,
                statute_refs=statute_refs,
            )

            return links

        except Exception as e:
            logger.error(f"[v0] Error linking incident {incident_id}: {str(e)}")
            return []

    def _build_linking_prompt(
        self,
        crime_type: str,
        description: str,
        location: str,
        occurred_at: datetime | None,
        statute_refs: list,
    ) -> str:
        """Build the prompt for Claude to identify relevant statutes."""
        
        date_str = occurred_at.strftime("%Y-%m-%d") if occurred_at else "Unknown date"
        
        statute_list = "\n".join(
            [
                f"  - {s['citation']}: {s['title']}\n"
                + "".join(
                    [
                        f"    * Section {sec['label']}: {sec['title']}\n"
                        for sec in s["sections"]
                    ]
                )
                for s in statute_refs[:30]  # Limit to 30 statutes in prompt
            ]
        )

        return f"""You are a Canadian legal expert analyzing a crime incident to identify relevant federal statutes.

INCIDENT DETAILS:
- Type: {crime_type}
- Location: {location}
- Date: {date_str}
- Description: {description}

CANADIAN FEDERAL STATUTES (Criminal Code, etc.):
{statute_list}

TASK:
1. Identify which statutes are DIRECTLY relevant to this crime
2. For each relevant statute, explain WHY it's relevant
3. Rate confidence (0-100) for each match
4. Return ONLY JSON, no other text

RESPONSE FORMAT (valid JSON only):
{{
  "links": [
    {{
      "statute_citation": "Criminal Code s. 235",
      "section_id": <numeric_id>,
      "confidence": 95,
      "reason": "This statute defines murder, which directly applies to this homicide case."
    }}
  ]
}}

Return ONLY the JSON object, no markdown, no explanation."""

    async def _parse_and_persist_links(
        self,
        session: AsyncSession,
        incident_id: str,
        response_text: str,
        statute_refs: list,
    ) -> list[dict]:
        """Parse AI response and save statute links to database."""
        
        links = []

        try:
            # Clean response (remove markdown code blocks if present)
            json_text = response_text.strip()
            if json_text.startswith("```"):
                json_text = json_text.split("```")[1]
                if json_text.startswith("json"):
                    json_text = json_text[4:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]

            import json

            parsed = json.loads(json_text.strip())

            for link_data in parsed.get("links", []):
                try:
                    # Find the section in database
                    section_id = link_data.get("section_id")
                    confidence = link_data.get("confidence", 0) / 100.0  # Convert to 0-1
                    reason = link_data.get("reason", "")

                    if not section_id or confidence < 0.3:
                        continue  # Skip low-confidence links

                    # Check if link already exists
                    existing = await session.execute(
                        select(StatuteIncidentLink).filter_by(
                            incident_id=incident_id, legal_section_id=section_id
                        )
                    )
                    if existing.scalars().first():
                        continue  # Already exists

                    # Create new link
                    link = StatuteIncidentLink(
                        incident_id=incident_id,
                        legal_section_id=section_id,
                        link_reason=reason,
                        confidence_score=confidence,
                        ai_model_version=self.AI_MODEL_VERSION,
                        review_status=LINK_REVIEW_STATUS_PENDING,
                    )
                    session.add(link)
                    links.append(
                        {
                            "incident_id": incident_id,
                            "section_id": section_id,
                            "confidence": confidence,
                            "reason": reason,
                        }
                    )

                except Exception as e:
                    logger.warning(f"[v0] Error processing link: {str(e)}")
                    continue

            await session.commit()
            logger.info(f"[v0] Created {len(links)} statute links for incident {incident_id}")

        except Exception as e:
            logger.error(
                f"[v0] Error parsing AI response for incident {incident_id}: {str(e)}"
            )
            await session.rollback()

        return links
