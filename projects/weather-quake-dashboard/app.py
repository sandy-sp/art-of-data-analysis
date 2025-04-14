import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.region_selector import render_region_selector
from src.api.open_meteo_api import fetch_historical_weather
from src.api.usgs_earthquake_api import fetch_earthquake_data
from src.utils.tectonic_loader import load_tectonic_boundaries
from src.utils.data_processing import filter_quakes_near_boundaries
from src.pages import map_view, time_series, correlations, quake_3d

st.set_page_config(
    page_title="🌍 Weather & Earthquake Insight Dashboard",
    layout="wide",
    page_icon="🌋"
)

@st.cache_data(show_spinner=False)
def cached_fetch_weather(lat, lon, start, end):
    return fetch_historical_weather(lat, lon, start, end)

@st.cache_data(show_spinner=False)
def cached_fetch_quakes(start, end, min_mag, lat, lon, limit):
    return fetch_earthquake_data(start, end, min_mag, lat, lon, limit)

# Display region picker before sidebar input
render_region_selector()

# Sidebar controls
user_inputs = render_sidebar()
refresh = st.sidebar.checkbox("🔄 Force Refresh", value=False)
filter_near_boundaries = st.sidebar.checkbox("📍 Filter quakes near tectonic boundaries", value=True)
max_distance_km = st.sidebar.slider("Max Distance to Boundary (km)", 10, 100, 50, step=5) if filter_near_boundaries else 0

# Main header
st.title("🌍 Weather & Earthquake Insight Dashboard")
st.markdown("""
This app combines **historical weather** (Open-Meteo) and **earthquake data** (USGS) to provide interactive
maps, time-series plots, and correlation analysis for better understanding of geophysical dynamics.
""")

if st.session_state.get("data_ready"):
    with st.spinner("Fetching weather and earthquake data..."):
        if refresh:
            hourly_df, _ = fetch_historical_weather(
                user_inputs['latitude'],
                user_inputs['longitude'],
                str(user_inputs['start_date']),
                str(user_inputs['end_date'])
            )
            quake_df = fetch_earthquake_data(
                str(user_inputs['start_date']),
                str(user_inputs['end_date']),
                user_inputs['min_magnitude'],
                user_inputs['latitude'],
                user_inputs['longitude'],
                user_inputs['limit']
            )
        else:
            hourly_df, _ = cached_fetch_weather(
                user_inputs['latitude'],
                user_inputs['longitude'],
                str(user_inputs['start_date']),
                str(user_inputs['end_date'])
            )
            quake_df = cached_fetch_quakes(
                str(user_inputs['start_date']),
                str(user_inputs['end_date']),
                user_inputs['min_magnitude'],
                user_inputs['latitude'],
                user_inputs['longitude'],
                user_inputs['limit']
            )

        if filter_near_boundaries:
            tectonics = load_tectonic_boundaries()
            if tectonics is not None and not tectonics.empty:
                quake_df = filter_quakes_near_boundaries(quake_df, tectonics, max_distance_km=max_distance_km)
                st.info("Filtered earthquakes to those within 50 km of tectonic boundaries.")

        st.session_state['weather_data'] = hourly_df
        st.session_state['quake_data'] = quake_df
        st.success("Data fetched successfully. You can now explore visualizations below.")
        st.session_state["data_ready"] = False

if 'weather_data' in st.session_state and 'quake_data' in st.session_state:
    data_bundle = {
        "weather": st.session_state['weather_data'],
        "earthquakes": st.session_state['quake_data'],
        "inputs": user_inputs
    }

    tabs = st.tabs(["🌍 Map View", "📈 Time Series", "🔍 Correlations", "🌐 3D Quake View"])

    with tabs[0]:
        map_view.display_map(data_bundle)

    with tabs[1]:
        time_series.display_timeseries(data_bundle)

    with tabs[2]:
        correlations.display_correlation_analysis(data_bundle)

    with tabs[3]:
        quake_3d.display_3d_quake_map(data_bundle)
else:
    st.info("👈 Use the sidebar to select a region and click 'Fetch & Analyze' to begin.")
