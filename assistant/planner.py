from __future__ import annotations

from typing import List, Sequence

from .models import Course, LearningPlan, LearningPlanStep, UserProfile


def _step_from_course(course: Course, index: int) -> LearningPlanStep:
    return LearningPlanStep(
        title=f"Step {index + 1}: {course.title}",
        description=(
            f"Work through {course.title} on {course.provider}. "
            f"Focus on modules matching your goal."
        ),
        resources=[course.url],
        est_time_hours=course.est_hours,
    )


def build_learning_plan(profile: UserProfile, courses: Sequence[Course]) -> LearningPlan:
    """Compose a simple, ordered learning plan from recommended courses."""

    steps: List[LearningPlanStep] = []

    # Warm-up step
    steps.append(
        LearningPlanStep(
            title="Step 0: Clarify success",
            description=(
                f"Write a 2–3 sentence description of what success looks like for "
                f"{profile.learning_goal}. Keep it visible during study sessions."
            ),
            resources=[],
            est_time_hours=1,
        )
    )

    for idx, course in enumerate(courses):
        steps.append(_step_from_course(course, idx))

    steps.append(
        LearningPlanStep(
            title="Step final: Apply your skills",
            description=(
                "Complete a small portfolio project that applies what you learned. "
                "Share it with a peer or mentor for feedback."
            ),
            resources=["https://www.kaggle.com/datasets", "https://github.com/trending/python?since=monthly"],
            est_time_hours=8,
        )
    )

    notes = [
        "Aim for consistent daily progress (30–60 minutes).",
        "Take quick notes after each session to capture insights and blockers.",
        "Celebrate wins—course checkpoints, projects completed, or concepts mastered.",
    ]

    if profile.phased_focus:
        notes.append(
            f"Phased focus provided: {', '.join(profile.phased_focus)}. Align steps with these phases."
        )

    return LearningPlan(goal=profile.learning_goal, steps=steps, notes=notes)


def build_weekly_plan(
    learning_plan: LearningPlan,
    *,
    weekly_time_hours: int | None = None,
    timeframe_weeks: int | None = None,
) -> List[LearningPlanStep]:
    """Break the learning plan into a weekly sequence of steps.

    This is intentionally lightweight: it slices the step list across the requested timeframe,
    repeating steps if needed and trimming when time runs short.
    """

    if not learning_plan.steps:
        return []

    total_steps = len(learning_plan.steps)
    weeks = timeframe_weeks or max(total_steps, 4)
    weekly_steps: List[LearningPlanStep] = []

    # Simple distribution: map each week to a step, cycling if timeframe exceeds steps.
    for week in range(weeks):
        step = learning_plan.steps[week % total_steps]
        weekly_steps.append(
            LearningPlanStep(
                title=f"Week {week + 1}: {step.title}",
                description=step.description,
                resources=step.resources,
                est_time_hours=step.est_time_hours or weekly_time_hours,
            )
        )

    return weekly_steps
