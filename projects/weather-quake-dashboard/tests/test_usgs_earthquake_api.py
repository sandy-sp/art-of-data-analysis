import pytest
from src.api.usgs_earthquake_api import fetch_earthquake_data


def test_fetch_earthquake_data_valid():
    df = fetch_earthquake_data(
        starttime="2023-09-01",
        endtime="2023-09-03",
        min_magnitude=4.0,
        latitude=34.0522,
        longitude=-118.2437,
        limit=10
    )
    assert not df.empty, "Expected non-empty earthquake DataFrame"
    assert "Magnitude" in df.columns
    assert "Latitude" in df.columns


def test_fetch_earthquake_data_invalid():
    df = fetch_earthquake_data(
        starttime="1800-01-01",
        endtime="1800-01-02",
        min_magnitude=9.9,
        latitude=0,
        longitude=0,
        limit=10
    )
    assert df.empty, "Expected empty DataFrame for unrealistic parameters"
