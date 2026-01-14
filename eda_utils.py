import pandas as pd
import numpy as np


def individual_data(df: pd.DataFrame, name: str) -> pd.DataFrame:
    student_df = pd.DataFrame(data=df[df["student_name"] == name])
    student_df["session_date"] = pd.to_datetime(student_df["session_date"])
    return student_df


def build_report(df: pd.DataFrame):
    student_df = df.groupby("student_name").agg(list).reset_index()
    student_df["average"] = student_df["progress_score"].apply(np.mean) * 10
    return student_df
