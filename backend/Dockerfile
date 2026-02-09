# Multi-stage Docker build for FastAPI backend
# Stage 1: Builder - Install dependencies
FROM python:3.13-slim as builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime - Minimal production image
FROM python:3.13-slim

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Set PATH to include user-installed packages
ENV PATH=/root/.local/bin:$PATH

# Expose application port
EXPOSE 8000

# Health check for container monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run application with uvicorn
# Use environment variable for number of workers (default: 4)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WORKERS:-4}
