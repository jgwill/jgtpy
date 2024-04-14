import json
class JGTBaseRequest:
    def __init__(self, quiet=True, verbose_level=0):
        self.quiet = quiet
        self.verbose_level = verbose_level

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
    
