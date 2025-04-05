# app/ui/controls.py

import streamlit as st
from datetime import datetime, timedelta
from app.config import boundaries # Import predefined boundaries

def display_sidebar_controls():
    """Displays Streamlit widgets in the sidebar for user input and returns selections."""

    st.sidebar.header("🔎 Filter Options")

    # --- Geographic Scope Selection ---
    # Use keys from the predefined bounding boxes + potentially 'City' later
    available_scopes = list(boundaries.PREDEFINED_BOUNDING_BOXES.keys())
    # available_scopes.append("City (Predefined)") # Add this later if using predefined cities
    # available_scopes.append("City (Custom)") # Add this later if implementing geocoding

    selected_scope = st.sidebar.selectbox(
        "Select Geographic Scope:",
        options=available_scopes,
        index=0 # Default to 'Global'
    )

    # --- Conditional Geographic Inputs (Placeholder for now) ---
    selected_location_params = {"scope": selected_scope}
    if selected_scope != "Global":
        st.sidebar.info(f"Scope selected: {selected_scope}. Using predefined boundaries.")
        # Later, we could add dropdowns for specific countries/regions if needed,
        # or inputs for city name/radius.
        # For now, the main script will fetch the box from boundaries.py

    # --- Time Range Selection ---
    st.sidebar.subheader("🗓️ Time Range")
    # Default to last 30 days
    default_end_date = datetime.now().date()
    default_start_date = default_end_date - timedelta(days=30)

    start_date = st.sidebar.date_input(
        "Start Date",
        value=default_start_date,
        max_value=default_end_date
    )
    end_date = st.sidebar.date_input(
        "End Date",
        value=default_end_date,
        min_value=start_date,
        max_value=default_end_date
    )

    # Convert dates to string format required by API (YYYY-MM-DD)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d') # API endtime is inclusive

    # --- Magnitude Selection ---
    st.sidebar.subheader("📈 Magnitude")
    min_magnitude = st.sidebar.slider(
        "Minimum Magnitude:",
        min_value=0.0,
        max_value=10.0,
        value=3.0, # Default minimum magnitude
        step=0.1
    )

    # --- Limit Selection ---
    st.sidebar.subheader("🔢 Event Limit")
    limit = st.sidebar.number_input(
        "Maximum Number of Events:",
        min_value=10,
        max_value=5000, # API limit is 20000, but keep it reasonable for performance
        value=1000,
        step=10
    )

    return {
        "scope": selected_scope,
        "starttime": start_date_str,
        "endtime": end_date_str,
        "min_magnitude": min_magnitude,
        "limit": limit
        # We will derive bounding_box or lat/lon/radius in main.py based on scope
    }