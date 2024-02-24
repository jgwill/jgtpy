import os
#import jgtdotenv
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()  # take environment variables from .env.
#env=load_dotenv(os.getenv(os.getcwd()))
env = dotenv_values(".env")



#@DEPRECATED
if os.getenv('FXCM_TOKEN_REST_API_DEMO') == "":
  load_dotenv(os.getenv('HOME'))
if os.getenv('FXCM_TOKEN_REST_API_DEMO') == "":
  load_dotenv(os.getenv(os.getcwd()))
#@title TOKENS
def getenv(tvar):
  return os.getenv(tvar)



#@DEPRECATED: 

_FXCM_TOKEN_REST_API_DEMO = os.getenv('FXCM_TOKEN_REST_API_DEMO')
_FXCM_TOKEN_REST_API_REAL = os.getenv('FXCM_TOKEN_REST_API_REAL')
_FXCM_DROPBOX_ACCESS_TOKEN = os.getenv('FXCM_DROPBOX_ACCESS_TOKEN')
_DROPBOX_ACCESS_TOKEN= _FXCM_DROPBOX_ACCESS_TOKEN
# print(FXCM_TOKEN_REST_API_DEMO)

local_fn_compression='gzip'


def get_pov_local_data_filename(instrument:str,timeframe:str,local_data_dir='./data',local_fn_suffix='.full.csv.gz'):
  print("-------#@STCIssue FIXING REQUIRED-----------------")
  tf=timeframe
  if tf=="m1":
    tf="mi1"
  return local_data_dir + "/"+ instrument.replace("/","-") + "_" + tf + local_fn_suffix

pysroot=os.getenv('pysroot')
#pysroot='/w/o/pys/'
CDS_URL_BASE=os.getenv('CDS_URL_BASE')
phurlbase=CDS_URL_BASE
#phurlbase='https://ai.guillaumeisabelle.com/sds/datasets/cds/' #todo rename as pds, cds are going to be indicators/cds data

DROPBOX_ETC_PATH= '/w/etc/'

#@title Demo Token
_tokendemo =_FXCM_TOKEN_REST_API_DEMO
_tokenreal=_FXCM_TOKEN_REST_API_REAL

_token=_tokendemo #default
if os.getenv('usereal') == 'True' :
  _token=_tokenreal
  print('TRADING REAL ACTIVATED')

def setreal():
  global _token
  _token=_tokenreal

def setdemo():
  global _token
  _token=_tokendemo


# %%
contextInstruments=['AUD/CAD',
 'AUD/JPY',
 'AUD/USD',
 'CAD/CHF',
 'CAD/JPY',
 'EUR/CAD',
 'EUR/USD',
 'GBP/CAD',
 'GBP/USD',
 'NAS100',
 'NZD/CAD',
 'NZD/USD',
 'USD/CAD'
 ]

contextTimeframes=['m1','m5','m15']
# contextTimeframes=['m1','m5','m15','H1','H4','D1','W1','M1']
