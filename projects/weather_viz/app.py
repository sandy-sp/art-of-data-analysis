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
from geopy.geocoders import Nominatim
import os

# Ensure output folder exists
os.makedirs("reports/visualizations", exist_ok=True)

st.title("🌤️ Weather Forecast Visualizer")

# Sidebar Inputs
city_name = st.sidebar.text_input("Enter city (e.g., Cleveland, OH):", "Cleveland, OH")
fetch_button = st.sidebar.button("Fetch & Visualize Weather")

def get_coordinates(city_name):
    try:
        geolocator = Nominatim(user_agent="weather_visualization_app")
        location = geolocator.geocode(city_name)
        return (location.latitude, location.longitude) if location else None
    except Exception as e:
        st.error(f"Error getting coordinates: {e}")
        return None

if fetch_button:
    with st.spinner("Fetching weather data..."):
        coords = get_coordinates(city_name)
        if coords:
            lat, lon = coords
            st.success(f"Coordinates: {lat:.4f}, {lon:.4f}")

            # Fetch + process
            hourly_vars = ["temperature_2m", "windspeed_10m", "precipitation", "winddirection_10m", "relativehumidity_2m"]
            daily_vars = ["temperature_2m_max", "temperature_2m_min"]
            data = api_handler.fetch_weather_data(lat, lon, hourly_vars, daily_vars)

            if data:
                hourly_df, daily_df = data_processor.process_weather_data(data)

                # Generate and show each plot
                temperature_plot.plot_hourly_temperature(hourly_df)
                st.image("reports/visualizations/hourly_temperature.png", caption="Hourly Temperature")

                wind_plot.plot_wind_speed(hourly_df)
                st.image("reports/visualizations/wind_plot.png", caption="Wind Speed")

                precipitation_plot.plot_precipitation(hourly_df)
                st.image("reports/visualizations/precipitation_plot.png", caption="Precipitation")

                wind_direction_plot.plot_wind_direction_rose(hourly_df)
                st.image("reports/visualizations/wind_direction_rose.png", caption="Wind Direction Rose")

                daily_temperature_range_plot.plot_daily_temperature_range(daily_df)
                st.image("reports/visualizations/daily_temperature_range_plot.png", caption="Daily Temp Range")

                humidity_plot.plot_humidity(hourly_df)
                st.image("reports/visualizations/humidity_plot.png", caption="Humidity")

                temperature_humidity_plot.plot_temperature_and_humidity(hourly_df)
                st.image("reports/visualizations/temperature_humidity_plot.png", caption="Temp & Humidity")

                wind_speed_direction_plot.plot_wind_speed_and_direction(hourly_df)
                st.image("reports/visualizations/wind_speed_direction_plot.png", caption="Wind Vectors")

                feels_like_temperature_plot.plot_feels_like_temperature(hourly_df)
                st.image("reports/visualizations/feels_like_temperature_plot.png", caption="Feels Like Temp")

            else:
                st.error("Failed to fetch weather data.")
        else:
            st.error("Could not determine coordinates for the city.")
