"""
Alligator Mouth State and Water State Analysis Library

This module provides enhanced analysis of the Alligator indicator by determining:
1. Mouth Direction: Buy, Sell, Neither
2. Mouth Phase: Opening, Open, Closing, Sleeping
3. Bar Position: Above, In, Below the mouth
4. Water State: Splashing, Eating, Throwing, Poping, Entering, Switching

Based on specifications from issues #28, #16 and jgtstrategies/pull/6.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Sequence, Tuple, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum


class MouthDirection(Enum):
    """Enumeration for mouth direction states"""
    BUY = "buy"
    SELL = "sell" 
    NEITHER = "neither"


class MouthPhase(Enum):
    """Enumeration for mouth phase states"""
    OPENING = "opening"
    OPEN = "open"
    CLOSING = "closing"
    SLEEPING = "sleeping"
    NONE = "none"


class BarPosition(Enum):
    """Enumeration for bar position relative to mouth"""
    ABOVE = "above"
    IN = "in"
    BELOW = "below"


class WaterState(Enum):
    """Enumeration for water states"""
    SPLASHING = "splashing"
    EATING = "eating"
    THROWING = "throwing"
    POPING = "poping"
    ENTERING = "entering"
    SWITCHING = "switching"
    SLEEPING = "sleeping"


@dataclass
class AlligatorMouthWaterState:
    """Data class to hold complete mouth and water state information"""
    mouth_direction: MouthDirection
    mouth_phase: MouthPhase
    bar_position: BarPosition
    water_state: WaterState
    confidence_score: float = 0.0
    transition_detected: bool = False


class AlligatorMouthWaterAnalyzer:
    """
    Main analyzer class for Alligator mouth and water states.
    """
    
    def __init__(self, lookback_periods: int = 3, threshold: float = 1e-8):
        self.lookback_periods = lookback_periods
        self.threshold = threshold
        self._previous_state: Optional[AlligatorMouthWaterState] = None
    
    def calculate_mouth_direction_extended(
        self, 
        jaw: Sequence[float], 
        teeth: Sequence[float], 
        lips: Sequence[float]
    ) -> Tuple[MouthDirection, float]:
        """Calculate mouth direction with confidence scoring."""
        if len(jaw) < 2 or len(teeth) < 2 or len(lips) < 2:
            return MouthDirection.NEITHER, 0.0
            
        # Calculate slopes  
        jaw_slope = jaw[-1] - jaw[-2]
        teeth_slope = teeth[-1] - teeth[-2]
        lips_slope = lips[-1] - lips[-2]
        
        # Current line ordering
        current_order_buy = lips[-1] > teeth[-1] > jaw[-1]
        current_order_sell = lips[-1] < teeth[-1] < jaw[-1]
        
        # Slope alignment
        slopes_up = jaw_slope > 0 and teeth_slope > 0 and lips_slope > 0
        slopes_down = jaw_slope < 0 and teeth_slope < 0 and lips_slope < 0
        
        # Calculate confidence
        jaw_teeth_sep = abs(teeth[-1] - jaw[-1])
        teeth_lips_sep = abs(lips[-1] - teeth[-1])
        total_separation = jaw_teeth_sep + teeth_lips_sep
        
        slope_magnitude = abs(jaw_slope) + abs(teeth_slope) + abs(lips_slope)
        confidence = min(1.0, (slope_magnitude + total_separation) / 10.0)
        
        # Determine direction
        if current_order_buy and slopes_up:
            return MouthDirection.BUY, confidence
        elif current_order_sell and slopes_down:
            return MouthDirection.SELL, confidence
        else:
            return MouthDirection.NEITHER, confidence * 0.5
    
    def calculate_mouth_phase_extended(
        self,
        jaw: Sequence[float],
        teeth: Sequence[float], 
        lips: Sequence[float],
        gator_oscillator: Optional[Sequence[float]] = None
    ) -> MouthPhase:
        """Calculate mouth phase with optional Gator Oscillator integration."""
        if len(jaw) < 2 or len(teeth) < 2 or len(lips) < 2:
            return MouthPhase.NONE
            
        # Calculate distances between lines
        current_dist = (abs(jaw[-1] - teeth[-1]) + abs(teeth[-1] - lips[-1])) / 2.0
        previous_dist = (abs(jaw[-2] - teeth[-2]) + abs(teeth[-2] - lips[-2])) / 2.0
        
        # Use Gator Oscillator if available
        if gator_oscillator is not None and len(gator_oscillator) >= 2:
            current_gator = abs(gator_oscillator[-1])
            previous_gator = abs(gator_oscillator[-2])
            
            if current_gator > previous_gator:
                return MouthPhase.OPENING if previous_gator < self.threshold else MouthPhase.OPEN
            elif current_gator < previous_gator:
                return MouthPhase.SLEEPING if current_gator < self.threshold else MouthPhase.CLOSING
            else:
                return MouthPhase.OPEN if current_gator > self.threshold else MouthPhase.SLEEPING
        else:
            # Fallback to distance calculation
            if current_dist > previous_dist:
                return MouthPhase.OPENING if previous_dist < self.threshold else MouthPhase.OPEN
            elif current_dist < previous_dist:
                return MouthPhase.SLEEPING if current_dist < self.threshold else MouthPhase.CLOSING
            else:
                return MouthPhase.OPEN if current_dist > self.threshold else MouthPhase.SLEEPING


# Convenience functions for backward compatibility
def calculate_mouth_direction(jaw: Sequence[float], teeth: Sequence[float], lips: Sequence[float]) -> str:
    """Backward compatible mouth direction calculation."""
    analyzer = AlligatorMouthWaterAnalyzer()
    direction, _ = analyzer.calculate_mouth_direction_extended(jaw, teeth, lips)
    return direction.value


def calculate_mouth_phase(jaw: Sequence[float], teeth: Sequence[float], lips: Sequence[float]) -> str:
    """Backward compatible mouth phase calculation."""
    analyzer = AlligatorMouthWaterAnalyzer()
    phase = analyzer.calculate_mouth_phase_extended(jaw, teeth, lips)
    return phase.value
