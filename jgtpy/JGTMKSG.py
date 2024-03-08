
# %% Imports
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import panel as pn

import matplotlib.pyplot as plt

plt.rcParams["figure.max_open_warning"] = 100

import pandas as pd
from jgtpy import JGTADS as ads, adshelper as ah, JGTPDSP as pds, JGTCDS as cds
from jgtpy import JGTChartConfig

import tlid

#%% Creating a default chart configuration
def create_default_chart_config():
    cc = JGTChartConfig.JGTChartConfig()
    cc.saucer_marker_size = 14
    cc.ac_signals_marker_size = 14
    cc.fig_ratio_x = 31
    cc.fig_ratio_y = 16
    cc.nb_bar_on_chart = 300
    cc.plot_style = "yahoo"
    return cc
  
#%% Pto Panel 240209


#support crop_last_dt="2022-10-13 13:45:00"

def generate_market_snapshots(instruments:str, timeframes:str, html_outdir_root:str=None,cc:JGTChartConfig.JGTChartConfig=None,crop_last_dt:str=None, show_chart:bool=False, show_tabs:bool=False,width:int=2550, height:int=1150,save_fig_image:bool=True,save_cds_data:bool=True,out_htm_viewer_prefix = "pto-mksg-",default_char_dir_name = "charts",default_chart_output_dir = "./",out_htm_viewer_ext = ".html",out_htm_viewer_full_fn= "pto-all-mksg.html",
  serve_it=False):
  """
  Generates market snapshots for the given instruments and timeframes.

  Parameters:
  - instruments (str): Comma-separated string of instrument names.
  - timeframes (str): Comma-separated string of timeframes.
  - html_outdir_root (str, optional): Root directory for HTML output. If not provided, a default directory will be used.
  - cc (JGTChartConfig.JGTChartConfig, optional): Chart configuration object. If not provided, a default configuration will be used.
  - crop_last_dt (str, optional): Date and time to crop the snapshots. If not provided, all data will be included.
  - show_chart (bool, optional): Whether to show the chart. Default is False.
  - show_tabs (bool, optional): Whether to show the tabs. Default is False.
  - width (int, optional): Width of the snapshots. Default is 2550.
  - height (int, optional): Height of the snapshots. Default is 1150.
  - save_fig_image (bool, optional): Whether to save the figure images. Default is True.
  - save_cds_data (bool, optional): Whether to save the CDS data. Default is True.
  - out_htm_viewer_prefix (str, optional): Prefix for the HTML viewer output. Default is "pto-mksg-".
  - default_char_dir_name (str, optional): Default directory name for charts. Default is "charts".
  - default_chart_output_dir (str, optional): Default output directory for charts. Default is "./".
  - out_htm_viewer_ext (str, optional): Extension for the HTML viewer output. Default is ".html".
  - out_htm_viewer_full_fn (str, optional): Full filename for the HTML viewer output. Default is "pto-all-mksg.html".
  - serve_it (bool, optional): Whether to serve the output. Default is False.

  Returns:
  - ptabs (pn.Tabs): A `pn.Tabs` object containing the generated market snapshots.
  """
  if cc is None:
    cc = create_default_chart_config()
  
  if html_outdir_root is None:
    # Read the environment variable
    jgtpy_data_dir = os.environ.get("JGTPY_DATA")

    # Check if the environment variable is set
    if jgtpy_data_dir is not None:
      # Join the environment variable with "charts" to create a new directory path
      
      scn_chart_dir = os.path.join(jgtpy_data_dir, default_char_dir_name)
      
      # Create the directory if it doesn't exist
      os.makedirs(scn_chart_dir, exist_ok=True)
      
      # Set html_outdir_root to the new directory
      html_outdir_root = scn_chart_dir
    else:
      print("Environment variable JGTPY_DATA is not set. Default to ./charts.")
      
      html_outdir_root = os.path.join(default_chart_output_dir,default_char_dir_name)
  timeframes = timeframes.split(",")
  perspectives = {}
  ptabs = pn.Tabs(width=width, height=height)

  for i in instruments.split(","):
    ifn=i.replace("/", "-")
    try:
      print(f"-------------{i}-------------------")

      figures = {}
      success = False
      for t in timeframes:
        print(i, t)
        f, ax, _ = ads.plot(i, t, show=show_chart, cc=cc, crop_last_dt=crop_last_dt,plot_ao_peaks=True)
        f.title = t
        figures[t] = f
        fnout, fnoutcsv = _mk_fnoutputs(html_outdir_root, i, t)
        
        if save_fig_image:        
          f.savefig(fnout)
        if save_cds_data:
          _.to_csv(fnoutcsv)

      tabs = pn.Tabs(width=width, height=height)

      for t in timeframes:
        tabs.append((t, figures[t]))

      if show_tabs:
        tabs.show()
        
      
      if crop_last_dt is not None:
        #cldt_fnstr=crop_last_dt.replace("/","-").replace(" ","_").replace(":","") 
        cldt_fnstr=tlid.strdt(crop_last_dt)
        tabs.title = i + " - " + crop_last_dt
        
        html_fname = ifn+"_"+ cldt_fnstr + out_htm_viewer_ext
        
      else:
        cldt_fnstr =tlid.get_minutes()
        tabs.title = i
        html_fname = ifn + out_htm_viewer_ext
        
      html_fname=html_fname.replace("..",".")
      print(html_fname)
      
      html_output_filepath = f"{html_outdir_root}/{out_htm_viewer_prefix}" + html_fname

      tabs.save(html_output_filepath, embed=True)

      perspectives[i] = tabs

      ptabs.append((i, tabs))
    except:
      print("An error occurred while processing:", i)
      pass
  
  full_html_output_filepath = f"{html_outdir_root}/{out_htm_viewer_full_fn}"
  print(full_html_output_filepath)

  ptabs.save(full_html_output_filepath, embed=True)
  print("Saved:", full_html_output_filepath)

  if serve_it:
    pn.extension()
    ptabs.servable()
  return ptabs

def _mk_fnoutputs(html_outdir_root, i, t,crop_last_dt=None):
    _suffix = ""
    if crop_last_dt is not None:
      _suffix = "_"+tlid.strdt(crop_last_dt)
    povfn = i.replace("/", "-") + "_" + t
    fnout = html_outdir_root + "/" + povfn +_suffix + ".png"
    fnoutcsv = html_outdir_root + "/" + povfn + _suffix+ ".cds.csv"
    return fnout,fnoutcsv


#%% For Many Crop DT Last


def generate_market_snapshots_for_many_crop_dt(i:str, timeframes, crop_last_dt_arr, html_outdir_root:str=None, cc:JGTChartConfig.JGTChartConfig=None, show_chart:bool=False, show_tabs:bool=False, width:int=2550, height:int=1150, save_fig_image:bool=True, save_cds_data:bool=True, out_htm_viewer_prefix="pto-mksg-bycrop-", default_char_dir_name="charts", default_chart_output_dir="./", out_htm_viewer_ext=".html", out_htm_viewer_full_fn="pto-all-mksg-bycrop.html", jgtpy_data_var="JGTPY_DATA_FULL", tf_of_signal:str=None, dt_of_signal:str=None, sig_type_name:str="",serve_it=False):
  """
  Generates market snapshots for multiple crop dates and timeframes.

  Args:
    i (str): The input string.
    timeframes: The list of timeframes.
    crop_last_dt_arr: The list of crop last dates.
    html_outdir_root (str, optional): The root directory for HTML output. Defaults to None.
    cc (JGTChartConfig.JGTChartConfig, optional): The chart configuration. Defaults to None.
    show_chart (bool, optional): Whether to show the chart. Defaults to False.
    show_tabs (bool, optional): Whether to show the tabs. Defaults to False.
    width (int, optional): The width of the tabs. Defaults to 2550.
    height (int, optional): The height of the tabs. Defaults to 1150.
    save_fig_image (bool, optional): Whether to save the figure image. Defaults to True.
    save_cds_data (bool, optional): Whether to save the CDS data. Defaults to True.
    out_htm_viewer_prefix (str, optional): The prefix for the HTML viewer output. Defaults to "pto-mksg-bycrop-".
    default_char_dir_name (str, optional): The default chart directory name. Defaults to "charts".
    default_chart_output_dir (str, optional): The default chart output directory. Defaults to "./".
    out_htm_viewer_ext (str, optional): The extension for the HTML viewer output. Defaults to ".html".
    out_htm_viewer_full_fn (str, optional): The full filename for the HTML viewer output. Defaults to "pto-all-mksg-bycrop.html".
    jgtpy_data_var (str, optional): The JGTPY data variable. Defaults to "JGTPY_DATA_FULL".
    tf_of_signal (str, optional): The timeframe of the signal. Defaults to None.
    dt_of_signal (str, optional): The date of the signal. Defaults to None.
    sig_type_name (str, optional): The name of the signal type. Defaults to "".
    serve_it (bool, optional): Whether to serve the output. Defaults to False.
  Returns:
    pn.Tabs: The generated market snapshots as a panel of tabs.
  """
  if cc is None:
    cc = create_default_chart_config()

  html_outdir_root = _mk_html_outdir_root_default(html_outdir_root, default_char_dir_name, default_chart_output_dir, jgtpy_data_var)

  if isinstance(timeframes, str):
    timeframes = timeframes.split(",")

  perspectives = {}
  ptabs = pn.Tabs(width=width, height=height)

  # If crop_last_dt_arr is type string, split
  if isinstance(crop_last_dt_arr, str):
    crop_last_dt_arr = crop_last_dt_arr.split(",")

  # Assume dt_of_signal is the first of the array
  if dt_of_signal is None:
    dt_of_signal = crop_last_dt_arr[0]

  for crop_last_dt in crop_last_dt_arr:
    ifn = i.replace("/", "-")
    try:
      print(f"-------------{i}-------------------")

      figures = {}
      success = False

      # We add one tag with the signal TF

      for t in timeframes:
        print(i, t, crop_last_dt)
        f, ax, _ = ads.plot(i, t, show=show_chart, cc=cc, crop_last_dt=crop_last_dt, plot_ao_peaks=True)
        f.title = t
        figures[t] = f
        fnout, fnoutcsv = _mk_fnoutputs(html_outdir_root, i, t, crop_last_dt)

        if save_fig_image:
          f.savefig(fnout)
        if save_cds_data:
          _.to_csv(fnoutcsv)

      tabs = pn.Tabs(width=width, height=height)

      if tf_of_signal is not None:
        first_tab_name = tf_of_signal + "s"
        tabs.append((first_tab_name, figures[tf_of_signal]))

      for t in timeframes:
        tabs.append((t, figures[t]))

      if show_tabs:
        tabs.show()

      cldt_fnstr = tlid.strdt(crop_last_dt)
      # tabs.title = i + " - " + crop_last_dt
      tabs.title = cldt_fnstr

      html_fname = ifn + "_" + cldt_fnstr + out_htm_viewer_ext
      _sig_type_str = ""
      if sig_type_name != "":
        _sig_type_str = " " + sig_type_name + " "
      html_title_name = i + " " + tf_of_signal + _sig_type_str + crop_last_dt

      html_fname = html_fname.replace("..", ".")
      print(html_fname)

      html_output_filepath = f"{html_outdir_root}/{out_htm_viewer_prefix}" + html_fname

      tabs.save(html_output_filepath, title=html_title_name, embed=True)

      perspectives[i] = tabs

      tabstitle = tf_of_signal + " " + crop_last_dt
      ptabs.append((tabstitle, tabs))

    except:
      print("An error occurred while processing:", i)
      pass

  full_html_title_name = i + " " + tf_of_signal + " " + sig_type_name + " " + dt_of_signal

  full_html_output_filepath = f"{html_outdir_root}/{out_htm_viewer_full_fn}"
  print(full_html_output_filepath)

  ptabs.save(full_html_output_filepath, title=full_html_title_name, embed=True)
  print("Crop by DT Saved:", full_html_output_filepath)

  if serve_it:
    pn.extension()
    ptabs.servable()
  return ptabs
  






def pto_generate_snapshot_240302_v2_by_crop_dates(
  i: str,
  timeframes: str,
  tf_of_signal: str,
  sig_type_name: str,
  crop_last_dt_arr,
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
  cc: JGTChartConfig.JGTChartConfig = None,
  serve_it=False
):
  """
  Generate market snapshots for multiple crop dates.

  Args:
    i (str): The input parameter.
    timeframes (str): The timeframes parameter.
    tf_of_signal (str): The tf_of_signal parameter.
    sig_type_name (str): The sig_type_name parameter.
    crop_last_dt_arr: The crop_last_dt_arr parameter.
    scn_root_dir (str, optional): The scn_root_dir parameter. Defaults to None.
    default_char_dir_name (str, optional): The default_char_dir_name parameter. Defaults to "charts".
    show_chart (bool, optional): The show_chart parameter. Defaults to False.
    show_tabs (bool, optional): The show_tabs parameter. Defaults to False.
    save_fig_image (bool, optional): The save_fig_image parameter. Defaults to True.
    save_cds_data (bool, optional): The save_cds_data parameter. Defaults to True.
    out_htm_viewer_full_fn (str, optional): The out_htm_viewer_full_fn parameter. Defaults to "index.html".
    out_htm_viewer_prefix (str, optional): The out_htm_viewer_prefix parameter. Defaults to "_index-".
    w (int, optional): The width parameter. Defaults to 2550.
    h (int, optional): The height parameter. Defaults to 1150.
    cc (JGTChartConfig.JGTChartConfig, optional): The cc parameter. Defaults to None.
    serve_it (bool, optional): The serve_it parameter. Defaults to False.
  Returns:
    The result of calling the `generate_market_snapshots_for_many_crop_dt` function.
  """
  if cc is None:
    cc = JGTChartConfig.JGTChartConfig()
  
  #if crop_last_dt_arr is type string, split
  if isinstance(crop_last_dt_arr, str):
    crop_last_dt_arr = crop_last_dt_arr.split(",")
  crop_last_dt_MAIN = crop_last_dt_arr[0] # First crop date will define our target output dir
  scntlid = tlid.strdt(crop_last_dt_MAIN)
  scntlid
  ifn = i.replace("/", "-")
  subdir_scene_name = f"{ifn}_{tf_of_signal}_{sig_type_name}_{scntlid}"  # GBP-USD_2307132100

  if scn_root_dir is None:
    scn_root_dir = os.environ["JGTPY_DATA_FULL"]
  
  scn_chart_dir = os.path.join(os.path.join(scn_root_dir,  default_char_dir_name), subdir_scene_name)
  os.makedirs(scn_chart_dir, exist_ok=True)
  
  
  return generate_market_snapshots_for_many_crop_dt(
  i=i,
  timeframes=timeframes,
  crop_last_dt_arr=crop_last_dt_arr,
  tf_of_signal=tf_of_signal,
  html_outdir_root=scn_chart_dir,
  width=w,
  height=h,
  cc=cc,
  show_chart=show_chart,
  show_tabs=show_tabs,
  save_fig_image=save_fig_image,
  save_cds_data=save_cds_data,
  out_htm_viewer_prefix=out_htm_viewer_prefix,
  out_htm_viewer_full_fn=out_htm_viewer_full_fn, #@STCGoal Expecting to be able to add many cropped DTs to the same file
  sig_type_name=sig_type_name,
  serve_it=serve_it
)












def _mk_html_outdir_root_default(html_outdir_root, default_char_dir_name, default_chart_output_dir, jgtpy_data_var):
    if html_outdir_root is None:
    # Read the environment variable
      jgtpy_data_dir = os.environ.get(jgtpy_data_var)

    # Check if the environment variable is set
      if jgtpy_data_dir is not None:
      # Join the environment variable with "charts" to create a new directory path
        scn_chart_dir = os.path.join(jgtpy_data_dir, default_char_dir_name)
      
      # Create the directory if it doesn't exist
        os.makedirs(scn_chart_dir, exist_ok=True)
      
      # Set html_outdir_root to the new directory
        html_outdir_root = scn_chart_dir
      else:
        print("Environment variable JGTPY_DATA is not set. Default to ./charts.")
      
        html_outdir_root = os.path.join(default_chart_output_dir,default_char_dir_name)
    return html_outdir_root


import argparse

def main():
    parser = argparse.ArgumentParser(description='CLI for pto_generate_snapshot_240302_v2_by_crop_dates function')
    
    parser.add_argument('-i','--instrument', type=str, required=True)
    parser.add_argument('-t','--timeframes', type=str, required=True)
    parser.add_argument('-tos','--tf_of_signal', type=str, required=True)
    parser.add_argument('-st','--sig_type_name', type=str, required=True)
    parser.add_argument('-cl','--crop_last_dt_arr', type=str, required=True)
    parser.add_argument('--scn_root_dir', type=str, default=None)
    parser.add_argument('--default_char_dir_name', type=str, default="charts")
    parser.add_argument('--show_chart', type=bool, default=False)
    parser.add_argument('--show_tabs', type=bool, default=False)
    parser.add_argument('--save_fig_image', type=bool, default=True)
    parser.add_argument('--save_cds_data', type=bool, default=True)
    parser.add_argument('--out_htm_viewer_full_fn', type=str, default="index.html")
    parser.add_argument('--out_htm_viewer_prefix', type=str, default="_index-")
    parser.add_argument('--width', type=int, default=2550)
    parser.add_argument('--height', type=int, default=1150)

    args = parser.parse_args()

    pto_generate_snapshot_240302_v2_by_crop_dates(
        i=args.instrument,
        timeframes=args.timeframes,
        tf_of_signal=args.tf_of_signal,
        sig_type_name=args.sig_type_name,
        crop_last_dt_arr=args.crop_last_dt_arr,
        scn_root_dir=args.scn_root_dir,
        default_char_dir_name=args.default_char_dir_name,
        show_chart=args.show_chart,
        show_tabs=args.show_tabs,
        save_fig_image=args.save_fig_image,
        save_cds_data=args.save_cds_data,
        out_htm_viewer_full_fn=args.out_htm_viewer_full_fn,
        out_htm_viewer_prefix=args.out_htm_viewer_prefix,
        w=args.width,
        h=args.height
    )

if __name__ == "__main__":
    main()