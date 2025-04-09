# 🌦️ Weather Forecast Visualizer
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Charts-Plotly-3e4f6a?logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Requests](https://img.shields.io/badge/API-Requests-20232a?logo=python&logoColor=white)](https://docs.python-requests.org)
[![Geopy](https://img.shields.io/badge/Geo-Pgeocode-008080?logo=earth&logoColor=white)](https://pypi.org/project/pgeocode)
[![Openpyxl](https://img.shields.io/badge/Excel-openpyxl-1a73e8?logo=microsoft-excel&logoColor=white)](https://pypi.org/project/openpyxl)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ed?logo=docker&logoColor=white)](https://www.docker.com)


An interactive web app to visualize hourly and daily weather forecasts using the [Open-Meteo API](https://open-meteo.com/). Built with **Streamlit** and **Plotly**, this tool fetches real-time weather data based on ZIP code input and displays interactive visualizations for temperature, humidity, wind, and precipitation.

---

## 📦 Features

- U.S. ZIP code-based forecast lookup with validation
- Interactive visualizations for:
  - Hourly & daily temperature
  - Feels-like temperature
  - Humidity & precipitation
  - Wind speed, direction, and vector field
  - Combined temperature & humidity
- Download weather data as CSV and Excel
- Sidebar with social links and project README reference
- Responsive layout for wide and narrow screens

---

## 🖥️ Live App Demo

> ✅ Live Demo: [🌦️ Weather Forecast Visualizer](https://art-of-data-analysis-weather-viz.streamlit.app/)


---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/sandy-sp/art_of_data_analysis_projects_weather_viz.git
cd art_of_data_analysis_projects_weather_viz/projects/weather_viz
```

### 2. Install Requirements

Make sure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

> `requirements.txt` should include:  
> `streamlit`, `pandas`, `plotly`, `pgeocode`, `requests`, `openpyxl`

### 3. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🧠 How It Works

- Uses `pgeocode` to convert ZIP code → latitude & longitude
- Queries Open-Meteo API for hourly and daily forecast data
- Processes it into clean `pandas` DataFrames
- Visualizes trends with Plotly (line, bar, polar, and vector plots)
- Presents UI via Streamlit with user-friendly layout and controls

---

## 📁 Project Structure

```
weather_viz/
├── app.py                      # Streamlit app entry point
├── requirements.txt
├── src/
   ├── api_handler.py          # Fetches weather data from API
   ├── data_processor.py       # Cleans and enriches raw API data
   └── visualizations/         # All interactive Plotly visualizations
    .....
```

---

## 📸 Sample Video
[![🌦️ Weather Forecast Visualizer](assets/weather_viz.png)](assets/weather_viz.mp4)

---

## 📋 License

MIT License © [Sandy](https://github.com/sandy-sp)

---

## 🤗 Connect with Me

If you liked this project and want to connect or collaborate:

- [LinkedIn](https://www.linkedin.com/in/sandeep-paidipati)
- [GitHub](https://github.com/sandy-sp)
- [Project README](https://github.com/sandy-sp/art-of-data-analysis/tree/main/projects/weather_viz)

