# app/main.py
import streamlit as st

# --- Page config MUST be the first Streamlit command ---
st.set_page_config(
    page_title="Earthquake Visualizer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
# --------------------------------------------------------

import logging
import pandas as pd

# Local application imports (Now safe to import after set_page_config)
from app.ui import controls
from app.core import usgs_api
# Import the functions, not the pre-loaded data constants
from app.core.geo_utils import (
    load_world_shapefile,
    load_geonames_iso_codes, # New function
    load_country_name_to_iso_mapping,
    load_admin1_data,
    load_geonames_cities,
    get_iso_code_for_country, # Keep lookup functions
    get_admin1_names_for_country,
    get_admin1_code,
    get_cities_for_admin1,
    get_city_coordinates,
    get_country_bounds
)
from app.visualizations import map_builder
from app.core import data_handler

# Import Streamlit components
import streamlit.components.v1 as components

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Load Data Function (with robust error handling) ---
def load_initial_data():
    """Loads geographic data, creates NE Name -> ISO map using shapefile codes."""
    geo_data_dict = {
        "world_gdf": None, "ne_country_list": None, "ne_name_to_iso_map": {},
        "admin1_data": None, "cities_df": None
    }
    try:
        # 1. Load Shapefile (includes ISO_A2 column now)
        world_gdf, ne_country_list = load_world_shapefile()
        if world_gdf is None or ne_country_list is None:
            logging.error("load_world_shapefile failed. Cannot proceed.")
            return None

        geo_data_dict["world_gdf"] = world_gdf
        geo_data_dict["ne_country_list"] = ne_country_list

        # 2. Load valid ISO codes from GeoNames
        valid_geonames_iso_codes = load_geonames_iso_codes()
        if not valid_geonames_iso_codes:
            logging.warning("Failed to load valid ISO codes from GeoNames countryInfo.txt. ISO mapping might be incomplete.")

        # 3. Create NE Name -> ISO Code map from Shapefile Data
        ne_name_to_iso_map = {}
        unvalidated_iso_codes = []
        if 'ISO_A2' in world_gdf.columns:
            ne_name_to_iso_map = dict(zip(world_gdf['NE_COUNTRY_NAME'], world_gdf['ISO_A2']))
            logging.info(f"Created initial Name -> ISO map with {len(ne_name_to_iso_map)} entries from shapefile.")

            for ne_name, iso_code in ne_name_to_iso_map.items():
                if iso_code not in valid_geonames_iso_codes and iso_code != '-99':
                    unvalidated_iso_codes.append(f"{ne_name} ({iso_code})")
            if unvalidated_iso_codes:
                logging.warning(f"Shapefile ISO codes not found in GeoNames countryInfo.txt for: {unvalidated_iso_codes[:10]}")
        else:
            logging.error("ISO_A2 column not found in loaded world_gdf. Cannot create Name -> ISO map.")
            st.error("Application Error: ISO_A2 code column missing from shapefile, cannot proceed with filtering.")
            return None

        geo_data_dict["ne_name_to_iso_map"] = ne_name_to_iso_map

        # 4. Load Admin1 and City data
        geo_data_dict["admin1_data"] = load_admin1_data()
        geo_data_dict["cities_df"] = load_geonames_cities()

        return geo_data_dict

    except Exception as e:
        st.error(f"An unexpected error occurred during initial data loading: {e}")
        logging.error("Unexpected error in load_initial_data sequence", exc_info=True)
        return None

# --- Main App Logic ---
st.title("🌍 USGS Earthquake Data Visualizer")
st.markdown("Filter earthquake data dynamically by Country, State/Province, or City.")
st.markdown("---")

# Load data *after* setting page config
geo_data = load_initial_data()

# --- Explicit Check for None returned by load_initial_data ---
if geo_data is None:
    st.error("Application initialization failed: Could not load essential geographic data. Please check logs and file paths.")
    logging.error("load_initial_data returned None. Stopping application.")
    st.stop()

# --- Safely Check Essential Components *within* the geo_data dictionary ---
logging.info(f"Checking loaded geo_data dictionary. Type: {type(geo_data)}")
world_gdf_value = geo_data.get("world_gdf")
country_list_value = geo_data.get("ne_country_list")

if world_gdf_value is None:
    st.error("Application initialization failed: 'world_gdf' is None within geo_data.")
    logging.error("'world_gdf' value is None in geo_data. Stopping.")
    st.stop()

if country_list_value is None:
    st.error("Application initialization failed: 'ne_country_list' is None within geo_data.")
    logging.error("'ne_country_list' value is None in geo_data. Stopping.")
    st.stop()

logging.info("Essential geo_data components ('world_gdf', 'ne_country_list') checks passed.")

# Display controls and get user inputs - Pass necessary loaded data to controls
user_inputs = controls.display_sidebar_controls(geo_data) # Pass geo_data dict

# --- Optional: Display Debug Info ---
# with st.expander("Debug: User Inputs"):
#    st.json(user_inputs)
# with st.expander("Debug: GeoData"):
#    st.write(f"Loaded Countries: {len(geo_data.get('ne_country_list', []))}")
#    st.write(f"ISO Map size: {len(geo_data.get('ne_name_to_iso_map', {}))}")
#    st.write(f"Admin1 Data Keys: {list(geo_data.get('admin1_data', {}).keys())[:5]}") # Show first 5 country codes
#    st.write(f"Cities DF Info:")
#    if geo_data.get("cities_df") is not None:
#         st.dataframe(geo_data["cities_df"].head())


# Caching wrapper function for API calls
@st.cache_data(ttl=900, show_spinner=False)
def cached_api_call(**params):
    # Ensure mutable types like lists are converted if needed for hashing
    if 'bounding_box' in params and isinstance(params['bounding_box'], list):
        params['bounding_box'] = tuple(params['bounding_box']) # Convert list to tuple
    logging.info(f"CACHE CHECK/MISS: Calling USGS API with params: {params}")
    data = usgs_api.fetch_earthquake_data(**params)
    return data

st.subheader("📊 Visualization & Data")

fetch_button_pressed = st.sidebar.button(
    "Fetch and Visualize Data",
    key="fetch_button",
    help="Click to load data based on current filters"
)

if fetch_button_pressed:
    # Retrieve necessary inputs
    country_name = user_inputs.get("country_name")
    state_name = user_inputs.get("state_name")
    city_name = user_inputs.get("city_name")
    radius_km = user_inputs.get("radius_km")
    country_iso_code = user_inputs.get("country_iso_code")
    admin1_code = user_inputs.get("admin1_code")

    api_params = {
        "starttime": user_inputs["starttime"], "endtime": user_inputs["endtime"],
        "min_magnitude": user_inputs["min_magnitude"], "limit": user_inputs["limit"],
    }
    map_center_bounds = None
    fetch_location_description = "selected filters"
    execute_fetch = False
    selected_level = user_inputs["selected_level"]

    if selected_level == "City" and city_name and country_iso_code and admin1_code and radius_km:
        fetch_location_description = f"city: {city_name}"
        coords = get_city_coordinates(country_iso_code, admin1_code, city_name, geo_data["cities_df"])
        if coords:
            api_params["latitude"], api_params["longitude"] = coords
            api_params["max_radius_km"] = radius_km
            map_center_bounds = [coords[1] - 1, coords[0] - 1, coords[1] + 1, coords[0] + 1]
            execute_fetch = True
        else:
            st.error(f"Could not find coordinates for city: {city_name}")

    elif selected_level in ["State", "Country"] and country_name:
        fetch_location_description = f"country: {country_name}"
        if selected_level == "State":
            fetch_location_description = f"state: {state_name}, {country_name} (using country bounds)"
        with st.spinner(f"Looking up boundaries for {country_name}..."):
            bounds = get_country_bounds(country_name, geo_data["world_gdf"])
        if bounds:
            api_params["bounding_box"] = bounds
            map_center_bounds = bounds
            execute_fetch = True
        else:
            st.error(f"Could not determine boundaries for country: {country_name}")

    elif selected_level == "Global":
        fetch_location_description = "global"
        execute_fetch = True
    else:
        st.warning("Please select a geographic filter or run a global search.")

    # Execute API Call and Display Results
    if execute_fetch:
        geojson_data = None
        try:
            with st.spinner(f"📡 Fetching data for {fetch_location_description}..."):
                geojson_data = cached_api_call(**api_params)
        except Exception as e:
            st.error(f"An error occurred during data fetching: {e}")
            logging.error(f"Error calling cached_api_call: {e}", exc_info=True)

        # Process results (rest of the logic remains largely the same as before)
        if geojson_data and 'features' in geojson_data:
            num_events = len(geojson_data['features'])
            if num_events > 0:
                st.success(f"✅ Found {num_events} earthquake events matching {fetch_location_description}.")
                # Generate and display map
                with st.spinner(f"🗺️ Generating map for {num_events} events..."):
                   # Map builder might need updating if it relied on global data previously
                    earthquake_map = map_builder.create_earthquake_map(
                        geojson_data,
                        center_on_bounds=map_center_bounds
                    )
                if earthquake_map:
                    st.info("Displaying Interactive Map:")
                    map_html = earthquake_map._repr_html_()
                    components.html(map_html, height=600, scrolling=False)
                else:
                    st.error("❌ Failed to generate map.")

                st.markdown("---")
                st.subheader("📄 Data Table")
                # Generate and display data table
                with st.spinner("Preparing data table..."):
                    df = data_handler.geojson_to_dataframe(geojson_data)

                if df is not None and not df.empty:
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f'earthquake_data_{user_inputs.get("country_name") or "global"}.csv',
                        mime='text/csv'
                    )
                elif df is not None:
                     st.info("The API returned data, but it resulted in an empty table after processing.")
                else:
                    st.warning("Could not process fetched data into a table.")

            else: # Zero events found
                st.warning(f"⚠️ No earthquake events found matching your criteria for {fetch_location_description}.")
                st.info("Displaying map of the selected area:")
                with st.spinner("Generating empty map..."):
                    empty_map = map_builder.create_earthquake_map(
                        {"type": "FeatureCollection", "features": []},
                        center_on_bounds=map_center_bounds
                    )
                if empty_map:
                    map_html = empty_map._repr_html_()
                    components.html(map_html, height=500, scrolling=False)
                st.subheader("📄 Data Table")
                st.dataframe(pd.DataFrame(columns=[
                    'Magnitude', 'Place', 'Time', 'Depth (km)', 'Latitude', 'Longitude', 'Details URL', 'USGS ID'
                ]), use_container_width=True)

        else: # Failed to fetch data
            st.error(f"❌ Failed to fetch or process data from the USGS API for {fetch_location_description}.")

else:
    st.info("Configure filters in the sidebar and click 'Fetch and Visualize Data' to load earthquake information.")
    st.markdown("---")