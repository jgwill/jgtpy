
import sys
import os

import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTPDSRequest import JGTPDSRequest

from jgtutils.jgtconstants import (TJAW_PERIODS, TTEETH_PERIODS, NB_BARS_BY_DEFAULT_IN_CDS)

class JGTIDSRequest(JGTPDSRequest):
    """
    Represents a JGT IDS (Indicator Data Structure) request.

    Args:
        aof_flag (bool): Flag indicating whether to include aof_flag (AO Peak V1 (Would be replaced by the scipy.signals peak)) data.
        balligator_flag (bool): Flag indicating whether to include Big Alligator data.
        mfi_flag (bool): Flag indicating whether to include mfi_flag (Money Flow Index) data.
        gator_oscillator_flag (bool): Flag indicating whether to include Gator Oscillator data.
        balligator_period_jaws (int): Period for the jaws line of the Alligator indicator.
        balligator_period_teeth (int): Period for the teeth line of the Alligator indicator.
        balligator_period_lips (int): Period for the lips line of the Alligator indicator.
        balligator_shift_jaws (int): Shift for the jaws line of the Alligator indicator.
        balligator_shift_teeth (int): Shift for the teeth line of the Alligator indicator.
        balligator_shift_lips (int): Shift for the lips line of the Alligator indicator.
        largest_fractal_period (int): Period for identifying the largest fractal.
        peak_distance (int): Distance between peaks.
        peak_width (int): Width of the peaks.
        peak_divider_min_height (int): Minimum height of the peak divider.
        rounding_decimal_min (int): Minimum decimal for rounding.
        disable_ao_peaks_v1 (bool): Flag indicating whether to disable AO Peak V1.
        include_ao_color (bool): Flag indicating whether to include AO color data.
        include_ac_color (bool): Flag indicating whether to include AC color data.
        addAlligatorOffsetInFutur (bool): Flag indicating whether to add Alligator offset in the future.
        talligator_flag (bool): Flag indicating whether to include Talligator data.
        talligator_period_jaws (int): Period for the jaws line of the Talligator indicator.
        talligator_period_teeth (int): Period for the teeth line of the Talligator indicator.
        talligator_period_lips (int): Period for the lips line of the Talligator indicator.
        talligator_shift_jaws (int): Shift for the jaws line of the Talligator indicator.
        talligator_shift_teeth (int): Shift for the teeth line of the Talligator indicator.
        talligator_shift_lips (int): Shift for the lips line of the Talligator indicator.
        
        
    """
    def __init__(self, 
                 aof_flag=False, 
                 balligator_flag=True, 
                 mfi_flag=True, 
                 gator_oscillator_flag=False,
                 balligator_period_jaws=89, 
                 balligator_period_teeth=55, 
                 balligator_period_lips=34,
                 balligator_shift_jaws=55, 
                 balligator_shift_teeth=34, 
                 balligator_shift_lips=21,
                 largest_fractal_period=89,
                 peak_distance=13,
                 peak_width=8,
                 peak_divider_min_height = 3,
                 rounding_decimal_min=11, 
                 disable_ao_peaks_v1=True,
                 include_ao_color=False,
                 include_ac_color=False,
                 addAlligatorOffsetInFutur=False,
                 talligator_flag=True, 
                 talligator_period_jaws=377, 
                 talligator_period_teeth=233, 
                 talligator_period_lips=144,
                 talligator_shift_jaws=233, 
                 talligator_shift_teeth=144, 
                 talligator_shift_lips=89,
                 *args, 
                 **kwargs):
        #super().__init__(None, None, None)
        super().__init__(*args, **kwargs)
        self.include_ao_color = include_ao_color
        self.include_ac_color = include_ac_color
        self.disable_ao_peaks_v1 = disable_ao_peaks_v1
        self.aof_flag = aof_flag
        self.balligator_flag = balligator_flag
        self.mfi_flag = mfi_flag
        self.gator_oscillator_flag = gator_oscillator_flag
        self.balligator_period_jaws = balligator_period_jaws
        self.balligator_period_teeth = balligator_period_teeth
        self.balligator_period_lips = balligator_period_lips
        self.balligator_shift_jaws = balligator_shift_jaws
        self.balligator_shift_teeth = balligator_shift_teeth
        self.balligator_shift_lips = balligator_shift_lips
        self.largest_fractal_period = largest_fractal_period
        self.rounding_decimal_min = rounding_decimal_min
        self.peak_distance = peak_distance
        self.peak_width = peak_width
        self.peak_divider_min_height = peak_divider_min_height
        self.addAlligatorOffsetInFutur = addAlligatorOffsetInFutur
        self.talligator_flag=talligator_flag
        self.talligator_period_jaws = talligator_period_jaws
        self.talligator_period_teeth = talligator_period_teeth
        self.talligator_period_lips = talligator_period_lips
        self.talligator_shift_jaws = talligator_shift_jaws
        self.talligator_shift_teeth = talligator_shift_teeth
        self.talligator_shift_lips = talligator_shift_lips

        #Migrated logics
        self.balligator_period_jaws = self.balligator_period_jaws 
        #if self.balligator_flag else 0 #balligator_period_jaws will be 0 if it is not used
        self.talligator_period_jaws = self.talligator_period_jaws 
        #if self.talligator_flag else 0 #talligator_period_jaws will be 0 if it is not used
        
        self.__values_changed__()

    def __values_changed__(self):
        if self.talligator_flag:
            self.talligator_fix_quotescount()
        else:
            if self.balligator_flag:
                self.balligator_fix_quotescount()
    
    def __from_args__(self, args):
        
        
        super().__from_args__(args)
        self.include_ao_color = args.include_ao_color if hasattr(args, 'include_ao_color') else False
        self.include_ac_color = args.include_ac_color if hasattr(args, 'include_ac_color') else False
        self.disable_ao_peaks_v1 = args.disable_ao_peaks_v1 if hasattr(args, 'disable_ao_peaks_v1') else True
        self.aof_flag = args.aof_flag if hasattr(args, 'aof_flag') else False
        self.balligator_flag = args.balligator_flag
        self.mfi_flag = args.mfi_flag
        self.gator_oscillator_flag = args.gator_oscillator_flag if hasattr(args, 'gator_oscillator_flag') else False
        self.balligator_period_jaws = args.balligator_period_jaws if hasattr(args, 'balligator_period_jaws') else 89
        self.balligator_period_teeth = args.balligator_period_teeth if hasattr(args, 'balligator_period_teeth') else 55
        self.balligator_period_lips = args.balligator_period_lips if hasattr(args, 'balligator_period_lips') else 34
        self.balligator_shift_jaws = args.balligator_shift_jaws if hasattr(args, 'balligator_shift_jaws') else 55
        self.balligator_shift_teeth = args.balligator_shift_teeth if hasattr(args, 'balligator_shift_teeth') else 34
        self.balligator_shift_lips = args.balligator_shift_lips if hasattr(args, 'balligator_shift_lips') else 21
        self.largest_fractal_period = args.largest_fractal_period if hasattr(args, 'largest_fractal_period') else 89
        self.rounding_decimal_min = args.rounding_decimal_min if hasattr(args, 'rounding_decimal_min') else 11
        self.peak_distance = args.peak_distance if hasattr(args, 'peak_distance') else 13
        self.peak_width = args.peak_width if hasattr(args, 'peak_width') else 8
        self.peak_divider_min_height = args.peak_divider_min_height if hasattr(args, 'peak_divider_min_height') else 3
        self.addAlligatorOffsetInFutur = args.addAlligatorOffsetInFutur if hasattr(args, 'addAlligatorOffsetInFutur') else False
        self.talligator_flag=args.talligator_flag
        self.talligator_period_jaws = args.talligator_period_jaws if hasattr(args, 'talligator_period_jaws') else 377
        self.talligator_period_teeth = args.talligator_period_teeth if hasattr(args, 'talligator_period_teeth') else 233
        self.talligator_period_lips = args.talligator_period_lips if hasattr(args, 'talligator_period_lips') else 144
        self.talligator_shift_jaws = args.talligator_shift_jaws if hasattr(args, 'talligator_shift_jaws') else 233
        self.talligator_shift_teeth = args.talligator_shift_teeth if hasattr(args, 'talligator_shift_teeth') else 144
        self.talligator_shift_lips = args.talligator_shift_lips if hasattr(args, 'talligator_shift_lips') else 89
        
        self.__values_changed__()
        
    # create a new JGTIDSRequest object from args (argparse)
    @staticmethod
    def from_args(args):
        # if hasattr(args, 'json_content'):
        #     #Create an instance from the json string content
        #     ## Dont use from_json
        #     rq = JGTIDSRequest()
        #     rq.__dict__ = json.loads(args.json_content)
        #     return rq
        
        instance=JGTIDSRequest()
        instance.__from_args__(args)
        
        return instance
    
    @staticmethod
    def from_json(json_str):
        #print("json_str:",json_str)
        return json.loads(json_str)
    
    @staticmethod
    def from_json_file(json_file_path):
        with open(json_file_path) as f:
            data = json.load(f)
            return data
        return None
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2) 
    
    def _get_talligator_required_additional_quotescount(self):            
        TJAW_REQUIRED_CALC_BARS = TJAW_PERIODS+TTEETH_PERIODS #@STCIssue We should use : self.talligator_period_jaws ,... instead of TJAW_PERIODS, TTEETH_PERIODS
        return TJAW_REQUIRED_CALC_BARS

    def talligator_fix_quotescount(self,nb_bars_by_default=NB_BARS_BY_DEFAULT_IN_CDS):
        if self.use_full:
            return
        
        if self.talligator_flag:
            if self.quotescount==-1:
                self.quotescount = nb_bars_by_default
            TALLIGATOR_REQ_QUOTECOUNT=self._get_talligator_required_additional_quotescount()

            self.quotescount = TALLIGATOR_REQ_QUOTECOUNT + self.quotescount

    
    def _get_balligator_required_additional_quotescount(self):            
        BJAW_REQUIRED_CALC_BARS = self.balligator_period_jaws+self.balligator_shift_jaws 
        return BJAW_REQUIRED_CALC_BARS

    def balligator_fix_quotescount(self,nb_bars_by_default=NB_BARS_BY_DEFAULT_IN_CDS):
        if self.use_full:
            return
        
        if self.balligator_flag and not self.talligator_flag:
            if self.quotescount==-1:
                self.quotescount = nb_bars_by_default
            BALLIGATOR_REQ_QUOTECOUNT=self._get_balligator_required_additional_quotescount()
            #print("self.quotescount:",self.quotescount)
            self.quotescount = BALLIGATOR_REQ_QUOTECOUNT + self.quotescount
            