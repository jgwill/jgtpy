# JGTPY Data Refresh Service - Implementation Roadmap

## Overview
Implementation of automated data refresh service for jgtpy package with timeframe-based scheduling, parallel processing, and cloud distribution capabilities.

**Related Issue**: [jgwill/jgtpy#38](https://github.com/jgwill/jgtpy/issues/38)

## Phase 1: Core Service Framework (Week 1-2)

### Task 1.1: Project Structure Setup
- [ ] Create `jgtpy/service/` module directory
- [ ] Add `__init__.py` and base service classes
- [ ] Update `pyproject.toml` with optional server dependencies
- [ ] Add `[serve]` extra requirements section

**Files to create:**
- `jgtpy/service/__init__.py`
- `jgtpy/service/base.py`
- `jgtpy/service/scheduler.py`

### Task 1.2: Basic Scheduler Implementation  
- [ ] Adapt `timeframe_scheduler.py` patterns for jgtpy
- [ ] Create `JGTScheduler` class with timeframe awareness
- [ ] Add support for multiple instruments/timeframes
- [ ] Implement graceful shutdown handling
- [ ] Make sure that a new cli command is runnable in `pyproject.toml` like : jgtschedulercli (or a better name than that)
- [ ] Important, launching a server and running a CLI to have fresh prices are 2 things (that service or runner or whatever you call it must be independent or at least installed by default and wont need the  `[serve]`)
- [ ]  We have to distribute the data to dropbox. Use "JGTPY_DROPBOX_APP_TOKEN" from the .env make sure to read CWD/.env or $HOME/.env or from the $HOME/.jgt/config.json

**Key Components:**
```python
class JGTScheduler:
    def __init__(self, config)
    def start(self)
    def stop(self)
    def schedule_refresh(self, timeframe, callback)
```

### Task 1.3: Configuration Management
- [ ] Extend `jgtcommon.py` settings for service configuration
- [ ] Add environment variable support for service settings
- [ ] Create default service configuration template
- [ ] Add validation for service configuration

**Environment Variables:**
- `JGTPY_SERVICE_INSTRUMENTS`
- `JGTPY_SERVICE_TIMEFRAMES`
- `JGTPY_SERVICE_REFRESH_INTERVAL`
- `JGTPY_SERVICE_PARALLEL_WORKERS`

### Task 1.4: CLI Entry Points
- [ ] Create `jgtservice` main CLI script
- [ ] Add service mode flags (--daemon, --web, --refresh-once)
- [ ] Integrate with existing argument parsing patterns
- [ ] Add service status and control commands

**New CLI Commands:**
```bash
jgtservice --daemon --timeframes "H1,m15" --instruments "EUR/USD,XAU/USD"
jgtservice --web --port 8080
jgtservice --refresh-once --all
jgtservice --status
```

## Phase 2: Data Processing Integration (Week 3-4)

### Task 2.1: Service Request Handlers
- [ ] Create service-specific request classes extending existing ones
- [ ] Add batch processing capabilities
- [ ] Implement request queuing and prioritization
- [ ] Add request tracking and status reporting

**New Classes:**
- `JGTServiceRequest` (extends `JGTCDSRequest`)
- `BatchProcessor`
- `RequestQueue`

### Task 2.2: Parallel Processing Engine
- [ ] Implement `concurrent.futures` based processor
- [ ] Add configurable worker pool management
- [ ] Create resource monitoring and throttling
- [ ] Add progress tracking and reporting

**Key Features:**
```python
class ParallelProcessor:
    def __init__(self, max_workers=4)
    def process_batch(self, requests)
    def monitor_resources(self)
    def get_progress(self)
```

### Task 2.3: Error Handling & Resilience
- [ ] Add comprehensive error handling for individual failures
- [ ] Implement retry mechanisms with exponential backoff
- [ ] Create failure isolation (one instrument failure doesn't stop others)
- [ ] Add detailed logging with structured output

### Task 2.4: Integration with Existing Services
- [ ] Integrate with `JGTCDSSvc.py` for CDS processing
- [ ] Use existing `JGTIDSSvc.py` for IDS processing  
- [ ] Maintain compatibility with current PDS services
- [ ] Add service-level caching and optimization

## Phase 3: Distribution & Upload (Week 5-6)

### Task 3.1: Modernize Dropbox Integration
- [ ] Update `JGTCloudFS.py` to use current dropbox package
- [ ] Add authentication handling and token management
- [ ] Implement batch upload capabilities
- [ ] Add upload progress tracking and resumption

**Enhanced CloudFS:**
```python
class JGTCloudFS:
    def __init__(self, token)
    def upload_batch(self, file_paths, remote_paths)
    def verify_uploads(self, file_list)
    def get_upload_status(self)
```

### Task 3.2: Upload Configuration
- [ ] Add configurable upload paths per data type
- [ ] Support different upload destinations (current vs full)
- [ ] Add upload filtering based on instrument/timeframe
- [ ] Implement upload scheduling and throttling

### Task 3.3: Upload Status & Monitoring
- [ ] Create upload status tracking system
- [ ] Add upload verification and integrity checking
- [ ] Implement upload retry mechanisms
- [ ] Add upload metrics and reporting

### Task 3.4: Local File Management
- [ ] Add automatic file cleanup policies
- [ ] Implement data retention management
- [ ] Create backup and archive functionality
- [ ] Add disk space monitoring

## Phase 4: Web Service & API (Week 7-8)

### Task 4.1: Modern Web Framework
- [ ] Replace deprecated Flask servers with FastAPI
- [ ] Create RESTful API endpoints for data access
- [ ] Add OpenAPI/Swagger documentation
- [ ] Implement proper HTTP status codes and error handling

**API Endpoints:**
```
GET /api/v1/data/{instrument}/{timeframe}
GET /api/v1/status
GET /api/v1/health
POST /api/v1/refresh
GET /api/v1/upload/status
```

### Task 4.2: Data Access API
- [ ] Create endpoints for CDS data retrieval
- [ ] Add filtering and pagination support
- [ ] Implement data format options (JSON, CSV)
- [ ] Add caching headers and ETags

### Task 4.3: Service Management API
- [ ] Add service control endpoints (start/stop/status)
- [ ] Create configuration update endpoints
- [ ] Add metrics and monitoring endpoints
- [ ] Implement health check functionality

### Task 4.4: Security & Authentication
- [ ] Add API key authentication if needed
- [ ] Implement rate limiting
- [ ] Add CORS support for web access
- [ ] Create access logging and monitoring

## Phase 5: Package Structure & Documentation (Week 9-10)

### Task 5.1: Package Configuration Updates
- [ ] Update `pyproject.toml` with server dependencies
- [ ] Create `[serve]` extra requirements group
- [ ] Add new CLI entry points
- [ ] Update package metadata and descriptions

**Additional Dependencies for [serve]:**
```toml
serve = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0", 
    "httpx>=0.25.0",
    "aiofiles>=23.2.1"
]
```

### Task 5.2: Service Scripts Registration
- [ ] Add `jgtservice` to project.scripts
- [ ] Create `jgtservice-web` for web-only mode
- [ ] Add `jgtservice-daemon` for background service
- [ ] Create `jgtservice-upload` for upload-only operations

### Task 5.3: Configuration Templates
- [ ] Create example service configuration files
- [ ] Add environment variable documentation
- [ ] Create Docker configuration examples
- [ ] Add systemd service templates

### Task 5.4: Documentation & Guides
- [ ] Create comprehensive user documentation
- [ ] Add API documentation with examples
- [ ] Create deployment guides for different environments
- [ ] Add troubleshooting and FAQ sections

## Phase 6: Testing & Validation (Week 11-12)

### Task 6.1: Unit Testing
- [ ] Add unit tests for all new service components
- [ ] Test scheduler functionality with mock timeframes
- [ ] Test parallel processing with controlled loads
- [ ] Add configuration validation tests

### Task 6.2: Integration Testing
- [ ] Test full service lifecycle (start/run/stop)
- [ ] Validate data processing pipeline integration
- [ ] Test Dropbox upload functionality
- [ ] Verify API endpoint functionality

### Task 6.3: Performance Testing
- [ ] Benchmark parallel processing performance
- [ ] Test memory usage during long runs
- [ ] Validate upload performance with large datasets
- [ ] Test service under various load conditions

### Task 6.4: End-to-End Testing
- [ ] Test complete workflow from scheduling to upload
- [ ] Validate error recovery and resilience
- [ ] Test configuration changes without restart
- [ ] Verify backward compatibility with existing tools

## Success Metrics

### Functional Metrics
- [ ] Service successfully processes data for all configured instruments/timeframes
- [ ] Parallel processing reduces total processing time by >50%
- [ ] Upload success rate >99% with retry mechanisms
- [ ] API response times <500ms for data requests

### Reliability Metrics  
- [ ] Service uptime >99.9% during testing period
- [ ] Individual processing failures don't affect other instruments
- [ ] Memory usage remains stable during 24+ hour runs
- [ ] Graceful recovery from network/service interruptions

### Integration Metrics
- [ ] `pip install jgtpy[serve]` works on clean environment
- [ ] Existing jgtcli commands continue to work unchanged
- [ ] Service configuration via environment variables works
- [ ] API provides equivalent data to direct file access

## Risk Mitigation

### Technical Risks
- **Risk**: Parallel processing causes resource exhaustion
  - **Mitigation**: Implement resource monitoring and adaptive throttling
  
- **Risk**: Network failures during uploads
  - **Mitigation**: Implement robust retry mechanisms and upload verification

- **Risk**: Service instability during long runs  
  - **Mitigation**: Add comprehensive health monitoring and auto-restart

### Integration Risks
- **Risk**: Breaking changes to existing workflow
  - **Mitigation**: Maintain strict backward compatibility, extensive testing

- **Risk**: Configuration complexity
  - **Mitigation**: Provide sensible defaults, clear documentation, validation

## Deployment Considerations

### Development Environment
- Local development with minimal configuration
- Mock services for external dependencies
- Hot reload for rapid iteration

### Production Environment
- Containerized deployment with Docker
- systemd service configuration for Linux
- Monitoring and alerting integration
- Log aggregation and analysis

### Monitoring & Observability
- Structured logging with correlation IDs
- Metrics collection (processing times, success rates, etc.)
- Health check endpoints for monitoring systems
- Alert definitions for critical failures

## Future Enhancements (Post-Launch)

- Horizontal scaling with multiple service instances
- Advanced caching strategies (Redis integration)
- Real-time WebSocket data feeds
- Advanced analytics and reporting dashboard
- Machine learning integration for predictive scheduling
- Multi-cloud upload support (AWS S3, Google Cloud Storage)
