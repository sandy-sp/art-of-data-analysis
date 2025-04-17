import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
from src.utils.tectonic_loader import load_tectonic_boundaries

def display_interactive_map(eq_df: pd.DataFrame, weather_df: pd.DataFrame, lat: float, lon: float):
    """
    Display earthquakes, weather, and tectonic boundaries on a Folium map with interactivity.
    """
    m = folium.Map(location=[lat, lon], zoom_start=6, control_scale=True)

    # Earthquake markers with clustering
    if not eq_df.empty:
        eq_cluster = MarkerCluster(name="📍 Earthquakes").add_to(m)
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

    # Weather location marker
    if not weather_df.empty:
        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color='blue', icon='cloud'),
            popup="Weather Data Location"
        ).add_to(m)

    # Tectonic plate boundaries with tooltip and popup
    if st.session_state.get("show_tectonics", False):
        tectonics = load_tectonic_boundaries()
        if tectonics is not None and not tectonics.empty:
            try:
                if "Name" not in tectonics.columns:
                    tectonics["Name"] = tectonics.index.astype(str)

                folium.GeoJson(
                    tectonics.__geo_interface__,
                    name="🌋 Tectonic Boundaries",
                    style_function=lambda x: {
                        "color": "orange",
                        "weight": 2,
                        "opacity": 0.8
                    },
                    tooltip=folium.GeoJsonTooltip(fields=["Name"], aliases=["Boundary ID"]),
                    popup=folium.GeoJsonPopup(fields=["Name"], labels=True)
                ).add_to(m)
            except Exception as geojson_err:
                st.warning(f"⚠️ Failed to render tectonic boundaries: {geojson_err}")
        else:
            st.warning("⚠️ Tectonic boundary data is empty or invalid.")

    folium.LayerControl(collapsed=True).add_to(m)
    output = st_folium(m, width=1000, height=600)

    if output.get("last_clicked"):
        st.session_state["map_last_clicked"] = output["last_clicked"]
        st.toast(f"🗺️ Clicked at: {output['last_clicked']}")
