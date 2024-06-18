
import sys
import os

import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTPDSRequest import JGTPDSRequest

from jgtutils.jgtconstants import (TJAW_PERIODS, TTEETH_PERIODS)

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
                 balligator_flag=False, 
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
                 talligator_flag=False, 
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
        
        if self.talligator_flag:
            self.talligator_fix_quotescount()
        else:
            if self.balligator_flag:
                self.balligator_fix_quotescount()
    
    # create a new JGTIDSRequest object from args (argparse)
    @staticmethod
    def from_args(args):
        return JGTIDSRequest(
            instrument=args.instrument,
            timeframe=args.timeframe,
            quotescount=args.quotescount,
            viewpath=args.viewpath,
            use_fresh=args.fresh,
            use_full=args.full,
            gator_oscillator_flag=args.gator_oscillator_flag,
            mfi_flag=args.mfi_flag,
            balligator_flag=args.balligator_flag,
            balligator_period_jaws=args.balligator_period_jaws,
            largest_fractal_period=args.largest_fractal_period,
            talligator_flag=args.talligator_flag,
            talligator_period_jaws=args.talligator_period_jaws,
            verbose_level=args.verbose
        )   
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2) 
    
    def _get_talligator_required_additional_quotescount(self):            
        TJAW_REQUIRED_CALC_BARS = TJAW_PERIODS+TTEETH_PERIODS #@STCIssue We should use : self.talligator_period_jaws ,... instead of TJAW_PERIODS, TTEETH_PERIODS
        return TJAW_REQUIRED_CALC_BARS

    def talligator_fix_quotescount(self,nb_bars_by_default=300):
        if self.use_full:
            return
        
        if self.talligator_flag:
            if self.quotescount==-1:
                self.quotescount = nb_bars_by_default
            TALLIGATOR_REQ_QUOTECOUNT=self._get_talligator_required_additional_quotescount()
            #print("self.quotescount:",self.quotescount)
            self.quotescount = TALLIGATOR_REQ_QUOTECOUNT + self.quotescount
            #print("self.quotescount:",self.quotescount)
            # if self.quotescount < TALLIGATOR_REQ_QUOTECOUNT + 300:
            #     self.quotescount = TALLIGATOR_REQ_QUOTECOUNT
    
    def _get_balligator_required_additional_quotescount(self):            
        BJAW_REQUIRED_CALC_BARS = self.balligator_period_jaws+self.balligator_shift_jaws 
        return BJAW_REQUIRED_CALC_BARS

    def balligator_fix_quotescount(self,nb_bars_by_default=300):
        if self.use_full:
            return
        
        if self.balligator_flag and not self.talligator_flag:
            if self.quotescount==-1:
                self.quotescount = nb_bars_by_default
            BALLIGATOR_REQ_QUOTECOUNT=self._get_balligator_required_additional_quotescount()
            #print("self.quotescount:",self.quotescount)
            self.quotescount = BALLIGATOR_REQ_QUOTECOUNT + self.quotescount
            