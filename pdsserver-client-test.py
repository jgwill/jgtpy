import requests
import json

response = requests.post('http://localhost:5000/getPH', json={'instrument': 'EUR/USD', 'timeframe': 'm1'})
print(response.json())

response = requests.get('http://localhost:5000/mk_fn', params={'instrument': 'EUR/USD', 'timeframe': 'm1', 'ext': 'csv'})
print(response.json())

