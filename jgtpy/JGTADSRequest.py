from jgtpy.JGTCDSRequest import JGTCDSRequest


class JGTADSRequest(JGTCDSRequest):
    def __init__(self, dummy_ads_flag=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dummy_cds_flag = dummy_ads_flag
