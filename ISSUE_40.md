# Issue #40: JGT Service Timeframe Parsing and Data Refresh Fixes

## Problem Analysis

### Current Issues Identified

1. **Timeframe Parsing Error**: The service is passing timeframes as a single string "D1 H4 H1" instead of individual timeframes, causing jgtfxcli to fail with "unrecognized arguments: H4 H1"

2. **Limited Data Processing**: Only processing 1 instrument/timeframe combination instead of all configured instruments and timeframes

3. **Missing PDS Data Refresh**: The service is not properly refreshing PDS (Price Data Service) data before creating CDS data

4. **Command Line Argument Handling**: The refresh-all.sh script is not properly passing multiple timeframes and instruments to the service

## Root Cause Analysis

### Issue 1: Timeframe Parsing in Configuration
- Environment variable `TRADABLE_TIMEFRAMES="D1 H4 H1"` contains spaces instead of commas
- The service is treating this as a single timeframe string instead of parsing it into individual timeframes
- This affects both the service configuration and the command line argument building

### Issue 2: PDS Data Refresh Dependency
- CDS data creation depends on fresh PDS data
- The current service implementation doesn't ensure PDS data is refreshed before CDS processing
- Need to integrate with `JGTPDSP.py` and `jgtwslhelper.py` for proper data refresh

### Issue 3: Command Line Argument Building
- The refresh-all.sh script builds command line arguments incorrectly
- Multiple timeframes should be passed as separate `-t` arguments
- Multiple instruments should be passed as separate `-i` arguments

## Fix Plan

### Phase 1: Fix Timeframe Parsing (Critical)

#### 1.1 Fix Environment Variable Parsing
- Update `JGTServiceConfig.from_env()` to properly handle space-separated timeframes
- Add support for both comma-separated and space-separated formats
- Ensure consistent parsing across all configuration sources

#### 1.2 Fix Command Line Argument Building
- Update `refresh-all.sh` to properly build command line arguments
- Ensure each timeframe gets its own `-t` argument
- Ensure each instrument gets its own `-i` argument

#### 1.3 Fix Service Argument Parsing
- Update `jgtservice.py` to properly handle multiple `-t` and `-i` arguments
- Fix the argument parsing logic in `create_config_from_args()`

### Phase 2: Integrate PDS Data Refresh (Critical)

#### 2.1 Understand PDS Refresh Flow
- Study `JGTPDSP.py` and `jgtwslhelper.py` to understand the data refresh mechanism
- Identify how `jgtfxcli` is used to refresh price data
- Understand the relationship between PDS and CDS data

#### 2.2 Update Service Processor
- Modify `ParallelProcessor` to ensure PDS data is fresh before CDS processing
- Integrate with `JGTPDSP.refreshPH()` or equivalent functionality
- Add proper error handling for PDS refresh failures

#### 2.3 Update CDS Processing
- Ensure `JGTCDSSvc.get()` is called with proper parameters
- Verify that fresh PDS data is available before CDS processing
- Add validation to check data freshness

### Phase 3: Fix Data Processing Flow

#### 3.1 Update Processor Logic
- Fix the `_process_single()` method to handle all instrument/timeframe combinations
- Ensure parallel processing works correctly with multiple combinations
- Add proper logging for each processing step

#### 3.2 Fix File Path Generation
- Update file path generation to match the expected directory structure
- Ensure CDS files are saved in the correct location
- Add validation for file creation success

#### 3.3 Fix Upload Integration
- Ensure uploader processes all generated files
- Fix batch upload logic to handle multiple files
- Add proper error handling for upload failures

### Phase 4: Testing and Validation

#### 4.1 Unit Testing
- Test timeframe parsing with various formats
- Test instrument parsing with various formats
- Test PDS refresh integration

#### 4.2 Integration Testing
- Test complete data refresh flow
- Test parallel processing with multiple combinations
- Test upload functionality

#### 4.3 End-to-End Testing
- Test `refresh-all.sh` with default parameters
- Test `jgtservice --refresh-once` with multiple instruments/timeframes
- Verify data files are created correctly

## Implementation Details

### Files to Modify

1. **jgtpy/service/base.py**
   - Fix `JGTServiceConfig.from_env()` timeframe parsing
   - Add support for space-separated timeframes

2. **jgtpy/jgtservice.py**
   - Fix argument parsing for multiple `-t` and `-i` arguments
   - Update `create_config_from_args()` method

3. **jgtpy/service/processor.py**
   - Integrate PDS data refresh before CDS processing
   - Fix `_process_single()` method
   - Update file path generation

4. **refresh-all.sh**
   - Fix command line argument building
   - Ensure proper `-t` and `-i` argument formatting

5. **jgtpy/service/uploader.py**
   - Fix batch upload logic
   - Add proper error handling

### Key Changes Required

#### 1. Timeframe Parsing Fix
```python
# In JGTServiceConfig.from_env()
timeframes_env = os.getenv("JGTPY_SERVICE_TIMEFRAMES",
                          os.getenv("TRADABLE_TIMEFRAMES", 
                                   os.getenv("LOW_TIMEFRAMES")))
if timeframes_env:
    # Handle both comma and space separation
    if ',' in timeframes_env:
        config.timeframes = [t.strip() for t in timeframes_env.split(",")]
    else:
        config.timeframes = [t.strip() for t in timeframes_env.split()]
```

#### 2. PDS Integration
```python
# In ParallelProcessor._process_single()
# First refresh PDS data
from JGTPDSP import refreshPH
refreshPH(instrument, timeframe, quote_count=-1, use_fresh=True)

# Then process CDS data
from JGTCDSSvc import get
cdf = get(instrument=instrument, timeframe=timeframe, ...)
```

#### 3. Command Line Argument Fix
```bash
# In refresh-all.sh
# Convert comma-separated timeframes to individual -t arguments
IFS=',' read -ra TF_ARRAY <<< "$TIMEFRAMES"
for tf in "${TF_ARRAY[@]}"; do
    tf=$(echo "$tf" | xargs)  # trim whitespace
    CMD="$CMD -t $tf"
done
```

## Success Criteria

1. **Timeframe Parsing**: Service correctly processes multiple timeframes from environment variables and command line arguments

2. **Data Refresh**: All configured instruments and timeframes are processed, not just one combination

3. **PDS Integration**: Fresh PDS data is retrieved before CDS processing

4. **File Generation**: CDS files are created for all instrument/timeframe combinations

5. **Upload Success**: All generated files are successfully uploaded to Dropbox

## Testing Strategy

### Manual Testing
1. Test `refresh-all.sh` with default parameters
2. Test `jgtservice --refresh-once` with multiple instruments/timeframes
3. Verify data files are created in `$JGTPY_DATA/cds/`
4. Verify uploads to Dropbox

### Automated Testing
1. Unit tests for timeframe parsing
2. Integration tests for data processing flow
3. End-to-end tests for complete refresh cycle

## Timeline

- **Phase 1**: 1-2 hours (Critical - timeframe parsing)
- **Phase 2**: 2-3 hours (Critical - PDS integration)
- **Phase 3**: 1-2 hours (Data processing flow)
- **Phase 4**: 1-2 hours (Testing and validation)

**Total Estimated Time**: 5-9 hours

## Notes

- This fix is critical for the service to work as expected
- The current implementation only processes one instrument/timeframe combination instead of all configured ones
- PDS data refresh is essential for accurate CDS data generation
- The timeframe parsing issue affects both the service and the refresh script
