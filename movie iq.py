import streamlit as st
import pickle
import pandas as pd




st.title("MovieIQ")
st.write("Predict Movie Success")

try:
    model = pickle.load(open("model.pkl", "rb"))
    st.success("Model loaded successfully")
except Exception as e:
    st.error(f"Error: {e}")

budget = st.number_input("Budget")
runtime = st.number_input("Runtime")
rating = st.number_input("Rating")

if st.button("Predict"):
    st.write("Budget:", budget)
    st.write("Runtime:", runtime)
    st.write("Rating:", rating)

    import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import ast

# 1. Project Title & Configuration
st.set_page_config(page_title="Movie Revenue Analysis Dashboard", layout="wide")
st.title("Movie Revenue Analysis Dashboard") #

# 2. Data Loading & Cleaning
@st.cache_data
def load_data():
    # Load the specific dataset requested
    df = pd.read_csv("movies.csv")
    
    # Extract genre names from the dictionary string
    def extract_genres(genre_str):
        try:
            # Safely evaluate the string into a list of dictionaries
            genres = ast.literal_eval(genre_str)
            return [g['name'] for g in genres]
        except:
            return ["Unknown"]
            
    df['genre_list'] = df['genres'].apply(extract_genres)
    
    # Explode the dataset to handle the one-to-many relationship between movies and genres
    df_exploded = df.explode('genre_list')
    return df, df_exploded

df, df_exploded = load_data()

# 3. Sidebar Filters
st.sidebar.header("Dashboard Filters")
all_genres = sorted(df_exploded['genre_list'].dropna().unique())
# Genre filter allowing multiple selections[cite: 2]
selected_genres = st.sidebar.multiselect("Select Genre", all_genres, default=all_genres[:5])

# Apply Filter
if selected_genres:
    filtered_df = df_exploded[df_exploded['genre_list'].isin(selected_genres)]
else:
    filtered_df = df_exploded

# Remove duplicates if a movie has multiple genres within the current filter
unique_movies_df = filtered_df.drop_duplicates(subset=['title'])

# 4. KPI Cards
st.header("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

# Calculate metrics[cite: 2]
total_movies = unique_movies_df['title'].count()
avg_revenue = unique_movies_df['revenue'].mean()
avg_budget = unique_movies_df['budget'].mean()
avg_rating = unique_movies_df['vote_average'].mean()

col1.metric("Total Movies", f"{total_movies:,}")
col2.metric("Average Revenue", f"${avg_revenue:,.0f}")
col3.metric("Average Budget", f"${avg_budget:,.0f}")
col4.metric("Average Rating", f"{avg_rating:.1f}/10")

# 5. Dataset Preview
st.subheader("Dataset Preview")
# Display the movie data[cite: 2]
st.dataframe(unique_movies_df[['title', 'budget', 'revenue', 'popularity', 'runtime', 'vote_average', 'genre_list']].head(10))

# 6. Interactive Charts
st.header("Exploratory Data Analysis")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Top 10 Revenue Movies[cite: 2]
    top_10 = unique_movies_df.nlargest(10, 'revenue')
    fig_top10 = px.bar(top_10, x='revenue', y='title', orientation='h', title="Top 10 Movies by Revenue")
    fig_top10.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top10, use_container_width=True)
    
    # Budget vs Revenue Scatter[cite: 2]
    fig_scatter = px.scatter(unique_movies_df, x='budget', y='revenue', size='popularity', hover_name='title', title="Budget vs Revenue (Sized by Popularity)")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Runtime Distribution[cite: 2]
    fig_runtime = px.histogram(unique_movies_df, x='runtime', nbins=30, title="Runtime Distribution")
    st.plotly_chart(fig_runtime, use_container_width=True)

with col_chart2:
    # Revenue by Genre[cite: 2]
    genre_revenue = filtered_df.groupby('genre_list')['revenue'].mean().reset_index()
    fig_genre = px.bar(genre_revenue, x='genre_list', y='revenue', title="Average Revenue by Genre")
    st.plotly_chart(fig_genre, use_container_width=True)
    
    # Popularity vs Revenue[cite: 2]
    fig_pop = px.scatter(unique_movies_df, x='popularity', y='revenue', hover_name='title', title="Popularity vs Revenue")
    st.plotly_chart(fig_pop, use_container_width=True)
    
    # Rating Distribution[cite: 2]
    fig_rating = px.histogram(unique_movies_df, x='vote_average', nbins=30, title="Rating Distribution")
    st.plotly_chart(fig_rating, use_container_width=True)

# 7. Business Insights & Recommendations
st.header("Executive Summary")
tab1, tab2 = st.tabs(["Business Insights", "Recommendations"])

with tab1:
    st.markdown("""
    * **Action movies generate high revenue.**[cite: 2]
    * **High-budget movies often earn more revenue.**[cite: 2]
    * **Some low-budget movies are also successful.**[cite: 2]
    * **Popular movies generally earn more.**[cite: 2]
    * **Highly rated movies attract audiences.**[cite: 2]
    """)

with tab2:
    st.markdown("""
    * **Invest more in profitable genres.**[cite: 2]
    * **Plan budgets based on historical performance.**[cite: 2]
    * **Improve marketing for movies with high audience interest.**[cite: 2]
    * **Study successful low-budget movies.**[cite: 2]
    * **Focus on genres with consistently good ratings.**[cite: 2]
    """)









 