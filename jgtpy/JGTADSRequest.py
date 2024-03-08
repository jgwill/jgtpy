
import sys
import os
import copy

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCDSRequest import JGTCDSRequest
from JGTChartConfig import JGTChartConfig


class JGTADSRequest(JGTCDSRequest):
    def __init__(self,
                 plot_ao_peaks=True, 
                 show=False, 
                 nb_bar_on_chart=300, 
                 min_bar_on_chart=299, 
                 cds_required_amount_of_bar_for_calc=None, 
                 nb_bar_to_retrieve=None,
                 tlid_range:str=None, 
                 cc:JGTChartConfig=None,
                 *args, 
                 **kwargs):
        super().__init__(*args, **kwargs)
        if cc is None:
            self.cc = JGTChartConfig()
        else:
            self.cc = cc
        
        self.tlid_range = tlid_range
        if self.tlid_range is not None:
            print("-- Possible Extension for a request with a TLID range in which we would generates various charts of signaling moments--")
        
        
        self.plot_ao_peaks = plot_ao_peaks
        self.show = show
        #self.big_alligator_flag = big_alligator_flag
        
        
        
        # IMPORTED from JGTChartConfig (Migrating from JGTChartConfig to JGTADSRequest)
        self.nb_bar_on_chart = nb_bar_on_chart
        self.min_bar_on_chart = min_bar_on_chart
        
        self.cds_required_amount_of_bar_for_calc = cds_required_amount_of_bar_for_calc if cds_required_amount_of_bar_for_calc is not None else self.balligator_period_jaws
        if self.balligator_period_jaws == 0 and self.largest_fractal_period != 0:
            self.cds_required_amount_of_bar_for_calc = self.largest_fractal_period
            
        self.nb_bar_to_retrieve = nb_bar_to_retrieve if nb_bar_to_retrieve is not None else self.nb_bar_on_chart + self.cds_required_amount_of_bar_for_calc
        
        #largest_fractal_period
        
        #@STCIssue Backward compatibility for using cc
        self.cc.nb_bar_on_chart = self.nb_bar_on_chart
        self.cc.min_bar_on_chart = self.min_bar_on_chart
        self.cc.balligator_period_jaws = self.balligator_period_jaws
        self.cc.cds_required_amount_of_bar_for_calc = self.cds_required_amount_of_bar_for_calc
        self.cc.nb_bar_to_retrieve = self.nb_bar_to_retrieve
    
    def copy(self):
        return copy.copy(self)
        # _cp= JGTADSRequest(self.plot_ao_peaks, self.show, self.nb_bar_on_chart, self.min_bar_on_chart, self.cds_required_amount_of_bar_for_calc, self.nb_bar_to_retrieve, self.tlid_range, self.cc)
        # _cp.super = super().__copy__()
    
    def copy_with_timeframe(self, timeframe:str):
        _cp = self.copy()
        _cp.timeframe = timeframe
        return _cp
    
    # def __str__(self) -> str:
    #     return super().__str__() + f"plot_ao_peaks: {self.plot_ao_peaks}, show: {self.show}, nb_bar_on_chart: {self.nb_bar_on_chart}, min_bar_on_chart: {self.min_bar_on_chart}, cds_required_amount_of_bar_for_calc: {self.cds_required_amount_of_bar_for_calc}, nb_bar_to_retrieve: {self.nb_bar_to_retrieve}, tlid_range: {self.tlid_range if self.tlid_range is not None else 'None'}, cc: {self.cc if self.cc is not None else 'None'}"


# Create an instance with default values
default_config = JGTADSRequest()

        
