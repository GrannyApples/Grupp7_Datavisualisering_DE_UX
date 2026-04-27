import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import choropleth


def render(df: pd.DataFrame, countries: pd.DataFrame, country_count: pd.DataFrame) -> None:
    """Världskarta – visar filmproduktion per land.
    Filtrera på land eller visa top N länder."""
    st.title("Filmproduktion per land")
    st.caption("Var produceras fantasyfilmer i världen?")
    st.markdown("---")

    #  Filter 
    
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        selected = st.multiselect(
            "Filtrera länder (lämna tomt = visa alla)",
            options=sorted(country_count["country_name"].tolist()),
            default=[],
        )
    with col_f2:
        show_top = st.slider("Visa top N länder", min_value=5, max_value=38, value=38)

    filtered_map = (
        country_count[country_count["country_name"].isin(selected)]
        if selected
        else country_count.head(show_top)
    )

    st.markdown("---")

    #  KPI-kort 

    col1, col2, col3 = st.columns(3)
    col1.metric("Länder visas", len(filtered_map))
    col2.metric("Top land",     filtered_map.iloc[0]["country_name"])
    col3.metric("Max filmer",   int(filtered_map.iloc[0]["antal_filmer"]))

    st.markdown("---")

    #  Karta 

    fig = choropleth(
        filtered_map,
        locations="iso3",
        color="antal_filmer",
        hover_name="country_name",
        title="Antal fantasyfilmer per land",
    )
    st.plotly_chart(fig, use_container_width=True)

    #  Tabell + bar

    st.subheader("Länder")
    top_countries = filtered_map[["country_name", "antal_filmer"]].reset_index(drop=True)
    top_countries.index += 1

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top_countries, use_container_width=True)
    with col2:
        fig2 = px.bar(
            filtered_map.head(10),
            x="antal_filmer", y="country_name", orientation="h",
            color="antal_filmer", color_continuous_scale="Viridis",
        )
        fig2.update_layout(yaxis_title="", xaxis_title="Antal filmer", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Detaljer för enskilt land 

    if selected and len(selected) == 1:
        st.markdown("---")
        st.subheader(f"Filmer från {selected[0]}")
        code = country_count[country_count["country_name"] == selected[0]]["country_code"].values[0]
        movie_ids = countries[countries["country_code"] == code]["movie_id"].tolist()
        land_filmer = (
            df[df["movie_id"].isin(movie_ids)]
            .sort_values("rating", ascending=False)
            [["title", "rating", "popularity", "release_year", "category"]]
            .copy()
        )
        land_filmer["rating"]     = land_filmer["rating"].round(2)
        land_filmer["popularity"] = land_filmer["popularity"].round(2)
        land_filmer = land_filmer.reset_index(drop=True)
        land_filmer.index += 1
        st.dataframe(land_filmer, use_container_width=True)