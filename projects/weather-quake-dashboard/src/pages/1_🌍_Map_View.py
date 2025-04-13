import streamlit as st
from src.api.open_meteo_api import fetch_historical_weather
from src.api.usgs_earthquake_api import fetch_earthquake_data
from src.components.map_display import display_interactive_map


def display_map(user_inputs):
    st.subheader("🗺️ Earthquakes & Weather Map")

    with st.spinner("Fetching weather & earthquake data..."):
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

    if quake_df.empty:
        st.warning("No earthquake data found for the selected location and time range.")
    else:
        display_interactive_map(quake_df, hourly_df, user_inputs['latitude'], user_inputs['longitude'])
