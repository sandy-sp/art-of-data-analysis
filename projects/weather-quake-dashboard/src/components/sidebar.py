import streamlit as st
from datetime import date
import calendar

def render_sidebar():
    st.sidebar.title("⚙️ Dashboard Controls")

    # --- Map & Display Settings ---
    with st.sidebar.expander("🗺️ Map Display Options", expanded=True):
        show_tectonics = st.checkbox("Show Tectonic Boundaries", value=True, key='tectonics_sidebar')
        st.session_state["show_tectonics"] = show_tectonics

        latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0,
                                   value=st.session_state.get("latitude", 37.7749), format="%.4f")
        longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0,
                                    value=st.session_state.get("longitude", -122.4194), format="%.4f")

    # --- Month & Year Filter ---
    with st.sidebar.expander("📅 Date Range Selection", expanded=True):
        available_periods = st.session_state.get("available_months", [])

        if available_periods:
            st.caption("🗓️ Only months with earthquake data are shown.")
            selected_period = st.selectbox("Select Available Month", available_periods, index=len(available_periods) - 1)
            year, month_str = selected_period.split('-')
            month_index = int(month_str)
            year = int(year)
        else:
            st.warning("⚠️ No available months found for this location. Using current month.")
            current_year = date.today().year
            year = st.selectbox("Year", list(range(current_year, current_year - 5, -1)))
            month = st.selectbox("Month", list(calendar.month_name)[1:], index=date.today().month - 1)
            month_index = list(calendar.month_name).index(month)

        start_date = date(year, month_index, 1)
        end_day = calendar.monthrange(year, month_index)[1]
        end_date = date(year, month_index, end_day)

    # --- Earthquake Filters ---
    with st.sidebar.expander("📊 Earthquake Filters", expanded=True):
        min_magnitude = st.slider("Minimum Magnitude", 0.0, 10.0, 4.0, step=0.1)
        max_distance_km = st.slider("Max Distance from Tectonic Plate (km)", 10, 1000, 50, step=10)

    # --- Final Fetch Button ---
    st.sidebar.markdown("---")
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
        st.sidebar.success("✅ Fetch parameters submitted.")

    return st.session_state.get("fetch_params", None)
