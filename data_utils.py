import pandas as pd
import streamlit as st
import io


def load_data():
    df = pd.read_csv(io.StringIO(st.secrets["DATA"]))
    df.drop(
        columns=["Column 8", "Upload 1 to 3 pages of the student's work here"],
        inplace=True,
    )
    df.rename(
        columns={
            "Timestamp": "session_date",
            "Student's Name": "student_name",
            "The topic the student is learning in school or working in the centre: (In one sentence write specific example Eg. I learn 2 digits by 1 digit multiplication such as 23 x 5)": "subject_topic",
            "Tutor's Note (write one or more sentences of how the student is doing and the topic the student is learning in school or working in the centre: ( Eg. I learn 2 digits by 1 digit multiplication such as 23 x 5)": "tutor_notes",
            "Email Address": "student_email",
            "On a scale from 1 to 10, how would you rate the student's performance at the tutoring centre today?\"\n(1 = Very Poor, 10 = Excellent)": "progress_score",
        },
        inplace=True,
    )
    df["student_name"] = df["student_name"].astype(str)
    df["subject_topic"] = df["subject_topic"].astype(str)
    df["tutor_notes"] = df["tutor_notes"].astype(str)
    df["student_email"] = df["student_email"].astype(str)
    df["progress_score"] = df["progress_score"].astype(float)
    df["session_date"] = pd.to_datetime(df["session_date"])

    return df