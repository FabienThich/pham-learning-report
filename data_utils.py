import pandas as pd
import streamlit as st

def load_data():
  df = pd.read_csv(st.secrets['DATASET'])
  # df['session_date'] = pd.to_datetime[df['session_date']]

  return df