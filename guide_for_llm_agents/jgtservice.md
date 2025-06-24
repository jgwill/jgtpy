# JGT Data Refresh Service

The JGT Data Refresh Service is a modern, automated system that replaces manual bash script workflows with scalable, production-ready data processing and distribution capabilities.

## Overview

The service provides:
- **Automated Data Processing**: Continuous refresh of financial data across multiple instruments and timeframes
- **Parallel Processing**: Multi-worker architecture for improved performance
- **Web API**: RESTful endpoints for data access and service management
- **Cloud Distribution**: Automated Dropbox uploads with modern API integration
- **Production Deployment**: Docker, systemd, and monitoring support

## Core Components

### Service Architecture
```
JGTServiceManager
├── JGTServiceConfig (Configuration & Environment)
├── JGTScheduler (Timeframe-based scheduling)
├── ParallelProcessor (Concurrent data processing)
├── CloudUploader (Dropbox integration)
└── JGTServiceAPI (FastAPI web service)
```

### Data Flow
```
Raw Data (PDS) → Enhanced Processing (CDS) → Cloud Upload → Web API Access
```

## Installation & Setup

### Basic Installation
```bash
# Install base package
pip install -e .

# Install with web service dependencies
pip install -e .[serve]
```

### Quick Setup Script
```bash
# Interactive setup with full dependencies
./setup-service.sh --full

# Quick setup with defaults
./setup-service.sh --quick
```

## Service Modes

### 1. One-Time Refresh
```bash
# Refresh specific instrument/timeframe
jgtservice --refresh-once -i EUR/USD -t H1

# Refresh all configured data
jgtservice --refresh-once --all

# With verbose logging
jgtservice --refresh-once -i EUR/USD -t H1 -v 2
```

### 2. Continuous Daemon Mode
```bash
# Start continuous processing
jgtservice --daemon --all

# With custom configuration
jgtservice --daemon -i EUR/USD,XAU/USD -t H1,H4 -v 2
```

### 3. Web API Server
```bash
# Start API server on default port
jgtservice --web

# Custom port
jgtservice --web --port 9000

# With specific instruments/timeframes
jgtservice --web -i EUR/USD -t H1,H4
```

## Convenience Scripts

### Data Refresh Scripts
```bash
# Refresh all data (excludes m1 by default)
./refresh-all.sh

# Specific timeframes and instruments
./refresh-all.sh "H1,H4,D1" "EUR/USD,XAU/USD"

# With verbose output
./refresh-all.sh "H1" "EUR/USD" --verbose
```

### Service Management Scripts
```bash
# Start API server
./start-api-server.sh

# Start continuous daemon
./start-daemon.sh

# Comprehensive status check
./check-status.sh --verbose

# Check API endpoints
./check-status.sh --web
```

## Web API Endpoints

### Data Access
```bash
# Get data for instrument/timeframe
GET /api/v1/data/{instrument}/{timeframe}
GET /api/v1/data/EUR/USD/H1

# Get latest data point
GET /api/v1/data/{instrument}/{timeframe}/latest
GET /api/v1/data/EUR/USD/H1/latest

# List available instruments/timeframes
GET /api/v1/instruments
GET /api/v1/timeframes
```

### Service Management
```bash
# Health check
GET /api/v1/health

# Service status
GET /api/v1/status

# Configuration
GET /api/v1/config

# Processing metrics
GET /api/v1/metrics

# Upload status
GET /api/v1/upload/status
```

### Control Endpoints
```bash
# Trigger refresh
POST /api/v1/refresh
{
  "instruments": ["EUR/USD"],
  "timeframes": ["H1", "H4"]
}
```

### API Documentation
- **Interactive Docs**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## Configuration

### Environment Variables
```bash
# Data paths
JGTPY_DATA=/path/to/current/data
JGTPY_DATA_FULL=/path/to/full/data

# Timeframe configuration
TRADABLE_TIMEFRAMES=m5,m15,m30,H1,H4,D1
HIGH_TIMEFRAMES=H4,D1,W1
LOW_TIMEFRAMES=m5,m15,m30

# Service configuration
JGTPY_SERVICE_MAX_WORKERS=4
JGTPY_SERVICE_WEB_PORT=8080
JGTPY_SERVICE_REFRESH_INTERVAL=300

# Dropbox integration
JGTPY_DROPBOX_APP_TOKEN=your_token_here
JGTPY_SERVICE_ENABLE_UPLOAD=true

# Security (optional)
JGTPY_API_KEY=your_api_key_here
```

### Configuration Sources (Priority Order)
1. Command line arguments
2. Environment variables
3. `$HOME/.jgt/config.json`
4. Current directory `.env`
5. `$HOME/.env`
6. Default values

## Performance Characteristics

### Processing Speed
- **Single instrument/timeframe**: ~8-14 seconds
- **Parallel processing**: 4 concurrent workers
- **Memory usage**: Stable during extended runs
- **Error recovery**: Individual failure isolation

### Scalability
- **Multiple instruments**: Parallel processing
- **Multiple timeframes**: Concurrent execution
- **Large datasets**: Efficient memory management
- **Continuous operation**: 24/7 daemon mode

## Integration with Existing JGT Tools

### CLI Integration
```bash
# Service processes data that CLI tools can use
jgtservice --refresh-once -i EUR/USD -t H1
jgtcli -i EUR/USD -t H1 -c 100  # Uses refreshed data

# Service can trigger CLI processing
jgtservice --refresh-once --all
jgtads -i EUR/USD -t H1 -c 100  # Create charts from service data
```

### Data Pipeline Integration
```bash
# Service maintains data pipeline
jgtservice --daemon --all  # Continuous PDS→CDS processing

# CLI tools access processed data
jgtmksg -i EUR/USD -t H1 -c 100  # Generate signals
jgtmouthwater -i EUR/USD -t H1 -c 100  # State analysis
```

## Deployment Options

### Development
```bash
# Local development
./start-api-server.sh
./start-daemon.sh
```

### Production - Docker
```bash
# Using provided Dockerfile
docker build -f examples/jgtservice/docker/Dockerfile -t jgtservice .
docker run -p 8080:8080 jgtservice

# Docker Compose with monitoring
docker-compose -f examples/jgtservice/config/docker-compose.yml up
```

### Production - Systemd
```bash
# Install systemd service
sudo cp examples/jgtservice/systemd/jgtservice.service /etc/systemd/system/
sudo systemctl enable jgtservice
sudo systemctl start jgtservice
```

## Monitoring & Troubleshooting

### Status Monitoring
```bash
# Check service status
./check-status.sh

# Detailed status with API check
./check-status.sh --web --verbose

# Service logs
jgtservice --status
```

### Common Issues
1. **Configuration errors**: Run `./check-status.sh --verbose`
2. **Missing dependencies**: Install with `pip install -e .[serve]`
3. **Permission issues**: Check data directory permissions
4. **Network issues**: Verify Dropbox token and connectivity

### Performance Monitoring
```bash
# API metrics
curl http://localhost:8080/api/v1/metrics

# Processing status
curl http://localhost:8080/api/v1/status

# Upload status
curl http://localhost:8080/api/v1/upload/status
```

## Migration from Manual Workflows

### Before (Manual Bash Scripts)
```bash
# Manual parallel processing
for instrument in EUR/USD XAU/USD; do
    for timeframe in H1 H4; do
        jgtcli -i "$instrument" -t "$timeframe" -c 100 &
    done
done
wait

# Manual upload
droxul /path/to/data
```

### After (Automated Service)
```bash
# Automated processing
./refresh-all.sh "H1,H4" "EUR/USD,XAU/USD"

# Or continuous daemon
./start-daemon.sh

# Web API access
curl http://localhost:8080/api/v1/data/EUR/USD/H1
```

## Best Practices

### Service Configuration
1. Use appropriate worker count for your system
2. Configure timeframe intervals based on data requirements
3. Set up proper environment variables
4. Enable Dropbox upload for data distribution
5. Use API authentication in production

### Performance Optimization
1. Monitor memory usage during extended runs
2. Adjust worker count based on CPU cores
3. Use appropriate refresh intervals
4. Monitor disk space for data storage
5. Configure proper logging levels

### Security Considerations
1. Use API keys for web service access
2. Configure CORS appropriately for production
3. Secure Dropbox token storage
4. Use HTTPS in production deployments
5. Implement proper access controls

## For LLM Agents

The JGT Data Refresh Service provides:
- **Consistent CLI interface** with existing JGT tools
- **Comprehensive help systems** (`--help` on all commands)
- **Structured logging** for troubleshooting
- **RESTful API** for programmatic access
- **Production deployment** templates
- **Integration examples** with existing workflows

All service components support verbose logging (`-v 2`) and provide detailed error messages for effective troubleshooting and integration. 