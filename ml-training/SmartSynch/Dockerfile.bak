# Use official Python runtime as a base image
FROM python:3.11-slim

# Set environment variable to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first
COPY requirements.txt .

# Ensure pip is installed and up to date
RUN python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE $PORT

# Start command
CMD uvicorn smartsynch.api.main:app --host 0.0.0.0 --port $PORT