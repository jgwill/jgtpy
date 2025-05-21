# %%

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCDSRequest import JGTCDSRequest

# import jgtfxcon.JGTPDS as pds
import JGTIDS as ids
import JGTPDSP as pds
from jgtutils.jgtos import get_data_path,mk_fullpath
from jgtutils import jgtos as jos
from JGTChartConfig import JGTChartConfig

# from . import jgtconstants
# .columns_to_remove as columns_to_remove

import pandas as pd


from jgtutils import jgtconstants as c
from jgtutils.coltypehelper import DTYPE_DEFINITIONS

from jgtutils.jgtconstants import NB_BARS_BY_DEFAULT_IN_CDS

#DTYPE_COLTYPE = coltypehelper.get_dtype_definitions()

# %%
def createFromPDSFileToCDSFile(
    instrument,
    timeframe,
    columns_to_remove=None,
    quiet=True,
    tlid_range=None,
    use_full=False,
    rq:JGTCDSRequest=None,
    use_fresh=True,
    keep_bid_ask=True,
    gator_oscillator_flag=False,
    mfi_flag=True,
    balligator_flag=False,
    balligator_period_jaws=89,
    largest_fractal_period=89,
    talligator_flag=False,
    talligator_period_jaws=377,
    viewpath=False,
    quotescount=NB_BARS_BY_DEFAULT_IN_CDS,
    dropna_volume=True,
):
    """
    Create a CDS file from a PDS file.

    Parameters:
    instrument (str): The instrument name.
    timeframe (str): The timeframe of the data.
    columns_to_remove (list, optional): List of column names to remove from the CDS file. Default is None.
    quiet (bool, optional): If True, suppresses the output. Default is True.
    tlid_range (str, optional): The TLID range to retrieve. Default is None.
    use_full (bool, optional): If True, reads/writes the full CDS file. Default is False.
    rq (JGTCDSRequest, optional): The JGTCDSRequest object to use for the processing. Defaults to None.
    use_fresh (bool, optional): If True, retrieves and reads fresh data. Default is False.
    keep_bid_ask (bool, optional): If True, keeps the bid and ask columns in the CDS file. Default is True.
    gator_oscillator_flag (bool, optional): If True, calculates the Gator Oscillator. Default is False.
    mfi_flag (bool, optional): If True, calculates the Money Flow Index. Default is False.
    balligator_flag (bool, optional): If True, calculates the Bill Williams Alligator. Default is False.
    balligator_period_jaws (int, optional): The period for the Bill Williams Alligator Jaws. Default is 89.
    largest_fractal_period (int, optional): The period for the largest fractal. Default is 89.
    talligator_flag (bool, optional): If True, calculates the Tide Alligator. Default is False.
    talligator_period_jaws (int, optional): The period for the Tide Alligator Jaws. Default is 377.
    viewpath (bool, optional): If True, displays the file path. Default is False.
    quotescount (int, optional): The number of quotes to keep. Default is 300.

    Returns:
    - fpath (str): The file path of the created CDS file.
    - c (DataFrame): The DataFrame containing the data.

    """
    if rq is None:
        #print("rq is None in createFromPDSFileToCDSFile")
        rq = JGTCDSRequest()
        rq.timeframe=timeframe
        rq.instrument=instrument
        rq.quotescount = quotescount
        rq.gator_oscillator_flag = gator_oscillator_flag
        rq.mfi_flag = mfi_flag
        rq.balligator_flag = balligator_flag
        rq.talligator_flag = talligator_flag
        rq.balligator_period_jaws = balligator_period_jaws
        rq.talligator_period_jaws = talligator_period_jaws
        rq.largest_fractal_period = largest_fractal_period
        rq.viewpath=viewpath
        rq.talligator_fix_quotescount()
    if rq.viewpath:
        cdspath = get_pov_local_data_filename(instrument,timeframe,use_full=use_full)
        print(cdspath)
        return cdspath,None
    # Working around an issue with keep_bid_ask, we use the value supplied in this function to override the value in the request
    rq.keep_bid_ask = keep_bid_ask
    rq.dropna_volume = dropna_volume

    cdf = createFromPDSFile(
        instrument, timeframe, quiet,         
        use_full=use_full, 
        rq=rq,
        columns_to_remove=columns_to_remove,
        use_fresh=use_fresh
    )


    # Define the file path based on the environment variable or local path
    fpath = writeCDS(instrument, timeframe, use_full, cdf)

    return fpath, cdf



def readCDSFile(
    instrument, timeframe, columns_to_remove=None, quiet=True, use_full=False,
    dt_crop_last=None,
    quote_count=None
):
    """
    Read a CDS file and return a pandas DataFrame.

    Parameters:
    instrument (str): The instrument name.
    timeframe (str): The timeframe of the data.
    columns_to_remove (list, optional): List of column names to remove from the DataFrame. Default is None.
    quiet (bool, optional): If True, suppresses the output messages. Default is True.
    use_full (bool, optional): If True, reads the full CDS file. Default is False.
    dt_crop_last (str, optional): The date to crop the data to. Default is None.
    quote_count (int, optional): The number of quotes to keep. Default is None.

    Returns:
    pandas.DataFrame: The DataFrame containing the CDS data.
    """
    # Define the file path based on the environment variable or local path
    data_path_cds = get_data_path("cds", use_full=use_full)
    fpath = pds.mk_fullpath(instrument, timeframe, "csv", data_path_cds)
    cdf = pd.read_csv(fpath,dtype=DTYPE_DEFINITIONS)

    # Set 'Date' as the index and convert it to datetime
    cdf["Date"] = pd.to_datetime(cdf["Date"])
    cdf.set_index("Date", inplace=True)
    # Remove the specified columns
    if columns_to_remove is not None:
        cdf = cdf.drop(columns=columns_to_remove, errors="ignore")
    
    if dt_crop_last is not None:
        cdf = cdf[cdf.index <= dt_crop_last]
    if quote_count is not None:
        cdf = cdf[-quote_count:]
    return cdf


def createFromPDSFile(
    instrument,
    timeframe,
    quiet=True,
    cc: JGTChartConfig = None,
    use_full=False, #@STCIssue USELESS Somehow here :NOPE it reads a different file
    rq:JGTCDSRequest=None,
    run_jgtfxcli_on_error=True,
    columns_to_remove=None,
    use_fresh=False

):
    """Create CDS (Chaos Data Service) with Fresh Data on the filestore

    Args:
        instrument (str): symbol
        timeframe (str): TF
        quiet (bool,optional): Output quiet
        cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.
        use_full (bool, optional): If True, reads the full CDS file. Default is False.
        rq (JGTCDSRequest, optional): The JGTCDSRequest object to use for the processing. Defaults to None. 
        run_jgtfxcli_on_error (bool, optional): If True, runs jgtfxcli on error. Default is True.
        columns_to_remove (list, optional): List of column names to remove from the DataFrame. Default is None.

    Returns:
        pandas.DataFrame: CDS DataFrame
    """
    try:
        df = _getPH_to_DF_wrapper_240304(instrument, timeframe, quiet, cc, use_full, rq=rq, run_jgtfxcli_on_error=run_jgtfxcli_on_error,
        columns_to_remove=columns_to_remove,
        use_fresh=use_fresh)
        #print("DEBUG H8 240325:: len getPH DF:",len(df))
        
        return df
    except Exception as e:
        print("Error in createFromPDSFile")
        print(e)
            
        return None

def __rq_patch(instrument,timeframe,rq):
    if rq is None:
        rq = JGTCDSRequest()
        rq.instrument=instrument
        rq.timeframe=timeframe
    return rq

def _getPH_to_DF_wrapper_240304(instrument, timeframe, quiet, cc, use_full, rq,use_fresh=False ,run_jgtfxcli_on_error=True,columns_to_remove=None):
    rq=__rq_patch(instrument,timeframe,rq)
    #print("_getPH_to_DF_wrapper_240304 rq.quotescount:",rq.quotescount)
    df=pds.getPH(instrument,
            timeframe,
            quote_count=rq.quotescount,
            quiet=quiet,
            use_full=use_full,
            use_fresh=use_fresh,
            run_jgtfxcli_on_error=run_jgtfxcli_on_error,
            keep_bid_ask=rq.keep_bid_ask,
            dropna_volume=rq.dropna_volume,
            )

    if not quiet:
        print(df)

    dfi = createFromDF(df, quiet=quiet, cc=cc,rq=rq,
                       columns_to_remove=columns_to_remove)
    return dfi

def createFromDF(df, quiet=True, 
                 cc: JGTChartConfig = None,
                 rq: JGTCDSRequest=None,
                 columns_to_remove=None
                 ):
    """
    Creates a new DataFrame with indicators, signals, and cleansed columns added based on the input DataFrame.

    Args:
      df (pandas.DataFrame): The input DataFrame to add indicators, signals, and cleansed columns to.
      quiet (bool, optional): Whether to suppress console output during processing. Defaults to True.
      cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.
      rq (JGTCDSRequest, optional): The JGTCDSRequest object to use for the processing. Defaults to None.
      columns_to_remove (list, optional): List of column names to remove from the DataFrame. Default is None.


    Returns:
      pandas.DataFrame: The new DataFrame with indicators, signals, and cleansed columns added.
    """
    if cc is None:
        cc = JGTChartConfig()
    if rq is None:
        rq = JGTCDSRequest()

    if df.index.name == "Date":
        df.reset_index(inplace=True)
    
    dfi = ids.tocds(df, quiet=quiet, cc=cc,rq=rq,columns_to_remove=columns_to_remove)
    
    return dfi

def create2(
    rq:JGTCDSRequest=None,  
    cc: JGTChartConfig = None,      
    quiet=True,
):
    return create(rq.instrument, rq.timeframe, quiet=quiet, cc=cc, rq=rq, use_full=rq.use_full, use_fresh=rq.use_fresh)

def create(
    instrument,
    timeframe,
    quiet=True,
    cc: JGTChartConfig = None,
    rq:JGTCDSRequest=None,
    use_full=False,
    use_fresh=False,
    columns_to_remove=None,    
):
    """Create CDS (Chaos Data Service) with Fresh Data

    Args:
        instrument (str): symbol
        timeframe (str): TF
        quiet (bool,optional): Output quiet
        cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.
        rq (JGTCDSRequest, optional): The JGTCDSRequest object to use for the processing. Defaults to None.
        use_full (bool, optional): If True, reads the full CDS file. Default is False.
        use_fresh (bool, optional): If True, tries to retrieves and reads fresh data. Default is False.
        

    Returns:
        pandas.DataFrame: CDS DataFrame
    """
    if not quiet:
        print("CDS create is being called")
    if cc is None:
        cc = JGTChartConfig()
    if rq is None:
        rq = JGTCDSRequest()
    
    dfi = _getPH_to_DF_wrapper_240304(instrument, timeframe, quiet, cc, use_full, rq,use_fresh=use_fresh,columns_to_remove=columns_to_remove)
    # df = pds.getPH(
    #     instrument, timeframe,quiet=quiet, cc=cc,
    #     use_full=use_full,
    #     run_jgtfxcli_on_error=True,
    #     use_fresh=use_fresh
    # )
    # dfi = createFromDF(df, quiet=quiet, cc=cc,rq=rq)
    return dfi


# createByRange
def createByRange(instrument:str, timeframe:str, start, end, stayConnected:bool=False, quiet:bool=True):
    """Create CDS with Fresh Data from a range

    Args:
        instrument (str): symbol
        timeframe (str): TF
        start (date): start date
        end (date): end date
        stayConnected (bool, optional): Leave FXCMPY connected. Defaults to False.
        quiet (bool,optional): Output quiet

    Returns:
        pandas.DataFrame: CDS DataFrame
    """
    pds.stayConnected = stayConnected
    df = pds.getPHByRange(
        instrument, timeframe, start, end, with_index=False, quiet=quiet
    )
    dfi = createFromDF(df, quiet=quiet)
    return dfi


columns_to_remove = [
    "aofvalue",
    "aofhighao",
    "aoflowao",
    "aofhigh",
    "aoflow",
    "aocolor",
    "accolor",
    "fdbbhigh",
    "fdbblow",
    "fdbshigh",
    "fdbslow",
]


def create_and_clean_data_from_file_df(instrument:str, timeframe:str):
    # Create DataFrame from PDS file
    cdf = createFromPDSFile(instrument, timeframe)

    # Remove specified columns if provided
    if columns_to_remove:
        cdf = cdf.drop(columns=columns_to_remove, errors="ignore")

    # Set 'Date' as the index
    cdf.set_index(c.DATE, inplace=True)

    return cdf


def _save_cds_data_to_file(df:pd.DataFrame, instrument:str, timeframe:str):
    # Define the file path based on the environment variable or local path
    data_path = get_data_path()
    fpath = pds.mk_fullpath(instrument, timeframe, "csv", data_path)

    # Save DataFrame to CSV
    df.to_csv(fpath)
    return fpath


def writeCDS(instrument, timeframe, use_full, cdf:pd.DataFrame):
    data_path_cds = get_data_path("cds", use_full=use_full)
    fpath = mk_fullpath(instrument, timeframe, "csv", data_path_cds)
    # print(fpath)
    cdf.to_csv(fpath, index=True)
    return fpath


def createFromFile_and_clean_and_save_data(instrument:str, timeframe:str):
    # Create DataFrame from PDS file
    cdf = create_and_clean_data_from_file_df(instrument, timeframe)
    _save_cds_data_to_file(cdf, instrument, timeframe)

    return cdf


def get_pov_local_data_filename(instrument:str,timeframe:str,use_full=False):
  nsdir="cds"
  return jos.get_pov_local_data_filename(instrument,timeframe,use_full=use_full,nsdir=nsdir)

def getSubscribed():
    return pds.getSubscribed()


def getActiveSymbols():
    AppSuiteConfigRootPath = os.getenv("AppSuiteConfigRootPath")
    fn = "activesymbol.txt"
    fpath = os.path.join(AppSuiteConfigRootPath, fn)
    with open(fpath) as f:
        first_line = f.readline()
        print(first_line)


# %%
def getLast(_df):
    return _df.iloc[-1]


def getPresentBar(_df):
    r = _df  # ['High','Low',indicator_AO_awesomeOscillator_column_name,signalCode_fractalDivergentBar_column_name,indicator_AC_accelerationDeceleration_column_name]
    return r.iloc[-1:]


def getPresentBarAsList(_df):
    _paf = _df.iloc[-1:]
    _pa = _paf.to_dict(orient="list")
    _dtctx = str(_paf.index.values[0])
    _pa["Date"] = _dtctx
    return _pa


def getLastCompletedBarAsList(_df):
    _paf = _df.iloc[-2:-1]
    _pa = _paf.to_dict(orient="list")
    _dtctx = str(_paf.index.values[0])
    _pa["Date"] = _dtctx
    return _pa


def checkFDB(_instrument:str, _timeframe:str):
    _df = create(_instrument)
    pa = getPresentBarAsList(_df)
    isfdb = pa[c.FDB][0] != 0.0
    fdb = pa[c.FDB]
    dtctx = pa[c.DATE]
    if isfdb:
        print(_instrument + "_" + _timeframe + " : We Have a Signal : " + dtctx)
        return True
    else:
        print(_instrument + "_" + _timeframe + " : No signal now : " + dtctx)
        return False


def print_quiet(quiet, content):
    if not quiet:
        print(content)
