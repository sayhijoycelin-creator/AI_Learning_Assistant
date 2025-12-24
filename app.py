from datetime import date
import json
import streamlit as st

from assistant import (
    build_learning_plan,
    build_motivation_message,
    build_weekly_plan,
    build_profile_from_answers,
    intake_questions,
    recommend_courses,
)

# ---------------- Page setup ----------------
st.set_page_config(page_title="Learning Assistant", page_icon="🧠", layout="wide")

# ---------------- Utilities ----------------
def to_dict(x):
    if hasattr(x, "model_dump"):
        return x.model_dump()
    if hasattr(x, "dict"):
        return x.dict()
    if hasattr(x, "__dict__"):
        return dict(x.__dict__)
    return {"value": str(x)}

def list_of_dicts(items):
    return [to_dict(i) for i in (items or [])]

def ensure_state():
    defaults = {
        "profile": None,
        "courses": [],
        "plan": None,
        "weekly_plan": None,
        "motivation_text": "",
        "last_motivation_date": None,
        "progress": 0,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

ensure_state()

# ---------------- Header ----------------
st.markdown(
    """
    <div style="padding: 18px 22px; border-radius: 16px; background: linear-gradient(90deg, #101828, #1d2939); color: white;">
        <div style="font-size: 28px; font-weight: 800;">🧠 Personal Learning Assistant</div>
        <div style="opacity: 0.85; margin-top: 6px;">Plan smarter. Learn consistently. Stay motivated daily.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

# ---------------- Sidebar: Intake ----------------
with st.sidebar:
    st.header("⚙️ Setup")
    name = st.text_input("Name", value="Learner")

    qs = list(intake_questions())
    answers = {}
    if len(qs) == 0:
        st.error("No intake questions found (intake_questions() returned empty).")
    else:
        st.caption("Answer these to personalize your plan:")
        for q in qs:
            answers[q.key] = st.text_input(q.prompt, value="")

    use_fallback = st.toggle("Use builtin fallback courses", value=True)

    st.divider()
    st.subheader("🎯 Actions")

    colA, colB = st.columns(2)
    with colA:
        gen_all = st.button("Generate", use_container_width=True)
    with colB:
        reset = st.button("Reset", use_container_width=True)

    if reset:
        for key in ["profile", "courses", "plan", "weekly_plan", "motivation_text", "last_motivation_date", "progress"]:
            st.session_state[key] = None if key in ["profile", "plan", "weekly_plan"] else ("" if key == "motivation_text" else 0 if key == "progress" else [])

    if gen_all:
        profile = build_profile_from_answers(name=name, answers=answers)
        courses = recommend_courses(profile, use_builtin_fallback=use_fallback)
        plan = build_learning_plan(profile, courses)
        weekly_plan = build_weekly_plan(
            plan,
            weekly_time_hours=getattr(profile, "weekly_time_hours", 6),
            timeframe_weeks=getattr(profile, "timeframe_weeks", 4),
        )

        st.session_state["profile"] = profile
        st.session_state["courses"] = courses
        st.session_state["plan"] = plan
        st.session_state["weekly_plan"] = weekly_plan

# ---------------- Main area: Tabs ----------------
tab_plan, tab_courses, tab_motivation, tab_debug = st.tabs(["📅 Plan", "📚 Courses", "🔥 Motivation", "🪛 Debug"])

# ---------- PLAN TAB ----------
with tab_plan:
    st.subheader("📅 Weekly Plan")
    if st.session_state["weekly_plan"] is None:
        st.info("Click **Generate** in the sidebar to create a plan.")
    else:
        # Progress bar (user-controlled for now)
        st.session_state["progress"] = st.slider("Your progress (%)", 0, 100, int(st.session_state["progress"]))
        st.progress(st.session_state["progress"] / 100)

        wp = st.session_state["weekly_plan"]
        if isinstance(wp, list):
            st.dataframe(list_of_dicts(wp), use_container_width=True)
        else:
            st.code(json.dumps(to_dict(wp), ensure_ascii=False, indent=2), language="json")

        st.caption("Next: we can add 'mark as done' per step and auto-calc progress.")

# ---------- COURSES TAB ----------
with tab_courses:
    st.subheader("📚 Recommended Courses")
    courses = st.session_state["courses"] or []
    st.caption(f"Found: {len(courses)}")

    if len(courses) == 0:
        st.warning(
            "No courses returned.\n\n"
            "**Most common reasons:**\n"
            "- Intake answers are empty → profile has no topic/level\n"
            "- Builtin fallback is too strict and filters everything out\n\n"
            "Next step: paste `assistant/recommender.py` here and I’ll make fallback always return a good starter set."
        )
    else:
        st.dataframe(list_of_dicts(courses), use_container_width=True)

    # Optional: quick “pin” interaction (front-end only for now)
    st.divider()
    st.subheader("📌 Pin a course")
    if len(courses) > 0:
        titles = []
        for c in courses:
            d = to_dict(c)
            titles.append(d.get("title") or d.get("name") or str(c))
        pinned = st.multiselect("Pick favorites", options=titles)
        if pinned:
            st.success(f"Pinned: {', '.join(pinned)}")

# ---------- MOTIVATION TAB ----------
with tab_motivation:
    st.subheader("🔥 Daily Motivation")

    if st.session_state["profile"] is None:
        st.info("Generate a plan first.")
    else:
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Regenerate today’s motivation", use_container_width=True):
                st.session_state["last_motivation_date"] = None

        with col2:
            progress = st.slider("Progress signal for motivation", 0, 100, 10)

        today = date.today().isoformat()
        if st.session_state["last_motivation_date"] != today:
            msg = build_motivation_message(
                st.session_state["profile"],
                progress_percent=progress,
                last_action="showed up and did a small step",
            )
            st.session_state["motivation_text"] = msg
            st.session_state["last_motivation_date"] = today

        st.markdown(
            f"""
            <div style="padding: 16px; border-radius: 14px; background: #0b1220; color: #e5e7eb;">
                <div style="font-weight: 700; font-size: 16px; margin-bottom: 6px;">Today’s message</div>
                <div style="opacity: 0.92; line-height: 1.6;">{st.session_state["motivation_text"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------- DEBUG TAB ----------
with tab_debug:
    st.subheader("🪛 Debug")
    st.write("Profile:", to_dict(st.session_state["profile"]) if st.session_state["profile"] else None)
    st.write("Courses count:", len(st.session_state["courses"] or []))
    st.write("Plan:", to_dict(st.session_state["plan"]) if st.session_state["plan"] else None)
    st.write("Weekly plan type:", type(st.session_state["weekly_plan"]).__name__)
