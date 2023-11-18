
"""
This module contains constant values used in JGTpy trading system. It includes colors for non-trading zone, selling zone, and buying zone. It also includes a list of columns to remove, column names for various indicators, and signal data frame columns naming.
"""
nonTradingZoneColor = 'gray'

sellingZoneColor = 'red'
buyingZoneColor = 'green'

# List of columns to remove
columns_to_remove = ['aofvalue', 'aofhighao', 'aoflowao', 'aofhigh', 'aoflow', 'aocolor', 'accolor','fdbbhigh','fdbblow','fdbshigh','fdbslow']

indicator_currentDegree_alligator_jaw_column_name = 'jaw' # 13 periods moving average, shifted 8 bars into the future
indicator_currentDegree_alligator_teeth_column_name = 'teeth' # 8 periods moving average, shifted 5 bars into the future
indicator_currentDegree_alligator_lips_column_name = 'lips' # 5 periods moving average, shifted 3 bars into the future
indicator_sixDegreeLarger_alligator_jaw_column_name = 'bjaw' # 89 periods moving average, shifted 55 bars into the future
indicator_sixDegreeLarger_alligator_teeth_column_name = 'bteeth' # 55 periods moving average, shifted 34 bars into the future
indicator_sixDegreeLarger_alligator_lips_column_name = 'blips' # 34 periods moving average, shifted 21 bars into the future

indicator_AO_awesomeOscillator_column_name = 'ao' # AO measure energy of momentum
indicator_AC_accelerationDeceleration_column_name = 'ac' # AC measure speed of momentum
indicator_AO_aboveZero_column_name = 'aoaz'
indicator_AO_bellowZero_column_name = 'aobz'
indicator_zeroLineCross_column_name = 'zlc'

indicator_gatorOscillator_low_column_name = 'gl' # Gator Oscillator low
indicator_gatorOscillator_high_column_name = 'gh' # Gator Oscillator high


indicator_mfi_marketFacilitationIndex_column_name = 'mfi' # MFI measure market facilitation index
    
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






