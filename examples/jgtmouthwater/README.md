# JGT Mouth Water Plotting Examples

Specialized plotting for alligator mouth and water states with symbol representation.

## Overview

This example demonstrates the mouth water plotting capabilities of jgtpy, which provides visual analysis of alligator mouth and water states using specialized symbols and multiple chart perspectives.

## Features

- **Symbol Representation**: ASCII-compatible symbols for all water states and mouth directions
- **Last Completed Period Focus**: Emphasizes the most recent completed bar (not current incomplete)
- **Multiple Chart Types**: 3 different visualization perspectives
- **Zone Integration**: Combines with zone color analysis
- **CLI Interface**: Easy command-line access

## Prerequisites

Ensure you have jgtpy installed:
```bash
pip install jgtpy
```

## Chart Types Available

### 1. Last State Analysis (default)
Detailed 2x2 analysis of the most recent completed bar:
- State summary with symbols
- Recent evolution timeline
- State distribution pie chart
- Zone-state correlation matrix

### 2. States Timeline
4-panel view showing evolution over time:
- Water states progression
- Mouth direction changes
- Bar position tracking
- Zone color background

### 3. Zone Combined
Price analysis with zone integration:
- Price chart with zone backgrounds
- Combined state visualization
- State change point detection

## Usage Examples

### Basic Usage (Last State Analysis)
```bash
jgtmouthwater -i EUR/USD -t m5 -c 50 --show
```

### States Timeline Chart
```bash
jgtmouthwater -i EUR/USD -t m5 -c 100 -ct states_timeline --show
```

### Zone Combined Analysis
```bash
jgtmouthwater -i EUR/USD -t m5 -c 75 -ct zone_combined --show
```

### Help and Options
```bash
jgtmouthwater --help
```

## Symbol Legend

### Water States
- `s` - Splashing (active movement)
- `o` - Eating (consuming trend)
- `X` - Throwing (rejecting movement)
- `^` - Popping (bursting action)
- `>` - Entering (beginning entry)
- `D` - Switching (changing state)
- `.` - Sleeping (dormant/quiet)

### Mouth Direction
- `^` - Buy direction (upward pressure)
- `v` - Sell direction (downward pressure)
- `D` - Neither (neutral/indecisive)

### Bar Position
- `^` - Above (price above alligator)
- `s` - In (price within alligator)
- `v` - Below (price below alligator)

## Running Examples

Execute the comprehensive demo:
```bash
./run.sh
```

This will generate all chart types and save example images for reference.

## Output Files

The examples generate:
- `last_state_analysis_example.png` - Detailed state analysis
- `states_timeline_example.png` - Evolution timeline
- `zone_combined_example.png` - Zone integration analysis
- `example_output.txt` - Console output with state information

## Integration with Trading Workflow

The mouth water analysis integrates seamlessly with the jgtpy pipeline:

```bash
# Generate CDS data with mouth water analysis
jgtcli -i EUR/USD -t m5 -c 100 -mw

# Create specialized visualization
jgtmouthwater -i EUR/USD -t m5 -c 100 -ct last_state_analysis --show
```

## Technical Details

- **Data Source**: Uses real forex data from connected broker
- **Analysis Period**: Focuses on last completed bar (second-to-last row)
- **Compatibility**: Matplotlib-compatible symbols for reliable rendering
- **Performance**: Optimized for real-time analysis with minimal latency

## Troubleshooting

If charts don't display:
1. Ensure you have matplotlib backend configured
2. Use `--show` flag to force display
3. Check that mouth water data is available in your dataset

For data issues:
1. Verify instrument and timeframe are valid
2. Ensure sufficient historical data (minimum 50 bars recommended)
3. Check broker connection for real-time data 