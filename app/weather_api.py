"""
Gets weather data from Open Meteo API.

Simple function that fetches historical weather for a specific date.
"""

import requests
from datetime import datetime
import pytz


def get_weather(date_str):
    """
    Fetch weather data for Sydney on a specific date.

    Args:
        date_str: Date in YYYY-MM-DD format (e.g., "2024-09-15")

    Returns:
        Dictionary with weather data

    Raises:
        ValueError: If date is invalid or in the future
    """
    # Check date is not in future (Sydney timezone)
    sydney_tz = pytz.timezone('Australia/Sydney')
    today = datetime.now(sydney_tz).date()
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    if date > today:
        raise ValueError(f"Date {date_str} is in the future. Use dates before {today}.")

    # Open Meteo API parameters
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": -33.8678,  # Sydney
        "longitude": 151.2073,
        "start_date": date_str,
        "end_date": date_str,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max",
            "wind_direction_10m_dominant",
            # Add whatever weather variables you need
        ],
        "timezone": "Australia/Sydney"
    }

    # Make request
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise ConnectionError(f"Failed to fetch weather data: {str(e)}")

    # Extract daily data (first day since we only requested one)
    if "daily" not in data:
        raise ValueError(f"No weather data available for {date_str}")

    daily = data["daily"]
    weather = {}
    for key, values in daily.items():
        if key != "time" and values:
            weather[key] = values[0]

    return weather
