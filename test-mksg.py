# %% Imports

import os
from jgtpy import mksg

instrument = "SPX500"
timeframes = "M1,W1,D1,H8,H4,H1,m15,m5"
timeframes = "M1,W1,D1,H4,H1,m15"
scntlid = "240209"
scntlid = "221013"
scn_root_dir = f"/b/Dropbox/jgt/drop/data/scn/SPX500_{scntlid}"

scn_jgtpy_data = os.path.join(scn_root_dir, "data")
os.environ["JGTPY_DATA"] = scn_jgtpy_data

scn_chart_dir = os.path.join(scn_root_dir, "charts")
os.makedirs(scn_chart_dir, exist_ok=True)

# %% Show the data directory
print(os.environ["JGTPY_DATA"])

# %% crop_last_dt
crop_last_dt = "2022-10-13 13:45:00"

mksg.generate_market_snapshots(
    instrument,
    timeframes,
    scn_chart_dir,
    show_chart=False,
    show_tabs=False,
    width=2550,
    height=1150,
    crop_last_dt=crop_last_dt,
)


# %%


# %% Plot timeframes of the data using mksg

mksg.generate_market_snapshots(
    instrument,
    timeframes,
    scn_chart_dir,
    show_chart=False,
    show_tabs=False,
    width=2550,
    height=1150,
)
