import streamlit as st
import logging
import json
import pandas as pd

# Local application imports
from app.ui import controls
from app.core import usgs_api
from app.core import geo_utils  # Keep this import
from app.visualizations import map_builder
from app.core import data_handler
from app.visualizations import chart_builder

import streamlit.components.v1 as components

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(page_title="Earthquake Visualizer", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
st.title("🌍 USGS Earthquake Data Visualizer")
st.markdown("Enter a country name to explore earthquake data within its boundaries for a time range.")
st.markdown("---")

# Load shapefile and country list - *** REMOVE THE ARGUMENT ***
with st.spinner("Loading world boundaries map and country list..."):
    # world_gdf, country_list = geo_utils.load_world_shapefile(SHAPEFILE_PATH)  # OLD WAY
    world_gdf, country_list = geo_utils.load_world_shapefile()  # NEW WAY (No argument)

if world_gdf is None or country_list is None:
    st.error("Application cannot start because the world boundaries data failed to load. Please check the path and file integrity.")
    st.stop()

# Sidebar controls
user_inputs = controls.display_sidebar_controls(country_list)

@st.cache_data(ttl=900, show_spinner=False)
def cached_api_call(**params):
    logging.info(f"CACHE MISS: Calling USGS API with params: {params}")
    if 'bounding_box' in params and isinstance(params['bounding_box'], list):
        params['bounding_box'] = tuple(params['bounding_box'])
    data = usgs_api.fetch_earthquake_data(**params)
    return data

st.subheader("📊 Earthquake Data Visualizations")

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

    if not country_name:
        st.error("Please select a country from the dropdown list in the sidebar.")
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

    if execute_fetch:
        with st.spinner(f"📡 Checking cache or fetching data for '{country_name}'..."):
            geojson_data = cached_api_call(**api_params)

        if geojson_data and 'features' in geojson_data and len(geojson_data['features']) > 0:
            num_events = len(geojson_data['features'])
            st.success(f"✅ Found {num_events} earthquake events for '{country_name}'.")

            with st.spinner(f"🗺️ Generating map for {num_events} events..."):
                earthquake_map = map_builder.create_earthquake_map(geojson_data, center_on_bounds=bounding_box)
            if earthquake_map:
                st.info("Displaying Interactive Map:")
                map_html = earthquake_map._repr_html_()
                components.html(map_html, height=600, scrolling=False)
            else:
                st.error("❌ Failed to generate map.")

            st.markdown("---")

            with st.spinner("Preparing data table..."):
                df = data_handler.geojson_to_dataframe(geojson_data)

            # ---- NEW 2x2 CHART TILE LAYOUT ----
            st.subheader("📽️ Summary Charts")

            with st.spinner("Rendering animations..."):
                mag_path = chart_builder.create_magnitude_histogram_animation(df)
                depth_path = chart_builder.create_depth_histogram_animation(df)
                ts_path = chart_builder.create_time_series_animation(df)
                loa_ani = chart_builder.create_location_animation(df)

            col1, col2 = st.columns(2)
            with col1:
                st.image(mag_path, caption="Magnitude Histogram")
            with col2:
                st.image(depth_path, caption="Depth Histogram")

            col3, col4 = st.columns(2)
            with col3:
                st.image(ts_path, caption="Earthquakes Over Time")
            with col4:
                st.image(loa_ani, caption="Location Animation")

            st.markdown("---")
            st.subheader("🎞️ Advanced Visualizations")

            tabs = st.tabs([
                "Cumulative Timeline",
                "Magnitude vs Depth",
                "Map: Quake Spread",
                "Shockwave Ripples",
                "Spiral Timeline",
                "Depth Strip Timeline"
            ])

            with tabs[0]:
                st.markdown(f"**Cumulative Earthquakes Over Time in {country_name}**")
                gif_path = chart_builder.create_cumulative_time_series(df)
                if gif_path: st.image(gif_path)

            with tabs[1]:
                st.markdown(f"**Magnitude vs. Depth for Earthquakes in {country_name}**")
                gif_path = chart_builder.create_magnitude_depth_scatter(df)
                if gif_path: st.image(gif_path)

            with tabs[2]:
                st.markdown(f"**Earthquake Spread Across {country_name}**")
                gif_path = chart_builder.create_location_scatter_animation(df)
                if gif_path: st.image(gif_path)

            with tabs[3]:
                st.markdown(f"**Seismic Shockwave Ripples in {country_name}**")
                gif_path = chart_builder.create_shockwave_map_animation(df)
                if gif_path: st.image(gif_path)

            with tabs[4]:
                st.markdown(f"**Spiral Timeline of Quakes in {country_name}**")
                gif_path = chart_builder.create_spiral_timeline(df)
                if gif_path: st.image(gif_path)

            with tabs[5]:
                st.markdown(f"**Depth Layered Timeline of Earthquakes in {country_name}**")
                gif_path = chart_builder.create_depth_strip_chart_animation(df)
                if gif_path: st.image(gif_path)

            # ---- FINAL: DATA TABLE + DOWNLOAD ----
            st.markdown("---")
            st.subheader("📄 Earthquake Data Table")

            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f'earthquake_data_{country_name}.csv',
                    mime='text/csv'
                )
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
    st.info("Select a country in the sidebar and click 'Fetch and Visualize Data' to load earthquake information.")
    st.markdown("---")

with st.sidebar:
    st.markdown("<div style='height: 100%; display: flex; flex-direction: column; justify-content: flex-end;'>", unsafe_allow_html=True)
    st.markdown("""
    <p style='margin-top: 10px; font-size: 16px;'>
        📘 Curious how this project works under the hood? <a href='https://github.com/sandy-sp/art-of-data-analysis/tree/main/projects/earthquake_viz/README.md' target='_blank'>Check out the GitHub README</a> for code, setup, and deployment tips.
    </p>
    <p style='margin-top: 20px; font-size: 16px;'>
        💡 Enjoying this project? Interested in building similar data apps or collaborating on earthquakes and visualization tools?
        Let’s connect and share ideas!
    </p>
    <style>
    .social-icons a {
        text-decoration: none;
        font-size: 20px;
        display: inline-flex;
        align-items: center;
        margin-right: 10px;
        margin-bottom: 6px;
    }
    .social-icons a:hover {
        text-decoration: underline;
    }
    </style>
    <div class='social-icons'>
        <a href="https://www.linkedin.com/in/sandeep-paidipati" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" width="24" style="margin-right:8px; vertical-align:middle;" /> LinkedIn
        </a><br>
        <a href="https://github.com/sandy-sp" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" width="24" style="margin-right:8px; vertical-align:middle;" /> GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)