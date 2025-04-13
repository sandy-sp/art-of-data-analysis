import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import requests
import json


TECTONIC_URL = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"


def render_region_selector():
    st.sidebar.subheader("🌍 Select Region via Tectonic Plates")

    country = st.sidebar.selectbox("Select Country", [
        "United States", "Japan", "Chile", "Turkey", "Indonesia", "India", "Mexico", "Philippines"
    ])

    st.sidebar.markdown("Click a plate boundary below to populate coordinates.")

    # Define a map centered roughly globally
    m = folium.Map(location=[10, 0], zoom_start=2, control_scale=True)

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

        # Optional: add simple click capture
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
