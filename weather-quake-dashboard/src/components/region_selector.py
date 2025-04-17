import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import pandas as pd
from src.api.usgs_earthquake_api import fetch_earthquake_data

US_LOCATIONS = {
    "New York, NY": "New York, NY, USA",
    "San Francisco, CA": "San Francisco, CA, USA",
    "Seattle, WA": "Seattle, WA, USA",
    "Los Angeles, CA": "Los Angeles, CA, USA",
    "Chicago, IL": "Chicago, IL, USA"
}

SUGGESTED_ZIPS = ["94103 (San Francisco)", "90001 (Los Angeles)", "98101 (Seattle)"]

@st.cache_data(show_spinner=False)
def geocode_location(query):
    geolocator = Nominatim(user_agent="quake-weather-app")
    location = geolocator.geocode(query, exactly_one=True, timeout=10)
    return (location.latitude, location.longitude) if location else (0, 0)

def render_region_selector():
    st.subheader("🗺️ Select US Region for Analysis")

    method = st.radio("Choose Location Method", ["City/State", "ZIP Code"], horizontal=True)

    if method == "ZIP Code":
        zip_input = st.text_input("🔢 Enter ZIP Code", value="10001")
        st.caption("💡 Try: " + ", ".join(SUGGESTED_ZIPS))
        query = f"{zip_input}, USA"
    else:
        location_name = st.selectbox("🏙️ Choose a U.S. City", list(US_LOCATIONS.keys()), index=1)
        query = US_LOCATIONS[location_name]

    latitude, longitude = geocode_location(query)
    st.session_state["latitude"] = latitude
    st.session_state["longitude"] = longitude

    with st.expander("🔧 Filters & Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            preview_min_mag = st.slider("Minimum Magnitude", 2.0, 7.0, 3.5, step=0.1)
        with col2:
            show_tectonics = st.checkbox("Show Tectonic Boundaries", value=True, key='tectonics_region_selector')
            st.session_state["show_tectonics"] = show_tectonics

    history_start = (datetime.now() - timedelta(days=5*365)).date()
    history_end = datetime.now().date()

    preview_df = fetch_earthquake_data(
        str(history_start), str(history_end),
        min_magnitude=preview_min_mag,
        latitude=latitude,
        longitude=longitude,
        max_radius_km=500
    )

    locations = preview_df[["Latitude", "Longitude"]].dropna().values.tolist()
    m = folium.Map(control_scale=True)

    for _, row in preview_df.iterrows():
        popup = folium.Popup(f"<b>{row['Place']}</b><br>Mag: {row['Magnitude']}<br>Date: {row['Time']}", max_width=250)
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=3,
            color='red',
            fill=True,
            fill_opacity=0.6,
            popup=popup,
            tooltip=f"{row['Place']} | Mag {row['Magnitude']} | {row['Time']}"
        ).add_to(m)


    if locations:
        m.fit_bounds(locations)
    else:
        m.location = [latitude, longitude]
        m.zoom_start = 5

    st.markdown("### 📍 Earthquake History Map (click for location info)")
    output = st_folium(m, width=1000, height=600)

    if output.get("last_clicked"):
        clicked_lat = output["last_clicked"]["lat"]
        clicked_lon = output["last_clicked"]["lng"]
        st.session_state["latitude"] = clicked_lat
        st.session_state["longitude"] = clicked_lon
        st.success(f"📌 Coordinates selected: ({clicked_lat:.4f}, {clicked_lon:.4f})")

    if not preview_df.empty:
        preview_df['Time'] = pd.to_datetime(preview_df['Time'])
        preview_df['Year-Month'] = preview_df['Time'].dt.to_period('M').astype(str)
        monthly_summary = preview_df.groupby('Year-Month').size().reset_index(name='Quake Count')
        st.session_state["available_months"] = monthly_summary["Year-Month"].tolist()

        st.markdown("### 📊 Summary")
        latest_event = preview_df.sort_values("Time", ascending=False).iloc[0]
        avg_mag = round(preview_df["Magnitude"].mean(), 2)

        st.info(f"""
        - **Total Events:** {len(preview_df)}  
        - **Most Recent:** {latest_event['Time']} @ {latest_event['Place']}  
        - **Average Magnitude:** {avg_mag}
        """)

        with st.expander("📈 View Monthly Earthquake Trend"):
            import plotly.express as px
            fig = px.bar(
                monthly_summary,
                x="Year-Month",
                y="Quake Count",
                title="Monthly Earthquake Frequency",
                labels={"Year-Month": "Month", "Quake Count": "Events"}
            )
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No data found for this region. Try a ZIP like 94103, 90001, or 98101 for better results.")
