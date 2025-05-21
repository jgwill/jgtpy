import argparse
import json
class JGTBaseRequest:
    def __init__(self, quiet=True, verbose_level=0,viewpath=False):
        self.quiet = quiet
        self.verbose_level = verbose_level
        self.viewpath = viewpath
    
    def __from_args__(self, args: argparse.Namespace):
        self.quiet = args.quiet
        self.verbose_level = args.verbose
        self.viewpath = args.viewpath
        
    # create a new JGTBaseRequest object from args (argparse)
    @staticmethod
    def from_args(args):
        instance=JGTBaseRequest(       )
        instance.__from_args__(args)
        return instance
    
    def __from_json__(self, json_str):
        #set values from json foreach of the keys included in the json_str
        try:
            json_obj=json.loads(json_str)
            for key in json_obj:
                setattr(self, key, json_obj[key])
        except Exception as e:
            print("ERROR(JGTBaseRequest): from_json", e)
            print("ERROR(JGTBaseRequest): from_json", json_str)
        
    
    @staticmethod
    def from_json(json_str):
        return json.loads(json_str)
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)
    
