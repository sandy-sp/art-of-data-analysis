import geopandas as gpd
import streamlit as st
import os

TECTONIC_FILE = "data/plate-boundaries2.json"  # rename to .geojson for clarity if needed

@st.cache_data(show_spinner=False)
def load_tectonic_boundaries():
    """
    Load tectonic plate boundaries as a GeoDataFrame.
    """
    if not os.path.exists(TECTONIC_FILE):
        st.error(f"Tectonic boundary file not found: {TECTONIC_FILE}")
        return None

    try:
        gdf = gpd.read_file(TECTONIC_FILE)
        return gdf
    except Exception as e:
        st.error(f"Error loading tectonic boundary GeoJSON: {e}")
        return None
