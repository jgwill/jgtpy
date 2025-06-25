#!/bin/bash
# JGT Data Refresh Service - Status Check
# Comprehensive status check for service configuration and health

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

. $HOME/.jgt/.env||. .env

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
    echo "Check JGT Data Refresh Service status and configuration"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Show verbose output including file details"
    echo "  -w, --web      Check web API endpoints (if running)"
    echo ""
    echo "This script checks:"
    echo "  - Service installation and availability"
    echo "  - Configuration validation"
    echo "  - Data directory status"
    echo "  - Dropbox connectivity"
    echo "  - API endpoints (if web mode enabled)"
}

# Parse options
VERBOSE=false
CHECK_WEB=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -w|--web)
            CHECK_WEB=true
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
echo "JGT Data Refresh Service - Status Check"
echo "=============================================="
print_status "Performing comprehensive status check..."
echo ""

# Check 1: Service Installation
print_status "1. Checking service installation..."
if command -v jgtservice &> /dev/null; then
    print_success "jgtservice command found"
    SERVICE_VERSION=$(python -c "import jgtpy; print(jgtpy.__version__)" 2>/dev/null || echo "unknown")
    print_status "   jgtpy version: $SERVICE_VERSION"
else
    print_error "jgtservice command not found!"
    print_error "   Install with: pip install -e ."
fi

# Check 2: Python Dependencies
print_status "2. Checking Python dependencies..."

# Core dependencies
if python -c "import jgtpy" 2>/dev/null; then
    print_success "Core jgtpy module available"
else
    print_error "jgtpy module not available"
fi

if python -c "import jgtutils" 2>/dev/null; then
    print_success "jgtutils module available"
else
    print_error "jgtutils module not available"
fi

if python -c "import dropbox" 2>/dev/null; then
    print_success "dropbox module available"
else
    print_warning "dropbox module not available (upload features disabled)"
fi

# Optional web dependencies
if python -c "import fastapi, uvicorn" 2>/dev/null; then
    print_success "FastAPI web dependencies available"
else
    print_warning "FastAPI dependencies not available"
    print_status "   Install with: pip install -e .[serve]"
fi

echo ""

# Check 3: Service Configuration
print_status "3. Checking service configuration..."
if jgtservice --status &> /dev/null; then
    print_success "Service configuration valid"
    
    # Run actual status check
    print_status "   Configuration details:"
    jgtservice --status 2>/dev/null | grep -E "(instruments|timeframes|workers|data|upload)" | while read -r line; do
        echo "     $line"
    done
else
    print_error "Service configuration invalid"
    print_status "   Running detailed status check:"
    jgtservice --status 2>&1 | sed 's/^/     /'
fi

echo ""

# Check 4: Environment Variables
print_status "4. Checking environment configuration..."

check_env_var() {
    local var_name="$1"
    local var_desc="$2"
    local required="$3"
    
    if [[ -n "${!var_name}" ]]; then
        if [[ "$var_name" == *"TOKEN"* ]]; then
            print_success "$var_desc: [CONFIGURED]"
        else
            print_success "$var_desc: ${!var_name}"
        fi
    else
        if [[ "$required" == "true" ]]; then
            print_error "$var_desc: Not configured"
        else
            print_warning "$var_desc: Not configured (optional)"
        fi
    fi
}

check_env_var "JGTPY_DATA" "Data path" "false"
check_env_var "JGTPY_DATA_FULL" "Full data path" "false"
check_env_var "JGTPY_DROPBOX_APP_TOKEN" "Dropbox token" "false"
check_env_var "TRADABLE_TIMEFRAMES" "Tradable timeframes" "false"
check_env_var "HIGH_TIMEFRAMES" "High timeframes" "false"
check_env_var "LOW_TIMEFRAMES" "Low timeframes" "false"
check_env_var "JGTPY_SERVICE_MAX_WORKERS" "Max workers" "false"
check_env_var "JGTPY_SERVICE_WEB_PORT" "Web port" "false"

echo ""

# Check 5: Data Directories
print_status "5. Checking data directories..."

check_data_dir() {
    local dir_path="$1"
    local dir_name="$2"
    
    if [[ -n "$dir_path" ]]; then
        if [[ -d "$dir_path" ]]; then
            print_success "$dir_name exists: $dir_path"
            
            if [[ "$VERBOSE" == true ]]; then
                # Count files
                if [[ -d "$dir_path/cds" ]]; then
                    CDS_COUNT=$(find "$dir_path/cds" -name "*.cds" 2>/dev/null | wc -l)
                    print_status "   CDS files: $CDS_COUNT"
                fi
                
                # Check permissions
                if [[ -w "$dir_path" ]]; then
                    print_status "   Permissions: Writable"
                else
                    print_warning "   Permissions: Not writable"
                fi
                
                # Check disk space
                if command -v df &> /dev/null; then
                    DISK_USAGE=$(df -h "$dir_path" 2>/dev/null | tail -1 | awk '{print $4" available"}')
                    print_status "   Disk space: $DISK_USAGE"
                fi
            fi
        else
            print_warning "$dir_name does not exist: $dir_path"
        fi
    else
        print_warning "$dir_name not configured"
    fi
}

check_data_dir "$JGTPY_DATA" "Current data directory"
check_data_dir "$JGTPY_DATA_FULL" "Full data directory"

echo ""

# Check 6: Dropbox Connectivity
print_status "6. Checking Dropbox connectivity..."
if [[ -n "$JGTPY_DROPBOX_APP_TOKEN" ]]; then
    if python -c "import dropbox; print('Token validation passed')" 2>/dev/null; then
        # Test actual Dropbox connection
        if python -c "
import dropbox
import os
try:
    dbx = dropbox.Dropbox(os.environ['JGTPY_DROPBOX_APP_TOKEN'])
    account = dbx.users_get_current_account()
    print(f'Connected as: {account.name.display_name}')
except Exception as e:
    print(f'Connection failed: {e}')
    exit(1)
" 2>/dev/null; then
            print_success "Dropbox connection successful"
        else
            print_error "Dropbox connection failed"
        fi
    else
        print_error "Dropbox module not available"
    fi
else
    print_warning "Dropbox token not configured (upload disabled)"
fi

echo ""

# Check 7: Web API (if requested)
if [[ "$CHECK_WEB" == true ]]; then
    print_status "7. Checking web API endpoints..."
    
    WEB_PORT="${JGTPY_SERVICE_WEB_PORT:-8080}"
    BASE_URL="http://localhost:$WEB_PORT"
    
    if command -v curl &> /dev/null; then
        # Test health endpoint
        if curl -s "$BASE_URL/api/v1/health" > /dev/null 2>&1; then
            print_success "API server is running on port $WEB_PORT"
            
            # Test other endpoints
            ENDPOINTS=(
                "/api/v1/health:Health check"
                "/api/v1/status:Service status"
                "/api/v1/instruments:Instruments list"
                "/api/v1/timeframes:Timeframes list"
            )
            
            for endpoint_info in "${ENDPOINTS[@]}"; do
                IFS=':' read -r endpoint desc <<< "$endpoint_info"
                if curl -s "$BASE_URL$endpoint" > /dev/null 2>&1; then
                    print_success "$desc endpoint working"
                else
                    print_warning "$desc endpoint not responding"
                fi
            done
        else
            print_warning "API server not running on port $WEB_PORT"
            print_status "   Start with: ./start-api-server.sh"
        fi
    else
        print_warning "curl not available - cannot test API endpoints"
    fi
    
    echo ""
fi

# Check 8: Recent Activity
print_status "8. Checking recent activity..."

if [[ -n "$JGTPY_DATA" && -d "$JGTPY_DATA" ]]; then
    # Find recent files
    RECENT_COUNT=$(find "$JGTPY_DATA" -name "*.cds" -newermt "1 hour ago" 2>/dev/null | wc -l)
    if [[ $RECENT_COUNT -gt 0 ]]; then
        print_success "Recent activity: $RECENT_COUNT files updated in last hour"
        
        if [[ "$VERBOSE" == true ]]; then
            print_status "   Recent files:"
            find "$JGTPY_DATA" -name "*.cds" -newermt "1 hour ago" 2>/dev/null | head -5 | while read -r file; do
                echo "     - $file"
            done
        fi
    else
        print_warning "No recent activity (no files updated in last hour)"
    fi
else
    print_warning "Cannot check recent activity (data directory not available)"
fi

echo ""

# Summary
print_status "Status check complete!"
echo ""
print_status "Quick start commands:"
echo "  ./refresh-all.sh                    # Refresh all data"
echo "  ./start-api-server.sh               # Start API server"
echo "  ./start-daemon.sh                   # Start continuous daemon"
echo "  jgtservice --status                 # Check configuration"
echo ""

if [[ "$CHECK_WEB" != true ]]; then
    print_status "Run with --web to check API endpoints"
fi 