FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variable for port
ENV PORT=8000

# Run the web service on container startup
CMD ["uvicorn", "smartsynch.api.main:app", "--host", "0.0.0.0", "--port", "8000"]