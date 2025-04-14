# 🌍 Weather & Earthquake Insight Dashboard

An advanced interactive dashboard built with Streamlit, combining **Open-Meteo weather data**, **USGS earthquake data**, and **high-resolution tectonic plate boundaries** to visualize geophysical activity and correlations.

---

## 🚀 Features

- 📍 **Region Picker**: Click on a tectonic map to select coordinates.
- 🌐 **Dynamic Country Zoom**: Auto-zooms map to selected country via geocoding.
- 📅 **Month & Year Filter**: Limits data to a valid 31-day window for Open-Meteo.
- 🌋 **Earthquake Analysis**:
  - Time series of magnitudes
  - Frequency bar charts
  - 3D depth scatterplot
  - Histogram of magnitudes
- 🔥 **Heatmaps**:
  - Earthquakes near vs far from tectonic boundaries
- 🗺️ **Tectonic Overlay**:
  - Load detailed USGS plate boundaries
  - Toggle on/off from the sidebar
- 📏 **Distance Filter**: Filter earthquakes within X km of tectonic plates

---

## 🛠️ Setup

```bash
git clone https://github.com/sandy-sp/art-of-data-analysis.git
cd projects/weather-quake-dashboard
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Additional Requirements
```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```plaintext
src/
├── api/                  # Open-Meteo and USGS API fetchers
├── components/           # Sidebar, region picker, map display
├── pages/                # Streamlit view modules
├── utils/                # Data processing + tectonic loader
├── data/                 # GeoJSON tectonic files, output
app.py                    # Entry point
```

---

## 📊 Visual Samples

| View               | Description                          |
|--------------------|--------------------------------------|
| Map View           | Earthquake & weather locations       |
| Time Series        | Temperature, humidity, frequency     |
| Correlations       | Scatter: magnitude vs temperature    |
| 3D View            | Earthquake depth by lat/lon/mag      |
| Heatmap            | Near vs far quake densities          |

---

## 🔗 Data Sources

- [Open-Meteo API](https://open-meteo.com/en/docs)
- [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [USGS Tectonic Boundaries (GeoJSON)](https://earthquake.usgs.gov/)

---

## 📄 License
MIT License © [Your Name](https://github.com/sandy-sp)
