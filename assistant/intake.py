from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

from .models import UserProfile
from .schemas import LearningProfilePayload


@dataclass(frozen=True)
class IntakeQuestion:
    """Represents a single intake question the assistant should ask."""

    key: str
    prompt: str
    guidance: str


_INTAKE_QUESTIONS: List[IntakeQuestion] = [
    IntakeQuestion(
        key="name",
        prompt="What name would you like me to use?",
        guidance="A nickname is perfect.",
    ),
    IntakeQuestion(
        key="learning_goal",
        prompt="What outcome are you aiming for (e.g., land a data analyst role, build ML projects)?",
        guidance="Keep this concrete so the plan can be focused.",
    ),
    IntakeQuestion(
        key="interested_topics",
        prompt="Which topics or skills do you want to cover first?",
        guidance="Examples: Python, SQL, pandas, data visualization, machine learning.",
    ),
    IntakeQuestion(
        key="current_level",
        prompt="How would you describe your current level?",
        guidance="Choose from beginner, intermediate, or advanced.",
    ),
    IntakeQuestion(
        key="provider_requirements",
        prompt="Do you have preferred course providers or requirements?",
        guidance="Examples: DataCamp-only, short courses (<10h), project-focused.",
    ),
    IntakeQuestion(
        key="timeframe_weeks",
        prompt="How many weeks do you want this plan to run?",
        guidance="Use a number (e.g., 8 for two months).",
    ),
    IntakeQuestion(
        key="weekly_time_hours",
        prompt="How many hours per week can you study?",
        guidance="A ballpark number helps break down the weekly schedule.",
    ),
    IntakeQuestion(
        key="phased_focus",
        prompt="Do you want phases (e.g., Month 1: data analysis; Month 2: finance)?",
        guidance="Separate phases with semicolons. Optional—leave blank if you prefer a straight path.",
    ),
]


def intake_questions() -> Sequence[IntakeQuestion]:
    """Return the ordered intake questions to ask a new learner."""

    return list(_INTAKE_QUESTIONS)


def build_profile_from_answers(name: str, answers: Dict[str, str]) -> UserProfile:
    """Create a user profile from intake answers collected interactively."""

    topics_raw = answers.get("interested_topics", "")
    topics = [t.strip() for t in topics_raw.split(",") if t.strip()] or ["python"]

    providers_raw = answers.get("provider_requirements", "") or "DataCamp"
    providers = [p.strip() for p in providers_raw.split(",") if p.strip()]

    weekly_time = answers.get("weekly_time_hours", "").strip()
    timeframe_weeks = answers.get("timeframe_weeks", "").strip()
    phases_raw = answers.get("phased_focus", "")
    phases = [p.strip() for p in phases_raw.split(";") if p.strip()]

    return UserProfile(
        name=(answers.get("name") or name).strip() or "Learner",
        learning_goal=answers.get("learning_goal", "").strip() or "Grow data skills",
        interested_topics=topics,
        current_level=answers.get("current_level", "").strip() or "beginner",
        provider_requirements=providers,
        weekly_time_hours=int(weekly_time) if weekly_time.isdigit() else None,
        timeframe_weeks=int(timeframe_weeks) if timeframe_weeks.isdigit() else None,
        phased_focus=phases,
        special_requirements=[s.strip() for s in answers.get("special_requirements", "").split(",") if s.strip()],
    )


def build_profile_from_payload(payload: LearningProfilePayload) -> UserProfile:
    """Convert a frontend intake payload into an internal UserProfile."""

    learning_goal = ", ".join(payload.learning_goals) if payload.learning_goals else "Grow data skills"
    return UserProfile(
        name=payload.name or "Learner",
        learning_goal=learning_goal,
        interested_topics=payload.learning_topics or ["python"],
        current_level=payload.current_level.overall or "beginner",
        provider_requirements=payload.preferred_providers or ["DataCamp"],
        weekly_time_hours=payload.time_commitment.hours_per_week,
        timeframe_weeks=payload.time_commitment.timeframe_weeks,
        phased_focus=[],
        special_requirements=payload.special_requirements or [],
    )
