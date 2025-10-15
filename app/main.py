"""
Main FastAPI Application for Weather Prediction API

This file defines all the API endpoints (URLs) that users can access.
Think of endpoints as functions that can be called over the internet.

Author: Your Name
Date: 2025
"""

# ============================================================================
# IMPORTS - Libraries we need
# ============================================================================

from fastapi import FastAPI, HTTPException, Query
from datetime import datetime

# Import our custom modules (files we created)
from weather_fetcher import fetch_weather_for_date
from model_predictor import predict_rain, predict_precipitation


# ============================================================================
# CREATE THE FASTAPI APPLICATION
# ============================================================================

# This creates your API application
# Think of it as creating a website that responds with data instead of HTML
app = FastAPI(
    title="Weather Prediction API",  # Name shown in documentation
    version="1.0.0",  # Your API version
    description="Predicts rain and precipitation for Sydney, Australia using machine learning"
)


# ============================================================================
# ENDPOINT 1: ROOT / HOME PAGE
# ============================================================================

@app.get("/")
def home():
    """
    Root endpoint - shows information about the API

    When someone visits: http://localhost:8000/
    They will see this information

    Returns:
        dict: JSON with project information and available endpoints
    """
    return {
        "project": "Weather Prediction API for Open Meteo",
        "location": "Sydney, Australia (-33.8678, 151.2073)",
        "description": "ML-based weather predictions for Sydney",

        # List of available endpoints
        "endpoints": [
            {
                "path": "/",
                "method": "GET",
                "description": "This page - API information"
            },
            {
                "path": "/health/",
                "method": "GET",
                "description": "Check if API is running"
            },
            {
                "path": "/predict/rain/",
                "method": "GET",
                "description": "Predict if it will rain 7 days from input date",
                "example": "/predict/rain/?date=2024-09-15"
            },
            {
                "path": "/predict/precipitation/fall/",
                "method": "GET",
                "description": "Predict precipitation for next 3 days",
                "example": "/predict/precipitation/fall/?date=2024-09-15"
            }
        ],

        # Input format
        "input_format": {
            "parameter": "date",
            "format": "YYYY-MM-DD",
            "example": "2024-09-15",
            "note": "Date must be in the past (historical data only)"
        },

        # Example outputs
        "example_outputs": {
            "rain_prediction": {
                "input_date": "2024-09-15",
                "prediction": {
                    "date": "2024-09-22",
                    "will_rain": True
                }
            },
            "precipitation_prediction": {
                "input_date": "2024-09-15",
                "prediction": {
                    "start_date": "2024-09-16",
                    "end_date": "2024-09-18",
                    "precipitation_fall": "5.2"
                }
            }
        },

        # Your GitHub repository
        "github": "https://github.com/YOUR_USERNAME/YOUR_REPO",

        # Link to interactive documentation
        "documentation": "/docs"
    }


# ============================================================================
# ENDPOINT 2: HEALTH CHECK
# ============================================================================

@app.get("/health/")
def health_check():
    """
    Health check endpoint - confirms the API is running

    When someone visits: http://localhost:8000/health/
    They will see a status message

    This is useful for:
    - Checking if the server is up
    - Monitoring tools (like Render's health checks)
    - Quick testing

    Returns:
        dict: JSON with status message
    """
    return {
        "status": "healthy",
        "message": "Weather Prediction API is running successfully!",
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# ENDPOINT 3: RAIN PREDICTION
# ============================================================================

@app.get("/predict/rain/")
def rain_prediction(
    date: str = Query(
        ...,  # ... means this parameter is required
        description="Date in YYYY-MM-DD format (must be a past date)",
        example="2024-09-15"
    )
):
    """
    Predict if it will rain exactly 7 days from the input date

    HOW IT WORKS:
    1. User provides a date (example: 2024-09-15)
    2. We fetch weather data for that date from Open Meteo API
    3. We prepare the data (feature engineering)
    4. We use our trained model to predict if it will rain 7 days later
    5. We return the prediction as JSON

    Example usage:
        http://localhost:8000/predict/rain/?date=2024-09-15

    Args:
        date (str): Input date in YYYY-MM-DD format

    Returns:
        dict: JSON with rain prediction
        {
            "input_date": "2024-09-15",
            "prediction": {
                "date": "2024-09-22",
                "will_rain": true
            }
        }

    Raises:
        HTTPException: If date is invalid or prediction fails
    """

    # STEP 1: Validate the date format
    # Try to parse the date string to make sure it's valid
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        # If date parsing fails, return error to user
        raise HTTPException(
            status_code=400,  # 400 = Bad Request (user's fault)
            detail=f"Invalid date format: '{date}'. Please use YYYY-MM-DD format (example: 2024-09-15)"
        )

    # STEP 2: Make the prediction
    # Call our predict_rain function from model_predictor.py
    try:
        result = predict_rain(date)
        return result

    except ValueError as e:
        # ValueError = something wrong with the input or data
        # Example: future date, missing data
        raise HTTPException(
            status_code=400,  # 400 = Bad Request
            detail=str(e)
        )

    except FileNotFoundError as e:
        # FileNotFoundError = model files missing
        raise HTTPException(
            status_code=500,  # 500 = Internal Server Error (our fault)
            detail=f"Model files not found. Please ensure models are properly deployed. Error: {str(e)}"
        )

    except Exception as e:
        # Any other unexpected error
        raise HTTPException(
            status_code=500,  # 500 = Internal Server Error
            detail=f"An error occurred during prediction: {str(e)}"
        )


# ============================================================================
# ENDPOINT 4: PRECIPITATION PREDICTION
# ============================================================================

@app.get("/predict/precipitation/fall/")
def precipitation_prediction(
    date: str = Query(
        ...,  # ... means this parameter is required
        description="Date in YYYY-MM-DD format (must be a past date)",
        example="2024-09-15"
    )
):
    """
    Predict cumulative precipitation (mm) for the next 3 days

    HOW IT WORKS:
    1. User provides a date (example: 2024-09-15)
    2. We fetch weather data for that date from Open Meteo API
    3. We prepare the data (feature engineering)
    4. We use our trained model to predict precipitation for next 3 days
    5. We return the prediction as JSON

    Example usage:
        http://localhost:8000/predict/precipitation/fall/?date=2024-09-15

    Args:
        date (str): Input date in YYYY-MM-DD format

    Returns:
        dict: JSON with precipitation prediction
        {
            "input_date": "2024-09-15",
            "prediction": {
                "start_date": "2024-09-16",
                "end_date": "2024-09-18",
                "precipitation_fall": "5.2"
            }
        }

    Raises:
        HTTPException: If date is invalid or prediction fails
    """

    # STEP 1: Validate the date format
    # Try to parse the date string to make sure it's valid
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        # If date parsing fails, return error to user
        raise HTTPException(
            status_code=400,  # 400 = Bad Request (user's fault)
            detail=f"Invalid date format: '{date}'. Please use YYYY-MM-DD format (example: 2024-09-15)"
        )

    # STEP 2: Make the prediction
    # Call our predict_precipitation function from model_predictor.py
    try:
        result = predict_precipitation(date)
        return result

    except ValueError as e:
        # ValueError = something wrong with the input or data
        # Example: future date, missing data
        raise HTTPException(
            status_code=400,  # 400 = Bad Request
            detail=str(e)
        )

    except FileNotFoundError as e:
        # FileNotFoundError = model files missing
        raise HTTPException(
            status_code=500,  # 500 = Internal Server Error (our fault)
            detail=f"Model files not found. Please ensure models are properly deployed. Error: {str(e)}"
        )

    except Exception as e:
        # Any other unexpected error
        raise HTTPException(
            status_code=500,  # 500 = Internal Server Error
            detail=f"An error occurred during prediction: {str(e)}"
        )


# ============================================================================
# WHAT HAPPENS WHEN YOU RUN THIS FILE?
# ============================================================================
"""
When you run: uvicorn app.main:app --reload

1. Uvicorn (the server) starts
2. It loads this file (main.py)
3. It looks for the 'app' variable (our FastAPI instance)
4. It starts listening for HTTP requests on port 8000
5. When a request comes in (example: GET /predict/rain/?date=2024-09-15):
   - Uvicorn receives it
   - FastAPI routes it to the correct function (rain_prediction)
   - The function executes
   - FastAPI converts the return value to JSON
   - Uvicorn sends the JSON response back to the user

That's it! Your API is now running and ready to receive requests.
"""


# ============================================================================
# HTTP STATUS CODES EXPLAINED
# ============================================================================
"""
You'll see these status codes in the code above. Here's what they mean:

200 OK - Everything worked perfectly
    Example: Successfully predicted rain

400 Bad Request - The user sent invalid data
    Example: Wrong date format, future date

404 Not Found - The resource doesn't exist
    Example: Wrong URL path

500 Internal Server Error - Something went wrong on our side
    Example: Model file missing, code bug

503 Service Unavailable - External service is down
    Example: Open Meteo API is not responding
"""


# ============================================================================
# TESTING YOUR API
# ============================================================================
"""
After starting the server, test these URLs in your browser:

1. Home page:
   http://localhost:8000/

2. Health check:
   http://localhost:8000/health/

3. Rain prediction:
   http://localhost:8000/predict/rain/?date=2024-09-15

4. Precipitation prediction:
   http://localhost:8000/predict/precipitation/fall/?date=2024-09-15

5. Interactive documentation (Swagger):
   http://localhost:8000/docs

   This is SUPER useful! You can:
   - See all endpoints
   - Try them out directly in the browser
   - See request/response formats
   - Test different inputs
"""
