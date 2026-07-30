import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Revenue Analysis", layout="wide")

st.title("🎬 Movie Revenue Analysis Dashboard")

df = pd.read_csv("movies.csv")

st.subheader("Dataset Preview")
st.dataframe(df)

st.divider()

# KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Movies", len(df))
col2.metric("Average Rating", round(df["vote_average"].mean(), 2))
col3.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")

st.divider()

# Revenue Chart
fig1 = px.bar(
    df.head(10),
    x="title",
    y="revenue",
    title="Top 10 Movies Revenue"
)
st.plotly_chart(fig1, use_container_width=True)

# Budget vs Revenue
fig2 = px.scatter(
    df,
    x="budget",
    y="revenue",
    color="vote_average",
    hover_name="title",
    title="Budget vs Revenue"
)
st.plotly_chart(fig2, use_container_width=True)

# Ratings Distribution
fig3 = px.histogram(
    df,
    x="vote_average",
    nbins=20,
    title="Movie Ratings Distribution"
)
st.plotly_chart(fig3, use_container_width=True


