import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry


st.set_page_config(
    page_title="Fantasy Movies Dashboard",
    page_icon="",
    layout="wide"
)


@st.cache_data
def load_data():
    movies    = pd.read_csv("data/powerbi/movies.csv")
    details   = pd.read_csv("data/powerbi/movie_details.csv")
    cast      = pd.read_csv("data/powerbi/movie_cast.csv")
    countries = pd.read_csv("data/powerbi/movie_origin_countries.csv")

    df = movies.merge(
        details[["movie_id","budget","revenue","runtime","director","overview"]],
        on="movie_id", how="left"
    )
    df["budget"]       = pd.to_numeric(df["budget"],       errors="coerce").fillna(0)
    df["revenue"]      = pd.to_numeric(df["revenue"],      errors="coerce").fillna(0)
    df["runtime"]      = pd.to_numeric(df["runtime"],      errors="coerce").fillna(0)
    df["rating"]       = pd.to_numeric(df["rating"],       errors="coerce")
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    return movies, details, cast, countries, df

movies, details, cast, countries, df = load_data()


def to_iso3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except Exception:
        return None

def to_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except Exception:
        return code


@st.cache_data
def build_country_count(countries_df):
    cc = (countries_df.groupby("country_code")
                      .size()
                      .reset_index(name="antal_filmer")
                      .sort_values("antal_filmer", ascending=False))
    cc["iso3"]         = cc["country_code"].apply(to_iso3)
    cc["country_name"] = cc["country_code"].apply(to_name)
    cc = cc.dropna(subset=["iso3"])
    return cc

country_count = build_country_count(countries)


st.sidebar.image(
    "https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_2-d537fb228cf3ded904ef09b136fe3fec72548ebc1fea3fbbd1ad9e36364db38b.svg",
    width=150
)
st.sidebar.title("Fantasy Movies")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigera", [
    "Översikt",
    "Kategorier",
    "Budget & Revenue",
    "Skådespelare",
    "Världskarta"
])

st.sidebar.markdown("---")
st.sidebar.caption(f"{len(df)} filmer | {df['category'].nunique()} kategorier")


if page == "Översikt":
    st.title("Fantasy Movies Dashboard")
    st.caption("Utforska fantasyfilmer från TMDB – betyg, popularitet och trender")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totalt filmer", f"{len(df):,}")
    col2.metric("Snittbetyg",    f"{df['rating'].mean():.2f} / 10")
    col3.metric("Kategorier",    df['category'].nunique())
    col4.metric("År spann",      f"{int(df['release_year'].min())}–{int(df['release_year'].max())}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Snittbetyg per kategori")
        avg = (df.groupby("category")["rating"]
                 .mean().reset_index()
                 .sort_values("rating", ascending=True))
        avg["rating"] = avg["rating"].round(2)
        fig = px.bar(avg, x="rating", y="category", orientation="h",
                     color="category", range_x=[0, 10], text="rating",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title="Snittbetyg", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Antal filmer per år")
        year = df.groupby("release_year").size().reset_index(name="antal")
        fig = px.line(year, x="release_year", y="antal", markers=True,
                      color_discrete_sequence=["#636EFA"])
        fig.update_layout(xaxis_title="År", yaxis_title="Antal filmer")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Fördelning per kategori")
        cat_count = df["category"].value_counts().reset_index()
        cat_count.columns = ["category", "antal"]
        fig = px.pie(cat_count, names="category", values="antal",
                     color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 mest populära")
        top10 = df.nlargest(10, "popularity")[["title","popularity","rating","category"]].copy()
        top10["popularity"] = top10["popularity"].round(2)
        fig = px.bar(top10, x="popularity", y="title", orientation="h",
                     color="category",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(showlegend=True, xaxis_title="Popularity", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)


elif page == "Kategorier":
    st.title("Kategorier")
    st.caption("Utforska filmer per fantasi-kategori")
    st.markdown("---")

    kategori = st.selectbox("Välj kategori", sorted(df["category"].unique()))
    filtered = df[df["category"] == kategori].sort_values("rating", ascending=False)

    col1, col2, col3 = st.columns(3)
    col1.metric("Antal filmer", len(filtered))
    col2.metric("Snittbetyg",   f"{filtered['rating'].mean():.2f}")
    col3.metric("Högsta betyg", f"{filtered['rating'].max():.1f}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Top 20 – {kategori}")
        show = filtered[["title","rating","popularity","release_year"]].head(20).copy()
        show["rating"]     = show["rating"].round(2)
        show["popularity"] = show["popularity"].round(2)
        show = show.reset_index(drop=True)
        show.index += 1
        st.dataframe(show, use_container_width=True)

    with col2:
        st.subheader("Betygsfördelning")
        fig = px.histogram(filtered, x="rating", nbins=20,
                           color_discrete_sequence=["#636EFA"])
        fig.update_layout(xaxis_title="Betyg", yaxis_title="Antal filmer")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Filmer per år i denna kategori")
    year_cat = filtered.groupby("release_year").size().reset_index(name="antal")
    fig = px.bar(year_cat, x="release_year", y="antal",
                 color_discrete_sequence=["#636EFA"])
    fig.update_layout(xaxis_title="År", yaxis_title="Antal filmer")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Budget & Revenue":
    st.title("Budget & Revenue")
    st.caption("Ekonomisk analys av fantasyfilmer")
    st.markdown("---")

    bdf = df[(df["budget"] > 0) & (df["revenue"] > 0)].copy()
    bdf["roi"] = ((bdf["revenue"] - bdf["budget"]) / bdf["budget"] * 100).round(1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Filmer med budgetdata", len(bdf))
    col2.metric("Total revenue",         f"${bdf['revenue'].sum()/1e9:.1f}B")
    col3.metric("Snitt ROI",             f"{bdf['roi'].mean():.0f}%")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Budget vs Revenue")
        fig = px.scatter(bdf, x="budget", y="revenue", color="category",
                         hover_name="title", size="popularity", size_max=30,
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(xaxis_title="Budget ($)", yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 högst ROI")
        top_roi = bdf.nlargest(10, "roi")[["title","budget","revenue","roi","category"]].copy()
        top_roi["budget"]  = top_roi["budget"].apply(lambda x: f"${x/1e6:.1f}M")
        top_roi["revenue"] = top_roi["revenue"].apply(lambda x: f"${x/1e6:.1f}M")
        top_roi["roi"]     = top_roi["roi"].apply(lambda x: f"{x:.0f}%")
        top_roi = top_roi.reset_index(drop=True)
        top_roi.index += 1
        st.dataframe(top_roi, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Snitt budget per kategori")
        avg_budget = bdf.groupby("category")["budget"].mean().reset_index()
        avg_budget["budget_M"] = (avg_budget["budget"] / 1e6).round(1)
        fig = px.bar(avg_budget, x="budget_M", y="category", orientation="h",
                     color="category", text="budget_M",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(texttemplate="%{text}M", textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title="Budget (miljoner $)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Snitt revenue per kategori")
        avg_rev = bdf.groupby("category")["revenue"].mean().reset_index()
        avg_rev["revenue_M"] = (avg_rev["revenue"] / 1e6).round(1)
        fig = px.bar(avg_rev, x="revenue_M", y="category", orientation="h",
                     color="category", text="revenue_M",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(texttemplate="%{text}M", textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title="Revenue (miljoner $)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)


elif page == "Skådespelare":
    st.title("Skådespelare")
    st.caption("Mest förekommande skådespelare i fantasyfilmer")
    st.markdown("---")

    top_actors = (cast.groupby("actor_name")
                      .size()
                      .reset_index(name="antal_filmer")
                      .nlargest(20, "antal_filmer"))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 20 mest förekommande")
        fig = px.bar(top_actors, x="antal_filmer", y="actor_name",
                     orientation="h", color="antal_filmer",
                     color_continuous_scale="Blues")
        fig.update_layout(yaxis_title="", xaxis_title="Antal filmer", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Sök skådespelare")
        search = st.text_input("Skriv skådespelarens namn")
        if search:
            result = cast[cast["actor_name"].str.contains(search, case=False, na=False)]
            if len(result) > 0:
                merged = result.merge(
                    df[["movie_id","title","rating","category"]],
                    on="movie_id", how="left"
                )
                st.dataframe(
                    merged[["actor_name","character","title","rating","category"]].head(20),
                    use_container_width=True
                )
            else:
                st.warning("Inga resultat hittades.")

elif page == "Världskarta":
    st.title("Filmproduktion per land")
    st.caption("Var produceras fantasyfilmer i världen?")
    st.markdown("---")

    
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        selected = st.multiselect(
            "Filtrera länder (lämna tomt = visa alla)",
            options=sorted(country_count["country_name"].tolist()),
            default=[]
        )
    with col_f2:
        show_top = st.slider("Visa top N länder", min_value=5, max_value=38, value=38)

    
    if selected:
        filtered_map = country_count[country_count["country_name"].isin(selected)]
    else:
        filtered_map = country_count.head(show_top)

    st.markdown("---")

    
    col1, col2, col3 = st.columns(3)
    col1.metric("Länder visas",  len(filtered_map))
    col2.metric("Top land",      filtered_map.iloc[0]["country_name"])
    col3.metric("Max filmer",    int(filtered_map.iloc[0]["antal_filmer"]))

    st.markdown("---")

    
    fig = px.choropleth(
        filtered_map,
        locations="iso3",
        locationmode="ISO-3",
        color="antal_filmer",
        hover_name="country_name",
        hover_data={"antal_filmer": True, "iso3": False, "country_code": False},
        color_continuous_scale="Viridis",
        title="Antal fantasyfilmer per land",
        labels={"antal_filmer": "Antal filmer"}
    )
    fig.update_geos(
        showcoastlines=True, coastlinecolor="gray",
        showland=True,       landcolor="lightgray",
        showocean=True,      oceancolor="#0d1b2a",
        showframe=False
    )
    fig.update_layout(height=520)
    st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("Länder")
    top_countries = (filtered_map[["country_name","antal_filmer"]]
                     .reset_index(drop=True))
    top_countries.index += 1

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top_countries, use_container_width=True)
    with col2:
        fig = px.bar(
            filtered_map.head(10),
            x="antal_filmer", y="country_name", orientation="h",
            color="antal_filmer", color_continuous_scale="Viridis",
            labels={"country_name": "Land", "antal_filmer": "Antal filmer"}
        )
        fig.update_layout(yaxis_title="", xaxis_title="Antal filmer", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    
    if selected and len(selected) == 1:
        st.markdown("---")
        st.subheader(f"Filmer från {selected[0]}")
        code = country_count[country_count["country_name"] == selected[0]]["country_code"].values[0]
        movie_ids = countries[countries["country_code"] == code]["movie_id"].tolist()
        land_filmer = df[df["movie_id"].isin(movie_ids)].sort_values("rating", ascending=False)
        land_filmer = land_filmer[["title","rating","popularity","release_year","category"]].copy()
        land_filmer["rating"]     = land_filmer["rating"].round(2)
        land_filmer["popularity"] = land_filmer["popularity"].round(2)
        land_filmer = land_filmer.reset_index(drop=True)
        land_filmer.index += 1
        st.dataframe(land_filmer, use_container_width=True)