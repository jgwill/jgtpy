# %% Imports

import os
from jgtpy import mksg
import tlid
from jgtpy import JGTChartConfig


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
tf_of_signal = "D1"
sig_type_name = "fdbs"

scntlid = "240209"
scntlid = "221013"


crop_last_dt = "2023-07-13 21:00"  # FDBS Signal

# %%

arch_chart_dir = "/var/lib/jgt/full/data/pto"
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

def pto_generate_snapshot_240302(
    i: str,
    timeframes: str,
    tf_of_signal: str,
    sig_type_name: str,
    crop_last_dt: str = None,
    scn_root_dir: str = None,
    default_char_dir_name: str = "charts",
    show_chart: bool = False,
    show_tabs: bool = False,
    save_fig_image: bool = True,
    save_cds_data: bool = True,
    out_htm_viewer_full_fn: str = "index.html",
    out_htm_viewer_prefix: str = "_index-",
    w: int = 2550,
    h: int = 1150,
    cc: JGTChartConfig.JGTChartConfig = None
):
    if cc is None:
        cc = JGTChartConfig.JGTChartConfig()
    scntlid = tlid.strdt(crop_last_dt)
    scntlid
    ifn = i.replace("/", "-")
    subdir_scene_name = f"{ifn}_{tf_of_signal}_{sig_type_name}_{scntlid}"  # GBP-USD_2307132100

    if scn_root_dir is None:
        scn_root_dir = os.environ["JGTPY_DATA_FULL"]
    
    scn_chart_dir = os.path.join(os.path.join(scn_root_dir,  default_char_dir_name), subdir_scene_name)
    os.makedirs(scn_chart_dir, exist_ok=True)
    
    
    mksg.generate_market_snapshots(
    instruments=instrument,
    timeframes=timeframes,
    html_outdir_root=scn_chart_dir,
    width=w,
    height=h,
    cc=cc,
    show_chart=show_chart,
    show_tabs=show_tabs,
    save_fig_image=save_fig_image,
    save_cds_data=save_cds_data,
    crop_last_dt=crop_last_dt,
    out_htm_viewer_prefix=out_htm_viewer_prefix,
    out_htm_viewer_full_fn=out_htm_viewer_full_fn #@STCGoal Expecting to be able to add many cropped DTs to the same file
)


#%% Exec


pto_generate_snapshot_240302(
    i=instrument,
    timeframes=timeframes,
    tf_of_signal=tf_of_signal,
    sig_type_name=sig_type_name,
    crop_last_dt=crop_last_dt,
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


# %% #@STCGoal Much later when there Were Profits 

crop_last_dt = "2023-07-13 21:00"  # FDBS Signal (ORIGINAL)
crop_last_dt = "2023-12-13 21:00"  # FDBS Signal (PROFIT)

pto_generate_snapshot_240302(
    i=instrument,
    timeframes=timeframes,
    tf_of_signal=tf_of_signal,
    sig_type_name=sig_type_name,
    crop_last_dt=crop_last_dt,
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

#%%
