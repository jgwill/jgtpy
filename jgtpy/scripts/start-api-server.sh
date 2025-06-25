#!/bin/bash
# JGT Data Refresh Service - Start API Server
# Launches the web API server for data access and service management

set -e  # Exit on any error

. $HOME/.jgt/.env||. .env

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_PORT=8080
PORT="${1:-$DEFAULT_PORT}"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} ✓ $1"
}

print_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} ✗ $1"
}

print_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} ⚠ $1"
}

# Help function
show_help() {
    echo "Usage: $0 [PORT] [OPTIONS]"
    echo ""
    echo "Start the JGT Data Refresh Service API server"
    echo ""
    echo "Arguments:"
    echo "  PORT          Port number for the API server (default: $DEFAULT_PORT)"
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0            # Start on default port $DEFAULT_PORT"
    echo "  $0 9000       # Start on port 9000"
    echo ""
    echo "Environment Variables:"
    echo "  JGTPY_SERVICE_WEB_PORT    Override default port"
    echo "  JGTPY_API_KEY            Optional API authentication key"
}

# Parse options
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Use environment variable if available
if [[ -n "$JGTPY_SERVICE_WEB_PORT" ]]; then
    PORT="$JGTPY_SERVICE_WEB_PORT"
fi

# Check if port is numeric
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    print_error "Port must be a number: $PORT"
    exit 1
fi

# Check if port is in valid range
if [[ $PORT -lt 1024 || $PORT -gt 65535 ]]; then
    print_warning "Port $PORT may require special privileges or be invalid"
fi

# Header
echo "=============================================="
echo "JGT Data Refresh Service - API Server"
echo "=============================================="
print_status "Starting API server on port $PORT..."
echo ""

# Check if jgtservice is available
if ! command -v jgtservice &> /dev/null; then
    print_error "jgtservice command not found!"
    print_error "Please install jgtpy with: pip install -e .[serve]"
    exit 1
fi

# Check if FastAPI dependencies are available
print_status "Checking service dependencies..."
if python -c "import fastapi, uvicorn" 2>/dev/null; then
    print_success "FastAPI dependencies available"
else
    print_error "FastAPI dependencies missing!"
    print_error "Please install with: pip install -e .[serve]"
    exit 1
fi

# Check service configuration
print_status "Validating service configuration..."
if jgtservice --status > /dev/null 2>&1; then
    print_success "Service configuration valid"
else
    print_warning "Service configuration issues detected"
    print_status "Running status check for details..."
    jgtservice --status
    echo ""
fi

# Check if port is already in use
if command -v netstat &> /dev/null; then
    if netstat -tuln | grep -q ":$PORT "; then
        print_error "Port $PORT is already in use!"
        print_status "Services using port $PORT:"
        netstat -tuln | grep ":$PORT "
        exit 1
    fi
elif command -v ss &> /dev/null; then
    if ss -tuln | grep -q ":$PORT "; then
        print_error "Port $PORT is already in use!"
        print_status "Services using port $PORT:"
        ss -tuln | grep ":$PORT "
        exit 1
    fi
fi

# Set environment variable for the service
export JGTPY_SERVICE_WEB_PORT="$PORT"

print_status "Configuration:"
print_status "- Port: $PORT"
print_status "- API Authentication: ${JGTPY_API_KEY:+Enabled}"
print_status "- Data Path: ${JGTPY_DATA:-Not configured}"
print_status "- Dropbox Upload: ${JGTPY_DROPBOX_APP_TOKEN:+Configured}"
echo ""

print_status "Starting web server..."
print_success "API server will be available at:"
print_success "  - API Base URL: http://localhost:$PORT/api/v1/"
print_success "  - Health Check: http://localhost:$PORT/api/v1/health"
print_success "  - API Documentation: http://localhost:$PORT/docs"
print_success "  - ReDoc Documentation: http://localhost:$PORT/redoc"
echo ""

print_status "Available API endpoints:"
echo "  GET  /api/v1/health                           - Health check"
echo "  GET  /api/v1/status                           - Service status"
echo "  GET  /api/v1/instruments                      - List instruments"
echo "  GET  /api/v1/timeframes                       - List timeframes"
echo "  GET  /api/v1/data/{instrument}/{timeframe}    - Get data"
echo "  GET  /api/v1/data/{instrument}/{timeframe}/latest - Latest data"
echo "  POST /api/v1/refresh                          - Trigger refresh"
echo "  GET  /api/v1/metrics                          - Processing metrics"
echo "  GET  /api/v1/config                           - Service configuration"
echo "  GET  /api/v1/upload/status                    - Upload status"
echo ""

print_warning "Press Ctrl+C to stop the server"
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    print_status "Shutting down API server..."
    print_success "API server stopped gracefully"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the API server
print_status "Launching JGT API server..."
exec jgtservice --web --port "$PORT" 