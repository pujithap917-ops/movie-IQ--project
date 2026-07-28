import streamlit as st
import pandas as pd

st.set_page_config(page_title="Movie Revenue Analysis", layout="wide")

st.title("🎬 Movie Revenue Analysis Dashboard")

df = pd.read_csv("movies.csv")

st.subheader("Dataset Preview")

st.dataframe(df)