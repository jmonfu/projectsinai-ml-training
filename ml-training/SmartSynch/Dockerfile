FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and ensure pip is available
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
ENV PORT=8000
EXPOSE 8000

# Command to run the application
CMD python3 -m uvicorn smartsynch.api.main:app --host 0.0.0.0 --port $PORT