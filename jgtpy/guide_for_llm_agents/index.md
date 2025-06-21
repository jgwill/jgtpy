# JGTPY Agent Guide

Welcome! This guide is designed for LLM-based agents. It explains the command line utilities shipped with **jgtpy** and how they work together.

## Quick Command Reference
```bash
# Data Generation
jgtcli -i EUR/USD -t m5 -c 100 -ba -ta -mw  # Full analysis
cdscli -i EUR/USD -t m5 -c 100               # Basic data

# Visualization  
jgtads -i EUR/USD -t m5 -c 100 -ba           # Comprehensive charts
jgtmouthwater -i EUR/USD -t m5 -c 50 --show  # Mouth/water analysis

# Utilities
pds2cds --input data.csv --output enhanced.csv  # Data conversion
guidecli_jgtpy --list                           # This documentation
```

## Core Sections

### Data Generation
- [jgtcli](jgtcli.md) - Primary enhanced data generation with full indicators
- [cdscli](cdscli.md) - Simplified CDS data creation  
- [pds2cds](pds2cds.md) - Raw data conversion utilities

### Visualization & Analysis
- [jgtads](adscli.md) - Advanced chart generation with multiple overlays
- [jgtmouthwater](jgtmouthwater.md) - Specialized alligator mouth/water state charts
- [jgtmksg](jgtmksg.md) - Market signal generation and analysis
- [jgtids](idscli.md) - Indicator-focused analysis

### Package Overview
- [Overview](overview.md) - Complete package capabilities and workflow
- [Integration](integration.md) - How commands work together

## Workflow Examples

### Complete Analysis Pipeline
```bash
# 1. Generate enhanced data
jgtcli -i EUR/USD -t m5 -c 200 -ba -ta -mw

# 2. Create comprehensive charts
jgtads -i EUR/USD -t m5 -c 200 -ba -ta -mw

# 3. Specialized mouth/water analysis
jgtmouthwater -i EUR/USD -t m5 -c 200 -ct last_state_analysis --show
```

### Multi-Timeframe Analysis
```bash
# Generate data across timeframes
jgtcli -i EUR/USD -t m5 -c 500 -ba -mw
jgtcli -i EUR/USD -t m15 -c 200 -ba -mw  
jgtcli -i EUR/USD -t H1 -c 100 -ba -mw

# Create comparative charts
jgtads -i EUR/USD -t m5 -c 500 -ba
jgtads -i EUR/USD -t m15 -c 200 -ba
jgtads -i EUR/USD -t H1 -c 100 -ba
```

## For LLM Agents

All commands provide:
- `--help` for detailed usage
- `-v` for verbose output and debugging
- Consistent parameter naming across utilities
- Standard error codes and messages

Use `guidecli_jgtpy --section SECTION_NAME` to get detailed information about any specific command.

