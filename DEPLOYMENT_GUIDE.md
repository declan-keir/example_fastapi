# Deployment Guide - Render (2025)

**Complete step-by-step guide to deploy your Weather Prediction API to Render**

This guide is up-to-date as of 2025 and includes all the latest Render features and best practices.

---

## 📚 Table of Contents

1. [What is Render?](#what-is-render)
2. [Why Render?](#why-render)
3. [Prerequisites](#prerequisites)
4. [Step 1: Prepare Your Code](#step-1-prepare-your-code)
5. [Step 2: Create GitHub Repository](#step-2-create-github-repository)
6. [Step 3: Sign Up for Render](#step-3-sign-up-for-render)
7. [Step 4: Deploy to Render](#step-4-deploy-to-render)
8. [Step 5: Test Your Deployed API](#step-5-test-your-deployed-api)
9. [Step 6: Monitor and Maintain](#step-6-monitor-and-maintain)
10. [Troubleshooting](#troubleshooting)
11. [GitHub Actions (Optional)](#github-actions-optional)

---

## 🌐 What is Render?

Render is a cloud platform that hosts your applications on the internet.

**Think of it like this:**
- Your laptop runs your API locally (only you can access it)
- Render runs your API in the cloud (anyone can access it via a URL)

**What Render does:**
1. Takes your code from GitHub
2. Builds a Docker container
3. Runs your container on their servers
4. Gives you a public URL (example: `https://your-app.onrender.com`)

---

## 🎯 Why Render?

**Free Tier Benefits:**
- ✅ Free hosting (no credit card required for free tier)
- ✅ Automatic HTTPS (secure connections)
- ✅ Easy deployment (just connect GitHub)
- ✅ Automatic deploys (updates when you push to GitHub)
- ✅ Good for small projects and learning

**Free Tier Limitations:**
- ⏰ Spins down after 15 minutes of inactivity (first request after spin-down is slow)
- 💾 Limited compute resources (512MB RAM)
- ⏱️ Limited build minutes per month (400 minutes)

**Alternatives:**
- Heroku (similar, but charges for everything now)
- Railway (similar to Render, generous free tier)
- Fly.io (more technical, good free tier)
- AWS/GCP/Azure (powerful but complex and expensive)

For this assignment, **Render's free tier is perfect**.

---

## ✅ Prerequisites

Before you start, make sure you have:

- [ ] Your code is working locally (test with `uvicorn app.main:app --reload`)
- [ ] All required files exist:
  - [ ] `app/main.py`
  - [ ] `app/weather_fetcher.py`
  - [ ] `app/model_predictor.py`
  - [ ] `requirements.txt`
  - [ ] `Dockerfile`
  - [ ] Model files in `app/models/`
- [ ] A GitHub account (create one at https://github.com if needed)
- [ ] Git installed on your computer
- [ ] All model files (`.joblib`, `threshold.txt`) in correct folders

---

## 📝 Step 1: Prepare Your Code

### 1.1 Create .gitignore file

Create a file named `.gitignore` in your project root:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Testing
.coverage
htmlcov/
.pytest_cache/

# Environment
.env
.env.local

# Logs
*.log

# OS
Thumbs.db
```

**Why?** This prevents unnecessary files from being uploaded to GitHub.

### 1.2 Create .dockerignore file

Create a file named `.dockerignore` in your project root:

```dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv/
.venv/
.git/
.gitignore
.env
*.md
.DS_Store
htmlcov/
.coverage
*.log
README.md
.github/
```

**Why?** This prevents Docker from copying unnecessary files into your image.

### 1.3 Verify Dockerfile

Make sure your `Dockerfile` exists and has this structure:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Critical parts:**
- `--host 0.0.0.0` (accepts external connections)
- `--port 8000` (Render expects port 8000 by default)

### 1.4 Test Locally with Docker

Before deploying, test that your Docker build works:

```bash
# Build the image
docker build -t weather-api .

# Run the container
docker run -p 8000:8000 weather-api

# Test in browser
# Open: http://localhost:8000/health/
```

If this works, you're ready to deploy!

---

## 🐙 Step 2: Create GitHub Repository

### 2.1 Create Repository on GitHub

1. Go to https://github.com
2. Click the "+" icon in top right → "New repository"
3. Fill in details:
   - **Repository name**: `weather-prediction-api` (or your choice)
   - **Description**: "Weather Prediction API for AT2"
   - **Public or Private**: Choose **Private** (requirement for assignment)
   - **Initialize with README**: Leave unchecked (you already have one)
4. Click "Create repository"

### 2.2 Add Course Staff as Collaborators

**IMPORTANT**: The assignment requires you to give admin access to course staff.

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Click "Collaborators" in left sidebar (may need to confirm password)
4. Click "Add people"
5. Add these GitHub usernames one by one:
   - `anthony.so@uts.edu.au`
   - `reasmey.tith@uts.edu.au`
   - `Natalia.Tkachenko@uts.edu.au`
   - `Huy.Nguyen-1@uts.edu.au`
   - `savinay.singh@uts.edu.au`
   - `TheHai.Bui@uts.edu.au`
6. Select "Admin" permission level for each
7. Click "Add [username] to this repository"

**Note**: They need to accept the invitation (sent via email).

### 2.3 Push Your Code to GitHub

In your terminal, in your project folder:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Weather Prediction API"

# Add remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace**:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO` with your repository name

### 2.4 Verify on GitHub

1. Go to your repository URL
2. Check that all files are there:
   - `app/` folder
   - `requirements.txt`
   - `Dockerfile`
   - Model files in `app/models/`
3. Make sure model files uploaded successfully (not too large)

**GitHub File Size Limit**: 100MB per file
- If model files are > 100MB, you need to use Git LFS (Large File Storage)
- See: https://git-lfs.github.com/

---

## 🚀 Step 3: Sign Up for Render

### 3.1 Create Render Account

1. Go to https://render.com
2. Click "Get Started" or "Sign Up"
3. **Sign up with GitHub** (recommended - easier integration)
   - Click "Sign up with GitHub"
   - Authorize Render to access your GitHub account
   - This lets Render see your repositories
4. Complete your profile

**Why sign up with GitHub?**
- Automatic repository access
- Easier deployment process
- Auto-deploy when you push to GitHub

### 3.2 Verify Email

Check your email and verify your account if required.

---

## 🌟 Step 4: Deploy to Render

### 4.1 Create a New Web Service

1. From Render dashboard, click "New +" (top right)
2. Select "Web Service"
3. You'll see a list of your GitHub repositories

**Don't see your repo?**
- Click "Configure account" or "Connect repository"
- Grant Render access to your repositories
- Select your `weather-prediction-api` repository

4. Click "Connect" next to your repository

### 4.2 Configure the Web Service

Render will auto-detect your Dockerfile and fill in most settings. Verify/update:

**Basic Settings:**
- **Name**: `your-name-weather-api` (this becomes your URL)
  - Must be unique across all Render
  - Example: `john-smith-weather-api`
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt, Singapore)
- **Branch**: `main` (or your default branch)

**Build Settings:**
- **Environment**: Docker (auto-detected from Dockerfile)
- **Dockerfile Path**: `./Dockerfile` (auto-filled)

**Instance Type:**
- Select **Free** (or choose paid for better performance)

**Advanced Settings** (click "Advanced"):
- **Auto-Deploy**: Yes (recommended - deploys on every GitHub push)
- **Health Check Path**: `/health/` (your health endpoint)

### 4.3 Environment Variables (if needed)

If your app uses environment variables (like API keys), add them here:

1. Scroll to "Environment Variables"
2. Click "Add Environment Variable"
3. Add key-value pairs
   - Example: `API_KEY` = `your-secret-key`

**For this assignment, you probably don't need any environment variables.**

### 4.4 Create Web Service

1. Review all settings
2. Click "Create Web Service"
3. Render will start building your app

**What happens now:**
1. Render clones your GitHub repository
2. Runs `docker build` using your Dockerfile
3. Creates a container from the image
4. Starts the container
5. Assigns a public URL

### 4.5 Watch the Build Process

You'll see live logs:
```
==> Cloning from https://github.com/YOUR_USERNAME/YOUR_REPO...
==> Downloading cache...
==> Building image...
==> Step 1/7 : FROM python:3.11-slim
==> ...
==> Build successful!
==> Starting service...
==> Your service is live 🎉
```

**Build time:** Usually 5-10 minutes for first deployment

**Common build output:**
- Downloading Python image
- Installing dependencies from requirements.txt
- Copying your code
- Starting uvicorn server

### 4.6 Get Your Live URL

Once deployment succeeds:
1. You'll see "Your service is live" with a green checkmark
2. At the top, you'll see your URL: `https://your-name-weather-api.onrender.com`
3. Copy this URL - this is your live API!

---

## 🧪 Step 5: Test Your Deployed API

### 5.1 Test in Browser

Open your browser and test these URLs (replace with your URL):

**1. Root endpoint:**
```
https://your-name-weather-api.onrender.com/
```
Expected: JSON with API information

**2. Health check:**
```
https://your-name-weather-api.onrender.com/health/
```
Expected: Status message

**3. Rain prediction:**
```
https://your-name-weather-api.onrender.com/predict/rain/?date=2024-09-15
```
Expected: Rain prediction JSON

**4. Precipitation prediction:**
```
https://your-name-weather-api.onrender.com/predict/precipitation/fall/?date=2024-09-15
```
Expected: Precipitation prediction JSON

**5. Swagger documentation:**
```
https://your-name-weather-api.onrender.com/docs
```
Expected: Interactive API documentation

### 5.2 First Request May Be Slow

**Important**: On the free tier, Render spins down your service after 15 minutes of inactivity.

- **First request after spin-down**: 30-60 seconds (cold start)
- **Subsequent requests**: Fast (< 1 second)

This is **normal** on the free tier. For the assignment, this is acceptable.

### 5.3 Test with cURL (Optional)

If you're comfortable with command line:

```bash
# Test health endpoint
curl https://your-name-weather-api.onrender.com/health/

# Test rain prediction
curl "https://your-name-weather-api.onrender.com/predict/rain/?date=2024-09-15"

# Test precipitation prediction
curl "https://your-name-weather-api.onrender.com/predict/precipitation/fall/?date=2024-09-15"
```

---

## 📊 Step 6: Monitor and Maintain

### 6.1 View Logs

To see what's happening in your app:

1. Go to your service in Render dashboard
2. Click "Logs" tab
3. You'll see real-time logs from your application

**What to look for:**
- Application startup messages
- Request logs (when someone accesses your API)
- Error messages (if something goes wrong)

Example logs:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6.2 Monitor Metrics

1. Click "Metrics" tab in Render dashboard
2. See:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

**Free tier limits:**
- 512 MB RAM
- 0.1 CPU
- Unlimited bandwidth

### 6.3 Redeploy (Manual)

If you need to redeploy manually:

1. Go to your service in Render
2. Click "Manual Deploy" → "Deploy latest commit"
3. Choose the branch
4. Click "Deploy"

### 6.4 Automatic Deploys

If you enabled Auto-Deploy:
- Every time you `git push` to GitHub
- Render automatically rebuilds and deploys
- Usually takes 5-10 minutes

**To push updates:**
```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push origin main
```

Render will automatically detect the push and start deploying.

---

## 🐛 Troubleshooting

### Issue 1: Build Fails

**Symptom**: Build fails with error messages

**Common causes:**
1. **Missing dependencies in requirements.txt**
   - Check build logs for "ModuleNotFoundError"
   - Add missing packages to requirements.txt

2. **Dockerfile errors**
   - Syntax errors in Dockerfile
   - Wrong Python version
   - Solution: Test locally with `docker build -t test .`

3. **Model files too large**
   - GitHub has 100MB file limit
   - Solution: Use Git LFS or reduce model size

**How to fix:**
1. Read the error message in build logs
2. Fix the issue in your code
3. Push to GitHub: `git add . && git commit -m "Fix" && git push`
4. Render will auto-deploy again

### Issue 2: Service Won't Start

**Symptom**: Build succeeds but service won't start

**Common causes:**
1. **Wrong port**
   - Render expects port 8000 by default
   - Check Dockerfile: `--port 8000`

2. **Wrong host**
   - Must use `--host 0.0.0.0` (not 127.0.0.1)
   - Check Dockerfile: `--host 0.0.0.0`

3. **Missing model files**
   - Check that model files are in GitHub repo
   - Check logs for "FileNotFoundError"

**How to debug:**
1. Check "Logs" tab in Render
2. Look for error messages when service starts
3. Common errors:
   ```
   FileNotFoundError: model.joblib not found
   ModuleNotFoundError: No module named 'fastapi'
   ```

### Issue 3: 404 Errors on Endpoints

**Symptom**: Homepage works but `/predict/rain/` returns 404

**Cause**: Path mismatch or code error

**Solution:**
1. Check your `app/main.py` has the endpoint defined
2. Make sure path is exactly `/predict/rain/` (with trailing slash if you defined it)
3. Check Render logs for startup errors

### Issue 4: Predictions Failing

**Symptom**: Endpoint returns 500 error or wrong predictions

**Common causes:**
1. **Model files missing or corrupt**
   - Check GitHub repo has all model files
   - Verify files aren't corrupted

2. **Feature mismatch**
   - Features in API don't match training
   - Check `model_predictor.py` feature order

3. **Wrong scaler**
   - Using different scaler than training
   - Make sure you're using the saved scaler.joblib

**How to debug:**
1. Check logs in Render for error messages
2. Look for ValueError or RuntimeError
3. Test locally first: `uvicorn app.main:app --reload`

### Issue 5: Slow First Request

**Symptom**: First request takes 30-60 seconds

**Cause**: This is normal on free tier (cold start)

**Not a bug!** Free tier spins down after 15 min inactivity.

**Solutions:**
- Accept it (fine for assignment)
- Upgrade to paid tier ($7/month, always on)
- Use a cron job to ping your API every 10 minutes (keeps it warm)

### Issue 6: Out of Memory

**Symptom**: Service crashes, logs show "Out of memory"

**Cause**: Free tier has 512MB RAM limit

**Solutions:**
1. **Reduce model size**
   - Use simpler models
   - Compress models

2. **Optimize code**
   - Don't load models multiple times
   - Use global caching (singleton pattern)

3. **Upgrade to paid tier**
   - More RAM available

---

## 🔄 GitHub Actions (Optional - Advanced)

You can automate deployment with GitHub Actions. This is **optional** but good practice.

### Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to Render
        run: |
          curl -X POST https://api.render.com/deploy/${{ secrets.RENDER_DEPLOY_HOOK }}

      - name: Wait for deployment
        run: sleep 60

      - name: Test deployment
        run: |
          curl -f https://your-name-weather-api.onrender.com/health/
```

**Setup:**
1. Get your Render Deploy Hook:
   - Go to Render dashboard → Your service → Settings
   - Scroll to "Deploy Hook"
   - Copy the URL

2. Add to GitHub Secrets:
   - Go to GitHub repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: Paste the deploy hook URL
   - Click "Add secret"

3. Push the workflow file:
   ```bash
   git add .github/workflows/deploy.yml
   git commit -m "Add GitHub Actions deployment"
   git push
   ```

Now every push to main will trigger deployment!

---

## ✅ Deployment Checklist

Before submitting your assignment, verify:

- [ ] API is deployed and accessible at public URL
- [ ] All endpoints work:
  - [ ] `/` returns project info
  - [ ] `/health/` returns status
  - [ ] `/predict/rain/?date=YYYY-MM-DD` returns rain prediction
  - [ ] `/predict/precipitation/fall/?date=YYYY-MM-DD` returns precipitation prediction
- [ ] Swagger docs accessible at `/docs`
- [ ] GitHub repository is private
- [ ] Course staff added as collaborators with admin access
- [ ] Repository includes:
  - [ ] All Python code
  - [ ] requirements.txt
  - [ ] Dockerfile
  - [ ] Model files
  - [ ] README.md
  - [ ] github.txt with repository URL
- [ ] Test predictions with recent dates (2024 data)
- [ ] Service has been running for at least 24 hours without errors
- [ ] Logs show no critical errors

---

## 📝 For Your Report

Include in your final report:

1. **GitHub Repository URL**
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO
   ```

2. **Render Deployment URL**
   ```
   https://your-name-weather-api.onrender.com
   ```

3. **Swagger Documentation URL**
   ```
   https://your-name-weather-api.onrender.com/docs
   ```

4. **Example API Calls**
   - Show example requests and responses
   - Include screenshots from Swagger UI

5. **Deployment Process**
   - Brief description of how you deployed
   - Any issues encountered and solutions
   - Performance observations (response times, etc.)

---

## 🎓 Summary

**You've learned:**
1. How to prepare code for deployment
2. How to use Git and GitHub
3. How to deploy with Docker to Render
4. How to monitor and maintain a live API
5. How to troubleshoot common issues

**Your API is now:**
- ✅ Live on the internet
- ✅ Accessible to anyone with the URL
- ✅ Automatically documented (Swagger)
- ✅ Ready for submission

**Congratulations! 🎉**

Your Weather Prediction API is now deployed and ready for assessment!

---

## 📚 Additional Resources

**Render Documentation:**
- https://render.com/docs

**Docker Documentation:**
- https://docs.docker.com/

**FastAPI Documentation:**
- https://fastapi.tiangolo.com/

**Git/GitHub Guides:**
- https://docs.github.com/en/get-started

**Help and Support:**
- Render Community: https://community.render.com/
- FastAPI Discord: https://discord.gg/fastapi
- Stack Overflow: Tag your questions with `render`, `fastapi`, `docker`
