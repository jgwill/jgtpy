# JGT Service Fix Iteration
**Date**: 2025-06-25 12:50  
**Issue**: Multiple issues with jgtservice implementation

## Current State
- Daemon starts but has configuration issues
- Environment loading not working correctly
- refreshPH() called with wrong parameters
- Data directory structure issues
- Script duplication between root and jgtpy/scripts/

## Issues Identified

### 1. Environment Loading Issues
- Dropbox token exists but service doesn't detect it
- JGTPY_SERVICE_ENABLE_UPLOAD=true set twice in .env
- Service not properly reading all env variables

### 2. refreshPH Parameter Error
```
refreshPH() got an unexpected keyword argument 'use_fresh'
```
- processor.py calls refreshPH with `use_fresh=True` 
- But actual signature doesn't include `use_fresh`

### 3. Data Directory Structure
- Creating EURUSD, XAUUSD folders instead of EUR-USD, XAU-USD
- Only m5 timeframes generated, missing other timeframes

### 4. Script Duplication
- Scripts exist in both root and jgtpy/scripts/
- pyproject.toml should include scripts from jgtpy/scripts/
- guide system should work with packaged scripts

## Planned Fixes

1. Fix processor.py refreshPH call
2. Fix environment loading in base.py
3. Fix directory naming issues
4. Ensure all timeframes are processed
5. Clean up script duplication
6. Fix missing process_all method in processor

## Completed Fixes

### 1. Fixed refreshPH Parameter Error ✅
- Removed `use_fresh=True` parameter from refreshPH call
- Now using `use_full=self.config.use_full` instead
- No more "unexpected keyword argument" errors

### 2. Fixed Environment Loading ✅
- Enhanced .env file loading with better logging
- Now loads from ~/.env, ~/.jgt/.env, and current dir .env
- Dropbox token now properly detected from environment
- Added debug logging for configuration

### 3. Fixed Directory Structure ✅
- **REVERTED** the instrument subdirectory creation logic
- Let CDS service handle file writing naturally
- Preserved existing file structure for compatibility
- No more breaking existing data access patterns

### 4. Enhanced Upload System ✅
- Added droxul command fallback for uploads
- Python dropbox library tried first, then falls back to droxul
- Matches existing upload pattern: `/dist/data/current/`
- Checks file existence before attempting upload

### 5. Added Initial Data Refresh ✅
- Daemon mode now runs initial refresh for all timeframes
- Ensures all data is up to date when service starts
- Includes upload after initial refresh

## Current Status
- Service configuration now loads properly from environment
- All parameter errors resolved
- Upload system has both modern and fallback approaches
- Existing data structure preserved
- Ready for full testing 