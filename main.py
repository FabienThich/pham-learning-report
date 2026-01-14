import streamlit as st
from eda_utils import *
from config import *

st.set_page_config(
    page_title="Pham Learning Report",
    layout="wide",
    initial_sidebar_state="auto",
)

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
