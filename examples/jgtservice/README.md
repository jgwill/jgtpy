# JGT Data Refresh Service - Deployment Examples

This directory contains deployment templates and configuration examples for the JGT Data Refresh Service in various environments.

## Quick Start

### Local Development
```bash
# Install with service dependencies
pip install -e ".[serve]"

# Run one-time refresh
jgtservice --refresh-once -i EUR/USD -t H1

# Run daemon mode
jgtservice --daemon --all

# Run web server
jgtservice --web --port 8080
```

### Docker Deployment
```bash
# Build and run with Docker Compose
cd examples/jgtservice
cp config/production.env .env
# Edit .env with your configuration
docker-compose up -d

# Run with monitoring stack
docker-compose --profile monitoring up -d
```

### systemd Service (Linux)
```bash
# Copy service file
sudo cp systemd/jgtservice.service /etc/systemd/system/

# Edit configuration
sudo nano /etc/systemd/system/jgtservice.service

# Enable and start service
sudo systemctl enable jgtservice
sudo systemctl start jgtservice

# Check status
sudo systemctl status jgtservice
```

## Configuration Files

### Environment Configuration
- `config/production.env` - Production environment template
- `config/development.env` - Development environment template (to be created)

### Deployment Templates
- `systemd/jgtservice.service` - systemd service configuration
- `docker/Dockerfile` - Docker container image
- `config/docker-compose.yml` - Multi-container deployment

### Monitoring (Optional)
- `monitoring/prometheus.yml` - Prometheus configuration (to be created)
- `monitoring/grafana/` - Grafana dashboards (to be created)

## Environment Variables

### Required Configuration
```bash
# Data storage paths
JGTPY_DATA=/path/to/current/data
JGTPY_DATA_FULL=/path/to/full/data

# Dropbox upload token
JGTPY_DROPBOX_APP_TOKEN=your_token_here
```

### Optional Configuration
```bash
# Service settings
JGTPY_SERVICE_MAX_WORKERS=4
JGTPY_SERVICE_WEB_PORT=8080
JGTPY_SERVICE_REFRESH_INTERVAL=300

# Timeframe configuration
TRADABLE_TIMEFRAMES=m1,m5,m15,m30,H1,H4,D1
HIGH_TIMEFRAMES=H4,D1,W1
LOW_TIMEFRAMES=m1,m5,m15

# Security
JGTPY_API_KEY=optional_api_key
```

## Deployment Scenarios

### Development Environment
- Single developer machine
- Local data storage
- Manual configuration
- Direct command line usage

### Staging Environment  
- Docker container
- Volume-mounted data
- Environment variable configuration
- Health checks enabled

### Production Environment
- systemd service or Docker Compose
- Persistent volume storage
- Comprehensive monitoring
- Automated restarts and logging

## Health Monitoring

### Health Check Endpoints
```bash
# Service health
curl http://localhost:8080/api/v1/health

# Service status
curl http://localhost:8080/api/v1/status

# Processing metrics
curl http://localhost:8080/api/v1/metrics
```

### Log Monitoring
```bash
# systemd logs
journalctl -u jgtservice -f

# Docker logs
docker logs -f jgtservice

# File logs (if configured)
tail -f /var/log/jgtservice/jgtservice.log
```

## Security Considerations

### Network Security
- Firewall configuration for port 8080
- Optional API key authentication
- HTTPS termination (use reverse proxy)

### File System Security
- Dedicated user account for service
- Restricted file permissions
- Separate data volumes

### Container Security
- Non-root user in containers
- Read-only root filesystem where possible
- Security scanning of container images

## Performance Tuning

### Resource Allocation
- CPU: Scale `JGTPY_SERVICE_MAX_WORKERS` based on available cores
- Memory: 2GB+ recommended for parallel processing
- Storage: SSD recommended for data directories

### Network Optimization
- Dropbox upload: Consider batch sizes for large datasets
- API responses: Enable compression for large data requests
- Monitoring: Adjust collection intervals based on load

## Troubleshooting

### Common Issues

1. **Service won't start**
   - Check configuration syntax
   - Verify data directory permissions
   - Confirm Dropbox token validity

2. **Processing failures**
   - Review individual instrument/timeframe logs
   - Check available disk space
   - Verify network connectivity

3. **Upload issues**
   - Validate Dropbox token and permissions
   - Check network connectivity
   - Review upload path configuration

### Debug Commands
```bash
# Verbose logging
jgtservice --refresh-once --all --verbose

# Status check
jgtservice --status

# Test configuration
python -c "from jgtpy.service import JGTServiceConfig; print(JGTServiceConfig.from_env().validate())"
```

## Backup and Recovery

### Data Backup
- Regular backup of data directories
- Configuration file backup
- Log file rotation and retention

### Service Recovery
- Automated restart policies
- Health check failure handling
- Graceful degradation strategies

## Migration Guide

### From Manual Scripts
1. Inventory current instruments and timeframes
2. Configure equivalent environment variables
3. Test with `--refresh-once` mode
4. Deploy daemon mode for continuous operation

### Version Upgrades
1. Stop service gracefully
2. Backup configuration and data
3. Update package: `pip install -U jgtpy[serve]`
4. Verify configuration compatibility
5. Restart service and monitor

---

For complete implementation details, see the main documentation: [docs/jgtservice_implementation.md](../../../docs/jgtservice_implementation.md) 
