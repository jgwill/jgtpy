
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

columns_to_normalize = ["ao", "ac"] #@a Migrate to jgtutils.jgtconstants

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
    FH13,    FH21,    FH34,    FH55,    FH89,    FL13,    FL21,    FL34,    FL55,    FL89,
    GL,GH,
)

from jgtutils import (
    jgtconstants as constants,
    jgtcommon as jgtcommon,
    jgtwslhelper as wsl,
)

def ids_add_indicators(
    dfsrc,
    enablegator_oscillator_flag=False,
    enablemfi_flag=False,
    dropnavalue=True,
    quiet=True,
    cleanupOriginalColumn=True,
    useLEGACY=True,
    cc: JGTChartConfig = None,
    bypass_index_reset=False,
    big_alligator=False,
    rq: JGTIDSRequest = None,
):
    """
    Adds technical indicators to a given DataFrame.

    Args:
    dfsrc (pandas.DataFrame): The DataFrame to which the indicators will be added.
    enablegator_oscillator_flag (bool, optional): Whether to enable the Gator Oscillator indicator. Defaults to False.
    enablemfi_flag (bool, optional): Whether to enable the Money Flow Index indicator. Defaults to False.
    dropnavalue (bool, optional): Whether to drop rows with NaN values. Defaults to True.
    quiet (bool, optional): Whether to suppress console output. Defaults to False.
    cleanupOriginalColumn (bool, optional): Whether to clean up the original column. Defaults to True.
    useLEGACY (bool, optional): Whether to use the legacy version of the function. Defaults to True.
    cc (JGTChartConfig, optional): The JGTChartConfig object. Defaults to None.
    bypass_index_reset (bool, optional): Whether to bypass resetting the index. Defaults to False.
    big_alligator (bool, optional): Whether to enable the Alligator indicator. Defaults to False.
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
        dfresult = Indicators.jgt_create_ids_indicators_as_dataframe(
            dfsrc,
            enablegator_oscillator_flag,
            enablemfi_flag,
            cleanupOriginalColumn,
            quiet,
        )
    else:
        dfresult = ids_add_indicators_LEGACY(
            dfsrc=dfsrc,
            enablegator_oscillator_flag=enablegator_oscillator_flag,
            enablemfi_flag=enablemfi_flag,
            dropnavalue=dropnavalue,
            quiet=quiet,
            min_nb_bar_on_chart=cc.min_bar_on_chart,
            bypass_index_reset=bypass_index_reset,
            big_alligator=big_alligator,
            ids_request=rq,
        )

    return round_columns(dfresult, rq.rounding_decimal_min)


def round_columns(df, rounding_decimal_min=10):
    for col in df.columns:
        if df[col].dtype == "float64" and df[col].apply(lambda x: x % 1 != 0).any():
            df[col] = df[col].round(decimals=rounding_decimal_min)
            df[col] = df[col].apply(lambda x: 0 if "e" in str(x) else x)
    return df




def ids_add_indicators_LEGACY(
    dfsrc,
    enablegator_oscillator_flag=False,
    enablemfi_flag=False,
    dropnavalue=True,
    quiet=True,
    addAlligatorOffsetInFutur=False,
    big_alligator=False,
    balligator_period_jaws=89,
    largest_fractal_period=89,
    min_nb_bar_on_chart=300,
    bypass_index_reset=False,
    ids_request: JGTIDSRequest = None,
):
    """
    Adds various technical indicators to the input DataFrame. Is the same as in the jgtapy.legacy module.

    Args:
    dfsrc (pandas.DataFrame): The input DataFrame.
    enablegator_oscillator_flag (bool, optional): Whether to enable the Gator Oscillator indicator. Defaults to False.
    enablemfi_flag (bool, optional): Whether to enable the Money Flow Index indicator. Defaults to False.
    dropnavalue (bool, optional): Whether to drop rows with NaN values. Defaults to True.
    quiet (bool, optional): Whether to suppress print statements. Defaults to False.
    addAlligatorOffsetInFutur (bool, optional): (NOT IMPLEMENTED) Whether to add the Alligator offset in the future. Defaults to True.
    big_alligator_jaws_period (int, optional): (NOT IMPLEMENTED) The period of the Alligator jaws. Defaults to 89.
    largest_fractal_period (int, optional): (NOT IMPLEMENTED) The largest fractal period. Defaults to 89.
    min_nb_bar_on_chart (int, optional): The minimum number of bars on the chart. Defaults to 300.
    bypass_index_reset (bool, optional): Whether to bypass resetting the index. Defaults to False.
    ids_request (JGTIDSRequest, optional): The JGTIDSRequest object. Defaults to None.

    Returns:
    pandas.DataFrame: The input DataFrame with added technical indicators.
    """

    if ids_request is None:
        ids_request = JGTIDSRequest()

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

    # Assign numbers to variables with prefix 'balligator_'
    balligator_period_jaws = ids_request.balligator_period_jaws
    balligator_period_teeth = ids_request.balligator_period_teeth
    balligator_period_lips = ids_request.balligator_period_lips
    balligator_shift_jaws = ids_request.balligator_shift_jaws
    balligator_shift_teeth = ids_request.balligator_shift_teeth
    balligator_shift_lips = ids_request.balligator_shift_lips

    bAlligator_required_bar_offset = (
        minimal_bars_with_indicators + balligator_period_jaws + balligator_shift_jaws
    )

    if ldfsrc >= bAlligator_required_bar_offset and big_alligator:

        try:
            i.alligator(
                period_jaws=balligator_period_jaws,
                period_teeth=balligator_period_teeth,
                period_lips=balligator_period_lips,
                shift_jaws=balligator_shift_jaws,
                shift_teeth=balligator_shift_teeth,
                shift_lips=balligator_shift_lips,
                column_name_jaws=BJAW,
                column_name_teeth=BTEETH,
                column_name_lips=BLIPS,
            )
        except:
            print("big_alligator failed")
    else:
        if not quiet:
            print("Skipping degree larger big Alligator")

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
        minimal_bars_with_indicators + largest_fractal_period
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

    if enablegator_oscillator_flag:

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

    if enablemfi_flag:
        try:
            i.bw_mfi(column_name=MFI)
        except:
            print("bw_mfi failed")

    if addAlligatorOffsetInFutur:
        try:
            _add_alligator_tmpcol_offset_in_futur(i)
        except:
            print("addAlligatorOffsetInFutur failed")

    dfresult = i.df

    if dropnavalue:
        dfresult = dfresult.dropna()
    try:
        dfresult.set_index("Date", inplace=True)
    except TypeError:
        pass

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




#@STCGoal Support for the CLI making IDS

import JGTIDS as ids
import JGTPDSP as pds
from jgtutils.jgtos import get_data_path

def _getPH_to_DF_wrapper_240304(instrument, timeframe, quiet, cc, use_full, rq,use_fresh=False ,run_jgtfxcli_on_error=True,columns_to_remove=None):

    df=pds.getPH(instrument,
            timeframe,
            quiet=quiet,
            use_full=use_full,
            use_fresh=use_fresh,
            run_jgtfxcli_on_error=run_jgtfxcli_on_error,
            )

    if not quiet:
        print(df)

    dfi = createFromDF(df, quiet=quiet, cc=cc,rq=rq,
                       columns_to_remove=columns_to_remove)
    return dfi


def createFromPDSFile(
    instrument,
    timeframe,
    quiet=True,
    cc: JGTChartConfig = None,
    use_full=False, #@STCIssue USELESS Somehow here :NOPE it reads a different file
    rq:JGTIDSRequest=None,
    run_jgtfxcli_on_error=True,
    columns_to_remove=None,
    use_fresh=False

):
    """Create IDS (Indicator Data Service) with Fresh Data on the filestore

    Args:
        instrument (str): symbol
        timeframe (str): TF
        quiet (bool,optional): Output quiet
        cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.
        use_full (bool, optional): If True, reads the full CDS file. Default is False.
        rq (JGTIDSRequest, optional): The JGTIDSRequest object to use for the processing. Defaults to None. 
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


def createFromPDSFileToIDSFile(
    instrument,
    timeframe,
    columns_to_remove=None,
    quiet=True,
    tlid_range=None,
    use_full=False,
    rq:JGTIDSRequest=None,
    use_fresh=False,
):
    """
    Create a IDS file from a PDS file.

    Parameters:
    instrument (str): The instrument name.
    timeframe (str): The timeframe of the data.
    columns_to_remove (list, optional): List of column names to remove from the CDS file. Default is None.
    quiet (bool, optional): If True, suppresses the output. Default is True.
    tlid_range (str, optional): The TLID range to retrieve. Default is None.
    use_full (bool, optional): If True, reads/writes the full CDS file. Default is False.
    rq (JGTIDSRequest, optional): The JGTIDSRequest object to use for the processing. Defaults to None.

    Returns:
    - fpath (str): The file path of the created CDS file.
    - c (DataFrame): The DataFrame containing the data.

    """
    if rq is None:
        rq = JGTIDSRequest()
    
    cdf = createFromPDSFile(
        instrument, timeframe, quiet,         
        use_full=use_full, 
        rq=rq,
        columns_to_remove=columns_to_remove,
        use_fresh=use_fresh
    )


    # Define the file path based on the environment variable or local path
    fpath = writeIDS(instrument, timeframe, use_full, cdf)

    return fpath, cdf

def createFromDF(df, quiet=True, 
                 cc: JGTChartConfig = None,
                 rq: JGTIDSRequest=None,
                 columns_to_remove=None
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
    
    #dfi = ids.tocds(df, quiet=quiet, cc=cc,rq=rq,columns_to_remove=columns_to_remove) 
    #@a REPLACE BY LOGICS TO CREATE OUR IDS
    dfi = toids(df, quiet=quiet, cc=cc, rq=rq, columns_to_remove=columns_to_remove)
    
    return dfi

def toids(dfsrc, quiet=True, cc: JGTChartConfig = None, rq: JGTIDSRequest=None, columns_to_remove=None):
    dfi = ids_add_indicators(dfsrc, cc=cc, rq=rq)
    
    return dfi

def writeIDS(instrument, timeframe, use_full, cdf):
    data_path_ids = get_data_path("ids", use_full=use_full)
    fpath = pds.mk_fullpath(instrument, timeframe, "csv", data_path_ids)
    # print(fpath)
    cdf.to_csv(fpath, index=True)
    return fpath

#@STCGoal CLI

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Process command parameters.")
    # jgtfxcommon.add_main_arguments(parser)
    jgtcommon.add_instrument_timeframe_arguments(parser)
    jgtcommon.add_date_arguments(parser)
    jgtcommon.add_tlid_range_argument(parser)
    jgtcommon.add_max_bars_arguments(parser)
    # jgtcommon.add_output_argument(parser)
    # jgtfxcommon.add_quiet_argument(parser)
    jgtcommon.add_verbose_argument(parser)
    
    jgtcommon.add_use_full_argument(parser)
    jgtcommon.add_use_fresh_argument(parser)
    parser.add_argument(
        "--enablegator_oscillator_flag",
        action="store_true",
        help="Enable the Gator Oscillator indicator.",
    )
    parser.add_argument(
        "--enablemfi_flag",
        action="store_true",
        help="Enable the Money Flow Index indicator.",
    )
    
    parser.add_argument(
        "--bypass_index_reset",
        action="store_true",
        help="Bypass resetting the index.",
    )
    parser.add_argument(
        "--big_alligator",
        action="store_true",
        help="Enable the Alligator indicator.",
    )
    parser.add_argument(
        "--balligator_period_jaws",
        type=int,
        default=89,
        help="The period of the Alligator jaws.",
    )
    parser.add_argument(
        "--largest_fractal_period",
        type=int,
        default=89,
        help="The largest fractal period.",
    )
    
    # jgtcommon.add_cds_argument(parser)
    args = parser.parse_args()
    return args


def main():
    cc = JGTChartConfig()
    rq = JGTIDSRequest()
    
    args = parse_args()
    
    #enablegator_oscillator_flag, enablemfi_flag, big_alligator, balligator_period_jaws, largest_fractal_period
    #@STCIssue Bellow Validation required.
    rq.enablegator_oscillator_flag=args.enablegator_oscillator_flag
    rq.enablemfi_flag=args.enablemfi_flag
    rq.big_alligator=args.big_alligator
    rq.balligator_period_jaws=args.balligator_period_jaws
    rq.largest_fractal_period=args.largest_fractal_period
    
    instrument = args.instrument
    timeframe = args.timeframe
    quotes_count = args.quotescount
    cc.nb_bar_on_chart = quotes_count
    
    verbose_level = args.verbose
    quiet = False
    if verbose_level == 0:
        quiet = True
    
    full = False
    fresh = False
    if args.fresh:
        fresh=True
    
    if args.full:
        full = True

    date_from = None
    date_to = None
    tlid_range = None
    if args.tlidrange:
        # @STCGoal Get range prices from cache or request new
        tlid_range = args.tlidrange
        print("#FUTURE Support for tlid range")
        tmpcmd = wsl._mkbash_cmd_string_jgtfxcli_range(
            instrument, timeframe, tlid_range,verbose_level=verbose_level,
            use_full=full
        )
        print(tmpcmd)
        print("#-----------Stay tune -------- Quitting for now")
        return

    if args.datefrom:
        date_from = args.datefrom.replace("/", ".")
    if args.dateto:
        date_to = args.dateto.replace("/", ".")


    process_ids = True

    if process_ids:
        print("Processing IDS")
        output = True


    if verbose_level > 1:
        if date_from:
            print("Date from : " + str(date_from))
        if date_to:
            print("Date to : " + str(date_to))

    try:

        print_quiet(quiet, "Getting for : " + instrument + "_" + timeframe)
        instruments = instrument.split(",")
        timeframes = timeframe.split(",")

        for instrument in instruments:
            for timeframe in timeframes:
                createIDS_for_main(
                    instrument,
                    timeframe,
                    quiet=quiet,
                    verbose_level=verbose_level,
                    tlid_range=tlid_range,
                    cc=cc,
                    use_full=full,
                    use_fresh=fresh
                )


    except Exception as e:
        jgtcommon.print_exception(e)




def createIDS_for_main(
    instrument,
    timeframe,
    quiet,
    verbose_level=0,
    tlid_range=None,
    cc: JGTChartConfig = None,
    use_full=False,
    use_fresh=False,
    rq: JGTIDSRequest = None,
):
    if rq is None:
        rq = JGTIDSRequest()
    # implementation goes here
    col2remove = constants.columns_to_remove
    config = jgtcommon.readconfig()
    if "columns_to_remove" in config:  # read it from config otherwise
        col2remove = config["columns_to_remove"]
    quietting = True
    if verbose_level > 1:
        quietting = False
        
    try:
        #cdspath, cdf = cds.createFromPDSFileToCDSFile(
        #@a Migrate to IDS Logics
        # cdspath, cdf = cds.createFromPDSFileToCDSFile( 
        cdspath, cdf = createFromPDSFileToIDSFile( 
            instrument, 
            timeframe, 
            quiet=quietting,
            rq=rq,
            #cc=cc,
            use_full=use_full,
            use_fresh=use_fresh,
            columns_to_remove=col2remove,
        )  # @STCIssue: This is not supporting -c NB_BARS_TO_PROCESS, should it ?
        
        print_quiet(quiet, cdspath)
        print_quiet(quiet, cdf)
    except Exception as e:
        print("Failed to create IDS for : " + instrument + "_" + timeframe)
        print("jgtapycli::Exception in ...(: " + str(e))
        

def print_quiet(quiet, content):
    if not quiet:
        print(content)


if __name__ == "__main__":
    main()


    