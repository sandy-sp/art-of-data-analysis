# app/ui/controls.py
import streamlit as st
from datetime import datetime, timedelta
# Import only the lookup function types needed, not data loaders
from app.core.geo_utils import (
    get_iso_code_for_country,
    get_admin1_names_for_country,
    get_admin1_code,
    get_cities_for_admin1
)
import logging
from typing import Dict, Any # For type hinting geo_data

# Accept the loaded geo_data dictionary
def display_sidebar_controls(geo_data: Dict[str, Any]):
    """Displays filtering controls in the sidebar and returns selections."""
    st.sidebar.header("🔎 Filter Options")

    # --- Retrieve necessary data from the passed dictionary ---
    ne_country_list = geo_data.get("ne_country_list", [])
    ne_name_to_iso_map = geo_data.get("ne_name_to_iso_map", {})
    admin1_data = geo_data.get("admin1_data", {})
    cities_df = geo_data.get("cities_df", pd.DataFrame()) # Get DataFrame or empty

    # Initialize user_inputs dictionary (same as before)
    user_inputs = {
        "selected_level": "Global", # Default level
        "country_name": None, "country_iso_code": None,
        "state_name": None, "admin1_code": None,
        "city_name": None, "radius_km": None,
        "starttime": None, "endtime": None,
        "min_magnitude": 3.0, "limit": 1000
    }

    # --- Geographic Level Selection ---
    st.sidebar.subheader("🌍 Geographic Filter")

    selected_country = st.sidebar.selectbox(
        "Select Country:",
        options=ne_country_list or ["Error: Countries failed to load"],
        index=None, placeholder="Start by choosing a country..."
    )
    user_inputs["country_name"] = selected_country

    admin1_options = []
    city_options = []

    if selected_country:
        user_inputs["selected_level"] = "Country"
        # Use the passed map
        iso_code = get_iso_code_for_country(selected_country, ne_name_to_iso_map)
        user_inputs["country_iso_code"] = iso_code
        logging.debug(f"Selected Country: {selected_country}, Resolved ISO Code: {iso_code}")

        if iso_code:
             # Use the passed admin1_data
            admin1_options = get_admin1_names_for_country(iso_code, admin1_data)
            if admin1_options:
                selected_state = st.sidebar.selectbox(
                    "Select State/Province (Optional):",
                    options=admin1_options, index=None, placeholder="Filter by state..."
                )
                user_inputs["state_name"] = selected_state

                if selected_state:
                    user_inputs["selected_level"] = "State"
                    # Use the passed admin1_data
                    admin1_code = get_admin1_code(iso_code, selected_state, admin1_data)
                    user_inputs["admin1_code"] = admin1_code
                    logging.debug(f"Selected State: {selected_state}, Resolved Admin1 Code: {admin1_code}")

                    if admin1_code is not None:
                        # Use the passed cities_df
                        city_options = get_cities_for_admin1(iso_code, admin1_code, cities_df)
                        if city_options:
                            selected_city = st.sidebar.selectbox(
                                "Select City (Optional):",
                                options=city_options, index=None, placeholder="Filter by city..."
                            )
                            user_inputs["city_name"] = selected_city

                            if selected_city:
                                user_inputs["selected_level"] = "City"
                                radius_km = st.sidebar.slider(
                                    "Radius around city (km):",
                                    min_value=10, max_value=500, value=100, step=10,
                                    help="Required for city-based search."
                                )
                                user_inputs["radius_km"] = radius_km
                                logging.debug(f"Selected City: {selected_city}, Radius: {radius_km}km")
            else:
                 st.sidebar.caption(f"No state/province data found for {selected_country}")
        else:
             st.sidebar.warning(f"Could not map '{selected_country}' to an ISO code. State/City filtering unavailable.")
    else:
         st.sidebar.caption("Select a country to enable further filtering.")

    # --- Other Filters (remain the same) ---
    st.sidebar.subheader("⚙️ Other Filters")
    default_end = datetime.now().date()
    default_start = default_end - timedelta(days=30)
    start_date = st.sidebar.date_input("Start Date", default_start, max_value=default_end)
    end_date = st.sidebar.date_input("End Date", default_end, min_value=start_date, max_value=default_end)
    user_inputs["starttime"] = start_date.strftime("%Y-%m-%d")
    user_inputs["endtime"] = end_date.strftime("%Y-%m-%d")
    user_inputs["min_magnitude"] = st.sidebar.slider("Minimum Magnitude:", 0.0, 10.0, user_inputs["min_magnitude"], 0.1)
    user_inputs["limit"] = st.sidebar.number_input("Maximum Number of Events:", 10, 5000, user_inputs["limit"], 10)

    return user_inputs