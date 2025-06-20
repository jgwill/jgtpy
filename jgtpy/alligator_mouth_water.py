"""
Alligator Mouth State and Water State Analysis Library

This module provides enhanced analysis of the Alligator indicator by determining:
1. Mouth Direction: Buy, Sell, Neither
2. Mouth Phase: Opening, Open, Closing, Sleeping
3. Bar Position: Above, In, Below the mouth
4. Water State: Splashing, Eating, Throwing, Poping, Entering, Switching

Based on specifications from issues #28, #16 and jgtstrategies/pull/6.
Implements the logic from Lua functions parse_mouth_dir_state and 
parse_mouth_bs_state_barpos__water with Python enhancements.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Sequence, Tuple, Dict, Optional, List, Union
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
    
    Provides enhanced analysis beyond the basic alligator_state module,
    including multi-period analysis, state transitions, and confidence scoring.
    """
    
    def __init__(self, lookback_periods: int = 3, threshold: float = 1e-8):
        """
        Initialize the analyzer.
        
        Args:
            lookback_periods: Number of periods to look back for trend analysis
            threshold: Minimum threshold for considering lines as separated
        """
        self.lookback_periods = lookback_periods
        self.threshold = threshold
        self._previous_state: Optional[AlligatorMouthWaterState] = None
    
    def calculate_mouth_direction_extended(
        self, 
        jaw: Sequence[float], 
        teeth: Sequence[float], 
        lips: Sequence[float]
    ) -> Tuple[MouthDirection, float]:
        """
        Calculate mouth direction with confidence scoring.
        
        Args:
            jaw: Jaw line values (slowest MA)
            teeth: Teeth line values (medium MA)  
            lips: Lips line values (fastest MA)
            
        Returns:
            Tuple of (direction, confidence_score)
        """
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
        
        # Calculate confidence based on slope magnitude and line separation
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
        """
        Calculate mouth phase with optional Gator Oscillator integration.
        
        Args:
            jaw: Jaw line values
            teeth: Teeth line values
            lips: Lips line values
            gator_oscillator: Optional gator oscillator values
            
        Returns:
            MouthPhase enum value
        """
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
        """
        Calculate where the price bar sits relative to the Alligator mouth.
        
        Args:
            price_high: High price of current bar
            price_low: Low price of current bar
            jaw: Current jaw value
            teeth: Current teeth value
            lips: Current lips value
            
        Returns:
            BarPosition enum value
        """
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
        """
        Calculate water state based on price action, AO momentum, and mouth characteristics.
        
        Args:
            price_high: High price sequence
            price_low: Low price sequence  
            ao_values: Awesome Oscillator values
            jaw: Jaw line values
            teeth: Teeth line values
            lips: Lips line values
            mouth_direction: Current mouth direction
            mouth_phase: Current mouth phase
            bar_position: Current bar position
            
        Returns:
            WaterState enum value
        """
        if len(ao_values) < 2 or len(price_high) < 2 or len(price_low) < 2:
            return WaterState.SLEEPING
            
        ao_current = ao_values[-1]
        ao_above_zero = ao_current > 0
        
        # Previous bar price levels for momentum analysis
        prev_high = price_high[-2]
        prev_low = price_low[-2]
        
        # Get previous bar position for transition detection
        prev_bar_pos = self.calculate_bar_position(
            prev_high, prev_low, jaw[-2], teeth[-2], lips[-2]
        )
        
        # Water state logic based on Lua implementation
        if mouth_direction == MouthDirection.SELL:
            current_high = price_high[-1]
            lips_val = lips[-1]
            jaw_val = jaw[-1]
            
            if current_high < lips_val:  # Below lips
                if bar_position == BarPosition.BELOW:
                    if mouth_phase == MouthPhase.OPENING:
                        return WaterState.SWITCHING
                    elif prev_high > lips[-2]:  # Previous was above lips
                        return WaterState.POPING
                    else:
                        return WaterState.SPLASHING
                        
            elif current_high > lips_val:  # Above lips
                if bar_position == BarPosition.IN:
                    if current_high < jaw_val:  # Below jaw
                        return WaterState.THROWING
                    elif prev_high < lips[-2]:  # Previous was below lips
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
                    elif prev_low < lips[-2]:  # Previous was below lips
                        return WaterState.POPING
                    else:
                        return WaterState.SPLASHING
                        
            elif current_low < lips_val:  # Below lips
                if bar_position == BarPosition.IN:
                    if current_low > jaw_val:  # Above jaw
                        return WaterState.THROWING
                    elif prev_low > lips[-2]:  # Previous was above lips
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
        """
        Analyze a single bar and return complete state information.
        
        Args:
            price_high: High price of current bar
            price_low: Low price of current bar
            ao_value: Awesome Oscillator value
            jaw: Jaw line sequence (needs at least 2 values)
            teeth: Teeth line sequence (needs at least 2 values)
            lips: Lips line sequence (needs at least 2 values)
            gator_oscillator: Optional gator oscillator sequence
            
        Returns:
            AlligatorMouthWaterState object with complete analysis
        """
        # Calculate mouth direction and confidence
        mouth_direction, confidence = self.calculate_mouth_direction_extended(jaw, teeth, lips)
        
        # Calculate mouth phase
        mouth_phase = self.calculate_mouth_phase_extended(jaw, teeth, lips, gator_oscillator)
        
        # Calculate bar position
        bar_position = self.calculate_bar_position(
            price_high, price_low, jaw[-1], teeth[-1], lips[-1]
        )
        
        # Calculate water state (needs sequences for momentum analysis)
        water_state = self.calculate_water_state_extended(
            [price_high] if isinstance(price_high, (int, float)) else price_high,
            [price_low] if isinstance(price_low, (int, float)) else price_low,
            [ao_value] if isinstance(ao_value, (int, float)) else ao_value,
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
    
    def analyze_dataframe(
        self,
        df: pd.DataFrame,
        high_col: str = "High",
        low_col: str = "Low", 
        ao_col: str = "AO",
        jaw_col: str = "JAW",
        teeth_col: str = "TEETH",
        lips_col: str = "LIPS",
        gator_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Analyze an entire DataFrame and add mouth/water state columns.
        
        Args:
            df: Input DataFrame with OHLC and indicator data
            high_col: Name of high price column
            low_col: Name of low price column
            ao_col: Name of Awesome Oscillator column
            jaw_col: Name of jaw line column
            teeth_col: Name of teeth line column
            lips_col: Name of lips line column
            gator_col: Optional name of gator oscillator column
            
        Returns:
            DataFrame with added columns:
            - mouth_direction
            - mouth_phase  
            - bar_position
            - water_state
            - mouth_confidence
            - state_transition
        """
        result_df = df.copy()
        
        # Initialize result columns
        mouth_directions = []
        mouth_phases = []
        bar_positions = []
        water_states = []
        confidences = []
        transitions = []
        
        # Reset state for new analysis
        self._previous_state = None
        
        for i in range(len(df)):
            if i < self.lookback_periods:
                # Not enough data for analysis
                mouth_directions.append(MouthDirection.NEITHER.value)
                mouth_phases.append(MouthPhase.NONE.value)
                bar_positions.append(BarPosition.IN.value)
                water_states.append(WaterState.SLEEPING.value)
                confidences.append(0.0)
                transitions.append(False)
                continue
            
            # Get sequences for analysis
            jaw_seq = df[jaw_col].iloc[max(0, i-self.lookback_periods):i+1].values
            teeth_seq = df[teeth_col].iloc[max(0, i-self.lookback_periods):i+1].values
            lips_seq = df[lips_col].iloc[max(0, i-self.lookback_periods):i+1].values
            
            gator_seq = None
            if gator_col and gator_col in df.columns:
                gator_seq = df[gator_col].iloc[max(0, i-self.lookback_periods):i+1].values
            
            # Analyze current bar
            state = self.analyze_single_bar(
                price_high=df[high_col].iloc[i],
                price_low=df[low_col].iloc[i],
                ao_value=df[ao_col].iloc[i],
                jaw=jaw_seq,
                teeth=teeth_seq,
                lips=lips_seq,
                gator_oscillator=gator_seq
            )
            
            # Store results
            mouth_directions.append(state.mouth_direction.value)
            mouth_phases.append(state.mouth_phase.value)
            bar_positions.append(state.bar_position.value)
            water_states.append(state.water_state.value)
            confidences.append(state.confidence_score)
            transitions.append(state.transition_detected)
        
        # Add columns to DataFrame
        result_df['mouth_direction'] = mouth_directions
        result_df['mouth_phase'] = mouth_phases
        result_df['bar_position'] = bar_positions
        result_df['water_state'] = water_states
        result_df['mouth_confidence'] = confidences
        result_df['state_transition'] = transitions
        
        return result_df


def generate_combined_signals(
    mouth_direction: str,
    mouth_phase: str,
    water_state: str,
    ao_momentum: float
) -> Dict[str, Union[bool, str]]:
    """
    Generate combined trading signals based on mouth and water states.
    
    Args:
        mouth_direction: Current mouth direction
        mouth_phase: Current mouth phase
        water_state: Current water state
        ao_momentum: Current AO value
        
    Returns:
        Dictionary of signal flags and descriptions
    """
    signals = {
        'feeding_up': False,
        'feeding_down': False,
        'sleeping_underwater': False,
        'transition_alert': False,
        'signal_description': 'no_signal'
    }
    
    ao_above_zero = ao_momentum > 0
    
    # Feeding signals
    if mouth_phase in ['open', 'opening'] and ao_above_zero and mouth_direction == 'buy':
        signals['feeding_up'] = True
        signals['signal_description'] = 'feeding_up_bullish'
        
    elif mouth_phase in ['open', 'opening'] and not ao_above_zero and mouth_direction == 'sell':
        signals['feeding_down'] = True
        signals['signal_description'] = 'feeding_down_bearish'
    
    # Sleeping underwater
    elif mouth_phase in ['closing', 'sleeping'] and not ao_above_zero:
        signals['sleeping_underwater'] = True
        signals['signal_description'] = 'sleeping_underwater_consolidation'
    
    # Transition alerts
    elif water_state in ['entering', 'switching', 'poping']:
        signals['transition_alert'] = True
        signals['signal_description'] = f'transition_{water_state}'
    
    return signals


def detect_state_changes(
    previous_states: Dict[str, str],
    current_states: Dict[str, str]
) -> Dict[str, bool]:
    """
    Detect changes between previous and current states.
    
    Args:
        previous_states: Previous state values
        current_states: Current state values
        
    Returns:
        Dictionary of change flags
    """
    changes = {}
    
    for key in ['mouth_direction', 'mouth_phase', 'water_state']:
        changes[f'{key}_changed'] = previous_states.get(key) != current_states.get(key)
    
    changes['any_change'] = any(changes.values())
    
    return changes


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


def bar_position(price_high: float, price_low: float, jaw: float, teeth: float, lips: float) -> str:
    """Backward compatible bar position calculation."""
    analyzer = AlligatorMouthWaterAnalyzer()
    position = analyzer.calculate_bar_position(price_high, price_low, jaw, teeth, lips)
    return position.value


def water_state(ao_value: float, bar_pos: str, phase: str) -> str:
    """Simplified water state calculation for backward compatibility."""
    # This is a simplified version - full version requires more context
    if bar_pos == "above" and ao_value > 0:
        return "splashing"
    elif bar_pos == "below" and ao_value < 0:
        return "splashing"
    elif bar_pos == "in" and phase in ["open", "opening"]:
        return "eating"
    elif bar_pos == "in" and phase in ["closing"]:
        return "switching"
    else:
        return "entering" 