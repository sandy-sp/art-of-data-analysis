from datetime import timedelta 
import requests
import logging
from datetime import datetime
from app.config import settings 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_earthquake_data(
    starttime: str = None,
    endtime: str = None,
    min_magnitude: float = None,
    limit: int = settings.DEFAULT_LIMIT,
    bounding_box: list = None,
    latitude: float = None,
    longitude: float = None,
    max_radius_km: float = None,
    **other_params
) -> dict | None:
    """
    Fetches earthquake data from the USGS FDSN Event Web Service.
    Prioritizes circular search over bounding box if both are provided.
    """
    api_url = f"{settings.USGS_API_BASE_URL}query"
    query_params = {
        "format": "geojson",
        "limit": limit,
    }

    # Add common filters
    if starttime:
        query_params["starttime"] = starttime
    if endtime:
        query_params["endtime"] = endtime
    if min_magnitude is not None:
        query_params["minmagnitude"] = min_magnitude

    # --- Location Filters (Priority: City → Bounding Box → None) ---
    if latitude is not None and longitude is not None and max_radius_km is not None:
        query_params.update({
            "latitude": latitude,
            "longitude": longitude,
            "maxradiuskm": max_radius_km
        })
        logging.info(f"Applying circular search: lat={latitude}, lon={longitude}, radius={max_radius_km}km")
    elif bounding_box and len(bounding_box) == 4:
        query_params.update({
            "minlongitude": bounding_box[0],
            "minlatitude": bounding_box[1],
            "maxlongitude": bounding_box[2],
            "maxlatitude": bounding_box[3],
        })
        logging.info(f"Applying bounding box search: {bounding_box}")
    else:
        logging.info("No specific geographic filter applied (global search).")

    # Additional params (e.g., orderby, maxdepth, etc.)
    query_params.update(other_params)

    logging.info(f"USGS API Request: {api_url}")
    logging.info(f"Parameters: {query_params}")

    try:
        response = requests.get(api_url, params=query_params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "features" in data:
            logging.info(f"Fetched {len(data['features'])} earthquake events.")
        else:
            logging.warning("Unexpected API response format: missing 'features' key.")

        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error during API fetch: {e}")
        return None
