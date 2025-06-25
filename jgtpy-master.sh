#!/bin/bash

# JGT Master Control Script
# Interactive menu for all JGT operations

set -e

. $HOME/.jgt/.env||. .env

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print colored output
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
    echo -e "${BLUE}  JGT Master Control Center${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_menu() {
    echo
    echo -e "${CYAN}Available Operations:${NC}"
    echo "1)  Setup Environment"
    echo "2)  Check System Status"
    echo "3)  Refresh Data"
    echo "4)  Start API Server"
    echo "5)  Start Daemon Service"
    echo "6)  Stop Services"
    echo "7)  View Logs"
    echo "8)  Show Documentation"
    echo "9)  Show Script Examples"
    echo "10) Install Scripts"
    echo "11) Initialize New Trading Environment"
    echo "12) Exit"
    echo
}

# Function to check if script exists
check_script() {
    local script="$1"
    if [[ -f "$SCRIPT_DIR/$script" ]]; then
        return 0
    else
        return 1
    fi
}

# Function to run script with error handling
run_script() {
    local script="$1"
    local args="$2"
    
    if check_script "$script"; then
        print_status "Running $script..."
        if bash "$SCRIPT_DIR/$script" $args; then
            print_status "$script completed successfully"
        else
            print_error "$script failed"
            return 1
        fi
    else
        print_error "Script $script not found"
        return 1
    fi
}

# Function to setup environment
setup_environment() {
    echo
    print_header
    echo -e "${CYAN}Environment Setup Options:${NC}"
    echo "1) Full setup (recommended)"
    echo "2) Quick setup"
    echo "3) Back to main menu"
    echo
    read -p "Choose option (1-3): " setup_choice
    
    case $setup_choice in
        1)
            run_script "setup-service.sh" "--full"
            ;;
        2)
            run_script "setup-service.sh" "--quick"
            ;;
        3)
            return
            ;;
        *)
            print_error "Invalid choice"
            setup_environment
            ;;
    esac
}

# Function to check status
check_status() {
    echo
    print_header
    echo -e "${CYAN}Status Check Options:${NC}"
    echo "1) Basic status"
    echo "2) Verbose status"
    echo "3) Web API status"
    echo "4) Back to main menu"
    echo
    read -p "Choose option (1-4): " status_choice
    
    case $status_choice in
        1)
            run_script "check-status.sh"
            ;;
        2)
            run_script "check-status.sh" "--verbose"
            ;;
        3)
            run_script "check-status.sh" "--web"
            ;;
        4)
            return
            ;;
        *)
            print_error "Invalid choice"
            check_status
            ;;
    esac
}

# Function to refresh data
refresh_data() {
    echo
    print_header
    echo -e "${CYAN}Data Refresh Options:${NC}"
    echo "1) Refresh all data (default)"
    echo "2) Custom timeframes and instruments"
    echo "3) Back to main menu"
    echo
    read -p "Choose option (1-3): " refresh_choice
    
    case $refresh_choice in
        1)
            run_script "refresh-all.sh"
            ;;
        2)
            echo
            read -p "Enter timeframes (comma-separated, e.g., H1,H4,D1): " timeframes
            read -p "Enter instruments (comma-separated, e.g., EUR/USD,XAU/USD): " instruments
            if [[ -n "$timeframes" && -n "$instruments" ]]; then
                run_script "refresh-all.sh" "\"$timeframes\" \"$instruments\""
            else
                print_error "Both timeframes and instruments are required"
                refresh_data
            fi
            ;;
        3)
            return
            ;;
        *)
            print_error "Invalid choice"
            refresh_data
            ;;
    esac
}

# Function to start services
start_services() {
    echo
    print_header
    echo -e "${CYAN}Service Options:${NC}"
    echo "1) Start API Server"
    echo "2) Start Daemon Service"
    echo "3) Back to main menu"
    echo
    read -p "Choose option (1-3): " service_choice
    
    case $service_choice in
        1)
            print_status "Starting API server in background..."
            nohup bash "$SCRIPT_DIR/start-api-server.sh" > logs/api-server.log 2>&1 &
            echo $! > .api-server.pid
            print_status "API server started (PID: $(cat .api-server.pid))"
            print_status "Logs: logs/api-server.log"
            ;;
        2)
            print_status "Starting daemon service in background..."
            nohup bash "$SCRIPT_DIR/start-daemon.sh" > logs/daemon.log 2>&1 &
            echo $! > .daemon.pid
            print_status "Daemon service started (PID: $(cat .daemon.pid))"
            print_status "Logs: logs/daemon.log"
            ;;
        3)
            return
            ;;
        *)
            print_error "Invalid choice"
            start_services
            ;;
    esac
}

# Function to stop services
stop_services() {
    echo
    print_header
    echo -e "${CYAN}Stop Services:${NC}"
    
    if [[ -f ".api-server.pid" ]]; then
        local pid=$(cat .api-server.pid)
        if kill -0 $pid 2>/dev/null; then
            print_status "Stopping API server (PID: $pid)..."
            kill $pid
            rm .api-server.pid
            print_status "API server stopped"
        else
            print_warning "API server not running"
            rm -f .api-server.pid
        fi
    else
        print_warning "No API server PID file found"
    fi
    
    if [[ -f ".daemon.pid" ]]; then
        local pid=$(cat .daemon.pid)
        if kill -0 $pid 2>/dev/null; then
            print_status "Stopping daemon service (PID: $pid)..."
            kill $pid
            rm .daemon.pid
            print_status "Daemon service stopped"
        else
            print_warning "Daemon service not running"
            rm -f .daemon.pid
        fi
    else
        print_warning "No daemon PID file found"
    fi
}

# Function to view logs
view_logs() {
    echo
    print_header
    echo -e "${CYAN}Log Files:${NC}"
    
    if [[ -d "logs" ]]; then
        echo "Available log files:"
        ls -la logs/ 2>/dev/null || echo "No log files found"
        
        echo
        echo "1) View API server logs"
        echo "2) View daemon logs"
        echo "3) View all logs"
        echo "4) Back to main menu"
        echo
        read -p "Choose option (1-4): " log_choice
        
        case $log_choice in
            1)
                if [[ -f "logs/api-server.log" ]]; then
                    tail -f logs/api-server.log
                else
                    print_warning "API server log not found"
                fi
                ;;
            2)
                if [[ -f "logs/daemon.log" ]]; then
                    tail -f logs/daemon.log
                else
                    print_warning "Daemon log not found"
                fi
                ;;
            3)
                if [[ -d "logs" ]]; then
                    tail -f logs/*.log
                else
                    print_warning "No logs directory found"
                fi
                ;;
            4)
                return
                ;;
            *)
                print_error "Invalid choice"
                view_logs
                ;;
        esac
    else
        print_warning "No logs directory found"
    fi
}

# Function to show documentation
show_documentation() {
    echo
    print_header
    echo -e "${CYAN}Documentation Options:${NC}"
    echo "1) Show all documentation"
    echo "2) Show service documentation"
    echo "3) Show script examples"
    echo "4) List available sections"
    echo "5) Back to main menu"
    echo
    read -p "Choose option (1-5): " doc_choice
    
    case $doc_choice in
        1)
            guidecli_jgtpy --all
            ;;
        2)
            guidecli_jgtpy --section jgtservice
            ;;
        3)
            guidecli_jgtpy --examples
            ;;
        4)
            guidecli_jgtpy --list
            ;;
        5)
            return
            ;;
        *)
            print_error "Invalid choice"
            show_documentation
            ;;
    esac
}

# Function to install scripts
install_scripts() {
    echo
    print_header
    echo -e "${CYAN}Script Installation:${NC}"
    echo "1) Install to current directory"
    echo "2) Install to custom directory"
    echo "3) Back to main menu"
    echo
    read -p "Choose option (1-3): " install_choice
    
    case $install_choice in
        1)
            guidecli_jgtpy --install-scripts
            ;;
        2)
            read -p "Enter target directory: " target_dir
            if [[ -n "$target_dir" ]]; then
                guidecli_jgtpy --install-scripts "$target_dir"
            else
                print_error "Directory is required"
                install_scripts
            fi
            ;;
        3)
            return
            ;;
        *)
            print_error "Invalid choice"
            install_scripts
            ;;
    esac
}

# Function to initialize new environment
init_environment() {
    echo
    print_header
    echo -e "${CYAN}Initialize New Trading Environment:${NC}"
    echo "1) Interactive setup"
    echo "2) Quick setup (defaults)"
    echo "3) Back to main menu"
    echo
    read -p "Choose option (1-3): " init_choice
    
    case $init_choice in
        1)
            read -p "Enter environment name (or press Enter for current directory): " env_name
            if [[ -n "$env_name" ]]; then
                jgt init "$env_name"
            else
                jgt init
            fi
            ;;
        2)
            read -p "Enter environment name (or press Enter for current directory): " env_name
            if [[ -n "$env_name" ]]; then
                jgt init "$env_name" --no-interactive
            else
                jgt init --no-interactive
            fi
            ;;
        3)
            return
            ;;
        *)
            print_error "Invalid choice"
            init_environment
            ;;
    esac
}

# Main menu loop
main_menu() {
    while true; do
        print_header
        print_menu
        read -p "Enter your choice (1-12): " choice
        
        case $choice in
            1)
                setup_environment
                ;;
            2)
                check_status
                ;;
            3)
                refresh_data
                ;;
            4)
                start_services
                ;;
            5)
                start_services
                ;;
            6)
                stop_services
                ;;
            7)
                view_logs
                ;;
            8)
                show_documentation
                ;;
            9)
                guidecli_jgtpy --examples
                ;;
            10)
                install_scripts
                ;;
            11)
                init_environment
                ;;
            12)
                print_status "Exiting JGT Master Control Center"
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please enter a number between 1 and 12."
                ;;
        esac
        
        echo
        read -p "Press Enter to continue..."
    done
}

# Check if running in correct directory
if [[ ! -f "setup-service.sh" ]]; then
    print_error "This script must be run from the JGT root directory"
    print_error "Please cd to the directory containing setup-service.sh"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Start main menu
main_menu 