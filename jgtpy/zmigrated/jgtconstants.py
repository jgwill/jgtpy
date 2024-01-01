
"""
This module contains constant values used in JGTpy trading system. It includes colors for non-trading zone, selling zone, and buying zone. It also includes a list of columns to remove, column names for various indicators, and signal data frame columns naming.
"""
nonTradingZoneColor = 'gray'

sellingZoneColor = 'red'
buyingZoneColor = 'green'

open_column_name = 'Open'
close_column_name = 'Close'
high_column_name = 'High'
low_column_name = 'Low'
OPEN=open_column_name
CLOSE=close_column_name
HIGH=high_column_name
LOW=low_column_name

bidopen_column_name = 'BidOpen'
bidhigh_column_name = 'BidHigh'
bidlow_column_name = 'BidLow'
bidclose_column_name = 'BidClose'
BIOPEN=bidopen_column_name
BIDHIGH=bidhigh_column_name
BIDLOW=bidlow_column_name
BIDCLOSE=bidclose_column_name

askopen_column_name = 'AskOpen'
askclose_column_name = 'AskClose'
askhigh_column_name = 'AskHigh'
asklow_column_name = 'AskLow'
ASKOPEN=askopen_column_name
ASKCLOSE=askclose_column_name
ASKHIGH=askhigh_column_name
ASKLOW=asklow_column_name

median_column_name = 'Median'
volume_column_name = 'Volume'
date_column_name = 'Date'
bar_height_column_name= "bar_height"
MEDIAN=median_column_name
VOLUME=volume_column_name
DATE=date_column_name
BAR_HEIGHT=bar_height_column_name


# List of columns to remove
columns_to_remove = ['aofvalue', 'aofhighao', 'aoflowao', 'aofhigh', 'aoflow', 'aocolor', 'accolor','fdbbhigh','fdbblow','fdbshigh','fdbslow']

indicator_currentDegree_alligator_jaw_column_name = 'jaw' # 13 periods moving average, shifted 8 bars into the future
indicator_currentDegree_alligator_teeth_column_name = 'teeth' # 8 periods moving average, shifted 5 bars into the future
indicator_currentDegree_alligator_lips_column_name = 'lips' # 5 periods moving average, shifted 3 bars into the future
JAW=indicator_currentDegree_alligator_jaw_column_name
TEETH=indicator_currentDegree_alligator_teeth_column_name
LIPS=indicator_currentDegree_alligator_lips_column_name

indicator_sixDegreeLarger_alligator_jaw_column_name = 'bjaw' # 89 periods moving average, shifted 55 bars into the future
indicator_sixDegreeLarger_alligator_teeth_column_name = 'bteeth' # 55 periods moving average, shifted 34 bars into the future
indicator_sixDegreeLarger_alligator_lips_column_name = 'blips' # 34 periods moving average, shifted 21 bars into the future
BJAW=indicator_sixDegreeLarger_alligator_jaw_column_name
BTEETH=indicator_sixDegreeLarger_alligator_teeth_column_name
BLIPS=indicator_sixDegreeLarger_alligator_lips_column_name

indicator_AO_awesomeOscillator_column_name = 'ao' # AO measure energy of momentum
indicator_AC_accelerationDeceleration_column_name = 'ac' # AC measure speed of momentum
AO=indicator_AO_awesomeOscillator_column_name
AC=indicator_AC_accelerationDeceleration_column_name

indicator_AO_aboveZero_column_name = 'aoaz'
indicator_AO_bellowZero_column_name = 'aobz'
indicator_zeroLineCross_column_name = 'zlc'
AOAZ=indicator_AO_aboveZero_column_name
AOBZ=indicator_AO_bellowZero_column_name
ZLC=indicator_zeroLineCross_column_name

indicator_gatorOscillator_low_column_name = 'gl' # Gator Oscillator low
indicator_gatorOscillator_high_column_name = 'gh' # Gator Oscillator high
GL=indicator_gatorOscillator_low_column_name
GH=indicator_gatorOscillator_high_column_name


indicator_mfi_marketFacilitationIndex_column_name = 'mfi' # MFI measure market facilitation index
MFI=indicator_mfi_marketFacilitationIndex_column_name
    

#Various fractal degrees
indicator_fractal_high_degree2_column_name="fh" # Fractal High of degree 2
indicator_fractal_low_degree2_column_name="fl" # Fractal Low of degree 2
indicator_fractal_high_degree3_column_name="fh3" # Fractal High of degree 3
indicator_fractal_low_degree3_column_name="fl3" # Fractal Low of degree 3
indicator_fractal_high_degree5_column_name="fh5" # Fractal High of degree 5
indicator_fractal_low_degree5_column_name="fl5" # Fractal Low of degree 5
indicator_fractal_high_degree8_column_name="fh8" # Fractal High of degree 8
indicator_fractal_low_degree8_column_name="fl8" # Fractal Low of degree 8
indicator_fractal_high_degree13_column_name="fh13" # Fractal High of degree 13
indicator_fractal_low_degree13_column_name="fl13" # Fractal Low of degree 13
indicator_fractal_high_degree21_column_name="fh21" # Fractal High of degree 21
indicator_fractal_low_degree21_column_name="fl21" # Fractal Low of degree 21
indicator_fractal_high_degree34_column_name="fh34" # Fractal High of degree 34
indicator_fractal_low_degree34_column_name="fl34" # Fractal Low of degree 34
indicator_fractal_high_degree55_column_name="fh55" # Fractal High of degree 55
indicator_fractal_low_degree55_column_name="fl55" # Fractal Low of degree 55
indicator_fractal_high_degree89_column_name="fh89" # Fractal High of degree 89
indicator_fractal_low_degree89_column_name="fl89" # Fractal Low of degree 89

FH = indicator_fractal_high_degree2_column_name
FL = indicator_fractal_low_degree2_column_name
FH3 = indicator_fractal_high_degree3_column_name
FL3 = indicator_fractal_low_degree3_column_name
FH5 = indicator_fractal_high_degree5_column_name
FL5 = indicator_fractal_low_degree5_column_name
FH8 = indicator_fractal_high_degree8_column_name
FL8 = indicator_fractal_low_degree8_column_name
FH13 = indicator_fractal_high_degree13_column_name
FL13 = indicator_fractal_low_degree13_column_name
FH21 = indicator_fractal_high_degree21_column_name
FL21 = indicator_fractal_low_degree21_column_name
FH34 = indicator_fractal_high_degree34_column_name
FL34 = indicator_fractal_low_degree34_column_name
FH55 = indicator_fractal_high_degree55_column_name
FL55 = indicator_fractal_low_degree55_column_name
FH89 = indicator_fractal_high_degree89_column_name
FL89 = indicator_fractal_low_degree89_column_name


indicator_ao_fractalPeakOfMomentum_column_name = 'aof'
indicator_ao_fractalPeakValue_column_name = 'aofvalue'
# %%
#@title SIGNAL's Data Frame Columns naming

# fractal divergent bar signals (or BDB)
signalCode_fractalDivergentBar_column_name = 'fdb' # Fractal Divergent Bar Code (contains the signal value either buy, sell or nothing)
signalSell_fractalDivergentBar_column_name = 'fdbs' # Fractal Divergent Bar Sell
signalBuy_fractalDivergentBar_column_name = 'fdbb' # Fractal Divergent Bar Buy

#ac
signalSell_AC_deceleration_column_name = 'acs'
signalBuy_AC_acceleration_column_name = 'acb'

#Fractal signal
signalSell_fractal_column_name = 'fs'
signalBuy_fractal_column_name = 'fb'

#Zero Line Cross Signal
signalBuy_zeroLineCrossing_column_name = 'zlcb'
signalSell_zeroLineCrossing_column_name = 'zlcs'
signal_zcol_column_name = 'zcol' # NOT SURE its a signal

signalSell_zoneSignal_column_name = 'sz'
signalBuy_zoneSinal_column_name = 'bz'

# Saucer signal
signalSell_saucer_column_name = 'ss'
signalBuy_saucer_column_name = 'sb'

# New variables assigned with capitalized names
AOF = indicator_ao_fractalPeakOfMomentum_column_name
AOFVALUE = indicator_ao_fractalPeakValue_column_name
FDB = signalCode_fractalDivergentBar_column_name
FDBB = signalBuy_fractalDivergentBar_column_name
FDBS = signalSell_fractalDivergentBar_column_name
ACS = signalSell_AC_deceleration_column_name
ACB = signalBuy_AC_acceleration_column_name
FS = signalSell_fractal_column_name
FB = signalBuy_fractal_column_name
ZLCB = signalBuy_zeroLineCrossing_column_name
ZLCS = signalSell_zeroLineCrossing_column_name
ZCOL = signal_zcol_column_name
SZ = signalSell_zoneSignal_column_name
BZ = signalBuy_zoneSinal_column_name
SS = signalSell_saucer_column_name
SB = signalBuy_saucer_column_name

PRICE_PEAK_ABOVE = 'price_peak_above'
AO_PEAK_ABOVE = 'ao_peak_above'
PRICE_PEAK_BELLOW = 'price_peak_bellow'
AO_PEAK_BELLOW = 'ao_peak_bellow'
