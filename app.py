
import streamlit as st

from ai_service import generate_study_output
from validators import (
    validate_quiz_count,
    validate_text,
)

st.set_page_config(
    page_title="AI StudyMate",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.5rem 2.75rem;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        background:
            radial-gradient(ellipse at 88% 12%, rgba(91, 132, 255, 0.30), transparent 34%),
            linear-gradient(120deg, #14213d 0%, #1c3260 58%, #294b83 100%);
        box-shadow: 0 18px 44px rgba(23, 42, 79, 0.15);
        color: #ffffff;
        margin-bottom: 2.25rem;
        animation: enter 550ms ease-out both;
    }

    .hero p {
        max-width: 660px;
        color: #d9e4f6;
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 0.65rem 0 0;
    }

    .hero h1 {
        color: #ffffff;
        font-size: clamp(2rem, 4vw, 2.8rem);
        letter-spacing: -0.045em;
        line-height: 1.12;
        margin: 0.7rem 0 0;
    }

    .hero-eyebrow {
        color: #adc6ff;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .hero-meta {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1.4rem;
        padding: 0.45rem 0.75rem;
        border: 1px solid rgba(219, 231, 255, 0.2);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        color: #e6efff;
        font-size: 0.8rem;
    }

    .section-heading {
        margin: 0 0 0.2rem;
        color: #18263d;
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    .section-description {
        margin: 0 0 1.2rem;
        color: #68778d;
        font-size: 0.94rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f4fb 0%, #f7f9fc 100%);
        border-right: 1px solid #e4eaf3;
    }

    [data-testid="stSidebar"] h1 {
        color: #18263d;
        letter-spacing: -0.035em;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #62718a;
    }

    [data-testid="stForm"],
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #e3e9f2;
        border-radius: 18px;
    }

    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stSlider"] {
        transition: border-color 180ms ease, box-shadow 180ms ease;
    }

    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stSelectbox"] [data-baseweb="select"]:focus-within {
        border-color: #456bd6;
        box-shadow: 0 0 0 3px rgba(69, 107, 214, 0.13);
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stDownloadButton"] button {
        border-radius: 10px;
        font-weight: 600;
        transition: transform 160ms ease, box-shadow 160ms ease, background-color 160ms ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover,
    [data-testid="stDownloadButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(38, 67, 125, 0.14);
    }

    [data-testid="stForm"],
    [data-testid="stVerticalBlockBorderWrapper"] {
        animation: enter 450ms ease-out both;
    }

    @keyframes enter {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1.25rem 1rem 2rem;
        }

        .hero {
            padding: 1.75rem 1.4rem;
            border-radius: 18px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            scroll-behavior: auto !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------

if "result" not in st.session_state:
    st.session_state.result = ""

if "last_task" not in st.session_state:
    st.session_state.last_task = ""

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Sidebar ----------

with st.sidebar:
    st.title("📚 AI StudyMate")

    st.caption("Your personal learning workspace")

    st.divider()

    st.subheader("Available tools")

    st.markdown(
        """
        - 📝 Summarize Notes
        - 🧠 Generate Quiz
        - ✍️ Improve My Answer
        - 💡 Explain Concept
        """
    )

    st.divider()

    st.subheader("How to use")

    st.markdown(
        """
        1. Select a study tool.
        2. Enter your notes or question.
        3. Choose the difficulty level.
        4. Click Generate.
        5. Review the result.
        """
    )

    st.caption(
        "AI-generated answers can contain mistakes. "
        "Verify important facts against your course material."
    )

    if st.button("Clear current result", use_container_width=True):
        st.session_state.result = ""
        st.session_state.last_task = ""
        st.rerun()

# ---------- Main header ----------

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Your personal learning workspace</div>
        <h1>Make every study session count.</h1>
        <p>
            Turn your notes into focused revision material, practice quizzes,
            stronger answers, and clear explanations — all in one place.
        </p>
        <div class="hero-meta">✦ &nbsp;Thoughtful tools for better learning</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Feature form ----------

st.markdown(
    """
    <div class="section-heading">What would you like to work on?</div>
    <div class="section-description">
        Choose a study tool, set your preferences, and add your material.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    with st.form("study_form"):
        task_column, level_column = st.columns([1.5, 1])

        with task_column:
            task = st.selectbox(
                "Study tool",
                options=[
                    "Summarize Notes",
                    "Generate Quiz",
                    "Improve My Answer",
                    "Explain Concept",
                ],
                help="Select the type of result you want the AI to generate.",
            )

        with level_column:
            level = st.selectbox(
                "Difficulty level",
                options=[
                    "Beginner",
                    "Intermediate",
                    "Advanced",
                ],
                index=0,
            )

        question_count = 5

        if task == "Generate Quiz":
            question_count = st.slider(
                "Number of questions",
                min_value=3,
                max_value=10,
                value=5,
            )

        placeholders = {
            "Summarize Notes": (
                "Paste your lecture notes, textbook excerpts, "
                "or study material here..."
            ),
            "Generate Quiz": (
                "Paste your study notes. The AI will create "
                "multiple-choice questions from them..."
            ),
            "Improve My Answer": (
                "Paste your original answer here. Include the "
                "question too, if possible..."
            ),
            "Explain Concept": (
                "Enter a topic or question, for example: "
                "Explain normalization in DBMS with examples..."
            ),
        }

        content = st.text_area(
            "Your study material or question",
            height=230,
            placeholder=placeholders[task],
            max_chars=20000,
            help="Maximum length: 20,000 characters.",
        )

        st.caption(
            f"Characters entered: {len(content):,} / 20,000"
        )

        submitted = st.form_submit_button(
            "✨ Generate Study Output",
            type="primary",
            use_container_width=True,
        )

# ---------- Validate and generate ----------

if submitted:
    is_valid, validated_content = validate_text(content)

    if not is_valid:
        st.warning(validated_content)

    else:
        count_valid, count_error = validate_quiz_count(
            question_count
        )

        if task == "Generate Quiz" and not count_valid:
            st.warning(count_error)

        else:
            try:
                with st.spinner(
                    "AI StudyMate is preparing your study material..."
                ):
                    result = generate_study_output(
                        task=task,
                        content=validated_content,
                        level=level,
                        question_count=question_count,
                    )

                st.session_state.result = result
                st.session_state.last_task = task

                st.session_state.history.insert(
                    0,
                    {
                        "task": task,
                        "level": level,
                        "input": validated_content,
                        "output": result,
                    },
                )

                # Keep only the five most recent results.
                st.session_state.history = (
                    st.session_state.history[:5]
                )

            except (RuntimeError, ValueError) as exc:
                st.error(str(exc))

            except Exception:
                st.error(
                    "Something unexpected happened. "
                    "Please try again."
                )

# ---------- Display output ----------

if st.session_state.result:
    st.divider()

    st.markdown(
        """
        <div class="section-heading">Your study material</div>
        <div class="section-description">
            Review, save, or revisit your latest AI-generated result.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"Task: {st.session_state.last_task}"
    )

    with st.container(border=True):
        st.markdown(st.session_state.result)

    st.download_button(
        label="⬇️ Download result as Markdown",
        data=st.session_state.result,
        file_name="ai_studymate_output.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.divider()

    with st.expander("View recent activity"):
        if st.session_state.history:
            for index, item in enumerate(
                st.session_state.history, start=1
            ):
                st.markdown(
                    f"**{index}. {item['task']}** "
                    f"— {item['level']}"
                )

                st.caption(
                    item["input"][:180]
                    + ("..." if len(item["input"]) > 180 else "")
                )

                st.divider()

        else:
            st.caption("No recent activity yet.")

else:
    st.info(
        "Your generated result will appear here after you "
        "submit valid content."
    )

# ---------- Footer ----------

st.divider()

st.caption(
    "AI StudyMate | Built with Python, Streamlit, and Gemini. "
    "Review generated answers before using them in exams."
)
