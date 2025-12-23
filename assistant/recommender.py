from __future__ import annotations

from typing import Iterable, List, Sequence

from .models import Course, UserProfile

_COURSE_CATALOG: List[Course] = [
    Course(
        title="Data Scientist with Python",
        provider="DataCamp",
        url="https://www.datacamp.com/tracks/data-scientist-with-python",
        topics=["python", "data analysis", "statistics", "machine learning"],
        level="beginner",
        summary="End-to-end track that introduces Python, data wrangling, and basic ML.",
        est_hours=88,
    ),
    Course(
        title="Data Analyst with Python",
        provider="DataCamp",
        url="https://www.datacamp.com/tracks/data-analyst-with-python",
        topics=["python", "pandas", "visualization"],
        level="beginner",
        summary="Core data analysis skills with pandas, visualization, and SQL foundations.",
        est_hours=62,
    ),
    Course(
        title="Machine Learning Scientist with Python",
        provider="DataCamp",
        url="https://www.datacamp.com/tracks/machine-learning-scientist-with-python",
        topics=["machine learning", "modeling", "python"],
        level="intermediate",
        summary="Deep dive into ML workflows, model tuning, and advanced techniques.",
        est_hours=80,
    ),
    Course(
        title="SQL Fundamentals",
        provider="DataCamp",
        url="https://www.datacamp.com/courses/introduction-to-sql",
        topics=["sql", "databases"],
        level="beginner",
        summary="Introductory SQL for data querying and analysis.",
        est_hours=4,
    ),
    Course(
        title="Deep Learning in Python",
        provider="DataCamp",
        url="https://www.datacamp.com/courses/deep-learning-in-python",
        topics=["deep learning", "neural networks", "python"],
        level="intermediate",
        summary="Neural network foundations with Keras and practical projects.",
        est_hours=16,
    ),
]


def _matches_topic(course: Course, interested_topics: Sequence[str]) -> bool:
    normalized = {t.lower() for t in interested_topics}
    course_topics = {t.lower() for t in course.topics}
    return bool(normalized & course_topics)


def _matches_level(course: Course, current_level: str) -> bool:
    order = {"beginner": 1, "intermediate": 2, "advanced": 3}
    requested = order.get(current_level.lower(), 1)
    course_order = order.get(course.level.lower(), 1)
    return course_order <= requested + 1


def _provider_allowed(course: Course, providers: Iterable[str]) -> bool:
    normalized = {p.lower() for p in providers}
    return not normalized or course.provider.lower() in normalized


def recommend_courses(
    profile: UserProfile,
    *,
    catalog: Sequence[Course] | None = None,
    limit: int = 3,
    use_builtin_fallback: bool = False,
) -> List[Course]:
    """Return tailored course recommendations based on profile.

    The catalog parameter allows plugging in fresh search results (e.g., from a DataCamp API
    response). Set use_builtin_fallback=True to fall back to a tiny offline catalog.
    """

    if catalog is None:
        if not use_builtin_fallback:
            return []
        catalog = _COURSE_CATALOG
    else:
        catalog = list(catalog)

    matches = [
        course
        for course in catalog
        if _provider_allowed(course, profile.provider_requirements)
        and _matches_topic(course, profile.interested_topics)
        and _matches_level(course, profile.current_level)
    ]

    if not matches:
        if use_builtin_fallback:
            matches = [
                c
                for c in catalog
                if _provider_allowed(c, profile.provider_requirements) and c.level == "beginner"
            ]

    return matches[:limit]
