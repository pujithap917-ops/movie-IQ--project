import streamlit as st
import pandas as pd

st.set_page_config(page_title="Movie Revenue Analysis", layout="wide")

st.title("🎬 Movie Revenue Analysis Dashboard")

df = pd.read_csv("movies.csv")

st.subheader("Dataset Preview")

st.dataframe(df) import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Movie Revenue Analysis Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Revenue Analysis Dashboard")
st.markdown("---")

# ---------------------------------------
# Load Dataset
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    df = df.drop_duplicates()
    return df

df = load_data()

# ---------------------------------------
# Sidebar Filters
# ---------------------------------------
st.sidebar.header("Filters")

genres = sorted(df["genres"].dropna().unique())

selected_genres = st.sidebar.multiselect(
    "Select Genre",
    genres,
    default=genres
)

filtered_df = df[df["genres"].isin(selected_genres)]

budget_range = st.sidebar.slider(
    "Budget Range",
    int(filtered_df["budget"].min()),
    int(filtered_df["budget"].max()),
    (
        int(filtered_df["budget"].min()),
        int(filtered_df["budget"].max())
    )
)

filtered_df = filtered_df[
    (filtered_df["budget"] >= budget_range[0]) &
    (filtered_df["budget"] <= budget_range[1])
]

rating = st.sidebar.slider(
    "Minimum Rating",
    float(filtered_df["vote_average"].min()),
    float(filtered_df["vote_average"].max()),
    float(filtered_df["vote_average"].min())
)

filtered_df = filtered_df[
    filtered_df["vote_average"] >= rating
]

# ---------------------------------------
# Dataset Preview
# ---------------------------------------
st.header("Dataset Preview")
st.dataframe(filtered_df)

# ---------------------------------------
# KPI Cards
# ---------------------------------------
st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Movies", len(filtered_df))
col2.metric("Average Revenue",
            f"${filtered_df['revenue'].mean():,.0f}")
col3.metric("Average Budget",
            f"${filtered_df['budget'].mean():,.0f}")
col4.metric("Average Rating",
            round(filtered_df["vote_average"].mean(),2))

st.markdown("---")

# ---------------------------------------
# Top Revenue Movies
# ---------------------------------------
st.subheader("Top 10 Revenue Movies")

top_movies = filtered_df.nlargest(10,"revenue")

fig = px.bar(
    top_movies,
    x="title",
    y="revenue",
    color="revenue",
    title="Top Revenue Movies"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------
# Revenue by Genre
# ---------------------------------------
st.subheader("Revenue by Genre")

genre_df = filtered_df.groupby("genres",as_index=False)["revenue"].mean()

fig = px.bar(
    genre_df,
    x="genres",
    y="revenue",
    color="revenue",
    title="Average Revenue by Genre"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------
# Budget vs Revenue
# ---------------------------------------
st.subheader("Budget vs Revenue")

fig = px.scatter(
    filtered_df,
    x="budget",
    y="revenue",
    color="vote_average",
    hover_name="title",
    size="popularity",
    title="Budget vs Revenue"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------
# Popularity vs Revenue
# ---------------------------------------
st.subheader("Popularity vs Revenue")

fig = px.scatter(
    filtered_df,
    x="popularity",
    y="revenue",
    color="vote_average",
    hover_name="title"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------
# Runtime Distribution
# ---------------------------------------
st.subheader("Runtime Distribution")

fig = px.histogram(
    filtered_df,
    x="runtime",
    nbins=25,
    title="Runtime Distribution"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------
# Rating Distribution
# ---------------------------------------
st.subheader("Rating Distribution")

fig = px.histogram(
    filtered_df,
    x="vote_average",
    nbins=20,
    title="Movie Ratings"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------
# Business Insights
# ---------------------------------------
st.header("Business Insights")

highest_revenue = filtered_df.loc[
    filtered_df["revenue"].idxmax(),
    "title"
]

highest_budget = filtered_df.loc[
    filtered_df["budget"].idxmax(),
    "title"
]

st.success(f"Highest Revenue Movie : {highest_revenue}")
st.success(f"Highest Budget Movie : {highest_budget}")

st.write("• Higher-budget movies generally generate higher revenue.")
st.write("• Popular movies tend to earn more revenue.")
st.write("• Highly rated movies usually attract more audience.")
st.write("• Some low-budget movies also perform exceptionally well.")

# ---------------------------------------
# Business Recommendations
# ---------------------------------------
st.header("Business Recommendations")

st.info("Invest more in genres with consistently high revenue.")
st.info("Plan budgets based on historical movie performance.")
st.info("Increase marketing for movies with high popularity potential.")
st.info("Study successful low-budget movies for better ROI.")
st.info("Focus on producing highly rated content.")
