import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import pycountry
import geopandas as gpd
from shapely.geometry import shape

TECTONIC_URL = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"

@st.cache_data(show_spinner=False)
def get_country_list():
    return sorted([c.name for c in pycountry.countries])

@st.cache_data(show_spinner=False)
def load_tectonic_geojson():
    res = requests.get(TECTONIC_URL)
    res.raise_for_status()
    return gpd.GeoDataFrame.from_features(res.json()["features"], crs="EPSG:4326")

def geocode_country_center(name: str):
    try:
        geolocator = Nominatim(user_agent="quake-weather-app")
        location = geolocator.geocode(name, exactly_one=True, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        st.sidebar.error(f"Geocoding failed: {e}")
    return 10, 0  # fallback to equator

def render_region_selector():
    st.sidebar.subheader("🌍 Select Region via Tectonic Plates")

    country_list = get_country_list()
    country = st.sidebar.selectbox("Select Country", country_list, index=country_list.index("Japan"))
    lat, lon = geocode_country_center(country)

    st.sidebar.markdown("Click on the map or choose a boundary near your country.")

    # Load tectonic plate data
    tectonics = load_tectonic_geojson()

    # Filter by distance to country center
    nearby_coords = []
    for idx, row in tectonics.iterrows():
        center = shape(row["geometry"]).centroid
        dist_km = geodesic((lat, lon), (center.y, center.x)).km
        if dist_km <= 1000:
            nearby_coords.append((f"Segment #{idx} at ({center.y:.2f}, {center.x:.2f})", center.y, center.x))

    if nearby_coords:
        selected = st.sidebar.selectbox(
            "Tectonic Boundary Nearby (within 1000km)",
            [label for label, _, _ in nearby_coords]
        )
        for label, y, x in nearby_coords:
            if label == selected:
                st.session_state["latitude"] = y
                st.session_state["longitude"] = x
                st.success(f"Selected from list: ({y:.4f}, {x:.4f})")
                break

    # Draw map
    m = folium.Map(location=[lat, lon], zoom_start=5, control_scale=True)
    folium.GeoJson(
        tectonics.__geo_interface__,
        name="Tectonic Boundaries",
        tooltip=folium.GeoJsonTooltip(fields=[]),
        highlight_function=lambda x: {"fillColor": "orange", "color": "red"},
        popup=folium.GeoJsonPopup(fields=[], labels=False)
    ).add_to(m)
    m.add_child(folium.LatLngPopup())

    output = st_folium(m, width=700, height=450)
    clicked = output.get("last_clicked")

    if clicked:
        st.session_state["latitude"] = clicked["lat"]
        st.session_state["longitude"] = clicked["lng"]
        st.success(f"Selected from map: ({clicked['lat']:.4f}, {clicked['lng']:.4f})")
