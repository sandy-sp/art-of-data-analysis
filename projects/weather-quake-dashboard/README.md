# 🌍 Weather & Earthquake Insight Dashboard

An interactive Streamlit dashboard that combines historical **weather** data (from Open-Meteo) with real-time **earthquake** data (from USGS) to help you explore geophysical patterns, correlations, and risks.

---

## 🚀 Features

- 🌡️ Hourly Temperature, Humidity, Wind, and Precipitation from Open-Meteo
- 🌋 USGS Earthquake Events by Time, Location, and Magnitude
- 🗺️ Interactive Folium Map View with clustered quakes and weather overlay
- 📈 Time Series Visualizations
- 🔍 Correlation Analysis: Temperature/Humidity vs Earthquake Magnitude
- 📤 Export-ready and testable with Pytest

---

## 📦 Setup

```bash
git clone https://github.com/yourusername/weather-quake-dashboard.git
cd weather-quake-dashboard
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧪 Run Tests

```bash
pytest tests/
```

---

## 🔗 API References

- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/)

---

## 📁 Project Structure

```plaintext
├── app.py                  # Streamlit entry point
├── pages/                  # Multi-tab view scripts
├── src/                    # API, component, and utility modules
├── data/                   # Raw and processed local data (optional caching)
├── tests/                  # Unit test modules
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

---

## 📸 Screenshots (Optional)
_Add `streamlit-folium`, `plotly`, or live gif previews here._

---

## 📄 License

MIT License © [Your Name](https://github.com/yourusername)
