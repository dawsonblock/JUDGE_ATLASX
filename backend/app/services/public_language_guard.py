"""Public language guard.

Checks public-facing text for risky language that could imply guilt,
make legal conclusions, or create defamation risk.

The guard does not blindly ban all words. It checks context:
- "court record states the person was convicted of X" → allowed
- "this judge released a criminal who then committed X" → blocked

Usage:
    from app.services.public_language_guard import check_public_text, LanguageGuardResult

    result = check_public_text("The court found the defendant guilty of fraud.")
    if result.is_blocked:
        # use result.preferred_phrasing
    elif result.has_warnings:
        # log result.warnings
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# ── Flagged term patterns ─────────────────────────────────────────────────────

# These terms may be legitimate in source-attributed, neutral court language
# but are problematic in direct assertions.
FLAGGED_TERMS: list[tuple[str, str]] = [
    # (term_pattern, human-readable reason)
    (r"\bguilty\b", "implies legal guilt determination"),
    (r"\bcriminal\b", "labels a person without conviction source"),
    (r"\bcorrupt\b", "implies wrongdoing without sourced evidence"),
    (r"\bproved?\b", "asserts proof without evidence reference"),
    (r"\bdefinitely\b", "asserts certainty — use 'according to [source]'"),
    (r"\bconvicted\b", "conviction claim — requires court record source"),
    (r"\boffender\b", "labels a person — requires conviction source"),
    (r"\bpredator\b", "high-risk personal label — requires reviewed source"),
    (r"\bfraudster\b", "high-risk personal label — requires reviewed source"),
    (r"\bcover.?up\b", "allegation of concealment — requires reviewed source"),
    (r"\billegal\b", "legal conclusion — use 'alleged' or cite the law"),
]

# Source-attribution phrases that contextualize flagged terms
SOURCE_ATTRIBUTION_PATTERNS: list[str] = [
    r"court record(s)?\s+(state[sd]?|show[s]?|indicate[s]?)",
    r"the (reviewed |sourced |verified )?source (report[s]?|state[s]?|show[s]?)",
    r"according to the (court|record|decision|judgment|verdict|registry)",
    r"per the (court|record|decision|judgment)",
    r"(as|as per|based on) (court|record|judgment|decision|source)",
    r"the (court|tribunal|judge) (found|ruled|determined|stated)",
    r"the (verdict|judgment|decision) (state[sd]?|show[s]?|found)",
    r"charged with",
    r"alleged(ly)?",
    r"accused of",
]

# Preferred neutral phrasing suggestions
PREFERRED_PHRASING: dict[str, str] = {
    "guilty": "The reviewed source reports that [person] was charged with / found guilty of [X] by [court].",
    "criminal": "The record does not establish criminal status unless a conviction source is linked.",
    "corrupt": "The reviewed source alleges [X]. The record does not establish corruption without a conviction.",
    "proved": "According to the reviewed source, [evidence] supports [X].",
    "definitely": "According to the reviewed source, [X].",
    "convicted": "The court record states [person] was convicted of [X] in [court], [date].",
    "offender": "The reviewed court record identifies [person] as convicted of [X].",
    "predator": "The reviewed source states [person] was convicted of [X].",
    "fraudster": "The reviewed source identifies [person] as convicted of fraud.",
    "cover-up": "The reviewed source reports allegations of concealment of [X].",
    "illegal": "The reviewed source reports that [X] may violate [specific law].",
}


@dataclass
class LanguageFlag:
    term: str
    reason: str
    position: int
    context_window: str
    is_source_attributed: bool
    preferred_phrasing: str | None = None


@dataclass
class LanguageGuardResult:
    text: str
    flags: list[LanguageFlag] = field(default_factory=list)
    is_blocked: bool = False
    has_warnings: bool = False
    preferred_phrasing: str | None = None
    summary: str = ""


def _extract_context(text: str, pos: int, window: int = 150) -> str:
    start = max(0, pos - window)
    end = min(len(text), pos + window)
    return text[start:end]


def _is_source_attributed(context: str) -> bool:
    """Return True if the context contains a source-attribution phrase."""
    context_lower = context.lower()
    for pattern in SOURCE_ATTRIBUTION_PATTERNS:
        if re.search(pattern, context_lower):
            return True
    return False


def check_public_text(text: str) -> LanguageGuardResult:
    """Check text for risky language.

    Returns a LanguageGuardResult with flags and whether the text is
    blocked (must not be published as-is) or only has warnings.

    Allowed:
        "The court record states the person was convicted of X."
        "According to the reviewed source, the defendant was charged with Y."

    Blocked:
        "This judge released a criminal who then committed X."
        "The defendant is definitely guilty."
    """
    flags: list[LanguageFlag] = []

    for pattern, reason in FLAGGED_TERMS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            term = match.group(0).lower()
            pos = match.start()
            context = _extract_context(text, pos)
            attributed = _is_source_attributed(context)

            flag = LanguageFlag(
                term=term,
                reason=reason,
                position=pos,
                context_window=context,
                is_source_attributed=attributed,
                preferred_phrasing=PREFERRED_PHRASING.get(term),
            )
            flags.append(flag)

    # A flag is a blocker if it is not source-attributed
    blocking_flags = [f for f in flags if not f.is_source_attributed]
    warning_flags = [f for f in flags if f.is_source_attributed]

    is_blocked = len(blocking_flags) > 0
    has_warnings = len(warning_flags) > 0

    # Build summary
    if is_blocked:
        blocked_terms = ", ".join({f.term for f in blocking_flags})
        summary = (
            f"Blocked: {len(blocking_flags)} unsourced risky term(s) detected: {blocked_terms}. "
            "Use neutral, source-attributed language."
        )
    elif has_warnings:
        warn_terms = ", ".join({f.term for f in warning_flags})
        summary = (
            f"Warning: {len(warning_flags)} risky term(s) present but appear source-attributed: "
            f"{warn_terms}. Review phrasing."
        )
    else:
        summary = "OK: No risky language patterns detected."

    # Collect preferred phrasing suggestions
    phrasing_suggestions = [
        f.preferred_phrasing
        for f in blocking_flags
        if f.preferred_phrasing
    ]
    preferred = "\n".join(phrasing_suggestions) if phrasing_suggestions else None

    return LanguageGuardResult(
        text=text,
        flags=flags,
        is_blocked=is_blocked,
        has_warnings=has_warnings,
        preferred_phrasing=preferred,
        summary=summary,
    )


def assert_public_safe(text: str) -> None:
    """Raise ValueError if text fails the public language guard.

    Use this in service/API code as a hard gate before publishing.
    """
    result = check_public_text(text)
    if result.is_blocked:
        raise ValueError(
            f"Text failed public language guard: {result.summary}\n"
            f"Preferred phrasing:\n{result.preferred_phrasing or '(see flags)'}"
        )
