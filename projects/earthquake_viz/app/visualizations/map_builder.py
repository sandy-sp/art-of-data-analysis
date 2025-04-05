import folium
import logging
import math
from datetime import datetime
# Optional: Use branca for colormaps if desired, requires installation
# import branca.colormap as cm
from folium.plugins import MarkerCluster  # Import MarkerCluster plugin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions for Styling ---

def get_color_by_depth(depth):
    """Assigns a color based on earthquake depth (in km)."""
    # USGS colors: Red(0-33km), Orange(33-70km), Yellow(70-150km), Green(150-300km), Blue(300-500km), Purple(>500km)
    # Simpler scale for now: Shallow (Yellow) -> Deep (Red)
    if depth < 0: # Handle potential negative depths if data contains them
        depth = 0

    if depth < 70:
        return 'yellow' # Shallow
    elif depth < 300:
        return 'orange' # Intermediate
    else:
        return 'red' # Deep

def get_radius_by_magnitude(magnitude):
    """Calculates marker radius based on earthquake magnitude."""
    # Use an exponential scale or similar to emphasize larger magnitudes
    if magnitude < 0:
        magnitude = 0 # Handle potential negative magnitudes
    # return 2 + magnitude * 2 # Linear scaling (adjust multiplier as needed)
    return math.pow(1.8, magnitude) if magnitude > 0 else 1 # Exponential scaling (adjust base)


# --- Main Map Creation Function ---

def create_earthquake_map(geojson_data: dict, center_on_bounds: list = None):
    """
    Creates a Folium map visualizing earthquake data from GeoJSON.

    Args:
        geojson_data (dict): The parsed GeoJSON data from the API.
        center_on_bounds (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]
                                           to center and fit the map. Defaults to None.

    Returns:
        folium.Map | None: The generated Folium map object, or None if data is invalid.
    """
    if not geojson_data or 'features' not in geojson_data:
        logging.error("Invalid or empty GeoJSON data received.")
        return None

    features = geojson_data['features']
    logging.info(f"Generating map for {len(features)} earthquake features.")

    # --- Initialize Map ---
    map_center = [0, 0]
    zoom_level = 2

    # If bounds are provided, calculate center and attempt to fit map
    if center_on_bounds:
        try:
            min_lon, min_lat, max_lon, max_lat = center_on_bounds
            # Basic check for validity
            if min_lon < max_lon and min_lat < max_lat:
                map_center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
                # Zoom level estimation is tricky; fitting bounds is better
            else:
                 logging.warning(f"Invalid bounds provided {center_on_bounds}, using default center.")
        except Exception as e:
            logging.warning(f"Error processing bounds {center_on_bounds}: {e}. Using default center.")


    # Create the base map
    fmap = folium.Map(location=map_center, zoom_start=zoom_level, tiles=None) # Start with no tiles initially

    # Add Tile Layers (allow user to switch)
    folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(fmap)
    folium.TileLayer('stamenterrain', name='Stamen Terrain', attr='stamenterrain').add_to(fmap)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True
    ).add_to(fmap)


    # --- Add Earthquake Markers using MarkerCluster ---
    marker_cluster = MarkerCluster(name="Earthquake Clusters").add_to(fmap)  # Create MarkerCluster layer

    for feature in features:
        try:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})

            if not properties or not geometry or geometry.get('type') != 'Point':
                logging.warning(f"Skipping feature with missing properties/geometry or non-Point type: {feature.get('id')}")
                continue

            coords = geometry.get('coordinates', [])
            if len(coords) < 2: # Need at least lon, lat
                logging.warning(f"Skipping feature with invalid coordinates: {feature.get('id')}")
                continue

            # GeoJSON coordinates are [longitude, latitude, depth]
            lon, lat = coords[0], coords[1]
            # Depth might be the third element or sometimes missing
            depth = coords[2] if len(coords) > 2 else 0

            mag = properties.get('mag', 0) # Default to 0 if missing
            place = properties.get('place', 'N/A')
            time_epoch = properties.get('time') # Time is usually epoch milliseconds

            # Format time for popup
            time_str = "N/A"
            if time_epoch:
                try:
                    # Convert milliseconds to seconds for datetime
                    time_dt = datetime.utcfromtimestamp(time_epoch / 1000)
                    time_str = time_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                except Exception as e:
                    logging.warning(f"Error formatting time {time_epoch}: {e}")
                    time_str = f"Invalid Time ({time_epoch})"

            # Create Popup Content
            popup_html = f"""
            <b>Location:</b> {place}<br>
            <b>Time:</b> {time_str}<br>
            <b>Magnitude:</b> {mag or 'N/A'}<br>
            <b>Depth:</b> {depth:.2f} km
            """
            popup = folium.Popup(popup_html, max_width=300)

            # Create CircleMarker
            marker = folium.CircleMarker(
                location=[lat, lon], # Folium uses [lat, lon]
                radius=get_radius_by_magnitude(mag),
                popup=popup,
                tooltip=f"Mag: {mag}, Depth: {depth:.1f}km", # Tooltip on hover
                color=get_color_by_depth(depth), # Outline color
                fill=True,
                fill_color=get_color_by_depth(depth), # Fill color
                fill_opacity=0.7
            )
            marker.add_to(marker_cluster)  # Add marker to MarkerCluster

        except Exception as e:
            logging.error(f"Error processing feature {feature.get('id')}: {e}", exc_info=True) # Log traceback

    # Fit map to bounds if provided and valid
    if center_on_bounds and 'min_lat' in locals(): # Check if bounds were validly processed
         try:
            fmap.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
            logging.info(f"Fitting map to bounds: [[{min_lat}, {min_lon}], [{max_lat}, {max_lon}]]")
         except Exception as e:
            logging.warning(f"Could not fit map to bounds {center_on_bounds}: {e}")


    # --- Add Layer Control ---
    folium.LayerControl().add_to(fmap)

    # --- Add Legend (using HTML) ---
    # A simple HTML legend added to the map object
    legend_html = """
    <div style="position: fixed;
         bottom: 50px; left: 50px; width: 180px; height: 120px;
         border:2px solid grey; z-index:9999; font-size:14px;
         background-color:rgba(255, 255, 255, 0.8);
         ">
     &nbsp; <b>Legend</b> <br>
     &nbsp; <b>Depth (km)</b> <br>
     &nbsp; <i class="fa fa-circle" style="color:yellow"></i> &lt; 70 km<br>
     &nbsp; <i class="fa fa-circle" style="color:orange"></i> 70 - 300 km<br>
     &nbsp; <i class="fa fa-circle" style="color:red"></i> &gt; 300 km<br>
     &nbsp; <b>Size ~ Magnitude</b>
    </div>
    """
    # Note: This requires Font Awesome icons, which Folium includes by default.
    fmap.get_root().html.add_child(folium.Element(legend_html))

    logging.info("Map generation complete with marker clustering.")  # Updated log message
    return fmap