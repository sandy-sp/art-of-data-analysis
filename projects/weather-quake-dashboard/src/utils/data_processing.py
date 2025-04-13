import pandas as pd
from typing import Tuple

def align_weather_quake_data(hourly_df: pd.DataFrame, quake_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges hourly weather data and earthquake events based on datetime proximity (hour-level resolution).
    Returns a joined DataFrame for correlation analysis.
    """
    if hourly_df.empty or quake_df.empty:
        return pd.DataFrame()

    # Convert time columns
    weather = hourly_df.copy()
    quakes = quake_df.copy()

    weather['time'] = pd.to_datetime(weather['time'])
    quakes['Time'] = pd.to_datetime(quakes['Time'])
    weather['hour'] = weather['time'].dt.floor('H')
    quakes['hour'] = quakes['Time'].dt.floor('H')

    # Merge on 'hour'
    merged = pd.merge(quakes, weather, on='hour', how='inner', suffixes=('_quake', '_weather'))
    return merged

def summarize_earthquake_stats(df: pd.DataFrame) -> dict:
    """
    Generates summary statistics from earthquake data.
    """
    if df.empty:
        return {"total": 0}

    return {
        "total": len(df),
        "avg_magnitude": round(df['Magnitude'].mean(), 2),
        "max_magnitude": round(df['Magnitude'].max(), 2),
        "deepest": round(df['Depth_km'].max(), 2),
    }
