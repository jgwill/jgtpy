
import sys
import os
import json


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTIDSRequest import JGTIDSRequest

class JGTCDSRequest(JGTIDSRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
    # def __str__(self) -> str:
    #     return super().__str__() + f"dummy_cds_flag: {self.dummy_cds_flag}\n" 
