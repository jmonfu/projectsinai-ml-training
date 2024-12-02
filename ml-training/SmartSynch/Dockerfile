FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Install package
RUN pip install -e .

# Expose port
EXPOSE 8000

# Run FastAPI application
CMD ["uvicorn", "smartsynch.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 