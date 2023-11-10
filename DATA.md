Here are the CDS column definitions in a Markdown table:

# JGTCDS Documentation


----

Here is the documentation for jgtconstants.py in Markdown format:

# Documentation for jgtconstants.py

This file contains constants and mappings used for technical analysis signals and indicators.

## Zone Color Constants

The following constants define colors for different market zones:

`nonTradingZoneColor = 'gray'`
`sellingZoneColor = 'red'` 
`buyingZoneColor = 'green'`

These map to the labeling of zones as non-trading, selling, or buying respectively.

## Alligator Indicator Mappings

Multiple variables map the Alligator indicator periods to column names:

`indicator_currentDegree_alligator_jaw_column_name = 'jaw'` 
`indicator_currentDegree_alligator_teeth_column_name = 'teeth'`
`indicator_currentDegree_alligator_lips_column_name = 'lips'`

`indicator_sixDegreeLarger_alligator_jaw_column_name = 'bjaw'`
`indicator_sixDegreeLarger_alligator_teeth_column_name = 'bteeth'` 
`indicator_sixDegreeLarger_alligator_lips_column_name = 'blips'`

This defines the Alligator Jaw, Teeth, Lips and potential buy signals.

## Additional Indicator Mappings

Several more indicators are mapped to column names, including:

- Awesome Oscillator (`ao`)
- AO Above/Bellow ZL (`aoaz`,`aobz`)
- Acceleration/Deceleration (`ac`)
- Gator Oscillator high/low (`gh`,`gl`)  
- Market Facilitation Index (`mfi`)
- Fractals of varying periods (`fh`,`fl` etc)

## Signal Column Mappings

Key signals are mapped to column names for identification:

- Fractal Divergence (`fdb`,`fdbs`,`fdbb`)
- AC signals (`acs`,`acb`)  
- Zone signals (`sz`,`bz`)
- Zero line signals (`zlcb`,`zlcs`)

This provides a dictionary to interpret signals in the data.






Below is a markdown table with 3 columns defining the requested columns:

| Column Name | Definition | Source | Status |
|-|-|-| - |
| fdbb, fdb, fdbs | Fractal Divergent Bar signal | JGTConstants.py | |
| aof | AO Fractal Peak indicator | JGTConstants.py | Incompleted:: detecting twin peaks |
| aoaz, aobz | AO indicator (above/below zero) | JGTConstants.py | Not a signal.  a ref |
| zlc, zlcb, zlcs, zcol | Zero Line Crossing signal | JGTConstants.py | |
| sz, bz | Buying/Selling zone signal | JGTConstants.py | |
| acs, acb | AC acceleration/deceleration signal | JGTConstants.py | |
| ss, sb | Saucer signal | JGTConstants.py | |

The columns are added to the DataFrame by functions like ids_add_indicators() and cds_add_signals_to_indicators() defined in JGTCDS.py.











----

## CDS Column Definitions

| Column | Description |
|-|-|
| Date | Date/time of bar | 
| Volume | Trading volume |
| Open | Opening price |
| High | Highest price |
| Low | Lowest price |  
| Close | Closing price |
| Median | Median price |
| ac | Accelerator oscillator |
| jaw | Alligator jaws value |
| teeth | Alligator teeth value |
| lips | Alligator lips value |
| bjaw | Big alligator jaws value |
| bteeth | Big alligator teeth value |
| blips | Big alligator lips value |
| ao | Awesome oscillator |
| fb | Fractals high value |
| fs | Fractals low value |
| fb3 | Fractals 3 period high value |  
| fs3 | Fractals 3 period low value |
| fb5 | Fractals 5 period high value |
| fs5 | Fractals 5 period low value |
| fb8 | Fractals 8 period high value |
| fs8 | Fractals 8 period low value |
| fb13 | Fractals 13 period high value |
| fs13 | Fractals 13 period low value |
| fb21 | Fractals 21 period high value |
| fs21 | Fractals 21 period low value |
| fb34 | Fractals 34 period high value |
| fs34 | Fractals 34 period low value |
| fb55 | Fractals 55 period high value |
| fs55 | Fractals 55 period high value |
| fb89 | Fractals 89 period high value |
| fs89 | Fractals 89 period low value |
| fdbbhigh | FDB Bullish high value |
| fdbblow | FDB Bullish low value |
| fdbb | Bool for FDB Bullish |
| fdb | Integer flag for FDB signal |
| fdbshigh | FDB Bearish high value |  
| fdbslow | FDB Bearish low value |
| fdbs | Bool for FDB Bearish |
| aof | AO Fractal peak value |
| aofvalue | AO value at Fractal peak |
| aofhighao | AO high value at Bull Fractal peak |
| aoflowao | AO low value at Bear Fractal peak |  
| aofhigh | Price high at Bull Fractal peak |
| aoflow | Price low at Bear Fractal peak |
| aoaz | AO signal color: Blue/Red | 
| aobz | AO signal color: Blue/Red |
| zlc | Zero Line Cross signal |
| zlcb | Zero Line Cross buy signal |
| zlcs | Zero Line Cross sell signal |
| aocolor | AO color: Blue/Red |
| accolor | Accelerator color: Blue/Red |
| zcol | Zero Line color: Blue/Red |
| sz | Signal strength value |
| bz | Buy strength value |
| acs | Accelerator sell signal | 
| acb | Accelerator buy signal |
| ss | Overall sell signal strength |
| sb | Overall buy signal strength |

Let me know if any clarification or expansion is needed for the column definitions.