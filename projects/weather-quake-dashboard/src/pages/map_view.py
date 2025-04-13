import streamlit as st
from src.components.map_display import display_interactive_map

def display_map(data_bundle):
    st.subheader("🗺️ Earthquakes & Weather Map")

    hourly_df = data_bundle["weather"]
    quake_df = data_bundle["earthquakes"]
    inputs = data_bundle["inputs"]

    if hourly_df.empty:
        st.warning("No weather data available for the selected location and time range.")

    if quake_df.empty:
        st.warning("No earthquake data found for the selected location and time range.")

    if not quake_df.empty:
        display_interactive_map(quake_df, hourly_df, inputs['latitude'], inputs['longitude'])
