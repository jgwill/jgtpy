FROM python:3.11-slim

# Set metadata
LABEL maintainer="Guillaume Isabelle <jgi@jgwill.com>"
LABEL description="JGT Data Refresh Service - Automated financial data processing"
LABEL version="0.6.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV JGTPY_DATA=/data/current
ENV JGTPY_DATA_FULL=/data/full

# Create user for security
RUN groupadd -r jgt && useradd -r -g jgt jgt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package with service dependencies
RUN pip install -e ".[serve]"

# Create data directories
RUN mkdir -p /data/current /data/full && \
    chown -R jgt:jgt /data /app

# Switch to non-root user
USER jgt

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${JGTPY_SERVICE_WEB_PORT:-8080}/api/v1/health || exit 1

# Expose port
EXPOSE 8080

# Default command - can be overridden
CMD ["jgtservice", "--daemon", "--all"] 
