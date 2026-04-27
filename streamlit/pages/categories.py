import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import bar_chart


def render(df: pd.DataFrame) -> None:
    """Kategorisidan – filtrera filmer per fantasy-kategori,
    visa top 20, betygsfördelning och filmer per år."""
    st.title("Kategorier")
    st.caption("Utforska filmer per fantasi-kategori")
    st.markdown("---")

    kategori = st.selectbox("Välj kategori", sorted(df["category"].unique()))
    filtered = df[df["category"] == kategori].sort_values("rating", ascending=False)

    # KPI-kort 
    col1, col2, col3 = st.columns(3)
    col1.metric("Antal filmer", len(filtered))
    col2.metric("Snittbetyg",   f"{filtered['rating'].mean():.2f}")
    col3.metric("Högsta betyg", f"{filtered['rating'].max():.1f}")

    st.markdown("---")

    #  Rad 1 
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Top 20 – {kategori}")
        show = filtered[["title", "rating", "popularity", "release_year"]].head(20).copy()
        show["rating"]     = show["rating"].round(2)
        show["popularity"] = show["popularity"].round(2)
        show = show.reset_index(drop=True)
        show.index += 1
        st.dataframe(show, use_container_width=True)

    with col2:
        st.subheader("Betygsfördelning")
        fig = px.histogram(
            filtered, x="rating", nbins=20,
            color_discrete_sequence=["#636EFA"],
        )
        fig.update_layout(xaxis_title="Betyg", yaxis_title="Antal filmer")
        st.plotly_chart(fig, use_container_width=True)

    #  Rad 2 
    st.subheader("Filmer per år i denna kategori")
    year_cat = filtered.groupby("release_year").size().reset_index(name="antal")
    fig = bar_chart(year_cat, x="release_year", y="antal", orientation="v")
    fig.update_layout(xaxis_title="År", yaxis_title="Antal filmer")
    st.plotly_chart(fig, use_container_width=True)