#!/usr/bin/env python
"""Convert a Price Data Service file to a Chaos Data Service file.

Exposes the ``pds2cds`` entry point. Run ``pds2cds --help`` for
command options.

@STCGoal pds2cds is the ONLY genuinely offline CDS producer (no broker call),
so it is what a deep-history rebuild has to use.  Its output must therefore be
indistinguishable in *shape* from what ``cdscli``/``jgtcli`` write, because the
same files are served by the chart/HTF endpoint.

Two things used to make that false, both because ``convert_pds_2_cds`` built a
default ``JGTCDSRequest()`` and never told it which timeframe it was looking at:

1. ``mouth_water_flag`` stayed False, so the six mouth-water columns
   (``mouth_direction``, ``mouth_phase``, ``bar_position``, ``water_state``,
   ``mouth_direction_confidence``, ``mouth_phase_confidence``) were absent from
   every file this tool produced -- while the endpoint serves them.
2. The per-timeframe alligator policy that ``jgtutils.jgtcommon`` applies at the
   argparse layer (``__balligator_flag__post_parse`` /
   ``__talligator_flag__post_parse``: no talligator on W1 or M1, no balligator
   on M1) never ran, because pds2cds takes a *file*, not ``-i/-t``.  The tide
   alligator needs 377+233 warmup bars and ``dropna()`` deletes them, so leaving
   it enabled on W1 silently cost 610 weekly bars -- about twelve years -- and
   leaving the big alligator enabled on M1 cost 144 monthly bars.

Both are fixed by deriving instrument/timeframe from the filename (or from
``-i``/``-t``) and building the request through the same policy the CLIs use.
"""

import sys
import os



sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# import .

from jgtutils import (
    jgtconstants as constants,
    jgtcommon as jgtcommon,
)

import JGTCDS as cds
import JGTCDSSvc as svc
from JGTCDSRequest import JGTCDSRequest

import pandas as pd

epilog = """
Proto usage:JGTPY_DATA=/tmp/fds;

jgtfxcli -i EUR/USD -t m5 -c 12000;

tlid_v=2409022200;python jgtpy/pds2cds.py -f /tmp/fds/pds/EUR-USD_m5 -c 500 -to $tlid_v -o /tmp/fds/pds/EUR-USD_m5.$tlid_v.cds.csv;
wc -l /tmp/fds/pds/EUR-USD_m5.$tlid_v.cds.csv;
tail -n 1 /tmp/fds/pds/EUR-USD_m5.$tlid_v.cds.csv
"""

#: Timeframes that jgtutils.jgtcommon knows about, longest first.
_KNOWN_TIMEFRAMES = ["M1", "W1", "D1", "H8", "H4", "H3", "H2", "H1", "m30", "m15", "m5", "m1"]


def _default_cds_required_bars():
  """Bars that ``dropna()`` will eat off the head of a full-featured CDS.

  It is the tide alligator's warmup -- ``talligator_period_jaws +
  talligator_shift_jaws`` = 377 + 233 = **610** -- and it is a *max*, not a sum,
  because every other indicator's warmup is shorter.  ``tjaw.first_valid_index()``
  measures 610 on real data and ``dropna()`` removes exactly 610 rows.

  The historical literal here was ``609``: 610 misread as a 0-based index.  The
  consequence was small but real -- ``pds2cds -c N`` returned N-1 rows instead
  of N.  Deriving it from the request keeps one source of truth with
  ``JGTIDSRequest._get_talligator_required_additional_quotescount``.
  """
  return JGTCDSRequest()._get_talligator_required_additional_quotescount()


def infer_instrument_timeframe_from_filename(pdsfile):
  """``.../pds/USD-CAD_W1.csv`` -> ``("USD/CAD", "W1")``.

  Returns ``(None, None)`` when the name does not follow the convention; callers
  must tolerate that rather than guess, because guessing the timeframe wrong
  changes which indicators are computed.
  """
  base = os.path.basename(pdsfile)
  for ext in (".cds.csv", ".csv"):
    if base.endswith(ext):
      base = base[: -len(ext)]
      break
  if "_" not in base:
    return None, None
  instrument_part, _, timeframe_part = base.rpartition("_")
  if timeframe_part not in _KNOWN_TIMEFRAMES:
    return None, None
  instrument = instrument_part.replace("-", "/") if "-" in instrument_part else instrument_part
  return instrument, timeframe_part


def apply_timeframe_indicator_policy(rq):
  """The same per-timeframe policy ``jgtcommon`` applies to every CDS CLI.

  Mirrors ``jgtutils.jgtcommon.__balligator_flag__post_parse`` and
  ``__talligator_flag__post_parse``.  Kept here as well as there because
  pds2cds can be called as a library, with no argparse in sight.
  """
  timeframe = getattr(rq, "timeframe", None)
  if timeframe == "M1":
    rq.balligator_flag = False
    rq.talligator_flag = False
  elif timeframe == "W1":
    rq.talligator_flag = False
  return rq


def build_cds_request(instrument=None, timeframe=None, mouth_water_flag=None,
                      balligator_flag=None, talligator_flag=None, mfi_flag=None):
  """Build the request pds2cds converts with.

  Defaults come from the user's settings exactly as they do for ``cdscli``
  (``load_arg_default_from_settings``), then the per-timeframe policy is
  applied.  The fallbacks when no setting exists are the ones
  ``JGTIDSRequest.__init__`` already used, plus ``mouth_water_flag=True`` -- so
  this tool can only ever emit *more* columns than it used to, never fewer.
  """
  def _from_settings(name, fallback):
    try:
      return jgtcommon.load_arg_default_from_settings(name, fallback)
    except Exception:
      return fallback

  rq = JGTCDSRequest()
  rq.instrument = instrument
  rq.timeframe = timeframe
  rq.balligator_flag = _from_settings("balligator_flag", True) if balligator_flag is None else balligator_flag
  rq.talligator_flag = _from_settings("talligator_flag", True) if talligator_flag is None else talligator_flag
  rq.mfi_flag = _from_settings("mfi_flag", True) if mfi_flag is None else mfi_flag
  rq.mouth_water_flag = _from_settings("mouth_water_flag", True) if mouth_water_flag is None else mouth_water_flag
  return apply_timeframe_indicator_policy(rq)


def _parse_args():
  parser=jgtcommon.new_parser("PDS File 2 CDS File",epilog,"pds2cds",add_exiting_quietly_flag=True)
  jgtcommon.add_input_file_argument(parser,add_f_alias=True)
  jgtcommon.add_output_argument(parser)
  jgtcommon.add_bars_amount_V2_arguments(parser)
  jgtcommon.add_tlid_date_to_argumments(parser)
  jgtcommon.add_instrument_standalone_argument(parser,load_from_settings=False,required=False)
  jgtcommon.add_timeframe_standalone_argument(parser,load_from_settings=False,required=False)
  jgtcommon.add_ids_mouth_water_argument(parser)
  args=jgtcommon.parse_args(parser)
  return args

def convert_pds_2_cds(pdsfile,cdsfile_out=None,quotescount=-1,tlid_dateto=None,
                      usual_cds_required_bars = None,
                      instrument=None,timeframe=None,rq=None,quiet=True):

  if not os.path.exists(pdsfile):
    #add .csv to support without extension
    pdsfile=pdsfile+".csv"
  if not os.path.exists(pdsfile):
    print("Error: File not found: "+pdsfile)
    from jgtutils.jgterrorcodes import JGTFILES_EXIT_ERROR_CODE
    exit(JGTFILES_EXIT_ERROR_CODE)

  inferred_instrument, inferred_timeframe = infer_instrument_timeframe_from_filename(pdsfile)
  instrument = instrument or inferred_instrument
  timeframe = timeframe or inferred_timeframe

  if rq is None:
    rq = build_cds_request(instrument=instrument, timeframe=timeframe)
  else:
    if instrument and not getattr(rq, "instrument", None):
      rq.instrument = instrument
    if timeframe and not getattr(rq, "timeframe", None):
      rq.timeframe = timeframe
    rq = apply_timeframe_indicator_policy(rq)

  if usual_cds_required_bars is None:
    usual_cds_required_bars = _default_cds_required_bars()

  df=pd.read_csv(pdsfile,index_col=0,parse_dates=True)
  if tlid_dateto:
    df=df.loc[:tlid_dateto]
  if quotescount>0:
    df=df.tail(quotescount+usual_cds_required_bars)
  cdsfile=cdsfile_out if cdsfile_out else pdsfile.replace(".csv",".cds.csv")
  cdf=cds.createFromDF(df, quiet=quiet, rq=rq)
  if cdf is None or len(cdf) == 0:
    raise ValueError(
        "pds2cds produced an empty CDS from %s (%d input bars). Refusing to write."
        % (pdsfile, len(df)))
  cdf.to_csv(cdsfile)
  if not quiet:
    print("INFO::CDS written: %s  rows=%d  columns=%d  timeframe=%s"
          % (cdsfile, len(cdf), len(cdf.columns), timeframe))
  return cdsfile

def main():
  args=_parse_args()
  mouth_water_flag = getattr(args, "mouth_water_flag", None)
  instrument = getattr(args, "instrument", None)
  timeframe = getattr(args, "timeframe", None)
  inferred_instrument, inferred_timeframe = infer_instrument_timeframe_from_filename(args.input_file)
  instrument = instrument or inferred_instrument
  timeframe = timeframe or inferred_timeframe
  rq = build_cds_request(instrument=instrument, timeframe=timeframe,
                         mouth_water_flag=mouth_water_flag)
  convert_pds_2_cds(args.input_file,args.output,args.quotescount,args.tlid_dateto,
                    instrument=instrument,timeframe=timeframe,rq=rq,
                    quiet=getattr(args,"quiet",True))
  # Return nothing. The `pds2cds` console script is `sys.exit(main())`, so
  # returning the output path would exit with a *string* -- which CPython prints
  # to stderr and turns into exit status 1 on every successful run.  Failures
  # here are exceptions or an explicit exit(), never a return value.
  return None

if __name__ == "__main__":
  main()

