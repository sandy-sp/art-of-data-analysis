# Weather Data Visualization Project

This project fetches weather forecast data from the Open-Meteo API and generates visualizations for temperature, wind speed, and precipitation.

## Table of Contents

1.  [Installation](#installation)
2.  [Usage](#usage)
3.  [Visualizations](#visualizations)
    * [Hourly Temperature](#hourly-temperature)
    * [Hourly Wind Speed](#hourly-wind-speed)
    * [Hourly Precipitation](#hourly-precipitation)

## Installation

1.  Clone this repository (if applicable).
2.  Navigate to the project directory: `cd weather_viz`
3.  Install the required dependencies: `pip install -r requirements.txt`

## Usage

1.  Ensure you have an internet connection to fetch data from the API.
2.  Run the main script to generate the visualizations: `python src/main.py`
3.  The generated visualization images will be saved in the `reports/visualizations` directory.
4.  You can view the visualizations below.

## Visualizations

### Hourly Temperature

![Hourly Temperature](reports/visualizations/hourly_temperature.png)

This plot shows the hourly temperature forecast for Cleveland, OH over the next 7 days. The y-axis represents the temperature in Celsius (°C), and the x-axis represents the time in hourly intervals.

### Hourly Wind Speed

![Hourly Wind Speed](reports/visualizations/wind_plot.png)

This plot shows the hourly wind speed forecast for Cleveland, OH over the next 7 days. The y-axis represents the wind speed in kilometers per hour (km/h), and the x-axis represents the time in hourly intervals.

### Hourly Precipitation

![Hourly Precipitation](reports/visualizations/precipitation_plot.png)

This plot shows the hourly precipitation forecast for Cleveland, OH over the next 7 days. The y-axis represents the precipitation in millimeters (mm), and the x-axis represents the time in hourly intervals. The precipitation is visualized using a bar chart.