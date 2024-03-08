
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTPDSRequest import JGTPDSRequest

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

    Attributes:
        aof_flag (bool): Flag indicating whether to include aof_flag
        balligator_flag (bool): Flag indicating whether to include Big Alligator data.
        mfi_flag (bool): Flag indicating whether to include mfi_flag (Market Facilitation Index) data.
        gator_oscillator_flag (bool): Flag indicating whether to include Gator Oscillator data.
        balligator_period_jaws (int): Period for the jaws line of the Alligator indicator.
        balligator_period_teeth (int): Period for the teeth line of the Alligator indicator.
        balligator_period_lips (int): Period for the lips line of the Alligator indicator.
        balligator_shift_jaws (int): Shift for the jaws line of the Alligator indicator.
        balligator_shift_teeth (int): Shift for the teeth line of the Alligator indicator.
        balligator_shift_lips (int): Shift for the lips line of the Alligator indicator.
        largest_fractal_period (int): Period for identifying the largest fractal.
        peak_distance (int): Distance between peaks.
        peak_width (int): Width of peaks.
        peak_divider_min_height (int): Minimum height of peaks.
        rounding_decimal_min (int): Minimum number of decimal places to round to.
    """
    def __init__(self, 
                 aof_flag=False, 
                 balligator_flag=False, 
                 mfi_flag=False, 
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
                 rounding_decimal_min=10, 
                 *args, 
                 **kwargs):
        #super().__init__(None, None, None)
        super().__init__(*args, **kwargs)
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

        #Migrated logics
        self.balligator_period_jaws = self.balligator_period_jaws if self.balligator_flag else 0 #balligator_period_jaws will be 0 if it is not used
        
        
        
    # def __str__(self) -> str:
    #     return super().__str__() + f"aof_flag: {self.aof_flag}\n" + f"balligator_flag: {self.balligator_flag}\n" + f"mfi_flag: {self.mfi_flag}\n" + f"gator_oscillator_flag: {self.gator_oscillator_flag}\n" + f"balligator_period_jaws: {self.balligator_period_jaws}\n" + f"balligator_period_teeth: {self.balligator_period_teeth}\n" + f"balligator_period_lips: {self.balligator_period_lips}\n" + f"balligator_shift_jaws: {self.balligator_shift_jaws}\n" + f"balligator_shift_teeth: {self.balligator_shift_teeth}\n" + f"balligator_shift_lips: {self.balligator_shift_lips}\n" + f"largest_fractal_period: {self.largest_fractal_period}\n" + f"peak_distance: {self.peak_distance}\n" + f"peak_width: {self.peak_width}\n" + f"peak_divider_min_height: {self.peak_divider_min_height}\n" + f"rounding_decimal_min: {self.rounding_decimal_min}\n"