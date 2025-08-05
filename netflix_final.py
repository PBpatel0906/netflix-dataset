# netflix_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'])
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    return df

df = load_data()

# ---- SIDEBAR ----
st.sidebar.header("🔍 Filter Options")
type_filter = st.sidebar.multiselect("Select Type", options=df['type'].unique(), default=df['type'].unique())
country_filter = st.sidebar.multiselect("Select Country", options=df['country'].dropna().unique(), default=["United States", "India"])
year_filter = st.sidebar.slider("Select Year Added", int(df['year_added'].min()), int(df['year_added'].max()), (2015, 2020))

# Apply filters
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter)) &
    (df['year_added'] >= year_filter[0]) &
    (df['year_added'] <= year_filter[1])
]

# ---- HEADER ----
st.title("🎬 Netflix Data Dashboard")
st.markdown("An interactive analysis of Netflix shows and movies dataset")

# ---- TABS ----
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🌍 Content by Country", "📅 Trends Over Time"])

# ---- TAB 1: OVERVIEW ----
with tab1:
    st.subheader("Top Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Titles", filtered_df.shape[0])
    col2.metric("Movies", filtered_df[filtered_df['type'] == "Movie"].shape[0])
    col3.metric("TV Shows", filtered_df[filtered_df['type'] == "TV Show"].shape[0])

    st.markdown("---")
    st.subheader("🎭 Top Genres")
    df['listed_in'] = df['listed_in'].fillna("Unknown")
    all_genres = df['listed_in'].str.split(', ', expand=True).stack()
    genre_counts = all_genres.value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']

    fig_genres = px.bar(genre_counts.head(10), x='Count', y='Genre', orientation='h', title="Top 10 Genres", height=400)
    st.plotly_chart(fig_genres, use_container_width=True)

# ---- TAB 2: CONTENT BY COUNTRY ----
with tab2:
    st.subheader("🌍 Number of Titles by Country")

    country_counts = filtered_df['country'].value_counts().head(15).reset_index()
    country_counts.columns = ['Country', 'Count']

    fig_country = px.bar(country_counts, x='Country', y='Count', title="Top 15 Countries with Most Titles")
    st.plotly_chart(fig_country, use_container_width=True)

# ---- TAB 3: TRENDS OVER TIME ----
with tab3:
    st.subheader("📅 Titles Added Over the Years")

    yearly = filtered_df.groupby('year_added').size().reset_index(name='Count')
    fig_year = px.line(yearly, x='year_added', y='Count', markers=True, title="Content Added Per Year")
    st.plotly_chart(fig_year, use_container_width=True)

    st.subheader("📈 Monthly Additions")
    monthly = filtered_df.groupby('month_added').size().reset_index(name='Count')
    fig_month = px.bar(monthly, x='month_added', y='Count', title="Content Added by Month", labels={'month_added': 'Month'})
    st.plotly_chart(fig_month, use_container_width=True)

# ---- FOOTER ----
st.markdown("---")

#st.markdown("Built with ❤ by [Your Name](https://www.linkedin.com/in/yourprofile) | Data Source: Netflix Dataset")
