
import pandas as pd

def createfromdf(_df):
  item=Criss(_df)
  return item

class Criss:
  df= pd.DataFrame()

  def fromdf(_df):
    item=Criss(_df)
    return item
  
  def __init__(self,_df: pd.DataFrame)-> None:
    self.df=_df
    #_df[_df["statement"]=="data"]
