"""Centralized review state machine.

All review status transitions must go through this module.  Route-level
code must NOT implement its own state transition logic.

Allowed states:
    draft
    pending_review
    needs_revision
    approved
    rejected
    archived
    superseded

Allowed transitions:
    draft           -> pending_review
    pending_review  -> approved
    pending_review  -> rejected
    pending_review  -> needs_revision
    needs_revision  -> pending_review
    approved        -> superseded
    approved        -> archived
    rejected        -> archived

Forbidden transitions (enforced centrally):
    draft           -> approved       (must pass review)
    rejected        -> approved       (rejected records cannot be approved directly)
    archived        -> approved       (archived records cannot be revived to approved)
    any             -> approved  without human actor metadata
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

# ── State constants ───────────────────────────────────────────────────────────

ReviewState = Literal[
    "draft",
    "pending_review",
    "needs_revision",
    "approved",
    "rejected",
    "archived",
    "superseded",
]

ALL_STATES: frozenset[ReviewState] = frozenset(
    {
        "draft",
        "pending_review",
        "needs_revision",
        "approved",
        "rejected",
        "archived",
        "superseded",
    }
)

# ── Allowed transition table ──────────────────────────────────────────────────

ALLOWED_TRANSITIONS: dict[ReviewState, frozenset[ReviewState]] = {
    "draft": frozenset({"pending_review"}),
    "pending_review": frozenset({"approved", "rejected", "needs_revision"}),
    "needs_revision": frozenset({"pending_review"}),
    "approved": frozenset({"superseded", "archived"}),
    "rejected": frozenset({"archived"}),
    "archived": frozenset(),   # terminal state
    "superseded": frozenset(), # terminal state
}

# States that require human actor metadata before transition is allowed
REQUIRES_HUMAN_ACTOR: frozenset[ReviewState] = frozenset({"approved"})


# ── Data classes ──────────────────────────────────────────────────────────────


@dataclass
class ReviewerActor:
    """Identity record of the human who performed a review action."""

    actor_id: str
    reviewed_at: datetime
    review_decision: str
    review_notes: str | None = None
    evidence_snapshot_id: int | None = None
    source_record_id: int | None = None

    def is_valid(self) -> bool:
        """Return True if all required fields are populated."""
        return bool(self.actor_id and self.reviewed_at and self.review_decision)


@dataclass
class TransitionResult:
    ok: bool
    from_state: str
    to_state: str
    reason: str | None = None
    errors: list[str] = field(default_factory=list)


# ── Core state machine ────────────────────────────────────────────────────────


class ReviewStateMachine:
    """Enforce state transition rules for a single review record."""

    def __init__(self, current_state: str):
        if current_state not in ALL_STATES:
            raise ValueError(f"Unknown review state: {current_state!r}")
        self.current_state: ReviewState = current_state  # type: ignore[assignment]

    def can_transition(self, target_state: str) -> tuple[bool, list[str]]:
        """Return (allowed, list_of_errors)."""
        errors: list[str] = []

        if target_state not in ALL_STATES:
            errors.append(f"Unknown target state: {target_state!r}")
            return False, errors

        allowed = ALLOWED_TRANSITIONS.get(self.current_state, frozenset())
        if target_state not in allowed:
            errors.append(
                f"Transition {self.current_state!r} -> {target_state!r} is not allowed. "
                f"Allowed transitions from {self.current_state!r}: {sorted(allowed) or 'none (terminal state)'}"
            )
            return False, errors

        return True, []

    def transition(
        self,
        target_state: str,
        *,
        actor: ReviewerActor | None = None,
    ) -> TransitionResult:
        """Attempt the transition, enforcing human actor requirements."""
        allowed, errors = self.can_transition(target_state)
        if not allowed:
            return TransitionResult(
                ok=False,
                from_state=self.current_state,
                to_state=target_state,
                errors=errors,
            )

        # Require human actor for transitions into states that need one
        target: ReviewState = target_state  # type: ignore[assignment]
        if target in REQUIRES_HUMAN_ACTOR:
            if actor is None:
                return TransitionResult(
                    ok=False,
                    from_state=self.current_state,
                    to_state=target_state,
                    errors=[
                        f"Transition to {target_state!r} requires a human reviewer actor. "
                        "Provide ReviewerActor with actor_id, reviewed_at, and review_decision."
                    ],
                )
            if not actor.is_valid():
                return TransitionResult(
                    ok=False,
                    from_state=self.current_state,
                    to_state=target_state,
                    errors=[
                        "ReviewerActor is incomplete. "
                        "actor_id, reviewed_at, and review_decision are all required."
                    ],
                )

        previous = self.current_state
        self.current_state = target
        return TransitionResult(ok=True, from_state=previous, to_state=target)


# ── Convenience helpers ───────────────────────────────────────────────────────


def is_terminal(state: str) -> bool:
    """Return True if the state has no further allowed transitions."""
    return not ALLOWED_TRANSITIONS.get(state, frozenset())  # type: ignore[arg-type]


def is_public_safe(state: str) -> bool:
    """Return True only if the state allows public visibility."""
    return state == "approved"


def requires_human_actor(target_state: str) -> bool:
    """Return True if transitioning to target_state requires a ReviewerActor."""
    return target_state in REQUIRES_HUMAN_ACTOR


def make_actor(
    actor_id: str,
    decision: str,
    notes: str | None = None,
    evidence_snapshot_id: int | None = None,
    source_record_id: int | None = None,
) -> ReviewerActor:
    """Convenience constructor for ReviewerActor with current UTC timestamp."""
    return ReviewerActor(
        actor_id=actor_id,
        reviewed_at=datetime.now(tz=timezone.utc),
        review_decision=decision,
        review_notes=notes,
        evidence_snapshot_id=evidence_snapshot_id,
        source_record_id=source_record_id,
    )
