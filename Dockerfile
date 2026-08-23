# Production Container for CareCover Copilot (Pure Python Backend & UI API Engine)

FROM python:3.11-slim

WORKDIR /app

# Install system utilities for PDF extraction and health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and application files
COPY . .

# Default PORT fallback
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
