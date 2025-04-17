import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

def display_map(weather_df, quake_df, latitude, longitude):
    st.subheader("🗺️ Interactive Weather & Earthquake Map")

    # Initialize Map
    m = folium.Map(location=[latitude, longitude], zoom_start=6, control_scale=True)

    # Earthquake markers
    quake_cluster = MarkerCluster(name='Earthquakes').add_to(m)
    for _, quake in quake_df.iterrows():
        folium.CircleMarker(
            location=[quake["Latitude"], quake["Longitude"]],
            radius=quake["Magnitude"] * 2,
            color="red",
            fill=True,
            fill_opacity=0.6,
            popup=f"📍{quake['Place']}<br>Magnitude: {quake['Magnitude']}<br>Depth: {quake['Depth_km']} km"
        ).add_to(quake_cluster)

    # Weather data marker (single location)
    if not weather_df.empty:
        folium.Marker(
            location=[latitude, longitude],
            icon=folium.Icon(color="blue", icon="cloud"),
            popup="🌤️ Weather Station"
        ).add_to(m)

    # Render map
    st_folium(m, width=900, height=500)
