# Production Container for CareCover Copilot (Pure Python Backend & UI API Engine)

FROM python:3.11-slim

WORKDIR /app

# Install system utilities for PDF extraction and network health monitoring
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and application files
COPY . .

# Expose API & Web Server Port
EXPOSE 8000

# Health Check Probe
HEALTHCHECK CMD curl --fail http://localhost:8000/api/health || exit 1

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
