#!/bin/bash

# JGT Quick Setup Script
# Fast setup for new users

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  JGT Quick Setup${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --help              Show this help message"
    echo "  --full              Full setup with all dependencies"
    echo "  --quick             Quick setup (default)"
    echo "  --init-env NAME     Initialize new trading environment"
    echo "  --install-scripts   Install scripts to current directory"
    echo "  --check-status      Check system status after setup"
    echo
    echo "Examples:"
    echo "  $0                    # Quick setup"
    echo "  $0 --full            # Full setup"
    echo "  $0 --init-env myenv  # Create new environment"
    echo "  $0 --install-scripts # Install scripts"
}

# Default values
SETUP_TYPE="quick"
INIT_ENV=""
INSTALL_SCRIPTS=false
CHECK_STATUS=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            print_help
            exit 0
            ;;
        --full)
            SETUP_TYPE="full"
            shift
            ;;
        --quick)
            SETUP_TYPE="quick"
            shift
            ;;
        --init-env)
            INIT_ENV="$2"
            shift 2
            ;;
        --install-scripts)
            INSTALL_SCRIPTS=true
            shift
            ;;
        --check-status)
            CHECK_STATUS=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            print_help
            exit 1
            ;;
    esac
done

print_header
print_status "Starting JGT Quick Setup..."

# Check if we're in the right directory
if [[ ! -f "setup-service.sh" ]]; then
    print_error "This script must be run from the JGT root directory"
    print_error "Please cd to the directory containing setup-service.sh"
    exit 1
fi

# Step 1: Setup service
print_status "Step 1: Setting up JGT service..."
if [[ "$SETUP_TYPE" == "full" ]]; then
    print_status "Running full setup..."
    bash setup-service.sh --full
else
    print_status "Running quick setup..."
    bash setup-service.sh --quick
fi

# Step 2: Install scripts if requested
if [[ "$INSTALL_SCRIPTS" == true ]]; then
    print_status "Step 2: Installing scripts..."
    if command -v guidecli_jgtpy >/dev/null 2>&1; then
        guidecli_jgtpy --install-scripts
    else
        print_warning "guidecli_jgtpy not found, skipping script installation"
    fi
fi

# Step 3: Initialize new environment if requested
if [[ -n "$INIT_ENV" ]]; then
    print_status "Step 3: Initializing new trading environment: $INIT_ENV"
    if command -v jgt >/dev/null 2>&1; then
        jgt init "$INIT_ENV" --no-interactive
    else
        print_warning "jgt command not found, skipping environment initialization"
    fi
fi

# Step 4: Check status if requested
if [[ "$CHECK_STATUS" == true ]]; then
    print_status "Step 4: Checking system status..."
    bash check-status.sh
fi

print_status "Setup completed successfully!"
echo
print_status "Next steps:"
echo "1. Run: ./jgtpy-master.sh          # Interactive menu"
echo "2. Run: ./refresh-all.sh           # Refresh data"
echo "3. Run: ./start-api-server.sh      # Start API server"
echo "4. Run: guidecli_jgtpy --examples  # View examples"
echo
print_status "For help:"
echo "  guidecli_jgtpy --help"
echo "  ./jgtpy-master.sh" 