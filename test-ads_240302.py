# %% Import packages
from jgtpy import JGTADS as ads
from jgtpy import JGTPDSP as pds
from jgtpy import JGTChartConfig
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

print(os.getenv("JGTPY_DATA"))


i = "GBP/USD"
# t="D1" #Where we look for signals
instrument = i

timeframes = "M1,W1,D1,H8,H4"
tf_of_signal = "H8"
tf_of_signal = "D1"

dt_of_signal = "2023-07-15 09:00"

chart,ax,_= ads.plot(i,"H4",crop_last_dt=dt_of_signal,show=False)


# %%
