import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.region_selector import render_region_selector
from src.api.open_meteo_api import fetch_historical_weather
from src.api.usgs_earthquake_api import fetch_earthquake_data
from src.visualizations.map import display_map
from src.visualizations.time_series import display_timeseries
from src.visualizations.correlations import display_correlations
from src.visualizations.quake_3d import display_3d_quakes

# Page setup
st.set_page_config(
    page_title="🌍 Weather & Earthquake Insight Dashboard",
    page_icon="🌋",
    layout="wide"
)

# Header
st.title("🌍 Weather & Earthquake Insight Dashboard")
st.markdown("""
This dashboard integrates **Open-Meteo** and **USGS Earthquake** data to help analyze and visualize:
- Historical weather trends
- Seismic activity and clustering
- Potential correlations
- 3D depth-based earthquake views
""")

# Region & Inputs
render_region_selector()
fetch_params = render_sidebar()

if fetch_params:
    with st.spinner("📡 Fetching Data..."):
        weather_df = fetch_historical_weather(
            fetch_params['latitude'], fetch_params['longitude'],
            str(fetch_params['start_date']), str(fetch_params['end_date'])
        )
        quake_df = fetch_earthquake_data(
            str(fetch_params['start_date']), str(fetch_params['end_date']),
            fetch_params['min_magnitude'], fetch_params['latitude'],
            fetch_params['longitude'], fetch_params['max_distance_km']
        )

    # Visualization Tabs
    tabs = st.tabs(["🗺️ Map View", "📊 Time Series", "🔗 Correlations", "🌐 3D Quakes"])

    with tabs[0]:
        display_map(weather_df, quake_df, fetch_params['latitude'], fetch_params['longitude'])

    with tabs[1]:
        display_timeseries(weather_df, quake_df)

    with tabs[2]:
        display_correlations(weather_df, quake_df)

    with tabs[3]:
        display_3d_quakes(quake_df)

else:
    st.info("👈 Select a region and filters from the sidebar to begin analysis.")
