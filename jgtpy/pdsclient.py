import requests
import json
import os

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgt2312

class JGTPDSProxyClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def getPH(self, instrument:str, timeframe:str):
        data = {"instrument": instrument, "timeframe": timeframe}
        response = requests.post(f"{self.base_url}/getPH", json=data)
        return response.text

    def getPH_from_filestore(
        self, instrument, timeframe, quiet=True, compressed=False, with_index=True
    ):
        data = {
            "instrument": instrument,
            "timeframe": timeframe,
            "quiet": quiet,
            "compressed": compressed,
            "with_index": with_index,
        }
        response = requests.post(f"{self.base_url}/getPH_from_filestore", json=data)
        return response.json()

    def h(
        self, instrument, timeframe
    ):
        data = {
            "instrument": instrument,
            "timeframe": timeframe
        }
        response = requests.post(f"{self.base_url}/h", json=data)
        return response.json()

    def cli(
        self,
        instrument,
        timeframe,
        datefrom=None,
        dateto=None,
        quote_count=335,
        verbose=0,
    ):
        data = {
            "instrument": instrument,
            "timeframe": timeframe,
            "datefrom": datefrom,
            "dateto": dateto,
            "quote_count": quote_count,
            "verbose": verbose,
        }
        response = requests.post(f"{self.base_url}/cli", json=data)
        return response.json()

    def cli2(
        self,
        instrument:str,
        timeframe:str,
    ):
        data = {
            "instrument": instrument,
            "timeframe": timeframe
        }
        response = requests.post(f"{self.base_url}/cli", json=data)
        print(response)
        return response.json()
    
    def run_init(self):        
        response = requests.get(f"{self.base_url}/init")
        return response.json()

    def fetch_mk_fn(self, instrument:str, timeframe:str, ext:str):
        params = {"instrument": instrument, "timeframe": timeframe, "ext": ext}
        response = requests.get(f"{self.base_url}/mk_fn", params=params)
        return response.json()

    def fetch_get_instrument_properties(self, instrument:str):
        data = {"instrument": instrument.replace("-", "/")}
        response = requests.post(f"{self.base_url}/iprop", json=data)
        return response.json()
