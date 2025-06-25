#!/bin/bash
# JGT Data Refresh Service - Start Daemon Mode
# Starts the service in continuous daemon mode with automated refresh scheduling

set -e  # Exit on any error

. $HOME/.jgt/.env||. .env

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Start the JGT Data Refresh Service in daemon mode"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Enable verbose logging"
    echo ""
    echo "The daemon will:"
    echo "  - Continuously refresh data based on timeframe scheduling"
    echo "  - Upload processed data to Dropbox (if configured)"
    echo "  - Provide health monitoring and status reporting"
    echo "  - Handle errors gracefully and continue processing"
    echo ""
    echo "Environment Variables:"
    echo "  JGTPY_SERVICE_REFRESH_INTERVAL    Refresh interval in seconds (default: 300)"
    echo "  JGTPY_SERVICE_MAX_WORKERS        Number of parallel workers (default: 4)"
    echo "  JGTPY_DROPBOX_APP_TOKEN          Dropbox token for uploads"
}

# Parse options
VERBOSE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Header
echo "=============================================="
echo "JGT Data Refresh Service - Daemon Mode"
echo "=============================================="
print_status "Starting daemon mode for continuous data refresh..."
echo ""

# Check if jgtservice is available
if ! command -v jgtservice &> /dev/null; then
    print_error "jgtservice command not found!"
    print_error "Please install jgtpy with: pip install -e ."
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
    print_warning "Continuing with daemon startup despite configuration warnings..."
fi

# Display configuration summary
print_status "Daemon configuration:"
print_status "- Refresh interval: ${JGTPY_SERVICE_REFRESH_INTERVAL:-300} seconds"
print_status "- Max workers: ${JGTPY_SERVICE_MAX_WORKERS:-4}"
print_status "- Data path: ${JGTPY_DATA:-Not configured}"
print_status "- Upload enabled: ${JGTPY_DROPBOX_APP_TOKEN:+Yes}"
print_status "- Verbose logging: ${VERBOSE:+Enabled}"
echo ""

print_status "Daemon features:"
echo "  ✓ Automatic timeframe-based refresh scheduling"
echo "  ✓ Parallel processing for improved performance"
echo "  ✓ Individual error isolation (failed instruments don't stop others)"
echo "  ✓ Graceful shutdown on SIGINT/SIGTERM"
echo "  ✓ Structured JSON logging for monitoring"
if [[ -n "$JGTPY_DROPBOX_APP_TOKEN" ]]; then
    echo "  ✓ Automatic Dropbox upload after processing"
else
    echo "  ⚠ Dropbox upload disabled (no token configured)"
fi
echo ""

print_warning "Daemon mode will run continuously until stopped with Ctrl+C"
print_warning "Monitor logs and system resources during operation"
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    print_status "Received shutdown signal..."
    print_status "Gracefully stopping daemon..."
    print_success "Daemon stopped successfully"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if we should run a quick test first
print_status "Running quick validation test..."
if jgtservice --refresh-once -i "EUR/USD" -t "H1" --quiet > /dev/null 2>&1; then
    print_success "Validation test passed - daemon should work correctly"
else
    print_warning "Validation test failed - daemon may encounter issues"
    print_status "You can continue anyway or stop and check configuration"
    echo ""
fi

# Start daemon
print_status "Starting JGT Data Refresh Daemon..."
print_success "Daemon is now running in continuous mode"
print_success "Processing will begin based on timeframe schedule"
echo ""

print_status "Monitoring information:"
echo "  - View logs in real-time as they appear below"
echo "  - Check status: jgtservice --status (in another terminal)"
echo "  - Monitor system resources: htop/top"
echo "  - View data files: ls \$JGTPY_DATA/cds/"
echo ""

print_warning "Press Ctrl+C to stop the daemon gracefully"
echo ""

# Build daemon command
DAEMON_CMD="jgtservice --daemon --all"
if [[ -n "$VERBOSE" ]]; then
    DAEMON_CMD="$DAEMON_CMD -v 2"
fi

print_status "Executing: $DAEMON_CMD"
echo ""

# Start the daemon
exec $DAEMON_CMD 