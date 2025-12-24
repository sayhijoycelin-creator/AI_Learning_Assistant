from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CurrentLevel:
    overall: str
    notes: Optional[str] = None


@dataclass
class TimeCommitment:
    hours_per_week: int
    timeframe_weeks: Optional[int] = None


@dataclass
class LearningProfilePayload:
    """Payload shape expected from the frontend intake flow."""

    name: str = "Learner"
    learning_goals: List[str] = field(default_factory=list)
    learning_topics: List[str] = field(default_factory=list)
    current_level: CurrentLevel = field(default_factory=lambda: CurrentLevel("Beginner"))
    preferred_providers: List[str] = field(default_factory=list)
    special_requirements: List[str] = field(default_factory=list)
    time_commitment: TimeCommitment = field(default_factory=lambda: TimeCommitment(6, None))

