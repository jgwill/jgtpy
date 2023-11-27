import requests
import json

import pandas as pd
from io import StringIO


print("-----------Run CLI---------")

import requests

#response = requests.post('http://localhost:5000/run_jgtcli',
#                         json={'instrument': 'EUR/USD',
#                               'timeframe': 'H4',
#                               'output': True,
#                               'cds': True,
#                               'verbose': 1,
#                               'datefrom': '01.01.2022 00:00:00',
#                               'dateto': '01.01.2023 00:00:00'})

#print(response.json())


response = requests.post('http://localhost:5000/run_jgtcli',
                         json={'instrument': 'EUR/USD',
                               'timeframe': 'H4',
                               'output': True,
                               'cds': True})
                               
print(response.json())
