import streamlit as st
import logging
import pandas as pd

# Local application imports
from app.ui import controls # Use the refactored controls
from app.core import usgs_api
# Import specific functions/data needed from geo_utils
from app.core.geo_utils import WORLD_GDF, get_country_bounds, get_city_coordinates
from app.visualizations import map_builder
from app.core import data_handler

# Import Streamlit components
import streamlit.components.v1 as components

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Page configuration
st.set_page_config(page_title="Earthquake Visualizer", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

st.title("🌍 USGS Earthquake Data Visualizer")
st.markdown("Filter earthquake data dynamically by Country, State/Province, or City.")
st.markdown("---")

# Check if essential data loaded correctly (WORLD_GDF is loaded inside geo_utils)
if WORLD_GDF is None:
    st.error("Application cannot start: Failed to load world boundaries data.")
    st.stop() # Stop execution if core data is missing

# Display controls and get user inputs
user_inputs = controls.display_sidebar_controls()

# --- Optional: Display Debug Info ---
# with st.expander("Debug: User Inputs"):
#    st.json(user_inputs)

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
        coords = get_city_coordinates(
            user_inputs["country_iso_code"],
            user_inputs["admin1_code"],
            user_inputs["city_name"]
        )
        if coords:
            api_params["latitude"] = coords[0]
            api_params["longitude"] = coords[1]
            api_params["max_radius_km"] = user_inputs["radius_km"]
            # Define a reasonable area around the city for map centering
            map_center_bounds = [coords[1] - 1, coords[0] - 1, coords[1] + 1, coords[0] + 1] # Small box around city
            execute_fetch = True
            logging.info(f"API Filter: City Radius Search ({fetch_location_description})")
        else:
            st.error(f"Could not find coordinates for city: {user_inputs['city_name']}")

    elif selected_level in ["State", "Country"] and user_inputs["country_name"]:
         # For State level, we currently fall back to Country bounding box
         # A future enhancement could involve getting state geometry and doing post-filtering
        fetch_location_description = f"country: {user_inputs['country_name']}"
        if selected_level == "State":
             fetch_location_description = f"state: {user_inputs['state_name']}, {user_inputs['country_name']} (using country bounds)"
             logging.info(f"API Filter: State selected, using Country Bounding Box for API call.")

        with st.spinner(f"Looking up boundaries for {user_inputs['country_name']}..."):
            bounds = get_country_bounds(user_inputs['country_name'], WORLD_GDF)
        if bounds:
            api_params["bounding_box"] = bounds
            map_center_bounds = bounds # Center map on country bounds
            execute_fetch = True
            logging.info(f"API Filter: Bounding Box Search ({fetch_location_description})")
        else:
            st.error(f"Could not determine boundaries for country: {user_inputs['country_name']}")

    elif selected_level == "Global":
         # No geographic filter applied (or country not selected)
         fetch_location_description = "global"
         st.info("No specific geographic filter selected. Fetching global data based on other filters.")
         execute_fetch = True
         logging.info(f"API Filter: Global Search")
         # map_center_bounds remains None, Folium will default

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

        # Process results
        if geojson_data and 'features' in geojson_data:
            num_events = len(geojson_data['features'])
            if num_events > 0:
                st.success(f"✅ Found {num_events} earthquake events matching {fetch_location_description}.")

                # Generate and display map
                with st.spinner(f"🗺️ Generating map for {num_events} events..."):
                    earthquake_map = map_builder.create_earthquake_map(
                        geojson_data,
                        center_on_bounds=map_center_bounds # Pass bounds for centering
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
                    # Add download button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f'earthquake_data_{user_inputs["country_name"] or "global"}.csv',
                        mime='text/csv'
                    )
                elif df is not None: # Empty dataframe case
                     st.info("The API returned data, but it resulted in an empty table after processing.")
                else: # df is None
                    st.warning("Could not process fetched data into a table.")

            else: # Zero events found
                st.warning(f"⚠️ No earthquake events found matching your criteria for {fetch_location_description}.")
                st.info("Displaying map of the selected area:")
                # Display empty map centered on the area if possible
                with st.spinner("Generating empty map..."):
                    empty_map = map_builder.create_earthquake_map(
                        {"type": "FeatureCollection", "features": []}, # Empty GeoJSON
                        center_on_bounds=map_center_bounds
                    )
                if empty_map:
                    map_html = empty_map._repr_html_()
                    components.html(map_html, height=500, scrolling=False)
                st.subheader("📄 Data Table")
                st.dataframe(pd.DataFrame(columns=[ # Show empty table with correct columns
                    'Magnitude', 'Place', 'Time', 'Depth (km)', 'Latitude', 'Longitude', 'Details URL', 'USGS ID'
                ]), use_container_width=True)

        else: # Failed to fetch data (geojson_data is None or malformed)
            st.error(f"❌ Failed to fetch or process data from the USGS API for {fetch_location_description}.")

else:
    st.info("Configure filters in the sidebar and click 'Fetch and Visualize Data' to load earthquake information.")
    st.markdown("---")