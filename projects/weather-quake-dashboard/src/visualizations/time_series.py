import streamlit as st
from src.utils.visualization import (
    plot_temperature_humidity,
    plot_earthquake_frequency,
    plot_magnitude_histogram
)
from src.utils.data_processing import summarize_earthquake_stats


def display_timeseries(data_bundle):
    st.subheader("📈 Time Series Plots")

    hourly_df = data_bundle["weather"]
    quake_df = data_bundle["earthquakes"]

    if hourly_df.empty:
        st.warning("No weather data available for the selected location and time range.")
    if quake_df.empty:
        st.warning("No earthquake data available for the selected location and time range.")

    # Summary stats
    st.markdown("### 📊 Earthquake Summary")
    summary = summarize_earthquake_stats(quake_df)
    st.write({
        "Total Events": summary.get("total", 0),
        "Average Magnitude": summary.get("avg_magnitude", "-"),
        "Max Magnitude": summary.get("max_magnitude", "-"),
        "Deepest Quake (km)": summary.get("deepest", "-")
    })

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

    st.markdown("### 📐 Magnitude Distribution")
    fig3 = plot_magnitude_histogram(quake_df)
    if fig3:
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No data to plot magnitude histogram.")
