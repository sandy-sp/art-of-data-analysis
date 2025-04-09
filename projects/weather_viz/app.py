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

@st.cache_resource
def save_fig_as_png(fig):
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    return buf

st.set_page_config(page_title="Weather Visualizer", layout="wide")
st.title("\U0001F324\uFE0F Weather Forecast Visualizer")

st.markdown("""
This tool fetches and visualizes **7-day weather forecasts** for any valid **U.S. ZIP code**.
Enter a ZIP code below and view interactive charts for temperature, humidity, wind, and more.
""")

if st.button("🔄 Reset & Enter New ZIP Code"):
    st.session_state.clear()
    st.rerun()

if "form_submitted" not in st.session_state:
    st.session_state["form_submitted"] = False

with st.form(key="zip_form"):
    st.subheader("\U0001F4CD Enter a U.S. ZIP Code")
    zip_code_input = st.text_input("ZIP Code", max_chars=5, placeholder="e.g., 44114")
    fetch_btn = st.form_submit_button("\U0001F4E5 Fetch & Visualize Weather")

if fetch_btn:
    zip_code_cleaned = zip_code_input.strip()

    if not zip_code_cleaned:
        st.warning("Please enter a ZIP code.")
        st.stop()

    if not zip_code_cleaned.isdigit() or len(zip_code_cleaned) != 5:
        st.warning("ZIP code must be exactly 5 digits.")
        st.stop()

    location_label, coords = get_location_from_zip(zip_code_cleaned)
    if not coords:
        st.error("Invalid ZIP code. Please try again.")
        st.stop()

    lat, lon = coords
    st.success(f"\U0001F4CC Location: {location_label} ({lat:.4f}, {lon:.4f})")

    hourly_vars = ["temperature_2m", "windspeed_10m", "precipitation", "winddirection_10m", "relativehumidity_2m"]
    daily_vars = ["temperature_2m_max", "temperature_2m_min"]

    with st.spinner("Fetching weather data..."):
        data = api_handler.fetch_weather_data(lat, lon, hourly_vars, daily_vars)

    if not data:
        st.error("Failed to fetch weather data.")
        st.stop()

    hourly_df, daily_df = data_processor.process_weather_data(data)

    st.session_state["form_submitted"] = True
    st.session_state["hourly_df"] = hourly_df
    st.session_state["daily_df"] = daily_df
    st.session_state["location_label"] = location_label
    st.session_state["zip_code_input"] = zip_code_cleaned

if st.session_state["form_submitted"]:
    hourly_df = st.session_state["hourly_df"]
    daily_df = st.session_state["daily_df"]
    location_label = st.session_state["location_label"]
    zip_code_input = st.session_state["zip_code_input"]
    # Display summary info above graphs
    try:
        start_date = hourly_df["time"].dt.date.min().strftime('%B %d, %Y')
        end_date = hourly_df["time"].dt.date.max().strftime('%B %d, %Y')
    except Exception:
        start_date = end_date = "Unavailable"
    st.markdown(f"### 📍 Forecast for **{location_label}** ({zip_code_input})")
    st.markdown(f"**Date Range:** {start_date} — {end_date}")
    st.markdown("---")
    hourly_df = st.session_state["hourly_df"]
    daily_df = st.session_state["daily_df"]
    location_label = st.session_state["location_label"]
    zip_code_input = st.session_state["zip_code_input"]

    if hourly_df is not None and not hourly_df.empty:
        csv_name = f"weather_data_{zip_code_input}.csv"
        xlsx_name = f"weather_data_{zip_code_input}.xlsx"

        with st.expander("\U0001F4C1 Download Weather Data"):
            st.download_button(
                label="⬇️ Download Weather Data (CSV)",
                data=hourly_df.to_csv(index=False).encode(),
                file_name=csv_name,
                mime="text/csv"
            )

            excel_buf = BytesIO()
            with pd.ExcelWriter(excel_buf, engine='openpyxl') as writer:
                hourly_df.to_excel(writer, sheet_name="Hourly", index=False)
                if daily_df is not None:
                    daily_df.to_excel(writer, sheet_name="Daily", index=False)

            st.download_button(
                label="⬇️ Download Weather Data (Excel)",
                data=excel_buf.getvalue(),
                file_name=xlsx_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.markdown("---")

    if hourly_df is not None and not hourly_df.empty:
        st.subheader("\U0001F4CA Hourly Visualizations")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(temperature_plot.plot_hourly_temperature(hourly_df, location=location_label), use_container_width=True)
        with col2:
            st.plotly_chart(feels_like_temperature_plot.plot_feels_like_temperature(hourly_df, location=location_label), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(humidity_plot.plot_humidity(hourly_df, location=location_label), use_container_width=True)
        with col4:
            st.plotly_chart(precipitation_plot.plot_precipitation(hourly_df, location=location_label), use_container_width=True)

        st.subheader("\U0001F4A8 Wind Visualizations")
        col5, col6 = st.columns(2)
        with col5:
            st.plotly_chart(wind_plot.plot_wind_speed(hourly_df, location=location_label), use_container_width=True)
        with col6:
            st.plotly_chart(wind_direction_plot.plot_wind_direction_rose(hourly_df, location=location_label), use_container_width=True)

        st.plotly_chart(wind_speed_direction_plot.plot_wind_speed_and_direction(hourly_df, location=location_label), use_container_width=True)

        st.subheader("\U0001F321\uFE0F Combined Forecasts")
        st.plotly_chart(temperature_humidity_plot.plot_temperature_and_humidity(hourly_df, location=location_label), use_container_width=True)

    if daily_df is not None and not daily_df.empty:
        st.subheader("\U0001F4C5 Daily Forecast")
        st.plotly_chart(daily_temperature_range_plot.plot_daily_temperature_range(daily_df, location=location_label), use_container_width=True)
