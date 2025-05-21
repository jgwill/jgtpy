import warnings

# Ignore FutureWarning
warnings.simplefilter(action="ignore", category=FutureWarning)

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


import pandas as pd
pd.options.mode.copy_on_write = True
import datetime
from JGTPDHelper import (
    jgtpd_drop_col_by_name,
    __cleanse_ao_peak_v1_secondary_columns,
    _pds_cleanse_original_columns,
    pds_cleanse_extra_columns,
)

from jgtapy import Indicators

from aohelper import add_ao_price_peaks_v2

from JGTChartConfig import JGTChartConfig
from JGTIDSRequest import JGTIDSRequest

# %%
# @title Vars
_dtformat = "%m.%d.%Y %H:%M:%S"

# %%
# @title INDICATOR's Data Frame Columns naming


from jgtutils.jgtconstants import *

from jgtutils.jgtconstants import (
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
    FDB,
    FDBB,
    FDBS,
    ACB,
    ACS,
    SB,
    SS,
    AO,
    AC,
    PRICE_PEAK_ABOVE,
    PRICE_PEAK_BELLOW,
    AO_PEAK_ABOVE,
    AO_PEAK_BELLOW,
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
    MFI,
    ZONE_SIGNAL,
)
from jgtutils.colconverthelper import zone_str_to_id

# %%
# @title Range shift add col drop na
# --@STCGoal PDS Utils
def _jgtpd_col_add_range_shifting_dropnas(
    dfsrc,
    ctxcolname=indicator_AO_awesomeOscillator_column_name,
    colprefix="pao",
    endrange=10,
):
    return _jgtpd_dropnas_on_any_rows(
        _jgtpd_col_add_range_shifting(dfsrc, ctxcolname, colprefix, endrange)
    )


# @title BACKWARD Range shift col
def _jgtpd_col_add_range_shifting(
    dfsrc,
    ctxcolname=indicator_AO_awesomeOscillator_column_name,
    colprefix="pao",
    endrange=10,
):
    """Add a BACKWARD range of shifted values
    for a column with a prefixed numbered.

    Args:
         dfsrc (DataFrame source)
         ctxcolname (column name from)
         colprefix (new columns prefix)
         endrange (the end of the range from 0)

    Returns:
      DataFrame with new columns
    """
    for i in range(endrange):
        dfsrc[colprefix + str(i)] = dfsrc[ctxcolname].shift(i)
    return dfsrc


# %%
# --@STCGoal IDS Indicators and related / CDS


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


columns_to_normalize = ["ao", "ac"]


def ids_add_indicatorsV2(
    dfsrc,
    dropnavalue=True,
    quiet=True,
    cleanupOriginalColumn=True,
    cc: JGTChartConfig = None,
    ids_request: JGTIDSRequest = None,
):
    """
    #@STCIssue Backward Compatibility ??
    #@STCGoal What is the ultimate goal ?
      #@STCGoal Well Migrated to the new version of the function
        #@STCIssue   JGTChartConfig/JGTIDSRequest Unclear about Creation of IDS and What Goes in the Chart (ADS)
          #@a ADSRequest vs IDSRequest/CDSRequest
    """
    return None


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

    #Migrated from Signature to Request Object
    enablegator_oscillator_flag=rq.gator_oscillator_flag
    enablemfi_flag=rq.mfi_flag
    big_alligator=rq.balligator_flag
    balligator_period_jaws=rq.balligator_period_jaws
    largest_fractal_period=rq.largest_fractal_period

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
            balligator_period_jaws=balligator_period_jaws,
            largest_fractal_period=largest_fractal_period,
        )

    return round_columns(dfresult, rq.rounding_decimal_min)


def round_columns(df, rounding_decimal_min=10):
    for col in df.columns:
        if df[col].dtype == "float64" and df[col].apply(lambda x: x % 1 != 0).any():
            df[col] = df[col].round(decimals=rounding_decimal_min)
            df[col] = df[col].apply(lambda x: 0 if "e" in str(x) else x)
    return df


def round_columns_v2(df, rounding_decimal_min=10):
    df = df.copy()
    float_cols = df.select_dtypes(include=["float64"]).columns
    for col in float_cols:
        if df[col].apply(lambda x: x % 1 != 0).any():
            df[col] = df[col].round(decimals=rounding_decimal_min)
            df[col] = df[col].apply(lambda x: 0 if "e" in str(x) else x)
    return df


def ids_add_indicators_LEGACY(
    dfsrc,
    enablegator_oscillator_flag=False,
    enablemfi_flag=True,
    dropnavalue=True,
    quiet=True,
    addAlligatorOffsetInFutur=False,
    big_alligator=False,
    balligator_period_jaws=89,
    largest_fractal_period=89,
    min_nb_bar_on_chart=NB_BARS_BY_DEFAULT_IN_CDS,
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
    min_nb_bar_on_chart (int, optional): The minimum number of bars on the chart. Defaults to NB_BARS_BY_DEFAULT_IN_CDS.
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


def _offset_alligator_tmpcol_in_futur(dfsrc):
    dfsrc["jaws_tmp2"] = dfsrc["jaws_tmp"].shift(8)
    dfsrc["teeth_tmp2"] = dfsrc["teeth_tmp"].shift(5)
    dfsrc["lips_tmp2"] = dfsrc["lips_tmp"].shift(3)

    return dfsrc


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


# %%
# @title Pandas JGT Utilities


def _jgtpd_dropnas_on_any_rows(dfsrc):
    return dfsrc.dropna(axis="rows")


def _jgtpd_drop_cols_from_to_by_name(dfsrc, firstcolname, lastcolname, _axis=1):
    try:
        return dfsrc.drop(dfsrc.loc[:, firstcolname:lastcolname].columns, axis=_axis)
    except:
        return dfsrc


def _jgtpd_col_drop_range(dfsrc, colprefix="pao", endrange=10):
    firstcolname = colprefix + str(1)
    lastcolname = colprefix + str(endrange)
    return _jgtpd_drop_cols_from_to_by_name(dfsrc, firstcolname, lastcolname, 1)


def _ids_add_fdb_intermediaries_columns(dfsrc):
    """
    Adds intermediate columns to the given DataFrame for the purpose of
    identifying fractal bullish and bearish bars.

    Args:
    - dfsrc: A pandas DataFrame containing OHLC data.

    Returns:
    - A pandas DataFrame with additional columns for intermediate calculations.
    """

    # Bullish
    dfsrc["HighisBellowLips"] = dfsrc.lips > dfsrc.High

    dfsrc["LowIsLower"] = dfsrc.Low < dfsrc.Low.shift()

    dfsrc["ClosedAboveMedian"] = dfsrc.Close > dfsrc.Median

    # Bearish FDBS

    dfsrc["LowisAboveLips"] = dfsrc.lips < dfsrc.Low

    dfsrc["HighIsHigher"] = dfsrc.High > dfsrc.High.shift()

    dfsrc["ClosedBellowMedian"] = dfsrc.Close < dfsrc.Median
    return dfsrc


def _ids_clear_fdb_intermediaries_columns(dfsrc, quiet=False):
    """
    This function drops FDB columns from a pandas dataframe that are not needed for further processing.signalCode_fractalDivergentBar_column_name

    Args:
    - dfsrc: pandas dataframe
    - quiet: boolean, default False. If True, suppresses the print statement when KeyError is caught.

    Returns:
    - dfsrc: pandas dataframe with the specified columns dropped.
    """
    try:
        dfsrc = _jgtpd_drop_cols_from_to_by_name(
            dfsrc, "HighisBellowLips", "ClosedBellowMedian"
        )
    except KeyError:
        if not quiet:
            print("Might cleared already")
        pass
    return dfsrc




def _ids_add_fdb_column_logics_v2(dfsrc, quiet=False):
    dfsrc["fdbb"] = (
        (dfsrc.lips > dfsrc.High)
        & (dfsrc.Low < dfsrc.Low.shift())
        & (dfsrc.Close > dfsrc.Median)
    ).astype(int)
    dfsrc["fdbs"] = (
        (dfsrc.lips < dfsrc.Low)
        & (dfsrc.High > dfsrc.High.shift())
        & (dfsrc.Close < dfsrc.Median)
    ).astype(int)
    dfsrc["fdb"] = dfsrc.apply(
        lambda row: 1 if row["fdbb"] > 0 else -1 if row["fdbs"] > 0 else 0, axis=1
    )
    return dfsrc


def _ids_add_fdb_column_logics(dfsrc, _dropIntermediariesColumns=True, quiet=False):
    """
    Adds FDB (Fractal Divergence Buy) and FDS (Fractal Divergence Sell) columns to the input dataframe based on certain conditions.

    Args:
    - dfsrc: pandas dataframe, input dataframe to which FDB and FDS columns need to be added.
    - _dropIntermediariesColumns: bool, default True. If True, intermediary columns added during the calculation will be dropped.
    - quiet: bool, default False. If True, suppresses the print statements.

    Returns:
    - dfsrc: pandas dataframe, dataframe with FDB and FDS columns added.
    """
    dfsrc = _ids_add_fdb_intermediaries_columns(dfsrc)
    for i, row in dfsrc.iterrows():

        ClosedAboveMedian = dfsrc.at[i, "ClosedAboveMedian"]
        LowIsLower = dfsrc.at[i, "LowIsLower"]
        HighisBellowLips = dfsrc.at[i, "HighisBellowLips"]
        ClosedBellowMedian = dfsrc.at[i, "ClosedBellowMedian"]
        HighIsHigher = dfsrc.at[i, "HighIsHigher"]
        LowisAboveLips = dfsrc.at[i, "LowisAboveLips"]

        # default values
        dfsrc.at[i, FDBB] = 0
        dfsrc.at[i, FDBS] = 0
        dfsrc.at[i, FDB] = 0

        ##################################################
        #########   FDBB
        isFDB = 0
        isFDBCode = 0
        high = 0
        low = 0
        if HighisBellowLips and LowIsLower and ClosedAboveMedian:
            isFDB = 1
            isFDBCode = 1
            high = dfsrc.at[i, HIGH]
            low = dfsrc.at[i, LOW]
        dfsrc.at[i, "fdbbhigh"] = high
        dfsrc.at[i, "fdbblow"] = low

        dfsrc.at[i, FDBB] = isFDB
        dfsrc.at[i, FDB] = isFDBCode  # So we have All
        isAfdbb = isFDB
        ##################################################
        #########   FDBS

        if not isAfdbb:
            isFDB = 0
            isFDBCode = 0
            high = 0
            low = 0
            if LowisAboveLips and HighIsHigher and ClosedBellowMedian:
                isFDB = 1
                isFDBCode = -1
                high = dfsrc.at[i, HIGH]
                low = dfsrc.at[i, LOW]

            dfsrc.at[i, "fdbshigh"] = high
            dfsrc.at[i, "fdbslow"] = low

            dfsrc.at[i, FDBS] = isFDB
            dfsrc.at[i, FDB] = isFDBCode
    if _dropIntermediariesColumns:
        dfsrc = _ids_clear_fdb_intermediaries_columns(dfsrc, quiet=quiet)
    return dfsrc


# @title aof_flag function pto (AO Fractals)


# @title Range shift col
def _add_ao_fractal_peak_v1(
    dfsrc,
    ctxcolname=indicator_AO_awesomeOscillator_column_name,
    poscolprefix="pao",
    negcolprefix="nao",
    endrange=10,
    quiet=False,
    cc: JGTChartConfig = None,
):
    """Make the AO Fractal Peak

    Args:
         dfsrc (DataFrame source)
         ctxcolname (column name from)
         poscolprefix (prefix positive (futur) ao sec col )
         negcolprefix (prefix negative (past) ao sec col )
         endrange (total range from 0 (zero being the current in the output))
         quiet (quiet mode)
         cc (JGTChartConfig, optional): The JGTChartConfig object. Defaults to None.

    Returns:
      DataFrame with new AO Peak columns
        aof (21,13,0,-13,-21) Fractal value of the peak
        aofvalue (AO Value)
        aofhighao (AO value on Bullish Peak)
        aoflowao (AO value of Bearish Peak)
        aofhigh  (Price High of that peak)
        aoflow   (Price Low of that Peak)

    """

    half = endrange / 2
    l_df = len(dfsrc)
    for o in range(endrange):
        i = int(o - half)

        _cn = poscolprefix + str(i)
        if i < 0:
            _cn = negcolprefix + str(i).replace("-", "")
        dfsrc[_cn] = dfsrc[ctxcolname].shift(i)

    # This filters out some noisy peaks that are too low or too high
    df_standardDeviation = dfsrc[ctxcolname].std()
    df_max = dfsrc[ctxcolname].max()
    df_min = dfsrc[ctxcolname].min()
    df_filterOutaof_flagThreshold_ABOVE = (df_standardDeviation + df_max) / 2
    df_filterOutaof_flagThreshold_BELLOW = ((df_standardDeviation * -1) + df_min) / 2

    if not quiet:
        print(
            "filterout (std) Above(max)/(min)Bellow:  ("
            + str(df_standardDeviation)
            + ")  "
            + str(df_filterOutaof_flagThreshold_ABOVE)
            + "("
            + str(df_max)
            + ") / ("
            + str(df_min)
            + ") "
            + str(df_filterOutaof_flagThreshold_BELLOW)
        )

    # Counting the peaks
    countUpPeak = 0
    countDownPeak = 0
    countDiscarted = 0
    for i, row in dfsrc.iterrows():
        baraof_flag = 0
        dt = i
        curHigh = dfsrc.at[i, "High"]
        curLow = dfsrc.at[i, "Low"]
        cur = dfsrc.at[i, indicator_AO_awesomeOscillator_column_name]
        n9 = dfsrc.at[i, "n9"]
        n13 = dfsrc.at[i, "n13"]
        n12 = dfsrc.at[i, "n12"]
        n11 = dfsrc.at[i, "n11"]
        n10 = dfsrc.at[i, "n10"]
        n8 = dfsrc.at[i, "n8"]
        n7 = dfsrc.at[i, "n7"]
        n6 = dfsrc.at[i, "n6"]
        n5 = dfsrc.at[i, "n5"]
        n4 = dfsrc.at[i, "n4"]
        n3 = dfsrc.at[i, "n3"]
        n2 = dfsrc.at[i, "n2"]
        n1 = dfsrc.at[i, "n1"]
        p0 = dfsrc.at[i, "p0"]
        p1 = dfsrc.at[i, "p1"]
        p2 = dfsrc.at[i, "p2"]
        p3 = dfsrc.at[i, "p3"]
        p4 = dfsrc.at[i, "p4"]
        p5 = dfsrc.at[i, "p5"]
        p6 = dfsrc.at[i, "p6"]
        p7 = dfsrc.at[i, "p7"]
        p8 = dfsrc.at[i, "p8"]
        p9 = dfsrc.at[i, "p9"]
        p10 = dfsrc.at[i, "p10"]
        p11 = dfsrc.at[i, "p11"]
        p12 = dfsrc.at[i, "p12"]
        p13 = dfsrc.at[i, "p13"]

        outHigh = 0
        outHighAO = 0
        outLow = 0
        outLowAO = 0

        # Ways to find a peak that might be enhanced later with another methods using sequence recognition in machine learning
        if (
            cur > p1
            and cur > p2
            and cur > p3
            and cur > p4
            and cur > p5
            and cur > p6
            and cur > p7
            and cur > p8
            and cur > p8
            and cur > p9
            and cur > p10
            and cur > p11
            and cur > p12
            and cur > p13
        ) and (
            cur > n1
            and cur > n2
            and cur > n3
            and cur > n4
            and cur > n5
            and cur > n6
            and cur > n7
            and cur > n8
            and cur > n9
            and cur > n10
            and cur > n11
            and cur > n12
            and cur > n13
        ):
            if cur > 0 and cur > df_filterOutaof_flagThreshold_ABOVE:
                baraof_flag = 21
                if not quiet:
                    print("We have an up peak at:" + str(dt))
                countUpPeak = countUpPeak + 1
            else:
                if cur > 0 and cur > df_standardDeviation and baraof_flag != 21:
                    baraof_flag = 13
                    if not quiet:
                        print("We have an up peak at:" + str(dt))
                    countUpPeak = countUpPeak + 1
        else:
            if (
                cur < p1
                and cur < p2
                and cur < p3
                and cur < p4
                and cur < p5
                and cur < p6
                and cur < p7
                and cur < p8
                and cur < p8
                and cur < p9
                and cur < p10
                and cur < p11
                and cur < p12
                and cur < p13
            ) and (
                cur < n1
                and cur < n2
                and cur < n3
                and cur < n4
                and cur < n5
                and cur < n6
                and cur < n7
                and cur < n8
                and cur < n9
                and cur < n10
                and cur < n11
                and cur < n12
                and cur < n13
            ):
                if cur < 0 and cur < df_filterOutaof_flagThreshold_BELLOW:
                    baraof_flag = -21
                    if not quiet:
                        print("We have an down peak at: " + str(dt))
                    countDownPeak = countDownPeak + 1
                else:
                    if (
                        cur < 0
                        and cur < df_standardDeviation * -1
                        and baraof_flag != -21
                    ):
                        baraof_flag = -13
                        if not quiet:
                            print("We have an down peak at: " + str(dt))
                        countDownPeak = countDownPeak + 1
        if baraof_flag != 0:
            if cur > 0:
                outHigh = curHigh
                outHighAO = cur
                outLowAO = 0
                outLow = 0  # We are Above ZL so we dont want to use Low
            else:
                outHigh = 0  # We are Bellow ZL so we dont want to use High
                outLow = curLow
                outLowAO = cur
                outHighAO = 0

        # aof_flag is the Fractal Peak Value, it would be used to find twin peak signals and learn

        # @STCIssue I question the use of some of these columns, they might be temporary

        dfsrc.at[i, indicator_ao_fractalPeakOfMomentum_column_name] = baraof_flag
        dfsrc.at[i, indicator_ao_fractalPeakValue_column_name] = cur  # current AO Value
        dfsrc.at[i, "aofhighao"] = outHighAO
        dfsrc.at[i, "aoflowao"] = outLowAO
        dfsrc.at[i, "aofhigh"] = outHigh
        dfsrc.at[i, "aoflow"] = outLow
    l_df = len(dfsrc)
    if not quiet:
        print(
            "Total Peak - Up:"
            + str(countUpPeak)
            + ", Dn: "
            + str(countDownPeak)
            + " on total: "
            + str(l_df)
        )
    dfsrc = __cleanse_ao_peak_v1_secondary_columns(dfsrc, True)
    return dfsrc


# @title Add CDS signals

from jgtutils.jgtconstants import MFI,MFI_SQUAT,MFI_GREEN,MFI_FADE,MFI_FAKE,MFI_SIGNAL,MFI_VAL,MFI_SQUAT_STR,MFI_FAKE_STR,MFI_FADE_STR,MFI_GREEN_STR,MFI_SQUAT_ID,MFI_FAKE_ID,MFI_FADE_ID,MFI_GREEN_ID

def _cds_add_mfi_squat_n_signals_column_logics_v1(dfsrc, quiet=False):
    """
    Adds MFI (Market Facilitation Index (reference: B. Williams)) squat column logics to the given DataFrame.

    Parameters:
    - dfsrc (DataFrame): The input DataFrame to which the MFI squat column logics will be added.
    - quiet (bool): If True, suppresses the output messages. Default is False.

    Returns:
    - dfsrc (DataFrame): The updated DataFrame with the MFI squat column logics added.
    """
    #@STCIssue If MFI Flags off that bugs. 'DataFrame' object has no attribute 'mfi'
    dfsrc[MFI_SQUAT] = (
        (dfsrc.Volume > 0)
        & (dfsrc.Volume > dfsrc.Volume.shift())
        & (dfsrc.mfi < dfsrc.mfi.shift())
    ).astype(int)
    dfsrc[MFI_GREEN] = (
        (dfsrc.Volume > 0)
        & (dfsrc.Volume > dfsrc.Volume.shift())
        & (dfsrc.mfi > dfsrc.mfi.shift())
    ).astype(int)
    dfsrc[MFI_FADE] = (
        (dfsrc.Volume > 0)
        & (dfsrc.Volume < dfsrc.Volume.shift())
        & (dfsrc.mfi < dfsrc.mfi.shift())
    ).astype(int)
    dfsrc[MFI_FAKE] = (
        (dfsrc.Volume > 0)
        & (dfsrc.Volume < dfsrc.Volume.shift())
        & (dfsrc.mfi > dfsrc.mfi.shift())
        ).astype(int)
    dfsrc[MFI_SIGNAL] = dfsrc.apply(
         lambda row: MFI_SQUAT_ID if row[MFI_SQUAT] > 0 else MFI_GREEN_ID if row[MFI_GREEN] > 0 else MFI_FADE_ID if row[MFI_FADE]>0 else MFI_FAKE_ID if row[MFI_FAKE]>0 else 0 , axis=1
     )
    #MFI_GREEN_STR = "++"
    #MFI_FADE_STR = "--"
    #MFI_FAKE_STR = "-+"
    #MFI_SQUAT_STR = "+-"
    dfsrc[MFI_VAL] = dfsrc.apply(
         lambda row: MFI_GREEN_STR if row[MFI_SIGNAL] == MFI_GREEN_ID else MFI_FADE_STR if row[MFI_SIGNAL] == MFI_FADE_ID else MFI_FAKE_STR if row[MFI_SIGNAL] == MFI_FAKE_ID else MFI_SQUAT_STR if row[MFI_SIGNAL] == MFI_SQUAT_ID else "0" , axis=1)
    return dfsrc



def cds_add_signals_to_indicators(
    dfires,
    _aopeak_range=28,
    quiet=False,
    cc: JGTChartConfig = None,
    rq: JGTIDSRequest = None,
):
    if rq is None:
        rq = JGTIDSRequest()
    if cc is None:
        cc = JGTChartConfig()

    if not rq.disable_ao_peaks_v1:
        dfires = _add_ao_fractal_peak_v1(
            dfires,
            AO,
            "p",
            "n",
            _aopeak_range,
            quiet=quiet,
            cc=cc,
        )
        dfires = __cleanse_ao_peak_v1_secondary_columns(dfires, quiet=True)
    return dfires


def tocds(
    dfsrc,
    quiet=True,
    cc: JGTChartConfig = None,
    rq: JGTIDSRequest = None,
    columns_to_remove=None,
    use_v2_jgtapyhelper=True,
    add_mfi_signals_proto=True,
):
    if rq is None:
        rq = JGTIDSRequest()
    if cc is None:
        cc = JGTChartConfig()
    if use_v2_jgtapyhelper:
        import jgtapyhelper as tah
        #print("RQ:", rq.timeframe)
        dfires =tah.toids(dfsrc, cc=cc, rq=rq, quiet=quiet, columns_to_remove=columns_to_remove)
    else:
        print("DEPRECATION NOTICE: tocds() is deprecated and will be removed in a future release. Please use toids() from jgtapyhelper instead.")
        dfires = ids_add_indicators(dfsrc, quiet=quiet, cc=cc, rq=rq)
    
    dfires = _ids_add_fdb_column_logics_v2(dfires, quiet=quiet)                 #@STCIssue SignalBusiness Code
    dfires = cds_add_signals_to_indicators(dfires, quiet=quiet, cc=cc, rq=rq)   #@STCIssue SignalBusiness Code
    dfires = jgti_add_zlc_plus_other_AO_signal(dfires, quiet=quiet, rq=rq)      #@STCIssue SignalBusiness Code
    if rq.keep_bid_ask==False:
        dfires = _pds_cleanse_original_columns(dfires, quiet=True)  
    dfires = __cleanse_ao_peak_v1_secondary_columns(dfires, quiet=True)
    dfires = __format_boolean_columns_to_int(dfires, quiet=True)
    dfires = add_ao_price_peaks_v2(dfires, quiet=True, rq=rq)   
    
    if add_mfi_signals_proto:
        dfires= _cds_add_mfi_squat_n_signals_column_logics_v1(dfires, quiet=quiet)
    
    
    # Remove the specified columns
    if columns_to_remove is not None:
        dfires.drop(columns=columns_to_remove, errors="ignore", inplace=True)
    return dfires


def __format_boolean_columns_to_int(dfsrc, quiet=True):
    for col in dfsrc.columns:
        if dfsrc[col].dtype == bool:
            dfsrc[col] = dfsrc[col].astype(int)
    return dfsrc




# @title ZLC Buy and Sell v2 2210161707


def jgti_add_zlc_plus_other_AO_signal(
    dfsrc,
    dropsecondaries=True,
    quiet=True,
    rq: JGTIDSRequest = None,
):
    if rq is None:
        rq = JGTIDSRequest()

    dfsrc = _jgtpd_col_add_range_shifting(dfsrc, AO, "pao", 10)
    dfsrc = _jgtpd_col_add_range_shifting(dfsrc, AC, "pac", 4)
    if not quiet:
        print("----added shofted range AO")

    # AO Above Zero
    dfsrc[AOAZ] = (dfsrc[AO] > 0).astype(int)
    # AO Bellow Zero
    dfsrc[AOBZ] = (dfsrc[AO] < 0).astype(int)

    c = 0
    xc = len(dfsrc)
    for i, row in dfsrc.iterrows():
        c = c + 1
        cao = dfsrc.at[i, AO]  # Current AO
        cac = dfsrc.at[i, AC]  # Current AC
        pac1 = dfsrc.at[i, "pac1"]  # Past AC 1
        pac2 = dfsrc.at[i, "pac2"]  # Past AC 2
        pac3 = dfsrc.at[i, "pac3"]  # Past AC 3
        cacgreen = False
        pac1green = False
        pac2green = False
        if cac > pac1:
            cacgreen = True
        if pac1 > pac2:
            pac1green = True
        if pac2 > pac3:
            pac2green = True

        pao1 = dfsrc.at[i, "pao1"]  # Past AO 1
        pao2 = dfsrc.at[i, "pao2"]  # Past AO 2
        pao3 = dfsrc.at[i, "pao3"]  # Past AO 3
        caogreen = False
        pao1green = False
        pao2green = False
        if cao > pao1:
            caogreen = True
        if pao1 > pao2:
            pao1green = True
        if pao2 > pao3:
            pao2green = True

        # For simplicity
        caored = not caogreen
        pao1red = not pao1green
        pao2red = not pao2green

        cacred = not cacgreen
        pac1red = not pac1green
        pac2red = not pac2green

        aoaz = dfsrc.at[i, AOAZ]
        aobz = dfsrc.at[i, AOBZ]

        # ZLC
        isZLCBuy:int = 0
        isZLCSell:int = 0
        zlcCode:int = 0
        if pao1 > 0 and aobz == 1:
            zlcCode = -1
            isZLCSell = 1
        if pao1 < 0 and aoaz == 1:
            zlcCode = 1
            isZLCBuy = 1

        dfsrc.at[i, ZLC] = int(zlcCode)
        dfsrc.at[i, ZLCB] = int(isZLCBuy)
        dfsrc.at[i, ZLCS] = int(isZLCSell)

        # dfsrc[signal_zcol_column_name] = dfsrc[signal_zcol_column_name].astype(object)
        # Coloring AO
        # dfsrc['aocolor'] = dfsrc['aocolor'].astype(object)

        if rq.include_ao_color:
            if caogreen:
                dfsrc.at[i, "aocolor"] = "green"
            else:
                dfsrc.at[i, "aocolor"] = "red"

        # Coloring AC
        # dfsrc['accolor'] = dfsrc['accolor'].astype(object)
        if rq.include_ac_color:
            if cacgreen:
                dfsrc.at[i, "accolor"] = "green"
            else:
                dfsrc.at[i, "accolor"] = "red"

        # --@STCIssue Zone  (Not sure, it might have to be ABove or Bellow)

        zoneColor = nonTradingZoneColor  # default Zone Color

        redZone:int = 0
        if cacred and caored and pac1red and pao1red:
            redZone:int = 1
            zoneColor = sellingZoneColor

        greenZone:int = 0
        if cacgreen and caogreen and pac1green and pao1green:
            greenZone = 1
            zoneColor = buyingZoneColor

        dfsrc.at[i, signal_zcol_column_name] = zoneColor
        dfsrc.at[i, ZONE_SIGNAL] = int(zone_str_to_id(zoneColor))

        # Sell Zone Signal

        dfsrc.at[i, SZ] = int(redZone)

        # Buy Zone Signal
        dfsrc.at[i, BZ] = int(greenZone)

        # AC Sell / Buy  3 AC Against AO af AC Bellow, 2 if above
        acSell:int = 0
        msgacSignal = "No "
        if cacred and pac1red and caogreen and pao1green:
            acSell = 1
            if (
                cac < 0 and pac2green
            ):  # We require 3 bars red on the AC When bellow zero
                acSell = 0
        acBuy:int = 0
        if cacgreen and pac1green and caored and pao1red:
            acBuy = 1
            if cac > 0 and pac2red:
                acBuy = 0

        # AC Sell Signal (Deceleration)

        dfsrc.at[i, ACS] = int(acSell)

        # AC Buy Signal (Acceleration)
        dfsrc.at[i, ACB] = int(acBuy)

        if acSell and not quiet:
            print("AC Sell Signal with AC Bellow Zero Line " + str(i))
        if acBuy and not quiet:
            print("AC Buy Signal with AC ABove Zero Line " + str(i))

        # Saucer Strategy
        # More on Saucer Strategy : http://simp.ly/p/2K1HBr
        saucerSell:int = 0
        if cao < 0 and caored and pao1green and pao2green:
            saucerSell = 1

        saucerBuy:int = 0
        if cao > 0 and caogreen and pao1red and pao2red:
            saucerBuy = 1

        dfsrc.at[i, SS] = int(saucerSell)
        dfsrc.at[i, SB] = int(saucerBuy)

        # What Happens on the Next PLUS 35 Periods ??
        if c < xc - 35:
            cPrice = row["Close"]
    return dfsrc


