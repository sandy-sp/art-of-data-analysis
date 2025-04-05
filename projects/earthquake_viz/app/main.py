import streamlit as st
import logging # Import logging
import json  # Import json for hashing complex dicts if needed
import pandas as pd  # Import pandas

# Local application imports
from app.ui import controls
from app.core import usgs_api
from app.config import boundaries, settings  # Import settings if needed elsewhere
from app.visualizations import map_builder # Ensure this is uncommented
from app.core import data_handler  # <--- IMPORT data_handler
from app.core import geo_utils  # <--- IMPORT geo_utils

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

# --- Load Shapefile (Cached) ---
# Load this once at the start using the cached function from geo_utils
# The actual loading only happens once per session due to @st.cache_resource
shapefile_path = boundaries.SHAPEFILE_PATH
with st.spinner("Loading world boundaries map..."):
    world_gdf = geo_utils.load_world_shapefile(shapefile_path)

# If shapefile loading fails, stop the app gracefully
if world_gdf is None:
    st.error("Application cannot start because the world boundaries shapefile failed to load. Please check the path and file integrity.")
    st.stop()  # Stop script execution

# --- Main Area for Visualization ---
st.subheader("📊 Visualization & Data")  # Update subheader slightly

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
    execute_fetch = True  # Initialize execute_fetch to True

    # Determine geographic parameters based on the selected scope
    if selected_scope == "Global":
        logging.info("Setting scope to Global.")
    elif selected_scope in boundaries.PREDEFINED_BOUNDING_BOXES:
        # Get the predefined bounding box for the selected country/region
        bounding_box = boundaries.PREDEFINED_BOUNDING_BOXES[selected_scope]
        api_params["bounding_box"] = bounding_box # Add bounding box to API params
        logging.info(f"Setting scope: {selected_scope} with box: {bounding_box}")
    elif selected_scope == "Country (Enter Name)":  # <--- ADD THIS BLOCK
        country_name = user_inputs.get("country_name", "").strip()
        if not country_name:
            st.error("Please enter a country name.")
            execute_fetch = False  # Don't fetch if name is empty
        else:
            logging.info(f"Attempting to find bounds for country: {country_name}")
            with st.spinner(f"Looking up boundaries for {country_name}..."):
                bounding_box = geo_utils.get_country_bounds(country_name, world_gdf)

            if bounding_box:
                api_params["bounding_box"] = bounding_box
                logging.info(f"Using bounds for {country_name}: {bounding_box}")
            else:
                st.error(f"Could not find boundaries for '{country_name}'. Please check the spelling or try a different name.")
                execute_fetch = False  # Don't fetch if bounds not found
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

    if execute_fetch:  # Only proceed if geographic parameters were valid
        # Display a spinner manually since it's disabled in the cache decorator
        with st.spinner(f"📡 Checking cache or fetching data for '{selected_scope}'..."):
            # Call the CACHED wrapper function instead of the original API function
            geojson_data = cached_api_call(**api_params)

        # --- Process and Visualize Results ---
        if geojson_data and 'features' in geojson_data and len(geojson_data['features']) > 0:
            num_events = len(geojson_data['features'])
            st.success(f"✅ Found {num_events} earthquake events (Data from cache or API).")

            # --- Map Generation ---
            with st.spinner(f"🗺️ Generating map for {num_events} events..."):
                 earthquake_map = map_builder.create_earthquake_map(
                     geojson_data,
                     center_on_bounds=bounding_box
                 )
            if earthquake_map:
                st.info("Displaying Interactive Map:")
                map_html = earthquake_map._repr_html_()
                components.html(map_html, height=600, scrolling=False)
            else:
                 st.error("❌ Failed to generate the map visualization.")

            # --- Data Table Generation ---                       # <--- NEW SECTION START
            st.markdown("---")  # Add a separator
            st.subheader("📄 Data Table")
            with st.spinner("Preparing data table..."):
                df = data_handler.geojson_to_dataframe(geojson_data)

            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True)  # Display the dataframe
                # Provide download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                     label="Download data as CSV",
                     data=csv,
                     file_name=f'earthquake_data_{user_inputs["starttime"]}_to_{user_inputs["endtime"]}.csv',
                     mime='text/csv',
                 )
            elif df is not None and df.empty:
                 st.info("No features found in data to display in table.")  # Should match map message
            else:
                st.warning("Could not process data into a table format.")
            # --- NEW SECTION END ---

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
            st.subheader("📄 Data Table")
            empty_df = data_handler.geojson_to_dataframe({"type": "FeatureCollection", "features": []})
            if empty_df is not None:
                 st.dataframe(empty_df, use_container_width=True)

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