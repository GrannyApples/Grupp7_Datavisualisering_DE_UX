import plotly.express as px
import pandas as pd

COLORS = px.colors.qualitative.Set2


def bar_chart(df: pd.DataFrame, x: str, y: str, color: str = None,
              orientation: str = "h", text: str = None) -> px.bar:
    """Återanvändbar horisontell/vertikal stapeldiagram.
    color, text är valfria parametrar."""
    fig = px.bar(
        df, x=x, y=y,
        orientation=orientation,
        color=color or y,
        text=text,
        color_discrete_sequence=COLORS,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)
    return fig


def line_chart(df: pd.DataFrame, x: str, y: str) -> px.line:
    """Linjediagram med punktmarkeringar – används för trender över tid."""
    fig = px.line(
        df, x=x, y=y,
        markers=True,
        color_discrete_sequence=["#636EFA"],
    )
    return fig


def pie_chart(df: pd.DataFrame, names: str, values: str) -> px.pie:
    """Donut-diagram för fördelning per kategori."""
    fig = px.pie(
        df, names=names, values=values,
        color_discrete_sequence=COLORS,
        hole=0.4,
    )
    return fig


def scatter_chart(df: pd.DataFrame, x: str, y: str, color: str,
                  hover_name: str, size: str) -> px.scatter:
    """Scatter-diagram – används för Budget vs Revenue.
    Storlek på punkter baseras på popularity."""
    fig = px.scatter(
        df, x=x, y=y,
        color=color,
        hover_name=hover_name,
        size=size, size_max=30,
        color_discrete_sequence=COLORS,
    )
    return fig


def choropleth(df: pd.DataFrame, locations: str, color: str,
               hover_name: str, title: str = "") -> px.choropleth:
    """Världskarta med färgskala – kräver ISO-3 landskoder.
    Används i Världskarta-sidan."""
    fig = px.choropleth(
        df,
        locations=locations,
        locationmode="ISO-3",
        color=color,
        hover_name=hover_name,
        hover_data={color: True, "iso3": False, "country_code": False},
        color_continuous_scale="Viridis",
        title=title,
        labels={color: "Antal filmer"},
    )
    fig.update_geos(
        showcoastlines=True, coastlinecolor="gray",
        showland=True,       landcolor="lightgray",
        showocean=True,      oceancolor="#0d1b2a",
        showframe=False,
    )
    fig.update_layout(height=520)
    return fig