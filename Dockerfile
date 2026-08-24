# Production Container for CareCover Copilot (Pure Python Streamlit Application)

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
ENV PORT=8000
EXPOSE 8000

# Health Check Probe
HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health || exit 1

CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8000} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false"]
