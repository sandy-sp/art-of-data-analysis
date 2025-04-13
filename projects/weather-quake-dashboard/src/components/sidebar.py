import streamlit as st
from datetime import date
import calendar

def render_sidebar():
    st.sidebar.title("🔧 Settings")

    # Location input
    st.sidebar.subheader("📍 Location")

    default_lat = st.session_state.get("latitude", 37.7749)
    default_lon = st.session_state.get("longitude", -122.4194)

    latitude = st.sidebar.number_input("Latitude", min_value=-90.0, max_value=90.0, value=default_lat, format="%.4f")
    longitude = st.sidebar.number_input("Longitude", min_value=-180.0, max_value=180.0, value=default_lon, format="%.4f")

    # Month and Year input (replaces Start/End Date)
    st.sidebar.subheader("🗓️ Date (Open-Meteo supports one month only)")
    current_year = date.today().year
    year = st.sidebar.selectbox("Year", list(range(current_year, current_year - 5, -1)))
    month = st.sidebar.selectbox("Month", list(calendar.month_name)[1:])

    # Compute start and end date for API
    month_index = list(calendar.month_name).index(month)
    start_date = date(year, month_index, 1)
    end_day = calendar.monthrange(year, month_index)[1]
    end_date = date(year, month_index, end_day)

    # Magnitude filter
    st.sidebar.subheader("🌋 Earthquake Filter")
    min_magnitude = st.sidebar.slider("Minimum Magnitude", 0.0, 10.0, 4.0, step=0.1)

    # Limit (USGS API allows up to 20,000, default 500)
    event_limit = st.sidebar.slider("Max Earthquakes", 10, 2000, 500, step=10)

    # Fetch data button
    fetch_btn = st.sidebar.button("📥 Fetch & Analyze")
    if fetch_btn:
        st.session_state["data_ready"] = True

    return {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "min_magnitude": min_magnitude,
        "limit": event_limit
    }
