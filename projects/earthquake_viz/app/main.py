# app/main.py

import streamlit as st
import logging # Import logging

from app.ui import controls
from app.core import usgs_api
from app.config import boundaries
# Import the visualization function (we'll create this next)
# from app.visualizations import map_builder
# We need components for rendering Folium HTML
import streamlit.components.v1 as components

# Configure logging (optional but helpful for debugging Streamlit apps)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Page Configuration ---
st.set_page_config(
    page_title="Earthquake Visualizer",
    page_icon="🌍",
    layout="wide" # Use wide layout for better map display
)

# --- Main Title ---
st.title("🌍 USGS Earthquake Data Visualizer")
st.markdown("Explore recent earthquake data fetched from the USGS API.")

# --- Sidebar Controls ---
user_inputs = controls.display_sidebar_controls()

# --- Data Fetching Logic ---
st.subheader("📊 Visualization")

# Add a button to trigger the data fetching and visualization
if st.sidebar.button("Fetch and Visualize Data", key="fetch_button"):

    api_params = {
        "starttime": user_inputs["starttime"],
        "endtime": user_inputs["endtime"],
        "min_magnitude": user_inputs["min_magnitude"],
        "limit": user_inputs["limit"],
    }
    selected_scope = user_inputs["scope"]

    # Determine geographic parameters based on scope
    bounding_box = None
    if selected_scope == "Global":
        logging.info("Fetching data for Global scope.")
        # No specific geographic params needed beyond defaults unless specified otherwise
        # bounding_box = boundaries.PREDEFINED_BOUNDING_BOXES["Global"] # Optionally pass global box
    elif selected_scope in boundaries.PREDEFINED_BOUNDING_BOXES:
        bounding_box = boundaries.PREDEFINED_BOUNDING_BOXES[selected_scope]
        api_params["bounding_box"] = bounding_box
        logging.info(f"Fetching data for scope: {selected_scope} with box: {bounding_box}")
    # Add elif blocks here later for 'City (Predefined)' or 'City (Custom)'

    # Display a spinner while fetching data
    with st.spinner(f"Fetching earthquake data for '{selected_scope}'... Please wait."):
        geojson_data = usgs_api.fetch_earthquake_data(**api_params)

    # --- Visualization ---
    if geojson_data and 'features' in geojson_data and len(geojson_data['features']) > 0:
        st.success(f"✅ Successfully fetched {len(geojson_data['features'])} events.")
        st.info("Generating map visualization...")

        # Placeholder for map generation - we will uncomment and implement map_builder soon
        # earthquake_map = map_builder.create_earthquake_map(geojson_data, center_on=bounding_box)
        # if earthquake_map:
        #     # Render the Folium map using Streamlit components
        #     map_html = earthquake_map._repr_html_() # Get HTML representation
        #     components.html(map_html, height=600)
        # else:
        #      st.error("❌ Failed to generate map.")
        st.warning("Map generation is not implemented yet. Displaying raw GeoJSON data:")
        st.json(geojson_data, expanded=False) # Display raw data for now

    elif geojson_data and 'features' in geojson_data and len(geojson_data['features']) == 0:
        st.warning(f"⚠️ No earthquake events found matching your criteria for '{selected_scope}'.")
        st.json(geojson_data) # Show the empty response structure
    else:
        st.error("❌ Failed to fetch data from USGS API. Please check logs or try again later.")

else:
    st.info("Adjust the filters in the sidebar and click 'Fetch and Visualize Data' to load results.")