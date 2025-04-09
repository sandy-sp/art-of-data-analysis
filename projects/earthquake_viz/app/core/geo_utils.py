import geopandas as gpd
import logging
import os
import streamlit as st 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Shapefile Loading (Cached) ---
# Use st.cache_resource to load the large shapefile only once.
@st.cache_resource(show_spinner=False)
def load_world_shapefile(shapefile_path: str):
    """
    Loads the world shapefile and extracts a list of country names.

    Returns:
        tuple(gpd.GeoDataFrame | None, list[str] | None): A tuple containing
        the loaded GeoDataFrame (or None on error) and a sorted list of
        unique country names (or None on error).
    """
    if not os.path.exists(shapefile_path):
        logging.error(f"Shapefile not found at path: {shapefile_path}")
        st.error(f"Error: World boundaries shapefile not found at {shapefile_path}. Please download and place it correctly.")
        return None, None  # Return None for both gdf and list
    try:
        logging.info(f"Loading shapefile from: {shapefile_path}")
        world_gdf = gpd.read_file(shapefile_path)

        # --- Identify country name column ---
        original_name_column = 'ADMIN'  # Example: Adjust this!
        if original_name_column not in world_gdf.columns:
            logging.error(f"Expected country name column '{original_name_column}' not found in shapefile.")
            possible_cols = [col for col in world_gdf.columns if 'NAME' in col.upper() or 'ADMIN' in col.upper()]
            if possible_cols:
                original_name_column = possible_cols[0]
                logging.warning(f"Using fallback column '{original_name_column}' for country names.")
            else:
                st.error("Could not automatically determine the country name column in the shapefile.")
                return None, None  # Return None for both

        world_gdf['COUNTRY_NAME'] = world_gdf[original_name_column]
        logging.info(f"Shapefile loaded successfully with {len(world_gdf)} countries.")

        # --- Extract and sort unique country names ---
        try:
            country_list = sorted(world_gdf['COUNTRY_NAME'].unique().tolist())
            logging.info(f"Extracted {len(country_list)} unique country names.")
        except Exception as e:
            logging.error(f"Failed to extract country names: {e}")
            st.error("Could not extract country list from shapefile.")
            return world_gdf, None  # Return GDF but None for list

        return world_gdf, country_list  # Return both GDF and the list

    except Exception as e:
        logging.error(f"Failed to load or process shapefile {shapefile_path}: {e}", exc_info=True)
        st.error(f"Error loading shapefile: {e}")
        return None, None  # Return None for both

# --- Get Bounds Function ---
def get_country_bounds(country_name: str, world_gdf: gpd.GeoDataFrame) -> list | None:
    """
    Finds the bounding box for a given country name in the loaded GeoDataFrame.

    Args:
        country_name (str): The name of the country to find.
        world_gdf (gpd.GeoDataFrame): The pre-loaded world GeoDataFrame.

    Returns:
        list | None: Bounding box [min_lon, min_lat, max_lon, max_lat] or None if not found.
    """
    if world_gdf is None:
        logging.error("World GeoDataFrame is not loaded.")
        return None

    try:
        # Attempt to find the country - case-insensitive matching is safer
        country_match = world_gdf[world_gdf['COUNTRY_NAME'].str.contains(country_name, case=False, na=False)]

        if country_match.empty:
            logging.warning(f"Country '{country_name}' not found in shapefile.")
            return None
        elif len(country_match) > 1:
            logging.warning(f"Multiple matches found for '{country_name}'. Using the first one: {country_match['COUNTRY_NAME'].iloc[0]}")
            country_geom = country_match.iloc[0].geometry
        else:
            country_geom = country_match.iloc[0].geometry

        # Get the bounding box tuple (minx, miny, maxx, maxy)
        bounds = country_geom.bounds

        # Access tuple elements by integer index, not string key
        bounds_list = [bounds[0], bounds[1], bounds[2], bounds[3]]
        logging.info(f"Found bounds for '{country_name}': {bounds_list}")
        return bounds_list

    except Exception as e:
        logging.error(f"Error finding bounds for country '{country_name}': {e}", exc_info=True)
        return None