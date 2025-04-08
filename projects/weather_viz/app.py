import streamlit as st
from geopy.geocoders import Nominatim
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

st.set_page_config(page_title="Weather Visualizer", layout="wide")
st.title("🌤️ Weather Forecast Visualizer")

with st.form(key="city_form"):
    st.subheader("🔍 Enter a City to Visualize Weather")
    city_name = st.text_input("City Name", value="Cleveland, OH")
    fetch_btn = st.form_submit_button("📥 Fetch & Visualize Weather")

# Function to geocode city name
@st.cache_data
def get_coordinates(city):
    try:
        geolocator = Nominatim(user_agent="weather_visualizer_app")
        location = geolocator.geocode(city)
        return (location.latitude, location.longitude) if location else None
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        return None

# Main logic
if fetch_btn:
    if not city_name.strip():
        st.warning("Please enter a valid city name.")
        st.stop()

    with st.spinner("Fetching weather data..."):
        coords = get_coordinates(city_name)

    if not coords:
        st.warning("Could not find the city. Please try a more specific name.")
        st.stop()

    lat, lon = coords
    st.success(f"Coordinates for {city_name}: {lat:.4f}, {lon:.4f}")

    # API Parameters
    hourly_vars = ["temperature_2m", "windspeed_10m", "precipitation", "winddirection_10m", "relativehumidity_2m"]
    daily_vars = ["temperature_2m_max", "temperature_2m_min"]

    # Fetch and process data
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
            fig = temperature_plot.plot_hourly_temperature(hourly_df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = feels_like_temperature_plot.plot_feels_like_temperature(hourly_df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            fig = humidity_plot.plot_humidity(hourly_df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        with col4:
            fig = precipitation_plot.plot_precipitation(hourly_df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        st.subheader("💨 Wind Visualizations")
        col5, col6 = st.columns(2)

        with col5:
            fig = wind_plot.plot_wind_speed(hourly_df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        with col6:
            fig = wind_direction_plot.plot_wind_direction_rose(hourly_df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        fig = wind_speed_direction_plot.plot_wind_speed_and_direction(hourly_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🌡️ Combined Forecasts")
        fig = temperature_humidity_plot.plot_temperature_and_humidity(hourly_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    if daily_df is not None and not daily_df.empty:
        st.subheader("📅 Daily Forecast")
        fig = daily_temperature_range_plot.plot_daily_temperature_range(daily_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
