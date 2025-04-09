import geopandas as gpd
import pandas as pd
import streamlit as st
import logging
import os

# --- File Paths ---
WORLD_SHP_PATH = "data/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
ADMIN1_CODES_FILE = "data/geonames/admin1CodesASCII.txt"
CITY_FILE_PATH = "data/geonames/cities500.txt"
COUNTRY_CODES_FILE = "data/geonames/countryInfo.txt"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------------------------------------------------------
# 🌍 COUNTRY SHAPEFILE AND BOUNDS
# -----------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_world_shapefile(shapefile_path: str = WORLD_SHP_PATH):
    """Loads the world country shapefile and returns (GeoDataFrame, list of country names)."""
    if not os.path.exists(shapefile_path):
        st.error(f"Country shapefile not found: {shapefile_path}")
        return None, None

    gdf = gpd.read_file(shapefile_path)
    name_col = 'ADMIN'
    if name_col not in gdf.columns:
        fallback = [col for col in gdf.columns if 'NAME' in col.upper()]
        if not fallback:
            st.error("Country name column not found in shapefile.")
            return None, None
        name_col = fallback[0]

    gdf['COUNTRY_NAME'] = gdf[name_col]
    country_list = sorted(gdf['COUNTRY_NAME'].unique().tolist())
    return gdf, country_list

def get_country_bounds(country_name: str, world_gdf: gpd.GeoDataFrame) -> list | None:
    """Returns bounding box [min_lon, min_lat, max_lon, max_lat] for a given country."""
    if world_gdf is None:
        return None

    match = world_gdf[world_gdf['COUNTRY_NAME'].str.contains(country_name, case=False, na=False)]
    if match.empty:
        return None

    geometry = match.iloc[0].geometry
    bounds = geometry.bounds
    return [bounds[0], bounds[1], bounds[2], bounds[3]]


# -----------------------------------------------------------------------------
# 🌐 COUNTRY AND ADMIN1 CODE MAPPING
# -----------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_country_code_mapping() -> dict:
    """Returns mapping from country name → ISO 2-letter code using countryInfo.txt"""
    if not os.path.exists(COUNTRY_CODES_FILE):
        return {}

    df = pd.read_csv(COUNTRY_CODES_FILE, sep='\t', comment='#')
    
    # --- Normalize known mismatches ---
    overrides = {
        "United States of America": "United States",
        "Russia": "Russian Federation",
        "South Korea": "Korea, Republic of",
        "North Korea": "Korea, Democratic People's Republic of",
        "Iran": "Iran, Islamic Republic of",
        "Syria": "Syrian Arab Republic",
        "Vietnam": "Viet Nam"
    }

    for user_label, canonical_label in overrides.items():
        df.loc[df["Country"] == canonical_label, "Country"] = user_label

    return dict(zip(df["Country"], df["ISO"]))

@st.cache_resource(show_spinner=False)
def load_admin1_code_mapping() -> dict:
    """Returns (country_code, admin1_name) → admin1_code from admin1CodesASCII.txt"""
    if not os.path.exists(ADMIN1_CODES_FILE):
        return {}
    mapping = {}
    with open(ADMIN1_CODES_FILE, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                full_code, name = parts[0], parts[1]
                country_code, admin1_code = full_code.split(".", 1)
                mapping[(country_code, name)] = admin1_code
    return mapping


# -----------------------------------------------------------------------------
# 🌆 GEONAMES CITY LOADER + FILTERS
# -----------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_geonames_cities() -> pd.DataFrame:
    """Loads cities500.txt and returns DataFrame with lat/lon, population, names."""
    if not os.path.exists(CITY_FILE_PATH):
        st.error(f"GeoNames city file not found: {CITY_FILE_PATH}")
        return pd.DataFrame()

    columns = [
        "geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude",
        "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code",
        "admin3_code", "admin4_code", "population", "elevation", "dem",
        "timezone", "modification_date"
    ]
    df = pd.read_csv(CITY_FILE_PATH, sep='\t', names=columns, header=None, dtype=str)
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df["population"] = df["population"].astype(int)
    return df

@st.cache_data(show_spinner=False)
def get_cities_by_admin1(country_code: str, admin1_code: str) -> list:
    """Returns sorted list of city names for given country and admin1 code."""
    df = load_geonames_cities()
    if df.empty:
        return []
    filtered = df[
        (df["country_code"] == country_code) &
        (df["admin1_code"] == admin1_code)
    ]
    return filtered.sort_values("population", ascending=False)["name"].unique().tolist()

@st.cache_data(show_spinner=False)
def get_city_coordinates(country_code: str, admin1_code: str, city_name: str) -> tuple | None:
    """Returns (lat, lon) tuple for given city."""
    df = load_geonames_cities()
    filtered = df[
        (df["country_code"] == country_code) &
        (df["admin1_code"] == admin1_code) &
        (df["name"].str.lower() == city_name.lower())
    ]
    if filtered.empty:
        return None
    return float(filtered.iloc[0]["latitude"]), float(filtered.iloc[0]["longitude"])
