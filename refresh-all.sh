#!/bin/bash
# JGT Data Refresh Service - Refresh All CDS Data
# Refreshes all configured instruments and timeframes (excluding m1)

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_TIMEFRAMES="m5,m15,H1,H4,D1,W1,M1"

# Try to get instruments from environment, fallback to default
if [ -n "$JGTPY_SERVICE_INSTRUMENTS" ]; then
    DEFAULT_INSTRUMENTS="$JGTPY_SERVICE_INSTRUMENTS"
elif [ -n "$JGTPY_INSTRUMENTS" ]; then
    DEFAULT_INSTRUMENTS="$JGTPY_INSTRUMENTS"
elif [ -n "$instruments" ]; then
    DEFAULT_INSTRUMENTS="$instruments"
else
    DEFAULT_INSTRUMENTS="EUR/USD,XAU/USD,SPX500,GBP/USD,USD/JPY,AUD/USD,USD/CAD"
fi

# Parse command line arguments
TIMEFRAMES="${1:-$DEFAULT_TIMEFRAMES}"
INSTRUMENTS="${2:-$DEFAULT_INSTRUMENTS}"
VERBOSE=""

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
    echo "Usage: $0 [TIMEFRAMES] [INSTRUMENTS] [OPTIONS]"
    echo ""
    echo "Refresh all CDS data for specified instruments and timeframes"
    echo ""
    echo "Arguments:"
    echo "  TIMEFRAMES    Comma-separated list of timeframes (default: $DEFAULT_TIMEFRAMES)"
    echo "  INSTRUMENTS   Comma-separated list of instruments (default: $DEFAULT_INSTRUMENTS)"
    echo ""
    echo "Options:"
    echo "  -v, --verbose     Enable verbose output"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Use defaults"
    echo "  $0 \"H1,H4,D1\"                       # Specific timeframes, default instruments"
    echo "  $0 \"H1,H4\" \"EUR/USD,XAU/USD\"       # Specific timeframes and instruments"
    echo "  $0 \"\" \"\" --verbose                # Defaults with verbose output"
}

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            # Already handled positional args above
            shift
            ;;
    esac
done

# Header
echo "==============================================="
echo "JGT Data Refresh Service - Refresh All CDS Data"
echo "==============================================="
print_status "Starting CDS data refresh..."
print_status "Timeframes: $TIMEFRAMES"
print_status "Instruments: $INSTRUMENTS"
echo ""

# Check if jgtservice is available
if ! command -v jgtservice &> /dev/null; then
    print_error "jgtservice command not found!"
    print_error "Please install jgtpy with: pip install -e ."
    exit 1
fi

# Check service status first
print_status "Checking service configuration..."
if jgtservice --status > /dev/null 2>&1; then
    print_success "Service configuration valid"
else
    print_warning "Service configuration issues detected"
    print_status "Running status check for details..."
    jgtservice --status
fi

echo ""

# Start the refresh process
print_status "Starting parallel CDS data refresh..."
print_status "This may take several minutes depending on the number of instruments/timeframes..."

start_time=$(date +%s)

# Build the command
CMD="jgtservice --refresh-once"

# Add timeframes if specified
if [[ -n "$TIMEFRAMES" && "$TIMEFRAMES" != "all" ]]; then
    # Convert comma-separated timeframes to individual -t arguments
    IFS=',' read -ra TF_ARRAY <<< "$TIMEFRAMES"
    for tf in "${TF_ARRAY[@]}"; do
        tf=$(echo "$tf" | xargs)  # trim whitespace
        if [[ -n "$tf" ]]; then
            CMD="$CMD -t $tf"
        fi
    done
else
    CMD="$CMD --all"
fi

# Add instruments if specified  
if [[ -n "$INSTRUMENTS" && "$INSTRUMENTS" != "all" ]]; then
    # Convert comma-separated instruments to individual -i arguments
    IFS=',' read -ra INST_ARRAY <<< "$INSTRUMENTS"
    for inst in "${INST_ARRAY[@]}"; do
        inst=$(echo "$inst" | xargs)  # trim whitespace
        if [[ -n "$inst" ]]; then
            CMD="$CMD -i \"$inst\""
        fi
    done
else
    CMD="$CMD --all"
fi

# Add verbose flag if requested
if [[ -n "$VERBOSE" ]]; then
    CMD="$CMD -v 2"
fi

print_status "Executing: $CMD"
echo ""

# Execute the refresh command
if eval $CMD; then
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    print_success "CDS data refresh completed successfully!"
    print_success "Total duration: ${duration} seconds"
else
    print_error "CDS data refresh failed!"
    print_error "Check the logs above for details"
    exit 1
fi

echo ""
print_status "Refresh summary:"
print_status "- Timeframes processed: $TIMEFRAMES"
print_status "- Instruments processed: $INSTRUMENTS"
print_status "- Duration: ${duration} seconds"

# Optional: Show recent data files
if command -v find &> /dev/null; then
    if [[ -n "$JGTPY_DATA" && -d "$JGTPY_DATA" ]]; then
        print_status "Recent CDS files created:"
        find "$JGTPY_DATA" -name "*.cds" -newermt "1 minute ago" 2>/dev/null | head -10 | while read -r file; do
            echo "  - $file"
        done
    fi
fi

echo ""
print_success "Refresh process completed!"
print_status "You can now access the refreshed data via:"
print_status "  - Direct file access in \$JGTPY_DATA/cds/"
print_status "  - API endpoints: jgtservice --web --port 8080"
print_status "  - CLI tools: jgtcli, cdscli, etc." 