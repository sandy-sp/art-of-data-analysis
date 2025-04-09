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
    **other_params # Catch any other valid API parameters
    ) -> dict | None:
    """
    Fetches earthquake data from the USGS FDSN Event Web Service.

    Args:
        starttime (str, optional): Lower time boundary (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS). Defaults to None.
        endtime (str, optional): Upper time boundary (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS). Defaults to None.
        min_magnitude (float, optional): Minimum magnitude. Defaults to None.
        limit (int, optional): Maximum number of events to return. Defaults to settings.DEFAULT_LIMIT.
        bounding_box (list, optional): [min_lon, min_lat, max_lon, max_lat]. Defaults to None.
        latitude (float, optional): Latitude for circular search. Defaults to None.
        longitude (float, optional): Longitude for circular search. Defaults to None.
        max_radius_km (float, optional): Max radius in km for circular search. Defaults to None.
        **other_params: Additional valid API parameters (e.g., maxdepth, orderby).

    Returns:
        dict | None: Parsed GeoJSON dictionary response from the API, or None if an error occurs.
    """
    api_url = f"{settings.USGS_API_BASE_URL}query"
    query_params = {
        "format": "geojson",
        "limit": limit,
    }

    # Add optional parameters if they are provided
    if starttime:
        query_params["starttime"] = starttime
    if endtime:
        query_params["endtime"] = endtime
    if min_magnitude is not None: # Check for None explicitly as 0 is a valid magnitude
        query_params["minmagnitude"] = min_magnitude

    # Handle geographic filters (priority: bounding box, then circle)
    if bounding_box and len(bounding_box) == 4:
        query_params["minlongitude"] = bounding_box[0]
        query_params["minlatitude"] = bounding_box[1]
        query_params["maxlongitude"] = bounding_box[2]
        query_params["maxlatitude"] = bounding_box[3]
        logging.info(f"Applying bounding box filter: {bounding_box}")
    elif latitude is not None and longitude is not None and max_radius_km is not None:
        query_params["latitude"] = latitude
        query_params["longitude"] = longitude
        query_params["maxradiuskm"] = max_radius_km
        logging.info(f"Applying circular filter: lat={latitude}, lon={longitude}, radius={max_radius_km}km")
    else:
         logging.info("No specific geographic filter applied (fetching globally or based on other params).")


    # Add any other parameters passed via kwargs
    query_params.update(other_params)

    logging.info(f"Querying USGS API: {api_url} with params: {query_params}")

    try:
        response = requests.get(api_url, params=query_params, timeout=30) # 30-second timeout
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        logging.info(f"API request successful (Status Code: {response.status_code})")
        data = response.json() # Parse the JSON response directly

        # Optional: Log basic info about the result
        if 'features' in data:
            logging.info(f"Fetched {len(data['features'])} earthquake events.")
        else:
             logging.warning("API response structure might be unexpected (no 'features' key).")

        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during API fetch: {e}")
        return None
