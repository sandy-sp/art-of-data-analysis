import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import requests
import json

TECTONIC_URL = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"

# Simple static mapping for demo (extend as needed)
COUNTRY_CENTERS = {
    "United States": (37.0902, -95.7129, 4),
    "Japan": (36.2048, 138.2529, 5),
    "Chile": (-35.6751, -71.5430, 5),
    "Turkey": (38.9637, 35.2433, 5),
    "Indonesia": (-0.7893, 113.9213, 4),
    "India": (20.5937, 78.9629, 4),
    "Mexico": (23.6345, -102.5528, 5),
    "Philippines": (13.4105, 122.5607, 5),
}


def render_region_selector():
    st.sidebar.subheader("🌍 Select Region via Tectonic Plates")

    country = st.sidebar.selectbox("Select Country", list(COUNTRY_CENTERS.keys()))
    lat, lon, zoom = COUNTRY_CENTERS.get(country, (10, 0, 2))

    st.sidebar.markdown("Click a plate boundary below to populate coordinates.")

    # Define a map centered on selected country
    m = folium.Map(location=[lat, lon], zoom_start=zoom, control_scale=True)

    try:
        res = requests.get(TECTONIC_URL)
        res.raise_for_status()
        data = res.json()

        folium.GeoJson(
            data,
            name="Tectonic Plate Boundaries",
            tooltip=folium.GeoJsonTooltip(fields=[]),
            highlight_function=lambda x: {"fillColor": "orange", "color": "red"},
            popup=folium.GeoJsonPopup(fields=[], labels=False)
        ).add_to(m)

        m.add_child(folium.LatLngPopup())

    except Exception as e:
        st.sidebar.error(f"Failed to load tectonic data: {e}")

    # Render map and capture click
    output = st_folium(m, width=700, height=450)
    clicked = output.get("last_clicked")

    if clicked:
        st.session_state["latitude"] = clicked["lat"]
        st.session_state["longitude"] = clicked["lng"]
        st.success(f"Selected Coordinates: ({clicked['lat']:.4f}, {clicked['lng']:.4f})")
