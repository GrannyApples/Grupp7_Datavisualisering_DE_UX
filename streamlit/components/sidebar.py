import streamlit as st

PAGES = [
    "Översikt",
    "Kategorier",
    "Budget & Revenue",
    "Skådespelare",
    "Världskarta",
]


def render_sidebar(df) -> str:
    """Renderar sidebaren med navigation och metadata.
    Returnerar namnet på den valda sidan."""
    st.sidebar.image(
        "https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_2-d537fb228cf3ded904ef09b136fe3fec72548ebc1fea3fbbd1ad9e36364db38b.svg",
        width=150,
    )
    st.sidebar.title("Fantasy Movies")
    st.sidebar.markdown("---")

    page = st.sidebar.radio("Navigera", PAGES)

    st.sidebar.markdown("---")
    st.sidebar.caption(
        f"{len(df):,} filmer | {df['category'].nunique()} kategorier"
    )

    return page