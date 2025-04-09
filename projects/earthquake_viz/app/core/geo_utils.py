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
COUNTRY_CODES_FILE = "data/geonames/countryInfo.txt"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------------------------------------------------------
# 🌍 DATA LOADING FUNCTIONS (Called from main.py)
# -----------------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading country boundaries...") # Add spinner message
def load_world_shapefile(shapefile_path: str = WORLD_SHP_PATH) -> Tuple[Optional[gpd.GeoDataFrame], Optional[List[str]]]:
    """Loads the world country shapefile."""
    # ... (keep the inside logic the same as before) ...
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
        # Keep only necessary columns
        return gdf[['NE_COUNTRY_NAME', 'geometry', name_col]], country_list # Keep original name col if needed for mapping
    except Exception as e:
        st.error(f"Error loading country shapefile: {e}")
        logging.error(f"Error loading country shapefile: {e}", exc_info=True)
        return None, None


# Pass world_gdf explicitly if needed for normalization logic
@st.cache_resource(show_spinner="Loading country code mappings...")
def load_country_name_to_iso_mapping(world_gdf: Optional[gpd.GeoDataFrame]) -> Dict[str, str]:
    """Loads mapping from Natural Earth country name to ISO code."""
    # ... (keep the inside parsing logic the same, BUT ensure normalization uses the passed world_gdf) ...
    mapping = {}
    if not os.path.exists(COUNTRY_CODES_FILE):
        st.warning(f"GeoNames country info file not found: {COUNTRY_CODES_FILE}")
        logging.warning(f"GeoNames country info file not found: {COUNTRY_CODES_FILE}")
        return mapping

    try:
        df_info = pd.read_csv(
            COUNTRY_CODES_FILE, sep='\t', comment='#', header=None,
            usecols=[0, 4], names=['ISO', 'Country'], dtype=str
        )
        geonames_mapping = dict(zip(df_info['Country'], df_info['ISO']))
        logging.info(f"Loaded {len(geonames_mapping)} raw country name to ISO code mappings.")

        # Normalization logic requires world_gdf
        normalized_mapping = {}
        if world_gdf is not None and not world_gdf.empty:
            ne_names = set(world_gdf['NE_COUNTRY_NAME'])
            # Define overrides mapping NE name -> GeoNames name
            ne_to_geonames_overrides = {
                "United States": "United States",
                "Russian Federation": "Russia",
                "Republic of Korea": "South Korea",
                "Democratic People's Republic of Korea": "North Korea",
                "Iran (Islamic Republic of)": "Iran",
                "Syrian Arab Republic": "Syria",
                "Viet Nam": "Vietnam",
                "Czechia": "Czech Republic",
                 "Republic of Serbia": "Serbia",
                # Add more overrides as identified
            }
            # Build the final map keyed by NE name
            for ne_name in ne_names:
                # Direct match in overrides?
                if ne_name in ne_to_geonames_overrides:
                     geonames_country = ne_to_geonames_overrides[ne_name]
                     iso_code = geonames_mapping.get(geonames_country)
                     if iso_code:
                          normalized_mapping[ne_name] = iso_code
                     # else: log missing geonames name from override
                # Direct match in geonames_mapping keys?
                elif ne_name in geonames_mapping:
                     normalized_mapping[ne_name] = geonames_mapping[ne_name]
                # else: log NE name not mapped

            logging.info(f"Created {len(normalized_mapping)} normalized NE Country Name -> ISO code mappings.")
        else:
             logging.warning("World GDF not provided for country name normalization. Mapping may be incomplete.")
             # Fallback: return raw geonames mapping? Or empty? Prefer empty if normalization is essential.
             # return geonames_mapping

        return normalized_mapping

    except Exception as e:
        st.error(f"Error loading country code mapping: {e}")
        logging.error(f"Error loading country code mapping: {e}", exc_info=True)
        return {}


@st.cache_resource(show_spinner="Loading admin level 1 data...")
def load_admin1_data() -> Dict[str, Dict[str, str]]:
    """Loads admin1 data from admin1CodesASCII.txt."""
    # ... (keep the inside logic the same) ...
    admin1_map: Dict[str, Dict[str, str]] = {}
    if not os.path.exists(ADMIN1_CODES_FILE):
        st.warning(f"GeoNames admin1 codes file not found: {ADMIN1_CODES_FILE}")
        logging.warning(f"GeoNames admin1 codes file not found: {ADMIN1_CODES_FILE}")
        return admin1_map
    try:
        with open(ADMIN1_CODES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2: # Use name (parts[1]), not ascii name (parts[2]) for keys
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
    """Loads cities500.txt into a Pandas DataFrame."""
    # ... (keep the inside logic the same) ...
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
            dtype={ # Simplified dtypes
                'latitude': float, 'longitude': float, 'population': pd.Int64Dtype(),
                'country_code': str, 'admin1_code': str, 'name': str
            },
            usecols=['name', 'latitude', 'longitude', 'country_code', 'admin1_code', 'population'], # Only load needed cols
            low_memory=False, encoding='utf-8'
        )
        logging.info(f"Loaded {len(df)} records from GeoNames city file.")
        return df
    except Exception as e:
        st.error(f"Error loading GeoNames city file: {e}")
        logging.error(f"Error loading GeoNames city file: {e}", exc_info=True)
        return pd.DataFrame()

# --- REMOVE MODULE-LEVEL DATA LOADING ---
# WORLD_GDF, NE_COUNTRY_LIST = load_world_shapefile() # REMOVE
# NE_NAME_TO_ISO_MAP = load_country_name_to_iso_mapping() # REMOVE
# ADMIN1_DATA = load_admin1_data() # REMOVE
# CITIES_DF = load_geonames_cities() # REMOVE
# -----------------------------------------


# -----------------------------------------------------------------------------
# 🔍 HIERARCHICAL LOOKUP FUNCTIONS (Now accept data as arguments)
# -----------------------------------------------------------------------------

# These functions no longer rely on global variables but get data passed in.
# Use @st.cache_data if the inputs (codes, names) and the underlying dataframes are hashable
# and the computation is expensive.

def get_iso_code_for_country(ne_country_name: str, ne_name_to_iso_map: Dict[str, str]) -> Optional[str]:
    """Gets the ISO code from the pre-loaded mapping."""
    return ne_name_to_iso_map.get(ne_country_name)

def get_admin1_names_for_country(country_iso_code: str, admin1_data: Dict[str, Dict[str, str]]) -> List[str]:
    """Gets Admin1 names from the pre-loaded admin1 data."""
    if not country_iso_code or country_iso_code not in admin1_data:
        return []
    return sorted(list(admin1_data[country_iso_code].keys()))

def get_admin1_code(country_iso_code: str, admin1_name: str, admin1_data: Dict[str, Dict[str, str]]) -> Optional[str]:
    """Gets Admin1 code from the pre-loaded admin1 data."""
    if not country_iso_code or country_iso_code not in admin1_data:
        return None
    return admin1_data[country_iso_code].get(admin1_name)

# Caching might still be useful here if filtering the large cities_df is slow
@st.cache_data(show_spinner=False)
def get_cities_for_admin1(country_iso_code: str, admin1_code: str, cities_df: pd.DataFrame) -> List[str]:
    """Gets city names by filtering the pre-loaded cities DataFrame."""
    if cities_df.empty or not country_iso_code or admin1_code is None:
        return []
    filtered_cities = cities_df[
        (cities_df['country_code'] == country_iso_code) &
        (cities_df['admin1_code'] == admin1_code)
    ]
    if filtered_cities.empty:
        return []
    return filtered_cities.sort_values('population', ascending=False)['name'].unique().tolist()

@st.cache_data(show_spinner=False)
def get_city_coordinates(country_iso_code: str, admin1_code: str, city_name: str, cities_df: pd.DataFrame) -> Optional[Tuple[float, float]]:
    """Gets city coordinates by filtering the pre-loaded cities DataFrame."""
    if cities_df.empty or not country_iso_code or admin1_code is None or not city_name:
        return None
    filtered_city = cities_df[
        (cities_df['country_code'] == country_iso_code) &
        (cities_df['admin1_code'] == admin1_code) &
        (cities_df['name'] == city_name)
    ]
    if filtered_city.empty:
        logging.warning(f"Could not find coordinates for city: {city_name}, {admin1_code}, {country_iso_code}")
        return None
    if len(filtered_city) > 1:
         logging.warning(f"Multiple coordinate entries found for city: {city_name}, {admin1_code}, {country_iso_code}. Using first.")
    lat = filtered_city.iloc[0]['latitude']
    lon = filtered_city.iloc[0]['longitude']
    return float(lat), float(lon)

# This function still directly uses the passed GDF
def get_country_bounds(country_name: str, world_gdf: Optional[gpd.GeoDataFrame]) -> Optional[List[float]]:
    """Gets country bounds from the pre-loaded world GeoDataFrame."""
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