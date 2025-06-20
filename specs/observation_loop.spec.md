# Observation Loop Specification

This document outlines the recurring workflow used by CLI agents and voice
interfaces to evaluate ADS charts and trading states.

## Overview
1. **Data Refresh** – Every few minutes a CLI agent pulls the latest CDS data and
   runs analysis modules such as `alligator_mouth_water`.
2. **Chart Generation** – The enriched dataset is plotted using `JGTADS` and
   overlay modules. Figures may be saved or sent to a display service.
3. **Voice Inspection Window** – A companion voice agent opens a short
   observation window (about 90 seconds). It reads current states from the plot
   or the data and describes key movements in natural language.
4. **Trigger Evaluation** – Spoken or textual descriptions are mapped back to
   programmatic rules. If conditions are met, the CLI agent issues trading
   actions or alerts.

## Data Contract
The loop expects the full CDS data columns, including the mouth and water state
fields described in `alligator_mouth_water.spec.md`.

## Extensibility
Future agents may adjust the refresh rate, include additional indicators or use
longer historical lookback windows to refine predictions.  Specifications should
remain modular so that each analysis or plotting step can be replaced without
breaking the loop.
