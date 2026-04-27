import sys
from pathlib import Path

# Lägg till streamlit/-mappen i Python-sökvägen så imports fungerar
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from utils.data_loader import load_data
from utils.geo import build_country_count
from components.sidebar import render_sidebar
from pages import overview, categories, budget, actors, worldmap

st.set_page_config(
    page_title="Fantasy Movies Dashboard",
    page_icon="🎬",
    layout="wide",
)

# Ladda data 
movies, details, cast, countries, df = load_data()
country_count = build_country_count(countries)

#  Sidebar & routing 
page = render_sidebar(df)

if page == "Översikt":
    overview.render(df)
elif page == "Kategorier":
    categories.render(df)
elif page == "Budget & Revenue":
    budget.render(df)
elif page == "Skådespelare":
    actors.render(df, cast)
elif page == "Världskarta":
    worldmap.render(df, countries, country_count)