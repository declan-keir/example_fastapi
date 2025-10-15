"""
Simple FastAPI application for weather predictions.

This file defines your API endpoints. Read through it to understand how it works.
"""

from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from predictor import predict_rain, predict_precipitation

# Create the API
app = FastAPI(
    title="Weather Prediction API",
    description="Predicts rain and precipitation for Sydney"
)


@app.get("/")
def home():
    """
    Root endpoint - shows info about your API
    """
    return {
        "project": "Weather Prediction API",
        "endpoints": [
            "GET / - This page",
            "GET /health/ - Health check",
            "GET /predict/rain/?date=YYYY-MM-DD - Rain prediction",
            "GET /predict/precipitation/fall/?date=YYYY-MM-DD - Precipitation prediction"
        ],
        "example": "http://localhost:8000/predict/rain/?date=2024-09-15",
        "docs": "/docs"
    }


@app.get("/health/")
def health():
    """
    Health check - used by Render to check if your app is running
    """
    return {"status": "healthy"}


@app.get("/predict/rain/")
def rain_prediction(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    """
    Predicts if it will rain 7 days from the given date.

    Example: /predict/rain/?date=2024-09-15
    Returns prediction for 2024-09-22
    """
    try:
        # Validate date format
        datetime.strptime(date, "%Y-%m-%d")

        # Make prediction
        result = predict_rain(date)
        return result

    except ValueError as e:
        # Bad date format or other validation error
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        # Model files missing
        raise HTTPException(status_code=404, detail=f"Model not found: {str(e)}")
    except Exception as e:
        # Something else went wrong
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/predict/precipitation/fall/")
def precipitation_prediction(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    """
    Predicts precipitation for the next 3 days from the given date.

    Example: /predict/precipitation/fall/?date=2024-09-15
    Returns prediction for 2024-09-16 to 2024-09-18
    """
    try:
        # Validate date format
        datetime.strptime(date, "%Y-%m-%d")

        # Make prediction
        result = predict_precipitation(date)
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Model not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
