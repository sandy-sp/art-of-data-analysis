import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.region_selector import render_region_selector
from src.api.open_meteo_api import fetch_historical_weather
from src.api.usgs_earthquake_api import fetch_earthquake_data
from src.visualizations.time_series import display_timeseries
from src.visualizations.correlations import display_correlations
from src.visualizations.quake_3d import display_3d_quakes

# Set Streamlit page configuration
st.set_page_config(
    page_title="🌍 Weather & Earthquake Insight Dashboard",
    page_icon="🌋",
    layout="wide"
)

# Header Content
st.title("🌍 Weather & Earthquake Insight Dashboard")
st.markdown("""
An interactive Streamlit dashboard for:
- Exploring weather and seismic trends
- Correlating earthquake and climate data
- Analyzing spatial and temporal risk factors
- Viewing 3D seismic depth visualizations
""")

# --- US Region Selector ---
render_region_selector()

# --- Sidebar Input ---
fetch_params = render_sidebar()

# --- Data Fetch & Visualization ---
if fetch_params:
    with st.spinner("📡 Fetching Data from APIs..."):
        weather_df = fetch_historical_weather(
            fetch_params['latitude'], fetch_params['longitude'],
            str(fetch_params['start_date']), str(fetch_params['end_date'])
        )
        quake_df = fetch_earthquake_data(
            str(fetch_params['start_date']), str(fetch_params['end_date']),
            fetch_params['min_magnitude'], fetch_params['latitude'],
            fetch_params['longitude'], fetch_params['max_distance_km']
        )

    st.markdown("---")
    tabs = st.tabs(["📈 Time Series", "🔗 Correlations", "🌐 3D Quakes"])

    with tabs[0]:
        display_timeseries(weather_df, quake_df)

    with tabs[1]:
        display_correlations(weather_df, quake_df)

    with tabs[2]:
        display_3d_quakes(quake_df)

else:
    st.info("👈 Use the sidebar and region selector to begin analysis.")
