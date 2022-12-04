import os
#import jgtdotenv
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
if os.getenv('FXCM_TOKEN_REST_API_DEMO') == "":
  load_dotenv(os.getenv('HOME'))
if os.getenv('FXCM_TOKEN_REST_API_DEMO') == "":
  load_dotenv(os.getenv(os.getcwd()))
#@title TOKENS

# keep expiring...
FXCM_TOKEN_REST_API_DEMO = os.getenv('FXCM_TOKEN_REST_API_DEMO')
FXCM_TOKEN_REST_API_REAL = os.getenv('FXCM_TOKEN_REST_API_REAL')
FXCM_DROPBOX_ACCESS_TOKEN = os.getenv('FXCM_DROPBOX_ACCESS_TOKEN')
DROPBOX_ACCESS_TOKEN= FXCM_DROPBOX_ACCESS_TOKEN
# print(FXCM_TOKEN_REST_API_DEMO)

local_fn_compression='gzip'

def get_pov_local_data_filename(instrument,timeframe,local_data_dir='./data',local_fn_suffix='.full.csv.gz',):
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
tokendemo =FXCM_TOKEN_REST_API_DEMO
tokenreal=FXCM_TOKEN_REST_API_REAL

token=tokendemo #default
if os.getenv('usereal') == 'True' :
  token=tokenreal
  print('TRADING REAL ACTIVATED')

def setreal():
  global token
  token=tokenreal

def setdemo():
  global token
  token=tokendemo


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
