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

    st.sidebar.markdown("Click a plate centroid marker below to set coordinates.")

    # Load tectonic data
    tectonics = load_tectonic_geojson()

    # Filter and prepare nearby centroids
    nearby_centroids = []
    for idx, row in tectonics.iterrows():
        centroid = shape(row["geometry"]).centroid
        distance = geodesic((lat, lon), (centroid.y, centroid.x)).km
        if distance <= 1000:
            nearby_centroids.append((centroid.y, centroid.x, f"Segment #{idx} ({distance:.0f} km)"))

    # Draw map
    m = folium.Map(location=[lat, lon], zoom_start=5, control_scale=True)

    # Plot centroids as clickable markers
    for lat_c, lon_c, label in nearby_centroids:
        folium.Marker(
            location=[lat_c, lon_c],
            popup=label,
            icon=folium.Icon(color='green', icon='map-marker')
        ).add_to(m)

    # Add tectonic boundaries layer
    folium.GeoJson(
        tectonics.__geo_interface__,
        name="Tectonic Boundaries",
        tooltip=folium.GeoJsonTooltip(fields=[]),
        highlight_function=lambda x: {"fillColor": "orange", "color": "red"},
        popup=folium.GeoJsonPopup(fields=[], labels=False)
    ).add_to(m)

    m.add_child(folium.LatLngPopup())

    # Render map and handle user click
    output = st_folium(m, width=700, height=450)
    clicked = output.get("last_clicked")

    if clicked:
        st.session_state["latitude"] = clicked["lat"]
        st.session_state["longitude"] = clicked["lng"]
        st.success(f"Selected Coordinates: ({clicked['lat']:.4f}, {clicked['lng']:.4f})")
