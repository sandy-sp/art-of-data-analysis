# app/core/geo_utils.py
import geopandas as gpd
import pandas as pd
import streamlit as st
import logging
import os
from typing import Dict, List, Tuple, Optional

# --- File Paths ---
WORLD_SHP_PATH = "data/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
ADMIN1_CODES_FILE = "data/geonames/admin1CodesASCII.txt"
CITY_FILE_PATH = "data/geonames/cities500.txt"
COUNTRY_CODES_FILE = "data/geonames/countryInfo.txt" # Make sure this file exists [cite: 1]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------------------------------------------------------
# 🌍 DATA LOADING FUNCTIONS (Called from main.py)
# -----------------------------------------------------------------------------

# ... load_world_shapefile, load_admin1_data, load_geonames_cities remain the same ...
# ... from the previous correct version ...

@st.cache_resource(show_spinner="Loading country boundaries...")
def load_world_shapefile(shapefile_path: str = WORLD_SHP_PATH) -> Tuple[Optional[gpd.GeoDataFrame], Optional[List[str]]]:
    if not os.path.exists(shapefile_path):
        st.error(f"Country shapefile not found: {shapefile_path}")
        logging.error(f"Country shapefile not found: {shapefile_path}")
        return None, None
    try:
        gdf = gpd.read_file(shapefile_path)
        name_col_candidates = ['ADMIN', 'NAME_EN', 'NAME', 'SOVEREIGNT', 'NAME_LONG']
        name_col = next((col for col in name_col_candidates if col in gdf.columns), None)

        if not name_col:
            st.error(f"Could not find a suitable country name column in shapefile: {shapefile_path}")
            logging.error(f"Could not find a suitable country name column in shapefile: {shapefile_path}")
            return None, None

        gdf['NE_COUNTRY_NAME'] = gdf[name_col]
        gdf.dropna(subset=['NE_COUNTRY_NAME'], inplace=True)
        country_list = sorted(gdf['NE_COUNTRY_NAME'].unique().tolist())
        logging.info(f"Loaded world shapefile. Found {len(country_list)} countries using column '{name_col}'.")
        return gdf[['NE_COUNTRY_NAME', 'geometry', name_col]], country_list
    except Exception as e:
        st.error(f"Error loading country shapefile: {e}")
        logging.error(f"Error loading country shapefile: {e}", exc_info=True)
        return None, None

@st.cache_resource(show_spinner="Loading admin level 1 data...")
def load_admin1_data() -> Dict[str, Dict[str, str]]:
    admin1_map: Dict[str, Dict[str, str]] = {}
    if not os.path.exists(ADMIN1_CODES_FILE):
        st.warning(f"GeoNames admin1 codes file not found: {ADMIN1_CODES_FILE}")
        logging.warning(f"GeoNames admin1 codes file not found: {ADMIN1_CODES_FILE}")
        return admin1_map
    try:
        with open(ADMIN1_CODES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    full_code, name = parts[0], parts[1]
                    if '.' in full_code:
                        country_code, admin1_code = full_code.split('.', 1)
                        if country_code not in admin1_map:
                            admin1_map[country_code] = {}
                        if name not in admin1_map[country_code]:
                             admin1_map[country_code][name] = admin1_code
        logging.info(f"Loaded admin1 mappings for {len(admin1_map)} countries.")
        return admin1_map
    except Exception as e:
        st.error(f"Error loading admin1 code mapping: {e}")
        logging.error(f"Error loading admin1 code mapping: {e}", exc_info=True)
        return {}

@st.cache_resource(show_spinner="Loading city data...")
def load_geonames_cities() -> pd.DataFrame:
    if not os.path.exists(CITY_FILE_PATH):
        st.error(f"GeoNames city file not found: {CITY_FILE_PATH}")
        logging.error(f"GeoNames city file not found: {CITY_FILE_PATH}")
        return pd.DataFrame()
    columns = [
        "geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude",
        "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code",
        "admin3_code", "admin4_code", "population", "elevation", "dem",
        "timezone", "modification_date"
    ]
    try:
        df = pd.read_csv(
            CITY_FILE_PATH, sep='\t', header=None, names=columns,
            dtype={ 'latitude': float, 'longitude': float, 'population': pd.Int64Dtype(),
                     'country_code': str, 'admin1_code': str, 'name': str },
            usecols=['name', 'latitude', 'longitude', 'country_code', 'admin1_code', 'population'],
            low_memory=False, encoding='utf-8'
        )
        logging.info(f"Loaded {len(df)} records from GeoNames city file.")
        return df
    except Exception as e:
        st.error(f"Error loading GeoNames city file: {e}")
        logging.error(f"Error loading GeoNames city file: {e}", exc_info=True)
        return pd.DataFrame()


# --- Updated Country Name to ISO Mapping Function ---
@st.cache_resource(show_spinner="Loading country code mappings...")
def load_country_name_to_iso_mapping(_world_gdf: Optional[gpd.GeoDataFrame]) -> Dict[str, str]:
    """Loads mapping from Natural Earth country name to ISO code, handling parsing errors."""
    mapping: Dict[str, str] = {} # Initialize as empty dict

    # 1. Check for dependent GeoDataFrame first
    if _world_gdf is None or _world_gdf.empty:
         st.warning("World GeoDataFrame not available for country name normalization. Cannot create mapping.")
         logging.warning("World GDF is None or empty in load_country_name_to_iso_mapping.")
         return mapping # Return empty if dependent data is missing

    # 2. Check if the target file exists
    if not os.path.exists(COUNTRY_CODES_FILE):
        st.error(f"CRITICAL: Required GeoNames country info file not found at: {COUNTRY_CODES_FILE}")
        logging.error(f"CRITICAL: Required file not found: {COUNTRY_CODES_FILE}")
        return mapping # Return empty dict if file missing

    # 3. Attempt to parse the file
    df_info = None
    try:
        df_info = pd.read_csv(
            COUNTRY_CODES_FILE,
            sep='\t',
            comment='#',          # Ignore comment lines [cite: 1]
            header=None,          # No header row in the data section [cite: 9]
            usecols=[0, 4],       # Column 0: ISO, Column 4: Country Name [cite: 9]
            names=['ISO', 'Country'], # Assign names
            dtype=str,            # Treat data as string
            encoding='utf-8',     # Explicitly use UTF-8
            on_bad_lines='warn'   # Warn about lines that can't be parsed instead of erroring immediately
        )
        # Check if parsing resulted in an empty DataFrame
        if df_info.empty:
            st.error(f"CRITICAL: Parsed country info file ('{COUNTRY_CODES_FILE}') but resulted in an empty DataFrame. Check file content/format.")
            logging.error(f"CRITICAL: Parsed {COUNTRY_CODES_FILE} resulted in an empty DataFrame.")
            return mapping # Return empty dict

        logging.info(f"Successfully parsed {COUNTRY_CODES_FILE}. Shape: {df_info.shape}")
        # Optional: Log head for detailed debug if needed
        # logging.debug(f"Head of parsed country info:\n{df_info.head()}")

    except pd.errors.EmptyDataError:
        st.error(f"CRITICAL: GeoNames country info file is empty: {COUNTRY_CODES_FILE}")
        logging.error(f"CRITICAL: pd.errors.EmptyDataError for {COUNTRY_CODES_FILE}")
        return mapping
    except Exception as e:
        st.error(f"CRITICAL: Failed to parse GeoNames country info file: {COUNTRY_CODES_FILE}. Error: {e}")
        logging.error(f"CRITICAL: Error parsing {COUNTRY_CODES_FILE} with pandas", exc_info=True)
        return mapping # Return empty dict on other parsing failures

    # 4. Proceed with mapping creation and normalization if parsing was successful
    try:
        # Create initial mapping from GeoNames Name -> ISO Code
        geonames_mapping = dict(zip(df_info['Country'], df_info['ISO']))
        if not geonames_mapping:
             logging.error("Created an empty geonames_mapping dictionary after parsing. Check parsing logic/file.")
             return {} # Return empty if the dict creation failed

        logging.info(f"Loaded {len(geonames_mapping)} raw country name to ISO code mappings from file.")

        # --- Normalization Step ---
        # (Using the _world_gdf passed as argument)
        normalized_mapping = {}
        ne_names = set(_world_gdf['NE_COUNTRY_NAME'])

        # --- !!! UPDATED DICTIONARY !!! ---
        # Define overrides mapping: ShapefileName -> GeoNames_countryInfo.txt_Name
        # Keys are names found in shapefile's 'ADMIN' col, Values are names in countryInfo.txt 'Country' col
        ne_to_geonames_overrides = {
            "United States of America": "United States",
            "South Korea": "Korea, Republic of",
            "North Korea": "Korea, Democratic People's Republic of",
            "Republic of Serbia": "Serbia",
            "The Bahamas": "Bahamas",
            "Netherlands": "The Netherlands",
            "Vietnam": "Viet Nam",
            "eSwatini": "Eswatini",
            "Palestine": "Palestinian Territory",
            "Russia": "Russian Federation",
            "Iran": "Iran, Islamic Republic of",
            "Syria": "Syrian Arab Republic",
            "Czechia": "Czech Republic",
            "Macedonia": "North Macedonia",
            "United Kingdom": "United Kingdom",
        }

        # Build the final map keyed by NE name
        mapped_count = 0
        unmapped_ne_names = []
        for ne_name in ne_names:
            geonames_name_to_lookup = ne_name # Default assumption
            # Check if an override exists for this NE name
            if ne_name in ne_to_geonames_overrides:
                geonames_name_to_lookup = ne_to_geonames_overrides[ne_name]

            # Find the ISO code using the potentially overridden GeoNames name
            iso_code = geonames_mapping.get(geonames_name_to_lookup)
            if iso_code:
                normalized_mapping[ne_name] = iso_code
                mapped_count += 1
            else:
                # Log unmapped Natural Earth names only once for clarity
                unmapped_ne_names.append(ne_name)

        logging.info(f"Created {len(normalized_mapping)} final NE Country Name -> ISO code mappings after normalization.")
        if unmapped_ne_names:
             logging.warning(f"Could not map {len(unmapped_ne_names)} NE country names to ISO codes. Examples: {unmapped_ne_names[:10]}") # Log first 10 examples

        return normalized_mapping # Return the result of normalization

    except Exception as e:
        # Catch errors during the mapping/normalization phase
        st.error(f"Error during country name normalization/mapping creation: {e}")
        logging.error("Error during country name normalization/mapping creation", exc_info=True)
        return {} # Return empty on normalization error


# -----------------------------------------------------------------------------
# 🔍 HIERARCHICAL LOOKUP FUNCTIONS (Accept data as arguments)
# -----------------------------------------------------------------------------
# ... (These functions remain the same as the previous correct version) ...

def get_iso_code_for_country(ne_country_name: str, ne_name_to_iso_map: Dict[str, str]) -> Optional[str]:
    return ne_name_to_iso_map.get(ne_country_name)

def get_admin1_names_for_country(country_iso_code: str, admin1_data: Dict[str, Dict[str, str]]) -> List[str]:
    if not country_iso_code or country_iso_code not in admin1_data: return []
    return sorted(list(admin1_data[country_iso_code].keys()))

def get_admin1_code(country_iso_code: str, admin1_name: str, admin1_data: Dict[str, Dict[str, str]]) -> Optional[str]:
    if not country_iso_code or country_iso_code not in admin1_data: return None
    return admin1_data[country_iso_code].get(admin1_name)

@st.cache_data(show_spinner=False)
def get_cities_for_admin1(country_iso_code: str, admin1_code: str, cities_df: pd.DataFrame) -> List[str]:
    if cities_df.empty or not country_iso_code or admin1_code is None: return []
    filtered_cities = cities_df[
        (cities_df['country_code'] == country_iso_code) & (cities_df['admin1_code'] == admin1_code) ]
    if filtered_cities.empty: return []
    return filtered_cities.sort_values('population', ascending=False)['name'].unique().tolist()

@st.cache_data(show_spinner=False)
def get_city_coordinates(country_iso_code: str, admin1_code: str, city_name: str, cities_df: pd.DataFrame) -> Optional[Tuple[float, float]]:
    if cities_df.empty or not country_iso_code or admin1_code is None or not city_name: return None
    filtered_city = cities_df[
        (cities_df['country_code'] == country_iso_code) & (cities_df['admin1_code'] == admin1_code) & (cities_df['name'] == city_name) ]
    if filtered_city.empty:
        logging.warning(f"Could not find coordinates for city: {city_name}, {admin1_code}, {country_iso_code}")
        return None
    if len(filtered_city) > 1:
         logging.warning(f"Multiple coordinate entries found for city: {city_name}, {admin1_code}, {country_iso_code}. Using first.")
    lat = filtered_city.iloc[0]['latitude']
    lon = filtered_city.iloc[0]['longitude']
    return float(lat), float(lon)

def get_country_bounds(country_name: str, world_gdf: Optional[gpd.GeoDataFrame]) -> Optional[List[float]]:
    if world_gdf is None or world_gdf.empty:
        logging.warning("World GeoDataFrame is not available for getting country bounds.")
        return None
    match = world_gdf[world_gdf['NE_COUNTRY_NAME'] == country_name]
    if match.empty:
        logging.warning(f"Could not find exact match for country '{country_name}' in world_gdf.")
        return None
    if len(match) > 1:
         logging.warning(f"Found multiple matches for country '{country_name}', using the first one.")
    try:
        geometry = match.iloc[0].geometry
        bounds = geometry.bounds
        return [bounds[0], bounds[1], bounds[2], bounds[3]]
    except Exception as e:
        logging.error(f"Error getting bounds for country '{country_name}': {e}", exc_info=True)
        return None