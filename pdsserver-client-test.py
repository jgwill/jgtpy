import requests
import json

response = requests.post('http://localhost:5000/getPH', json={'instrument': 'EUR/USD', 'timeframe': 'H4'})
#print(response.json())
print(response.text)

print("mk_fn")
response = requests.get('http://localhost:5000/mk_fn', params={'instrument': 'EUR/USD', 'timeframe': 'm1', 'ext': 'csv'})
print(response.json())

print("------------------")
print("---- from file store route ---")


import pandas as pd

#response = requests.post('http://localhost:5000/getPH_from_filestore', json={'instrument': 'EUR/USD', 'timeframe': 'H4', 'quiet': True, 'compressed': False, 'with_index': True}) df = pd.read_json(response.text, orient='split')
import requests
import pandas as pd
from io import StringIO

response = requests.post('http://localhost:5000/getPH_from_filestore',
                         json={'instrument': 'EUR/USD',
                               'timeframe': 'H4',
                               'quiet': True,
                               'compressed': False,
                               'with_index': True})
df = pd.read_json(StringIO(response.text), orient='split')

print(df)

print("-----------Run CLI---------")

import requests

response = requests.post('http://localhost:5000/run_jgtcli',
                         json={'instrument': 'EUR/USD',
                               'timeframe': 'H4',
                               'output': True,
                               'cds': True,
                               'verbose': 1,
                               'datefrom': '01.01.2022 00:00:00',
                               'dateto': '01.01.2023 00:00:00'})
print(response.json())

import requests

response = requests.post('http://localhost:5000/run_jgtcli',
                         json={'instrument': 'EUR/USD',
                               'timeframe': 'H4',
                               'output': True,
                               'cds': True})
                               
print(response.json())