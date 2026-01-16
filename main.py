import streamlit as st
import pandas as pd
from eda_utils import individual_data, build_report
from data_utils import load_data
from config import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    SIDEBAR_STATE,
    SCORE_GOOD,
    SCORE_BAD,
    SUBJECT_COLOURS,
)

st.set_page_config(
    page_title=PAGE_TITLE,
    layout=LAYOUT,
    page_icon=PAGE_ICON,
    initial_sidebar_state=SIDEBAR_STATE,
)

# st.markdown(
#     """
#     <style>
#     #MainMenu {visibility: hidden;}
#     header {visibility: hidden;}
#     footer {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

data = load_data()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.container():
        spacer_left, col, spacer_right = st.columns([2, 3, 2])

        with col:
            with st.form("login_form"):
                first_name = st.text_input("Student First Name")
                last_name = st.text_input("Student Last Name")
                submitted = st.form_submit_button("View Dashboard")

            if submitted:
                input_name = f"{first_name.strip()} {last_name.strip()}"

                student_rows = data[(data["student_name"] == input_name)]

                if student_rows.empty:
                    st.error("❌ Student not found. Please check the details.")
                    st.stop()

                st.session_state.authenticated = True
                st.session_state.input_name = input_name

                st.rerun()

        st.stop()

if st.session_state.authenticated:
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
        background-color: #1E90FF;
        color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🔒 Logout", key="logout"):
        st.session_state.authenticated = False
        st.session_state.student_name = ""
        st.rerun()

student_name = st.session_state.input_name
student_data = individual_data(data, student_name)
student_report = build_report(student_data)
average_score = round(student_report["average"].iloc[0], 1)

subject_colours = SUBJECT_COLOURS
subjects = student_data["subject_topic"].astype(str).unique()

session_attended_this_month = student_data[
    student_data["session_date"].dt.month == pd.Timestamp.today().month
].shape[0]
session_attended_last_month = student_data[
    (student_data["session_date"].dt.month == (pd.Timestamp.today().month - 1 or 12))
    & (
        student_data["session_date"].dt.year
        == (pd.Timestamp.today().year - (1 if pd.Timestamp.today().month == 1 else 0))
    )
].shape[0]


progress_status = (
    "Progressing Well"
    if average_score > SCORE_GOOD
    else "On Track" if average_score > SCORE_BAD else "Needs Improvement"
)

progress_status_color = (
    "normal"
    if average_score > SCORE_GOOD
    else "off" if average_score > SCORE_BAD else "off"
)

session_attended_status = f"{session_attended_last_month} Attended Last Month"

session_attended_status_color = "off"

with st.container():

    st.markdown(
        f"<h2 style='text-align: center;'> 📘 {student_name} — Progress Overview </h2>",
        unsafe_allow_html=True,
    )

    spacer_left, col1, col2, col3, spacer_right = st.columns([1, 1.5, 1.5, 1.5, 1])

    col1.metric(
        label="🗓️ Total Sessions Attended",
        value=int(session_attended_this_month),
        delta=session_attended_status,
        delta_color=session_attended_status_color,
        border=True,
    )

    col2.metric(
        label="📈 Average Progress Score",
        value=f"{average_score}%",
        delta=progress_status,
        delta_color=progress_status_color,
        border=True,
    )

    with col3:
        badge_html = ""

        for subject in subjects:
            colour = subject_colours.get(subject, "#6C757D")  # gray fallback
            badge_html += f"""
                <span style="
                    background-color:{colour};
                    display:flex;
                    color:white;
                    margin-top:2px;
                    padding:5px 12px;
                    border-radius:5px;
                    font-size:14px;
                    margin-right:8px;
                ">
                    {subject}
                </span>
            """
        st.markdown(badge_html, unsafe_allow_html=True)

    # use matplotlib
    # spacer_left, col1, col2, spacer_right = st.columns([1, 3, 3, 1])
    # with col1:
    #     st.line_chart(student_data, x="session_date", y="progress_score")
