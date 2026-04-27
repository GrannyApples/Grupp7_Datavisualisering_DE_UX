import pandas as pd
import streamlit as st
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "powerbi"


@st.cache_data
def load_data() -> tuple:
    movies    = pd.read_csv(DATA_DIR / "movies.csv")
    details   = pd.read_csv(DATA_DIR / "movie_details.csv")
    cast      = pd.read_csv(DATA_DIR / "movie_cast.csv")
    countries = pd.read_csv(DATA_DIR / "movie_origin_countries.csv")

    df = movies.merge(
        details[["movie_id", "budget", "revenue", "runtime", "director", "overview"]],
        on="movie_id",
        how="left",
    )

    for col in ["budget", "revenue", "runtime"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["rating"]       = pd.to_numeric(df["rating"],       errors="coerce")
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

    return movies, details, cast, countries, df