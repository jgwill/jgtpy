
>default args (mimic of jgtcli)
```

Namespace(instrument=None, timeframe=None, datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=0, ads=False, full=False, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
```
----



```python
instance.__dict__.update(JGTIDSRequest.from_args(args).__dict__)

```
* Does that actually update the current class dictionary with the instance from the super ?

>pds
```

Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}
#chg args type:list[str]
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}
...Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}

jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}

_dependent_arguments_rules::namespace
jgtcommon::namespace: nsjgtcommonargs
jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}

#chg args to argparse. Namespace
jgtcommon::namespace: nsjgtcommonargs
jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}
jgtcommon::namespace: nsjgtcommonargs
jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}

#chg: etattr(args, 'quiet', True)
jgtcommon::namespace: nsjgtcommonargs
jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}
# fixjgtcommon::namespace: nsjgtcommonargs
jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}
jgtcommon::namespace: nsjgtcommonargs
jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False}
JGTBaseRequest.from_args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
baserq= <JGTBaseRequest.JGTBaseRequest object at 0x76f23ae9ff10>

jgtcommon::namespace: nsjgtcommonargs
jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False, quiet=False)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 1, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False, 'quiet': False}
JGTBaseRequest.from_args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=1, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False, quiet=False)
baserq= <JGTBaseRequest.JGTBaseRequest object at 0x730d8f5a3f40>
{
  "quiet": false,
  "verbose_level": 1,
  "viewpath": false
}
jgtcommon::namespace: nsjgtcommonargs
jgtcommon::args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=0, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False)
Quiet mode activated in parser
Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=0, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False, quiet=True)
{'instrument': 'SPX500', 'timeframe': 'D1', 'datefrom': None, 'dateto': None, 'tlidrange': None, 'quotescount': -1, 'verbose': 0, 'ads': False, 'full': True, 'notfull': False, 'fresh': False, 'notfresh': False, 'mfi_flag': False, 'no_mfi_flag': False, 'gator_oscillator_flag': False, 'balligator_flag': False, 'balligator_period_jaws': 89, 'talligator_flag': False, 'talligator_period_jaws': 377, 'largest_fractal_period': 89, 'viewpath': False, 'dropna_volume': False, 'dont_dropna_volume': False, 'quiet': True}
JGTBaseRequest.from_args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=0, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False, quiet=True)
baserq= <JGTBaseRequest.JGTBaseRequest object at 0x75365ce9ff40>
{
  "quiet": true,
  "verbose_level": 0,
  "viewpath": false
}
JGTBaseRequest.from_args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=0, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False, quiet=True)
{
  "quiet": true,
  "verbose_level": 0,
  "viewpath": false
}
JGTBaseRequest.from_args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=False, dropna_volume=False, dont_dropna_volume=False, quiet=False)
{
  "quiet": false,
  "verbose_level": 2,
  "viewpath": false
}
JGTBaseRequest.from_args: Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=False, dont_dropna_volume=False, quiet=False)
{
  "quiet": false,
  "verbose_level": 2,
  "viewpath": true
}
# Clean JGTBaseRequest using  quiet=args.quiet,
{
  "quiet": false,
  "verbose_level": 2,
  "viewpath": true
}
{
  "quiet": true,
  "verbose_level": 0,
  "viewpath": true
}
```

----
# JGTPDSRequest

```
> The base request is creating the instance from_args then the __dict__ of JGTPDSRequest are updated from what seems a temp instance of it : 
instance=JGTBaseRequest.from_args(args)
instance.__dict__.update(JGTPDSRequest.from_args(args).__dict__)
>>>

# LOOPING ISsue

        tmp_instance=JGTPDSRequest.from_args(args)
        instance.__dict__.update(tmp_instance.__dict__)
INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False)
INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False)

>__timeframes_post_parseINFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, timeframes=None)

INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, timeframes=None, crop_last_dt=None)

INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, keepbidask=False, keep_bid_ask=False, rmbidask=True, timeframes=None, crop_last_dt=None)
-self.crop_last_dt is not None-
{
  "crop_last_dt": "None",
  "dropna_volume": true,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "quiet": true,
  "quotescount": -1,
  "timeframe": "D1",
  "timeframes": [
    "M1",
    "W1",
    "D1",
    "H8",
    "H4"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 0,
  "viewpath": false
}

INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, keepbidask=False, keep_bid_ask=False, rmbidask=True, timeframes=None, crop_last_dt=None)
{
  "crop_last_dt": null,
  "dropna_volume": true,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "quiet": true,
  "quotescount": -1,
  "timeframe": "D1",
  "timeframes": [
    "M1",
    "W1",
    "D1",
    "H8",
    "H4"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 0,
  "viewpath": false
}

expect TFs empty:

INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, keepbidask=False, keep_bid_ask=False, rmbidask=True, timeframes=None, crop_last_dt=None)
{
  "crop_last_dt": null,
  "dropna_volume": true,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "quiet": true,
  "quotescount": -1,
  "timeframe": "D1",
  "timeframes": [
    "M1",
    "W1",
    "D1",
    "H8",
    "H4"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 0,
  "viewpath": false
}
#fixed typo
INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, keepbidask=False, keep_bid_ask=False, rmbidask=True, timeframes=None, crop_last_dt=None)
{
  "crop_last_dt": null,
  "dropna_volume": true,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "quiet": true,
  "quotescount": -1,
  "timeframe": "D1",
  "timeframes": [
    "M1",
    "W1",
    "D1",
    "H8",
    "H4"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 0,
  "viewpath": false
}
INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, keepbidask=False, keep_bid_ask=False, rmbidask=True, timeframes=None, crop_last_dt=None)
{
  "crop_last_dt": null,
  "dropna_volume": true,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "quiet": true,
  "quotescount": -1,
  "timeframe": "D1",
  "timeframes": null,
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 0,
  "viewpath": false
}
INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1,H4', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, keepbidask=False, keep_bid_ask=False, rmbidask=True, timeframes=None, crop_last_dt=None)
{
  "crop_last_dt": null,
  "dropna_volume": true,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "quiet": true,
  "quotescount": -1,
  "timeframe": "D1,H4",
  "timeframes": null,
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 0,
  "viewpath": false
}
INFO(JGTPDSRequest): from_args Namespace(instrument='SPX500', timeframe='D1,H4', datefrom=None, dateto=None, tlidrange=None, quotescount=-1, verbose=2, ads=False, full=True, notfull=False, fresh=False, notfresh=False, mfi_flag=False, no_mfi_flag=False, gator_oscillator_flag=False, balligator_flag=False, balligator_period_jaws=89, talligator_flag=False, talligator_period_jaws=377, largest_fractal_period=89, viewpath=True, dropna_volume=True, dont_dropna_volume=False, quiet=False, keepbidask=False, keep_bid_ask=False, rmbidask=True, timeframes=None, crop_last_dt=None)
{
  "crop_last_dt": null,
  "dropna_volume": true,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "quiet": true,
  "quotescount": -1,
  "timeframe": "D1,H4",
  "timeframes": [
    "D1",
    "H4"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 0,
  "viewpath": false
}

```
# JGTIDSRequests


```

{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": false,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": true,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "",
  "keep_bid_ask": true,
  "largest_fractal_period": 89,
  "mfi_flag": true,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": true,
  "quotescount": 300,
  "rounding_decimal_min": 11,
  "talligator_flag": false,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "",
  "timeframes": [
    ""
  ],
  "use_fresh": false,
  "use_full": false,
  "verbose_level": 0,
  "viewpath": false
}
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": false,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": true,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "largest_fractal_period": 89,
  "mfi_flag": false,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": -1,
  "rounding_decimal_min": 11,
  "talligator_flag": false,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "D1,H4",
  "timeframes": [
    "D1",
    "H4"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 2,
  "viewpath": true
}
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": true,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": true,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "SPX500",
  "keep_bid_ask": false,
  "largest_fractal_period": 89,
  "mfi_flag": true,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": -1,
  "rounding_decimal_min": 11,
  "talligator_flag": true,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "D1,H4",
  "timeframes": [
    "D1",
    "H4"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 2,
  "viewpath": true
}

We dont do talligator for W1
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": true,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": true,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "SPX500",
  "keep_bid_ask": true,
  "largest_fractal_period": 89,
  "mfi_flag": true,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": -1,
  "rounding_decimal_min": 11,
  "talligator_flag": true,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "W1",
  "timeframes": [
    "W1"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 2,
  "viewpath": true
}
We dont do talligator for W1
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": true,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": true,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "SPX500",
  "keep_bid_ask": true,
  "largest_fractal_period": 89,
  "mfi_flag": true,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": -1,
  "rounding_decimal_min": 11,
  "talligator_flag": false,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "W1",
  "timeframes": [
    "W1"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 2,
  "viewpath": true
}
We dont drop for M1
We dont do balligator for M1
We dont do talligator for M1
We dont do MFI for M1
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": false,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": false,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "SPX500",
  "keep_bid_ask": true,
  "largest_fractal_period": 89,
  "mfi_flag": false,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": -1,
  "rounding_decimal_min": 11,
  "talligator_flag": false,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "M1",
  "timeframes": [
    "M1"
  ],
  "use_fresh": false,
  "use_full": true,
  "verbose_level": 2,
  "viewpath": true
}
We dont dropna volume for M1
We dont do balligator for M1
We dont do talligator for M1
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": false,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": false,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "SPX500",
  "keep_bid_ask": true,
  "largest_fractal_period": 89,
  "mfi_flag": true,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": -1,
  "rounding_decimal_min": 11,
  "talligator_flag": false,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "M1",
  "timeframes": [
    "M1"
  ],
  "use_fresh": true,
  "use_full": true,
  "verbose_level": 2,
  "viewpath": true
}
We dont dropna volume for M1
We dont do balligator for M1
We dont do talligator for M1
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": false,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": false,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "SPX500",
  "keep_bid_ask": true,
  "largest_fractal_period": 89,
  "mfi_flag": true,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": -1,
  "rounding_decimal_min": 11,
  "talligator_flag": false,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "M1",
  "timeframes": [
    "M1"
  ],
  "use_fresh": true,
  "use_full": false,
  "verbose_level": 2,
  "viewpath": true
}
We dont dropna volume for M1
We dont do balligator for M1
We dont do talligator for M1
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": false,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": false,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "SPX500",
  "keep_bid_ask": true,
  "largest_fractal_period": 89,
  "mfi_flag": true,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": 400,
  "rounding_decimal_min": 11,
  "talligator_flag": false,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "M1",
  "timeframes": [
    "M1"
  ],
  "use_fresh": true,
  "use_full": false,
  "verbose_level": 2,
  "viewpath": true
}
We dont dropna volume for M1
We dont do balligator for M1
We dont do talligator for M1
{
  "addAlligatorOffsetInFutur": false,
  "aof_flag": false,
  "balligator_flag": false,
  "balligator_period_jaws": 89,
  "balligator_period_lips": 34,
  "balligator_period_teeth": 55,
  "balligator_shift_jaws": 55,
  "balligator_shift_lips": 21,
  "balligator_shift_teeth": 34,
  "crop_last_dt": null,
  "disable_ao_peaks_v1": true,
  "dropna_volume": false,
  "gator_oscillator_flag": false,
  "include_ac_color": false,
  "include_ao_color": false,
  "instrument": "EUR/USD",
  "keep_bid_ask": true,
  "largest_fractal_period": 89,
  "mfi_flag": true,
  "peak_distance": 13,
  "peak_divider_min_height": 3,
  "peak_width": 8,
  "quiet": false,
  "quotescount": 400,
  "rounding_decimal_min": 11,
  "talligator_flag": false,
  "talligator_period_jaws": 377,
  "talligator_period_lips": 144,
  "talligator_period_teeth": 233,
  "talligator_shift_jaws": 233,
  "talligator_shift_lips": 89,
  "talligator_shift_teeth": 144,
  "timeframe": "M1",
  "timeframes": [
    "M1"
  ],
  "use_fresh": true,
  "use_full": false,
  "verbose_level": 2,
  "viewpath": true
}
