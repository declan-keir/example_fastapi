"""
Loads models and makes predictions.

THIS IS WHERE YOU CUSTOMIZE TO MATCH YOUR TRAINING!
"""

import joblib
import numpy as np
from datetime import datetime, timedelta
from weather_api import get_weather


# Global variables to cache loaded models
_rain_model = None
_rain_preprocessor = None
_precip_model = None
_precip_preprocessor = None


def load_rain_model():
    """Load rain prediction model (loads once, then cached)"""
    global _rain_model, _rain_preprocessor

    if _rain_model is None:
        _rain_model = joblib.load('app/models/rain_or_not/model.joblib')
        _rain_preprocessor = joblib.load('app/models/rain_or_not/scaler.joblib')
        # If you have threshold:
        # with open('app/models/rain_or_not/threshold.txt') as f:
        #     _rain_threshold = float(f.read())

    return _rain_model, _rain_preprocessor


def load_precip_model():
    """Load precipitation prediction model (loads once, then cached)"""
    global _precip_model, _precip_preprocessor

    if _precip_model is None:
        _precip_model = joblib.load('app/models/precipitation_fall/model.joblib')
        _precip_preprocessor = joblib.load('app/models/precipitation_fall/scaler.joblib')

    return _precip_model, _precip_preprocessor


def prepare_rain_features(weather_data):
    """
    Transform weather data into features for rain model.

    CUSTOMIZE THIS TO MATCH YOUR TRAINING!
    Use the same features in the same order as your training data.
    """
    # Example - replace with YOUR features
    features = [
        weather_data.get('temperature_2m_max', 0),
        weather_data.get('temperature_2m_min', 0),
        weather_data.get('precipitation_sum', 0),
        weather_data.get('wind_speed_10m_max', 0),
        # Add your features here in the SAME ORDER as training
    ]

    # If you did circular encoding for wind direction:
    # wind_dir = weather_data.get('wind_direction_10m_dominant', 0)
    # wind_rad = np.radians(wind_dir)
    # features.append(np.sin(wind_rad))
    # features.append(np.cos(wind_rad))

    # If you added seasonal features:
    # month = datetime.strptime(date_str, "%Y-%m-%d").month
    # month_angle = 2 * np.pi * (month - 1) / 12
    # features.append(np.sin(month_angle))
    # features.append(np.cos(month_angle))

    return np.array([features])


def prepare_precip_features(weather_data):
    """
    Transform weather data into features for precipitation model.

    CUSTOMIZE THIS TO MATCH YOUR TRAINING!
    """
    # Example - replace with YOUR features
    features = [
        weather_data.get('temperature_2m_max', 0),
        weather_data.get('temperature_2m_min', 0),
        weather_data.get('precipitation_sum', 0),
        weather_data.get('wind_speed_10m_max', 0),
        # Add your features here
    ]

    return np.array([features])


def predict_rain(date_str):
    """
    Predict if it will rain 7 days from date_str.

    Returns:
        {
            "input_date": "2024-09-15",
            "prediction": {
                "date": "2024-09-22",
                "will_rain": true/false
            }
        }
    """
    # Load model
    model, preprocessor = load_rain_model()

    # Get weather data for input date
    weather = get_weather(date_str)

    # Prepare features (CUSTOMIZE prepare_rain_features!)
    X = prepare_rain_features(weather)

    # Apply preprocessing (scaler, etc)
    X_processed = preprocessor.transform(X)

    # Make prediction
    # For classification:
    prediction = model.predict(X_processed)[0]
    will_rain = bool(prediction)

    # Or if using probabilities with threshold:
    # prob = model.predict_proba(X_processed)[0, 1]
    # will_rain = prob >= threshold

    # Calculate prediction date (7 days ahead)
    input_date = datetime.strptime(date_str, "%Y-%m-%d")
    pred_date = input_date + timedelta(days=7)

    return {
        "input_date": date_str,
        "prediction": {
            "date": pred_date.strftime("%Y-%m-%d"),
            "will_rain": will_rain
        }
    }


def predict_precipitation(date_str):
    """
    Predict precipitation for next 3 days from date_str.

    Returns:
        {
            "input_date": "2024-09-15",
            "prediction": {
                "start_date": "2024-09-16",
                "end_date": "2024-09-18",
                "precipitation_fall": "5.2"
            }
        }
    """
    # Load model
    model, preprocessor = load_precip_model()

    # Get weather data for input date
    weather = get_weather(date_str)

    # Prepare features (CUSTOMIZE prepare_precip_features!)
    X = prepare_precip_features(weather)

    # Apply preprocessing
    X_processed = preprocessor.transform(X)

    # Make prediction
    precip_mm = model.predict(X_processed)[0]

    # Ensure non-negative
    precip_mm = max(0, float(precip_mm))

    # Calculate date range
    input_date = datetime.strptime(date_str, "%Y-%m-%d")
    start_date = input_date + timedelta(days=1)
    end_date = input_date + timedelta(days=3)

    return {
        "input_date": date_str,
        "prediction": {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "precipitation_fall": f"{precip_mm:.1f}"
        }
    }
