# Multi-stage production container for CareCover Copilot (Backend & Frontend)

# Stage 1: Build React Tailwind Frontend static assets
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python Runtime Environment
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

# Copy source code, Python modules, and backend files
COPY . .

# Copy compiled React frontend assets from Stage 1 into static docs/ distribution
COPY --from=frontend-builder /app/docs ./docs

# Expose Streamlit & API Ports
EXPOSE 8501 5173

# Health Check Probe
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
