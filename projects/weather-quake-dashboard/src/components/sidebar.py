import streamlit as st
from datetime import date
import calendar

def render_sidebar():
    st.sidebar.title("🔧 Settings")

    # --- Step 1: Region Selection ---
    st.sidebar.subheader("1️⃣ Select Region")
    st.sidebar.subheader("🗺️ Map Options")
    show_tectonics = st.sidebar.checkbox("Show Tectonic Boundaries", value=True)
    st.session_state["show_tectonics"] = show_tectonics

    default_lat = st.session_state.get("latitude", 37.7749)
    default_lon = st.session_state.get("longitude", -122.4194)

    latitude = st.sidebar.number_input("Latitude", min_value=-90.0, max_value=90.0,
                                       value=default_lat, format="%.4f")
    longitude = st.sidebar.number_input("Longitude", min_value=-180.0, max_value=180.0,
                                        value=default_lon, format="%.4f")

    # --- Step 2: Month & Year Selection ---
    st.sidebar.subheader("2️⃣ Select Month & Year")

    # --- Get available months from session ---
    available_periods = st.session_state.get("available_months", [])

    if available_periods:
        st.caption("🗓️ Only months with earthquake data are shown.")
        selected_period = st.sidebar.selectbox("📆 Select Available Month", available_periods, index=len(available_periods)-1)
        year, month_str = selected_period.split('-')
        month_index = int(month_str)
        year = int(year)
    else:
        # fallback if no data available
        st.sidebar.warning("⚠️ No available months found for this location. Using defaults.")
        current_year = date.today().year
        year = st.sidebar.selectbox("Year", list(range(current_year, current_year - 5, -1)))
        month = st.sidebar.selectbox("Month", list(calendar.month_name)[1:], index=date.today().month - 1)
        month_index = list(calendar.month_name).index(month)

    # Calculate date range
    start_date = date(year, month_index, 1)
    end_day = calendar.monthrange(year, month_index)[1]
    end_date = date(year, month_index, end_day)

    # --- Step 3: Filters ---
    st.sidebar.subheader("3️⃣ Set Filters")
    min_magnitude = st.sidebar.slider("Minimum Earthquake Magnitude", 0.0, 10.0, 4.0, step=0.1)
    max_distance_km = st.sidebar.slider("Max Distance to Tectonic Boundary (km)", 10, 200, 50, step=10)

    # --- Step 4: Data Fetch Button ---
    st.sidebar.subheader("4️⃣ Fetch Data")
    if st.sidebar.button("📥 Fetch & Analyze"):
        st.session_state["data_ready"] = True
        st.session_state["fetch_params"] = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "min_magnitude": min_magnitude,
            "max_distance_km": max_distance_km
        }
        st.sidebar.success("✅ Fetching data...")

    return st.session_state.get("fetch_params", None)
