import os
import datetime

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon


def create_filestore_path(
    instrument, timeframe, quiet=True, compressed=False, tlid_range=None,output_path=None
):
    # Define the file path based on the environment variable or local path
    if output_path is None:
        data_path = get_data_path()
    else: # get path from var in os
        data_path = output_path
        
    if not quiet:
        print(data_path)

    ext = "csv"
    if compressed:
        ext = "csv.gz"

    fpath = mk_fullpath(instrument, timeframe, ext, data_path, tlid_range=tlid_range)

    if os.name == "nt":
        fpath = fpath.replace("/", "\\")
    return fpath


def mk_fn(instrument, timeframe, ext="csv"):
    """Make a file name with instrument and timeframe

    Args:
        instrument (str): symbol
        timeframe (str): TF
        ext (str): ext name "csv"

    Returns:
        str: file name
    """
    _tf = timeframe
    _i = instrument.replace("/", "-")
    if timeframe == "m1":
        _tf = timeframe.replace("m1", "mi1")
    _fn = _i + "_" + _tf + "." + ext
    return _fn.replace("..", ".")


def mk_fn_range(instrument, timeframe, start: datetime, end: datetime, ext="csv"):
    _tf = timeframe
    _i = instrument.replace("/", "-")
    if timeframe == "m1":
        _tf = timeframe.replace("m1", "mi1")
    start_str = jgtcommon.tlid_dt_to_string(start)
    end_str = jgtcommon.tlid_dt_to_string(end)
    _fn = f"{_i}_{_tf}_{start_str}_{end_str}.{ext}"
    # _fn= _i + '_' + _tf + '.' + ext
    _fn = _fn.replace("..", ".")
    _fn = _fn.replace("/", "-")
    return _fn


def mk_fullpath(instrument, timeframe, ext, path, tlid_range=None):
    if tlid_range is None:
        fn = mk_fn(instrument, timeframe, ext)
    else:
        start_dt, end_dt = jgtcommon.tlid_range_to_start_end_datetime(
            tlid_range=tlid_range
        )
        # print(str(start_dt),str(end_dt))
        fn = mk_fn_range(instrument, timeframe, start_dt, end_dt, ext)
    rpath = os.path.join(path, fn)
    if os.name == "nt":
        rpath = rpath.replace("/", "\\")
    # path + '/'+fn
    return rpath


# .replace('..','.').replace('//','/')


def get_data_path():
    default_dot = "./data"
    default_dotdot = "../data"
    data_path = os.environ.get("JGTPY_DATA", default_dot)

    if not os.path.exists(data_path):
        data_path = os.environ.get("JGTPY_DATA", default_dotdot)

    if os.name == "nt":
        data_path = data_path.replace("/", "\\")

    if not os.path.exists(data_path):
        raise Exception(
            "Data directory not found. Please create a directory named 'data' in the current or parent directory, or set the JGTPY_DATA environment variable."
        )

    data_path = os.path.join(data_path, "pds")
    return data_path
