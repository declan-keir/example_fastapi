"""
Model Prediction Module

This module loads trained machine learning models and makes predictions.

THE PREDICTION PIPELINE:
1. Load models (first time only, then cached)
2. Fetch weather data for input date
3. Prepare features (feature engineering)
4. Scale features (StandardScaler)
5. Make prediction with model
6. Format and return result

Author: Your Name
Date: 2025
"""

# ============================================================================
# IMPORTS
# ============================================================================

import os  # For file paths
import numpy as np  # For numerical operations
from datetime import datetime, timedelta  # For date calculations
import joblib  # For loading saved models

# Import our weather fetcher
from weather_fetcher import fetch_weather_for_date


# ============================================================================
# CONFIGURATION - Model paths and prediction settings
# ============================================================================

# Paths to model files
RAIN_MODEL_PATH = "app/models/rain_or_not/model.joblib"
RAIN_SCALER_PATH = "app/models/rain_or_not/scaler.joblib"
RAIN_THRESHOLD_PATH = "app/models/rain_or_not/threshold.txt"

PRECIP_MODEL_PATH = "app/models/precipitation_fall/model.joblib"
PRECIP_SCALER_PATH = "app/models/precipitation_fall/scaler.joblib"

# Prediction parameters
RAIN_PREDICTION_DAYS = 7  # Predict rain 7 days ahead
PRECIPITATION_PREDICTION_DAYS = 3  # Predict precipitation for next 3 days


# ============================================================================
# GLOBAL MODEL CACHE
# These variables store loaded models in memory after first use
# This is called "lazy loading" - we only load models when needed
# ============================================================================

_rain_model = None  # Will store the rain prediction model
_rain_scaler = None  # Will store the rain feature scaler
_rain_threshold = None  # Will store the rain classification threshold

_precip_model = None  # Will store the precipitation prediction model
_precip_scaler = None  # Will store the precipitation feature scaler


# ============================================================================
# FUNCTION 1: LOAD RAIN MODELS
# ============================================================================

def load_rain_models():
    """
    Load the rain prediction model, scaler, and threshold.

    This function:
    1. Checks if models are already loaded (if so, returns cached versions)
    2. Loads model.joblib (your trained classification model)
    3. Loads scaler.joblib (StandardScaler fitted on training data)
    4. Loads threshold.txt (optimal probability threshold)
    5. Caches them in global variables for future use

    This is called "singleton pattern" - models are loaded once and reused.
    This is MUCH faster than loading models for every prediction.

    Returns:
        tuple: (model, scaler, threshold)

    Raises:
        FileNotFoundError: If model files are missing
        RuntimeError: If model loading fails
    """
    global _rain_model, _rain_scaler, _rain_threshold

    # If already loaded, return cached versions
    if _rain_model is not None:
        return _rain_model, _rain_scaler, _rain_threshold

    # Check if model files exist
    if not os.path.exists(RAIN_MODEL_PATH):
        raise FileNotFoundError(
            f"Rain model not found at {RAIN_MODEL_PATH}. "
            "Please copy your trained model.joblib file to this location."
        )
    if not os.path.exists(RAIN_SCALER_PATH):
        raise FileNotFoundError(
            f"Rain scaler not found at {RAIN_SCALER_PATH}. "
            "Please copy your scaler.joblib file to this location."
        )
    if not os.path.exists(RAIN_THRESHOLD_PATH):
        raise FileNotFoundError(
            f"Rain threshold file not found at {RAIN_THRESHOLD_PATH}. "
            "Please create threshold.txt with your optimal threshold."
        )

    # Load the model and scaler using joblib
    try:
        _rain_model = joblib.load(RAIN_MODEL_PATH)
        _rain_scaler = joblib.load(RAIN_SCALER_PATH)

        # Load threshold from text file
        with open(RAIN_THRESHOLD_PATH, 'r') as f:
            threshold_str = f.read().strip()
            _rain_threshold = float(threshold_str)

        # Validate threshold is reasonable (should be between 0 and 1)
        if not (0 <= _rain_threshold <= 1):
            raise ValueError(f"Threshold must be between 0 and 1, got {_rain_threshold}")

        print("✓ Rain models loaded successfully")
        print(f"  Model type: {type(_rain_model).__name__}")
        print(f"  Scaler type: {type(_rain_scaler).__name__}")
        print(f"  Threshold: {_rain_threshold}")

    except Exception as e:
        # If loading fails, reset global variables
        _rain_model = None
        _rain_scaler = None
        _rain_threshold = None
        raise RuntimeError(f"Failed to load rain models: {str(e)}")

    return _rain_model, _rain_scaler, _rain_threshold


# ============================================================================
# FUNCTION 2: LOAD PRECIPITATION MODELS
# ============================================================================

def load_precipitation_models():
    """
    Load the precipitation prediction model and scaler.

    Similar to load_rain_models, but for precipitation prediction.
    Precipitation is a regression task (predicting a number, not a category).

    Returns:
        tuple: (model, scaler)

    Raises:
        FileNotFoundError: If model files are missing
        RuntimeError: If model loading fails
    """
    global _precip_model, _precip_scaler

    # If already loaded, return cached versions
    if _precip_model is not None:
        return _precip_model, _precip_scaler

    # Check if model files exist
    if not os.path.exists(PRECIP_MODEL_PATH):
        raise FileNotFoundError(
            f"Precipitation model not found at {PRECIP_MODEL_PATH}. "
            "Please copy your trained model.joblib file to this location."
        )
    if not os.path.exists(PRECIP_SCALER_PATH):
        raise FileNotFoundError(
            f"Precipitation scaler not found at {PRECIP_SCALER_PATH}. "
            "Please copy your scaler.joblib file to this location."
        )

    # Load the model and scaler
    try:
        _precip_model = joblib.load(PRECIP_MODEL_PATH)
        _precip_scaler = joblib.load(PRECIP_SCALER_PATH)

        print("✓ Precipitation models loaded successfully")
        print(f"  Model type: {type(_precip_model).__name__}")
        print(f"  Scaler type: {type(_precip_scaler).__name__}")

    except Exception as e:
        # If loading fails, reset global variables
        _precip_model = None
        _precip_scaler = None
        raise RuntimeError(f"Failed to load precipitation models: {str(e)}")

    return _precip_model, _precip_scaler


# ============================================================================
# FUNCTION 3: PREPARE FEATURES FOR RAIN PREDICTION
# ============================================================================

def prepare_rain_features(weather_data: dict, date_obj: datetime) -> np.ndarray:
    """
    Transform raw weather data into features for the rain prediction model.

    FEATURE ENGINEERING:
    This is the process of converting raw data into inputs the model understands.
    You need to do the SAME transformations you did during training!

    Args:
        weather_data (dict): Raw weather data from Open Meteo API
        date_obj (datetime): The input date (for seasonal features)

    Returns:
        np.ndarray: 2D array of features ready for the model (shape: 1 x num_features)

    Example transformations:
        - Wind direction: 270° → sin/cos encoding
        - Weather code: 63 → binary feature (is it code 63 or 65?)
        - Month: September → sin/cos seasonal encoding
    """

    # Initialize feature dictionary
    features = {}

    # ========================================================================
    # DIRECT FEATURES - Use as-is from weather data
    # ========================================================================

    # Temperature features
    features['temperature_2m_max'] = weather_data.get('temperature_2m_max', 0)
    features['temperature_2m_min'] = weather_data.get('temperature_2m_min', 0)
    features['apparent_temperature_max'] = weather_data.get('apparent_temperature_max', 0)
    features['apparent_temperature_min'] = weather_data.get('apparent_temperature_min', 0)

    # Solar and atmospheric features
    features['daylight_duration'] = weather_data.get('daylight_duration', 0)
    features['shortwave_radiation_sum'] = weather_data.get('shortwave_radiation_sum', 0)
    features['et0_fao_evapotranspiration'] = weather_data.get('et0_fao_evapotranspiration', 0)

    # Wind features
    features['wind_speed_10m_max'] = weather_data.get('wind_speed_10m_max', 0)
    features['wind_gusts_10m_max'] = weather_data.get('wind_gusts_10m_max', 0)

    # ========================================================================
    # WIND DIRECTION - Circular encoding (sin/cos)
    # ========================================================================
    # WHY? Wind direction is circular: 0° and 360° are the same direction
    # If we use raw degrees, the model thinks 0° and 360° are far apart
    # Solution: Convert to sin/cos to preserve circular nature

    wind_direction = weather_data.get('wind_direction_10m_dominant', 0)
    if wind_direction is None:
        wind_direction = 0

    # Convert degrees to radians (required for sin/cos)
    wind_radians = np.radians(float(wind_direction))

    # Create two features: sin and cos
    features['wind_direction_sin'] = np.sin(wind_radians)
    features['wind_direction_cos'] = np.cos(wind_radians)

    # Example:
    # - North (0°): sin=0, cos=1
    # - East (90°): sin=1, cos=0
    # - South (180°): sin=0, cos=-1
    # - West (270°): sin=-1, cos=0

    # ========================================================================
    # WEATHER CODE - Binary encoding
    # ========================================================================
    # WHY? During training, you found that codes 63 and 65 are predictive
    # These codes represent moderate and heavy rain
    # Create a binary feature: 1 if code is 63 or 65, else 0

    weather_code = weather_data.get('weather_code', 0)
    if weather_code is None:
        weather_code = 0

    features['is_weather_code_63_or_65'] = int(weather_code == 63 or weather_code == 65)

    # ========================================================================
    # SEASONAL FEATURES - Cyclical month encoding
    # ========================================================================
    # WHY? Months are cyclical: December and January are close in weather
    # But as numbers, 12 and 1 seem far apart
    # Solution: Convert to sin/cos to capture seasonal patterns

    month = date_obj.month  # 1-12

    # Convert month to angle (0 to 2π)
    month_angle = 2 * np.pi * (month - 1) / 12

    features['season_sin'] = np.sin(month_angle)
    features['season_cos'] = np.cos(month_angle)

    # Example:
    # - January (1): angle=0, sin=0, cos=1
    # - April (4): angle=π/2, sin=1, cos=0
    # - July (7): angle=π, sin=0, cos=-1
    # - October (10): angle=3π/2, sin=-1, cos=0

    # ========================================================================
    # CONVERT TO NUMPY ARRAY
    # ========================================================================
    # Models expect features in a specific order
    # This order MUST match the order you used during training!

    feature_order = [
        'temperature_2m_max',
        'temperature_2m_min',
        'apparent_temperature_max',
        'apparent_temperature_min',
        'daylight_duration',
        'shortwave_radiation_sum',
        'et0_fao_evapotranspiration',
        'wind_speed_10m_max',
        'wind_gusts_10m_max',
        'wind_direction_sin',
        'wind_direction_cos',
        'is_weather_code_63_or_65',
        'season_sin',
        'season_cos',
    ]

    # Create array in correct order
    feature_values = [features[name] for name in feature_order]

    # Convert to 2D numpy array (shape: 1 x num_features)
    # Why 2D? sklearn expects 2D arrays (rows=samples, columns=features)
    X = np.array([feature_values])

    return X


# ============================================================================
# FUNCTION 4: PREPARE FEATURES FOR PRECIPITATION PREDICTION
# ============================================================================

def prepare_precipitation_features(weather_data: dict, date_obj: datetime) -> np.ndarray:
    """
    Transform raw weather data into features for precipitation prediction.

    Similar to prepare_rain_features, but with different features.
    Precipitation models might need different inputs than rain models.

    Args:
        weather_data (dict): Raw weather data from Open Meteo API
        date_obj (datetime): The input date (for seasonal features)

    Returns:
        np.ndarray: 2D array of features ready for the model
    """

    features = {}

    # Precipitation-related features (important for predicting future precipitation)
    features['precipitation_sum'] = weather_data.get('precipitation_sum', 0)
    features['precipitation_hours'] = weather_data.get('precipitation_hours', 0)

    # Temperature features
    features['temperature_2m_max'] = weather_data.get('temperature_2m_max', 0)
    features['temperature_2m_min'] = weather_data.get('temperature_2m_min', 0)
    features['apparent_temperature_max'] = weather_data.get('apparent_temperature_max', 0)
    features['apparent_temperature_min'] = weather_data.get('apparent_temperature_min', 0)

    # Solar features
    features['sunshine_duration'] = weather_data.get('sunshine_duration', 0)
    features['daylight_duration'] = weather_data.get('daylight_duration', 0)

    # Wind direction (circular encoding)
    wind_direction = weather_data.get('wind_direction_10m_dominant', 0)
    if wind_direction is None:
        wind_direction = 0
    wind_radians = np.radians(float(wind_direction))
    features['wind_direction_sin'] = np.sin(wind_radians)
    features['wind_direction_cos'] = np.cos(wind_radians)

    # Weather code (binary encoding)
    weather_code = weather_data.get('weather_code', 0)
    if weather_code is None:
        weather_code = 0
    features['is_weather_code_63_or_65'] = int(weather_code == 63 or weather_code == 65)

    # Seasonal features
    month = date_obj.month
    month_angle = 2 * np.pi * (month - 1) / 12
    features['season_sin'] = np.sin(month_angle)
    features['season_cos'] = np.cos(month_angle)

    # Feature order (MUST match training!)
    feature_order = [
        'precipitation_sum',
        'precipitation_hours',
        'temperature_2m_max',
        'temperature_2m_min',
        'apparent_temperature_max',
        'apparent_temperature_min',
        'sunshine_duration',
        'daylight_duration',
        'wind_direction_sin',
        'wind_direction_cos',
        'is_weather_code_63_or_65',
        'season_sin',
        'season_cos',
    ]

    # Convert to numpy array
    feature_values = [features[name] for name in feature_order]
    X = np.array([feature_values])

    return X


# ============================================================================
# FUNCTION 5: PREDICT RAIN
# ============================================================================

def predict_rain(date_str: str) -> dict:
    """
    Predict if it will rain exactly 7 days from the input date.

    THE COMPLETE PIPELINE:
    1. Parse input date
    2. Load models (if not already loaded)
    3. Fetch weather data for input date
    4. Prepare features (feature engineering)
    5. Scale features with StandardScaler
    6. Get prediction probability from model
    7. Apply threshold for binary classification
    8. Return formatted result

    Args:
        date_str (str): Input date in YYYY-MM-DD format

    Returns:
        dict: Prediction result in the format:
        {
            "input_date": "2024-09-15",
            "prediction": {
                "date": "2024-09-22",
                "will_rain": true
            }
        }

    Raises:
        ValueError: If date is invalid or weather data unavailable
        FileNotFoundError: If model files are missing
        RuntimeError: If prediction fails
    """

    # STEP 1: Parse the input date
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD format.")

    # Calculate prediction date (7 days ahead)
    prediction_date = date_obj + timedelta(days=RAIN_PREDICTION_DAYS)

    # STEP 2: Load models (cached after first load)
    model, scaler, threshold = load_rain_models()

    # STEP 3: Fetch weather data for the input date
    weather_data = fetch_weather_for_date(date_str)

    # STEP 4: Prepare features
    X = prepare_rain_features(weather_data, date_obj)

    # STEP 5: Scale features
    # StandardScaler transforms features to have mean=0 and std=1
    # This uses the SAME scaling parameters (mean/std) from training
    # CRITICAL: You must use the SAME scaler you fitted on training data!
    X_scaled = scaler.transform(X)

    # STEP 6: Get prediction probability
    # For classification models, predict_proba returns probabilities
    # Returns shape: (1, 2) for binary classification
    #   - Column 0: probability of class 0 (no rain)
    #   - Column 1: probability of class 1 (rain)
    # We want the probability of rain (column 1)
    probability = model.predict_proba(X_scaled)[0, 1]

    # STEP 7: Apply threshold for binary decision
    # If probability >= threshold, predict rain
    # Example: If probability=0.73 and threshold=0.5, predict rain
    will_rain = bool(probability >= threshold)

    # STEP 8: Format and return result
    return {
        "input_date": date_str,
        "prediction": {
            "date": prediction_date.strftime("%Y-%m-%d"),
            "will_rain": will_rain
        }
    }


# ============================================================================
# FUNCTION 6: PREDICT PRECIPITATION
# ============================================================================

def predict_precipitation(date_str: str) -> dict:
    """
    Predict cumulative precipitation (mm) for the next 3 days.

    Similar pipeline to predict_rain, but for regression.

    Args:
        date_str (str): Input date in YYYY-MM-DD format

    Returns:
        dict: Prediction result in the format:
        {
            "input_date": "2024-09-15",
            "prediction": {
                "start_date": "2024-09-16",
                "end_date": "2024-09-18",
                "precipitation_fall": "5.2"
            }
        }

    Raises:
        ValueError: If date is invalid or weather data unavailable
        FileNotFoundError: If model files are missing
        RuntimeError: If prediction fails
    """

    # STEP 1: Parse the input date
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD format.")

    # Calculate prediction range (next 3 days)
    start_date = date_obj + timedelta(days=1)
    end_date = date_obj + timedelta(days=PRECIPITATION_PREDICTION_DAYS)

    # STEP 2: Load models
    model, scaler = load_precipitation_models()

    # STEP 3: Fetch weather data
    weather_data = fetch_weather_for_date(date_str)

    # STEP 4: Prepare features
    X = prepare_precipitation_features(weather_data, date_obj)

    # STEP 5: Scale features
    X_scaled = scaler.transform(X)

    # STEP 6: Get prediction
    # For regression models, predict returns the predicted value
    # Returns shape: (1,) - a single predicted value
    precipitation_mm = model.predict(X_scaled)[0]

    # STEP 7: Ensure non-negative
    # Precipitation cannot be negative, so clip to minimum of 0
    precipitation_mm = max(0.0, float(precipitation_mm))

    # STEP 8: Format and return result
    # Note: precipitation_fall is returned as a string per assessment spec
    return {
        "input_date": date_str,
        "prediction": {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "precipitation_fall": f"{precipitation_mm:.1f}"
        }
    }


# ============================================================================
# UNDERSTANDING STANDARDSCALER
# ============================================================================
"""
StandardScaler is one of the most important preprocessing steps!

WHY WE NEED IT:
Different features have different scales:
- Temperature: 10-35°C
- Wind speed: 0-100 km/h
- Precipitation: 0-200mm
- Daylight: 35000-50000 seconds

Without scaling, the model might think large values are more important.
StandardScaler makes all features comparable.

HOW IT WORKS:
1. During training (in experiments repo):
   scaler = StandardScaler()
   scaler.fit(X_train)  # Learns mean and std for each feature
   X_train_scaled = scaler.transform(X_train)

2. For prediction (here in API):
   X_scaled = scaler.transform(X_new)  # Uses same mean/std from training

FORMULA:
scaled_value = (original_value - mean) / std

EXAMPLE:
Feature: temperature_2m_max
Training data: mean=22°C, std=5°C

Original value: 27°C
Scaled value: (27 - 22) / 5 = 1.0

Original value: 17°C
Scaled value: (17 - 22) / 5 = -1.0

After scaling:
- Values around the training mean → close to 0
- Values above the training mean → positive
- Values below the training mean → negative
- Most values between -3 and +3

CRITICAL: You MUST use the same scaler from training!
If you fit a new scaler on new data, the scaling will be different!
"""


# ============================================================================
# UNDERSTANDING MODEL PREDICTION
# ============================================================================
"""
CLASSIFICATION (Rain Prediction):
model.predict_proba(X) returns probabilities for each class

Example output:
[[0.27, 0.73]]  # 27% chance no rain, 73% chance rain

We extract the rain probability (second column):
probability = model.predict_proba(X)[0, 1]  # 0.73

Then apply threshold:
will_rain = probability >= 0.5  # True

REGRESSION (Precipitation Prediction):
model.predict(X) returns predicted values

Example output:
[5.2]  # Predicted 5.2mm of precipitation

We extract the value:
precipitation_mm = model.predict(X)[0]  # 5.2

Then ensure non-negative:
precipitation_mm = max(0, precipitation_mm)  # Can't be negative
"""


# ============================================================================
# TESTING THIS MODULE
# ============================================================================
"""
To test this module directly:

if __name__ == "__main__":
    # Test rain prediction
    try:
        result = predict_rain("2024-09-15")
        print("Rain prediction:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")

    # Test precipitation prediction
    try:
        result = predict_precipitation("2024-09-15")
        print("\nPrecipitation prediction:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
"""
