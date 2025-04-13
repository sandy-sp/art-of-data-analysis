import streamlit as st
from src.api.open_meteo_api import fetch_historical_weather
from src.api.usgs_earthquake_api import fetch_earthquake_data
from src.utils.data_processing import align_weather_quake_data
from src.utils.visualization import plot_magnitude_vs_weather


def display_correlation_analysis(user_inputs):
    st.subheader("🔍 Weather vs. Earthquake Correlation")

    with st.spinner("Merging weather and earthquake data..."):
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

        joined_df = align_weather_quake_data(hourly_df, quake_df)

    st.markdown("### 🔬 Scatter: Magnitude vs Temperature & Humidity")
    fig = plot_magnitude_vs_weather(joined_df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data to generate correlation chart.")
