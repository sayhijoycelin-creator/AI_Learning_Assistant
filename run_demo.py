from assistant import (
    build_learning_plan,
    build_motivation_message,
    build_weekly_plan,
    build_profile_from_answers,
    intake_questions,
    recommend_courses,
)

def main():
    # 1) Ask intake questions and collect answers
    answers = {}
    for q in intake_questions():
        print(q.prompt)
        answers[q.key] = input("> ").strip()

    profile = build_profile_from_answers(name="Learner", answers=answers)

    # 2) Recommend courses (offline fallback)
    courses = recommend_courses(profile, use_builtin_fallback=True)

    # 3) Turn recommendations into a sequenced learning plan
    plan = build_learning_plan(profile, courses)

    # 4) Break it down week-by-week
    weekly_plan = build_weekly_plan(
        plan,
        weekly_time_hours=profile.weekly_time_hours,
        timeframe_weeks=profile.timeframe_weeks,
    )

    # 5) Motivation nudge
    motivation = build_motivation_message(
        profile,
        progress_percent=10,
        last_action="finished pandas basics",
    )

    print("\n=== COURSES ===")
    for c in courses:
        print("-", c)

    print("\n=== PLAN ===")
    print(plan)

    print("\n=== WEEKLY PLAN ===")
    print(weekly_plan)

    print("\n=== MOTIVATION ===")
    print(motivation)

if __name__ == "__main__":
    main()
