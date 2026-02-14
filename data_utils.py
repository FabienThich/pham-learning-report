import pandas as pd
import streamlit as st


def load_data():
    df = pd.read_csv('production.csv', usecols=range(7))
    df["student_name"] = df["student_name"].astype(str)
    df["subject_topic"] = df["subject_topic"].astype(str)
    df["tutor_notes"] = df["tutor_notes"].astype(str)
    df["student_email"] = df["student_email"].astype(str)
    df["progress_score"] = df["progress_score"].astype(float)
    df["session_date"] = pd.to_datetime(df["session_date"])

    return df
