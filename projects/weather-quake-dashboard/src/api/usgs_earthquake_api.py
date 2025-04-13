import requests
import pandas as pd
from datetime import datetime
from typing import Tuple

def fetch_earthquake_data(
    starttime: str,
    endtime: str,
    min_magnitude: float,
    latitude: float,
    longitude: float,
    max_radius_km: float = 500,
    limit: int = 500
) -> pd.DataFrame:
    """
    Fetch earthquake data from USGS Earthquake API.
    Returns a DataFrame of event information.
    """
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": min_magnitude,
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": max_radius_km,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        features = data.get("features", [])
        records = []

        for feature in features:
            props = feature.get("properties", {})
            geom = feature.get("geometry", {})
            coords = geom.get("coordinates", [None, None, None])

            record = {
                "Time": datetime.utcfromtimestamp(props.get("time", 0) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                "Place": props.get("place", "N/A"),
                "Magnitude": props.get("mag", 0.0),
                "Latitude": coords[1],
                "Longitude": coords[0],
                "Depth_km": coords[2],
                "URL": props.get("url", "")
            }
            records.append(record)

        df = pd.DataFrame(records)
        return df

    except Exception as e:
        print(f"[USGS] Failed to fetch earthquake data: {e}")
        return pd.DataFrame()
