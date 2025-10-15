# Weather Prediction API - Complete Beginner's Guide

**📖 This is a simplified example implementation for AT2 Weather Prediction API**

This guide will walk you through **EVERY STEP** of building and deploying your weather prediction API. Take your time, read everything carefully, and follow along step-by-step.

---

## 📚 Table of Contents

1. [What You're Building](#what-youre-building)
2. [Technologies Used](#technologies-used)
3. [Project Structure](#project-structure)
4. [Understanding the Code](#understanding-the-code)
5. [Setup Instructions](#setup-instructions)
6. [Testing Your API Locally](#testing-your-api-locally)
7. [Understanding Machine Learning Components](#understanding-machine-learning-components)
8. [Deployment to Render](#deployment-to-render)
9. [Common Issues & Solutions](#common-issues--solutions)

---

## 🎯 What You're Building

You are creating a **Weather Prediction API** that:

1. **Takes a date as input** (example: 2024-09-15)
2. **Makes two types of predictions:**
   - **Rain Prediction**: Will it rain exactly 7 days from the input date? (Yes/No)
   - **Precipitation Prediction**: How much rain (in mm) will fall in the next 3 days?
3. **Returns predictions as JSON** that can be accessed via a web browser or other applications

### Real-World Example:
- You give the API: `2024-09-15`
- **Rain prediction** tells you: "Yes, it will rain on 2024-09-22"
- **Precipitation prediction** tells you: "5.2mm of rain will fall between 2024-09-16 and 2024-09-18"

---

## 🔧 Technologies Used

### 1. **FastAPI** - The Web Framework
- **What it is**: A modern Python framework for building web APIs
- **Why we use it**: It's fast, easy to learn, and automatically creates documentation
- **What it does**: Receives HTTP requests (from web browsers), processes them, and sends back responses

### 2. **Open Meteo API** - Weather Data Source
- **What it is**: A free weather data service that provides historical weather information
- **Why we use it**: We need historical weather data to make predictions
- **What it does**: When you give it a date, it returns weather data (temperature, wind, rain, etc.) for Sydney

### 3. **Scikit-learn** - Machine Learning Library
- **What it is**: A Python library for machine learning
- **Why we use it**: To load our trained models and make predictions
- **What it does**: Takes weather data, processes it, and predicts future weather

### 4. **StandardScaler** - Data Preprocessing
- **What it is**: A tool that normalizes your data (makes all numbers similar in scale)
- **Why we use it**: Machine learning models work better when all input values are in a similar range
- **Example**: Temperature might be 20-30, but wind speed might be 0-100. StandardScaler makes them comparable.

### 5. **Joblib** - Model Storage
- **What it is**: A library for saving and loading Python objects
- **Why we use it**: To save our trained models to files and load them later
- **What it does**: Saves models as `.joblib` files that can be loaded instantly

### 6. **Docker** - Containerization
- **What it is**: A tool that packages your application and all its dependencies together
- **Why we use it**: So your app runs the same way everywhere (your computer, Render's servers, anywhere)
- **What it does**: Creates a "container" with Python, your code, and all libraries needed

### 7. **Render** - Hosting Platform
- **What it is**: A cloud service that runs your application on the internet
- **Why we use it**: So anyone can access your API from anywhere
- **What it does**: Takes your Docker container and makes it available at a public URL

### 8. **Uvicorn** - ASGI Server
- **What it is**: A lightning-fast server that runs your FastAPI application
- **Why we use it**: FastAPI needs a server to handle incoming web requests
- **What it does**: Listens for HTTP requests and passes them to your FastAPI app

---

## 📁 Project Structure

```
example/
├── README.md                          # This file - your complete guide
├── DEPLOYMENT_GUIDE.md                # Detailed deployment instructions
├── requirements.txt                   # List of all Python packages needed
├── Dockerfile                         # Instructions for Docker to build your app
├── app/
│   ├── main.py                       # Main FastAPI application (API endpoints)
│   ├── weather_fetcher.py            # Fetches weather data from Open Meteo API
│   ├── model_predictor.py            # Loads models and makes predictions
│   └── models/
│       ├── rain_or_not/
│       │   ├── model.joblib          # Your trained rain prediction model
│       │   ├── scaler.joblib         # StandardScaler for rain model
│       │   └── threshold.txt         # Optimal threshold for classification
│       └── precipitation_fall/
│           ├── model.joblib          # Your trained precipitation model
│           └── scaler.joblib         # StandardScaler for precipitation model
```

### What Each File Does:

- **main.py**: The heart of your API. Defines all endpoints (/, /health/, /predict/rain/, etc.)
- **weather_fetcher.py**: Gets weather data from Open Meteo API for any date
- **model_predictor.py**: Loads your trained models and makes predictions
- **model.joblib**: Your trained machine learning model (you create this in the experiments repo)
- **scaler.joblib**: The StandardScaler fitted on your training data
- **threshold.txt**: For rain prediction, the optimal probability threshold to classify rain/no-rain
- **requirements.txt**: Lists all Python packages (FastAPI, scikit-learn, etc.)
- **Dockerfile**: Tells Docker how to build and run your application

---

## 🧠 Understanding the Code

### 1. main.py - The API Application

This file creates your FastAPI application and defines all the endpoints.

**Key Concepts:**

#### What is an Endpoint?
An endpoint is a URL path that does something specific. Think of it like a function you can call over the internet.

**Example Endpoints:**
- `GET /` - Shows information about your API
- `GET /health/` - Checks if the API is running
- `GET /predict/rain/?date=2024-09-15` - Predicts rain for a specific date

#### What is a GET Request?
- A GET request is when you ask a server for information
- You type a URL in your browser → that's a GET request
- Format: `http://localhost:8000/predict/rain/?date=2024-09-15`
  - `http://localhost:8000` - where the server is running
  - `/predict/rain/` - the endpoint path
  - `?date=2024-09-15` - the query parameter (input)

#### What is JSON?
JSON (JavaScript Object Notation) is a format for sending data. It looks like this:

```json
{
  "input_date": "2024-09-15",
  "prediction": {
    "date": "2024-09-22",
    "will_rain": true
  }
}
```

### 2. weather_fetcher.py - Getting Weather Data

This file fetches historical weather data from Open Meteo API.

**How it Works:**

1. **You provide a date**: "2024-09-15"
2. **It builds a URL**: `https://archive-api.open-meteo.com/v1/archive?latitude=-33.8678&longitude=151.2073&start_date=2024-09-15&end_date=2024-09-15&daily=temperature_2m_max,...`
3. **Sends HTTP request** to Open Meteo
4. **Receives JSON response** with weather data
5. **Extracts the data** and returns it as a Python dictionary

**Important Parameters:**
- `latitude` and `longitude`: Sydney's coordinates
- `start_date` and `end_date`: The date you want weather for
- `daily`: List of weather variables (temperature, wind, rain, etc.)

### 3. model_predictor.py - Making Predictions

This file loads your trained models and makes predictions.

**The Prediction Pipeline:**

```
Input Date → Fetch Weather Data → Prepare Features → Scale Features → Model Prediction → Return Result
```

**Step-by-Step:**

1. **Load the model** (first time only, then cached in memory)
2. **Fetch weather data** for the input date
3. **Prepare features**: Transform raw weather data into model inputs
   - Example: Convert wind direction (0-360°) to sin/cos values
4. **Scale features**: Use StandardScaler to normalize values
5. **Make prediction**: Pass scaled features to the model
6. **Format response**: Return prediction as JSON

**StandardScaler Explained:**

Imagine you have:
- Temperature: 25°C (range: 10-40)
- Wind speed: 15 km/h (range: 0-100)
- Precipitation: 5mm (range: 0-200)

StandardScaler transforms these to:
- Temperature: 0.5 (range: -2 to 2)
- Wind speed: -0.3 (range: -2 to 2)
- Precipitation: -0.1 (range: -2 to 2)

This makes them comparable and helps the model work better.

---

## 🚀 Setup Instructions

### Prerequisites

Before you start, install:

1. **Python 3.9 or higher**
   - Check: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. **pip** (Python package installer)
   - Usually comes with Python
   - Check: `pip --version` or `pip3 --version`

3. **Git** (for version control)
   - Check: `git --version`
   - Download: https://git-scm.com/

### Step 1: Create a Virtual Environment

A virtual environment keeps your project dependencies separate from other projects.

```bash
# Navigate to the example folder
cd example/

# Create a virtual environment named 'venv'
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# You should see (venv) at the start of your terminal line
```

### Step 2: Install Dependencies

```bash
# Make sure you're in the example/ folder with venv activated
pip install -r requirements.txt

# This installs:
# - fastapi (web framework)
# - uvicorn (server)
# - scikit-learn (machine learning)
# - pandas (data processing)
# - requests (HTTP requests)
# - joblib (model loading)
# - and others...
```

### Step 3: Add Your Trained Models

**IMPORTANT:** You need to train your models first (in the experiments repo), then copy them here.

Your models should be saved as:
- `app/models/rain_or_not/model.joblib` - your trained rain classification model
- `app/models/rain_or_not/scaler.joblib` - StandardScaler fitted on your training data
- `app/models/rain_or_not/threshold.txt` - optimal threshold (example: 0.5)
- `app/models/precipitation_fall/model.joblib` - your trained precipitation regression model
- `app/models/precipitation_fall/scaler.joblib` - StandardScaler for precipitation

**How to save models in your experiments:**

```python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

# After training your model
model = LogisticRegression()
scaler = StandardScaler()

# Fit them on your training data
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
model.fit(X_train_scaled, y_train)

# Save them
joblib.dump(model, 'model.joblib')
joblib.dump(scaler, 'scaler.joblib')

# For threshold (find optimal threshold using your validation set)
with open('threshold.txt', 'w') as f:
    f.write('0.5')  # Replace with your optimal threshold
```

---

## 🧪 Testing Your API Locally

### Step 1: Start the Server

```bash
# Make sure you're in example/ folder with venv activated
uvicorn app.main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
```

**What `--reload` does**: Automatically restarts the server when you change code (useful during development)

### Step 2: Test in Your Browser

Open your web browser and visit:

#### 1. Root Endpoint
- **URL**: http://localhost:8000/
- **What you'll see**: JSON with project information, endpoints, and expected inputs/outputs

#### 2. Health Check
- **URL**: http://localhost:8000/health/
- **What you'll see**: Status message confirming API is running

#### 3. Rain Prediction
- **URL**: http://localhost:8000/predict/rain/?date=2024-09-15
- **What you'll see**: JSON prediction for rain 7 days from 2024-09-15

```json
{
  "input_date": "2024-09-15",
  "prediction": {
    "date": "2024-09-22",
    "will_rain": true
  }
}
```

#### 4. Precipitation Prediction
- **URL**: http://localhost:8000/predict/precipitation/fall/?date=2024-09-15
- **What you'll see**: JSON prediction for precipitation in next 3 days

```json
{
  "input_date": "2024-09-15",
  "prediction": {
    "start_date": "2024-09-16",
    "end_date": "2024-09-18",
    "precipitation_fall": "5.2"
  }
}
```

### Step 3: Explore Swagger Documentation

FastAPI automatically creates interactive documentation!

- **URL**: http://localhost:8000/docs

**What is Swagger?**
- Swagger (OpenAPI) is a tool that automatically generates interactive API documentation
- You can see all your endpoints, their inputs/outputs, and even TEST them directly in the browser
- FastAPI generates this for FREE - you don't need to write any extra code

**How to use Swagger UI:**
1. Go to http://localhost:8000/docs
2. You'll see all your endpoints listed
3. Click on any endpoint (e.g., GET /predict/rain/)
4. Click "Try it out"
5. Enter a date (e.g., 2024-09-15)
6. Click "Execute"
7. See the response below!

This is SUPER useful for testing and showing how your API works.

---

## 🧠 Understanding Machine Learning Components

### What is a Machine Learning Model?

Think of a model as a trained function:
- **Input**: Weather conditions on a specific day
- **Output**: Prediction about future weather

**How it's trained:**
1. You give it thousands of examples: "On this day, the weather was X, and 7 days later it rained/didn't rain"
2. The model learns patterns: "When temperature is high and humidity is low, it usually doesn't rain"
3. After training, you can give it new weather data and it predicts the future

### The Prediction Pipeline Explained

#### 1. Feature Engineering
Raw weather data needs to be transformed into "features" the model can understand.

**Example:**
- **Raw data**: `wind_direction = 270°` (pointing West)
- **Problem**: The model doesn't understand that 0° and 360° are the same direction
- **Solution**: Convert to circular encoding
  - `wind_direction_sin = sin(270° * π/180) = -1`
  - `wind_direction_cos = cos(270° * π/180) = 0`

#### 2. StandardScaler - The Normalizer

**Why we need it:**
- Features have different scales:
  - Temperature: 10-35°C
  - Wind speed: 0-100 km/h
  - Daylight hours: 10-14 hours
- Models perform better when all features are on similar scales

**How it works:**
```python
# Training phase (in experiments repo)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)  # Learns the mean and std of each feature
X_train_scaled = scaler.transform(X_train)  # Applies transformation

# Save the scaler
joblib.dump(scaler, 'scaler.joblib')

# Prediction phase (in API)
scaler = joblib.load('scaler.joblib')
X_new_scaled = scaler.transform(X_new)  # Uses same mean/std from training
```

**Formula:**
```
scaled_value = (original_value - mean) / standard_deviation
```

**Example:**
- Original temperature: 25°C
- Mean from training: 20°C
- Std from training: 5°C
- Scaled: (25 - 20) / 5 = 1.0

#### 3. Model Inference (Making Predictions)

**For Rain Prediction (Classification):**
```python
# Model returns probabilities
probability = model.predict_proba(X_scaled)[0, 1]  # Probability of rain
# Example: probability = 0.73 (73% chance of rain)

# Apply threshold
threshold = 0.5  # Or your optimal threshold
will_rain = probability >= threshold  # True if >= 0.5
```

**For Precipitation Prediction (Regression):**
```python
# Model returns continuous value
precipitation_mm = model.predict(X_scaled)[0]
# Example: precipitation_mm = 5.2

# Ensure non-negative (precipitation can't be negative)
precipitation_mm = max(0, precipitation_mm)
```

### What is a Threshold?

For rain prediction, the model outputs a probability (0.0 to 1.0). You need to decide: "At what probability do we say it will rain?"

- **Threshold = 0.5**: If probability ≥ 0.5, predict rain
- **Lower threshold (0.3)**: More sensitive, predicts rain more often (fewer missed rain days, but more false alarms)
- **Higher threshold (0.7)**: More conservative, predicts rain less often (fewer false alarms, but might miss some rain days)

You should find the optimal threshold using your validation set to balance precision and recall.

---

## 🌐 Deployment to Render

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete step-by-step deployment instructions.

**Quick Overview:**

1. **Create a GitHub repository** and push your code
2. **Sign up for Render** (free tier)
3. **Create a new Web Service** on Render
4. **Connect your GitHub repo**
5. **Select Docker** as the deployment method
6. **Click Deploy**
7. **Wait 5-10 minutes** for deployment
8. **Access your API** at the provided URL

Your API will be live at: `https://your-app-name.onrender.com`

---

## ❓ Common Issues & Solutions

### Issue 1: "Module not found" errors

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure virtual environment is activated
# You should see (venv) at start of terminal
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: "Model file not found"

**Problem**: `FileNotFoundError: model.joblib not found`

**Solution**:
- Make sure you've copied your trained models to the correct folders
- Check file names: `model.joblib`, `scaler.joblib`, `threshold.txt`
- Check folder structure: `app/models/rain_or_not/` and `app/models/precipitation_fall/`

### Issue 3: "Cannot fetch data for future date"

**Problem**: `ValueError: Cannot fetch data for future date`

**Solution**:
- Open Meteo only has historical data (past dates)
- Use dates before today (in Sydney timezone)
- Example: If today is 2025-10-15 in Sydney, use dates like 2024-09-15

### Issue 4: Port already in use

**Problem**: `ERROR: [Errno 48] Address already in use`

**Solution**:
```bash
# Kill the process using port 8000
# On Mac/Linux:
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### Issue 5: StandardScaler feature mismatch

**Problem**: `ValueError: X has 10 features, but StandardScaler expected 11`

**Solution**:
- Make sure the features you create in `model_predictor.py` match exactly what you used during training
- Check the order of features - they must be in the same order
- Common issue: Missing a feature or adding an extra one

**Check your features:**
```python
# In model_predictor.py, make sure your feature list matches training
features = [
    'temperature_max',
    'temperature_min',
    'wind_speed',
    # ... should match your training exactly
]
```

### Issue 6: Swagger docs not showing

**Problem**: Can't access http://localhost:8000/docs

**Solution**:
- Make sure the server is running (check terminal for errors)
- Try http://127.0.0.1:8000/docs instead
- Clear browser cache
- Try a different browser

### Issue 7: Render deployment fails

**Problem**: Deployment fails on Render

**Common causes & solutions**:

1. **Missing Dockerfile**
   - Make sure `Dockerfile` is in your repository root

2. **Wrong port**
   - Render expects port 8000
   - Check your `Dockerfile` CMD: `"--port", "8000"`

3. **Large model files**
   - GitHub has 100MB file limit
   - Use Git LFS for large files: https://git-lfs.github.com/

4. **Dependency errors**
   - Check your `requirements.txt` has all dependencies
   - Try `pip freeze > requirements.txt` to capture everything

---

## 📝 Next Steps

1. **Test thoroughly locally** - Try different dates, check error handling
2. **Write tests** - Create test cases for your endpoints (optional but good practice)
3. **Deploy to Render** - Follow the deployment guide
4. **Document everything** - Update this README with your specific details
5. **Test production** - Make sure deployed API works correctly
6. **Submit** - Prepare your submission with all required files

---

## 🆘 Getting Help

If you're stuck:

1. **Read error messages carefully** - They usually tell you what's wrong
2. **Check the console/terminal** - Look for error logs
3. **Use Swagger docs** - Test endpoints and see what responses you get
4. **Google the error** - Someone else has probably had the same issue
5. **Check FastAPI docs** - https://fastapi.tiangolo.com/
6. **Check scikit-learn docs** - https://scikit-learn.org/

---

## 🎓 Key Concepts to Remember

1. **API Endpoint**: A URL path that does something (like a function you call over the internet)
2. **GET Request**: Asking a server for information
3. **JSON**: A format for sending data between client and server
4. **StandardScaler**: Normalizes features to similar scales
5. **Model Inference**: Using a trained model to make predictions on new data
6. **Docker**: Packages your app so it runs the same everywhere
7. **Swagger/OpenAPI**: Automatic interactive documentation for your API

---

**Good luck! Take it step by step, and you'll get there! 🚀**
