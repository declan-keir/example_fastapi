# ============================================================================
# Dockerfile for Weather Prediction API
# ============================================================================
#
# WHAT IS DOCKER?
# Docker is a tool that packages your application and all its dependencies
# into a "container" - a standardized unit that runs the same way everywhere.
#
# WHY USE DOCKER?
# - Consistency: Runs the same on your laptop, Render, AWS, anywhere
# - Isolation: Your app doesn't interfere with other apps
# - Easy deployment: Just upload the Dockerfile and it works
#
# HOW IT WORKS:
# 1. Docker reads this file line by line
# 2. Each instruction creates a "layer" in the image
# 3. The final image contains everything needed to run your app
# 4. You can run this image as a container
#
# BUILDING THE IMAGE:
# docker build -t weather-api .
#
# RUNNING THE CONTAINER:
# docker run -p 8000:8000 weather-api
#
# ============================================================================


# ============================================================================
# STEP 1: Base Image
# ============================================================================
# Start with an official Python image
# This image already has Python 3.11 installed

FROM python:3.11-slim

# What is "slim"?
# - python:3.11 = full image with everything (~900MB)
# - python:3.11-slim = minimal image with just Python (~150MB)
# - Slim is smaller and faster to download
# - We use slim because we don't need extra tools


# ============================================================================
# STEP 2: Set Working Directory
# ============================================================================
# Create and set the working directory inside the container
# All subsequent commands will run in this directory

WORKDIR /app

# This creates /app folder and moves into it
# Your code will live here inside the container


# ============================================================================
# STEP 3: Copy Requirements File
# ============================================================================
# Copy requirements.txt first (before copying all code)
# Why? Docker caching! If requirements don't change, this layer is cached

COPY requirements.txt .

# The dot (.) means "copy to current directory" (/app)


# ============================================================================
# STEP 4: Install Python Dependencies
# ============================================================================
# Install all packages listed in requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# What do these flags mean?
# --no-cache-dir: Don't store pip cache (saves space)
# --upgrade pip: Make sure pip itself is up to date
# -r requirements.txt: Install from requirements file

# Why && instead of separate RUN commands?
# - Each RUN creates a new layer
# - Combining commands into one RUN = one layer = smaller image


# ============================================================================
# STEP 5: Copy Application Code
# ============================================================================
# Copy all your application files into the container

COPY . .

# First dot (.): Copy everything from current directory (your computer)
# Second dot (.): To current directory in container (/app)

# This copies:
# - app/ folder (all your Python code)
# - All other files in your project


# ============================================================================
# STEP 6: Expose Port
# ============================================================================
# Tell Docker that the container will listen on port 8000

EXPOSE 8000

# This is just documentation - it doesn't actually publish the port
# You still need to publish it when running: docker run -p 8000:8000


# ============================================================================
# STEP 7: Run the Application
# ============================================================================
# This is the command that runs when the container starts

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Explanation:
# - uvicorn: The ASGI server that runs FastAPI
# - app.main:app:
#   - app.main = the main.py file in app/ folder
#   - :app = the FastAPI instance named "app"
# - --host 0.0.0.0: Listen on all network interfaces
#   - 0.0.0.0 = accept connections from anywhere
#   - 127.0.0.1 = only accept from localhost (doesn't work in Docker)
# - --port 8000: Listen on port 8000

# Why 0.0.0.0 instead of 127.0.0.1?
# Inside a container, 127.0.0.1 only accepts connections from inside the container
# 0.0.0.0 accepts connections from outside the container (from the host, internet, etc.)


# ============================================================================
# UNDERSTANDING THE CONTAINER
# ============================================================================
#
# YOUR COMPUTER                    DOCKER CONTAINER
# ┌──────────────────┐            ┌──────────────────┐
# │                  │            │                  │
# │  Your code       │  ──────>   │  /app/           │
# │  requirements.txt│            │  - app/          │
# │  Dockerfile      │            │  - requirements  │
# │                  │            │  - Python 3.11   │
# │                  │            │                  │
# └──────────────────┘            └──────────────────┘
#         │                              │
#         │                              │
#         └──────> docker build ─────────┘
#
# When you run: docker build -t weather-api .
# Docker creates an image containing everything needed to run your app
#
# When you run: docker run -p 8000:8000 weather-api
# Docker starts a container from that image and runs your app
#
# Port mapping: -p 8000:8000
# - First 8000: Port on your computer
# - Second 8000: Port inside container
# - Connections to localhost:8000 → forwarded to container:8000


# ============================================================================
# COMMON DOCKER COMMANDS
# ============================================================================
#
# Build image:
#   docker build -t weather-api .
#   (-t = tag/name the image)
#
# Run container:
#   docker run -p 8000:8000 weather-api
#   (-p = publish port)
#
# Run in background:
#   docker run -d -p 8000:8000 weather-api
#   (-d = detached mode)
#
# List running containers:
#   docker ps
#
# List all containers:
#   docker ps -a
#
# Stop container:
#   docker stop <container_id>
#
# View logs:
#   docker logs <container_id>
#
# Remove container:
#   docker rm <container_id>
#
# Remove image:
#   docker rmi weather-api
#
# Shell into container:
#   docker exec -it <container_id> /bin/bash


# ============================================================================
# DOCKERFILE BEST PRACTICES
# ============================================================================
#
# 1. Use official base images (python:3.11-slim)
# 2. Copy requirements.txt before code (caching)
# 3. Use --no-cache-dir to reduce image size
# 4. Combine RUN commands with && (fewer layers)
# 5. Use .dockerignore to exclude unnecessary files
# 6. Don't run as root (use USER command for production)
# 7. Use specific version tags (3.11-slim, not latest)
# 8. Keep images small (use slim or alpine variants)


# ============================================================================
# .dockerignore FILE (create this separately)
# ============================================================================
#
# Create a file named .dockerignore in your project root:
#
# __pycache__
# *.pyc
# *.pyo
# *.pyd
# .Python
# venv/
# .venv/
# .git/
# .gitignore
# .env
# *.md
# .DS_Store
# htmlcov/
# .coverage
# *.log
#
# This tells Docker to ignore these files when copying
# Makes the image smaller and faster to build


# ============================================================================
# DEPLOYMENT TO RENDER
# ============================================================================
#
# Render automatically detects this Dockerfile and uses it for deployment.
#
# Process:
# 1. You push code to GitHub (including this Dockerfile)
# 2. Connect GitHub repo to Render
# 3. Render detects Dockerfile
# 4. Render builds the Docker image
# 5. Render runs the container
# 6. Your API is live!
#
# Render configuration:
# - Environment: Docker
# - Build command: (automatic)
# - Start command: (from CMD in Dockerfile)
# - Port: 8000 (from EXPOSE)
