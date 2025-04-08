# ☔️ Weather Forecast Visualizer

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-orange?logo=streamlit)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-blue?logo=plotly)](https://plotly.com/python/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-yellow?logo=pandas)](https://pandas.pydata.org/)
[![Open-Meteo](https://img.shields.io/badge/API-Open--Meteo-green)](https://open-meteo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌐 Overview

The **Weather Forecast Visualizer** is a Streamlit-based web application that fetches and visualizes hourly and daily weather data for any ZIP code in the United States.
It uses the free [Open-Meteo API](https://open-meteo.com/) for real-time forecasts and displays interactive visualizations using **Plotly**.

---

## 🔗 Features

- ZIP code-based location lookup using `pgeocode`
- Hourly and daily weather data via Open-Meteo API
- Visualizations:
  - Temperature, Feels-like Temperature
  - Humidity and Precipitation
  - Wind Speed, Direction, and Vector Field
  - Combined Temperature & Humidity
- Downloadable content:
  - CSV and Excel for raw weather data
  - PNG charts for all visualizations

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/sandy-sp/art-of-data-analysis.git
cd art-of-data-analysis/projects/weather_viz
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

Make sure you have the following libraries installed:
- `streamlit`
- `pandas`
- `plotly`
- `pgeocode`
- `kaleido`
- `openpyxl`

### 3. Run the App
```bash
streamlit run app.py
```
Then open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
weather_viz/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Required dependencies
├── README.md               # Project overview and usage
├── src/
│   ├── api_handler.py      # Open-Meteo API integration
│   ├── data_processor.py   # Data transformation logic
│   └── visualizations/     # All plotly-based chart modules
└── reports/
    └── visualizations/     # PNG chart outputs (optional)
```

---

## 📈 Visualizations Gallery

> All plots are interactive and downloadable

- Hourly Temperature Line Chart
- Feels Like Temperature Plot
- Humidity Over Time
- Precipitation Bars
- Wind Speed Line + Direction Rose
- Wind Speed & Direction Vector Field
- Combined Temperature and Humidity
- Daily Max/Min Temperature Trend

---

## 🌐 Credits

- Weather data provided by **[Open-Meteo](https://open-meteo.com/)** — a free and open weather API.
- ZIP-to-Geo lookup powered by **[pgeocode](https://pypi.org/project/pgeocode/)**

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

### 🙏 Thanks for using Weather Forecast Visualizer!

If you find this tool useful, feel free to star the repository or share feedback.

