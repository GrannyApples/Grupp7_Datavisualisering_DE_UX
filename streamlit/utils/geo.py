import pycountry
import pandas as pd
import streamlit as st


def to_iso3(code: str) -> str | None:
    """Konverterar landskod alpha-2 (t.ex. 'SE') till alpha-3 (t.ex. 'SWE').
    Behövs för Plotly choropleth som kräver ISO-3 format."""
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except Exception:
        return None


def to_name(code: str) -> str:
    """Konverterar landskod alpha-2 till läsbart landsnamn (t.ex. 'SE' → 'Sweden')."""
    try:
        return pycountry.countries.get(alpha_2=code).name
    except Exception:
        return code


@st.cache_data
def build_country_count(countries_df: pd.DataFrame) -> pd.DataFrame:
    """Räknar antal filmer per land och lägger till ISO-3 och landsnamn.
    Cachas så det inte räknas om varje gång."""
    cc = (
        countries_df.groupby("country_code")
        .size()
        .reset_index(name="antal_filmer")
        .sort_values("antal_filmer", ascending=False)
    )
    cc["iso3"]         = cc["country_code"].apply(to_iso3)
    cc["country_name"] = cc["country_code"].apply(to_name)
    cc = cc.dropna(subset=["iso3"])
    return cc