class JGTPDSRequest:
    def __init__(self, instrument:str="SPX500", timeframe:str="H4", crop_last_dt:str=None):
        self.instrument = instrument
        self.timeframe = timeframe
        self.crop_last_dt = crop_last_dt
