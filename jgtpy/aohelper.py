

import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from JGTPDHelper import jgtpd_drop_col_by_name
from jgtutils import jgtconstants as c

from JGTIDSRequest import JGTIDSRequest

peak_distance = 13  #distance: Set this to the number of periods that define the minimum peak separation. To meet the 5-8 bar criterion, set distance=5.
peak_width=8 #width: This parameter could be used to define the minimum width of the peak in terms of bars. However, for AO and price peaks, the distance parameter may suffice to ensure the peak duration you are seeking. This parameter is optional and can be set or omitted based on the specific requirements.

def pto_add_ao_price_peaks(data: pd.DataFrame,quiet=True,rq: JGTIDSRequest = None,
):
    if rq is None:
        rq = JGTIDSRequest()
    try:
        data.reset_index(inplace=True)
    except:
        pass
    
    peak_distance=rq.peak_distance
    peak_width=rq.peak_width
    peak_divider_min_height = rq.peak_divider_min_height
    
    data['ao_above'] = data['ao'].apply(lambda x: x if x > 0 else 0)
    data['ao_bellow'] = data['ao'].apply(lambda x: x if x < 0 else 0)
    data['ao_bellow'] = data['ao_bellow'] * -1
    data['price_bellow'] = data['Close'] * -1
    #data.to_csv('criss.csv')
    
    #data['ao'] = data['ao'] * -1
    # data['Close'] = data['Close'] * -1
    # data['Open'] = data['Open'] * -1
    # data['Low'] = data['Low'] * -1
    # data['High'] = data['High'] * -1


    #%% #@STCGoal Determine the Awesome Oscillator (AO) min peaks height
    ao_above_min = data['ao_above'].min()
    ao_above_max = data['ao_above'].max()
    ao_bellow_min = data['ao_bellow'].min()
    ao_bellow_max = data['ao_bellow'].max()

    
    above_min_peak_height = ao_above_max / peak_divider_min_height
    bellow_min_peak_height= ao_bellow_max / peak_divider_min_height

    if not quiet:
        print(f"Above min: {ao_above_min} max: {ao_above_max}")
        print(f"Bellow min: {ao_bellow_min} max: {ao_bellow_max}")
        print(f"Above min peak height: {above_min_peak_height} Bellow min peak height: {bellow_min_peak_height}")

    #%% Find Peaks arguments Tweeks
    peak_height_bellow = bellow_min_peak_height 
    peak_height_above = above_min_peak_height # To ensure peaks are above/below the zero-line, set the height parameter accordingly. For AO peaks, you'd set a minimum height above zero for bullish peaks or a maximum height below zero for bearish peaks. For price peaks, the height can be set relative to a reference level or omitted if not required.

    #%% Find peaks in AO Above

    ao_peaks_above, _ = find_peaks(data['ao_above'],height=peak_height_above,distance=peak_distance,width=peak_width)

    #%% Find peaks in AO Bellow

    ao_peaks_bellow, _ = find_peaks(data['ao_bellow'],height=peak_height_bellow,distance=peak_distance,width=peak_width)


    # Find peaks in price
    price_peaks_above, _ = find_peaks(data['Close'],distance=peak_distance,width=peak_width)

    price_peaks_bellow, _ = find_peaks(data['price_bellow'],distance=peak_distance,width=peak_width)

    #%% View Peaks 
    
    
    if not quiet:
        print(ao_peaks_above)
        print(ao_peaks_bellow)
        print(price_peaks_above)
        print(price_peaks_bellow)
    
    #%% Add Price Above Peaks to the dataframe

    data['price_peak_above'] = np.zeros(len(data), dtype=int)

    for p in price_peaks_above:
        data.loc[p, 'price_peak_above'] = 1


    #%% Add Price Bellow Peaks to the dataframe

    data['price_peak_bellow'] = np.zeros(len(data), dtype=int)

    for p in price_peaks_bellow:
        data.loc[p, 'price_peak_bellow'] = 1

    #%% ADd Above Peaks to the data frame
    data['ao_peak_above'] = np.zeros(len(data), dtype=int)

    for p in ao_peaks_above:
        data.loc[p, 'ao_peak_above'] = 1
        
    #%% ADd Bellow Peaks to the data frame
    data['ao_peak_bellow'] = np.zeros(len(data), dtype=int)

    for p in ao_peaks_bellow:
        data.loc[p, 'ao_peak_bellow'] = 1 

    
    #Cleanup
    data = jgtpd_drop_col_by_name(data,'ao_bellow',1,True)
    data = jgtpd_drop_col_by_name(data,'ao_above',1,True)
    data = jgtpd_drop_col_by_name(data,'price_bellow',1,True)
    
    try:
        data.set_index('Date', inplace=True)
    except:
        pass
    return data
