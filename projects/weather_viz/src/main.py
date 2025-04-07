from src import api_handler
from src import data_processor
from src.visualizations import temperature_plot
from src.visualizations import wind_plot
from src.visualizations import precipitation_plot
from src.visualizations import wind_direction_plot
from src.visualizations import daily_temperature_range_plot
from src.visualizations import humidity_plot
from src.visualizations import feels_like_temperature_plot
from src.visualizations import temperature_humidity_plot
from src.visualizations import wind_speed_direction_plot 
from geopy.geocoders import Nominatim
import time

def get_coordinates(city_name):
    """
    Get latitude and longitude coordinates for a given city name.
    
    Args:
        city_name (str): Name of the city (can include state/country for precision)
        
    Returns:
        tuple: (latitude, longitude) or None if city not found
    """
    try:
        # Nominatim requires a unique user-agent
        geolocator = Nominatim(user_agent="weather_visualization_app")
        location = geolocator.geocode(city_name)
        
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not find coordinates for '{city_name}'")
            return None
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None

if __name__ == "__main__":
    # Get city name from user
    city_name = input("Enter a city name (e.g., Cleveland, OH): ")
    
    # Get coordinates for the city
    coordinates = get_coordinates(city_name)
    
    if coordinates:
        latitude, longitude = coordinates
        print(f"Using coordinates: {latitude}, {longitude} for {city_name}")
    else:
        # Fallback to manual coordinate entry
        try:
            print("\nFalling back to manual coordinate entry.")
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
        except ValueError:
            print("Invalid coordinates. Exiting.")
            exit(1)

    # Define the weather variables we want to fetch
    hourly_variables = ["temperature_2m", "windspeed_10m", "precipitation", "winddirection_10m", "relativehumidity_2m"]
    daily_variables = ["temperature_2m_max", "temperature_2m_min"]

    # Fetch the weather data from the API
    weather_data = api_handler.fetch_weather_data(latitude, longitude, hourly_variables, daily_variables)

    if weather_data:
        # Process the raw data into Pandas DataFrames
        hourly_df, daily_df = data_processor.process_weather_data(weather_data)

        # Generate the hourly temperature plot
        temperature_plot.plot_hourly_temperature(hourly_df)

        # Generate the hourly wind speed plot
        wind_plot.plot_wind_speed(hourly_df)

        # Generate the hourly precipitation plot
        precipitation_plot.plot_precipitation(hourly_df)

        # Generate the wind direction rose plot
        wind_direction_plot.plot_wind_direction_rose(hourly_df)

        # Generate the daily temperature range plot
        daily_temperature_range_plot.plot_daily_temperature_range(daily_df)

        # Generate the hourly humidity plot
        humidity_plot.plot_humidity(hourly_df)

        # Generate the combined temperature and humidity plot
        temperature_humidity_plot.plot_temperature_and_humidity(hourly_df)

        # Generate the combined wind speed and direction plot
        wind_speed_direction_plot.plot_wind_speed_and_direction(hourly_df)

        # Generate the hourly "feels like" temperature plot
        feels_like_temperature_plot.plot_feels_like_temperature(hourly_df)

        print("All visualizations generated successfully!")
    else:
        print("Failed to fetch weather data. Please check the error messages.")