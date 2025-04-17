# 🌍 Weather & Earthquake Insight Dashboard

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Charts-Plotly-3e4f6a?logo=plotly&logoColor=white)](https://plotly.com)
[![Folium](https://img.shields.io/badge/Maps-Folium-43a047?logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![Open-Meteo](https://img.shields.io/badge/API-Open--Meteo-green)](https://open-meteo.com/)
[![USGS](https://img.shields.io/badge/API-USGS-grey)](https://earthquake.usgs.gov/fdsnws/event/1/)
[![Geopy](https://img.shields.io/badge/Geocoding-Geopy-blue)](https://pypi.org/project/geopy/)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ed?logo=docker)](https://www.docker.com)

An interactive Streamlit app that visualizes the intersection of weather patterns, earthquake data, and tectonic boundaries in the United States using real-time geospatial APIs.

---

## 🔍 Features

- Select U.S. region via **city/state or ZIP code**
- Auto-fetch latitude/longitude with geocoding
- Real-time data from:
  - Open-Meteo API (weather)
  - USGS API (earthquakes)
- Visual components:
  - Time-series trends
  - Correlation scatterplots (magnitude ↔ weather)
  - 3D earthquake depth views
  - Interactive Folium map with clustered markers
  - Tectonic boundary overlay with tooltips + zoom cues
- Downloadable **GeoJSON export** of filtered events
- Smart fallback messaging + suggested ZIPs for data-rich regions

---

## 🚨 Live on Streamlit Cloud

> 🟢 Try it now: [🌍 Weather & Earthquake Insight Dashboard](https://art-of-data-analysis-weather-quake-dashboard.streamlit.app/)

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/sandy-sp/art-of-data-analysis.git
cd projects/weather-quake-dashboard
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or .\\venv\\Scripts\\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch App

```bash
streamlit run app.py
```

---

## 📦 Project Structure

```
weather-quake-dashboard/
├── app.py                     # Main Streamlit app
├── requirements.txt
├── src/
│   ├── api/                   # API calls (Open-Meteo, USGS)
│   ├── components/            # Sidebar, region selector, map
│   ├── utils/                 # Data processing, caching, tectonic loading
│   └── visualizations/        # Plotly/Folium visualizations
├── data/                      # Optional local tectonic GeoJSON
├── assets/                    # Screenshots, videos, thumbnails
└── .streamlit/                # Theme and config
```

---

## 🧠 How It Works

- Location selection → Geocoded using `Geopy`
- Coordinates → Used to query:
  - `Open-Meteo` archive for hourly weather
  - `USGS` for seismic activity within radius
- All data → Processed, filtered, merged using `Pandas`
- Displayed using:
  - `Plotly` (3D, correlation, bar)
  - `Folium` (interactive map + tectonics)
- Smart UI behavior via `Streamlit.session_state`

---

## 💾 Export Options

- Download **Excel** for weather data
- Download **CSV** for earthquakes
- Export combined **GeoJSON** of quakes + tectonics

---

## 🧪 Tested With

- Python 3.10
- Streamlit 1.25+
- geopandas, plotly, folium, requests, geopy

---

## 📜 License

MIT License © [Sandy SP](https://github.com/sandy-sp)

---

## 🤝 Connect & Collaborate

- [LinkedIn](https://www.linkedin.com/in/sandeep-paidipati)
- [GitHub](https://github.com/sandy-sp)
- [Project README](https://github.com/sandy-sp/art-of-data-analysis/tree/main/projects/weather-quake-dashboard)
