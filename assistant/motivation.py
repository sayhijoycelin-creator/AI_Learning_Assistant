from __future__ import annotations

import random
from typing import Optional

from .models import UserProfile


def build_motivation_message(
    profile: UserProfile, progress_percent: Optional[int] = None, last_action: str | None = None
) -> str:
    """Return a supportive, personalized message."""

    openers = [
        f"Hey {profile.name}, you’ve got this!",
        f"Keep it up, {profile.name}!",
        f"Great work staying committed, {profile.name}!",
    ]

    encouragements = [
        "Every small session compounds into big gains.",
        "Momentum beats perfection—show up for today’s session.",
        "Remember why you started and celebrate each checkpoint.",
    ]

    if progress_percent is not None:
        encouragements.append(f"Nice! You’re {progress_percent}% into your plan already.")

    if last_action:
        encouragements.append(f"Your last win: {last_action}. Let’s build on it.")

    return " ".join([random.choice(openers), random.choice(encouragements)])

