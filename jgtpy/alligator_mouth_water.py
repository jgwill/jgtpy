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
    
    def calculate_bar_position(
        self,
        price_high: float,
        price_low: float,
        jaw: float,
        teeth: float,
        lips: float
    ) -> BarPosition:
        """Calculate where the price bar sits relative to the Alligator mouth."""
        highest_line = max(jaw, teeth, lips)
        lowest_line = min(jaw, teeth, lips)
        
        if price_low > highest_line:
            return BarPosition.ABOVE
        elif price_high < lowest_line:
            return BarPosition.BELOW
        else:
            return BarPosition.IN
    
    def calculate_water_state_extended(
        self,
        price_high: Sequence[float],
        price_low: Sequence[float],
        ao_values: Sequence[float],
        jaw: Sequence[float],
        teeth: Sequence[float],
        lips: Sequence[float],
        mouth_direction: MouthDirection,
        mouth_phase: MouthPhase,
        bar_position: BarPosition
    ) -> WaterState:
        """Calculate water state based on price action and mouth characteristics."""
        if len(ao_values) < 2 or len(price_high) < 2 or len(price_low) < 2:
            return WaterState.SLEEPING
            
        ao_current = ao_values[-1]
        
        # Previous bar price levels for momentum analysis
        prev_high = price_high[-2] if len(price_high) >= 2 else price_high[-1]
        prev_low = price_low[-2] if len(price_low) >= 2 else price_low[-1]
        
        # Get previous bar position for transition detection
        if len(jaw) >= 2 and len(teeth) >= 2 and len(lips) >= 2:
            prev_bar_pos = self.calculate_bar_position(
                prev_high, prev_low, jaw[-2], teeth[-2], lips[-2]
            )
        else:
            prev_bar_pos = bar_position
        
        # Water state logic based on Lua implementation
        if mouth_direction == MouthDirection.SELL:
            current_high = price_high[-1]
            lips_val = lips[-1]
            jaw_val = jaw[-1]
            
            if current_high < lips_val:  # Below lips
                if bar_position == BarPosition.BELOW:
                    if mouth_phase == MouthPhase.OPENING:
                        return WaterState.SWITCHING
                    elif len(lips) >= 2 and prev_high > lips[-2]:  # Previous was above lips
                        return WaterState.POPING
                    else:
                        return WaterState.SPLASHING
                        
            elif current_high > lips_val:  # Above lips
                if bar_position == BarPosition.IN:
                    if current_high < jaw_val:  # Below jaw
                        return WaterState.THROWING
                    elif len(lips) >= 2 and prev_high < lips[-2]:  # Previous was below lips
                        return WaterState.ENTERING
                    else:
                        return WaterState.EATING
                        
        elif mouth_direction == MouthDirection.BUY:
            current_low = price_low[-1]
            lips_val = lips[-1]
            jaw_val = jaw[-1]
            
            if current_low > lips_val:  # Above lips
                if bar_position == BarPosition.ABOVE:
                    if mouth_phase == MouthPhase.OPENING:
                        return WaterState.SWITCHING
                    elif len(lips) >= 2 and prev_low < lips[-2]:  # Previous was below lips
                        return WaterState.POPING
                    else:
                        return WaterState.SPLASHING
                        
            elif current_low < lips_val:  # Below lips
                if bar_position == BarPosition.IN:
                    if current_low > jaw_val:  # Above jaw
                        return WaterState.THROWING
                    elif len(lips) >= 2 and prev_low > lips[-2]:  # Previous was above lips
                        return WaterState.ENTERING
                    else:
                        return WaterState.EATING
        
        # Default cases
        if mouth_phase in [MouthPhase.SLEEPING, MouthPhase.NONE]:
            return WaterState.SLEEPING
        elif bar_position == BarPosition.IN and mouth_phase in [MouthPhase.CLOSING, MouthPhase.OPENING]:
            return WaterState.SWITCHING
        elif bar_position != prev_bar_pos:
            return WaterState.ENTERING
        else:
            return WaterState.EATING
    
    def analyze_single_bar(
        self,
        price_high: float,
        price_low: float,
        ao_value: float,
        jaw: Sequence[float],
        teeth: Sequence[float],
        lips: Sequence[float],
        gator_oscillator: Optional[Sequence[float]] = None
    ) -> AlligatorMouthWaterState:
        """Analyze a single bar and return complete state information."""
        # Calculate mouth direction and confidence
        mouth_direction, confidence = self.calculate_mouth_direction_extended(jaw, teeth, lips)
        
        # Calculate mouth phase
        mouth_phase = self.calculate_mouth_phase_extended(jaw, teeth, lips, gator_oscillator)
        
        # Calculate bar position
        bar_position = self.calculate_bar_position(
            price_high, price_low, jaw[-1], teeth[-1], lips[-1]
        )
        
        # Calculate water state (needs sequences for momentum analysis)
        price_high_seq = [price_high] if isinstance(price_high, (int, float)) else price_high
        price_low_seq = [price_low] if isinstance(price_low, (int, float)) else price_low
        ao_seq = [ao_value] if isinstance(ao_value, (int, float)) else ao_value
        
        water_state = self.calculate_water_state_extended(
            price_high_seq, price_low_seq, ao_seq,
            jaw, teeth, lips, mouth_direction, mouth_phase, bar_position
        )
        
        # Detect transitions
        transition_detected = False
        if self._previous_state is not None:
            transition_detected = (
                self._previous_state.mouth_direction != mouth_direction or
                self._previous_state.mouth_phase != mouth_phase or
                self._previous_state.water_state != water_state
            )
        
        # Create state object
        current_state = AlligatorMouthWaterState(
            mouth_direction=mouth_direction,
            mouth_phase=mouth_phase,
            bar_position=bar_position,
            water_state=water_state,
            confidence_score=confidence,
            transition_detected=transition_detected
        )
        
        # Store for next iteration
        self._previous_state = current_state
        
        return current_state


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
