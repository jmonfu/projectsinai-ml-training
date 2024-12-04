FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and Python
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variable for port
ENV PORT=8000

# Run the web service on container startup
CMD ["python3", "-m", "uvicorn", "smartsynch.api.main:app", "--host", "0.0.0.0", "--port", "8000"]