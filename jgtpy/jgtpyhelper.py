import os
from matplotlib.figure import Figure

def savefig_pov(fig:Figure, instrument:str, timeframe:str,path=".", dpi:float=None):
    if dpi is None:
        dpi=fig.dpi
    try:
        exn = ".png"
        if path == "pov" or path==".":
            path = os.getcwd()  # saving in current directory
        if os.path.isdir(path):
            fn = instrument.replace("/", "-") + "_" + timeframe + exn
            fig.savefig(
                os.path.join(path, fn),
                dpi=dpi,
            )
        else:
            fig.savefig(path, dpi=dpi)
    except Exception as e:
        print("Error saving figure to: " + path)
        print(e)
        # traceback.print_exc()


def savefig_timeframe(fig:Figure, timeframe:str,path=".", dpi:float=None):
    if dpi is None:
        dpi=fig.dpi
    try:
        exn = ".png"
        if path == "pov" or path==".":
            path = os.getcwd()  # saving in current directory
        if os.path.isdir(path):
            fn = timeframe.replace("m1","min1") + exn
            fig.savefig(
                os.path.join(path, fn),
                dpi=dpi,
            )
        else:
            fig.savefig(path, dpi=dpi)
    except Exception as e:
        print("Error saving figure to: " + path)
        print(e)
        # traceback.print_exc()



def get_dt_fmt_for_timeframe(timeframe,separator="\n"):
    if timeframe in ["H1", "H2", "H3", "H4", "H6", "H8"]:
        return f"%y-%m-%d{separator}%H"
    elif timeframe in ["m5", "m15"]:
        return f"%y-%m-%d{separator}%H:%M"
    elif timeframe == "M1":
        return "%Y-%m"
    else:
        return "%Y-%m-%d"




def tst():
  #%%
  import jgtpyhelper as jgth
  r=jgth.get_dt_fmt_for_timeframe("H1"," ")
  r=jgth.get_dt_fmt_for_timeframe("H1")
  r
  
# %%
