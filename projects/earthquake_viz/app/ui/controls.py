import streamlit as st
from datetime import datetime, timedelta
from app.core.geo_utils import get_cities_by_admin1, get_city_coordinates

def display_sidebar_controls(country_list: list):
    st.sidebar.header("🔎 Filter Options")

    # --- Country Selection ---
    st.sidebar.subheader("🌍 Location")
    selected_country = st.sidebar.selectbox(
        "Select Country:",
        options=country_list,
        index=None,
        placeholder="Choose a country..."
    )

    selected_state = None
    selected_city = None
    radius_km = None

    if selected_state:
        # Map state name → admin1 code
        # For now, let’s assume admin1_code = selected_state (in practice, map via Admin1 file)
        admin1_code = selected_state  # TODO: map properly using admin1CodesASCII.txt
        country_code = "US"  # TODO: map selected_country → ISO code

        city_list = get_cities_by_admin1(country_code, admin1_code)
        if city_list:
            selected_city = st.sidebar.selectbox("Select City:", options=city_list)
            radius_km = st.sidebar.slider("Radius around city (km):", 10, 500, 100, 10)

    # --- Date Range ---
    st.sidebar.subheader("🗓️ Time Range")
    default_end_date = datetime.now().date()
    default_start_date = default_end_date - timedelta(days=30)
    start_date = st.sidebar.date_input("Start Date", default_start_date, max_value=default_end_date)
    end_date = st.sidebar.date_input("End Date", default_end_date, min_value=start_date, max_value=default_end_date)

    # --- Magnitude ---
    st.sidebar.subheader("📈 Magnitude")
    min_magnitude = st.sidebar.slider("Minimum Magnitude:", 0.0, 10.0, 3.0, 0.1)

    # --- Limit ---
    st.sidebar.subheader("🔢 Event Limit")
    limit = st.sidebar.number_input("Maximum Number of Events:", 10, 5000, 1000, 10)

    return {
        "country_name": selected_country,
        "state_name": selected_state,
        "city_name": selected_city,
        "radius_km": radius_km,
        "starttime": start_date.strftime("%Y-%m-%d"),
        "endtime": end_date.strftime("%Y-%m-%d"),
        "min_magnitude": min_magnitude,
        "limit": limit
    }