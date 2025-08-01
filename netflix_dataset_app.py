import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide')
st.title("🎬 Netflix Data Analysis Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", [
    "Overview",
    "Content by Year",
    "Type Distribution",
    "Top Genres",
    "Top Actors",
    "India Insights",
    "Month & Quarter Trends",
    "Duration Analysis",
    "Movie vs TV Genres"
])

# --- 1. Overview ---
if options == "Overview":
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Country Distribution (Top 10)")
    top_countries = df['country'].value_counts().head(10)
    st.bar_chart(top_countries)

# --- 2. Content by Year ---
elif options == "Content by Year":
    content_peryear = df.groupby('year_added').size()
    fig, ax = plt.subplots()
    sns.lineplot(x=content_peryear.index, y=content_peryear.values, marker='o', ax=ax)
    ax.set_title("Year-wise Netflix Content Additions")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Titles")
    st.pyplot(fig)

# --- 3. Type Distribution ---
elif options == "Type Distribution":
    st.subheader("Content Type Distribution")
    fig, ax = plt.subplots()
    df['type'].value_counts().plot.pie(autopct='%0.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

# --- 4. Top Genres ---
elif options == "Top Genres":
    df['listed_in'] = df['listed_in'].astype(str)
    all_genres = df['listed_in'].str.split(', ').explode()
    top_genres = all_genres.value_counts().head(10)

    st.subheader("Top 10 Global Genres")
    st.bar_chart(top_genres)

# --- 5. Top Actors ---
elif options == "Top Actors":
    df['cast'] = df['cast'].astype(str)
    global_cast = df['cast'].str.split(', ').explode()
    top_actors = global_cast.value_counts().head(10)

    st.subheader("Top 10 Most Featured Actors")
    fig, ax = plt.subplots()
    top_actors.plot(kind='barh', ax=ax, color='slateblue')
    ax.set_xlabel("Appearances")
    ax.invert_yaxis()
    st.pyplot(fig)

# --- 6. India Insights ---
elif options == "India Insights":
    india_df = df[df['country'].astype(str).str.contains('India', na=False)]

    st.subheader("India: Year-wise Content Additions")
    india_years = india_df.groupby('year_added').size()
    fig, ax = plt.subplots()
    sns.lineplot(x=india_years.index, y=india_years.values, marker='o', ax=ax, color='green')
    st.pyplot(fig)

    st.subheader("Top Genres in India")
    india_genres = india_df['listed_in'].str.split(', ').explode().value_counts().head(10)
    st.bar_chart(india_genres)

    st.subheader("Top Actors in India")
    india_cast = india_df['cast'].str.split(', ').explode().value_counts().head(10)
    fig, ax = plt.subplots()
    india_cast.plot(kind='barh', ax=ax, color='darkorange')
    ax.invert_yaxis()
    st.pyplot(fig)

# --- 7. Month & Quarter Trends ---
elif options == "Month & Quarter Trends":
    df['month_added'] = df['date_added'].dt.month_name()
    df['quarter_added'] = df['date_added'].dt.quarter

    st.subheader("Month-wise Content Additions")
    month_counts = df['month_added'].value_counts().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    st.bar_chart(month_counts)

    st.subheader("Quarter-wise Content Additions")
    quarter_counts = df['quarter_added'].value_counts().sort_index()
    st.bar_chart(quarter_counts)

# --- 8. Duration Analysis ---
elif options == "Duration Analysis":
    movies_df = df[df['type'] == 'Movie'].copy()
    tv_df = df[df['type'] == 'TV Show'].copy()

    movies_df['minutes'] = movies_df['duration'].astype(str).str.extract('(\d+)').astype(float)
    tv_df['seasons'] = tv_df['duration'].astype(str).str.extract('(\d+)').astype(float)

    st.subheader("Movie Duration Distribution")
    fig, ax = plt.subplots()
    sns.histplot(movies_df['minutes'].dropna(), bins=30, kde=True, ax=ax, color='crimson')
    st.pyplot(fig)

    st.subheader("TV Show Season Count")
    fig, ax = plt.subplots()
    sns.countplot(x=tv_df['seasons'].dropna(), ax=ax)
    st.pyplot(fig)

    st.info(f"Average Movie Duration: {movies_df['minutes'].mean():.2f} minutes")
    st.info(f"Average Seasons in TV Shows: {tv_df['seasons'].mean():.2f}")

# --- 9. Movie vs TV Genres ---
elif options == "Movie vs TV Genres":
    movies_df = df[df['type'] == 'Movie'].copy()
    tv_df = df[df['type'] == 'TV Show'].copy()

    movie_genres = movies_df['listed_in'].str.split(', ').explode().value_counts().head(10)
    tv_genres = tv_df['listed_in'].str.split(', ').explode().value_counts().head(10)

    st.subheader("Top Genres in Movies")
    fig, ax = plt.subplots()
    sns.barplot(x=movie_genres.values, y=movie_genres.index, ax=ax, palette='Blues_d')
    st.pyplot(fig)

    st.subheader("Top Genres in TV Shows")
    fig, ax = plt.subplots()
    sns.barplot(x=tv_genres.values, y=tv_genres.index, ax=ax, palette='Oranges_d')
    st.pyplot(fig)