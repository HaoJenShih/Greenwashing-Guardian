# =========================
# Stage 1: Build stage
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies (build dependencies)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy only dependency files for caching
COPY pyproject.toml poetry.lock* ./

# Use pip cache to install dependencies into /install
RUN uv pip install --prefix=/install --cache-dir=/root/.cache/pip .

# =========================
# Stage 2: Production stage
# =========================
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies installed in builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p data/reports data/vector_stores downloads

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Install curl (for healthcheck)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8000", "--workers", "4"]
