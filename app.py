
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Ahimsa Fellowship | Learning Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- SAMPLE DATA ----------

FELLOWS = [
    {"name": "Aarav Mehta", "progress": 72, "attendance": 90, "quiz": 85},
    {"name": "Mira Shah", "progress": 58, "attendance": 85, "quiz": 78},
    {"name": "Kabir Rao", "progress": 91, "attendance": 96, "quiz": 92},
    {"name": "Tara Sen", "progress": 43, "attendance": 75, "quiz": 68},
]

CURRICULUM = {
    "Month 1 – Foundations": {
        "Week 1 – Introduction to Animal Advocacy": {
            "Day 1 – Theory": [
                "Introduction to animal advocacy",
                "The moral status of animals",
                "Understanding animal sentience"
            ],
            "Day 2 – Theory": [
                "History of the animal protection movement",
                "Animal welfare and animal rights",
                "Introduction to evidence-based advocacy"
            ],
            "Day 3 – Practical": [
                "Mapping the animal advocacy ecosystem",
                "Stakeholder identification exercise"
            ]
        },
        "Week 2 – Understanding Animal Welfare": {
            "Day 1 – Theory": [
                "The Five Domains Model",
                "Animal welfare assessment"
            ],
            "Day 2 – Theory": [
                "Farmed animal welfare",
                "Companion animal welfare"
            ],
            "Day 3 – Practical": [
                "Case study analysis",
                "Developing an animal welfare assessment"
            ]
        }
    },
    "Month 2 – Research and Evidence": {
        "Week 1 – Research Methods": {
            "Day 1 – Theory": [
                "Introduction to research methods",
                "Qualitative and quantitative research"
            ],
            "Day 2 – Theory": [
                "Evidence synthesis",
                "Evaluating research quality"
            ],
            "Day 3 – Practical": [
                "Research question development",
                "Literature review exercise"
            ]
        }
    },
    "Month 3 – Advocacy and Implementation": {
        "Week 1 – Advocacy Strategies": {
            "Day 1 – Theory": [
                "Campaign strategy and theory of change",
                "Institutional and policy advocacy"
            ],
            "Day 2 – Theory": [
                "Coalition building",
                "Communication and public engagement"
            ],
            "Day 3 – Practical": [
                "Designing an advocacy campaign",
                "Presentation and peer feedback"
            ]
        }
    }
}

# ---------- SESSION STATE ----------

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "assignment_submitted" not in st.session_state:
    st.session_state.assignment_submitted = False

if "grievances" not in st.session_state:
    st.session_state.grievances = []

if "assignments" not in st.session_state:
    st.session_state.assignments = []


# ---------- DESIGN ----------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --forest: #193D32;
    --forest-light: #285B49;
    --ivory: #F7F5EF;
    --gold: #B69A60;
    --charcoal: #303833;
    --muted: #788078;
    --border: #E6E3D9;
}

.stApp {
    background: var(--ivory);
    font-family: 'DM Sans', sans-serif;
    color: var(--charcoal);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: var(--forest);
    border-right: 1px solid #315747;
}

[data-testid="stSidebar"] * {
    color: #F7F5EF !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #D2DED5 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #476556;
}

[data-testid="stSidebar"] label {
    color: #E7EDE8 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent;
    border-radius: 7px;
    padding: 7px 10px;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #285B49;
}

.portal-header {
    background: var(--forest);
    padding: 32px 36px;
    border-radius: 12px;
    color: white;
    margin-bottom: 30px;
    border-bottom: 3px solid var(--gold);
}

.portal-header h1 {
    color: white;
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 34px;
    font-weight: 600;
    margin-bottom: 6px;
}

.portal-header p {
    color: #DCE6DE;
    font-size: 14px;
    margin-bottom: 0;
    letter-spacing: 0.3px;
}

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--forest) !important;
}

h2 {
    font-size: 27px !important;
}

h3 {
    font-size: 21px !important;
}

p, li, label {
    font-family: 'DM Sans', sans-serif;
}

.info-card {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 10px;
    border: 1px solid var(--border);
    border-top: 3px solid var(--gold);
    min-height: 120px;
    box-shadow: 0 2px 8px rgba(30, 50, 35, 0.03);
}

.info-card h3 {
    color: var(--forest) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 29px;
    font-weight: 700;
    margin: 0 0 7px 0;
}

.info-card p {
    color: var(--muted);
    font-size: 13px;
    margin: 0;
}

.stButton > button,
.stFormSubmitButton > button {
    background: var(--forest);
    color: white;
    border: 1px solid var(--forest);
    border-radius: 7px;
    padding: 8px 20px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: var(--forest-light);
    border-color: var(--forest-light);
    color: white;
}

.stProgress > div > div > div {
    background-color: var(--forest-light);
}

[data-testid="stMetric"] {
    background: white;
    padding: 17px;
    border: 1px solid var(--border);
    border-radius: 9px;
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
}

[data-testid="stMetricValue"] {
    color: var(--forest);
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 9px;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stNumberInput input {
    background: white;
    border-radius: 7px;
}

.stTabs [data-baseweb="tab"] {
    color: var(--forest);
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    border-bottom-color: var(--gold) !important;
}

div[data-testid="stExpander"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
}

[data-testid="stAlert"] {
    border-radius: 8px;
}

hr {
    border-color: var(--border);
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## 🌿 AHIMSA")
    st.caption("FELLOWSHIP LEARNING PORTAL")
    st.divider()

    role = st.selectbox(
        "Demo user role",
        ["Fellow", "Faculty", "Programme Director"]
    )

    st.divider()

    if role == "Fellow":
        pages = [
            "My Dashboard",
            "Curriculum & Learning",
            "Quizzes",
            "Assignments",
            "Feedback & Grievances"
        ]
    elif role == "Faculty":
        pages = [
            "Faculty Dashboard",
            "Curriculum & Learning",
            "Quizzes",
            "Assignments",
            "Feedback & Grievances"
        ]
    else:
        pages = [
            "Programme Dashboard",
            "Curriculum & Learning",
            "Assignments",
            "Feedback & Grievances"
        ]

    page = st.radio("NAVIGATION", pages)

    st.divider()
    st.caption("Demonstration environment")
    st.caption("January 2027 Cohort")

# ---------- HEADER ----------

st.markdown("""
<div class="portal-header">
    <h1>Ahimsa Fellowship</h1>
    <p>Applied Animal Advocacy Certificate Programme · Learning Portal</p>
</div>
""", unsafe_allow_html=True)

# ---------- FELLOW DASHBOARD ----------

if page == "My Dashboard":
    st.markdown("## Welcome back, Ananya 👋")
    st.write("Here is your learning overview.")

    c1, c2, c3, c4 = st.columns(4)

    for col, number, label in [
        (c1, "72%", "Programme progress"),
        (c2, "85%", "Quiz average"),
        (c3, "90%", "Attendance"),
        (c4, "3", "Pending activities")
    ]:
        with col:
            st.markdown(
                f'<div class="info-card"><h3>{number}</h3><p>{label}</p></div>',
                unsafe_allow_html=True
            )

    st.markdown("### My learning progress")
    st.progress(0.72)
    st.caption("72% of the programme completed")

    left, right = st.columns(2)

    with left:
        st.markdown("### Upcoming activities")
        st.info("**5 November** – Animal Welfare Assessment")
        st.info("**7 November** – Week 2 Quiz")
        st.info("**10 November** – Practical Assignment")

    with right:
        st.markdown("### Continue learning")
        st.write("**Month 1 · Week 2**")
        st.write("Understanding Animal Welfare")
        if st.button("Open current week"):
            st.session_state.open_week = True
            st.info("Go to Curriculum & Learning in the sidebar.")

    
    st.divider()

    st.markdown("### Programme announcements")

    announcements = [
        ("Programme orientation", "Welcome to the Ahimsa Fellowship. Orientation details and joining instructions will be shared here."),
        ("Week 2 learning materials", "The additional reading materials for Understanding Animal Welfare are now available."),
        ("Upcoming practical session", "Please review the preparation materials before the next practical session.")
    ]

    for title, message in announcements:
        with st.expander(title):
            st.write(message)

    st.divider()

    st.markdown("### Monthly discussion threads")

    thread = st.selectbox(
        "Select a discussion thread",
        [
            "Month 1 – Foundations of Animal Advocacy",
            "Month 2 – Research and Evidence",
            "Month 3 – Advocacy and Implementation"
        ]
    )

    st.write(f"**{thread}**")
    st.caption("Share reflections and engage with fellow learners.")

    if "discussion_posts" not in st.session_state:
        st.session_state.discussion_posts = []

    with st.form("discussion_form"):
        post = st.text_area(
            "Your contribution",
            placeholder="Share a question, reflection or observation..."
        )
        post_submit = st.form_submit_button("Post contribution")

    if post_submit:
        if post.strip():
            st.session_state.discussion_posts.append({
                "thread": thread,
                "author": "Ananya Sharma",
                "message": post
            })
            st.success("Your contribution has been posted in this demonstration.")
        else:
            st.warning("Please enter a contribution.")

    for item in st.session_state.discussion_posts:
        if item["thread"] == thread:
            with st.container(border=True):
                st.caption(item["author"])
                st.write(item["message"])

    st.markdown("### Programme themes")
    st.write(
        "Animal Welfare · Evidence-Based Advocacy · "
        "Policy and Institutional Change"
    )

# ---------- FACULTY DASHBOARD ----------

elif page == "Faculty Dashboard":
    st.markdown("## Faculty Dashboard")
    st.write("Teaching overview and learner engagement.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Active fellows", "24")
    c2.metric("Assignments awaiting review", "8")
    c3.metric("Upcoming sessions", "3")

    st.markdown("### Recent learner activity")
    activity = pd.DataFrame([
        ["Ananya Sharma", "Week 1 Quiz", "Submitted"],
        ["Rohan Mehta", "Policy Brief", "Awaiting review"],
        ["Sara Khan", "Field Report", "Submitted"],
        ["Dev Patel", "Week 2 Quiz", "Not attempted"],
    ], columns=["Fellow", "Activity", "Status"])

    st.dataframe(activity, use_container_width=True, hide_index=True)


# ---------- PROGRAMME DASHBOARD ----------

elif page == "Programme Dashboard":
    st.markdown("## Programme Management")
    st.write(
        "Cohort monitoring, learner progress and programme administration."
    )

    # Cohort overview
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Enrolled fellows", "24")
    c2.metric("Average progress", "66%")
    c3.metric("Average attendance", "87%")
    c4.metric("Pending reviews", "8")

    st.divider()

    # Cohort performance
    st.markdown("### Fellow progress and performance")

    df = pd.DataFrame(FELLOWS)
    df.columns = [
        "Fellow",
        "Progress (%)",
        "Attendance (%)",
        "Quiz average (%)"
    ]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Cohort progress")
    st.bar_chart(
        df.set_index("Fellow")["Progress (%)"]
    )

    st.divider()

    # Assignment management
    st.markdown("### Assignment review")

    assignment_data = pd.DataFrame([
        ["Ananya Sharma", "Policy Brief", "Submitted", "Awaiting review"],
        ["Rohan Mehta", "Field Report", "Submitted", "Under review"],
        ["Sara Khan", "Campaign Plan", "Submitted", "Reviewed"],
        ["Dev Patel", "Policy Brief", "Pending", "Not submitted"]
    ], columns=[
        "Fellow",
        "Assignment",
        "Submission",
        "Review status"
    ])

    st.dataframe(
        assignment_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Grievance management
    st.markdown("### Grievance management")
    st.caption(
        "Illustrative workflow only. This is not a secure operational "
        "grievance management system."
    )

    grievance_data = pd.DataFrame([
        ["AHM-1001", "Academic", "Received", "Programme Director"],
        ["AHM-1002", "Administrative", "Under review", "Programme Admin"],
        ["AHM-1003", "Conduct", "Escalated", "Designated Escalation Officer"]
    ], columns=[
        "Ticket",
        "Category",
        "Status",
        "Assigned to"
    ])

    st.dataframe(
        grievance_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Announcements
    st.markdown("### Programme announcements")

    announcements = [
        ("Programme orientation", "Welcome session and programme introduction."),
        ("Week 2 reading materials", "Additional reading materials have been added."),
        ("Upcoming practical session", "Please review the preparation instructions.")
    ]

    for title, description in announcements:
        with st.expander(title):
            st.write(description)

    st.divider()

    st.markdown("### Publish an announcement")

    with st.form("announcement_form"):
        announcement_title = st.text_input("Announcement title")
        announcement_message = st.text_area("Announcement message")
        audience = st.selectbox(
            "Audience",
            ["Entire cohort", "Faculty", "Fellows"]
        )
        publish = st.form_submit_button("Publish announcement")

    if publish:
        if announcement_title.strip() and announcement_message.strip():
            st.success(
                f"Demonstration announcement prepared for: {audience}"
            )
        else:
            st.warning("Please complete the announcement title and message.")


# ---------- CURRICULUM ----------

elif page == "Curriculum & Learning":
    st.markdown("## Curriculum & Learning")
    st.write(
        "Your structured learning pathway across the "
        "Ahimsa Fellowship programme."
    )

    month = st.selectbox(
        "Programme month",
        list(CURRICULUM.keys())
    )

    week = st.selectbox(
        "Learning week",
        list(CURRICULUM[month].keys())
    )

    day = st.selectbox(
        "Session",
        list(CURRICULUM[month][week].keys())
    )

    # Session descriptions
    SESSION_DETAILS = {
        "Day 1 – Theory": {
            "type": "THEORY SESSION",
            "description": (
                "Build foundational knowledge through structured "
                "instruction, guided readings and discussion."
            ),
            "objectives": [
                "Understand key concepts and terminology",
                "Engage critically with relevant evidence",
                "Connect theoretical ideas with animal advocacy practice"
            ]
        },
        "Day 2 – Theory": {
            "type": "THEORY SESSION",
            "description": (
                "Explore the subject in greater depth through "
                "case studies, academic material and guided discussion."
            ),
            "objectives": [
                "Examine different perspectives and approaches",
                "Evaluate supporting evidence",
                "Identify implications for advocacy practice"
            ]
        },
        "Day 3 – Practical": {
            "type": "PRACTICAL SESSION",
            "description": (
                "Apply the concepts introduced during the week "
                "through exercises, case analysis and practical work."
            ),
            "objectives": [
                "Apply learning to a practical advocacy challenge",
                "Develop analytical and problem-solving skills",
                "Reflect on learning and identify areas for improvement"
            ]
        }
    }

    details = SESSION_DETAILS.get(day, SESSION_DETAILS["Day 1 – Theory"])

    st.divider()

    st.caption(f"{month}  /  {week}")

    st.markdown(f"### {day}")

    if details["type"] == "PRACTICAL SESSION":
        st.markdown(
            '<span style="background:#E9E2CE;color:#66532B;'
            'padding:5px 12px;border-radius:15px;font-size:11px;'
            'font-weight:700;letter-spacing:1px;">'
            'PRACTICAL SESSION</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span style="background:#E2EDE5;color:#285B49;'
            'padding:5px 12px;border-radius:15px;font-size:11px;'
            'font-weight:700;letter-spacing:1px;">'
            'THEORY SESSION</span>',
            unsafe_allow_html=True
        )

    st.markdown("#### About this session")
    st.write(details["description"])

    st.markdown("#### Learning objectives")
    for objective in details["objectives"]:
        st.markdown(f"- {objective}")

    st.markdown("#### Topics covered")
    for topic in CURRICULUM[month][week][day]:
        st.markdown(f"- {topic}")

    st.divider()

    st.markdown("### Learning resource library")
    st.caption("Resources organised by session and material type.")

    resources = [
        {
            "name": "Session reading",
            "type": "PDF",
            "description": "Core reading material for the session.",
            "size": "Sample resource"
        },
        {
            "name": "Lecture presentation",
            "type": "SLIDES",
            "description": "Faculty presentation and key concepts.",
            "size": "Sample resource"
        },
        {
            "name": "Additional reading",
            "type": "READING",
            "description": "Further academic and reference material.",
            "size": "Sample resource"
        },
        {
            "name": "Case study",
            "type": "CASE MATERIAL",
            "description": "Applied case material for critical analysis.",
            "size": "Sample resource"
        }
    ]

    for resource in resources:
        with st.expander(
            f"📄 {resource['name']}  ·  {resource['type']}"
        ):
            st.write(resource["description"])
            st.caption(resource["size"])
            st.info(
                "This is a sample resource entry. Actual documents "
                "will be uploaded by faculty."
            )

    st.divider()

    st.markdown("### Session completion")
    st.caption(
        "Mark the session complete after reviewing its learning materials."
    )

    completed = st.checkbox(
        "I have completed this learning session",
        key=f"completed_{month}_{week}_{day}"
    )

    if completed:
        st.success("Session marked as completed in this demonstration.")

# ---------- QUIZZES ----------
elif page == "Quizzes":
    st.markdown("## Knowledge Check")
    st.write("Sample quiz · Introduction to Animal Advocacy")

    st.info("This demonstration quiz contains three questions.")

    questions = [
        {
            "question": "What is the primary purpose of animal welfare science?",
            "options": [
                "To assess animals' experiences and welfare",
                "To study only animal behaviour",
                "To focus exclusively on human interests"
            ],
            "answer": "To assess animals' experiences and welfare",
            "explanation": "Animal welfare science examines animals' experiences, including their physical and mental states."
        },
        {
            "question": "What is evidence-based advocacy?",
            "options": [
                "Advocacy based only on personal opinion",
                "Advocacy informed by reliable evidence and research",
                "Advocacy without evaluating outcomes"
            ],
            "answer": "Advocacy informed by reliable evidence and research",
            "explanation": "Evidence-based advocacy uses research and relevant evidence to inform decisions and interventions."
        },
        {
            "question": "Which is an example of a practical advocacy activity?",
            "options": [
                "Stakeholder mapping",
                "Ignoring policy developments",
                "Avoiding evaluation"
            ],
            "answer": "Stakeholder mapping",
            "explanation": "Stakeholder mapping helps identify relevant actors, relationships and opportunities for advocacy."
        }
    ]

    with st.form("quiz_form"):
        answers = []
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i+1}. {q['question']}**")
            answer = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"quiz_{i}"
            )
            answers.append(answer)
            st.divider()

        submitted = st.form_submit_button("Submit quiz")

    if submitted:
        score = sum(
            answers[i] == questions[i]["answer"]
            for i in range(len(questions))
        )
        st.session_state.quiz_submitted = True
        st.session_state.quiz_score = score
        st.session_state.quiz_answers = answers

    if st.session_state.quiz_submitted:
        score = st.session_state.quiz_score
        st.success(f"You scored {score} out of 3 ({score / 3:.0%}).")

        for i, q in enumerate(questions):
            if st.session_state.quiz_answers[i] == q["answer"]:
                st.markdown(f"**Question {i+1}: Correct**")
            else:
                st.markdown(f"**Question {i+1}: Incorrect**")
                st.write(f"Correct answer: {q['answer']}")
            st.caption(q["explanation"])

        if st.button("Attempt again"):
            st.session_state.quiz_submitted = False
            st.rerun()

# ---------- ASSIGNMENTS ----------

elif page == "Assignments":
    st.markdown("## Assignments")
    st.write("Practical learning and applied advocacy exercises.")

    st.markdown("### Current assignment")
    st.info(
        "**Assignment: Develop an Animal Advocacy Policy Brief**\n\n"
        "Prepare a short policy brief identifying an animal welfare issue, "
        "the relevant stakeholders, supporting evidence and proposed actions."
    )

    st.markdown("### Assessment rubric")

    rubric = pd.DataFrame([
        ["Understanding of the issue", "25%"],
        ["Quality of evidence", "25%"],
        ["Analysis and recommendations", "30%"],
        ["Clarity and presentation", "20%"]
    ], columns=["Assessment criterion", "Weight"])

    st.dataframe(rubric, use_container_width=True, hide_index=True)

    st.markdown("### Submit your assignment")

    with st.form("assignment_form"):
        fellow_name = st.text_input("Fellow name", "Ananya Sharma")
        assignment_title = st.text_input(
            "Assignment title",
            "Animal Advocacy Policy Brief"
        )
        submission = st.text_area(
            "Submission summary",
            placeholder="Enter a short summary of your work..."
        )
        submitted = st.form_submit_button("Submit assignment")

    if submitted:
        if submission.strip():
            st.session_state.assignments.append({
                "Fellow": fellow_name,
                "Assignment": assignment_title,
                "Date": str(date.today()),
                "Status": "Submitted"
            })
            st.success("Demonstration submission received.")
        else:
            st.warning("Please enter a submission summary.")

    if role in ["Faculty", "Programme Director"]:
        st.markdown("### Submission overview")
        if st.session_state.assignments:
            st.dataframe(
                pd.DataFrame(st.session_state.assignments),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.caption("No demonstration submissions yet.")

# ---------- FEEDBACK AND GRIEVANCES ----------

elif page == "Feedback & Grievances":
    st.markdown("## Feedback & Grievances")
    st.write("A dedicated space for learner feedback and concerns.")

    feedback_tab, grievance_tab = st.tabs([
        "Session feedback",
        "Grievance redressal"
    ])

    with feedback_tab:
        st.markdown("### Share your feedback")
        with st.form("feedback_form"):
            session_name = st.text_input("Session or activity")
            rating = st.slider("How useful was this session?", 1, 5, 4)
            comments = st.text_area("Additional feedback")
            feedback_submit = st.form_submit_button("Submit feedback")

        if feedback_submit:
            st.success("Thank you. Your demonstration feedback has been recorded.")

    with grievance_tab:
        st.markdown("### Confidential grievance submission")
        st.warning(
            "Demonstration only. This form is not a secure or anonymous "
            "grievance channel and must not be used for real complaints."
        )

        with st.form("grievance_form"):
            category = st.selectbox(
                "Category",
                [
                    "Academic",
                    "Administrative",
                    "Conduct",
                    "Harassment",
                    "Other"
                ]
            )
            description = st.text_area("Describe your concern")
            anonymous = st.checkbox("Request anonymous handling")
            grievance_submit = st.form_submit_button("Submit demonstration grievance")

        if grievance_submit:
            if description.strip():
                ticket = f"AHM-{len(st.session_state.grievances)+1001}"
                st.session_state.grievances.append({
                    "Ticket": ticket,
                    "Category": category,
                    "Status": "Received"
                })
                st.success(f"Demonstration ticket generated: {ticket}")
            else:
                st.warning("Please enter a description.")

        if role == "Programme Director" and st.session_state.grievances:
            st.markdown("### Demonstration grievance register")
            st.dataframe(
                pd.DataFrame(st.session_state.grievances),
                use_container_width=True,
                hide_index=True
            )

# ---------- FOOTER ----------

st.divider()
st.caption(
    "Ahimsa Fellowship Learning Portal · Proof of Concept · "
    "Sample data only · Not for operational use"
)
