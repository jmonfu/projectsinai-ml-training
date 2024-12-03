FROM python:3.11-slim

WORKDIR /app

# Install dependencies in one RUN
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the rest
COPY . .

ENV PORT=8000
EXPOSE 8000

CMD python3 -m uvicorn smartsynch.api.main:app --host 0.0.0.0 --port $PORT