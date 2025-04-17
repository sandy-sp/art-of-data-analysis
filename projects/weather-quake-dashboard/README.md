# 🌍 Weather & Earthquake Insight Dashboard

An interactive Streamlit dashboard integrating **Open-Meteo weather data**, **USGS earthquake data**, and **tectonic plate boundaries** to visualize and explore geophysical patterns and correlations.

---

## 🚀 Features

- 📊 **Time Series Analysis**  
  Explore trends in temperature, humidity, and earthquake frequency.

- 🔗 **Correlation Visualization**  
  Analyze potential relationships between earthquake magnitude and weather.

- 🌐 **3D Earthquake Visualization**  
  View depth and magnitude of seismic events in a fully rotatable 3D plot.

- 📍 **Region Selector**  
  Choose a country or click on the map to set analysis coordinates.

---

## 🧰 Technologies

- [Streamlit](https://streamlit.io)
- [Plotly](https://plotly.com/python/)
- [Folium](https://python-visualization.github.io/folium/)
- [Open-Meteo API](https://open-meteo.com/en/docs)
- [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/)

---

## 🛠️ Setup

```bash
# Clone the repository
git clone https://github.com/sandy-sp/art-of-data-analysis.git
cd projects/weather-quake-dashboard

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📁 Directory Structure

```plaintext
weather-quake-dashboard/
├── app.py                        # Main Streamlit entry point
├── requirements.txt             # Python dependencies
├── data/                        # Static GeoJSON tectonic boundary files
├── src/
│   ├── api/                     # API integration (Open-Meteo, USGS)
│   ├── components/              # Sidebar and region selector
│   ├── utils/                   # Data processing, caching, tectonic loader
│   └── visualizations/          # Map, time series, correlations, 3D plots
└── .streamlit/
    └── config.toml              # UI theme config
```

---

## 📸 Screenshots

![Map View](assets/screenshot_map.png)
![Time Series](assets/screenshot_time_series.png)
![Correlations](assets/screenshot_correlation.png)
![3D Quake View](assets/screenshot_3d.png)

*(Place your actual screenshot files in an `assets/` folder.)*

---

## 🪪 License

MIT License © [Sandy SP](https://github.com/sandy-sp)

---
