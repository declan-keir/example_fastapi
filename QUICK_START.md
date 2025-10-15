# Quick Start Guide

**Get your API running in 5 minutes!**

This is a condensed version of the main README for quick reference.

---

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

### 2. Add Your Models

Copy your trained model files to:
- `app/models/rain_or_not/model.joblib`
- `app/models/rain_or_not/scaler.joblib`
- `app/models/rain_or_not/threshold.txt`
- `app/models/precipitation_fall/model.joblib`
- `app/models/precipitation_fall/scaler.joblib`

### 3. Run Locally

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs to test!

### 4. Deploy to Render

1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Connect your GitHub repo
5. Click Deploy

Done! 🎉

---

## 📁 File Checklist

- [ ] `app/main.py` - API endpoints
- [ ] `app/weather_fetcher.py` - Fetch weather data
- [ ] `app/model_predictor.py` - Make predictions
- [ ] `requirements.txt` - Dependencies
- [ ] `Dockerfile` - Deployment config
- [ ] Model files in `app/models/`

---

## 🧪 Test Endpoints

**Locally:**
- http://localhost:8000/
- http://localhost:8000/health/
- http://localhost:8000/predict/rain/?date=2024-09-15
- http://localhost:8000/predict/precipitation/fall/?date=2024-09-15
- http://localhost:8000/docs (Swagger)

**After deployment:**
Replace `localhost:8000` with your Render URL: `your-app.onrender.com`

---

## 🐛 Common Issues

**"Module not found"**
→ Run `pip install -r requirements.txt`

**"Model file not found"**
→ Copy your .joblib files to `app/models/`

**"Cannot fetch future date"**
→ Use past dates only (before today)

**Port already in use**
→ Kill the process or use different port: `--port 8001`

---

## 📚 Full Documentation

For detailed explanations:
- [README.md](README.md) - Complete guide
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Render deployment
- Model folders - READMEs with training instructions

---

**Need help?** Read the error message carefully - it usually tells you what's wrong!
