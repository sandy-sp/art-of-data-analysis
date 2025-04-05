# app/config/boundaries.py

# --- Shapefile Configuration ---
# IMPORTANT: Ensure this path is correct
SHAPEFILE_PATH = "data/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"

# --- Predefined Bounding Boxes ---
# Removing "Global". Keep others only if needed as alternative presets.
#PREDEFINED_BOUNDING_BOXES = {
    # "USA (Contiguous)": [-125, 24, -66, 50], # Example removed/commented
    # "Japan": [122, 24, 146, 46],       # Example removed/commented
# }

# Keep predefined cities if you plan to use them later
# PREDEFINED_CITIES = {
#    "San Francisco": {"lat": 37.7749, "lon": -122.4194, "default_radius_km": 100},
#}