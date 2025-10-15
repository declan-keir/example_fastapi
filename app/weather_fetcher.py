"""
Weather Data Fetcher

This module fetches historical weather data from the Open Meteo API.

WHAT IT DOES:
- Takes a date as input
- Makes an HTTP request to Open Meteo API
- Gets weather data (temperature, wind, rain, etc.) for Sydney on that date
- Returns the data as a Python dictionary

Author: Your Name
Date: 2025
"""

# ============================================================================
# IMPORTS
# ============================================================================

import requests  # Library for making HTTP requests (talking to APIs)
from datetime import datetime  # For working with dates
import pytz  # For handling timezones (Sydney timezone)


# ============================================================================
# CONSTANTS - Values that never change
# ============================================================================

# Sydney's location (latitude and longitude)
SYDNEY_LATITUDE = -33.8678
SYDNEY_LONGITUDE = 151.2073

# Open Meteo API endpoint (the URL we send requests to)
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"


# ============================================================================
# MAIN FUNCTION: FETCH WEATHER DATA
# ============================================================================

def fetch_weather_for_date(date_str: str) -> dict:
    """
    Fetch historical weather data from Open Meteo API for a specific date.

    This function does the following:
    1. Validates the date is not in the future
    2. Builds the API request with required parameters
    3. Sends the HTTP GET request to Open Meteo
    4. Receives the JSON response
    5. Extracts and returns the weather data

    Args:
        date_str (str): Date in YYYY-MM-DD format (example: "2024-09-15")

    Returns:
        dict: Dictionary containing weather data with keys like:
            - temperature_2m_max: Maximum temperature (°C)
            - temperature_2m_min: Minimum temperature (°C)
            - precipitation_sum: Total precipitation (mm)
            - wind_speed_10m_max: Maximum wind speed (km/h)
            - wind_direction_10m_dominant: Wind direction (degrees)
            - And more...

    Raises:
        ValueError: If date is invalid or in the future
        ConnectionError: If API request fails

    Example:
        >>> data = fetch_weather_for_date("2024-09-15")
        >>> print(data['temperature_2m_max'])
        25.3
    """

    # STEP 1: Parse the date string into a datetime object
    # This validates the date format and creates a date object we can work with
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date format: '{date_str}'. "
            "Please use YYYY-MM-DD format (example: 2024-09-15)"
        )

    # STEP 2: Check if date is in the future
    # Open Meteo only has historical data, not future data
    # We need to check against Sydney timezone (not your local timezone)

    # Get current date in Sydney timezone
    sydney_tz = pytz.timezone('Australia/Sydney')
    today_sydney = datetime.now(sydney_tz).date()

    # Compare input date with today in Sydney
    if date_obj.date() > today_sydney:
        raise ValueError(
            f"Cannot fetch weather data for future date {date_str}. "
            f"Current date in Sydney is {today_sydney}. "
            f"Please provide a date on or before {today_sydney}."
        )

    # STEP 3: Build the API request parameters
    # These parameters tell Open Meteo what data we want

    params = {
        # Location (Sydney coordinates)
        "latitude": SYDNEY_LATITUDE,
        "longitude": SYDNEY_LONGITUDE,

        # Date range (we want just one day, so start and end are the same)
        "start_date": date_str,
        "end_date": date_str,

        # Weather variables we want (daily aggregates)
        # This is a list of weather metrics
        "daily": [
            "weather_code",                    # Weather condition code (0-99)
            "temperature_2m_max",              # Max temperature at 2m height (°C)
            "temperature_2m_min",              # Min temperature at 2m height (°C)
            "apparent_temperature_max",        # Max "feels like" temperature (°C)
            "apparent_temperature_min",        # Min "feels like" temperature (°C)
            "precipitation_sum",               # Total precipitation (mm)
            "precipitation_hours",             # Hours with precipitation
            "wind_speed_10m_max",              # Max wind speed at 10m height (km/h)
            "wind_gusts_10m_max",              # Max wind gusts at 10m height (km/h)
            "wind_direction_10m_dominant",     # Dominant wind direction (degrees: 0-360)
            "shortwave_radiation_sum",         # Solar radiation (MJ/m²)
            "et0_fao_evapotranspiration",      # Evapotranspiration (mm)
            "daylight_duration",               # Daylight duration (seconds)
            "sunshine_duration",               # Sunshine duration (seconds)
        ],

        # Timezone for the response data
        "timezone": "Australia/Sydney",
    }

    # STEP 4: Send the HTTP GET request to Open Meteo API
    # This is like opening a URL in your browser, but in Python

    try:
        # Make the request with a 10 second timeout
        # timeout=10 means "if no response after 10 seconds, give up"
        response = requests.get(OPEN_METEO_URL, params=params, timeout=10)

    except requests.exceptions.Timeout:
        # If request takes too long
        raise ConnectionError(
            "API request timed out after 10 seconds. "
            "The Open Meteo API might be slow. Please try again."
        )

    except requests.exceptions.ConnectionError:
        # If can't connect to the API (no internet, API is down, etc.)
        raise ConnectionError(
            "Failed to connect to Open Meteo API. "
            "Please check your internet connection and try again."
        )

    except Exception as e:
        # Any other unexpected network error
        raise ConnectionError(f"Unexpected error connecting to API: {str(e)}")

    # STEP 5: Check if the request was successful
    # HTTP status code 200 means "OK" (success)

    if response.status_code != 200:
        raise ValueError(
            f"Open Meteo API returned error: HTTP {response.status_code}. "
            f"This might mean the date is invalid or the API is having issues."
        )

    # STEP 6: Parse the JSON response
    # The API sends back data in JSON format, convert it to a Python dictionary

    try:
        data = response.json()
    except ValueError:
        raise ValueError(
            "Received invalid JSON from Open Meteo API. "
            "The API might be having issues."
        )

    # STEP 7: Extract the daily weather data
    # The response structure looks like this:
    # {
    #   "daily": {
    #     "time": ["2024-09-15"],
    #     "temperature_2m_max": [25.3],
    #     "temperature_2m_min": [15.2],
    #     ...
    #   }
    # }

    if "daily" not in data:
        raise ValueError(
            f"No weather data available for date {date_str}. "
            "The API response is missing daily data."
        )

    daily_data = data["daily"]

    # STEP 8: Convert the data into a simpler format
    # Currently, each value is in a list (example: [25.3])
    # We want just the value (example: 25.3)

    weather_dict = {}

    # Loop through each weather variable
    for key, values in daily_data.items():
        # Skip the "time" key (we already know the date)
        if key != "time" and values:
            # Take the first value (there's only one since we requested one day)
            weather_dict[key] = values[0]

    # STEP 9: Validate we actually got data
    if not weather_dict:
        raise ValueError(
            f"No weather data available for date {date_str}. "
            "The API returned empty data."
        )

    # STEP 10: Return the weather data dictionary
    return weather_dict


# ============================================================================
# UNDERSTANDING THE RESPONSE
# ============================================================================
"""
Example response from fetch_weather_for_date("2024-09-15"):

{
    "weather_code": 3,                      # Weather condition (3 = overcast)
    "temperature_2m_max": 25.3,             # Max temp: 25.3°C
    "temperature_2m_min": 15.2,             # Min temp: 15.2°C
    "apparent_temperature_max": 24.1,       # Feels like max: 24.1°C
    "apparent_temperature_min": 14.8,       # Feels like min: 14.8°C
    "precipitation_sum": 2.5,               # Total rain: 2.5mm
    "precipitation_hours": 3.0,             # Rained for 3 hours
    "wind_speed_10m_max": 18.5,             # Max wind: 18.5 km/h
    "wind_gusts_10m_max": 32.1,             # Max gusts: 32.1 km/h
    "wind_direction_10m_dominant": 270,     # Wind from west (270°)
    "shortwave_radiation_sum": 15.2,        # Solar radiation: 15.2 MJ/m²
    "et0_fao_evapotranspiration": 3.8,      # Evapotranspiration: 3.8mm
    "daylight_duration": 43200,             # Daylight: 43200 seconds (12 hours)
    "sunshine_duration": 28800,             # Sunshine: 28800 seconds (8 hours)
}
"""


# ============================================================================
# WEATHER CODE REFERENCE
# ============================================================================
"""
The weather_code tells you the weather condition:

Clear sky:
  0 - Clear

Cloudy:
  1 - Mainly clear
  2 - Partly cloudy
  3 - Overcast

Fog:
  45 - Fog
  48 - Depositing rime fog

Drizzle:
  51 - Light drizzle
  53 - Moderate drizzle
  55 - Dense drizzle

Rain:
  61 - Slight rain
  63 - Moderate rain
  65 - Heavy rain

Snow:
  71 - Slight snow
  73 - Moderate snow
  75 - Heavy snow

Showers:
  80 - Slight rain showers
  81 - Moderate rain showers
  82 - Violent rain showers

Thunderstorm:
  95 - Thunderstorm
  96 - Thunderstorm with slight hail
  99 - Thunderstorm with heavy hail
"""


# ============================================================================
# TESTING THIS MODULE
# ============================================================================
"""
To test this module directly, you can run:

python -c "from weather_fetcher import fetch_weather_for_date; print(fetch_weather_for_date('2024-09-15'))"

Or create a test script:

if __name__ == "__main__":
    # Test with a valid date
    try:
        data = fetch_weather_for_date("2024-09-15")
        print("Weather data for 2024-09-15:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error: {e}")

    # Test with future date (should fail)
    try:
        data = fetch_weather_for_date("2099-01-01")
    except ValueError as e:
        print(f"Expected error: {e}")
"""
