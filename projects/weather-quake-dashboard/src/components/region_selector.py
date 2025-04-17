import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import pycountry
from datetime import datetime, timedelta
from src.api.usgs_earthquake_api import fetch_earthquake_data
import pandas as pd
import plotly.express as px

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

        # --- Fetch Quake History (last 5 years) ---
        history_start = (datetime.now() - timedelta(days=5*365)).date()
        history_end = datetime.now().date()

        with st.spinner("📡 Scanning earthquake history..."):
            preview_df = fetch_earthquake_data(
                str(history_start), str(history_end),
                min_magnitude=3.5,
                latitude=latitude,
                longitude=longitude,
                max_radius_km=500  # generous for preview
            )

        # --- Summarize Available Dates ---
        if not preview_df.empty:
            preview_df['Time'] = pd.to_datetime(preview_df['Time'])
            preview_df['Year-Month'] = preview_df['Time'].dt.to_period('M').astype(str)
            monthly_summary = preview_df.groupby('Year-Month').size().reset_index(name='Quake Count')

            st.markdown("### 📅 Earthquake History (Last 5 Years)")
            st.dataframe(monthly_summary, use_container_width=True, hide_index=True)

            # --- Historical Trend Chart ---
            with st.expander("📈 View Earthquake Frequency Trend", expanded=False):
                fig = px.bar(
                    monthly_summary,
                    x="Year-Month",
                    y="Quake Count",
                    title="🧨 Earthquakes per Month (Past 5 Years)",
                    labels={"Year-Month": "Month", "Quake Count": "Number of Events"}
                )
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

            # --- Optional: Preview Map of Quakes ---
            with st.expander("🗺️ View Historical Quake Locations"):
                locations = preview_df[["Latitude", "Longitude"]].dropna().values.tolist()
                preview_map = folium.Map(control_scale=True)

                # Add quake markers
                for loc in locations:
                    folium.CircleMarker(
                        location=loc,
                        radius=2,
                        color="red",
                        fill=True,
                        fill_opacity=0.5
                    ).add_to(preview_map)

                # Fit map to bounds
                if locations:
                    preview_map.fit_bounds(locations)
                else:
                    preview_map.location = [latitude, longitude]
                    preview_map.zoom_start = 4

                st_folium(preview_map, width=700, height=400)
        else:
            st.warning("⚠️ No earthquakes found in this region over the past 5 years.")

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

