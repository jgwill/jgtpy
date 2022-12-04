#import fxcmpy and check the imported version
import fxcmpy as fx
import datetime as dt
import pandas as pd
#fxcmpy.__version__
import jgtpy.JGTConfig as jgtc


con=None
#global con=None

#@title Demo Token
# token ='6c8d49b0be4e220d842d6c1d5350.1.12541cc4c8'
token = jgtc.token
#print(token)
def create_con():
  return fx.fxcmpy(access_token = token, log_level='error',log_file=None)
#config_file='fxcm.cfg')

def create_con_cfg():
  return fx.fxcmpy(config_file='fxcm.cfg', log_level='error',log_file=None)

# def __dummy():
#   m=fxcmpy.fxcmpy

def connect(quiet=True):
  global con
  try:
    if not con or not con.connection_status == 'established':
      con = create_con()
      if not quiet:
        print('Connected')
    else:
      if not quiet:
        print('ALready Connected')
  except ConnectionError:
    print('Connection Error, retrying')
    con = create_con()
  except TimeoutError                              :
    print('ohoh, Timeout, retrying...')
    try:
      con = None
      con = create_con()
    except ConnectionError:
      print('ohoh AGAIN, Connection error, retrying...FUCK OFF')
      pass
    except TimeoutError                              :
      print('ohoh AGAIN, Timeout, retrying...FUCK OFF')
      pass
  return con
  #print(con.connection_status)



def disconnect(quiet=False):
  global con
  if con and con.connection_status == 'established' :
    con.close()
    if not quiet:
      print('Disconnected')
  else:
    if not quiet:
      print('Not connected')
  con= None
  return con
  
def status():
  global con
  if con :
    print(con.connection_status)
  else:
    print('Not connected')

