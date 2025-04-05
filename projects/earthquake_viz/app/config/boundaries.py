# app/config/boundaries.py

# Bounding Box Format: [min_longitude, min_latitude, max_longitude, max_latitude]

PREDEFINED_BOUNDING_BOXES = {
    "Global": [-180, -90, 180, 90], # Full world
    "USA (Contiguous)": [-125, 24, -66, 50], # Example for testing
    "Japan": [122, 24, 146, 46],       # Example for testing
    # Add more continents, countries, regions as needed
}

# Could also add predefined city centers + default radius later
PREDEFINED_CITIES = {
    "San Francisco": {"lat": 37.7749, "lon": -122.4194, "default_radius_km": 100},
    # Add more cities
}