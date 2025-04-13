import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.region_selector import render_region_selector
from src.api.open_meteo_api import fetch_historical_weather
from src.api.usgs_earthquake_api import fetch_earthquake_data
from src.pages import map_view, time_series, correlations

st.set_page_config(
    page_title="🌍 Weather & Earthquake Insight Dashboard",
    layout="wide",
    page_icon="🌋"
)

# Display region picker before sidebar input
render_region_selector()

# Sidebar controls
user_inputs = render_sidebar()

# Main header
st.title("🌍 Weather & Earthquake Insight Dashboard")
st.markdown("""
This app combines **historical weather** (Open-Meteo) and **earthquake data** (USGS) to provide interactive
maps, time-series plots, and correlation analysis for better understanding of geophysical dynamics.
""")

# Only fetch data once Fetch button is pressed
if st.session_state.get("data_ready"):
    with st.spinner("Fetching weather and earthquake data..."):
        hourly_df, _ = fetch_historical_weather(
            user_inputs['latitude'],
            user_inputs['longitude'],
            str(user_inputs['start_date']),
            str(user_inputs['end_date'])
        )

        quake_df = fetch_earthquake_data(
            starttime=str(user_inputs['start_date']),
            endtime=str(user_inputs['end_date']),
            min_magnitude=user_inputs['min_magnitude'],
            latitude=user_inputs['latitude'],
            longitude=user_inputs['longitude'],
            limit=user_inputs['limit']
        )

        st.session_state['weather_data'] = hourly_df
        st.session_state['quake_data'] = quake_df
        st.success("Data fetched successfully. You can now explore visualizations below.")
        st.session_state["data_ready"] = False  # Reset trigger

# Tabs for views
if 'weather_data' in st.session_state and 'quake_data' in st.session_state:
    data_bundle = {
        "weather": st.session_state['weather_data'],
        "earthquakes": st.session_state['quake_data'],
        "inputs": user_inputs
    }

    tabs = st.tabs(["🌍 Map View", "📈 Time Series", "🔍 Correlations"])

    with tabs[0]:
        map_view.display_map(data_bundle)

    with tabs[1]:
        time_series.display_timeseries(data_bundle)

    with tabs[2]:
        correlations.display_correlation_analysis(data_bundle)
else:
    st.info("👈 Use the sidebar to select a region and click 'Fetch & Analyze' to begin.")
