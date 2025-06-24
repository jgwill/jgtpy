# JGT Data Refresh Service - Quick Start Scripts

This directory contains convenience scripts for common JGT service operations.

## Available Scripts

### 🔧 `setup-service.sh`
**Initial setup and configuration**
```bash
./setup-service.sh          # Interactive setup
./setup-service.sh --full   # Install with web dependencies
./setup-service.sh --quick  # Quick setup with defaults
```

### 📊 `check-status.sh`
**Comprehensive status check**
```bash
./check-status.sh           # Basic status check
./check-status.sh --verbose # Detailed information
./check-status.sh --web     # Check API endpoints
```

### 🔄 `refresh-all.sh`
**Refresh all CDS data (excludes m1 by default)**
```bash
./refresh-all.sh                                # Default timeframes/instruments
./refresh-all.sh "H1,H4,D1"                     # Specific timeframes
./refresh-all.sh "H1,H4" "EUR/USD,XAU/USD"      # Specific timeframes + instruments
./refresh-all.sh "" "" --verbose                # Defaults with verbose output
```

### 🌐 `start-api-server.sh`
**Launch web API server**
```bash
./start-api-server.sh       # Start on default port 8080
./start-api-server.sh 9000  # Start on port 9000
```

### 🚀 `start-daemon.sh`
**Start continuous daemon mode**
```bash
./start-daemon.sh           # Standard daemon mode
./start-daemon.sh --verbose # Verbose logging
```

## Quick Workflow

### First Time Setup
```bash
# 1. Initial setup
./setup-service.sh --full

# 2. Check everything is working
./check-status.sh --verbose

# 3. Run a test refresh
./refresh-all.sh "H1" "EUR/USD" --verbose
```

### Daily Operations
```bash
# Check service status
./check-status.sh

# Refresh all data
./refresh-all.sh

# Start API server for data access
./start-api-server.sh

# Start continuous processing
./start-daemon.sh
```

### Monitoring & Development
```bash
# Detailed status with API check
./check-status.sh --web --verbose

# Refresh specific data with logging
./refresh-all.sh "H1,H4" "EUR/USD,XAU/USD" --verbose

# Test API server on custom port
./start-api-server.sh 9090
```

## Environment Variables

These scripts respect the following environment variables:

- `JGTPY_DATA` - Current data storage path
- `JGTPY_DATA_FULL` - Full historical data path
- `JGTPY_DROPBOX_APP_TOKEN` - Dropbox upload token
- `JGTPY_SERVICE_MAX_WORKERS` - Number of parallel workers
- `JGTPY_SERVICE_WEB_PORT` - Web server port
- `JGTPY_API_KEY` - Optional API authentication

## Configuration Files

Scripts will load configuration from:
1. `$HOME/.jgt/.env` (created by setup script)
2. Current directory `.env`
3. Environment variables

## Error Handling

All scripts include:
- ✅ Comprehensive error checking
- 🎨 Colored output for easy reading
- 📝 Detailed logging and status messages
- 🛡️ Graceful shutdown handling
- 🔍 Helpful troubleshooting information

## API Endpoints

When the API server is running (`./start-api-server.sh`):

- **Documentation**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/api/v1/health
- **Service Status**: http://localhost:8080/api/v1/status
- **Data Access**: http://localhost:8080/api/v1/data/{instrument}/{timeframe}

## Getting Help

Each script includes built-in help:
```bash
./script-name.sh --help
```

For comprehensive documentation, see:
- [docs/jgtservice_implementation.md](docs/jgtservice_implementation.md)
- [examples/jgtservice/README.md](examples/jgtservice/README.md)

## Troubleshooting

1. **Scripts not executable**: Run `chmod +x *.sh`
2. **Command not found**: Run `./setup-service.sh` first
3. **Configuration issues**: Run `./check-status.sh --verbose`
4. **Permission errors**: Check data directory permissions
5. **Network issues**: Verify Dropbox token and connectivity

---

*These scripts provide a user-friendly interface to the powerful JGT Data Refresh Service, making complex operations simple and accessible.* 