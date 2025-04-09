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

# --- Load Data Function ---
# Use caching here if desired, or rely on caching within the load functions themselves
# @st.cache_resource # Cache the entire loaded data dictionary
def load_initial_data():
    """Loads all necessary geographic data after page config."""
    world_gdf, ne_country_list = load_world_shapefile()
    ne_name_to_iso_map = load_country_name_to_iso_mapping(world_gdf) # Pass world_gdf if needed for normalization
    admin1_data = load_admin1_data()
    cities_df = load_geonames_cities()
    return {
        "world_gdf": world_gdf,
        "ne_country_list": ne_country_list,
        "ne_name_to_iso_map": ne_name_to_iso_map,
        "admin1_data": admin1_data,
        "cities_df": cities_df
    }

# --- Main App Logic ---
st.title("🌍 USGS Earthquake Data Visualizer")
st.markdown("Filter earthquake data dynamically by Country, State/Province, or City.")
st.markdown("---")

# Load data *after* setting page config
geo_data = load_initial_data()

# Check if essential data loaded correctly
if geo_data["world_gdf"] is None or geo_data["ne_country_list"] is None:
    st.error("Application cannot start: Failed to load world boundaries data.")
    st.stop() # Stop execution if core data is missing

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
    api_params = {
        "starttime": user_inputs["starttime"],
        "endtime": user_inputs["endtime"],
        "min_magnitude": user_inputs["min_magnitude"],
        "limit": user_inputs["limit"],
    }
    map_center_bounds = None # For centering map view
    fetch_location_description = "selected filters" # Default description
    execute_fetch = False

    selected_level = user_inputs["selected_level"]

    # Determine API parameters based on the selected geographic level
    if selected_level == "City" and user_inputs["city_name"] and user_inputs["radius_km"]:
        fetch_location_description = f"city: {user_inputs['city_name']}"
        # Pass the loaded cities_df to the lookup function
        coords = get_city_coordinates(
            user_inputs["country_iso_code"],
            user_inputs["admin1_code"],
            user_inputs["city_name"],
            geo_data["cities_df"] # Pass loaded data
        )
        if coords:
            api_params["latitude"] = coords[0]
            api_params["longitude"] = coords[1]
            api_params["max_radius_km"] = user_inputs["radius_km"]
            map_center_bounds = [coords[1] - 1, coords[0] - 1, coords[1] + 1, coords[0] + 1]
            execute_fetch = True
            logging.info(f"API Filter: City Radius Search ({fetch_location_description})")
        else:
            st.error(f"Could not find coordinates for city: {user_inputs['city_name']}")

    elif selected_level in ["State", "Country"] and user_inputs["country_name"]:
        fetch_location_description = f"country: {user_inputs['country_name']}"
        if selected_level == "State":
             fetch_location_description = f"state: {user_inputs['state_name']}, {user_inputs['country_name']} (using country bounds)"
             logging.info(f"API Filter: State selected, using Country Bounding Box for API call.")

        with st.spinner(f"Looking up boundaries for {user_inputs['country_name']}..."):
             # Pass the loaded world_gdf to the lookup function
            bounds = get_country_bounds(user_inputs['country_name'], geo_data["world_gdf"]) # Pass loaded data
        if bounds:
            api_params["bounding_box"] = bounds
            map_center_bounds = bounds
            execute_fetch = True
            logging.info(f"API Filter: Bounding Box Search ({fetch_location_description})")
        else:
            st.error(f"Could not determine boundaries for country: {user_inputs['country_name']}")

    elif selected_level == "Global":
         fetch_location_description = "global"
         st.info("No specific geographic filter selected. Fetching global data based on other filters.")
         execute_fetch = True
         logging.info(f"API Filter: Global Search")

    else:
         st.warning("Please select a geographic filter (at least Country) or run a global search.")


    # --- Execute API Call and Display Results ---
    if execute_fetch:
        geojson_data = None
        try:
            with st.spinner(f"📡 Checking cache or fetching data for {fetch_location_description}..."):
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