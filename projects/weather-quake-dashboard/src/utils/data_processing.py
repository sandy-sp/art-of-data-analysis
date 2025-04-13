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
    weather['hour'] = weather['time'].dt.floor('h')
    quakes['hour'] = quakes['Time'].dt.floor('h')

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

def validate_alignment(hourly_df: pd.DataFrame, quake_df: pd.DataFrame, min_matches: int = 3) -> Tuple[bool, str]:
    """
    Validates whether weather and earthquake data align sufficiently for analysis.
    Returns a tuple (is_valid, message).
    """
    if hourly_df.empty:
        return False, "Weather data is empty."
    if quake_df.empty:
        return False, "Earthquake data is empty."

    weather_hours = pd.to_datetime(hourly_df['time']).dt.floor('H')
    quake_hours = pd.to_datetime(quake_df['Time']).dt.floor('H')

    matched_hours = set(weather_hours).intersection(set(quake_hours))
    if len(matched_hours) < min_matches:
        return False, f"Insufficient overlapping hours between weather and earthquake data ({len(matched_hours)} found, {min_matches} required)."

    return True, "Data is aligned and ready."
