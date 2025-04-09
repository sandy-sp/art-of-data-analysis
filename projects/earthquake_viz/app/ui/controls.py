import streamlit as st
from datetime import datetime, timedelta

def display_sidebar_controls(country_list: list):  # Add country_list parameter
    """Displays Streamlit widgets in the sidebar for user input and returns selections."""

    st.sidebar.header("🔎 Filter Options")

    # --- Geographic Input (Country Selection) ---
    st.sidebar.subheader("🌍 Location")
    selected_country = st.sidebar.selectbox(
        "Select Country:",
        options=country_list,  # Use the list from the shapefile
        index=None,  # Start with no selection
        placeholder="Choose a country..."  # Show placeholder text
    )

    # --- Time Range Selection ---
    st.sidebar.subheader("🗓️ Time Range")
    default_end_date = datetime.now().date()
    default_start_date = default_end_date - timedelta(days=30)
    start_date = st.sidebar.date_input("Start Date", value=default_start_date, max_value=default_end_date)
    end_date = st.sidebar.date_input("End Date", value=default_end_date, min_value=start_date, max_value=default_end_date)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # --- Magnitude Selection ---
    st.sidebar.subheader("📈 Magnitude")
    min_magnitude = st.sidebar.slider("Minimum Magnitude:", 0.0, 10.0, 3.0, 0.1)

    # --- Limit Selection ---
    st.sidebar.subheader("🔢 Event Limit")
    limit = st.sidebar.number_input("Maximum Number of Events:", 10, 5000, 1000, 10)

    # Return all selections
    final_selections = {
        "country_name": selected_country,  # Use selected_country from selectbox
        "starttime": start_date_str,
        "endtime": end_date_str,
        "min_magnitude": min_magnitude,
        "limit": limit
    }
    return final_selections