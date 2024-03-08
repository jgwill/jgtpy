# %% Imports

import os
from jgtpy import mksg
import tlid
from jgtpy import JGTChartConfig
import panel as pn


default_char_dir_name = "charts"

cc = JGTChartConfig.JGTChartConfig()  # Assuming JGTChartConfig is a class, initialize it
show_chart = False
show_tabs = False
save_fig_image = True
save_cds_data = False




instrument = "SPX500"
instrument = "GBP/USD"

timeframes = "M1,W1,D1,H8,H4,H1,m15,m5"
timeframes = "M1,W1,D1,H4,H1,m15"
timeframes = "M1,W1,D1,H8,H4"
timeframes = "M1,W1,D1,H4"
tf_of_signal = "H4"
tf_of_signal = "D1"
sig_type_name = "fdbs"





# %%


scn_root_dir = "/var/lib/jgt/full"

scn_jgtpy_data = os.path.join(scn_root_dir, "data")

os.environ["JGTPY_DATA"] = scn_jgtpy_data
os.environ["JGTPY_DATA_FULL"] = scn_jgtpy_data
# %% Show the data directory
print(os.environ["JGTPY_DATA"])



out_htm_viewer_full_fn= "index.html"
out_htm_viewer_prefix="index-"
w = 2550
h = 1150

#-----------------------------------------------



#generate_market_snapshots_for_many_crop_dt
crop_last_dates = ["2023-07-13 21:00","2023-10-15 21:00","2023-12-13 21:00"]  # D1 FDBS Signal (PROFIT)
crop_last_dates = ["2023-07-15 09:00","2023-07-16 09:00","2023-10-17 21:00","2023-11-05 21:00","2023-12-13 21:00"]  # H8 FDBS Signal (PROFIT)
crop_last_dates = ["2023-07-15 09:00","2023-10-17 21:00","2023-11-05 21:00"]  # H8 FDBS Signal (PROFIT)
# mksg.generate_market_snapshots_for_many_crop_dt(i, timeframes, crop_last_dates, scn_root_dir, cc, show_chart, show_tabs, w, h, save_fig_image, save_cds_data, out_htm_viewer_prefix, default_char_dir_name, scn_chart_dir, out_htm_viewer_full_fn, "JGTPY_DATA_FULL")




ptabs=mksg.pto_generate_snapshot_240302_v2_by_crop_dates(
    i=instrument,
    timeframes=timeframes,
    tf_of_signal=tf_of_signal,
    sig_type_name=sig_type_name,
    crop_last_dt_arr=crop_last_dates,
    scn_root_dir=scn_root_dir,
    default_char_dir_name=default_char_dir_name,
    cc=cc,
    show_chart=show_chart,
    show_tabs=show_tabs,
    save_fig_image=save_fig_image,
    save_cds_data=save_cds_data,
    out_htm_viewer_full_fn=out_htm_viewer_full_fn,
    out_htm_viewer_prefix=out_htm_viewer_prefix,
    w=w,
    h=h
)

# %%
pn.extension()
ptabs.servable()
# %%
