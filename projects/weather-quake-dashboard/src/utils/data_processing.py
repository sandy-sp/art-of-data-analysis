import pandas as pd
from typing import Tuple
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import nearest_points
from geopy.distance import geodesic


def align_weather_quake_data(hourly_df: pd.DataFrame, quake_df: pd.DataFrame) -> pd.DataFrame:
    if hourly_df.empty or quake_df.empty:
        return pd.DataFrame()

    weather = hourly_df.copy()
    quakes = quake_df.copy()

    weather['time'] = pd.to_datetime(weather['time'])
    quakes['Time'] = pd.to_datetime(quakes['Time'])
    weather['hour'] = weather['time'].dt.floor('H')
    quakes['hour'] = quakes['Time'].dt.floor('H')

    merged = pd.merge(quakes, weather, on='hour', how='inner', suffixes=('_quake', '_weather'))
    return merged

def summarize_earthquake_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"total": 0}

    return {
        "total": len(df),
        "avg_magnitude": round(df['Magnitude'].mean(), 2),
        "max_magnitude": round(df['Magnitude'].max(), 2),
        "deepest": round(df['Depth_km'].max(), 2),
    }

def validate_alignment(hourly_df: pd.DataFrame, quake_df: pd.DataFrame, min_matches: int = 3) -> Tuple[bool, str]:
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

def filter_quakes_near_boundaries(quake_df: pd.DataFrame, boundary_gdf: gpd.GeoDataFrame, max_distance_km: float = 50.0) -> pd.DataFrame:
    """
    Filters earthquakes to only those within `max_distance_km` from any tectonic boundary.
    """
    if quake_df.empty or boundary_gdf.empty:
        return pd.DataFrame()

    quake_gdf = gpd.GeoDataFrame(
        quake_df.copy(),
        geometry=gpd.points_from_xy(quake_df['Longitude'], quake_df['Latitude']),
        crs='EPSG:4326'
    )

    def min_distance_km(row_geom):
        distances = boundary_gdf.geometry.apply(lambda line: geodesic((row_geom.y, row_geom.x), (line.centroid.y, line.centroid.x)).km)
        return distances.min()

    quake_gdf['distance_km'] = quake_gdf.geometry.apply(min_distance_km)
    filtered = quake_gdf[quake_gdf['distance_km'] <= max_distance_km].copy()
    return filtered.drop(columns=['geometry'])
