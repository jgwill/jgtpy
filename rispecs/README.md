# JGTpy RISE Specifications

> Reverse-engineer → Intent-extract → Specify → Export

This directory contains RISE-compliant specifications for JGTpy - the core data services package that transforms raw price data into signal-rich trading intelligence through IDS, CDS, and ADS layers.

## Quick Start

1. **Start Here**: [`app.specs.md`](./app.specs.md) - Master orchestration specification
2. **Data Flow**: [`data-pipeline.spec.md`](./data-pipeline.spec.md) - PDS→IDS→CDS→ADS flow
3. **CLI Tools**: [`cli.spec.md`](./cli.spec.md) - All available commands

## Specification Map

```
app.specs.md                    ← Master specification (start here)
├── data-pipeline.spec.md       ← PDS→IDS→CDS→ADS transformation
├── ids.spec.md                 ← Indicator Data Service
├── cds.spec.md                 ← Chaos Data Service (signals)
├── ads.spec.md                 ← Advanced Data Service (charts)
├── cli.spec.md                 ← CLI tools (jgtcli, cdscli, etc.)
├── signals.spec.md             ← Signal detection logic
├── glyph.spec.md               ← Glyph generation for terminal
└── service.spec.md             ← jgtservice daemon
```

## RISE Framework Compliance

✅ **Desired Outcome Definition** - What users CREATE, not problems to solve  
✅ **Structural Tension** - Current reality vs desired state drives progression  
✅ **Natural Advancement** - Clear flow from current to desired  
✅ **Autonomous Specification** - Another LLM could implement from spec alone

## Key Concepts

### Data Layer Hierarchy
1. **PDS** - Price Data Service (raw OHLCV)
2. **IDS** - Indicator Data Service (adds Williams indicators)
3. **CDS** - Chaos Data Service (adds trading signals)
4. **ADS** - Advanced Data Service (visualization/charts)

### Core Signals
- **FDB** - Fractal Divergent Bar (buy/sell)
- **ZLC** - Zero Line Crossing
- **Saucer** - AO saucer patterns
- **Zone** - Green/Red zone signals

### CLI Tools
- `jgtcli` - Price/indicator data operations
- `cdscli` - Signal generation
- `jgtads` - Advanced charting
- `jgtservice` - Daemon mode

## Specification Version

- **Version**: 1.0
- **Framework**: RISE
- **Created**: 2026-01-31
