import streamlit as st
from datetime import date, timedelta

def render_sidebar():
    st.sidebar.title("🔧 Settings")

    # Location input
    st.sidebar.subheader("📍 Location")
    latitude = st.sidebar.number_input("Latitude", min_value=-90.0, max_value=90.0, value=37.7749, format="%.4f")
    longitude = st.sidebar.number_input("Longitude", min_value=-180.0, max_value=180.0, value=-122.4194, format="%.4f")

    # Date range (limit Open-Meteo API max range to 31 days)
    st.sidebar.subheader("🗓️ Date Range")
    today = date.today()
    start_date = st.sidebar.date_input("Start Date", today - timedelta(days=7), max_value=today)
    end_date = st.sidebar.date_input("End Date", today, min_value=start_date, max_value=today)

    # Magnitude filter
    st.sidebar.subheader("🌋 Earthquake Filter")
    min_magnitude = st.sidebar.slider("Minimum Magnitude", 0.0, 10.0, 4.0, step=0.1)

    # Limit (USGS API allows up to 20,000, default 500)
    event_limit = st.sidebar.slider("Max Earthquakes", 10, 2000, 500, step=10)

    return {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "min_magnitude": min_magnitude,
        "limit": event_limit
    }
