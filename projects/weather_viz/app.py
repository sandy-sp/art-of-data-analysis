import streamlit as st
import pandas as pd
import pgeocode
from io import BytesIO
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

@st.cache_data
def get_location_from_zip(zip_code):
    nomi = pgeocode.Nominatim('us')
    result = nomi.query_postal_code(zip_code)
    if pd.notna(result.latitude) and pd.notna(result.longitude):
        label = f"{result.place_name}, {result.state_name}"
        return label, (result.latitude, result.longitude)
    return None, None

st.set_page_config(page_title="Weather Visualizer", layout="wide")
st.title("🌤️ Weather Forecast Visualizer")

with st.form(key="zip_form"):
    st.subheader("📍 Enter a U.S. ZIP Code")
    zip_code_input = st.text_input("ZIP Code", max_chars=5, placeholder="e.g., 44114")
    fetch_btn = st.form_submit_button("📥 Fetch & Visualize Weather")

if fetch_btn:
    if not zip_code_input.strip():
        st.warning("Please enter a ZIP code.")
        st.stop()

    location_label, coords = get_location_from_zip(zip_code_input.strip())
    if not coords:
        st.error("Invalid ZIP code. Please try again.")
        st.stop()

    lat, lon = coords
    st.success(f"📌 Location: {location_label} ({lat:.4f}, {lon:.4f})")

    hourly_vars = ["temperature_2m", "windspeed_10m", "precipitation", "winddirection_10m", "relativehumidity_2m"]
    daily_vars = ["temperature_2m_max", "temperature_2m_min"]

    with st.spinner("Fetching weather data..."):
        data = api_handler.fetch_weather_data(lat, lon, hourly_vars, daily_vars)

    if not data:
        st.error("Failed to fetch weather data.")
        st.stop()

    hourly_df, daily_df = data_processor.process_weather_data(data)

    if hourly_df is not None and not hourly_df.empty:
        # 📥 Download CSV
        st.download_button(
            label="⬇️ Download Hourly Data (CSV)",
            data=hourly_df.to_csv(index=False).encode(),
            file_name="hourly_data.csv",
            mime="text/csv"
        )
        # 📥 Download Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            hourly_df.to_excel(writer, sheet_name="Hourly", index=False)
            if daily_df is not None:
                daily_df.to_excel(writer, sheet_name="Daily", index=False)
        st.download_button(
            label="⬇️ Download All Data (Excel)",
            data=output.getvalue(),
            file_name="weather_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

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
