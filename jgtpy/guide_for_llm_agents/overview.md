# JGTPY Overview

`jgtpy` is a comprehensive financial data processing and visualization package for algorithmic trading analysis.

## Core Concept: Data Pipeline
PDS → CDS → IDS → ADS → Plotting

- **PDS** (Price Data Service): Raw OHLCV price data from brokers
- **CDS** (Chaos Data Service): Enhanced data with technical indicators and zone analysis  
- **IDS** (Indicator Data Service): Advanced indicator calculations
- **ADS** (Analytics Data Service): Chart generation and visualization

## Available Console Commands

### Primary Data Generation
- `jgtcli` - Main CLI for CDS generation with full indicator suite
- `cdscli` - Simplified CDS generation  
- `pds2cds` - Convert raw PDS files to CDS format

### Visualization & Analysis  
- `jgtads` - Advanced chart generation with multiple indicator overlays
- `jgtmksg` - Market signal generation and analysis
- `jgtids` - Indicator-focused analysis
- `jgtmouthwater` - Specialized alligator mouth/water state visualization

### Utilities
- `adscli` - Legacy ADS chart generation
- `idscli` - IDS file operations
- `adsfromcds` - Extract ADS data from CDS files
- `guidecli_jgtpy` - This documentation system

## Key Features

### Technical Indicators
- Bill Williams Suite: Alligator, Awesome Oscillator, Accelerator
- Volume indicators: MFI, Volume analysis
- Custom mouth/water state analysis for trend identification

### Zone Analysis  
- Automatic buy/sell/neutral zone detection
- Zone-based coloring and visualization
- Integration with all chart types

### Multi-Timeframe Support
- m1, m5, m15, m30, H1, H4, D1 timeframes
- Cross-timeframe analysis capabilities

### Broker Integration
- Real-time data from connected brokers
- Historical data processing
- Multiple instrument support (EUR/USD, GBP/USD, etc.)

## Quick Start

```bash
# Generate enhanced data with all indicators
jgtcli -i EUR/USD -t m5 -c 100 -ba -ta -mw

# Create comprehensive charts  
jgtads -i EUR/USD -t m5 -c 100

# Specialized mouth water analysis
jgtmouthwater -i EUR/USD -t m5 -c 50 --show
```

## For LLM Agents

This package is designed to be LLM-friendly with:
- Consistent CLI interfaces across all commands
- Comprehensive help systems (`--help` on any command)
- Standardized data formats and file structures
- Detailed documentation via `guidecli_jgtpy`

All commands support `-v` verbosity levels and provide clear error messages for troubleshooting.
