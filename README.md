# Weather Prediction API - Simple Example

Build and deploy a weather prediction API for Sydney using FastAPI.

---

## What You're Building

An API with 4 endpoints:
- `/` - Project info
- `/health/` - Health check
- `/predict/rain/?date=2024-09-15` - Rain prediction (7 days ahead)
- `/predict/precipitation/fall/?date=2024-09-15` - Precipitation prediction (3 days ahead)

---

## Quick Setup

### 1. Install Poetry (if needed)

```bash
pip install poetry
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Activate Environment
```bash
poetry env activate
# Copy the path and run:
source /path/to/venv/bin/activate
```

### 4. Add Your Models

Put your trained models in:
```
app/models/rain_or_not/
  ├── model.joblib
  ├── scaler.joblib (or whatever preprocessing you used)
  └── threshold.txt (optional, for classification)

app/models/precipitation_fall/
  ├── model.joblib
  └── scaler.joblib (or whatever preprocessing you used)
```

### 5. Run It

```bash
poetry run uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

---

## Project Structure

```
example/
├── app/
│   ├── main.py              # Your API endpoints (READ THIS FIRST)
│   ├── weather_api.py       # Gets weather data from Open Meteo
│   ├── predictor.py         # Loads models and makes predictions
│   └── models/              # Put your trained models here
├── pyproject.toml           # Poetry config
├── Dockerfile               # For deployment
└── README.md                # This file
```

---

## Understanding the Files

### app/main.py

This is your API. It has 4 endpoints:

```python
@app.get("/")
def home():
    # Returns project info

@app.get("/health/")
def health():
    # Returns "healthy"

@app.get("/predict/rain/")
def rain(date: str):
    # 1. Get weather data for that date
    # 2. Make prediction
    # 3. Return result

@app.get("/predict/precipitation/fall/")
def precipitation(date: str):
    # Same pattern
```

### app/weather_api.py

Gets weather data from Open Meteo:

```python
def get_weather(date_str):
    # Makes HTTP request to Open Meteo API
    # Returns weather data dictionary
```

### app/predictor.py

Loads your models and makes predictions:

```python
def predict_rain(date_str):
    # 1. Load model (cached after first load)
    # 2. Get weather data
    # 3. Prepare features (YOUR feature engineering here)
    # 4. Apply any preprocessing (scaler, etc)
    # 5. Make prediction
    # 6. Return result
```

**IMPORTANT:** The feature preparation in `predictor.py` must match exactly what you did in training!

---

## Key Concepts

### API Endpoints

An endpoint is a URL that does something:
- `/health/` → returns status
- `/predict/rain/?date=2024-09-15` → returns rain prediction

The `?date=2024-09-15` part is a query parameter.

### Preprocessing

Whatever you used in training (StandardScaler, MinMaxScaler, etc), you must:
1. Save it: `joblib.dump(scaler, 'scaler.joblib')`
2. Load it in API: `scaler = joblib.load('scaler.joblib')`
3. Use the SAME scaler - don't create a new one!

### Feature Engineering

Your features in the API must match training exactly:
- Same transformations
- Same order
- Same names

Example:
```python
# If you did this in training:
features = ['temp', 'wind', 'humidity']
X = data[features]

# Do the same in API:
weather_features = {
    'temp': weather_data['temperature_2m_max'],
    'wind': weather_data['wind_speed_10m_max'],
    'humidity': weather_data['relative_humidity']
}
X = np.array([[weather_features[f] for f in features]])
```

### Swagger Docs

FastAPI auto-creates docs at `/docs`. Use this to test your API!

---

## Testing

### Local Testing

```bash
poetry run uvicorn app.main:app --reload
```

Then visit:
- http://localhost:8000/docs (Swagger - test here!)
- http://localhost:8000/health/
- http://localhost:8000/predict/rain/?date=2024-09-15

### Docker Testing

```bash
docker build -t weather-api .
docker run -p 8000:8000 weather-api
```

---

## Deployment to Render

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Make repo **private** and add course staff as collaborators (Admin).

### Step 2: Deploy on Render

1. Go to render.com
2. Sign up with GitHub
3. New + → Web Service
4. Connect your repo
5. Settings:
   - Environment: Docker
   - Instance: Free
6. Deploy!

You'll get a URL like: `https://your-app.onrender.com`

---

## Common Issues

**"Module not found"**
```bash
poetry install
```

**"Model file not found"**
- Copy your model files to `app/models/`

**"Feature mismatch"**
- Your features must match training exactly
- Check feature names and order in `predictor.py`

**"Wrong predictions"**
- Using wrong scaler/preprocessing? Must use the saved one from training
- Features in wrong order?
- Date calculations wrong?

---

## What to Customize

You MUST customize these parts to match YOUR models:

### 1. app/predictor.py

Change the feature preparation to match your training:

```python
def prepare_features(weather_data):
    # THIS MUST MATCH YOUR TRAINING!
    features = {
        'temp': weather_data['temperature_2m_max'],
        # ... add your features
    }
    return features
```

### 2. Model Loading

If you used different file names or additional files:

```python
# Add any other files you need:
model = joblib.load('app/models/rain_or_not/model.joblib')
scaler = joblib.load('app/models/rain_or_not/scaler.joblib')
# encoder = joblib.load('app/models/rain_or_not/encoder.joblib')  # if you used one
```

### 3. Preprocessing Steps

Match whatever you did:

```python
# If you used StandardScaler:
X_scaled = scaler.transform(X)

# If you used MinMaxScaler:
X_scaled = scaler.transform(X)

# If you used something else:
X_processed = your_preprocessor.transform(X)
```

---

## Tips

- Read the code files - they have comments explaining what each part does
- Test locally before deploying
- Use Swagger docs (`/docs`) to test your API
- Check Render logs if something breaks
- Feature engineering must match training EXACTLY

---

## Need Help?

- Read error messages carefully
- Check the comments in the code files
- Look at your training notebooks to see what you did
- Test with simple dates first (e.g., 2024-01-01)

---

**That's it! Keep it simple and it'll work fine.**
