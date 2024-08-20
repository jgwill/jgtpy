
import sys
import os
import copy
import json


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCDSRequest import JGTCDSRequest
from JGTChartConfig import JGTChartConfig


class JGTADSRequest(JGTCDSRequest):
    def __init__(self,
                 plot_ao_peaks=True, 
                 show=False, 
                 nb_bar_on_chart=None, 
                 min_bar_on_chart=None, 
                 cds_required_amount_of_bar_for_calc=None, 
                 nb_bar_to_retrieve=None,
                 tlid_range:str=None, 
                 cc:JGTChartConfig=None,
                 save_additional_figures_path:str=None,
                 save_additional_figures_dpi=300,
                 show_plain_plot=False,
                 show_feature_one_plot=False,
                 show_feature_two_plot=False,
                 show_feature_2403_plot=False,
                 save_figure_as_pov:bool=False,
                 save_figure_as_timeframe:bool=False,
                 *args, 
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        #largest_fractal_period
        
        if cc is None:
            self.cc = JGTChartConfig()
            self.show_feature_one_plot = show_feature_one_plot
            self.show_feature_two_plot = show_feature_two_plot
            self.show_plain_plot = show_plain_plot
            self.show_feature_2403_plot = show_feature_2403_plot
            self.set_feature_one_plot(show_feature_one_plot)
            self.set_feature_two_plot(show_feature_two_plot)
            self.set_plain_plot(show_plain_plot)
            self.set_feature_2403_plot(show_feature_2403_plot)
        else:
            self.cc = cc
            self.show_feature_one_plot = cc.show_feature_one_plot
            self.show_feature_two_plot = cc.show_feature_two_plot
            self.show_feature_2403_plot = cc.show_feature_2403_plot
            self.show_plain_plot = cc.show_plain_plot
        
        self.tlid_range = tlid_range
        if self.tlid_range is not None:
            print("-- Possible Extension for a request with a TLID range in which we would generates various charts of signaling moments--")
        
        self.save_additional_figures_path = save_additional_figures_path
        self.save_additional_figures_dpi = save_additional_figures_dpi
        
        self.plot_ao_peaks = plot_ao_peaks
        self.show = show
        #self.big_alligator_flag = big_alligator_flag
        
        
        
        # IMPORTED from JGTChartConfig (Migrating from JGTChartConfig to JGTADSRequest)
        if nb_bar_on_chart is not None:
            self.cc.nb_bar_on_chart = nb_bar_on_chart
        self.nb_bar_on_chart = self.cc.nb_bar_on_chart
            
        if min_bar_on_chart is not None:
            self.cc.min_bar_on_chart = min_bar_on_chart
        self.min_bar_on_chart = self.cc.min_bar_on_chart
            
        if cds_required_amount_of_bar_for_calc is not None:
            self.cc.cds_required_amount_of_bar_for_calc = cds_required_amount_of_bar_for_calc
        self.cds_required_amount_of_bar_for_calc = self.cc.cds_required_amount_of_bar_for_calc
        
        
        self.cds_required_amount_of_bar_for_calc = cds_required_amount_of_bar_for_calc if cds_required_amount_of_bar_for_calc is not None else self.balligator_period_jaws
        
        self.nb_bar_to_retrieve = nb_bar_to_retrieve if nb_bar_to_retrieve is not None else self.nb_bar_on_chart + self.cds_required_amount_of_bar_for_calc
        
        
        self.save_figure_as_pov=save_figure_as_pov
        self.save_figure_as_timeframe=save_figure_as_timeframe
        
        #@STCIssue Fix quotescount 
        if self.nb_bar_to_retrieve< self.quotescount:
            self.nb_bar_to_retrieve = self.quotescount
        
        #if self.balligator_period_jaws == 0 and self.largest_fractal_period != 0:
        #    self.cds_required_amount_of_bar_for_calc = self.largest_fractal_period
            
        
        #self.reset()
    
    def set_feature_2403_plot(self, value:bool):
        self.show_feature_2403_plot = value
        self.cc.show_feature_2403_plot = value
        #self.reset()
    
    def set_feature_one_plot(self, value:bool):
        self.show_feature_one_plot = value
        self.cc.show_feature_one_plot = value
        #self.reset()
        
    def set_feature_two_plot(self, value:bool):
        self.show_feature_two_plot = value
        self.cc.show_feature_two_plot = value
        
    def set_plain_plot(self, value:bool):
        self.show_plain_plot = value
        self.cc.show_plain_plot = value
        #self.reset()
     
    def reset(self):
        
        #self.cc.reset()
        
        #@STCIssue Backward compatibility for using cc
        # self.cc.nb_bar_on_chart = self.nb_bar_on_chart
        # self.cc.min_bar_on_chart = self.min_bar_on_chart
        
        self.balligator_period_jaws = self.cc.balligator_period_jaws 
        #self.cc.cds_required_amount_of_bar_for_calc = self.cds_required_amount_of_bar_for_calc
        self.nb_bar_to_retrieve = self.cc.nb_bar_to_retrieve
    
    def copy(self):
        return copy.copy(self)
        # _cp= JGTADSRequest(self.plot_ao_peaks, self.show, self.nb_bar_on_chart, self.min_bar_on_chart, self.cds_required_amount_of_bar_for_calc, self.nb_bar_to_retrieve, self.tlid_range, self.cc)
        # _cp.super = super().__copy__()
    
    def copy_with_timeframe(self, timeframe:str):
        _cp = self.copy()
        _cp.timeframe = timeframe
        return _cp
    
    def to_json(self,filename:str=None):
        json_o = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
        if filename is not None:
            with open(filename, 'w') as f:
                f.write(json_o)
        return json_o
    
    @staticmethod
    def from_json(json_str:str):
        return json.loads(json_str)
        
# Create an instance with default values
default_config = JGTADSRequest()


