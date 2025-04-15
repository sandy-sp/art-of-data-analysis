import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
from src.utils.tectonic_loader import load_tectonic_boundaries

def display_interactive_map(eq_df: pd.DataFrame, weather_df: pd.DataFrame, lat: float, lon: float):
    """
    Display earthquakes and optionally weather station data on a Folium map.
    """
    m = folium.Map(location=[lat, lon], zoom_start=6, control_scale=True)

    # Earthquake Markers
    if not eq_df.empty:
        eq_cluster = MarkerCluster(name="Earthquakes").add_to(m)
        for _, row in eq_df.iterrows():
            popup = f"<b>{row['Place']}</b><br>Mag: {row['Magnitude']}<br>Depth: {row['Depth_km']} km"
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=row['Magnitude'] * 2,
                color='red',
                fill=True,
                fill_opacity=0.6,
                popup=popup
            ).add_to(eq_cluster)

    # Weather Marker
    if not weather_df.empty:
        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color='blue', icon='cloud'),
            popup="Weather Data Location"
        ).add_to(m)

    # Tectonic Plate Boundaries
    if st.session_state.get("show_tectonics", False):
        tectonics = load_tectonic_boundaries()
        if tectonics is not None and not tectonics.empty:
            folium.GeoJson(
                tectonics.__geo_interface__,
                name="Tectonic Boundaries",
                style_function=lambda x: {"color": "orange", "weight": 2, "opacity": 0.7},
            ).add_to(m)
        else:
            st.warning("⚠️ Could not render tectonic boundaries.")

    folium.LayerControl().add_to(m)
    st_folium(m, width=900, height=550)
