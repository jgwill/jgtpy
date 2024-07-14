import json
class JGTBaseRequest:
    def __init__(self, quiet=True, verbose_level=0,viewpath=False):
        self.quiet = quiet
        self.verbose_level = verbose_level
        self.viewpath = viewpath
   
    # create a new JGTBaseRequest object from args (argparse)
    @staticmethod
    def from_args(args):
        return JGTBaseRequest(
            quiet=args.quiet,
            verbose_level=args.verbose if args.verbose else 0,
            viewpath=args.viewpath if args.viewpath else False
        )
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
    
