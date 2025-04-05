# app/main.py

import streamlit as st
import logging # Import logging
import json  # Import json for hashing complex dicts if needed

# Local application imports
from app.ui import controls
from app.core import usgs_api
from app.config import boundaries
from app.visualizations import map_builder # Ensure this is uncommented

# Import Streamlit components for rendering HTML (like Folium maps)
import streamlit.components.v1 as components

# Configure logging (optional but helpful for debugging Streamlit apps)
# Logs will appear in the terminal where you run 'streamlit run ...'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Page Configuration ---
# This should be the first Streamlit command in your script
st.set_page_config(
    page_title="Earthquake Visualizer",
    page_icon="🌍",    # Can be an emoji or a URL
    layout="wide",     # Use wide layout for better map display
    initial_sidebar_state="expanded" # Keep sidebar open initially
)

# --- Main Application Title ---
st.title("🌍 USGS Earthquake Data Visualizer")
st.markdown("Explore recent earthquake data fetched from the USGS API, visualized on an interactive map.")
st.markdown("---") # Visual separator

# --- Sidebar Controls ---
# Display the input widgets in the sidebar and get the user's selections
user_inputs = controls.display_sidebar_controls()

# --- Caching Wrapper Function ---
@st.cache_data(ttl=900, show_spinner=False)  # Cache for 15 minutes
def cached_api_call(**params):
    """Wrapper function to cache the results of fetch_earthquake_data."""
    logging.info(f"CACHE MISS: Calling USGS API with params: {params}")
    # Convert bounding_box list to tuple to make it hashable for caching if present
    if 'bounding_box' in params and isinstance(params['bounding_box'], list):
        params['bounding_box'] = tuple(params['bounding_box'])

    # Ensure all dictionary values are hashable (convert lists/dicts if necessary)
    data = usgs_api.fetch_earthquake_data(**params)
    return data
# --- End Caching Wrapper ---

# --- Main Area for Visualization ---
st.subheader("📊 Visualization")

# Add a button in the sidebar to trigger the data fetching and visualization
if st.sidebar.button("Fetch and Visualize Data", key="fetch_button", help="Click to load data based on current filters"):

    # Prepare parameters for the API call based on user inputs
    api_params = {
        "starttime": user_inputs["starttime"],
        "endtime": user_inputs["endtime"],
        "min_magnitude": user_inputs["min_magnitude"],
        "limit": user_inputs["limit"],
    }
    selected_scope = user_inputs["scope"]
    bounding_box = None # Initialize bounding_box to None

    # Determine geographic parameters based on the selected scope
    if selected_scope == "Global":
        logging.info("Setting scope to Global.")
    elif selected_scope in boundaries.PREDEFINED_BOUNDING_BOXES:
        # Get the predefined bounding box for the selected country/region
        bounding_box = boundaries.PREDEFINED_BOUNDING_BOXES[selected_scope]
        api_params["bounding_box"] = bounding_box # Add bounding box to API params
        logging.info(f"Setting scope: {selected_scope} with box: {bounding_box}")
    # -----
    # TODO: Add 'elif' blocks here later for City scopes
    # Example:
    # elif selected_scope == "City (Predefined)":
    #     selected_city_name = user_inputs.get("city_name") # Assume controls.py returns this
    #     if selected_city_name in boundaries.PREDEFINED_CITIES:
    #          city_info = boundaries.PREDEFINED_CITIES[selected_city_name]
    #          api_params["latitude"] = city_info["lat"]
    #          api_params["longitude"] = city_info["lon"]
    #          api_params["maxradiuskm"] = city_info["default_radius_km"] # Or get radius from user input
    #          logging.info(f"Fetching data for city: {selected_city_name}")
    #      else:
    #          st.sidebar.error(f"Predefined city '{selected_city_name}' not found.")
    #          st.stop() # Stop execution if city is invalid
    # -----

    # Display a spinner manually since it's disabled in the cache decorator
    with st.spinner(f"📡 Checking cache or fetching data for '{selected_scope}'..."):
        # Call the CACHED wrapper function instead of the original API function
        geojson_data = cached_api_call(**api_params)

    # --- Process and Visualize Results ---
    if geojson_data and 'features' in geojson_data and len(geojson_data['features']) > 0:
        num_events = len(geojson_data['features'])
        st.success(f"✅ Found {num_events} earthquake events (Data from cache or API).")

        # Display spinner while generating the potentially complex map
        with st.spinner(f"🗺️ Generating map for {num_events} events... This may take a moment."):
             earthquake_map = map_builder.create_earthquake_map(
                 geojson_data,
                 center_on_bounds=bounding_box # Pass bounds to help center/fit map
             )

        # If map generation was successful, display it
        if earthquake_map:
            st.info("Displaying Interactive Map (Scroll to zoom, Click markers for details):")
            # Render the Folium map using Streamlit components HTML rendering
            map_html = earthquake_map._repr_html_() # Get HTML representation of the map
            components.html(map_html, height=600, scrolling=False) # Adjust height as needed
        else:
             # Handle error if map creation failed despite having data
             st.error("❌ Failed to generate the map visualization.")

    elif geojson_data and 'features' in geojson_data and len(geojson_data['features']) == 0:
        # Handle case where API call was successful but returned no events
        st.warning(f"⚠️ No earthquake events found matching your criteria for '{selected_scope}' (Data from cache or API). Try expanding the time range or lowering the minimum magnitude.")
        # Optionally display an empty map centered on the target area
        st.info("Displaying map of the selected area:")
        with st.spinner("Generating empty map..."):
            empty_map = map_builder.create_earthquake_map({"type": "FeatureCollection", "features": []}, center_on_bounds=bounding_box)
            if empty_map:
                 map_html = empty_map._repr_html_()
                 components.html(map_html, height=500, scrolling=False)

    else:
        # Handle case where the API call itself failed (fetch_earthquake_data returned None)
        st.error("❌ Failed to fetch data from the USGS API. Possible network issue or API error. Check the terminal logs for more details.")

else:
    # Initial message shown before the button is clicked
    st.info("Adjust the filters in the sidebar and click 'Fetch and Visualize Data' to load and display earthquake information.")
    st.markdown("---")

# You can add more sections below if needed, e.g., a data table display
# st.sidebar.markdown("---")
# st.sidebar.info("App created using Streamlit and Folium.")