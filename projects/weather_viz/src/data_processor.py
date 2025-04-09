import pandas as pd

def process_weather_data(weather_data):
    """Processes the raw weather data JSON into Pandas DataFrames."""
    if not weather_data:
        return None, None

    hourly_data = weather_data.get("hourly")
    daily_data = weather_data.get("daily")

    hourly_df = None
    if hourly_data:
        hourly_df = pd.DataFrame(hourly_data)

        # Basic validation
        if 'time' not in hourly_df.columns:
            print("Warning: 'time' column missing in hourly data.")
            hourly_df = None
        else:
            hourly_df['time'] = pd.to_datetime(hourly_df['time'])

            if 'temperature_2m' in hourly_df and 'relativehumidity_2m' in hourly_df:
                hourly_df['feels_like_temperature_2m'] = _calculate_heat_index(
                    hourly_df['temperature_2m'], hourly_df['relativehumidity_2m'])

            if 'temperature_2m' in hourly_df and 'windspeed_10m' in hourly_df:
                hourly_df['wind_chill_2m'] = _calculate_wind_chill(
                    hourly_df['temperature_2m'], hourly_df['windspeed_10m'])

            if 'windspeed_10m' in hourly_df:
                hourly_df['avg_daily_windspeed_10m'] = hourly_df.groupby(hourly_df['time'].dt.date)['windspeed_10m'].transform('mean')

            if 'precipitation' in hourly_df:
                hourly_df['precipitation_intensity'] = hourly_df['precipitation'].diff().fillna(0)

    daily_df = None
    if daily_data:
        daily_df = pd.DataFrame(daily_data)

        if 'time' not in daily_df.columns:
            print("Warning: 'time' column missing in daily data.")
            daily_df = None
        else:
            daily_df['time'] = pd.to_datetime(daily_df['time'])

    return hourly_df, daily_df

def _calculate_heat_index(temperature, relative_humidity):
    """Calculates the heat index (feels like temperature)."""
    return temperature + 0.6 * (relative_humidity - 60)

def _calculate_wind_chill(temperature, wind_speed):
    """Calculates the wind chill factor."""
    return temperature - 0.5 * (wind_speed - 10)
