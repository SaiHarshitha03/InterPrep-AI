import streamlit as st
from dotenv import load_dotenv

from resume_parser import extract_text_from_pdf
from ai_engine import (
    analyze_resume,
    generate_questions,
    evaluate_answer,
    generate_follow_up,
    transcribe_audio
)

load_dotenv()

st.set_page_config(
    page_title="InterPrep AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# SESSION STATE
# -----------------------------

defaults = {
    "resume_text": "",
    "job_description": "",
    "analysis": "",
    "questions": "",
    "current_question": "",
    "evaluation": "",
    "voice_transcript": "",
    "interview_started": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background: #0b0f19;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Header */

.hero {
    padding: 35px 40px;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        #111827 0%,
        #172554 50%,
        #111827 100%
    );
    border: 1px solid #26324a;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
}

.hero-title span {
    color: #60a5fa;
}

.hero-subtitle {
    color: #aab4c8;
    font-size: 17px;
    line-height: 1.6;
}

/* Cards */

.card {
    background: #111827;
    border: 1px solid #26324a;
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 10px;
}

.card-title {
    font-size: 21px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 6px;
}

.card-description {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.5;
}

/* Stats */

.stat-card {
    background: #111827;
    border: 1px solid #26324a;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
}

.stat-number {
    font-size: 30px;
    font-weight: 800;
    color: #60a5fa;
}

.stat-label {
    color: #94a3b8;
    font-size: 13px;
}

/* Section */

.section-title {
    font-size: 27px;
    font-weight: 750;
    color: white;
    margin-top: 20px;
    margin-bottom: 18px;
}

/* Buttons */

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 45px;
}

/* Upload */

[data-testid="stFileUploader"] {
    background: #0f172a;
    border: 1px dashed #475569;
    border-radius: 14px;
    padding: 10px;
}

/* Text area */

textarea {
    border-radius: 12px !important;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #26324a;
}

/* Hide menu */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HERO
# -----------------------------

st.markdown("""
<div class="hero">

<div class="hero-title">
🎯 Inter<span>Prep AI</span>
</div>

<div class="hero-subtitle">
Your AI-Powered Personalized Interview Preparation Platform
</div>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown("## ⚙️ Interview Setup")

    st.markdown("### Question Type")

    category = st.selectbox(
        "",
        [
            "Mixed",
            "Technical",
            "Project",
            "Machine Learning",
            "DSA",
            "HR / Behavioral",
            "Internship"
        ]
    )

    st.markdown("### Difficulty")

    difficulty = st.select_slider(
        "",
        options=[
            "Easy",
            "Medium",
            "Hard"
        ],
        value="Medium"
    )

    st.markdown("### Number of Questions")

    count = st.slider(
        "",
        5,
        30,
        10
    )

    st.markdown("---")

    st.markdown("""
    **💡 How InterPrep AI works**

    1. 📄 Upload your resume
    2. 💼 Add the job description
    3. 🧠 AI compares both
    4. 🎯 Generate questions
    5. 🎤 Practice interview
    6. 📊 Get feedback
    """)


# -----------------------------
# TABS
# -----------------------------

tab_resume, tab_analysis, tab_questions, tab_mock = st.tabs(
    [
        "📄  Preparation",
        "🧠  Resume Analysis",
        "❓  Interview Questions",
        "🎤  Mock Interview"
    ]
)


# =========================================================
# PREPARATION
# =========================================================

with tab_resume:

    st.markdown(
        '<div class="section-title">Prepare for your Interview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            color:#94a3b8;
            font-size:15px;
            margin-bottom:25px;
        ">
        Add the job description and your resume.
        InterPrep AI will compare them and create
        personalized interview preparation.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==============================
    # JOB DESCRIPTION
    # ==============================

    st.markdown(
        """
        <div class="card">
            <div class="card-title">💼 Job Description</div>
            <div class="card-description">
                Paste the complete job description for the position
                you are preparing for.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Job Description",
        height=230,
        placeholder="""Paste the job description here...

Example:

Software Engineer Intern

Requirements:
• Python
• Java
• SQL
• Data Structures
• Machine Learning
• REST APIs

Responsibilities:
• Develop software applications
• Work with engineering teams
• Debug and optimize applications
• Build scalable solutions
""",
        label_visibility="collapsed",
        key="job_description_input"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==============================
    # RESUME
    # ==============================

        # ==============================
    # RESUME
    # ==============================

    st.markdown(
        """
        <div class="card">
            <div class="card-title">📄 Your Resume</div>
            <div class="card-description">
                Upload the resume you will use for this interview.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    resume_file = st.file_uploader(
        "Upload your Resume",
        type=["pdf"],
        key="resume_upload",
        label_visibility="collapsed"
    )

    if resume_file:
        st.success(
            f"✓ Resume ready: {resume_file.name}"
        )

    # ==============================
    # ANALYZE
    # ==============================

    if st.button(
        "🚀 Analyze & Prepare",
        use_container_width=True,
        type="primary",
        key="analyze_prepare"
    ):

        if not job_description.strip():

            st.error(
                "Please enter the Job Description."
            )

        elif resume_file is None:

            st.error(
                "Please upload your Resume."
            )

        else:

            with st.spinner(
                "📖 Reading your resume..."
            ):

                resume_text = extract_text_from_pdf(
                    resume_file
                )

            st.session_state.resume_text = resume_text
            st.session_state.job_description = job_description

            with st.spinner(
                "🧠 Comparing Resume with Job Description..."
            ):

                st.session_state.analysis = analyze_resume(
                    resume_text,
                    job_description
                )

            # Reset interview data when a new resume/JD is analyzed
            st.session_state.questions = ""
            st.session_state.current_question = ""
            st.session_state.evaluation = ""
            st.session_state.voice_transcript = ""
            st.session_state.interview_started = False

            st.success(
                "🎯 Your personalized interview profile is ready!"
            )

            st.balloons()

   



    


# =========================================================
# ANALYSIS
# =========================================================

with tab_analysis:

    st.markdown(
        '<div class="section-title">🧠 Resume × Job Analysis</div>',
        unsafe_allow_html=True
    )

    if st.session_state.analysis:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            st.session_state.analysis
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Upload your resume and add a job description "
            "to generate the analysis."
        )


# =========================================================
# QUESTIONS
# =========================================================

with tab_questions:

    st.markdown(
        '<div class="section-title">❓ Personalized Interview Questions</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.resume_text:

        st.warning(
            "Complete the preparation step first."
        )

    elif not st.session_state.job_description:

        st.warning(
            "Add a job description first."
        )

    else:

        st.markdown("""
        <div class="card">
        <div class="card-title">🎯 Questions tailored to YOU</div>
        <div class="card-description">
        These questions are generated using both your resume
        and the requirements of the job.
        </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "✨ Generate Personalized Questions",
            use_container_width=True
        ):

            with st.spinner(
                "Creating personalized interview questions..."
            ):

                st.session_state.questions = generate_questions(
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    category,
                    difficulty,
                    count
                )

        if st.session_state.questions:

            st.markdown(
                st.session_state.questions
            )


# =========================================================
# MOCK INTERVIEW
# =========================================================

with tab_mock:

    st.markdown(
        '<div class="section-title">🎤 AI Mock Interview</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.resume_text:

        st.warning(
            "📄 Please upload and analyze your resume first."
        )

    elif not st.session_state.job_description:

        st.warning(
            "💼 Please add the job description first."
        )

    else:

        # -----------------------------
        # INTERVIEWER CARD
        # -----------------------------

        st.markdown("""
        <div class="card">

        <div class="card-title">
        👨‍💼 AI Interviewer
        </div>

        <div class="card-description">
        Answer naturally using your microphone.
        Your response will be transcribed and evaluated
        against your resume and the target job.
        </div>

        </div>
        """, unsafe_allow_html=True)

        # -----------------------------
        # START INTERVIEW
        # -----------------------------


        if not st.session_state.current_question:
            if st.button(
                "🎬 Start Mock Interview",
                use_container_width=True,
                type="primary",
                key="start_mock_interview"
           ):

        

                with st.spinner(
                    "🤖 Preparing your first question..."
                ):

                    question = generate_questions(
                        st.session_state.resume_text,
                        st.session_state.job_description,
                        "Mixed",
                        "Interview Level",
                        1
                    )

                    st.session_state.current_question = question
                    st.session_state.interview_started = True

                st.rerun()

        # -----------------------------
        # QUESTION
        # -----------------------------

        if st.session_state.current_question:

            st.markdown("### 👨‍💼 Interviewer")

            st.info(
                st.session_state.current_question
            )

            st.markdown("---")

            # -----------------------------
            # VOICE ANSWER
            # -----------------------------

            st.markdown("### 🎙️ Your Answer")

            st.caption(
                "Click the microphone and speak your answer."
            )

            audio_value = st.audio_input(
                "🎙️ Record your answer",
                key="answer_audio"
            )
            

            # -----------------------------
            # PROCESS AUDIO
            # -----------------------------

            if audio_value:

                st.audio(
                    audio_value,
                    format="audio/wav"
                )

                if st.button(
                    "📝 Convert Speech to Text",
                    use_container_width=True
                ):

                    with st.spinner(
                        "🎧 Converting your answer..."
                    ):

                        transcript = transcribe_audio(
                            audio_value
                        )

                    st.session_state.voice_transcript = transcript

                    st.success(
                        "✅ Your answer has been transcribed."
                    )

            # -----------------------------
            # TRANSCRIPT
            # -----------------------------

            if st.session_state.get(
                "voice_transcript"
            ):

                st.markdown(
                    "### 📝 Transcribed Answer"
                )

                edited_answer = st.text_area(
                    "Review or edit your answer",
                    value=st.session_state.voice_transcript,
                    height=220,
                    key="edited_answer"
                )

                st.markdown("")

                col1, col2 = st.columns(2)

                # -----------------------------
                # EVALUATE
                # -----------------------------

                with col1:

                    if st.button(
                        "📊 Evaluate Answer",
                        use_container_width=True
                    ):

                        if not edited_answer.strip():

                            st.warning(
                                "Your answer is empty."
                            )

                        else:

                            with st.spinner(
                                "🧠 AI is evaluating your answer..."
                            ):

                                evaluation = evaluate_answer(
                                    st.session_state.current_question,
                                    edited_answer,
                                    st.session_state.resume_text,
                                    st.session_state.job_description
                                )

                                st.session_state.evaluation = evaluation

                            st.success(
                                "Evaluation complete!"
                            )

                # -----------------------------
                # FOLLOW UP
                # -----------------------------

                with col2:

                    if st.button(
                        "🔥 Ask Follow-up",
                        use_container_width=True
                    ):

                        with st.spinner(
                            "🤔 Preparing a deeper question..."
                        ):

                            follow_up = generate_follow_up(
                                st.session_state.current_question,
                                edited_answer,
                                st.session_state.resume_text
                            )

                        st.session_state.current_question = follow_up
                        st.session_state.evaluation = ""

                        # Clear previous answer
                        st.session_state.voice_transcript = ""

                        st.rerun()

            # -----------------------------
            # EVALUATION
            # -----------------------------

            if st.session_state.get(
                "evaluation"
            ):

                st.markdown("---")

                st.markdown(
                    "### 📊 Interview Feedback"
                )

                st.markdown(
                    st.session_state.evaluation
                )