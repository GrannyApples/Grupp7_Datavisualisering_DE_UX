import streamlit as st
import pandas as pd
import plotly.express as px


def render(df: pd.DataFrame, cast: pd.DataFrame) -> None:
    """Skådespelarsidan – visar top 20 mest förekommande
    och sökfunktion för enskild skådespelare."""
    st.title("Skådespelare")
    st.caption("Mest förekommande skådespelare i fantasyfilmer")
    st.markdown("---")

    top_actors = (
        cast.groupby("actor_name")
        .size()
        .reset_index(name="antal_filmer")
        .nlargest(20, "antal_filmer")
    )

    #  Rad 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 20 mest förekommande")
        fig = px.bar(
            top_actors, x="antal_filmer", y="actor_name",
            orientation="h", color="antal_filmer",
            color_continuous_scale="Blues",
        )
        fig.update_layout(yaxis_title="", xaxis_title="Antal filmer", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Sök skådespelare")
        search = st.text_input("Skriv skådespelarens namn")
        if search:
            result = cast[cast["actor_name"].str.contains(search, case=False, na=False)]
            if len(result) > 0:
                merged = result.merge(
                    df[["movie_id", "title", "rating", "category"]],
                    on="movie_id",
                    how="left",
                )
                st.dataframe(
                    merged[["actor_name", "character", "title", "rating", "category"]].head(20),
                    use_container_width=True,
                )
            else:
                st.warning("Inga resultat hittades.")