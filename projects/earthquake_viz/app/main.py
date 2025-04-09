import streamlit as st
import logging
import json
import pandas as pd

# Local application imports
from app.ui import controls
from app.core import usgs_api
from app.config.boundaries import SHAPEFILE_PATH  # Import specific path
from app.core import geo_utils
from app.visualizations import map_builder
from app.core import data_handler

# Import Streamlit components
import streamlit.components.v1 as components

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Page configuration
st.set_page_config(page_title="Earthquake Visualizer", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

st.title("🌍 USGS Earthquake Data Visualizer")
st.markdown("Enter a country name to explore recent earthquake data within its boundaries.")
st.markdown("---")

# Load shapefile and country list
with st.spinner("Loading world boundaries map and country list..."):
    world_gdf, country_list = geo_utils.load_world_shapefile(SHAPEFILE_PATH)  # Adjusted call to unpack tuple

if world_gdf is None or country_list is None:  # Check both parts
    st.error("Application cannot start because the world boundaries data failed to load. Please check the path and file integrity.")
    st.stop()

# Sidebar controls
user_inputs = controls.display_sidebar_controls(country_list)  # Pass country_list to controls function

# Caching wrapper function
@st.cache_data(ttl=900, show_spinner=False)
def cached_api_call(**params):
    logging.info(f"CACHE MISS: Calling USGS API with params: {params}")
    if 'bounding_box' in params and isinstance(params['bounding_box'], list):
        params['bounding_box'] = tuple(params['bounding_box'])
    data = usgs_api.fetch_earthquake_data(**params)
    return data

st.subheader("📊 Visualization & Data")

if st.sidebar.button("Fetch and Visualize Data", key="fetch_button", help="Click to load data based on current filters"):

    api_params = {
        "starttime": user_inputs["starttime"],
        "endtime": user_inputs["endtime"],
        "min_magnitude": user_inputs["min_magnitude"],
        "limit": user_inputs["limit"],
    }
    bounding_box = None
    execute_fetch = False
    country_name = user_inputs.get("country_name")

    # Validate country input and get bounds
    if not country_name:
        st.error("Please select a country from the dropdown list in the sidebar.")  # Updated error message
    else:
        logging.info(f"Attempting to find bounds for country: {country_name}")
        with st.spinner(f"Looking up boundaries for {country_name}..."):
            bounding_box = geo_utils.get_country_bounds(country_name, world_gdf)

        if bounding_box:
            api_params["bounding_box"] = bounding_box
            logging.info(f"Using bounds for {country_name}: {bounding_box}")
            execute_fetch = True
        else:
            st.error(f"Could not find boundaries for selected country '{country_name}'.")

    # Execute API call and visualization
    if execute_fetch:
        with st.spinner(f"📡 Checking cache or fetching data for '{country_name}'..."):
            geojson_data = cached_api_call(**api_params)

        if geojson_data and 'features' in geojson_data and len(geojson_data['features']) > 0:
            num_events = len(geojson_data['features'])
            st.success(f"✅ Found {num_events} earthquake events for '{country_name}' (Data from cache or API).")
            with st.spinner(f"🗺️ Generating map for {num_events} events..."):
                earthquake_map = map_builder.create_earthquake_map(geojson_data, center_on_bounds=bounding_box)
            if earthquake_map:
                st.info("Displaying Interactive Map:")
                map_html = earthquake_map._repr_html_()
                components.html(map_html, height=600, scrolling=False)
            else:
                st.error("❌ Failed to generate map.")
            st.markdown("---")
            st.subheader("📄 Data Table")
            with st.spinner("Preparing data table..."):
                df = data_handler.geojson_to_dataframe(geojson_data)
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download data as CSV", data=csv, file_name=f'earthquake_data_{country_name}.csv', mime='text/csv')
            elif df is not None:
                st.info("No features for table.")
            else:
                st.warning("Could not process data into table.")

        elif geojson_data and 'features' in geojson_data and len(geojson_data['features']) == 0:
            st.warning(f"⚠️ No earthquake events found matching your criteria for '{country_name}'.")
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
            st.error("❌ Failed to fetch data from the USGS API.")

else:
    st.info("Select a country in the sidebar and click 'Fetch and Visualize Data' to load earthquake information.")  # Updated message
    st.markdown("---")