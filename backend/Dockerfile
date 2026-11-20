# Multi-stage production Dockerfile for PEACOCK Backend Service
# Compatible with Railway, Render, Fly.io, and Docker Compose

# --- Stage 1: Build Dependencies ---
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Stage 2: Final Runtime Image ---
FROM python:3.12-slim

WORKDIR /app

# Install runtime database client libraries and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy project files
COPY alembic.ini .
COPY alembic alembic
COPY app app
COPY scripts scripts
COPY backend/entrypoint.sh entrypoint.sh

# Ensure upload media directories exist and set script permissions
RUN mkdir -p media/venues media/packages media/vendors media/invitations media/payment_receipts \
    && chmod +x entrypoint.sh

# Default Railway/Docker port
EXPOSE 8000

# Health check against FastAPI /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

ENTRYPOINT ["./entrypoint.sh"]
