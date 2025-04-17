import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import pycountry

@st.cache_data(show_spinner=False)
def get_country_list():
    return sorted([country.name for country in pycountry.countries])

@st.cache_data(show_spinner=False)
def geocode_country(country_name):
    geolocator = Nominatim(user_agent="quake-weather-app")
    location = geolocator.geocode(country_name, exactly_one=True, timeout=10)
    return (location.latitude, location.longitude) if location else (0, 0)

def render_region_selector():
    st.subheader("🌍 Select Region")

    col1, col2 = st.columns([1, 2])

    with col1:
        country_list = get_country_list()
        selected_country = st.selectbox("🌎 Select Country", country_list, index=country_list.index("Japan"))
        latitude, longitude = geocode_country(selected_country)
        
        # Store selected coordinates in session state
        st.session_state["latitude"] = latitude
        st.session_state["longitude"] = longitude

        st.write(f"📍 Selected: {selected_country} ({latitude:.2f}, {longitude:.2f})")

    with col2:
        st.markdown("🗺️ **Refine location by clicking on the map:**")
        m = folium.Map(location=[latitude, longitude], zoom_start=5, control_scale=True)
        folium.Marker([latitude, longitude], tooltip="Selected Country Center", icon=folium.Icon(color="blue")).add_to(m)

        # Allow users to click map to refine coordinates
        m.add_child(folium.LatLngPopup())

        output = st_folium(m, width=700, height=400)

        # Update coordinates if clicked
        if output.get("last_clicked"):
            clicked_lat = output["last_clicked"]["lat"]
            clicked_lon = output["last_clicked"]["lng"]
            st.session_state["latitude"] = clicked_lat
            st.session_state["longitude"] = clicked_lon
            st.success(f"📌 Refined Coordinates: ({clicked_lat:.4f}, {clicked_lon:.4f})")

