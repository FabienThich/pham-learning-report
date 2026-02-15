import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
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
    CUSTOM_STOPWORDS,
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
    with st.container():
        spacer_left, col, spacer_right = st.columns([5, 1, 5])
        with col:
            st.image(
                "https://d3319dbeb6b402e32373.cdn6.editmysite.com/uploads/b/d3319dbeb6b402e323737239b0ee6f596f116c7c071babecae5ccf2e57bd640c/pham-learning-logo-transparent_1629744830.png?width=2400&optimize=medium",
                width=200,
            )
        spacer_left, col, spacer_right = st.columns([2, 3, 2])

        with col:
            with st.form("login_form"):
                first_name = st.text_input("Student First Name")
                last_name = st.text_input("Student Last Name")
                submitted = st.form_submit_button("View Dashboard")

            if submitted:
                input_name = f"{first_name.strip()}"
                # input_name = f"{first_name.strip()} {last_name.strip()}"

                student_rows = data[
                    data["student_name"].str.contains(input_name, case=False, na=False)
                ]

                if student_rows.empty:
                    st.error("❌ Student not found. Please check the details.")
                    st.stop()

                st.session_state.authenticated = True
                st.session_state.input_name = input_name

                st.rerun()

        st.stop()

student_name = st.session_state.input_name
student_data = individual_data(data, student_name)
student_report = build_report(student_data)

if student_report.empty or pd.isna(student_report["average"].iloc[0]):
    average_score = None
else:
    average_score = round(student_report["average"].iloc[0], 1)

subject_colours = SUBJECT_COLOURS
subjects = [s for s in student_report["subject_topic"].iloc[0] if s.lower() != "nan"]

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


if average_score is None:
    progress_status = "Not Available"
    progress_status_color = "off"
else:
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

    spacer_left, col_title, col_button = st.columns([0.5, 6, 0.5])
    with col_button:
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
    with col_title:
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
        value="N/A" if average_score is None else f"{average_score}%",
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
                    margin-right:0px;
                ">
                    {subject}
                </span>
            """
        st.markdown(badge_html, unsafe_allow_html=True)

        if not subjects:
            st.markdown("Subjects not available.")

    # use matplotlib
    spacer_left, col1, col2, spacer_right = st.columns([1, 2.25, 2.25, 1])
    with col1:
        if not student_data["progress_score"].isna().all():
            st.line_chart(student_data, x="session_date", y="progress_score")
        else:
            st.info("No progress score data available.")

    with col2:
        notes = student_report.get("tutor_notes", [])

        text = " ".join(
            str(n) for n in notes if pd.notna(n) and str(n).lower() != "nan"
        )

        if text.strip():

            custom_stopwords = set(CUSTOM_STOPWORDS)

            for name_part in student_name.lower().split():
                custom_stopwords.add(name_part)

            wc = WordCloud(
                width=500,
                height=300,
                background_color="#0E1117",
                colormap="coolwarm",
                max_words=10,
                stopwords=custom_stopwords,
            ).generate(text)

            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info("No tutor notes available.")
