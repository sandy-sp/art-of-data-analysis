# app/core/geo_utils.py
import geopandas as gpd
import pandas as pd
import streamlit as st
import logging
import os
from typing import Dict, List, Tuple, Optional, Set

# --- File Paths ---
WORLD_SHP_PATH = "data/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
ADMIN1_CODES_FILE = "data/geonames/admin1CodesASCII.txt"
CITY_FILE_PATH = "data/geonames/cities500.txt"
COUNTRY_CODES_FILE = "data/geonames/countryInfo.txt" # Make sure this file exists [cite: 1]
# --- Add path for Admin 1 shapefile ---
ADMIN1_SHP_PATH = "data/shapefiles/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------------------------------------------------------
# 🌍 DATA LOADING FUNCTIONS (Called from main.py)
# -----------------------------------------------------------------------------

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

        iso_col_candidates = ['ISO_A2', 'ADM0_A2', 'ISO_A2_EH']
        iso_col = next((col for col in iso_col_candidates if col in gdf.columns), None)
        if not iso_col:
            st.error(f"Could not find a suitable ISO column in shapefile: {shapefile_path}")
            logging.error(f"Could not find a suitable ISO column in shapefile: {shapefile_path}")
            return None, None

        gdf['NE_COUNTRY_NAME'] = gdf[name_col]
        gdf.dropna(subset=['NE_COUNTRY_NAME', iso_col], inplace=True)
        country_list = sorted(gdf['NE_COUNTRY_NAME'].unique().tolist())
        logging.info(f"Loaded world shapefile. Found {len(country_list)} countries using name column '{name_col}' and ISO column '{iso_col}'.")
        return gdf[['NE_COUNTRY_NAME', iso_col, 'geometry']].rename(columns={iso_col: 'ISO_A2'}), country_list
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

@st.cache_resource(show_spinner="Loading GeoNames ISO codes...")
def load_geonames_iso_codes() -> Set[str]:
    """ Parses countryInfo.txt to get a set of valid ISO A2 codes. """
    iso_codes: Set[str] = set()
    if not os.path.exists(COUNTRY_CODES_FILE):
        st.error(f"CRITICAL: Required GeoNames country info file not found at: {COUNTRY_CODES_FILE}")
        logging.error(f"CRITICAL: Required file not found: {COUNTRY_CODES_FILE}")
        return iso_codes

    try:
        df_info = pd.read_csv(
            COUNTRY_CODES_FILE, sep='\t', comment='#', header=None,
            usecols=[0], names=['ISO'], dtype=str, encoding='utf-8', on_bad_lines='warn'
        )
        if not df_info.empty:
            iso_codes = set(df_info['ISO'].unique())
            logging.info(f"Loaded {len(iso_codes)} unique ISO A2 codes from {COUNTRY_CODES_FILE}.")
        else:
            logging.error(f"Parsed {COUNTRY_CODES_FILE} but resulted in an empty DataFrame.")
            st.error(f"Parsed country info file ('{COUNTRY_CODES_FILE}') but found no ISO codes.")
        return iso_codes
    except Exception as e:
        st.error(f"CRITICAL: Failed to parse ISO codes from {COUNTRY_CODES_FILE}. Error: {e}")
        logging.error(f"CRITICAL: Error parsing ISO codes from {COUNTRY_CODES_FILE}", exc_info=True)
        return iso_codes

# --- NEW: Function to load Admin 1 shapefile ---
@st.cache_resource(show_spinner="Loading state/province boundaries...")
def load_admin1_shapefile(shapefile_path: str = ADMIN1_SHP_PATH) -> Optional[gpd.GeoDataFrame]:
    if not os.path.exists(shapefile_path):
        st.warning(f"Admin 1 shapefile not found: {shapefile_path}. State/Province map zooming disabled.")
        logging.warning(f"Admin 1 shapefile not found: {shapefile_path}")
        return None
    try:
        gdf = gpd.read_file(shapefile_path)
        logging.info(f"Loaded Admin 1 shapefile with {len(gdf)} features. Columns: {gdf.columns.tolist()}")
        iso_col = 'iso_a2' if 'iso_a2' in gdf.columns else None
        name_col = 'name' if 'name' in gdf.columns else None
        if not iso_col or not name_col:
            st.warning(f"Admin 1 shapefile missing required columns (ISO A2 or Name). State zooming might fail.")
            logging.warning(f"Admin 1 shapefile missing required columns. ISO Col: {iso_col}, Name Col: {name_col}")
            return gdf
        return gdf[['geometry', iso_col, name_col]].rename(columns={iso_col: 'ISO_A2', name_col: 'ADMIN1_NAME'})
    except Exception as e:
        st.error(f"Error loading Admin 1 shapefile: {e}")
        logging.error(f"Error loading Admin 1 shapefile: {e}", exc_info=True)
        return None

# -----------------------------------------------------------------------------
# 🔍 HIERARCHICAL LOOKUP FUNCTIONS (Accept data as arguments)
# -----------------------------------------------------------------------------

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

# --- NEW: Function to get State/Province bounds ---
def get_state_bounds(country_iso_code: str, state_name: str, admin1_gdf: Optional[gpd.GeoDataFrame]) -> Optional[List[float]]:
    if admin1_gdf is None or admin1_gdf.empty:
        logging.warning("Admin 1 GeoDataFrame is not available for getting state bounds.")
        return None
    if 'ISO_A2' not in admin1_gdf.columns or 'ADMIN1_NAME' not in admin1_gdf.columns:
        logging.warning(f"Required columns ('ISO_A2', 'ADMIN1_NAME') not found in Admin 1 GDF. Columns: {admin1_gdf.columns}")
        return None
    match = admin1_gdf[
        (admin1_gdf['ISO_A2'].astype(str) == str(country_iso_code)) &
        (admin1_gdf['ADMIN1_NAME'].astype(str).str.lower() == str(state_name).lower())
    ]
    if match.empty:
        logging.warning(f"Could not find exact match for state: '{state_name}' in country '{country_iso_code}' within Admin 1 GDF.")
        return None
    if len(match) > 1:
        logging.warning(f"Found multiple boundary matches for state '{state_name}', country '{country_iso_code}'. Using the first one.")
    try:
        geometry = match.iloc[0].geometry
        bounds = geometry.bounds
        logging.info(f"Found bounds for state '{state_name}', country '{country_iso_code}': {bounds}")
        return [bounds[0], bounds[1], bounds[2], bounds[3]]
    except Exception as e:
        logging.error(f"Error getting bounds for state '{state_name}', country '{country_iso_code}': {e}", exc_info=True)
        return None