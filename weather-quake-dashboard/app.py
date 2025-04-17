import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.region_selector import render_region_selector
from src.api.open_meteo_api import fetch_historical_weather
from src.api.usgs_earthquake_api import fetch_earthquake_data
from src.utils.tectonic_loader import load_tectonic_boundaries
from src.utils.exporter import export_quakes_and_boundaries_geojson
from src.visualizations.time_series import display_timeseries
from src.visualizations.correlations import display_correlations
from src.visualizations.quake_3d import display_3d_quakes

# Set Streamlit page configuration
st.set_page_config(
    page_title="🌍 Weather & Earthquake Insight Dashboard",
    page_icon="🌋",
    layout="wide"
)

# Styled Header
st.markdown("""
    <h1 style='font-size: 2.4rem; color: #333;'>🌍 Weather & Earthquake Insight Dashboard</h1>
    <p style='font-size: 1.1rem; color: #555;'>
        An interactive Streamlit dashboard for:
        <ul>
            <li>Exploring weather and seismic trends</li>
            <li>Correlating earthquake and climate data</li>
            <li>Analyzing spatial and temporal risk factors</li>
            <li>Viewing 3D seismic depth visualizations</li>
            <li>Try using a ZIP code like 94103 (San Francisco), or 90001 (Los Angeles)</li>
        </ul>
    </p>
""", unsafe_allow_html=True)

# --- US Region Selector ---
render_region_selector()

# --- Sidebar Input ---
fetch_params = render_sidebar()

# --- Data Fetch & Visualization ---
if fetch_params:
    with st.spinner("📡 Fetching Data from APIs..."):
        weather_df = fetch_historical_weather(
            fetch_params['latitude'], fetch_params['longitude'],
            str(fetch_params['start_date']), str(fetch_params['end_date'])
        )
        quake_df = fetch_earthquake_data(
            str(fetch_params['start_date']), str(fetch_params['end_date']),
            fetch_params['min_magnitude'], fetch_params['latitude'],
            fetch_params['longitude'], fetch_params['max_distance_km']
        )
        boundary_gdf = load_tectonic_boundaries()

    if len(quake_df) < 5:
        st.warning("⚠️ The selected region has limited earthquake data. Try using a ZIP code like 94103 (San Francisco), 90001 (Los Angeles), or 98101 (Seattle) for richer visualizations.")

    st.markdown("---")
    tabs = st.tabs(["📈 Time Series", "🔗 Correlations", "🌐 3D Quakes"])

    with tabs[0]:
        display_timeseries(weather_df, quake_df)

    with tabs[1]:
        display_correlations(weather_df, quake_df)

    with tabs[2]:
        display_3d_quakes(quake_df)

    st.markdown("### 🗂 Export GeoJSON")
    if st.button("📤 Download Earthquakes + Boundaries GeoJSON"):
        geojson_data = export_quakes_and_boundaries_geojson(quake_df, boundary_gdf)
        st.download_button(
            label="📎 Save GeoJSON",
            data=geojson_data,
            file_name="earthquakes_with_boundaries.geojson",
            mime="application/geo+json"
        )
else:
    st.info("👈 Use the sidebar and region selector to begin analysis.")

with st.sidebar:
    st.markdown("<div style='height: 100%; display: flex; flex-direction: column; justify-content: flex-end;'>", unsafe_allow_html=True)
    st.markdown("""
    <p style='margin-top: 10px; font-size: 16px;'>
        📘 Curious how this project works under the hood? <a href='https://github.com/sandy-sp/art-of-data-analysis/tree/main/projects/weather-quake-dashboard/README.md' target='_blank'>Check out the GitHub README</a> for code, setup, and deployment tips.
    </p>
    <p style='margin-top: 20px; font-size: 16px;'>
        💡 Enjoying this project? Interested in building similar data apps or collaborating on visualization tools?
        Let’s connect and share ideas!
    </p>
    <style>
    .social-icons a {
        text-decoration: none;
        font-size: 20px;
        display: inline-flex;
        align-items: center;
        margin-right: 10px;
        margin-bottom: 6px;
    }
    .social-icons a:hover {
        text-decoration: underline;
    }
    </style>
    <div class='social-icons'>
        <a href="https://www.linkedin.com/in/sandeep-paidipati" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" width="24" style="margin-right:8px; vertical-align:middle;" /> LinkedIn
        </a><br>
        <a href="https://github.com/sandy-sp" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" width="24" style="margin-right:8px; vertical-align:middle;" /> GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
