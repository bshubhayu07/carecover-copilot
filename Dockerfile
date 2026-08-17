# Production Container for CareCover Copilot (React Frontend & FastAPI Backend)

# Stage 1: Build React Frontend static bundle
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python API Runtime
FROM python:3.11-slim

WORKDIR /app

# Install system utilities for PDF extraction and network health monitoring
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements & install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and backend files
COPY . .

# Copy compiled React frontend assets from Stage 1 into static docs/ distribution
COPY --from=frontend-builder /app/docs ./docs

# Expose API & Static Web Server Port
EXPOSE 8000

# Health Check Probe
HEALTHCHECK CMD curl --fail http://localhost:8000/api/health || exit 1

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
