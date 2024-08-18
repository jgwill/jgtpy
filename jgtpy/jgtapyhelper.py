import warnings

# Ignore FutureWarning
warnings.simplefilter(action="ignore", category=FutureWarning)

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from jgtapy import Indicators

import pandas as pd
import datetime


from JGTChartConfig import JGTChartConfig
from JGTIDSRequest import JGTIDSRequest


from jgtutils.jgtconstants import (
    IDS_COLUMNS_TO_NORMALIZE,
    JAW,
    BJAW,
    TEETH,
    BTEETH,
    LIPS,
    BLIPS,
    OPEN,
    HIGH,
    LOW,
    CLOSE,
    BAR_HEIGHT,
    FH,
    FH3,
    FH5,
    FL,
    FL3,
    FL5,
    FH8,
    FL8,
    AO,
    AC,
    FH13,
    FH21,
    FH34,
    FH55,
    FH89,
    FL13,
    FL21,
    FL34,
    FL55,
    FL89,
    GL,
    GH,
    MFI,
    VOLUME,
    TJAW,
    TTEETH,
    TLIPS,
    NB_BARS_BY_DEFAULT_IN_CDS,
)

from jgtutils import jgtos as jos

columns_to_normalize = IDS_COLUMNS_TO_NORMALIZE  # @a Migrate to jgtutils.jgtconstants

from jgtutils import (
    jgtconstants as constants,
    jgtcommon as jgtcommon,
    jgtwslhelper as wsl,
)


def ids_add_indicators(
    dfsrc,
    dropnavalue=True,
    quiet=True,
    cleanupOriginalColumn=True,
    useLEGACY=True,
    cc: JGTChartConfig = None,
    bypass_index_reset=False,
    rq: JGTIDSRequest = None,
):
    """
    Adds technical indicators to a given DataFrame.

    Args:
    dfsrc (pandas.DataFrame): The DataFrame to which the indicators will be added.
    dropnavalue (bool, optional): Whether to drop rows with NaN values. Defaults to True.
    quiet (bool, optional): Whether to suppress console output. Defaults to False.
    cleanupOriginalColumn (bool, optional): Whether to clean up the original column. Defaults to True.
    useLEGACY (bool, optional): Whether to use the legacy version of the function. Defaults to True.
    cc (JGTChartConfig, optional): The JGTChartConfig object. Defaults to None.
    bypass_index_reset (bool, optional): Whether to bypass resetting the index. Defaults to False.
    rq (JGTIDSRequest, optional): The JGTIDSRequest object. Defaults to None.

    Returns:
    pandas.DataFrame: The DataFrame with the added indicators.
    """

    if cc is None:
        cc = JGTChartConfig()
    if rq is None:
        rq = JGTIDSRequest()

    dfresult = None
    if (
        not useLEGACY
    ):  # Because jgtapy has to be upgraded with new column name, we wont use it until our next release
        print("## --- NOT SURE YOU WILL GET WHAT YOU WANT ----")
        dfresult = Indicators.jgt_create_ids_indicators_as_dataframe(
            dfsrc,
            rq.gator_oscillator_flag,
            rq.mfi_flag,
            cleanupOriginalColumn,
            quiet,
        )
    else:
        dfresult = ids_add_indicators__legacy(
            dfsrc=dfsrc,
            dropnavalue=dropnavalue,
            quiet=quiet,
            min_nb_bar_on_chart=cc.min_bar_on_chart,
            bypass_index_reset=bypass_index_reset,
            rq=rq,
        )

    #print("IDS::debug len(dfresult):" + str(len(dfresult)))
    #print(" dfresult.columns:", dfresult.columns)
    dfresult= round_columns(dfresult, rq.rounding_decimal_min)
    return dfresult


def round_columns(df, rounding_decimal_min=10):
    for col in df.columns:
        if df[col].dtype == "float64" and df[col].apply(lambda x: x % 1 != 0).any():
            df[col] = df[col].round(decimals=rounding_decimal_min)
            df[col] = df[col].apply(lambda x: 0 if "e" in str(x) else x)
    return df

def calculate_mfi_sq(row, prev_row):
    if pd.isna(row[VOLUME]):
        return '0'
    elif row[VOLUME] > prev_row[VOLUME] and row['MFI'] > prev_row['MFI']:
        return '++ Green'
    elif row[VOLUME] < prev_row[VOLUME] and row['MFI'] < prev_row['MFI']:
        return '-- Fade'
    elif row[VOLUME] < prev_row[VOLUME] and row['MFI'] > prev_row['MFI']:
        return '-+ Fake'
    elif row[VOLUME] > prev_row[VOLUME] and row['MFI'] < prev_row['MFI']:
        return '+- Squat'
    else:
        return '0'

def ids_add_indicators__legacy(
    dfsrc,
    dropnavalue=True,
    quiet=True,
    min_nb_bar_on_chart=NB_BARS_BY_DEFAULT_IN_CDS,
    bypass_index_reset=False,
    rq: JGTIDSRequest = None,
):
    """
    Adds various technical indicators to the input DataFrame. Is the same as in the jgtapy.legacy module.

    Args:
    dfsrc (pandas.DataFrame): The input DataFrame.
    dropnavalue (bool, optional): Whether to drop rows with NaN values. Defaults to True.
    quiet (bool, optional): Whether to suppress print statements. Defaults to False.
    min_nb_bar_on_chart (int, optional): The minimum number of bars on the chart. Defaults to NB_BARS_BY_DEFAULT.
    bypass_index_reset (bool, optional): Whether to bypass resetting the index. Defaults to False.
    rq (JGTIDSRequest, optional): The JGTIDSRequest object. Defaults to None.

    Returns:
    pandas.DataFrame: The input DataFrame with added technical indicators.
    """

    if rq is None:
        #print("rq is None is ids_add_indicators__legacy")
        rq = JGTIDSRequest()
    
    if rq.timeframe == "M1":
        #print("rq.timeframe is M1")
        rq.balligator_flag = False
        rq.talligator_flag = False
    
    # @a Migrating to the new JGTIDSRequest
    gator_oscillator_flag = rq.gator_oscillator_flag
    mfi_flag = rq.mfi_flag
    addAlligatorOffsetInFutur = rq.addAlligatorOffsetInFutur
    

    ldfsrc = len(dfsrc)
    # TODO
    df_nb_bars = min_nb_bar_on_chart  # @STCIssue: We have charts with as few as 80 bars and some indicators wont work. We need to find a way to make it work with less bars.
    df_nb_bars = (
        ldfsrc  # @a workaround for now - adequate limits is the amount of bars we have.
    )
    minimal_bars_with_indicators = 25
    FIX_TOO_SHORT_DATAFRAME__PROTO = False

    if FIX_TOO_SHORT_DATAFRAME__PROTO:
        dfsrc = fix_too_short_df(dfsrc)

    if not quiet:
        print("Adding indicators...")
    i = Indicators(dfsrc)
    # print("IDS::debug len(dfsrc)" + str(ldfsrc))

    try:
        i.ao_ac_oscillator(
            column_name_ao=AO,
            column_name_ac=AC,
        )
    except:
        print("ao_ac_oscillator failed")

    try:
        i.alligator(
            period_jaws=13,
            period_teeth=8,
            period_lips=5,
            shift_jaws=8,
            shift_teeth=5,
            shift_lips=3,
            column_name_jaws=JAW,
            column_name_teeth=TEETH,
            column_name_lips=LIPS,
        )
    except:
        print("alligator failed")
   

    bAlligator_required_bar_offset = (
        minimal_bars_with_indicators + rq.balligator_period_jaws + rq.balligator_shift_jaws
    )

    if ldfsrc >= bAlligator_required_bar_offset and rq.balligator_flag:

        try:
            i.alligator(
                period_jaws=rq.balligator_period_jaws,
                period_teeth=rq.balligator_period_teeth,
                period_lips=rq.balligator_period_lips,
                shift_jaws=rq.balligator_shift_jaws,
                shift_teeth=rq.balligator_shift_teeth,
                shift_lips=rq.balligator_shift_lips,
                column_name_jaws=BJAW,
                column_name_teeth=BTEETH,
                column_name_lips=BLIPS,
            )
        except:
            print("balligator_flag failed")
    else:
        if not quiet:
            print("Skipping degree larger big Alligator")

    # Tide Alligator

    talligator_required_bar_offset = (
        minimal_bars_with_indicators + rq.talligator_period_jaws + rq.talligator_shift_jaws
    )

    is_tide_alligator_has_enough_bar_in_dfsrc = ldfsrc >= talligator_required_bar_offset
    
    _msg_tide_nb_bars = "Tide Alligator has not enough bars in the DataFrame"
    #print("RQ.TIMEFRAME:",rq.timeframe)
    if rq.timeframe == "M1":
        _msg_tide_nb_bars = "Tide Alligator not added to M1 timeframe"
    if not is_tide_alligator_has_enough_bar_in_dfsrc and rq.talligator_flag:
        print_quiet(quiet,_msg_tide_nb_bars)
    we_add_tide_alligator_condition_met = is_tide_alligator_has_enough_bar_in_dfsrc and rq.talligator_flag and rq.timeframe != "M1"
    if rq.talligator_flag: 
        print_quiet(quiet,"talligator_flag is True")
    else:
        print_quiet(quiet,"talligator_flag is False")
        
    if we_add_tide_alligator_condition_met:
        print_quiet(quiet,"Adding Tide Alligator")

        try:
            i.alligator(
                period_jaws=rq.talligator_period_jaws,
                period_teeth=rq.talligator_period_teeth,
                period_lips=rq.talligator_period_lips,
                shift_jaws=rq.talligator_shift_jaws,
                shift_teeth=rq.talligator_shift_teeth,
                shift_lips=rq.talligator_shift_lips,
                column_name_jaws=TJAW,
                column_name_teeth=TTEETH,
                column_name_lips=TLIPS,
            )
            #print("Added Tide Alligator")
        except:
            print("talligator_flag failed")
    else:
        #print("NOT Adding Tide Alligator, WHY ??")
        if not quiet:
            print("Skipping degree Tide Alligator")

    # Creating Fractal Indicators for degrees 2,3,5,8,13,21,34,55,89

    try:
        i.fractals(
            column_name_high=FH,
            column_name_low=FL,
        )
    except:
        print("fractals failed")
    try:
        i.fractals3(
            column_name_high=FH3,
            column_name_low=FL3,
        )
    except:
        print("fractals 3 failed")
    try:
        i.fractals5(
            column_name_high=FH5,
            column_name_low=FL5,
        )
    except:
        print("fractals 5 failed")
    try:
        i.fractals8(
            column_name_high=FH8,
            column_name_low=FL8,
        )
    except:
        print("fractals 8 failed")
    try:
        i.fractals13(
            column_name_high=FH13,
            column_name_low=FL13,
        )
    except:
        print("fractals 13 failed")
    if (
        df_nb_bars >= minimal_bars_with_indicators + 21
    ):  # @a The amount of bars the chart has to have to calculate the indicator is the minimal number of bars we want with indicators + the period of the indicator
        try:
            i.fractals21(
                column_name_high=FH21,
                column_name_low=FL21,
            )
        except:
            print("fractals 21 failed")

    if df_nb_bars >= minimal_bars_with_indicators + 34:
        try:
            i.fractals34(
                column_name_high=FH34,
                column_name_low=FL34,
            )
        except:
            print("fractals 34 failed")
    else:
        if not quiet:
            print("Skipping Fractal 34")

    if df_nb_bars >= minimal_bars_with_indicators + 55:
        try:
            i.fractals55(
                column_name_high=FH55,
                column_name_low=FL55,
            )
        except:
            print("fractals 55 failed")
    else:
        if not quiet:
            print("Skipping Fractal 55")

    largest_fractal_bar_required_offset = (
        minimal_bars_with_indicators + rq.largest_fractal_period
    )
    if df_nb_bars >= largest_fractal_bar_required_offset:
        try:
            i.fractals89(
                column_name_high=FH89,
                column_name_low=FL89,
            )
        except:
            print("fractals 89 failed")
    else:
        if not quiet:
            print("Skipping Fractal 89")

    if gator_oscillator_flag:

        try:
            i.gator(
                period_jaws=13,
                period_teeth=8,
                period_lips=5,
                shift_jaws=8,
                shift_teeth=5,
                shift_lips=3,
                column_name_val1=GL,
                column_name_val2=GH,
            )
        except:
            print("gator failed")

    if mfi_flag:
        try:
            i.bw_mfi(column_name=MFI)
            # Add SQUAT Bar column to the DataFrame
            ## formula
            """
            from jgtutils.jgtconstants import MFI_SQUAT_STR,MFI_FAKE_STR,MFI_FADE_STR,MFI_GREEN_STR,MFI_SQUAT_ID,MFI_FAKE_ID,MFI_FADE_ID,MFI_GREEN_ID
            df.replace(MFI_SQUAT_STR, MFI_SQUAT_ID, inplace=True)  # Squat (+-) signal
            df.replace(MFI_FAKE_STR, MFI_FAKE_ID, inplace=True)    # Fake (-+) signal
            df.replace(MFI_FADE_STR, MFI_FADE_ID, inplace=True)    # Fade (--) signal
            df.replace(MFI_GREEN_STR, MFI_GREEN_ID, inplace=True)  # Green (++) signal
            """
            #print(" ADDING SQUAT PROTO Will be in CDS Module")

        except Exception as e:
            print("bw_mfi failed")
            print(e)

    if addAlligatorOffsetInFutur:
        try:
            _add_alligator_tmpcol_offset_in_futur(i)
        except:
            print("addAlligatorOffsetInFutur failed")

    dfresult = i.df

    #print("-------------------------------")
    #print(dfresult)
    #print("Lenght of dfresult b4 dropna: " + str(len(dfresult)))
    #dropnavalue = False
    if dropnavalue:
        dfresult = dfresult.dropna()
    try:
        dfresult.set_index("Date", inplace=True)
    except TypeError:
        pass
    #print("--------FOUND BUG 240615109 in dropna()-------")
    #print("Lenght of dfresult after dropna: " + str(len(dfresult)))
    #print(dfresult)
    #print("-------------------------------")

    normalize = True
    if normalize:
        dfresult = normalize_columns(dfresult, columns_to_normalize)

    if not quiet:
        print("done adding indicators :)")

    # if addAlligatorOffsetInFutur:
    #   _offset_alligator_tmpcol_in_futur(dfresult)
    return dfresult


def fix_too_short_df(dfsrc):
    """
    Fixes a DataFrame that is too short for calculating indicators.

    Args:
    dfsrc (pandas.DataFrame): The input DataFrame.

    Returns:
    pandas.DataFrame: The fixed DataFrame.
    """
    # print("IDS::debug len(dfsrc)" + str(len(dfsrc)))
    if len(dfsrc) < 110:

        # Get the 'Date' value from the first row
        start_date = dfsrc.iloc[0]["Date"]

        # Create a date range starting from the start_date
        date_range = pd.date_range(start=start_date, periods=110)
        # Create a DataFrame with the first row replicated 110 times
        dfsrc_first_row = pd.DataFrame([dfsrc.iloc[0]] * 110)

        # Add the date range to the DataFrame
        dfsrc_first_row["Date"] = date_range

        # Concatenate the two DataFrames
        dfsrc = pd.concat([dfsrc_first_row, dfsrc], ignore_index=True)
    return dfsrc


def normalize_columns(df: pd.DataFrame, columns: list, in_place=True) -> pd.DataFrame:
    if in_place:
        df_normalized = df
        for column in columns:
            df.loc[:, column] = df[column] / df[column].abs().max()
        return df
    else:
        df_normalized = df.copy()
        for column in columns:
            df_normalized.loc[:, column] = df[column] / df[column].abs().max()
    return df_normalized


def _add_alligator_tmpcol_offset_in_futur(i):

    i.smma(8, "jaws_tmp", "Median")
    i.smma(5, "teeth_tmp", "Median")
    i.smma(3, "lips_tmp", "Median")
    # df=i.df
    # Define the logic for adding alligator offset in the future
    # ...
    # indicator_currentDegree_alligator_jaw_column_name
    # from jgtapy.utils import  calculate_smma
    # df_j = calculate_smma(df['Median'], 8, 'jaws_tmp', median_col)
    # df_t = calculate_smma(df_median, period_teeth, column_name_teeth, median_col)
    # df_l = calculate_smma(df_median, period_lips, column_name_lips, median_col)

    # # Shift SMMAs
    # df_j[column_name_jaws] = df_j[column_name_jaws].shift(shift_jaws)
    # df_t[column_name_teeth] = df_t[column_name_teeth].shift(shift_teeth)
    # df_l[column_name_lips] = df_l[column_name_lips].shift(shift_lips)

    return i


# @STCGoal Support for the CLI making IDS

import JGTIDS as ids
import JGTPDSP as pds
from jgtutils.jgtos import get_data_path

#The new function name, following Python's PEP 8 style guide, could be `get_ph_to_df_and_create_ids_df`. This name is more readable and still describes what the function does: it gets PH to DataFrame and then creates IDS DataFrame.
def get_ph_to_df_and_create_ids_df(
    rq, run_jgtfxcli_on_error=True, columns_to_remove=None, quiet=True
):
    if rq is None:
        rq = JGTIDSRequest()
    df = pds.getPH(
        instrument=rq.instrument,
        timeframe=rq.timeframe,
        use_full=rq.use_full,
        use_fresh=rq.use_fresh,
        run_jgtfxcli_on_error=run_jgtfxcli_on_error,
        quiet=quiet,
        quote_count=rq.quotescount,
        keep_bid_ask=rq.keep_bid_ask,
        dropna_volume=rq.dropna_volume,
    )

    if not quiet:
        print(df)
    #print("rq.quotescount in get_ph_to_df_and_create_ids_df:", rq.quotescount)
    dfi = create_from_df(df, quiet=quiet, rq=rq, columns_to_remove=columns_to_remove)
    #print("get_ph_to_df_and_create_ids_df:: len :create_from_df", len(dfi))
    #exit(0)
    return dfi


def create_from_pds_file(
    rq: JGTIDSRequest = None,
    quiet=True,
    run_jgtfxcli_on_error=True,
    columns_to_remove=None,
    keep_bid_ask=False,
):
    """Create IDS (Indicator Data Service) with Fresh Data on the filestore

    Args:
        quiet (bool,optional): Output quiet
        rq (JGTIDSRequest, optional): The JGTIDSRequest object to use for the processing. Defaults to None.
        run_jgtfxcli_on_error (bool, optional): If True, runs jgtfxcli on error. Default is True.
        columns_to_remove (list, optional): List of column names to remove from the DataFrame. Default is None.
        keep_bid_ask (bool, optional): If True, keeps the bid and ask columns. Default is False.

    Returns:
        pandas.DataFrame: CDS DataFrame
    """
    if rq is None:
        rq = JGTIDSRequest()
    rq.keep_bid_ask = keep_bid_ask
    try:
        df = get_ph_to_df_and_create_ids_df(
            quiet=quiet,
            rq=rq,
            run_jgtfxcli_on_error=run_jgtfxcli_on_error,
            columns_to_remove=columns_to_remove,
        )

        return df
    except Exception as e:
        print("Error in createFromPDSFile")
        print(e)

        return None


def create_from_pds_file_to_ids_file(
    rq: JGTIDSRequest = None,
    columns_to_remove=None,
    quiet=True,
    keep_bid_ask=False,
):
    """
    Create a IDS file from a PDS file.

    Parameters:
    rq (JGTIDSRequest, optional): The JGTIDSRequest object to use for the processing. Defaults to None.
    columns_to_remove (list, optional): List of column names to remove from the IDS file. Default is None.
    quiet (bool, optional): If True, suppresses the output. Default is True.
    keep_bid_ask (bool, optional): If True, keeps the bid and ask columns. Default is False.

    Returns:
    - fpath (str): The file path of the created IDS file.
    - c (DataFrame): The DataFrame containing the data.

    """
    if rq is None:
        rq = JGTIDSRequest()
    #to workround the issue of the bid and ask columns, we set the request to the supplied value in this function
    rq.keep_bid_ask = keep_bid_ask
    if not quiet:
        print("columns_to_remove:", columns_to_remove)
    cdf = create_from_pds_file(rq=rq, quiet=quiet, columns_to_remove=columns_to_remove,keep_bid_ask=keep_bid_ask)

    # Define the file path based on the environment variable or local path
    fpath = write_ids(rq.instrument, rq.timeframe, rq.use_full, cdf)

    return fpath, cdf


def get_pov_local_data_filename(instrument:str,timeframe:str,use_full=False):
  nsdir="ids"
  return jos.get_pov_local_data_filename(instrument,timeframe,use_full=use_full,nsdir=nsdir)


def create_from_df(
    df,
    quiet=True,
    cc: JGTChartConfig = None,
    rq: JGTIDSRequest = None,
    columns_to_remove=None,
):
    """
    Creates a new DataFrame with indicators, signals, and cleansed columns added based on the input DataFrame.

    Args:
      df (pandas.DataFrame): The input DataFrame to add indicators, signals, and cleansed columns to.
      quiet (bool, optional): Whether to suppress console output during processing. Defaults to True.
      cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.
      rq (JGTIDSRequest, optional): The JGTIDSRequest object to use for the processing. Defaults to None.
      columns_to_remove (list, optional): List of column names to remove from the DataFrame. Default is None.


    Returns:
      pandas.DataFrame: The new DataFrame with indicators, signals, and cleansed columns added.
    """
    if cc is None:
        cc = JGTChartConfig()
    if rq is None:
        rq = JGTIDSRequest()

    if df.index.name == "Date":
        df.reset_index(inplace=True)

    # dfi = ids.tocds(df, quiet=quiet, cc=cc,rq=rq,columns_to_remove=columns_to_remove)
    # @a REPLACE BY LOGICS TO CREATE OUR IDS
    dfi = toids(df, quiet=quiet, cc=cc, rq=rq, columns_to_remove=columns_to_remove)

    return dfi


def toids(
    dfsrc,
    quiet=True,
    cc: JGTChartConfig = None,
    rq: JGTIDSRequest = None,
    columns_to_remove=None,
    format_boolean_columns_to_int=True,
    keep_bid_ask=False,
):
    dfi = ids_add_indicators(dfsrc, cc=cc, rq=rq)
    if format_boolean_columns_to_int:
        dfi = __format_boolean_columns_to_int(dfi, quiet=True)
    return dfi


def __format_boolean_columns_to_int(dfsrc, quiet=True):
    for col in dfsrc.columns:
        if dfsrc[col].dtype == bool:
            dfsrc[col] = dfsrc[col].astype(int)
    return dfsrc


def write_ids(instrument, timeframe, use_full, cdf):
    data_path_ids = get_data_path("ids", use_full=use_full)
    fpath = pds.mk_fullpath(instrument, timeframe, "csv", data_path_ids)
    # print(fpath)
    cdf.to_csv(fpath, index=True)
    return fpath

from jgtutils.coltypehelper import DTYPE_DEFINITIONS

def read_ids(instrument, timeframe, use_full=False):
    data_path_ids = get_data_path("ids", use_full=use_full)
    fpath = pds.mk_fullpath(instrument, timeframe, "csv", data_path_ids)
    if not os.path.exists(fpath):
        rq: JGTIDSRequest = JGTIDSRequest()
        rq.instrument = instrument
        rq.timeframe = timeframe
        rq.use_full = use_full
        createIDSService(rq)
    cdf = pd.read_csv(fpath, index_col=0,parse_dates=True,dtype=DTYPE_DEFINITIONS)
    return cdf

def select_value_in_currentbar(instrument, timeframe,coln, use_full=False):
    current_bar_data = read_ids_currentbar(instrument, timeframe, use_full)
    return current_bar_data[coln]

def select_value_in_lastcompletedbar(instrument, timeframe,coln, use_full=False):
    completed_bar = read_ids_lastcompletedbar(instrument, timeframe, use_full)
    return completed_bar[coln]

def read_ids_currentbar(instrument, timeframe, use_full):
    df=read_ids(instrument, timeframe, use_full)
    current_bar=df.iloc[-1]
    return current_bar

def read_ids_lastcompletedbar(instrument, timeframe, use_full):
    df=read_ids(instrument, timeframe, use_full)
    lastcompleted_bar=df.iloc[-2]
    return lastcompleted_bar

def createIDSService(
    rq: JGTIDSRequest = None,
    quiet=True,
    verbose_level=0,
):
    if rq is None:
        rq = JGTIDSRequest()
    # implementation goes here
    col2remove = constants.columns_to_remove
    config = jgtcommon.readconfig()
    if "columns_to_remove" in config:  # read it from config otherwise
        col2remove = config["columns_to_remove"] #@STCIssue Should be using settings (jgtutils) or what would be supplied in the request.
    quietting = True
    if verbose_level > 1:
        quietting = False
    
    if rq.viewpath:
        filepath=get_pov_local_data_filename(rq.instrument,rq.timeframe,rq.use_full)
        print(filepath)
        return
    try:
        # cdspath, cdf = cds.createFromPDSFileToCDSFile(
        # @a Migrate to IDS Logics
        # cdspath, cdf = cds.createFromPDSFileToCDSFile(
        idspath, idf = create_from_pds_file_to_ids_file(
            rq=rq,
            quiet=quietting,
            columns_to_remove=col2remove,
            keep_bid_ask=rq.keep_bid_ask,
        )  # @STCIssue: This is not supporting -c NB_BARS_TO_PROCESS, should it ?

        print_quiet(quiet, idspath)
        if verbose_level >1:
            print_quiet(quiet, idf)
        return idspath, idf
    except Exception as e:
        print("Failed to create IDS for : " + rq.instrument + "_" + rq.timeframe)
        print("jgtapycli::Exception in ...(: " + str(e))


def print_quiet(quiet, content):
    if not quiet:
        print(content)


