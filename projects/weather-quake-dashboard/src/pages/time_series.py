import streamlit as st
from src.utils.visualization import plot_temperature_humidity, plot_earthquake_frequency


def display_timeseries(data_bundle):
    st.subheader("📈 Time Series Plots")

    hourly_df = data_bundle["weather"]
    quake_df = data_bundle["earthquakes"]

    if hourly_df.empty:
        st.warning("No weather data available for the selected location and time range.")
    if quake_df.empty:
        st.warning("No earthquake data available for the selected location and time range.")

    st.markdown("### 🌡️ Temperature and Humidity")
    fig1 = plot_temperature_humidity(hourly_df)
    if fig1:
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No data to plot temperature and humidity.")

    st.markdown("### 🌋 Earthquake Frequency")
    fig2 = plot_earthquake_frequency(quake_df)
    if fig2:
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data to plot earthquake frequency.")
