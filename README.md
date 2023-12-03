

# jgtpy (ids)

Enhanced JGTPy CDS, IDS, PDS Services


## Installation
```sh
pip install -U jgtpy
```

## Example

```py

    >>> import pandas as pd
    >>> import jgtpy
    >>> df=jgtpy.getPH('EUR/USD','H4')
    >>>
    >>> # retrieve 3000 periods and generate from the DF
    >>> df=jgtpy.getPH('EUR/USD','H4',3000,with_index=False)
    >>> dfi=jgtpy.createFromDF(df)
    >>>
    >>> # Create with Timerange
    >>> start="11.17.2022 00:00:00"
    >>> end="11.25.2022 00:00:00"
    >>> df=jgtpy.createByRange("USD/CAD","m15",start,end)
    >>>
    >>> # offsets date for retreival
    >>> dtfirst_with_offset=jgtetl.svc_offset_dt_by_tf(dtfirst,ctx.timeframe)
    >>> df=createByRange(ctx.instrument,ctx.timeframe,dtfirst_with_offset,dtlast)

```

## More

* [DATA](DATA.md)
