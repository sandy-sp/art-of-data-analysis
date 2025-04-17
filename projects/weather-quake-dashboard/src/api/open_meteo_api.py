import requests
import pandas as pd
from typing import Tuple
from src.utils.caching import cached_api_call

def _fetch_open_meteo(lat, lon, start_date, end_date):
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
        "hourly": "temperature_2m,relativehumidity_2m,precipitation"
    }

    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        hourly_df = pd.DataFrame(data.get("hourly", {}))
        if not hourly_df.empty:
            hourly_df['time'] = pd.to_datetime(hourly_df['time'])

        return hourly_df
    except Exception as e:
        print(f"[Open-Meteo API Error]: {e}")
        return pd.DataFrame()

def fetch_historical_weather(lat: float, lon: float, start_date: str, end_date: str) -> pd.DataFrame:
    return cached_api_call(_fetch_open_meteo, lat, lon, start_date, end_date)
