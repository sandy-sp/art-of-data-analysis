import streamlit as st
from src.utils.data_processing import align_weather_quake_data
from src.utils.visualization import plot_magnitude_vs_weather


def display_correlation_analysis(data_bundle):
    st.subheader("🔍 Weather vs. Earthquake Correlation")

    hourly_df = data_bundle["weather"]
    quake_df = data_bundle["earthquakes"]

    if hourly_df.empty:
        st.warning("No weather data available for the selected location and time range.")
    if quake_df.empty:
        st.warning("No earthquake data available for the selected location and time range.")

    joined_df = align_weather_quake_data(hourly_df, quake_df)

    st.markdown("### 🔬 Scatter: Magnitude vs Temperature & Humidity")
    fig = plot_magnitude_vs_weather(joined_df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data to generate correlation chart.")