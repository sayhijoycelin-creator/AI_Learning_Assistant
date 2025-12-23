from __future__ import annotations

from typing import Dict, Iterable, List

from .models import Course, UserProfile
from .recommender import recommend_courses


def build_search_query(profile: UserProfile) -> Dict[str, str]:
    """Build a simple search query payload for an external course API."""

    return {
        "keywords": ", ".join(profile.interested_topics + [profile.learning_goal]),
        "level": profile.current_level,
        "providers": ", ".join(profile.provider_requirements) if profile.provider_requirements else "",
    }


def filter_searched_courses(profile: UserProfile, search_results: Iterable[Course], limit: int = 3) -> List[Course]:
    """Filter external search results to the learner's level and topics."""

    return recommend_courses(profile, catalog=list(search_results), limit=limit, use_builtin_fallback=False)

