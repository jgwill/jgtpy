# pds2cds - PDS to CDS Data Conversion

Utility for converting raw Price Data Service (PDS) files into enhanced Chaos Data Service (CDS) format with basic indicators.

## Console Command
```bash
pds2cds --input INPUT_FILE --output OUTPUT_FILE [OPTIONS]
```

## Parameters
- `--input, -i` - Input PDS CSV file path
- `--output, -o` - Output CDS CSV file path  
- `--instrument` - Trading pair override (e.g., EUR/USD)
- `--timeframe` - Timeframe override (e.g., m5, m15, H1)
- `-v, --verbose` - Verbosity level

## Usage Examples

### Basic File Conversion
```bash
# Convert single PDS file to CDS
pds2cds --input raw_data.csv --output enhanced_data.csv

# With instrument specification
pds2cds --input eurusd_raw.csv --output eurusd_cds.csv --instrument EUR/USD
```

### Batch Processing
```bash
# Multiple file conversion
pds2cds --input data/eur_m5.csv --output cds/eur_m5.csv --instrument EUR/USD --timeframe m5
pds2cds --input data/gbp_m5.csv --output cds/gbp_m5.csv --instrument GBP/USD --timeframe m5
pds2cds --input data/usd_m5.csv --output cds/usd_m5.csv --instrument USD/JPY --timeframe m5
```

### Directory Processing
```bash
# Process multiple files with pattern
for file in data/*.csv; do
    base=$(basename "$file" .csv)
    pds2cds --input "$file" --output "cds/${base}_cds.csv" -v 1
done
```

## Input PDS Format Requirements
Expected CSV columns in PDS files:
- Date/Time column (various formats supported)
- BidOpen, BidHigh, BidLow, BidClose
- AskOpen, AskHigh, AskLow, AskClose (optional)
- Volume (optional)

Example PDS format:
```csv
DateTime,BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose,Volume
2024-01-15 10:00:00,1.0856,1.0859,1.0854,1.0857,1.0858,1.0861,1.0856,1.0859,150
```

## Output CDS Enhancements
Converted files include:
- Standardized datetime formatting
- Basic zone classification (buy/sell/neutral)
- Data validation and cleaning
- Missing data interpolation
- Consistent column naming
- Proper CSV structure for jgtpy tools

## Integration with jgtpy Pipeline

### Typical Workflow
```bash
# 1. Convert raw broker data to CDS
pds2cds --input broker_export.csv --output base_cds.csv --instrument EUR/USD --timeframe m5

# 2. Enhance with full indicators
jgtcli --input-file base_cds.csv -i EUR/USD -t m5 -ba -ta -mw

# 3. Generate charts
jgtads -i EUR/USD -t m5 -c 200 -ba -ta
```

### Data Source Integration
```bash
# From MT4/MT5 exports
pds2cds --input MT5_EURUSD_M5.csv --output eurusd_m5.csv --instrument EUR/USD --timeframe m5

# From broker API data
pds2cds --input api_data.csv --output processed.csv --instrument GBP/USD --timeframe m15

# From third-party data providers
pds2cds --input provider_data.csv --output standardized.csv -v 1
```

## Data Validation Features
- Automatic datetime parsing and standardization
- OHLC data validation (High >= Low, etc.)
- Missing data detection and reporting
- Duplicate timestamp handling
- Volume data validation (if present)
- Timezone handling and conversion

## Error Handling
The tool provides detailed error reporting for:
- Invalid file formats
- Missing required columns
- Data inconsistencies
- File access issues
- Memory limitations for large files

## Performance Considerations
- Optimized for large CSV files (millions of rows)
- Memory-efficient streaming processing
- Progress reporting for long operations
- Batch processing capabilities
- Automatic data type optimization

## Output Location
By default, creates files in:
```
/workspace/data/current/cds/[OUTPUT_FILE]
```

Use absolute paths for custom locations.
