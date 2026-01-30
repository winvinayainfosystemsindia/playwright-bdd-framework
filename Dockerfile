# Multi-stage Dockerfile for Playwright BDD Framework
# Stage 1: Base image with Python and system dependencies
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy as base

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies installation
FROM base as dependencies

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium firefox webkit && \
    playwright install-deps

# Stage 3: Application
FROM dependencies as application

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p reports/screenshots reports/videos reports/logs reports/allure-results

# Set proper permissions
RUN chmod -R 755 /app

# Create non-root user for security
RUN useradd -m -u 1000 testuser && \
    chown -R testuser:testuser /app

# Switch to non-root user
USER testuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import playwright; print('OK')" || exit 1

# Default command
CMD ["pytest", "-m", "smoke", "--alluredir=reports/allure-results", "-v"]

# Stage 4: CI/CD optimized image
FROM dependencies as ci

# Copy only necessary files
COPY config/ ./config/
COPY features/ ./features/
COPY pages/ ./pages/
COPY step_definitions/ ./step_definitions/
COPY utils/ ./utils/
COPY fixtures/ ./fixtures/
COPY tests/ ./tests/
COPY conftest.py pytest.ini ./

# Create directories
RUN mkdir -p reports/screenshots reports/videos reports/logs

# Set user
USER testuser

# CI command
CMD ["pytest", "--alluredir=reports/allure-results", "-n", "auto", "-v"]
