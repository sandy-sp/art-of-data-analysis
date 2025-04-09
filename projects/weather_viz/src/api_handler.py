import requests

def fetch_weather_data(latitude, longitude, hourly_variables, daily_variables=None, forecast_days=7):
    """Fetches weather data from the Open-Meteo API."""
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(hourly_variables),
        "forecast_days": forecast_days
    }
    if daily_variables:
        params["daily"] = ",".join(daily_variables)

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Basic structure validation
        if not data or "hourly" not in data or not data.get("hourly", {}).get("time"):
            print("Warning: Incomplete or malformed response received from API.")
            return None

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
