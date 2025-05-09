# Art of Data Analysis

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Charts-Plotly-3e4f6a?logo=plotly&logoColor=white)](https://plotly.com)
[![Folium](https://img.shields.io/badge/Maps-Folium-43a047?logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-0.10%2B-green?logo=python&logoColor=white)](https://geopandas.org/)
[![Matplotlib](https://img.shields.io/badge/Plots-Matplotlib-yellow?logo=python&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Charts-Seaborn-4B8BBE?logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Requests](https://img.shields.io/badge/API-Requests-20232a?logo=python&logoColor=white)](https://docs.python-requests.org)
[![Open-Meteo](https://img.shields.io/badge/API-Open--Meteo-green)](https://open-meteo.com/)
[![USGS](https://img.shields.io/badge/API-USGS-grey)](https://earthquake.usgs.gov/fdsnws/event/1/)
[![Geopy](https://img.shields.io/badge/Geocoding-Geopy-blue)](https://pypi.org/project/geopy/)
[![Openpyxl](https://img.shields.io/badge/Excel-openpyxl-1a73e8?logo=microsoft-excel&logoColor=white)](https://pypi.org/project/openpyxl)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ed?logo=docker)](https://www.docker.com)


## Overview

Welcome to **Art of Data Analysis**, a curated portfolio of end-to-end data analysis projects. This repository showcases how raw data is transformed into actionable insights and compelling visual stories using Python, SQL, and modern data visualization tools. Each project demonstrates a specific skillset in the data analysis pipeline—from data ingestion to storytelling.

Whether it's identifying patterns, making predictions, or building interactive dashboards, the focus is on clarity, efficiency, and insight.

---

## Projects Included

### 1. 🌋 Weather & Earthquake Insight Dashboard ([Live App](https://art-of-data-analysis-weather-quake.streamlit.app/))
An interactive **Streamlit** dashboard combining **Open-Meteo**, **USGS**, and **tectonic plate data** to visualize weather and seismic activity over time and space.

Key features:

- Select region by U.S. **ZIP code or city/state**
- Integrated APIs:
  - Open-Meteo for historical weather (temperature, humidity, precipitation)
  - USGS Earthquake API for seismic event data
- Interactive visualizations:
  - Time series of weather vs. quake activity
  - Scatterplot correlation between magnitude and weather
  - 3D earthquake depth with rotation + zoom
  - Folium map with clustered quakes, tectonic overlays, tooltips
- Download filtered **GeoJSON**, **CSV**, or **Excel**

**Stack**: Python 3.10+, Streamlit, Plotly, Folium, GeoPandas, Open-Meteo, USGS API, Geopy

**Run Locally**:
```bash
git clone https://github.com/sandy-sp/art-of-data-analysis.git
cd projects/weather-quake-dashboard
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

### 2. 🌍 USGS Earthquake Visualizer ([Live App](https://art-of-data-analysis-earthquake-viz.streamlit.app/))
A geographic data app that uses the **USGS Earthquake API** to map recent earthquakes within country borders. Key features:

- Country-specific filtering using GeoPandas + Natural Earth shapefiles
- Interactive Folium map with:
  - Magnitude-based marker size
  - Depth-based marker color (legend included)
  - Marker clustering for performance
- Animated chart visualizations (e.g., histograms, time series, spiral timelines)
- CSV export of filtered dataset
- Streamlit sidebar UI with caching optimizations

**Stack**: Python 3.9+, Streamlit, GeoPandas, Folium, Requests, Pandas, Matplotlib, Seaborn

**Run Locally**:
```bash
git clone https://github.com/sandy-sp/art-of-data-analysis.git
cd projects/earthquake_viz
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```

> ✉️ Download Natural Earth shapefiles from:
> https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/

---

### 3. ✨ Weather Forecast Visualizer ([Live App](https://art-of-data-analysis-weather-viz.streamlit.app/))
An interactive **Streamlit** dashboard that fetches and visualizes hourly/daily weather forecasts using the [Open-Meteo API](https://open-meteo.com/). Features include:

- Forecast by ZIP code (U.S.) with location validation
- Interactive Plotly charts for temperature, humidity, wind & precipitation
- Combined temperature & humidity analysis
- CSV/Excel export of forecast data

**Stack**: Streamlit, Plotly, Pandas, Requests, Openpyxl, Pgeocode

**Run Locally**:
```bash
git clone https://github.com/sandy-sp/art_of_data_analysis_projects_weather_viz.git
cd art_of_data_analysis_projects_weather_viz/projects/weather_viz
pip install -r requirements.txt
streamlit run app.py
```

---

## Skills Demonstrated

- **Data Wrangling & Cleaning**: Handling missing values, transformation, reshaping
- **EDA & Visualization**: Seaborn, Matplotlib, Plotly, Geo-based mapping (Folium)
- **Statistical Reasoning**: Applying inference techniques where relevant
- **APIs & Data Fetching**: Requests, real-time data ingestion
- **Streamlit UI Development**: Custom interactive dashboards
- **Geospatial Data**: Shapefile parsing, map generation, spatial joins
- **Excel Automation**: Using openpyxl for exports

---

## Getting Started

### Clone This Repository:
```bash
git clone https://github.com/sandy-sp/art-of-data-analysis.git
```

Explore each project individually from its folder. Each includes:
- `README.md`: Project-specific setup and context
- `*.ipynb` or `app.py`: Notebooks or Streamlit scripts
- `/src/`: Modular scripts for data, visualization, APIs
- Output assets or charts

You may need to install dependencies using `pip` or `conda`, depending on the project.

---

## Contributions
This is a personal portfolio, but suggestions and constructive feedback are welcome. Open an issue or fork and submit a pull request.

---

## Contact
- Email: [sandeep.paidipati@gmail.com](mailto:sandeep.paidipati@gmail.com)
- LinkedIn: [https://www.linkedin.com/in/sandeep-paidipati/](https://www.linkedin.com/in/sandeep-paidipati/)
- GitHub: [https://github.com/sandy-sp](https://github.com/sandy-sp)

---

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use, adapt, and learn from the code provided.

---

Thanks for exploring the **Art of Data Analysis**!

