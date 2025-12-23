# AI Learning Assistant

A lightweight, local-friendly module for building a personal learning assistant that:

- clarifies a learner's goals and current level through an intake flow,
- recommends DataCamp courses that fit the learner's level,
- drafts a step-by-step learning plan from those courses,
- breaks work into weekly chunks based on your time and timeline,
- sends supportive daily encouragement,
- and logs conversations for later review.

## Features

- **Interactive intake**: Ask a short set of questions to capture name, learning goal(s), topics, level, provider preferences, time budget, and desired timeline.
- **Profile-driven recommendations**: Use the intake answers to get level-appropriate course suggestions from dynamic search results (or, optionally, a tiny offline sample catalog).
- **Structured plans**: Turn recommended courses into an ordered learning plan with actionable steps.
- **Weekly breakdowns**: Convert the learning plan into week-by-week steps using your time budget and desired duration.
- **Daily motivation**: Generate friendly encouragement messages that reference recent progress.
- **Conversation logging**: Persist assistant chats to JSON Lines for easy replay or analysis.

## Quick start

```python
from assistant import (
    ConversationLogger,
    ConversationMessage,
    build_learning_plan,
    build_motivation_message,
    build_weekly_plan,
    build_profile_from_answers,
    build_profile_from_payload,
    build_search_query,
    filter_searched_courses,
    LearningProfilePayload,
    intake_questions,
    recommend_courses,
)

# 1) Ask intake questions first (in chat or CLI) and collect answers
answers = {}
for q in intake_questions():
    print(q.prompt)
    answers[q.key] = input("> ").strip()

profile = build_profile_from_answers(name="Learner", answers=answers)

# 2) Recommend courses that match the learner's level/topics
# Normally you would call an external search API here using build_search_query(profile).
# For illustration, assume `search_results` is returned from that API as a list of Course objects.
# courses = filter_searched_courses(profile, search_results)
# If you want a tiny offline fallback, set use_builtin_fallback=True:
courses = recommend_courses(profile, use_builtin_fallback=True)

# 3) Turn recommendations into a sequenced learning plan
plan = build_learning_plan(profile, courses)

# 3b) Break it down week-by-week using time and timeline from intake
weekly_plan = build_weekly_plan(
    plan,
    weekly_time_hours=profile.weekly_time_hours,
    timeframe_weeks=profile.timeframe_weeks,
)

# 4) Send a motivational nudge using recent context
motivation = build_motivation_message(profile, progress_percent=10, last_action="finished pandas basics")

# 5) Log the conversation for later review
logger = ConversationLogger("logs/conversation.jsonl")
logger.append(ConversationMessage(role="user", content="Help me start learning data science!"))
logger.append(ConversationMessage(role="assistant", content="Here are some courses to begin..."))
```

### React intake → backend mapping

If you use the provided `IntakeChat.tsx` snippet (see `examples/IntakeChat.tsx`), send its structured payload straight to the backend and convert it with `build_profile_from_payload`:

```python
from fastapi import FastAPI
from assistant import LearningProfilePayload, build_profile_from_payload, recommend_courses

app = FastAPI()

@app.post("/intake")
def intake(payload: LearningProfilePayload):
    profile = build_profile_from_payload(payload)
    courses = recommend_courses(profile, use_builtin_fallback=True)
    return {
        "profile": profile,
        "courses": [c.__dict__ for c in courses],
    }
```

This repository is intentionally minimal so it can be embedded into a broader application (CLI, web, or chat) as you build out your personal learning companion.
