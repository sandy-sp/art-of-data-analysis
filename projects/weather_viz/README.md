# 🌦️ Weather Forecast Visualizer

An interactive web app to visualize hourly and daily weather forecasts using the [Open-Meteo API](https://open-meteo.com/). Built with **Streamlit** and **Plotly**, this tool fetches real-time weather data based on city input and displays interactive visualizations for temperature, humidity, wind, and precipitation.

---

## 📦 Features

- City-based weather forecast lookup (via geolocation)
- Interactive visualizations for:
  - Hourly & daily temperature
  - Feels-like temperature
  - Humidity & precipitation
  - Wind speed, direction, and vector field
  - Combined temperature & humidity
- Responsive layout for wide and narrow screens

---

## 🖥️ Live App Demo

> Coming soon! (You can deploy to [Streamlit Cloud](https://streamlit.io/cloud) or use Docker.)

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
> `streamlit`, `pandas`, `plotly`, `geopy`, `requests`

### 3. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🧠 How It Works

- Uses `geopy` to convert city name → latitude & longitude
- Queries Open-Meteo API for hourly and daily data
- Processes it into `pandas` DataFrames
- Plots data interactively with Plotly
- Displays all visuals in a clean, responsive Streamlit UI

---

## 📁 Project Structure

```
weather_viz/
├── app.py                      # Streamlit app entry point
├── requirements.txt
├── src/
│   ├── api_handler.py          # Fetches weather data from API
│   ├── data_processor.py       # Cleans and enriches raw API data
│   └── visualizations/         # All interactive Plotly visualizations
└── reports/
    └── visualizations/         # (Not used in Streamlit mode)
```

---

## 📸 Sample Visualizations

> Include screenshots here once the app is running:
- Hourly Temperature Line Chart
- Wind Direction Rose
- Wind Speed Vectors

---

## 📤 Deployment (Optional)

You can deploy this app via:
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Render](https://render.com)
- Docker + Cloud VM

Let me know if you'd like a deploy guide!

---

## 📝 License

MIT License © Sandy

```

---

