import streamlit as st
import pandas as pd
from components.charts import bar_chart, scatter_chart


def render(df: pd.DataFrame) -> None:
    """Budget & Revenue – ekonomisk analys av fantasyfilmer.
    Visar scatter, ROI-tabell och snitt budget/revenue per kategori."""
    st.title("Budget & Revenue")
    st.caption("Ekonomisk analys av fantasyfilmer")
    st.markdown("---")

    bdf = df[(df["budget"] > 0) & (df["revenue"] > 0)].copy()
    bdf["roi"] = ((bdf["revenue"] - bdf["budget"]) / bdf["budget"] * 100).round(1)

    #  KPI-kort 
    col1, col2, col3 = st.columns(3)
    col1.metric("Filmer med budgetdata", len(bdf))
    col2.metric("Total revenue",         f"${bdf['revenue'].sum() / 1e9:.1f}B")
    col3.metric("Snitt ROI",             f"{bdf['roi'].mean():.0f}%")

    st.markdown("---")

    #  Rad 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Budget vs Revenue")
        fig = scatter_chart(bdf, x="budget", y="revenue",
                            color="category", hover_name="title", size="popularity")
        fig.update_layout(xaxis_title="Budget ($)", yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 högst ROI")
        top_roi = bdf.nlargest(10, "roi")[["title", "budget", "revenue", "roi", "category"]].copy()
        top_roi["budget"]  = top_roi["budget"].apply(lambda x: f"${x / 1e6:.1f}M")
        top_roi["revenue"] = top_roi["revenue"].apply(lambda x: f"${x / 1e6:.1f}M")
        top_roi["roi"]     = top_roi["roi"].apply(lambda x: f"{x:.0f}%")
        top_roi = top_roi.reset_index(drop=True)
        top_roi.index += 1
        st.dataframe(top_roi, use_container_width=True)

    # Rad 2 
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Snitt budget per kategori")
        avg_budget = bdf.groupby("category")["budget"].mean().reset_index()
        avg_budget["budget_M"] = (avg_budget["budget"] / 1e6).round(1)
        fig = bar_chart(avg_budget, x="budget_M", y="category", text="budget_M")
        fig.update_traces(texttemplate="%{text}M")
        fig.update_layout(xaxis_title="Budget (miljoner $)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Snitt revenue per kategori")
        avg_rev = bdf.groupby("category")["revenue"].mean().reset_index()
        avg_rev["revenue_M"] = (avg_rev["revenue"] / 1e6).round(1)
        fig = bar_chart(avg_rev, x="revenue_M", y="category", text="revenue_M")
        fig.update_traces(texttemplate="%{text}M")
        fig.update_layout(xaxis_title="Revenue (miljoner $)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)