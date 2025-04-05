import streamlit as st
from datetime import datetime, timedelta
# from app.config import boundaries # No longer needed here

def display_sidebar_controls():
    """Displays Streamlit widgets in the sidebar for user input and returns selections."""

    st.sidebar.header("🔎 Filter Options")

    # --- Geographic Input (Country Name Only) ---
    st.sidebar.subheader("🌍 Location")
    country_name_input = st.sidebar.text_input(
        "Enter Country Name:",
        help="Enter the English name of the country (e.g., Germany, Japan, Brazil)."
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
        # Scope is implicitly "Country" now
        "country_name": country_name_input.strip() if country_name_input else None, # Pass stripped name or None
        "starttime": start_date_str,
        "endtime": end_date_str,
        "min_magnitude": min_magnitude,
        "limit": limit
    }
    return final_selections