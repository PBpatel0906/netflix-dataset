
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview", 
        "📈 Year Trends", 
        "🌍 Country & Type", 
        "🎭 Genres & Actors", 
        "🕒 Time Trends", 
        "🎥 Durations",
        "🌏 Country Content View"
    ])

    # --- Tab 1: Overview ---
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10))

        st.subheader("Top 10 Countries")
        top_countries = df['country'].value_counts().head(10)
        st.bar_chart(top_countries)
        st.write("These are the top 10 countries by number of Netflix titles.")

        st.subheader("Content Type Distribution")
        type_counts = df['type'].value_counts()

        col1, col2 = st.columns([1, 2])
        with col1:
            fig, ax = plt.subplots(figsize=(4, 4))
            type_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'], ax=ax)
            ax.set_ylabel("")
            st.pyplot(fig)
        with col2:
            st.markdown("""
            This pie chart shows the **proportion of Movies vs TV Shows** on Netflix.
            - 📽️ Movies: single entries (e.g. films)
            - 📺 TV Shows: series content
            """)

    # --- Tab 2: Year Trends ---
    with tab2:
        st.subheader("Content Added Per Year")
        content_per_year = df['year_added'].value_counts().sort_index()

        fig, ax = plt.subplots()
        sns.lineplot(x=content_per_year.index, y=content_per_year.values, marker='o', ax=ax, color='blue')
        ax.set_title("Netflix Titles Added Each Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Titles")
        ax.grid(True)
        st.pyplot(fig)

        st.write("This line chart shows how many titles were **added to Netflix** each year.")

        st.subheader("Content Released Per Year")
        release_trend = df['release_year'].value_counts().sort_index()
        st.area_chart(release_trend)
        st.write("This chart shows the release years of content, regardless of when it was added to Netflix.")

    # --- Tab 3: Country and Type ---
    with tab3:
        st.subheader("Top Countries by Content Type")
        grouped = df.groupby(['type', 'country']).size().reset_index(name='count')
        top_grouped = grouped.sort_values(by='count', ascending=False).head(20)

        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(data=top_grouped, x='country', y='count', hue='type', ax=ax)
        ax.set_title("Top Countries by Movies & TV Shows")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)

        st.write("This bar chart shows the top countries producing Movies or TV Shows on Netflix.")

    # --- Tab 4: Genres and Actors ---
    with tab4:
        st.subheader("Top 10 Global Genres")
        genres = df['listed_in'].str.split(', ').explode()
        top_genres = genres.value_counts().head(10)
        st.bar_chart(top_genres)
        st.write("This chart shows the most common genres across all Netflix titles.")

        st.subheader("Top 10 Global Actors")
        actors = df['cast'].str.split(', ').explode()
        top_actors = actors.value_counts().head(10)
        fig, ax = plt.subplots()
        top_actors.plot(kind='barh', ax=ax, color='skyblue')
        ax.invert_yaxis()
        st.pyplot(fig)
        st.write("This chart shows the most frequently appearing actors in the dataset.")

    # --- Tab 5: Month and Quarter Trends ---
    with tab5:
        st.subheader("Content Added by Month")
        month_counts = df['month_added'].value_counts().reindex([
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])
        st.bar_chart(month_counts)
        st.write("This chart shows how many titles were added in each month across all years.")

        st.subheader("Content Added by Quarter")
        quarter_counts = df['quarter_added'].value_counts().sort_index()
        st.bar_chart(quarter_counts)
        st.write("This shows quarterly trends of content additions.")

    # --- Tab 6: Durations ---
    with tab6:
        movies_df = df[df['type'] == 'Movie'].copy()
        tv_df = df[df['type'] == 'TV Show'].copy()

        movies_df['minutes'] = movies_df['duration'].str.extract('(\d+)').astype(float)
        tv_df['seasons'] = tv_df['duration'].str.extract('(\d+)').astype(float)

        st.subheader("Movie Duration Distribution")
        fig, ax = plt.subplots()
        sns.histplot(movies_df['minutes'].dropna(), bins=30, kde=True, ax=ax, color='crimson')
        st.pyplot(fig)
        st.write("This histogram shows how long Netflix movies typically are.")

        st.subheader("TV Shows by Season Count")
        fig, ax = plt.subplots()
        sns.countplot(x=tv_df['seasons'].dropna(), ax=ax)
        st.pyplot(fig)
        st.write("This chart shows how many TV Shows have 1, 2, 3... seasons.")

        st.info(f"🎞️ Average Movie Duration: {movies_df['minutes'].mean():.2f} minutes")
        st.info(f"📺 Average TV Show Seasons: {tv_df['seasons'].mean():.2f}")

    # --- Tab 7: Country Content View ---
    with tab7:
        st.subheader("Select Country/Countries")
        countries = df['country'].dropna().unique().tolist()
        countries.sort()

        selected_countries = st.multiselect("Choose one or more countries", countries, default=["India"])

        if selected_countries:
            filtered = df[df['country'].isin(selected_countries)]

            st.markdown("### 🧮 Content Type Distribution")
            type_counts = filtered['type'].value_counts(normalize=True) * 100

            fig, ax = plt.subplots(figsize=(4, 4))
            type_counts.plot.pie(autopct='%1.1f%%', ax=ax, colors=['#ff9999','#66b3ff'])
            ax.set_ylabel("")
            st.pyplot(fig)

            st.markdown("### 🎞️ Titles and Descriptions")
            display_cols = ['title', 'type', 'description', 'country', 'release_year']
            st.dataframe(filtered[display_cols].sort_values(by='release_year', ascending=False), use_container_width=True)
        else:
            st.info("Please select at least one country to view the data.")

except FileNotFoundError:
    st.error("❌ File 'netflix_titles.csv' not found in the current folder.")
