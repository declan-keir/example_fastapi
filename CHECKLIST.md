# Complete Assessment Checklist

**Use this to track your progress through the FastAPI part of AT2**

---

## 📚 Phase 1: Understanding (Day 1)

- [ ] Read START_HERE.md completely
- [ ] Read README.md (all sections)
- [ ] Read through app/main.py with all comments
- [ ] Read through app/weather_fetcher.py
- [ ] Read through app/model_predictor.py
- [ ] Understand what StandardScaler does
- [ ] Understand feature engineering concepts
- [ ] Understand API endpoints and HTTP methods
- [ ] Understand Swagger documentation

**Time estimate**: 3-4 hours

---

## ⚙️ Phase 2: Environment Setup (Day 1-2)

### Virtual Environment
- [ ] Python 3.9+ installed and verified
- [ ] Created virtual environment (`python -m venv venv`)
- [ ] Activated virtual environment
- [ ] Installed all dependencies (`pip install -r requirements.txt`)
- [ ] No errors during installation

### Project Structure
- [ ] Copied entire example folder to your workspace
- [ ] All folders exist (app, app/models, etc.)
- [ ] All Python files exist
- [ ] Configuration files exist

**Time estimate**: 30 minutes

---

## 🤖 Phase 3: Add Your Models (Day 2)

### Train Models (in experiments repo)
- [ ] Rain prediction model trained and tested
- [ ] Precipitation prediction model trained and tested
- [ ] StandardScalers fitted on training data
- [ ] Optimal threshold found for rain model
- [ ] Models saved as .joblib files
- [ ] Performance documented

### Copy Models to API Repo
- [ ] app/models/rain_or_not/model.joblib exists
- [ ] app/models/rain_or_not/scaler.joblib exists
- [ ] app/models/rain_or_not/threshold.txt exists (contains single number 0-1)
- [ ] app/models/precipitation_fall/model.joblib exists
- [ ] app/models/precipitation_fall/scaler.joblib exists
- [ ] Can load all models without errors

### Verify Models
```python
import joblib
rain_model = joblib.load('app/models/rain_or_not/model.joblib')
rain_scaler = joblib.load('app/models/rain_or_not/scaler.joblib')
with open('app/models/rain_or_not/threshold.txt') as f:
    threshold = float(f.read())
print(f"✓ Rain model loaded: {type(rain_model).__name__}")
print(f"✓ Rain scaler loaded: {type(rain_scaler).__name__}")
print(f"✓ Threshold: {threshold}")
```

- [ ] Above code runs without errors

**Time estimate**: 1-2 hours

---

## 🔧 Phase 4: Customize Code (Day 2-3)

### Update Feature Engineering

Review `app/model_predictor.py`:

- [ ] Features in `prepare_rain_features()` match your training
- [ ] Feature order matches your training exactly
- [ ] All transformations match (wind direction, weather code, etc.)
- [ ] Features in `prepare_precipitation_features()` match your training
- [ ] Feature order matches your training exactly

### Update Configuration

Review `app/main.py`:

- [ ] Update github.txt with your repo URL
- [ ] Update any project-specific information
- [ ] Verify all endpoint paths are correct

**Time estimate**: 2-3 hours

---

## 🧪 Phase 5: Local Testing (Day 3)

### Start Server
```bash
uvicorn app.main:app --reload
```

- [ ] Server starts without errors
- [ ] See "Application startup complete" message
- [ ] Models load successfully (check console output)

### Test Endpoints in Browser

Test each URL and verify response:

- [ ] http://localhost:8000/ (project info)
- [ ] http://localhost:8000/health/ (health check)
- [ ] http://localhost:8000/predict/rain/?date=2024-09-15 (rain prediction)
- [ ] http://localhost:8000/predict/precipitation/fall/?date=2024-09-15 (precipitation)

### Test Swagger Documentation
- [ ] http://localhost:8000/docs (interactive docs load)
- [ ] Can see all 4 endpoints listed
- [ ] Can expand each endpoint
- [ ] "Try it out" button works
- [ ] Can execute requests from Swagger UI
- [ ] Responses look correct

### Test Error Handling
- [ ] Invalid date format: /predict/rain/?date=invalid
  - [ ] Returns 400 error with clear message
- [ ] Future date: /predict/rain/?date=2099-01-01
  - [ ] Returns 400 error about future date
- [ ] Missing date parameter: /predict/rain/
  - [ ] Returns 422 validation error

### Test Different Dates
- [ ] Try 5+ different historical dates
- [ ] All return valid predictions
- [ ] No server crashes
- [ ] Predictions are reasonable (not NaN, not extreme values)

### Test Both Models
- [ ] Rain predictions return boolean (true/false)
- [ ] Precipitation predictions return numeric string
- [ ] Date calculations are correct (7 days, 3 days)

**Time estimate**: 2 hours

---

## 🐳 Phase 6: Docker Testing (Day 3-4)

### Build Docker Image
```bash
docker build -t weather-api .
```

- [ ] Build completes without errors
- [ ] No warnings about missing files
- [ ] Build time < 10 minutes

### Run Docker Container
```bash
docker run -p 8000:8000 weather-api
```

- [ ] Container starts successfully
- [ ] Models load correctly
- [ ] Server is accessible

### Test Dockerized App
- [ ] http://localhost:8000/docs works
- [ ] Can make predictions
- [ ] All endpoints functional
- [ ] Same behavior as non-Docker version

**Time estimate**: 1 hour

---

## 📦 Phase 7: GitHub Setup (Day 4)

### Create Repository
- [ ] Created private GitHub repository
- [ ] Repository name is descriptive
- [ ] Description added

### Add Collaborators
Add as Admin (per assessment requirement):
- [ ] anthony.so@uts.edu.au
- [ ] reasmey.tith@uts.edu.au
- [ ] Natalia.Tkachenko@uts.edu.au
- [ ] Huy.Nguyen-1@uts.edu.au
- [ ] savinay.singh@uts.edu.au
- [ ] TheHai.Bui@uts.edu.au

### Push Code
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

- [ ] All files pushed successfully
- [ ] .gitignore working (venv/ not pushed)
- [ ] Model files uploaded (< 100MB each)
- [ ] Can see all files on GitHub

### Verify Repository
- [ ] README.md displays on repo homepage
- [ ] All Python files present
- [ ] Dockerfile present
- [ ] requirements.txt present
- [ ] Model files in correct folders
- [ ] No sensitive data (passwords, API keys)

### Update github.txt
- [ ] github.txt contains correct repository URL
- [ ] URL is accessible (you can open it in browser)

**Time estimate**: 1 hour

---

## 🚀 Phase 8: Render Deployment (Day 4-5)

### Render Account Setup
- [ ] Created Render account
- [ ] Signed up with GitHub (recommended)
- [ ] Email verified

### Create Web Service
- [ ] Clicked "New +" → "Web Service"
- [ ] Connected GitHub repository
- [ ] Correct repo selected

### Configure Service
- [ ] Name set (unique, descriptive)
- [ ] Region selected (closest to you)
- [ ] Branch: main (or your default)
- [ ] Environment: Docker (auto-detected)
- [ ] Instance type: Free
- [ ] Auto-deploy: Yes (enabled)

### Deploy
- [ ] Clicked "Create Web Service"
- [ ] Build started
- [ ] Build logs show progress
- [ ] Build completed successfully (green checkmark)
- [ ] Service is "Live"
- [ ] Got public URL

### Health Check
- [ ] Set health check path to `/health/`
- [ ] Health check passes

**Time estimate**: 1-2 hours (mostly waiting for build)

---

## 🧪 Phase 9: Production Testing (Day 5)

Replace `your-app.onrender.com` with your actual Render URL:

### Test All Endpoints
- [ ] https://your-app.onrender.com/ (project info)
- [ ] https://your-app.onrender.com/health/ (health check)
- [ ] https://your-app.onrender.com/predict/rain/?date=2024-09-15
- [ ] https://your-app.onrender.com/predict/precipitation/fall/?date=2024-09-15
- [ ] https://your-app.onrender.com/docs (Swagger)

### Test Multiple Dates
- [ ] Test with 10+ different historical dates
- [ ] All predictions succeed
- [ ] No 500 errors
- [ ] Reasonable prediction values

### Test Error Handling
- [ ] Invalid date returns 400 error
- [ ] Future date returns 400 error
- [ ] Error messages are clear and helpful

### Performance Check
- [ ] First request (cold start): < 60 seconds
- [ ] Subsequent requests: < 5 seconds
- [ ] No timeouts

### Monitor Logs
- [ ] Can access logs in Render dashboard
- [ ] Logs show requests coming in
- [ ] No error messages in logs
- [ ] Models loading correctly

**Time estimate**: 2 hours

---

## 📊 Phase 10: Documentation (Day 5-6)

### Screenshots
Take screenshots of:
- [ ] Render dashboard showing service is live
- [ ] Swagger UI showing all endpoints
- [ ] Example rain prediction request/response
- [ ] Example precipitation prediction request/response
- [ ] Logs showing successful requests
- [ ] GitHub repository

### Update Documentation
- [ ] Updated README.md with your specifics
- [ ] Documented your models (type, performance)
- [ ] Added your GitHub URL
- [ ] Added your Render URL
- [ ] Noted any customizations

### Testing Documentation
- [ ] Documented test cases
- [ ] Documented edge cases tested
- [ ] Documented error scenarios tested

**Time estimate**: 2 hours

---

## 📝 Phase 11: Final Report (Day 6-7)

### API Structure Section
- [ ] Described all endpoints
- [ ] Explained input parameters
- [ ] Showed example requests/responses
- [ ] Included Swagger screenshots
- [ ] Explained error handling

### Deployment Section
- [ ] Described deployment process
- [ ] Included GitHub repo URL
- [ ] Included Render deployment URL
- [ ] Showed deployment was successful (screenshot)
- [ ] Explained Docker containerization

### Model Integration Section
- [ ] Explained how models are loaded
- [ ] Described feature engineering
- [ ] Explained StandardScaler usage
- [ ] Described prediction pipeline
- [ ] Linked to model performance from experiments

### Instructions Section
- [ ] How to access the API
- [ ] How to use Swagger docs
- [ ] Example API calls with curl or browser
- [ ] How to interpret responses

### Technical Details
- [ ] Technologies used (FastAPI, Docker, Render)
- [ ] Why each technology was chosen
- [ ] Challenges faced and solutions
- [ ] Performance observations

**Time estimate**: 4-6 hours

---

## 📦 Phase 12: Submission Preparation (Day 7)

### Create ZIP Files

#### API ZIP (36120-25SP-AT2-STUDENTID-api.zip)
Should contain:
- [ ] All Python code (app/ folder)
- [ ] requirements.txt
- [ ] Dockerfile
- [ ] README.md
- [ ] github.txt
- [ ] Model files (.joblib)
- [ ] .gitignore, .dockerignore

Verify:
- [ ] Can unzip and see all files
- [ ] Total size < 100MB (or used Git LFS)
- [ ] No venv/ or __pycache__/

### Final Checks

#### GitHub Repository
- [ ] Repository is private
- [ ] All collaborators added with Admin access
- [ ] All code is pushed
- [ ] README is up to date
- [ ] github.txt has correct URL

#### Render Deployment
- [ ] API is live and accessible
- [ ] All endpoints working
- [ ] No errors in logs
- [ ] Has been running for 24+ hours
- [ ] URL documented in report

#### Report (DOCX format, < 3000 words)
- [ ] API structure described
- [ ] Deployment process documented
- [ ] GitHub URL included
- [ ] Render URL included
- [ ] Screenshots included
- [ ] Testing documented
- [ ] Format is DOCX (NOT PDF!)
- [ ] Filename: 36120-25SP-AT2-STUDENTID-report.docx

### Submission Package
- [ ] API ZIP file ready
- [ ] Report DOCX file ready
- [ ] Experiments ZIP ready (from other repo)
- [ ] All filenames match required format
- [ ] Total submission < 200MB

**Time estimate**: 2 hours

---

## ✅ Final Verification (Before Submit)

### 24 Hours Before Deadline
- [ ] Render app is still running
- [ ] Make test API calls to verify
- [ ] Check logs for any errors
- [ ] Review all submission files

### 1 Hour Before Deadline
- [ ] Make final test API call
- [ ] Verify GitHub repo accessible
- [ ] Verify Render URL accessible
- [ ] Check report has all URLs

### At Submission
- [ ] Upload API ZIP to Canvas
- [ ] Upload Experiments ZIP to Canvas
- [ ] Upload Report DOCX to Canvas
- [ ] Submit on time
- [ ] Breathe! 🎉

---

## 📊 Time Breakdown

**Total estimated time: 30-40 hours**

- Understanding: 4 hours
- Setup: 2 hours
- Model training: 10 hours (in experiments repo)
- Code customization: 3 hours
- Testing: 4 hours
- Deployment: 3 hours
- Documentation: 4 hours
- Report writing: 6 hours
- Buffer: 4-8 hours

**Recommended schedule:**
- Week 1: Understanding + Setup + Model Training
- Week 2: Customization + Testing + Deployment
- Week 3: Documentation + Report + Submission

---

## 🆘 Troubleshooting Checklist

If something doesn't work, check:

- [ ] Virtual environment is activated
- [ ] All dependencies installed
- [ ] Model files exist in correct folders
- [ ] Model files are not corrupted
- [ ] Feature engineering matches training
- [ ] Date format is YYYY-MM-DD
- [ ] Date is in the past (not future)
- [ ] No typos in file paths
- [ ] Docker is running (for Docker tests)
- [ ] Internet connection working (for API calls)
- [ ] Render service is not sleeping
- [ ] GitHub repo is accessible
- [ ] Collaborators were added correctly

---

**Print this checklist and tick off items as you complete them!**

**Good luck! 🚀**
