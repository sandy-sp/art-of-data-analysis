import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def geojson_to_dataframe(geojson_data: dict) -> pd.DataFrame | None:
    """
    Converts earthquake GeoJSON data into a Pandas DataFrame.

    Args:
        geojson_data (dict): Parsed GeoJSON dictionary from the USGS API.

    Returns:
        pd.DataFrame | None: A Pandas DataFrame containing key earthquake
                             information, or None if input is invalid.
    """
    if not geojson_data or 'features' not in geojson_data:
        logging.warning("Cannot create DataFrame from invalid or empty GeoJSON data.")
        return None

    features = geojson_data['features']
    if not features:
        logging.info("GeoJSON data has no features, returning empty DataFrame.")
        # Return an empty DataFrame with expected columns if features list is empty
        return pd.DataFrame(columns=[
            'Magnitude', 'Place', 'Time', 'Depth (km)',
            'Latitude', 'Longitude', 'Details URL', 'USGS ID'
        ])

    records = []
    for feature in features:
        try:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            coords = geometry.get('coordinates', [])

            # Basic validation
            if geometry.get('type') != 'Point' or len(coords) < 2:
                logging.warning(f"Skipping feature due to invalid geometry: {feature.get('id')}")
                continue

            # Extract data, providing defaults for missing values
            mag = properties.get('mag')
            place = properties.get('place', 'N/A')
            time_epoch_ms = properties.get('time')
            depth = coords[2] if len(coords) > 2 else 0.0 # Depth is 3rd element
            lat = coords[1] # Latitude is 2nd element
            lon = coords[0] # Longitude is 1st element
            details_url = properties.get('url', '#')
            usgs_id = feature.get('id', 'N/A')

            # Convert epoch milliseconds to datetime string
            time_str = "N/A"
            if time_epoch_ms:
                try:
                    time_dt = datetime.utcfromtimestamp(time_epoch_ms / 1000)
                    time_str = time_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                except Exception as e:
                    logging.warning(f"Could not format time for event {usgs_id}: {e}")

            # Append record to list
            records.append({
                'Magnitude': mag,
                'Place': place,
                'Time': time_str,
                'Depth (km)': depth,
                'Latitude': lat,
                'Longitude': lon,
                'Details URL': details_url,
                'USGS ID': usgs_id
            })

        except Exception as e:
            logging.error(f"Error processing feature {feature.get('id', 'Unknown ID')}: {e}", exc_info=True)
            continue # Skip to next feature if error occurs

    # Create DataFrame
    df = pd.DataFrame(records)
    logging.info(f"Created DataFrame with {len(df)} records.")

    # Optional: Sort by time descending by default?
    # df = df.sort_values(by='Time', ascending=False)

    return df