import streamlit as st
from src.components.sidebar import render_sidebar
from src.pages import map_view, time_series, correlations

st.set_page_config(
    page_title="🌍 Weather & Earthquake Insight Dashboard",
    layout="wide",
    page_icon="🌋"
)

# Sidebar controls
user_inputs = render_sidebar()

# Main header
st.title("🌍 Weather & Earthquake Insight Dashboard")
st.markdown("""
This app combines **historical weather** (Open-Meteo) and **earthquake data** (USGS) to provide interactive
maps, time-series plots, and correlation analysis for better understanding of geophysical dynamics.
""")

# Tabs for views
tabs = st.tabs(["🌍 Map View", "📈 Time Series", "🔍 Correlations"])

with tabs[0]:
    map_view.display_map(user_inputs)

with tabs[1]:
    time_series.display_timeseries(user_inputs)

with tabs[2]:
    correlations.display_correlation_analysis(user_inputs)
