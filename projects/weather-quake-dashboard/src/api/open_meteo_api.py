import requests
import pandas as pd
from typing import Tuple

def fetch_historical_weather(lat: float, lon: float, start_date: str, end_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetch historical weather data from Open-Meteo API.
    Returns a tuple of (hourly_df, daily_df).
    """
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
        "hourly": "temperature_2m,relativehumidity_2m,precipitation,winddirection_10m,windspeed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    }

    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        hourly_df = pd.DataFrame(data.get("hourly", {}))
        daily_df = pd.DataFrame(data.get("daily", {}))

        if not hourly_df.empty:
            hourly_df['time'] = pd.to_datetime(hourly_df['time'])

        if not daily_df.empty:
            daily_df['time'] = pd.to_datetime(daily_df['time'])

        return hourly_df, daily_df

    except Exception as e:
        print(f"[Open-Meteo] Failed to fetch weather data: {e}")
        return pd.DataFrame(), pd.DataFrame()
