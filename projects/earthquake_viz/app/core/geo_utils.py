import geopandas as gpd
import pandas as pd
import streamlit as st
import logging
import os
from typing import Dict, List, Tuple, Optional

# --- File Paths ---
# Shapefile for country boundaries and names recognized by the UI
WORLD_SHP_PATH = "data/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
# Shapefile for state/province boundaries (needed for state-level spatial filtering if desired)
# Consider adding the 10m admin 1 shapefile path if state-specific geometry filtering is needed later.
# ADMIN1_SHP_PATH = "data/shapefiles/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp"

# GeoNames Files
ADMIN1_CODES_FILE = "data/geonames/admin1CodesASCII.txt"
CITY_FILE_PATH = "data/geonames/cities500.txt"
COUNTRY_CODES_FILE = "data/geonames/countryInfo.txt" # Provides Country Name -> ISO Code mapping

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------------------------------------------------------
# 🌍 COUNTRY SHAPEFILE AND BOUNDS (Using Natural Earth for consistent names)
# -----------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_world_shapefile(shapefile_path: str = WORLD_SHP_PATH) -> Tuple[Optional[gpd.GeoDataFrame], Optional[List[str]]]:
    """
    Loads the world country shapefile (Natural Earth) used for UI selection
    and bounding box retrieval.
    Returns:
        Tuple[Optional[gpd.GeoDataFrame], Optional[List[str]]]:
            GeoDataFrame and sorted list of country names from the shapefile.
    """
    if not os.path.exists(shapefile_path):
        st.error(f"Country shapefile not found: {shapefile_path}")
        logging.error(f"Country shapefile not found: {shapefile_path}")
        return None, None
    try:
        gdf = gpd.read_file(shapefile_path)
        # --- Determine the primary country name column ---
        # Prioritize 'ADMIN', then 'NAME_EN', 'NAME', 'SOVEREIGNT' etc. Adjust if needed.
        name_col_candidates = ['ADMIN', 'NAME_EN', 'NAME', 'SOVEREIGNT', 'NAME_LONG']
        name_col = next((col for col in name_col_candidates if col in gdf.columns), None)

        if not name_col:
            st.error(f"Could not find a suitable country name column in shapefile: {shapefile_path}")
            logging.error(f"Could not find a suitable country name column in shapefile: {shapefile_path}")
            return None, None

        # Use a consistent internal column name
        gdf['NE_COUNTRY_NAME'] = gdf[name_col]
        # Ensure NaN names are handled (e.g., fill with a placeholder or filter out)
        gdf.dropna(subset=['NE_COUNTRY_NAME'], inplace=True)
        country_list = sorted(gdf['NE_COUNTRY_NAME'].unique().tolist())
        logging.info(f"Loaded world shapefile. Found {len(country_list)} countries using column '{name_col}'.")
        # Keep only necessary columns to save memory
        return gdf[['NE_COUNTRY_NAME', 'geometry']], country_list
    except Exception as e:
        st.error(f"Error loading country shapefile: {e}")
        logging.error(f"Error loading country shapefile: {e}", exc_info=True)
        return None, None

def get_country_bounds(country_name: str, world_gdf: gpd.GeoDataFrame) -> Optional[List[float]]:
    """
    Returns bounding box [min_lon, min_lat, max_lon, max_lat] for a given country
    using the Natural Earth GeoDataFrame.
    """
    if world_gdf is None or world_gdf.empty:
        logging.warning("World GeoDataFrame is not available for getting country bounds.")
        return None

    # Use exact match on the consistent internal column name
    match = world_gdf[world_gdf['NE_COUNTRY_NAME'] == country_name]
    if match.empty:
        logging.warning(f"Could not find exact match for country '{country_name}' in world_gdf.")
        return None
    if len(match) > 1:
         logging.warning(f"Found multiple matches for country '{country_name}', using the first one.")

    try:
        geometry = match.iloc[0].geometry
        bounds = geometry.bounds # (minx, miny, maxx, maxy) -> (min_lon, min_lat, max_lon, max_lat)
        return [bounds[0], bounds[1], bounds[2], bounds[3]]
    except Exception as e:
        logging.error(f"Error getting bounds for country '{country_name}': {e}", exc_info=True)
        return None

# -----------------------------------------------------------------------------
# ⚙️ GEONAMES DATA LOADING & MAPPINGS
# -----------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_country_name_to_iso_mapping() -> Dict[str, str]:
    """
    Loads mapping from country name (as found in countryInfo.txt) to ISO 3166-1 alpha-2 code.
    """
    mapping = {}
    if not os.path.exists(COUNTRY_CODES_FILE):
        st.warning(f"GeoNames country info file not found: {COUNTRY_CODES_FILE}")
        logging.warning(f"GeoNames country info file not found: {COUNTRY_CODES_FILE}")
        return mapping

    try:
        # Skip comment lines, handle potential parsing issues
        df_info = pd.read_csv(
            COUNTRY_CODES_FILE,
            sep='\t',
            comment='#',
            header=None,
            usecols=[0, 4], # ISO code, Country Name
            names=['ISO', 'Country'],
            dtype=str
        )
        # Create mapping: Country Name -> ISO Code
        # Handle potential duplicates if any, maybe log warning
        mapping = dict(zip(df_info['Country'], df_info['ISO']))
        logging.info(f"Loaded {len(mapping)} country name to ISO code mappings.")

        # --- Crucial Normalization Step ---
        # Add overrides to map Natural Earth names (from shapefile) to GeoNames names if they differ
        # This mapping is KEY to linking UI selection -> ISO code -> GeoNames data
        # Example: Natural Earth might use 'United States', GeoNames 'United States of America'
        # You might need to inspect both datasets to build this override map accurately.
        ne_to_geonames_overrides = {
            "United States": "United States", # Example if NE uses 'United States' and countryInfo.txt uses it too
            "Russian Federation": "Russia", # Example if NE uses 'Russian Federation' and countryInfo.txt uses 'Russia'
            "Republic of Korea": "South Korea",
            "Democratic People's Republic of Korea": "North Korea",
            "Iran (Islamic Republic of)": "Iran",
            "Syrian Arab Republic": "Syria",
            "Viet Nam": "Vietnam",
            "Czechia": "Czech Republic",
            "Republic of Serbia": "Serbia",
            "The former Yugoslav Republic of Macedonia": "North Macedonia",
            # Add more mappings as needed based on discrepancies found...
        }
        # We need the reverse: Map the names from countryInfo.txt to the ISO code,
        # but store it keyed by the potential Natural Earth name.
        normalized_mapping = {}
        ne_gdf, _ = load_world_shapefile() # Load NE names
        if ne_gdf is not None:
             ne_names = set(ne_gdf['NE_COUNTRY_NAME'])
             for geonames_country, iso_code in mapping.items():
                 # Check if direct match exists in NE names
                 if geonames_country in ne_names:
                      normalized_mapping[geonames_country] = iso_code
                 else:
                      # Check if an override exists for this GeoNames country
                      found_override = False
                      for ne_name, gn_override_name in ne_to_geonames_overrides.items():
                           if gn_override_name == geonames_country and ne_name in ne_names:
                                normalized_mapping[ne_name] = iso_code
                                found_override = True
                                break
                      # if not found_override:
                      #      logging.warning(f"GeoNames country '{geonames_country}' not found directly or via override in Natural Earth names. Skipping.")

        logging.info(f"Created {len(normalized_mapping)} normalized NE Country Name -> ISO code mappings.")
        return normalized_mapping

    except Exception as e:
        st.error(f"Error loading country code mapping: {e}")
        logging.error(f"Error loading country code mapping: {e}", exc_info=True)
        return {}


@st.cache_resource(show_spinner=False)
def load_admin1_data() -> Dict[str, Dict[str, str]]:
    """
    Loads admin1 data from admin1CodesASCII.txt.
    Returns:
        Dict[str, Dict[str, str]]: Nested dictionary: { country_code: { admin1_name: admin1_code } }
    """
    admin1_map: Dict[str, Dict[str, str]] = {}
    if not os.path.exists(ADMIN1_CODES_FILE):
        st.warning(f"GeoNames admin1 codes file not found: {ADMIN1_CODES_FILE}")
        logging.warning(f"GeoNames admin1 codes file not found: {ADMIN1_CODES_FILE}")
        return admin1_map

    try:
        with open(ADMIN1_CODES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3: # Need at least code, name, ascii name
                    full_code, name = parts[0], parts[1] # Use the primary 'name' column
                    # code format: CountryCode.Admin1Code (e.g., US.CA)
                    if '.' in full_code:
                        country_code, admin1_code = full_code.split('.', 1)
                        if country_code not in admin1_map:
                            admin1_map[country_code] = {}
                        # Store mapping from name -> code for the specific country
                        # Handle potential duplicate names within a country if necessary (e.g., use name+code as key)
                        if name not in admin1_map[country_code]:
                             admin1_map[country_code][name] = admin1_code
                        # else:
                        #     logging.warning(f"Duplicate admin1 name '{name}' found for country '{country_code}'. Keeping first code '{admin1_map[country_code][name]}'.")

        logging.info(f"Loaded admin1 mappings for {len(admin1_map)} countries.")
        return admin1_map
    except Exception as e:
        st.error(f"Error loading admin1 code mapping: {e}")
        logging.error(f"Error loading admin1 code mapping: {e}", exc_info=True)
        return {}

@st.cache_resource(show_spinner=False)
def load_geonames_cities() -> pd.DataFrame:
    """
    Loads cities500.txt into a Pandas DataFrame.
    """
    if not os.path.exists(CITY_FILE_PATH):
        st.error(f"GeoNames city file not found: {CITY_FILE_PATH}")
        logging.error(f"GeoNames city file not found: {CITY_FILE_PATH}")
        return pd.DataFrame()

    # Define columns based on GeoNames Readme for the main 'geoname' table
    columns = [
        "geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude",
        "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code",
        "admin3_code", "admin4_code", "population", "elevation", "dem",
        "timezone", "modification_date"
    ]
    try:
        df = pd.read_csv(
            CITY_FILE_PATH,
            sep='\t',
            header=None,
            names=columns,
            dtype={ # Specify types to avoid issues, esp for codes and potentially large pop
                'geonameid': int,
                'name': str,
                'asciiname': str,
                'alternatenames': str,
                'latitude': float,
                'longitude': float,
                'feature_class': str,
                'feature_code': str,
                'country_code': str, # Keep as string (ISO codes)
                'cc2': str,
                'admin1_code': str, # Keep as string (can be numeric or alphanumeric)
                'admin2_code': str,
                'admin3_code': str,
                'admin4_code': str,
                'population': pd.Int64Dtype(), # Use nullable integer for population
                'elevation': pd.Int64Dtype(), # Use nullable integer
                'dem': pd.Int64Dtype(),      # Use nullable integer
                'timezone': str,
                'modification_date': str
            },
            low_memory=False, # Can help with mixed types if dtype specification isn't perfect
            encoding='utf-8'
        )
        logging.info(f"Loaded {len(df)} records from GeoNames city file.")
        # Keep only necessary columns? Maybe filter PPL* feature codes?
        # df = df[df['feature_class'] == 'P'] # Optional: Filter only populated places
        return df[['name', 'latitude', 'longitude', 'country_code', 'admin1_code', 'population']] # Keep essential columns
    except Exception as e:
        st.error(f"Error loading GeoNames city file: {e}")
        logging.error(f"Error loading GeoNames city file: {e}", exc_info=True)
        return pd.DataFrame()

# -----------------------------------------------------------------------------
# 🔍 HIERARCHICAL LOOKUP FUNCTIONS
# -----------------------------------------------------------------------------

# Cached dataframes/dicts from above loaders
# These calls ensure data is loaded only once due to @st.cache_resource
WORLD_GDF, NE_COUNTRY_LIST = load_world_shapefile()
NE_NAME_TO_ISO_MAP = load_country_name_to_iso_mapping()
ADMIN1_DATA = load_admin1_data() # {country_iso: {admin1_name: admin1_code}}
CITIES_DF = load_geonames_cities()


def get_iso_code_for_country(ne_country_name: str) -> Optional[str]:
    """Gets the ISO 3166-1 alpha-2 code for a Natural Earth country name."""
    return NE_NAME_TO_ISO_MAP.get(ne_country_name)

# Use @st.cache_data for functions that perform filtering/lookups on cached data
@st.cache_data(show_spinner=False)
def get_admin1_names_for_country(country_iso_code: str) -> List[str]:
    """Gets a sorted list of Admin1 names (states/provinces) for a given country ISO code."""
    if not country_iso_code or country_iso_code not in ADMIN1_DATA:
        return []
    # Return sorted list of names (keys of the inner dict)
    return sorted(list(ADMIN1_DATA[country_iso_code].keys()))

@st.cache_data(show_spinner=False)
def get_admin1_code(country_iso_code: str, admin1_name: str) -> Optional[str]:
    """Gets the Admin1 code for a given country ISO code and Admin1 name."""
    if not country_iso_code or country_iso_code not in ADMIN1_DATA:
        return None
    # Lookup the name in the inner dictionary for the country
    return ADMIN1_DATA[country_iso_code].get(admin1_name)


@st.cache_data(show_spinner=False)
def get_cities_for_admin1(country_iso_code: str, admin1_code: str) -> List[str]:
    """Gets a sorted list of city names for a given country ISO and admin1 code."""
    if CITIES_DF.empty or not country_iso_code or admin1_code is None: # admin1_code can be '00' etc.
        return []
    # Filter the global cities DataFrame
    filtered_cities = CITIES_DF[
        (CITIES_DF['country_code'] == country_iso_code) &
        (CITIES_DF['admin1_code'] == admin1_code)
    ]
    if filtered_cities.empty:
        return []
    # Return sorted unique city names, perhaps sort by population descending?
    # return sorted(filtered_cities['name'].unique().tolist())
    return filtered_cities.sort_values('population', ascending=False)['name'].unique().tolist()


@st.cache_data(show_spinner=False)
def get_city_coordinates(country_iso_code: str, admin1_code: str, city_name: str) -> Optional[Tuple[float, float]]:
    """Gets (latitude, longitude) for a specific city."""
    if CITIES_DF.empty or not country_iso_code or admin1_code is None or not city_name:
        return None
    # Filter DataFrame for the specific city
    filtered_city = CITIES_DF[
        (CITIES_DF['country_code'] == country_iso_code) &
        (CITIES_DF['admin1_code'] == admin1_code) &
        (CITIES_DF['name'] == city_name) # Use exact name match from dropdown
    ]
    if filtered_city.empty:
        logging.warning(f"Could not find coordinates for city: {city_name}, {admin1_code}, {country_iso_code}")
        return None
    if len(filtered_city) > 1:
         logging.warning(f"Multiple coordinate entries found for city: {city_name}, {admin1_code}, {country_iso_code}. Using first.")

    # Extract latitude and longitude
    lat = filtered_city.iloc[0]['latitude']
    lon = filtered_city.iloc[0]['longitude']
    return float(lat), float(lon)