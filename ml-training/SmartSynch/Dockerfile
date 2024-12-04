# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python3", "-m", "uvicorn", "smartsynch.api.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]