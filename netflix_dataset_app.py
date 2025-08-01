import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.title("🎬 Netflix Interactive Data Dashboard")

# --- Load Data from local file ---
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month_name()
    df['quarter_added'] = df['date_added'].dt.quarter
    df['listed_in'] = df['listed_in'].astype(str)
    df['cast'] = df['cast'].astype(str)
    return df

try:
    df = load_data()
    st.success("✅ Dataset loaded successfully!")

    # --- Tabs for Dashboard Sections ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", 
        "📈 Year Trends", 
        "🌍 Country & Type", 
        "🎭 Genres & Actors", 
        "🕒 Time Trends", 
        "🎥 Durations"
    ])

    # --- Tab 1: Overview ---
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10))

        st.subheader("Top 10 Countries")
        top_countries = df['country'].value_counts().head(10)
        st.bar_chart(top_countries)

        st.subheader("Content Type Distribution")
        fig1, ax1 = plt.subplots()
        df['type'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1)
        ax1.set_ylabel("")
        st.pyplot(fig1)

    # --- Tab 2: Year Trends ---
    with tab2:
        st.subheader("Content Added Per Year")
        content_per_year = df['year_added'].value_counts().sort_index()
        st.line_chart(content_per_year)

        st.subheader("Content Released Per Year")
        release_trend = df['release_year'].value_counts().sort_index()
        st.area_chart(release_trend)

    # --- Tab 3: Country and Type ---
    with tab3:
        st.subheader("Top Countries by Content Type")
        grouped = df.groupby(['type', 'country']).size().reset_index(name='count')
        top_grouped = grouped.sort_values(by='count', ascending=False).head(20)
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        sns.barplot(data=top_grouped, x='country', y='count', hue='type', ax=ax2)
        ax2.set_title("Top Countries by Movies & TV Shows")
        st.pyplot(fig2)

    # --- Tab 4: Genres and Actors ---
    with tab4:
        st.subheader("Top 10 Global Genres")
        genres = df['listed_in'].str.split(', ').explode()
        top_genres = genres.value_counts().head(10)
        st.bar_chart(top_genres)

        st.subheader("Top 10 Global Actors")
        actors = df['cast'].str.split(', ').explode()
        top_actors = actors.value_counts().head(10)
        fig3, ax3 = plt.subplots()
        top_actors.plot(kind='barh', ax=ax3, color='skyblue')
        ax3.invert_yaxis()
        st.pyplot(fig3)

    # --- Tab 5: Month and Quarter Trends ---
    with tab5:
        st.subheader("Content Added by Month")
        month_counts = df['month_added'].value_counts().reindex([
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])
        st.bar_chart(month_counts)

        st.subheader("Content Added by Quarter")
        quarter_counts = df['quarter_added'].value_counts().sort_index()
        st.bar_chart(quarter_counts)

    # --- Tab 6: Durations ---
    with tab6:
        movies_df = df[df['type'] == 'Movie'].copy()
        tv_df = df[df['type'] == 'TV Show'].copy()

        # Movies: extract minutes
        movies_df['minutes'] = movies_df['duration'].str.extract('(\d+)').astype(float)

        # TV Shows: extract seasons
        tv_df['seasons'] = tv_df['duration'].str.extract('(\d+)').astype(float)

        st.subheader("Movie Duration Distribution")
        fig4, ax4 = plt.subplots()
        sns.histplot(movies_df['minutes'].dropna(), bins=30, kde=True, ax=ax4, color='crimson')
        st.pyplot(fig4)

        st.subheader("TV Shows by Season Count")
        fig5, ax5 = plt.subplots()
        sns.countplot(x=tv_df['seasons'].dropna(), ax=ax5)
        st.pyplot(fig5)

        st.info(f"🎞 Average Movie Duration: {movies_df['minutes'].mean():.2f} minutes")
        st.info(f"📺 Average Number of TV Seasons: {tv_df['seasons'].mean():.2f}")

except FileNotFoundError:
    st.error("❌ File 'netflix_titles.csv' not found in the current folder.")
