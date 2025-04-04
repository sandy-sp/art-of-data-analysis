import pandas as pd

def process_weather_data(weather_data):
    """Processes the raw weather data JSON into Pandas DataFrames."""
    if weather_data:
        hourly_data = weather_data.get("hourly")
        daily_data = weather_data.get("daily")

        hourly_df = None
        if hourly_data:
            hourly_df = pd.DataFrame(hourly_data)
            if 'time' in hourly_df.columns:
                hourly_df['time'] = pd.to_datetime(hourly_df['time'])

        daily_df = None
        if daily_data:
            daily_df = pd.DataFrame(daily_data)
            if 'time' in daily_df.columns:
                daily_df['time'] = pd.to_datetime(daily_df['time'])

        return hourly_df, daily_df
    else:
        return None, None

if __name__ == "__main__":
    # This is a sample JSON response (replace with actual API output for testing)
    sample_data = {
        "latitude": 41.5023,
        "longitude": -81.7095,
        "generationtime_ms": 0.12,
        "utc_offset_seconds": 0,
        "timezone": "GMT",
        "timezone_abbreviation": "GMT",
        "elevation": 202.0,
        "hourly_units": {
            "time": "iso8601",
            "temperature_2m": "°C",
            "windspeed_10m": "km/h",
            "precipitation": "mm"
        },
        "hourly": {
            "time": [
                "2025-04-04T00:00",
                "2025-04-04T01:00"
            ],
            "temperature_2m": [
                11.1,
                11.8
            ],
            "windspeed_10m": [
                14.8,
                4.6
            ],
            "precipitation": [
                0.0,
                0.0
            ]
        },
        "daily_units": {
            "time": "iso8601",
            "temperature_2m_max": "°C",
            "temperature_2m_min": "°C"
        },
        "daily": {
            "time": [
                "2025-04-04",
                "2025-04-05"
            ],
            "temperature_2m_max": [
                12.3,
                18.4
            ],
            "temperature_2m_min": [
                5.7,
                4.9
            ]
        }
    }

    hourly_df, daily_df = process_weather_data(sample_data)

    if hourly_df is not None:
        print("Processed Hourly DataFrame (from data_processor.py):")
        print(hourly_df.head())
    if daily_df is not None:
        print("\nProcessed Daily DataFrame (from data_processor.py):")
        print(daily_df.head())