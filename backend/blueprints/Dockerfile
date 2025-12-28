# Multi-stage build for the Todo CLI Application
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

FROM base AS dependencies

# Install Python dependencies
COPY pyproject.toml .
COPY uv.lock* . || true

# Install uv package manager if not available
RUN pip install --upgrade pip \
    && pip install uv

# Install project dependencies
RUN uv venv --seed --python 3.13 .venv \
    && . .venv/bin/activate \
    && uv pip install --system --no-cache-dir -e .

FROM base AS runtime

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv

# Copy application code
COPY . .

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Set permissions
RUN chmod +x /app/src/main.py

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; from src.main import main; print('App is healthy')" || exit 1

# Default command
CMD ["python", "-m", "todo_app.main"]
