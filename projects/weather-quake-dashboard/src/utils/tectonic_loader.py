import geopandas as gpd
import streamlit as st
import os

TECTONIC_FILE = "data/plate-boundaries.json"
TECTONIC_URL = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"

@st.cache_data(show_spinner=False)
def load_tectonic_boundaries():
    """
    Load tectonic plate boundaries as a GeoDataFrame.
    Tries local file first, falls back to online source if needed.
    """
    try:
        if os.path.exists(TECTONIC_FILE):
            gdf = gpd.read_file(TECTONIC_FILE)
        else:
            st.warning("Local tectonic boundary file not found. Loading from URL...")
            gdf = gpd.read_file(TECTONIC_URL)

        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)

        if not gdf.geometry.is_valid.all():
            st.warning("Some geometries in the tectonic data are invalid and may be skipped.")

        return gdf
    except Exception as e:
        st.error(f"Error loading tectonic boundaries: {e}")
        return None
