import requests
import pandas as pd
from datetime import datetime
from src.utils.caching import cached_api_call

def _fetch_usgs_earthquake_data(starttime, endtime, min_magnitude, latitude, longitude, max_radius_km):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": min_magnitude,
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": max_radius_km,
        "limit": 500
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        features = response.json().get("features", [])
        
        records = [{
            "Time": datetime.utcfromtimestamp(f["properties"]["time"] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            "Place": f["properties"]["place"],
            "Magnitude": f["properties"]["mag"],
            "Latitude": f["geometry"]["coordinates"][1],
            "Longitude": f["geometry"]["coordinates"][0],
            "Depth_km": f["geometry"]["coordinates"][2]
        } for f in features]

        return pd.DataFrame(records)
    except Exception as e:
        print(f"[USGS API Error]: {e}")
        return pd.DataFrame()

def fetch_earthquake_data(starttime: str, endtime: str, min_magnitude: float,
                          latitude: float, longitude: float, max_radius_km: float) -> pd.DataFrame:
    return cached_api_call(_fetch_usgs_earthquake_data, starttime, endtime, min_magnitude,
                           latitude, longitude, max_radius_km)
