# 🌍 USGS Earthquake Visualizer

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Requests](https://img.shields.io/badge/API-Requests-20232a?logo=python&logoColor=white)](https://docs.python-requests.org)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-0.10%2B-green?logo=python&logoColor=white)](https://geopandas.org/)
[![Folium](https://img.shields.io/badge/Folium-0.12%2B-blue)](https://python-visualization.github.io/folium/)
[![Matplotlib](https://img.shields.io/badge/Plots-Matplotlib-yellow?logo=python&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Charts-Seaborn-4B8BBE?logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![USGS](https://img.shields.io/badge/API-earthquake.usgs.gov-green)](https://earthquake.usgs.gov/)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ed?logo=docker&logoColor=white)](https://www.docker.com)

---

## 📖 Overview

An interactive geospatial dashboard that allows users to fetch and explore recent earthquake events using the [USGS Earthquake Catalog API](https://earthquake.usgs.gov/fdsnws/event/1/). Users can filter events by location (country), time, and magnitude, and view results on an interactive map with animated data visualizations.

---

## 🚨 Live on Streamlit Cloud

> 🟢 Try it now: [🌍 USGS Earthquake Visualizer](https://art-of-data-analysis-earthquake-viz.streamlit.app/)

---

## 🚀 Features

- **Country-Specific Filtering**: Select a country from a dropdown sourced from Natural Earth shapefiles.
- **Interactive Map (Folium)**:
  - Color by depth (yellow/orange/red)
  - Size by magnitude (exponential scaling)
  - Clustered markers with tooltips & popups
  - Layer toggles (OpenStreetMap, Terrain, Satellite)
- **Custom Filters**:
  - Start date, end date
  - Minimum magnitude
  - Max number of events
- **Animated Chart Grid**:
  - Magnitude histogram
  - Depth histogram
  - Time series (events over time)
  - Location scatter (lat/lon)
- **Advanced Visualizations in Tabs**:
  - Cumulative timeline
  - Magnitude vs. depth scatter
  - Earthquake location timeline
  - Shockwave ripple animation
  - Spiral timeline
  - Depth strip chart
- **Data Table + CSV Export**:
  - Clean `st.dataframe` view
  - Download filtered results as CSV
- **Caching & Performance**:
  - API caching (15 mins)
  - Shapefile caching

---

## 📊 Data Sources & Credits

- **USGS Earthquake Catalog API**: [earthquake.usgs.gov](https://earthquake.usgs.gov/fdsnws/event/1/)
- **Natural Earth Shapefiles**: Admin 0 – Countries  
  [naturalearthdata.com](https://www.naturalearthdata.com/)

---

## 📊 How It Works

1. **User Input**: Choose a country and filter options from the sidebar.
2. **Geo Filtering**: Country boundaries from Natural Earth are used to form bounding box.
3. **API Query**: Fetches earthquake GeoJSON data from USGS.
4. **Map Rendering**: Folium displays events as color/size-coded markers.
5. **Chart Animations**: Matplotlib renders GIFs saved in `data/output_charts/`.
6. **DataFrame & CSV**: Displayed in `st.dataframe` and downloadable.

---

## 🖼️ Earthquakes in USA from 2024/04/09 to 2025/04/09 (Sample Output Gallery Charts)
All visualizations are dynamically generated using real earthquake data.

| Chart | Description |
|-------|-------------|
| ![](data/output_charts/magnitude.gif) | Histogram showing distribution of magnitudes |
| ![](data/output_charts/depth.gif) | Histogram of earthquake depths (in km) |
| ![](data/output_charts/timeseries.gif) | Events per day over the selected time range |
| ![](data/output_charts/locations.gif) | Earthquake locations plotted on 2D map |
| ![](data/output_charts/cumulative_timeseries.gif) | Cumulative earthquake timeline |
| ![](data/output_charts/magnitude_vs_depth.gif) | Scatter plot of magnitude vs depth |
| ![](data/output_charts/quake_locations.gif) | Timeline-based location animation |
| ![](data/output_charts/shockwave.gif) | Shockwave ripple effect for each event |
| ![](data/output_charts/spiral_timeline.gif) | Spiral plot encoding time, depth, magnitude |
| ![](data/output_charts/depth_strip.gif) | Horizontal strip chart grouping depth zones |

---

## 📁 Project Structure

```
earthquake_viz/
├── app/
│   ├── config/            # API and shapefile paths
│   ├── core/              # API calls, data processing, geospatial utils
│   ├── ui/                # Streamlit UI components
│   ├── visualizations/    # Map builder & animated charts
│   └── main.py            # Streamlit entry point
├── data/                  # Natural Earth shapefiles & Output folder for .gif charts
├── requirements.txt       # Dependency list
└── README.md              # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sandy-sp/art-of-data-analysis.git
cd projects/earthquake_viz
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Shapefile(if required)
- URL: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/
- Extract to: `data/shapefiles/ne_110m_admin_0_countries/`

### 5. Run the App
```bash
streamlit run app/main.py
```

---

## 📄 License

MIT License © [Sandy](https://github.com/sandy-sp)

---

## 🙏 Connect with Me

- [LinkedIn](https://www.linkedin.com/in/sandeep-paidipati)
- [GitHub](https://github.com/sandy-sp)
- [Data Portfolio](https://github.com/sandy-sp/art-of-data-analysis)

