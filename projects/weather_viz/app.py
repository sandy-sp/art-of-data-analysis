import streamlit as st
from src import api_handler, data_processor
from src.visualizations import (
    temperature_plot,
    wind_plot,
    precipitation_plot,
    wind_direction_plot,
    daily_temperature_range_plot,
    humidity_plot,
    feels_like_temperature_plot,
    temperature_humidity_plot,
    wind_speed_direction_plot
)

# ✅ Sample location dictionary
us_locations = {
    "Ohio": {
        "Cleveland": [41.4993, -81.6944],
        "Columbus": [39.9612, -82.9988],
    },
    "California": {
        "San Francisco": [37.7749, -122.4194],
        "Los Angeles": [34.0522, -118.2437],
    },
    "Texas": {
        "Houston": [29.7604, -95.3698],
        "Dallas": [32.7767, -96.7970],
    },
}

st.set_page_config(page_title="Weather Visualizer", layout="wide")
st.title("🌤️ Weather Forecast Visualizer")

with st.form(key="location_form"):
    st.subheader("📍 Select a US State and City")
    selected_state = st.selectbox("State", list(us_locations.keys()))
    selected_city = st.selectbox("City", list(us_locations[selected_state].keys()))
    fetch_btn = st.form_submit_button("📥 Fetch & Visualize Weather")

# Main logic
if fetch_btn:
    lat, lon = us_locations[selected_state][selected_city]
    location_label = f"{selected_city}, {selected_state}"
    st.success(f"Coordinates for {location_label}: {lat:.4f}, {lon:.4f}")

    # API Parameters
    hourly_vars = ["temperature_2m", "windspeed_10m", "precipitation", "winddirection_10m", "relativehumidity_2m"]
    daily_vars = ["temperature_2m_max", "temperature_2m_min"]

    # Fetch & process data
    with st.spinner("Fetching weather data..."):
        data = api_handler.fetch_weather_data(lat, lon, hourly_vars, daily_vars)

    if not data:
        st.error("Failed to fetch weather data.")
        st.stop()

    hourly_df, daily_df = data_processor.process_weather_data(data)

    if hourly_df is None or hourly_df.empty:
        st.warning("No hourly data available.")
    else:
        st.subheader("📊 Hourly Visualizations")
        col1, col2 = st.columns(2)

        with col1:
            fig = temperature_plot.plot_hourly_temperature(hourly_df, location=location_label)
            if fig: st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = feels_like_temperature_plot.plot_feels_like_temperature(hourly_df, location=location_label)
            if fig: st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            fig = humidity_plot.plot_humidity(hourly_df, location=location_label)
            if fig: st.plotly_chart(fig, use_container_width=True)

        with col4:
            fig = precipitation_plot.plot_precipitation(hourly_df, location=location_label)
            if fig: st.plotly_chart(fig, use_container_width=True)

        st.subheader("💨 Wind Visualizations")
        col5, col6 = st.columns(2)

        with col5:
            fig = wind_plot.plot_wind_speed(hourly_df, location=location_label)
            if fig: st.plotly_chart(fig, use_container_width=True)

        with col6:
            fig = wind_direction_plot.plot_wind_direction_rose(hourly_df, location=location_label)
            if fig: st.plotly_chart(fig, use_container_width=True)

        fig = wind_speed_direction_plot.plot_wind_speed_and_direction(hourly_df, location=location_label)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🌡️ Combined Forecasts")
        fig = temperature_humidity_plot.plot_temperature_and_humidity(hourly_df, location=location_label)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    if daily_df is not None and not daily_df.empty:
        st.subheader("📅 Daily Forecast")
        fig = daily_temperature_range_plot.plot_daily_temperature_range(daily_df, location=location_label)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
