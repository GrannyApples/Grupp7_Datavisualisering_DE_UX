import streamlit as st
import pandas as pd
from components.charts import bar_chart, line_chart, pie_chart


def render(df: pd.DataFrame) -> None:
    """Översiktssidan – visar nyckeltal, snittbetyg per kategori,
    filmer per år, fördelning och top 10 populäraste."""
    st.title("Fantasy Movies Dashboard")
    st.caption("Utforska fantasyfilmer från TMDB – betyg, popularitet och trender")
    st.markdown("---")

    #  KPI-kort
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totalt filmer", f"{len(df):,}")
    col2.metric("Snittbetyg",    f"{df['rating'].mean():.2f} / 10")
    col3.metric("Kategorier",    df["category"].nunique())
    col4.metric("År spann",      f"{int(df['release_year'].min())}–{int(df['release_year'].max())}")

    st.markdown("---")

    # Rad 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Snittbetyg per kategori")
        avg = (
            df.groupby("category")["rating"]
            .mean().reset_index()
            .sort_values("rating", ascending=True)
        )
        avg["rating"] = avg["rating"].round(2)
        fig = bar_chart(avg, x="rating", y="category", text="rating")
        fig.update_layout(xaxis_title="Snittbetyg", yaxis_title="", xaxis_range=[0, 10])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Antal filmer per år")
        year = df.groupby("release_year").size().reset_index(name="antal")
        fig = line_chart(year, x="release_year", y="antal")
        fig.update_layout(xaxis_title="År", yaxis_title="Antal filmer")
        st.plotly_chart(fig, use_container_width=True)

    # Rad 2 
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Fördelning per kategori")
        cat_count = df["category"].value_counts().reset_index()
        cat_count.columns = ["category", "antal"]
        fig = pie_chart(cat_count, names="category", values="antal")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 mest populära")
        top10 = df.nlargest(10, "popularity")[["title", "popularity", "rating", "category"]].copy()
        top10["popularity"] = top10["popularity"].round(2)
        fig = bar_chart(top10, x="popularity", y="title", color="category")
        fig.update_layout(showlegend=True, xaxis_title="Popularity", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)