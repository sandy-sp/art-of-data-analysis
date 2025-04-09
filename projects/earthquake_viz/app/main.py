import streamlit as st
import logging
import pandas as pd

# Local application imports
from app.ui import controls
from app.core import usgs_api
from app.config.boundaries import SHAPEFILE_PATH 
from app.core import geo_utils
from app.visualizations import map_builder
from app.core import data_handler
from app.core.geo_utils import get_city_coordinates

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

user_inputs = controls.display_sidebar_controls(country_list)

# --- DEBUG UI TEST: Display raw values and force State/City dropdowns in main UI ---
st.markdown("---")
st.subheader("🧪 Debug: Current User Inputs")

st.json(user_inputs)

# Check country code resolution
if not user_inputs.get("country_code"):
    st.warning("⚠️ Country code not resolved from selected country name.")

# Force state dropdown from admin1_code_map if country_code exists
if user_inputs.get("country_code"):
    country_code = user_inputs["country_code"]
    admin1_map = geo_utils.load_admin1_code_mapping()
    matching_states = sorted([
        name for (code, name) in admin1_map.keys() if code == country_code
    ])

    if matching_states:
        st.subheader("🏛️ Test State Selection")
        selected_state = st.selectbox("Select a State (Main UI test)", matching_states)
        state_code = admin1_map.get((country_code, selected_state))
        st.write("Resolved Admin1 Code:", state_code)

        # Force city dropdown
        from app.core.geo_utils import get_cities_by_admin1
        cities = get_cities_by_admin1(country_code, state_code)
        if cities:
            st.subheader("🏙️ Test City Selection")
            selected_city = st.selectbox("Select a City (Main UI test)", cities)
            st.write("Selected City:", selected_city)
        else:
            st.info("No cities found for selected state.")
    else:
        st.info("No states found for selected country code.")


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

    country_name = user_inputs.get("country_name")
    state_name = user_inputs.get("state_name")
    city_name = user_inputs.get("city_name")
    radius_km = user_inputs.get("radius_km")
    country_code = user_inputs.get("country_code")
    admin1_code = user_inputs.get("admin1_code")

    execute_fetch = False
    map_center_bounds = None  # Used to center the map

    if not country_name:
        st.error("Please select a country from the dropdown list in the sidebar.")
    else:
        # CITY FILTER
        if city_name and country_code and admin1_code and radius_km:
            logging.info(f"City filter selected: {city_name}, {state_name}")
            coords = get_city_coordinates(country_code, admin1_code, city_name)
            if coords:
                api_params["latitude"] = coords[0]
                api_params["longitude"] = coords[1]
                api_params["max_radius_km"] = radius_km
                map_center_bounds = [coords[1] - 2, coords[0] - 2, coords[1] + 2, coords[0] + 2]
                logging.info(f"Using city radius search: {coords} ± {radius_km} km")
                execute_fetch = True
            else:
                st.error(f"Could not determine coordinates for city: {city_name}")
        # COUNTRY or STATE FILTER
        else:
            logging.info(f"Using fallback bounding box for: {country_name}")
            with st.spinner(f"Looking up boundaries for {country_name}..."):
                map_center_bounds = geo_utils.get_country_bounds(country_name, world_gdf)

            if map_center_bounds:
                api_params["bounding_box"] = map_center_bounds
                logging.info(f"Using bounding box for {country_name}: {map_center_bounds}")
                execute_fetch = True
            else:
                st.error(f"Could not determine boundaries for: {country_name}")


    # Execute API call and visualization
    if execute_fetch:
        with st.spinner(f"📡 Checking cache or fetching data for '{country_name}'..."):
            geojson_data = cached_api_call(**api_params)

        if geojson_data and 'features' in geojson_data and len(geojson_data['features']) > 0:
            num_events = len(geojson_data['features'])
            st.success(f"✅ Found {num_events} earthquake events for '{country_name}' (Data from cache or API).")
            with st.spinner(f"🗺️ Generating map for {num_events} events..."):
                earthquake_map = map_builder.create_earthquake_map(geojson_data, center_on_bounds=map_center_bounds)
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