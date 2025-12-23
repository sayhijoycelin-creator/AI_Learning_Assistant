from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class UserProfile:
    """Represents a learner's preferences and context."""

    name: str
    learning_goal: str
    interested_topics: List[str]
    current_level: str
    provider_requirements: List[str] = field(default_factory=list)
    weekly_time_hours: Optional[int] = None
    timeframe_weeks: Optional[int] = None
    phased_focus: List[str] = field(default_factory=list)
    special_requirements: List[str] = field(default_factory=list)


@dataclass
class Course:
    """Describes a recommended course."""

    title: str
    provider: str
    url: str
    topics: List[str]
    level: str
    summary: str
    est_hours: Optional[int] = None


@dataclass
class LearningPlanStep:
    """A single actionable step in a learning plan."""

    title: str
    description: str
    resources: List[str] = field(default_factory=list)
    est_time_hours: Optional[int] = None


@dataclass
class LearningPlan:
    """A structured plan with multiple steps."""

    goal: str
    steps: List[LearningPlanStep]
    notes: List[str] = field(default_factory=list)


@dataclass
class ConversationMessage:
    """Conversation message stored by the logger."""

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
