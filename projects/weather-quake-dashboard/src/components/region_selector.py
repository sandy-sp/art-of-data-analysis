import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import requests
import json

TECTONIC_URL = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"

def geocode_country_center(name: str):
    try:
        geolocator = Nominatim(user_agent="quake-weather-app")
        location = geolocator.geocode(name, exactly_one=True, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        st.sidebar.error(f"Geocoding failed: {e}")
    return 10, 0  # fallback to global center

def render_region_selector():
    st.sidebar.subheader("🌍 Select Region via Tectonic Plates")

    country = st.sidebar.text_input("Enter Country Name", "Japan")
    lat, lon = geocode_country_center(country)

    st.sidebar.markdown("Click a plate boundary below to populate coordinates.")

    # Define a map centered on selected country
    m = folium.Map(location=[lat, lon], zoom_start=5, control_scale=True)

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
