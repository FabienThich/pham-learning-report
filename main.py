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
)

st.set_page_config(
    page_title=PAGE_TITLE,
    layout=LAYOUT,
    page_icon=PAGE_ICON,
    initial_sidebar_state=SIDEBAR_STATE,
)

data = load_data()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

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
    if st.button("🔒 Logout"):
        st.session_state.authenticated = False
        st.session_state.student_name = ""
        st.rerun()

student_name = st.session_state.input_name
student_data = individual_data(data, student_name)
student_report = build_report(student_data)
average_score = round(student_report["average"].iloc[0], 1)

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

    spacer_left, col1, col2, col3, spacer_right = st.columns([1, 2, 2, 2, 1])

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

    # col3.metric(
    #     label="⏱️ Total Tutoring Time",
    #     value=int(total_tutor_time),
    #     # update this below
    #     delta=total_tutor_time_status,
    #     delta_color=total_tutor_time_status_color,
    #     border=True,
    # )

# use matplotlib
# st.line_chart(student_data, x="session_date", y="progress_score")
