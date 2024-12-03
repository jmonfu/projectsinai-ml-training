FROM python:3.9-slim

WORKDIR /app

# Copy only requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files
COPY smartsynch/ ./smartsynch/
COPY setup.py .

# Install package
RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "smartsynch.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"] 