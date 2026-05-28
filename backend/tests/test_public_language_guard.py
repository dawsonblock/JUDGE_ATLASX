"""Tests for the public language guard.

Verifies:
- Unsourced risky terms are blocked
- Source-attributed risky terms are warnings only
- Neutral language passes
- assert_public_safe raises on blocked text
"""

from __future__ import annotations

import pytest

from app.services.public_language_guard import (
    LanguageGuardResult,
    assert_public_safe,
    check_public_text,
)


# ── Blocked (unsourced risky language) ───────────────────────────────────────


@pytest.mark.parametrize(
    "text,expected_term",
    [
        ("This judge released a criminal who then committed X.", "criminal"),
        ("The defendant is definitely guilty.", "guilty"),
        ("The offender was released early.", "offender"),
        ("The cover-up was orchestrated by officials.", "cover-up"),
        ("The predator was identified in the area.", "predator"),
        ("This is definitely a fraudster.", "fraudster"),
        ("The behavior was illegal.", "illegal"),
        ("The evidence proved wrongdoing.", "proved"),
        ("The official is corrupt.", "corrupt"),
        ("The person was convicted.", "convicted"),
    ],
)
def test_blocked_unsourced_term(text: str, expected_term: str) -> None:
    """Risky terms without source attribution should be blocked."""
    result = check_public_text(text)
    assert result.is_blocked, f"Expected block for: {text!r}"
    terms = {f.term for f in result.flags}
    assert any(expected_term in t for t in terms), (
        f"Expected {expected_term!r} in flags, got {terms}"
    )


# ── Allowed (source-attributed) ───────────────────────────────────────────────


@pytest.mark.parametrize(
    "text",
    [
        "The court record states the person was convicted of theft in 2023.",
        "According to the reviewed source, the defendant was charged with fraud.",
        "The court found the defendant guilty of mischief.",
        "Per the court, the accused was found guilty.",
        "The judgment states the person was found guilty of breach of trust.",
        "The verdict found the accused guilty as charged.",
        "The court ruled the defendant was convicted.",
        "Based on the court record, the defendant was convicted of X.",
        "The reviewed source reports the person was charged with Y.",
        "The tribunal determined the respondent was guilty of misconduct.",
    ],
)
def test_source_attributed_terms_are_warnings_not_blocked(text: str) -> None:
    """Source-attributed risky terms should be warnings, not blockers."""
    result = check_public_text(text)
    assert not result.is_blocked, (
        f"Expected no block for source-attributed text: {text!r}\n"
        f"Flags: {[(f.term, f.is_source_attributed) for f in result.flags]}"
    )


# ── Clean text ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "text",
    [
        "The case was dismissed in 2022.",
        "The court record documents a filed motion.",
        "Statistical data from Saskatoon Open Data for Q2 2024.",
        "The legislation was passed in Parliament in 1985.",
        "The reviewed source indicates the hearing is scheduled.",
    ],
)
def test_clean_text_passes(text: str) -> None:
    """Neutral text without risky terms should pass without flags."""
    result = check_public_text(text)
    assert not result.is_blocked, f"Expected no block for clean text: {text!r}"
    assert "OK" in result.summary or not result.flags


# ── assert_public_safe ────────────────────────────────────────────────────────


def test_assert_public_safe_raises_on_blocked() -> None:
    """assert_public_safe must raise ValueError on blocked text."""
    with pytest.raises(ValueError, match="public language guard"):
        assert_public_safe("The criminal was released.")


def test_assert_public_safe_passes_clean() -> None:
    """assert_public_safe must not raise on clean text."""
    # Should not raise
    assert_public_safe("The court record indicates the case was filed in 2023.")


# ── Preferred phrasing ────────────────────────────────────────────────────────


def test_blocked_result_includes_preferred_phrasing() -> None:
    """Blocked results should include preferred phrasing when available."""
    result = check_public_text("The defendant is definitely guilty.")
    assert result.is_blocked
    blocked_flags = [f for f in result.flags if not f.is_source_attributed]
    assert any(f.preferred_phrasing for f in blocked_flags), (
        "Blocked flags should include preferred phrasing suggestions"
    )


# ── Guilt conclusion ──────────────────────────────────────────────────────────


def test_guilt_conclusion_blocked() -> None:
    """Direct guilt conclusions without court attribution must be blocked."""
    result = check_public_text("She is guilty and should be in prison.")
    assert result.is_blocked
    assert any(f.term == "guilty" and not f.is_source_attributed for f in result.flags)


def test_guilt_from_court_record_is_warning() -> None:
    """A guilt statement sourced to a court record should be a warning, not blocked."""
    result = check_public_text(
        "The court record states she was found guilty of the charge."
    )
    assert not result.is_blocked
