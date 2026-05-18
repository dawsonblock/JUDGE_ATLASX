"""Source authority weights and supersession logic for contradiction resolution.

Defines authority hierarchy for sources to determine contradiction severity
and automatic supersession decisions.
"""

from __future__ import annotations

from typing import Optional

# Source authority hierarchy (higher = more authoritative)
# Based on the JUDGE_ATLASX production roadmap requirements
SOURCE_AUTHORITY_WEIGHTS = {
    "official_court": 1.00,
    "official_legislation": 1.00,
    "official_statistics": 0.95,
    "government_publication": 0.90,
    "court_record": 0.90,
    "recognized_media": 0.70,
    "local_media": 0.55,
    "user_submission": 0.30,
    "ai_extraction": 0.20,
    "unknown": 0.10,
}


def get_source_authority_weight(source_type: Optional[str]) -> float:
    """Get authority weight for a source type.

    Args:
        source_type: Source type string

    Returns:
        Authority weight (0.0-1.0)
    """
    if not source_type:
        return SOURCE_AUTHORITY_WEIGHTS["unknown"]

    return SOURCE_AUTHORITY_WEIGHTS.get(source_type.lower(), SOURCE_AUTHORITY_WEIGHTS["unknown"])


def calculate_authority_gap(weight1: float, weight2: float) -> float:
    """Calculate the gap between two source authority weights.

    Args:
        weight1: First source authority weight
        weight2: Second source authority weight

    Returns:
        Absolute difference between weights (0.0-1.0)
    """
    return abs(weight1 - weight2)


def should_supersede(new_claim_authority: float, old_claim_authority: float, claim_type: str) -> bool:
    """Determine if a new claim should supersede an old claim based on authority.

    Supersession rules:
    - Newer statute supersedes older statute
    - Appeal may supersede lower ruling status
    - Official correction supersedes media report
    - Court docket update supersedes stale schedule

    Args:
        new_claim_authority: Authority weight of new claim
        old_claim_authority: Authority weight of old claim
        claim_type: Type of claim (statute, appeal, correction, docket, etc.)

    Returns:
        True if new claim should supersede old claim
    """
    # Higher authority always wins
    if new_claim_authority > old_claim_authority:
        return True

    # Same authority: check claim type rules
    if new_claim_authority == old_claim_authority:
        if claim_type in ["statute_update", "appeal", "correction", "docket_update"]:
            return True

    return False


def supersede_by_statute(new_claim_date, old_claim_date) -> bool:
    """Newer statute supersedes older statute.

    Args:
        new_claim_date: Date of new claim
        old_claim_date: Date of old claim

    Returns:
        True if new claim is newer
    """
    return new_claim_date > old_claim_date


def supersede_by_appeal(new_claim_type: str, old_claim_type: str) -> bool:
    """Appeal may supersede lower ruling status.

    Args:
        new_claim_type: Type of new claim
        old_claim_type: Type of old claim

    Returns:
        True if new claim is an appeal and old is a lower ruling
    """
    appeal_types = ["appeal", "supreme_court", "appellate_court"]
    lower_types = ["trial_court", "provincial_court", "district_court"]

    return new_claim_type in appeal_types and old_claim_type in lower_types


def supersede_by_correction(new_source_type: str, old_source_type: str) -> bool:
    """Official correction supersedes media report.

    Args:
        new_source_type: Source type of new claim
        old_source_type: Source type of old claim

    Returns:
        True if new is official and old is media
    """
    official_types = ["official_court", "official_legislation", "court_record"]
    media_types = ["recognized_media", "local_media", "news_article"]

    return new_source_type in official_types and old_source_type in media_types


def supersede_by_docket(new_claim_status: str, old_claim_status: str) -> bool:
    """Court docket update supersedes stale schedule.

    Args:
        new_claim_status: Status of new claim
        old_claim_status: Status of old claim

    Returns:
        True if new claim is current and old is stale
    """
    current_statuses = ["active", "pending", "scheduled"]
    stale_statuses = ["completed", "archived", "withdrawn"]

    return new_claim_status in current_statuses and old_claim_status in stale_statuses
