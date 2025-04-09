import streamlit as st
from datetime import datetime, timedelta

from app.core.geo_utils import (
    get_cities_by_admin1,
    get_city_coordinates,
    load_country_code_mapping,
    load_admin1_code_mapping
)

def display_sidebar_controls(country_list: list):
    st.sidebar.header("🔎 Filter Options")

    # Load code mappings
    country_code_map = load_country_code_mapping()
    admin1_code_map = load_admin1_code_mapping()

    # --- Country Selection ---
    st.sidebar.subheader("🌍 Country")
    selected_country = st.sidebar.selectbox(
        "Select Country:",
        options=country_list,
        index=None,
        placeholder="Choose a country..."
    )

    selected_state = None
    selected_city = None
    radius_km = None
    city_list = []

    country_code = None
    admin1_code = None

    # --- State Selection ---
    if selected_country:
        country_code = country_code_map.get(selected_country)
        if country_code:
            matching_admins = sorted([
                name for (code, name) in admin1_code_map.keys() if code == country_code
            ])
            if matching_admins:
                st.sidebar.subheader("🏛️ State/Province")
                selected_state = st.sidebar.selectbox(
                    "Select State/Province:",
                    options=matching_admins,
                    index=None,
                    placeholder="Choose a state..."
                )
                st.sidebar.caption(f"[DEBUG] Country selected: {selected_country}")
                st.sidebar.caption(f"[DEBUG] Resolved country code: {country_code}")

                # Resolve admin1 code
                if selected_state:
                    admin1_code = admin1_code_map.get((country_code, selected_state))

                    # --- City Selection ---
                    if admin1_code:
                        city_list = get_cities_by_admin1(country_code, admin1_code)
                        if city_list:
                            st.sidebar.subheader("🏙️ City + Radius")
                            selected_city = st.sidebar.selectbox(
                                "Select City:",
                                options=city_list,
                                index=None,
                                placeholder="Choose a city..."
                            )
                            radius_km = st.sidebar.slider(
                                "Radius around city (km):",
                                min_value=10, max_value=500, value=100, step=10
                            )

    # --- Date Range ---
    st.sidebar.subheader("🗓️ Time Range")
    default_end = datetime.now().date()
    default_start = default_end - timedelta(days=30)
    start_date = st.sidebar.date_input("Start Date", default_start, max_value=default_end)
    end_date = st.sidebar.date_input("End Date", default_end, min_value=start_date, max_value=default_end)

    # --- Magnitude ---
    st.sidebar.subheader("📈 Magnitude")
    min_magnitude = st.sidebar.slider("Minimum Magnitude:", 0.0, 10.0, 3.0, 0.1)

    # --- Limit ---
    st.sidebar.subheader("🔢 Event Limit")
    limit = st.sidebar.number_input("Maximum Number of Events:", 10, 5000, 1000, 10)

    return {
        "country_name": selected_country,
        "country_code": country_code,
        "state_name": selected_state,
        "admin1_code": admin1_code,
        "city_name": selected_city,
        "radius_km": radius_km,
        "starttime": start_date.strftime("%Y-%m-%d"),
        "endtime": end_date.strftime("%Y-%m-%d"),
        "min_magnitude": min_magnitude,
        "limit": limit
    }
