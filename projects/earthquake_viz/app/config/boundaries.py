# --- Shapefile Configuration ---
# IMPORTANT: Replace with the correct path to your downloaded shapefile
# Ensure this path is relative to the root of your project or absolute
SHAPEFILE_PATH = "data/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp" #<-- UPDATE THIS PATH

# --- Predefined Bounding Boxes ---
# Bounding Box Format: [min_longitude, min_latitude, max_longitude, max_latitude]
PREDEFINED_BOUNDING_BOXES = {
    "Global": [-180, -90, 180, 90], # Full world
    # "USA (Contiguous)": [-125, 24, -66, 50], # Keep examples if useful, or remove
    # "Japan": [122, 24, 146, 46],
}

# Keep predefined cities if you plan to use them later
PREDEFINED_CITIES = {
    "San Francisco": {"lat": 37.7749, "lon": -122.4194, "default_radius_km": 100},
}