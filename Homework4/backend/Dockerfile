FROM python:3.11-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    libopenblas-dev libomp-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Remove hardcoded port
ENV PORT=${PORT:-8000}

# Use environment variable for port
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT