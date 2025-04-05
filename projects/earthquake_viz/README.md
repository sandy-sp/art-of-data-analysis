# 🌍 USGS Earthquake Visualizer

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-0.10%2B-green?logo=python&logoColor=white)](https://geopandas.org/)
[![Folium](https://img.shields.io/badge/Folium-0.12%2B-blue)](https://python-visualization.github.io/folium/)

## 📖 Overview

This project is an interactive web application built with Python and Streamlit. It allows users to fetch, visualize, and explore recent earthquake data sourced from the USGS Earthquake Catalog API. The primary focus is on visualizing earthquakes occurring within the boundaries of a user-selected country, leveraging geospatial libraries for accurate filtering and mapping.

## 🚀 Features

* **Country-Specific Search:** Filters earthquake data based on geographic boundaries for a user-selected country. Users select the country from a dropdown list populated dynamically from the shapefile, preventing spelling errors.
* **Dynamic Boundary Loading:** Uses GeoPandas to load country boundaries from a Natural Earth shapefile, providing accurate filtering coordinates to the USGS API.
* **Interactive Map (Folium/Leaflet.js):**
    * Displays earthquake epicenters on a zoomable, pannable map.
    * **Marker Styling:** Earthquake markers are visually encoded:
        * **Size:** Represents earthquake magnitude (larger markers for stronger quakes, using an exponential scale).
        * **Color:** Represents earthquake depth (Yellow: <70km, Orange: 70-300km, Red: >300km).
    * **Marker Clustering:** Automatically groups nearby markers at lower zoom levels for better readability and performance, especially with dense datasets (`folium.plugins.MarkerCluster`).
    * **Informative Popups:** Clicking on a marker reveals details: Magnitude, Location (Place Name), Depth, and Time (UTC).
    * **Tooltips:** Hovering over markers shows quick info (Magnitude, Depth).
    * **Multiple Base Layers:** Allows switching between OpenStreetMap, Stamen Terrain, and Esri Satellite map tiles via a layer control.
    * **Map Legend:** A clear legend explains the color/size coding for depth and magnitude.
* **Customizable Data Filters:** Refine the earthquake search by:
    * Date Range (Start Date, End Date)
    * Minimum Magnitude (0.0 - 10.0 slider)
    * Maximum Number of Events to fetch (Limit)
* **Data Table Display:** Presents the fetched earthquake details (Magnitude, Place, Time, Depth, Coordinates, USGS ID, Details URL) in a sortable Pandas DataFrame displayed via `st.dataframe`.
* **Data Download:** Allows users to download the filtered earthquake data currently displayed in the table as a CSV file.
* **Performance Optimization:**
    * **API Caching:** Caches results from the USGS API (`@st.cache_data`) for a set duration (e.g., 15 minutes) to speed up repeated queries with the same parameters and reduce API load.
    * **Shapefile Caching:** Caches the loaded GeoPandas DataFrame containing world boundaries (`@st.cache_resource`) to avoid slow file I/O on every user interaction.
* **User-Friendly Interface:** Built with Streamlit, featuring a clean layout with controls neatly organized in the sidebar.

## 🛠️ Technologies Used

* **Core Language:** Python 3.9+
* **Web Framework / UI:** Streamlit
* **Data Handling:** Pandas
* **Geospatial Processing:** GeoPandas
* **Interactive Mapping:** Folium (Leaflet.js wrapper)
* **API Communication:** Requests
* **Configuration:** Standard Python modules (`app/config/`)

## 📊 Data Sources & Credits

* **Earthquake Data:** Sourced from the **USGS Earthquake Catalog API**.
    * API Endpoint: [https://earthquake.usgs.gov/fdsnws/event/1/](https://earthquake.usgs.gov/fdsnws/event/1/)
    * *Disclaimer:* Please adhere to USGS data usage policies and acknowledge them appropriately if distributing or publishing results. Data is typically updated frequently but may not be instantaneous.
* **Country Boundaries:** Sourced from **Natural Earth**.
    * Website: [https://www.naturalearthdata.com/](https://www.naturalearthdata.com/)
    * Dataset Used: Admin 0 – Countries (specifically the 110m resolution cultural vector shapefile).
    * *License:* Natural Earth data is in the public domain. Credit is appreciated.

## 📁 Project Structure

## 📁 Project Structure

The project is organized into a modular structure to ensure separation of concerns:

```
earthquake-visualizer/
├── app/                    # Main application source code package
│   ├── config/             # Configuration files (API URLs, shapefile paths, boundary definitions)
│   ├── core/               # Core logic (API interaction, geospatial utilities, data processing)
│   ├── ui/                 # Streamlit UI components (e.g., sidebar controls)
│   ├── visualizations/     # Map and chart generation logic
│   ├── __init__.py         # Makes 'app' a Python package
│   └── main.py             # Main Streamlit application script (orchestrates UI, data, visualizations)
├── data/
│   └── shapefiles/         # Directory to store downloaded shapefiles
│       └── ne_110m_admin_0_countries/ # Example: Contains Natural Earth shapefile data
├── venv/                   # Python virtual environment 
├── README.md               # Project documentation (this file)
└── requirements.txt        # Python package dependencies
```
## ⚙️ Setup & Installation

Follow these steps to set up and run the project locally:

1.  **Clone the Repository:**
    ```bash
    # Replace with your repository URL if applicable
    git clone <your-repository-url>
    cd earthquake-visualizer
    ```

2.  **Create and Activate Virtual Environment:**
    * This isolates project dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows use: venv\Scripts\activate
    ```

3.  **Install System Dependencies (for GeoPandas):**
    * GeoPandas often requires the GDAL library. Installation varies by OS.
    * **On Debian/Ubuntu Linux:**
        ```bash
        sudo apt-get update
        sudo apt-get install libgdal-dev gdal-bin python3-gdal -y
        ```
    * **On other systems (macOS, Windows):** Using Conda (`conda install geopandas`) is often easier. Alternatively, refer to the official [GeoPandas Installation Guide](https://geopandas.org/en/stable/getting_started/install.html) for detailed instructions.

4.  **Install Python Dependencies:**
    * Installs all required Python packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Download Country Boundaries Shapefile:**
    * Navigate to [Natural Earth Downloads (110m Cultural Vectors - Admin 0 Countries)](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/).
    * Download the **Shapefile** version (a `.zip` file).
    * Create the directory `data/shapefiles/` in your project root if it doesn't exist.
    * Unzip the downloaded file. Place the extracted contents (files like `.shp`, `.shx`, `.dbf`, `.prj`, etc.) into a subdirectory within `data/shapefiles/` (e.g., `data/shapefiles/ne_110m_admin_0_countries/`).

6.  **Configure and Verify Shapefile Path:**
    * Open the file `app/config/boundaries.py`.
    * Ensure the `SHAPEFILE_PATH` variable points correctly to the `.shp` file you just placed (e.g., `"data/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"`).
    * **Important:** Verify the country name column used in `app/core/geo_utils.py` (inside the `load_world_shapefile` function, check the `original_name_column` variable). It needs to match the actual column name in your downloaded shapefile (common names are 'ADMIN', 'NAME', 'SOVEREIGNT'). Adjust if necessary. You can test this by running `python app/core/geo_utils.py` if you uncomment the test block within it.

## ▶️ Running the Application

1.  **Activate your virtual environment:**
    ```bash
    source venv/bin/activate
    ```
2.  **Navigate to the project root directory** (`earthquake-visualizer/`).
3.  **Run the Streamlit application:**
    ```bash
    streamlit run app/main.py
    ```
4.  Streamlit will provide a local URL (usually `http://localhost:8501`). Open this URL in your web browser to use the application.

## ✨ Future Enhancements (Ideas)

* Implement search by City name + radius using `geopy`.
* Add more visualization types (e.g., magnitude/depth histograms, time series plots) using `app/visualizations/chart_builder.py`.
* Allow selection of multiple countries or regions simultaneously.
* Add more advanced map interaction features or layers (e.g., tectonic plate boundaries).
* Implement more robust error handling and user feedback mechanisms.
* Add unit tests for core functions (API calls, data processing, geo utils).
* Explore options for deploying the application (e.g., Streamlit Community Cloud).

