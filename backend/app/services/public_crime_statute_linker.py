"""
Crime-to-Statute Candidate Linking Service (Alpha — Disabled)

Alpha status: DISABLED. This service is syntactically valid and importable
but returns [] for all calls until evidence-grounded linking is implemented
and passes internal review.

Rationale:
- LLM-inferred statute applicability from free-text incident descriptions
  alone does not meet the evidence-grounded standard required for legal/crime
  data.
- Any StatuteIncidentLink this service creates must have
  review_status=LINK_REVIEW_STATUS_PENDING and must never appear in a
  public API response without human approval.
- This service must never publish statute conclusions.

When re-enabled, this service must:
1. Verify reviewed evidence exists for the incident before running.
2. Use LLMProvider (not a direct Anthropic/OpenAI client) via ReviewerAssistant.
3. Import LLMTaskType (not TaskType) from app.llm.schemas.
4. Be fully synchronous — use sqlalchemy.orm.Session, not AsyncSession.
5. Set every link to review_status=LINK_REVIEW_STATUS_PENDING only.
"""

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.services.public_link_statuses import LINK_REVIEW_STATUS_PENDING

logger = logging.getLogger(__name__)

# Alpha guard — set to True only after evidence-grounded implementation
# has passed internal review and boundary tests.
_LINKER_ENABLED = False


class CrimeStatuteLinker:
    """
    Candidate linker: crime incidents -> Canadian federal statute sections.

    Alpha status: disabled. All calls return [] until evidence-grounded
    linking passes internal review.

    When enabled this service produces pending-review candidates only:
    - review_status is always LINK_REVIEW_STATUS_PENDING on every link.
    - No link is ever published or exposed to any public API by this service.
    - Human review via the admin queue is required before any link is visible.
    """

    AI_MODEL_VERSION = "1.0"

    def __init__(self, llm_provider=None):
        """
        Accept an optional LLM provider for future use.

        Args:
            llm_provider: LLMProvider instance (unused while alpha-disabled).
        """
        self.llm = llm_provider
        if _LINKER_ENABLED:
            logger.info(
                "[v0] CrimeStatuteLinker initialized — ENABLED "
                "(produces pending candidates only)"
            )
        else:
            logger.info(
                "[v0] CrimeStatuteLinker initialized — DISABLED in alpha "
                "(returns [] for all calls)"
            )

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
        Return candidate statute links for admin review.

        Alpha: always returns [].
        Re-enable only after evidence-grounded implementation and proof review.

        Returns:
            list[dict] — always [] while _LINKER_ENABLED is False.
        """
        if not _LINKER_ENABLED:
            logger.warning(
                "[v0] CrimeStatuteLinker is disabled in alpha until "
                "evidence-grounded linking is implemented and reviewed. "
                "Returning []."
            )
            return []

        # Unreachable in alpha — implementation placeholder only.
        # Steps required when re-enabling:
        # 1. Verify incident has reviewed evidence via session query.
        # 2. Fetch statutes with session.execute(...) — no await.
        # 3. Build prompt via _build_linking_prompt().
        # 4. Call self.llm.complete(...) via ReviewerAssistant boundary.
        # 5. Parse response and call _parse_and_persist_links(session, ...).
        # 6. Never set any link review_status to "approved" here.
        logger.error(
            "[v0] CrimeStatuteLinker._LINKER_ENABLED is True but "
            "implementation is not complete. This path must not be reached."
        )
        return []

    def _build_linking_prompt(
        self,
        crime_type: str,
        description: str,
        location: str,
        occurred_at: datetime | None,
        statute_refs: list,
    ) -> str:
        """
        Build a candidate-linking prompt (kept for test reference only).

        This method does NOT call any LLM. It constructs a prompt string
        for use when the linker is re-enabled under the LLMProvider /
        ReviewerAssistant boundary.
        """
        date_str = occurred_at.strftime("%Y-%m-%d") if occurred_at else "Unknown date"

        statute_list = "\n".join(
            [
                f"  - {s['citation']}: {s['title']}\n"
                + "".join(
                    [
                        f"    * Section {sec['label']}: {sec['title']}\n"
                        for sec in s.get("sections", [])
                    ]
                )
                for s in statute_refs[:30]
            ]
        )

        return (
            f"INCIDENT: {crime_type} at {location} on {date_str}.\n"
            f"Description: {description}\n\n"
            f"CANADIAN FEDERAL STATUTES:\n{statute_list}\n\n"
            f"Identify candidate statute sections relevant to this incident. "
            f"Return JSON with: statute_citation, section_id, confidence (0-100), "
            f"reason. All candidates require human review before use. "
            f"Do not state that a statute applies — only that it is a candidate "
            f"for review."
        )

    def _parse_and_persist_links(
        self,
        session: Session,
        incident_id: str,
        response_text: str,
        statute_refs: list,
    ) -> list[dict]:
        """
        Parse LLM response and save pending-review statute links to the DB.

        All links are created with review_status=LINK_REVIEW_STATUS_PENDING.
        No link is published or made public by this method.

        Note: this method is unreachable while _LINKER_ENABLED is False.
        """
        import json
        from sqlalchemy import select
        from app.models.entities import StatuteIncidentLink

        links: list[dict] = []

        try:
            json_text = response_text.strip()
            if json_text.startswith("```"):
                json_text = json_text.split("```")[1]
                if json_text.startswith("json"):
                    json_text = json_text[4:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]

            parsed = json.loads(json_text.strip())

            for link_data in parsed.get("links", []):
                try:
                    section_id = link_data.get("section_id")
                    confidence = link_data.get("confidence", 0) / 100.0
                    reason = link_data.get("reason", "")

                    if not section_id or confidence < 0.3:
                        continue

                    existing = session.execute(
                        select(StatuteIncidentLink).filter_by(
                            incident_id=incident_id,
                            legal_section_id=section_id,
                        )
                    )
                    if existing.scalars().first():
                        continue

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
                    logger.warning(f"[v0] Error processing candidate link: {e}")
                    continue

            session.commit()
            logger.info(
                f"[v0] Created {len(links)} pending-review statute candidates "
                f"for incident {incident_id}"
            )

        except Exception as e:
            logger.error(
                f"[v0] Error parsing LLM response for incident {incident_id}: {e}"
            )
            session.rollback()

        return links
