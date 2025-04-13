import pytest
from src.api.open_meteo_api import fetch_historical_weather


def test_fetch_historical_weather_valid():
    hourly_df, daily_df = fetch_historical_weather(
        lat=37.7749,
        lon=-122.4194,
        start_date="2023-09-01",
        end_date="2023-09-03"
    )
    assert not hourly_df.empty, "Expected non-empty hourly weather DataFrame"
    assert not daily_df.empty, "Expected non-empty daily weather DataFrame"
    assert "temperature_2m" in hourly_df.columns
    assert "temperature_2m_max" in daily_df.columns


def test_fetch_historical_weather_invalid():
    hourly_df, daily_df = fetch_historical_weather(
        lat=999, lon=999, start_date="2023-09-01", end_date="2023-09-03"
    )
    assert hourly_df.empty and daily_df.empty, "Expected empty DataFrames for invalid coordinates"