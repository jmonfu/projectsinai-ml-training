FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "smartsynch.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 