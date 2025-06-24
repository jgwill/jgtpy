# Issue #38: Data Refresh Service Implementation

## Current Package Analysis

### Existing Architecture

#### Core Services
1. **PDS (Price Data Service)** - `JGTPDSPSvc.py`
   - Base price data acquisition and storage
   - Used by all other services as foundation

2. **IDS (Indicator Data Service)** - `JGTIDSSvc.py`
   - Technical indicator calculations
   - Adds indicators like Alligator, AO, AC, MFI, fractals
   - Produces data documented in `docs/IDS_purpose.md`

3. **CDS (Chaos Data Service)** - `JGTCDSSvc.py`
   - Advanced indicator processing and signal generation
   - Combines IDS data with additional analysis
   - Produces columns documented in `docs/CDS_data_columns.md`

#### Current CLI Tools
- `jgtcli` - Main CDS data processing
- `cdscli` - CDS-specific operations  
- `jgtids` - IDS processing
- `jgtads` - Advanced Data Service
- Other utilities for specific operations

#### Request Architecture
- `JGTPDSRequest.py` - Base request class
- `JGTIDSRequest.py` - Extends PDS for indicators
- `JGTCDSRequest.py` - Extends IDS for chaos data
- All use `jgtcommon.py` for settings and argument parsing

#### Legacy Server Components
- `fsserver.py` - Old Flask server (deprecated)
- `idsserver.py` - Old IDS server (deprecated)
- `JGTCloudFS.py` - Dropbox integration (3-4 years old, unused)

### Current Data Flow

```
PDS (Base Price Data) → IDS (+ Indicators) → CDS (+ Signals/Analysis)
```

### Example Current Usage (from user request)
```bash
for t in H4 H1 m15 m5; do 
  for i in XAU/USD EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD; do 
    (jgtcli -i $i -t $t --fresh && (p=$(jgtcli -i $i -t $t --fresh -vp); droxul upload $p /dist/data/current/cds&))
  done
done
```

## Requirements Analysis

### Primary Goals
1. **Automated Data Refresh Service**
   - Run at specified timeframes using scheduler similar to `timeframe_scheduler.py`
   - Support parallel processing for multiple instruments/timeframes
   - Initial data refresh on service startup

2. **Distribution/Upload Integration**
   - Dropbox upload using Python dropbox package (not droxul CLI)
   - Upload to configurable paths
   - Support both current and full data variants

3. **Service Architecture** 
   - New CLI entry point for service mode
   - Web API endpoints for data access
   - Configurable via environment variables and settings files

4. **Package Structure**
   - `pip install jgtpy[serve]` for server dependencies
   - Keep base package lightweight
   - Optional server requirements

### Environment Variables (from user example)
```bash
JGTPY_DATA=/src/jgtpy/data/current
JGTPY_DATA_FULL=/src/jgtpy/data/full
TRADABLE_TIMEFRAMES="D1 H4 H1"
HIGH_TIMEFRAMES="M1 W1 D1 H4"
LOW_TIMEFRAMES="H4 H1 m15 m5"
JGTPY_DROPBOX_APP_TOKEN=<token>
```

## Technical Requirements

### Scheduler Integration
- Implement timeframe-based scheduling similar to `jgtutils.timeframe_scheduler`
- Support `-t <timeframe>` with automatic refresh
- Configurable instrument/timeframe combinations

### Parallel Processing
- Use `concurrent.futures` for parallel data processing
- Process multiple instruments/timeframes simultaneously
- Respect system resources and API limits

### Data Upload
- Modernize `JGTCloudFS.py` Dropbox integration
- Use Python `dropbox` package directly
- Support batch uploads with error handling

### Web Service
- Replace deprecated server files with modern implementation
- REST API endpoints for data access
- Health checks and status endpoints

## Implementation Strategy

### Phase 1: Core Service Framework
1. Create new service module `jgtpy/service/`
2. Implement base scheduler using timeframe_scheduler patterns
3. Add parallel processing for data refresh
4. Update pyproject.toml with new CLI entries

### Phase 2: Data Processing Integration  
1. Integrate with existing PDS/IDS/CDS services
2. Add configuration management for instruments/timeframes
3. Implement error handling and logging
4. Add status tracking and metrics

### Phase 3: Distribution & Upload
1. Modernize Dropbox integration
2. Add configurable upload paths
3. Implement batch processing and retry logic
4. Add upload status tracking

### Phase 4: Web Service & API
1. Create modern web service framework
2. Add REST endpoints for data access
3. Implement authentication if needed
4. Add monitoring and health checks

### Phase 5: Package Structure & Documentation
1. Update pyproject.toml for optional server dependencies
2. Add comprehensive documentation
3. Create deployment guides
4. Add example configurations

## Key Design Decisions

### Service Architecture
- Single service binary with multiple modes (scheduler, web server, one-time refresh)
- Configuration-driven instrument/timeframe selection
- Modular design allowing independent components

### Data Management
- Support both "current" and "full" data variants
- Configurable data retention policies  
- Atomic updates to prevent partial data states

### Error Handling
- Graceful degradation on individual instrument/timeframe failures
- Comprehensive logging with structured output
- Retry mechanisms for transient failures

### Performance
- Parallel processing with configurable concurrency
- Memory-efficient data processing
- Optimized I/O operations

## Success Criteria

1. **Functional Requirements**
   - [ ] Service runs continuously with timeframe-based refresh
   - [ ] Parallel processing of multiple instruments/timeframes
   - [ ] Automatic Dropbox upload of processed data
   - [ ] Web API access to current data
   - [ ] Configuration via environment variables

2. **Non-Functional Requirements**
   - [ ] `pip install jgtpy[serve]` works correctly
   - [ ] Service resilient to individual processing failures
   - [ ] Memory usage remains stable during long runs
   - [ ] Processing times within acceptable limits
   - [ ] Comprehensive logging and monitoring

3. **Integration Requirements**
   - [ ] Compatible with existing jgtcli workflow
   - [ ] Uses current PDS/IDS/CDS processing logic
   - [ ] Settings system integration maintained
   - [ ] Backward compatibility with existing scripts

## Next Steps

1. **Analysis Phase**: Complete detailed code review of existing services
2. **Design Phase**: Create detailed technical specifications  
3. **Implementation Phase**: Begin with Phase 1 development
4. **Testing Phase**: Comprehensive testing with real data
5. **Documentation Phase**: User guides and API documentation
6. **Deployment Phase**: Production deployment procedures

## Notes

- This implementation will modernize the data processing pipeline while maintaining compatibility
- Focus on reliability and observability for production use
- Consider containerization for easier deployment
- Plan for horizontal scaling if needed in future
