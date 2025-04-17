import geopandas as gpd
import streamlit as st
import os
import requests
from io import BytesIO

TECTONIC_FILE = "data/plate-boundaries.json"
TECTONIC_URL = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"

@st.cache_data(show_spinner=False)
def load_tectonic_boundaries():
    """
    Load tectonic plate boundaries as a GeoDataFrame.
    Priority: Local file -> Remote download -> Error fallback.
    """
    try:
        gdf = None

        # Try local file
        if os.path.exists(TECTONIC_FILE):
            gdf = gpd.read_file(TECTONIC_FILE)
            st.info("📁 Loaded tectonic boundaries from local file.")

        # Fallback to online download
        else:
            st.warning("⚠️ Local tectonic file not found. Fetching from remote URL...")
            response = requests.get(TECTONIC_URL, timeout=20)
            response.raise_for_status()
            gdf = gpd.read_file(BytesIO(response.content))

            # Save to local cache if successful
            os.makedirs(os.path.dirname(TECTONIC_FILE), exist_ok=True)
            with open(TECTONIC_FILE, 'wb') as f:
                f.write(response.content)
            st.success("✅ Remote tectonic data loaded and cached locally.")

        if gdf is None or gdf.empty:
            st.error("❌ Failed to load tectonic boundary data.")
            return None

        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)

        if not gdf.geometry.is_valid.all():
            st.warning("⚠️ Some geometries in tectonic data are invalid and may be skipped.")
            gdf = gdf[gdf.geometry.is_valid]

        return gdf

    except Exception as e:
        st.exception(f"🔥 Exception while loading tectonic boundaries: {e}")
        return None
