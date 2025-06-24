# JGT Service Documentation

## Overview

The JGT Service provides automated data refresh capabilities for financial instruments across multiple timeframes. It replaces manual bash script workflows with a comprehensive, scalable solution.

## Quick Start

### 1. Environment Setup
```bash
# Quick setup (recommended for new users)
./jgtpy-quick-setup.sh

# Full setup with all dependencies
./jgtpy-quick-setup.sh --full

# Interactive setup
./jgtpy-master.sh
```

### 2. Initialize New Trading Environment
```bash
# Interactive setup
jgt init my-trading-env

# Quick setup with defaults
jgt init my-trading-env --no-interactive

# Setup in current directory
jgt init
```

### 3. Basic Operations
```bash
# Check system status
./check-status.sh

# Refresh data
./refresh-all.sh

# Start API server
./start-api-server.sh
```

## Guide System

The enhanced guide system provides comprehensive documentation and script management:

### Documentation Access
```bash
# List available sections
guidecli_jgtpy --list

# Show specific section
guidecli_jgtpy --section jgtservice

# Show all documentation
guidecli_jgtpy --all

# Show script examples
guidecli_jgtpy --examples
```

### Script Management
```bash
# List available scripts
guidecli_jgtpy --scripts
# These scripts are packaged with the library and work even outside the repo

# Show script content
guidecli_jgtpy --script refresh-all.sh

# Install scripts to current directory
guidecli_jgtpy --install-scripts

# Install scripts to specific directory
guidecli_jgtpy --install-scripts /path/to/trading/env
```

## Master Control Script

The `jgtpy-master.sh` provides an interactive menu for all operations:

```bash
./jgtpy-master.sh
```

**Menu Options:**
1. Setup Environment
2. Check System Status  
3. Refresh Data
4. Start API Server
5. Start Daemon Service
6. Stop Services
7. View Logs
8. Show Documentation
9. Show Script Examples
10. Install Scripts
11. Initialize New Trading Environment
12. Exit

## Service Architecture

### Core Components

1. **Configuration Manager** (`service/config.py`)
   - Environment variable support
   - JSON configuration files
   - Default settings management

2. **Scheduler** (`service/scheduler.py`)
   - Timeframe-based scheduling
   - Market hours awareness
   - Configurable intervals

3. **Processor** (`service/processor.py`)
   - Parallel data processing
   - Concurrent.futures implementation
   - Error handling and retry logic

4. **Upload Manager** (`service/upload.py`)
   - Dropbox integration
   - Batch uploads
   - Progress tracking

5. **Web API** (`service/api.py`)
   - FastAPI implementation
   - RESTful endpoints
   - Real-time data access

### CLI Commands

#### Service Management
```bash
# Start daemon mode
jgtservice daemon

# Start web server
jgtservice web

# One-time refresh
jgtservice refresh

# Check status
jgtservice status
```

#### Web API
```bash
# Start API server
jgtservice web --port 8080

# Access endpoints
curl http://localhost:8080/api/v1/health
curl http://localhost:8080/api/v1/data/EUR/USD/H1
```

## Configuration

### Environment Variables
```bash
# Data paths
JGTPY_DATA=/path/to/current/data
JGTPY_DATA_FULL=/path/to/full/data

# Service settings
JGTPY_SERVICE_MAX_WORKERS=4
JGTPY_SERVICE_WEB_PORT=8080
JGTPY_SERVICE_REFRESH_INTERVAL=300

# Dropbox integration
JGTPY_DROPBOX_APP_TOKEN=your_token_here
JGTPY_SERVICE_ENABLE_UPLOAD=true
```

### Configuration Files
- `config/trading.json` - Trading environment configuration
- `config/settings.json` - Service settings
- `.env` - Environment variables

## API Endpoints

### Health & Status
- `GET /api/v1/health` - Service health check
- `GET /api/v1/status` - Detailed status information
- `GET /api/v1/config` - Current configuration

### Data Access
- `GET /api/v1/data/{instrument}/{timeframe}` - Get data for instrument/timeframe
- `GET /api/v1/data/{instrument}/{timeframe}/latest` - Get latest data point
- `GET /api/v1/instruments` - List available instruments
- `GET /api/v1/timeframes` - List available timeframes

### Service Management
- `POST /api/v1/refresh` - Trigger data refresh
- `POST /api/v1/refresh/{instrument}/{timeframe}` - Refresh specific data
- `GET /api/v1/logs` - Get service logs
- `GET /api/v1/metrics` - Get performance metrics

### Authentication (Optional)
- `POST /api/v1/auth/login` - Authenticate user
- `GET /api/v1/auth/verify` - Verify authentication

## Deployment

### Systemd Service
```bash
# Install service
sudo cp examples/jgtservice/systemd/jgtservice.service /etc/systemd/system/
sudo systemctl enable jgtservice
sudo systemctl start jgtservice
```

### Docker
```bash
# Build image
docker build -t jgtservice .

# Run container
docker run -d --name jgtservice -p 8080:8080 jgtservice
```

### Docker Compose
```bash
# Start with monitoring
docker-compose -f examples/jgtservice/config/docker-compose.yml up -d
```

## Monitoring

### Log Files
- `logs/service.log` - Service logs
- `logs/api.log` - API access logs
- `logs/processor.log` - Processing logs

### Metrics
- Processing times
- Success/failure rates
- Data freshness
- API response times

### Health Checks
```bash
# Check service health
curl http://localhost:8080/api/v1/health

# Check data freshness
curl http://localhost:8080/api/v1/status
```

## Troubleshooting

### Common Issues

1. **Service won't start**
   - Check environment variables
   - Verify dependencies are installed
   - Check log files

2. **Data not refreshing**
   - Verify market hours
   - Check timeframe configuration
   - Review processing logs

3. **API not responding**
   - Check if service is running
   - Verify port configuration
   - Check firewall settings

### Debug Mode
```bash
# Enable debug logging
export JGTPY_DEBUG=true
jgtservice daemon --verbose
```

### Log Analysis
```bash
# View real-time logs
tail -f logs/service.log

# Search for errors
grep ERROR logs/service.log

# Check processing times
grep "Processing completed" logs/processor.log
```

## Integration Examples

### Python Client
```python
import requests

# Get data
response = requests.get('http://localhost:8080/api/v1/data/EUR/USD/H1')
data = response.json()

# Trigger refresh
requests.post('http://localhost:8080/api/v1/refresh/EUR/USD/H1')
```

### Bash Scripts
```bash
# Refresh specific data
curl -X POST http://localhost:8080/api/v1/refresh/EUR/USD/H1

# Get latest data
curl http://localhost:8080/api/v1/data/EUR/USD/H1/latest
```

### Cron Jobs
```bash
# Refresh data every hour
0 * * * * /path/to/jgtservice refresh

# Check health every 5 minutes
*/5 * * * * curl -f http://localhost:8080/api/v1/health || echo "Service down"
```

## Development

### Installation with Development Dependencies
```bash
pip install jgtpy[serve,dev-lint,dev-test,dev-docs]
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jgtpy

# Run specific test
pytest tests/test_service.py
```

### Code Quality
```bash
# Lint code
flake8 jgtpy/

# Format code
isort jgtpy/
black jgtpy/
```

## Support

### Documentation
- `guidecli_jgtpy --help` - Command help
- `guidecli_jgtpy --examples` - Usage examples
- `guidecli_jgtpy --section jgtservice` - Service documentation

### Scripts
- `./jgtpy-master.sh` - Interactive control center
- `./jgtpy-quick-setup.sh` - Quick setup
- `./check-status.sh` - Status checking

### Environment Management
- `jgt init` - Initialize new trading environment
- `guidecli_jgtpy --install-scripts` - Install scripts
- `guidecli_jgtpy --scripts` - List available scripts 