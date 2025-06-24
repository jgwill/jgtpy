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
import argparse
import sys
import os

# Add jgtpy path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtutils import jgtcommon
import JGTCDS as cds


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


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Alligator Mouth and Water State Analysis CLI",
        epilog="Analyze market data using enhanced Alligator mouth and water state logic."
    )
    
    # Core arguments
    parser.add_argument(
        "-i", "--instrument", 
        required=True,
        help="Instrument symbol (e.g., EUR/USD, SPX500)"
    )
    parser.add_argument(
        "-t", "--timeframe",
        required=True, 
        help="Timeframe (e.g., D1, H4, H1, M15)"
    )
    
    # Output options
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: auto-generated based on instrument/timeframe)"
    )
    parser.add_argument(
        "--output-format",
        choices=["csv", "json", "both"],
        default="csv",
        help="Output format (default: csv)"
    )
    
    # Analysis options
    parser.add_argument(
        "--lookback-periods",
        type=int,
        default=3,
        help="Number of lookback periods for analysis (default: 3)"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=1e-8,
        help="Threshold for mouth phase detection (default: 1e-8)"
    )
    
    # Data options
    parser.add_argument(
        "--use-full",
        action="store_true",
        help="Use full dataset"
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Data directory (default: from JGTPY_DATA env var or standard location)"
    )
    
    # Verbosity
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv, -vvv)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output"
    )
    
    return parser.parse_args()


def load_cds_data(instrument: str, timeframe: str, data_dir: Optional[str] = None, use_full: bool = False) -> pd.DataFrame:
    """Load CDS data for the given instrument and timeframe."""
    # Determine data directory
    if data_dir is None:
        data_dir = os.environ.get("JGTPY_DATA", os.path.join(os.path.dirname(__file__), "..", "data", "current"))
    
    # Build file path
    filename = f"{instrument.replace('/', '-')}__{timeframe}.csv" if use_full else f"{instrument.replace('/', '-')}_{timeframe}.csv"
    filepath = os.path.join(data_dir, "cds", filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CDS file not found: {filepath}")
    
    # Load the data and set the date index for easier time based access
    df = pd.read_csv(filepath, parse_dates=["Date"])
    if "Date" in df.columns:
        df.set_index("Date", inplace=True)
    
    # Ensure we have the required columns
    required_cols = ['jaw', 'teeth', 'lips', 'ao', 'High', 'Low']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Required columns missing from CDS data: {missing_cols}")
    
    return df


def analyze_dataframe(df: pd.DataFrame, lookback_periods: int = 3, threshold: float = 1e-8, verbose: int = 0) -> pd.DataFrame:
    """Analyze the entire dataframe and add mouth/water state columns."""
    analyzer = AlligatorMouthWaterAnalyzer(lookback_periods=lookback_periods, threshold=threshold)
    
    # Initialize result columns
    df = df.copy()
    df['mouth_direction'] = 'neither'
    df['mouth_phase'] = 'none'
    df['bar_position'] = 'in'
    df['water_state'] = 'sleeping'
    df['mouth_confidence'] = 0.0
    df['state_transition'] = False
    
    if verbose > 0:
        print(f"Analyzing {len(df)} bars...")
    
    # Analyze each bar (need at least lookback_periods bars for analysis)
    for i in range(lookback_periods, len(df)):
        try:
            # Get the required sequences
            jaw_seq = df['jaw'].iloc[max(0, i-lookback_periods):i+1].values
            teeth_seq = df['teeth'].iloc[max(0, i-lookback_periods):i+1].values
            lips_seq = df['lips'].iloc[max(0, i-lookback_periods):i+1].values
            ao_seq = df['ao'].iloc[max(0, i-lookback_periods):i+1].values
            high_seq = df['High'].iloc[max(0, i-lookback_periods):i+1].values
            low_seq = df['Low'].iloc[max(0, i-lookback_periods):i+1].values
            
            # Perform analysis
            state = analyzer.analyze_single_bar(
                price_high=df['High'].iloc[i],
                price_low=df['Low'].iloc[i],
                ao_value=df['ao'].iloc[i],
                jaw=jaw_seq,
                teeth=teeth_seq,
                lips=lips_seq
            )
            
            # Store results
            df.loc[df.index[i], 'mouth_direction'] = state.mouth_direction.value
            df.loc[df.index[i], 'mouth_phase'] = state.mouth_phase.value
            df.loc[df.index[i], 'bar_position'] = state.bar_position.value
            df.loc[df.index[i], 'water_state'] = state.water_state.value
            df.loc[df.index[i], 'mouth_confidence'] = state.confidence_score
            df.loc[df.index[i], 'state_transition'] = state.transition_detected
            
        except Exception as e:
            if verbose > 1:
                print(f"Warning: Analysis failed for bar {i}: {e}")
            continue
    
    if verbose > 0:
        print(f"Analysis complete. Added mouth/water state columns.")
        
        # Print summary statistics
        print("\nMouth Direction Distribution:")
        print(df['mouth_direction'].value_counts())
        print("\nWater State Distribution:")
        print(df['water_state'].value_counts())
        
        transitions = df['state_transition'].sum()
        print(f"\nState transitions detected: {transitions}")
    
    return df


def save_results(df: pd.DataFrame, instrument: str, timeframe: str, output_path: Optional[str] = None, 
                output_format: str = "csv", data_dir: Optional[str] = None, verbose: int = 0) -> str:
    """Save analysis results to file."""
    if output_path is None:
        # Auto-generate output path
        if data_dir is None:
            data_dir = os.environ.get("JGTPY_DATA", os.path.join(os.path.dirname(__file__), "..", "data", "current"))
        
        # Create mouth_water subdirectory
        output_dir = os.path.join(data_dir, "mouth_water")
        os.makedirs(output_dir, exist_ok=True)
        
        base_filename = f"{instrument.replace('/', '-')}_{timeframe}_mouth_water"
        output_path = os.path.join(output_dir, base_filename)
    
    # Save based on format
    saved_files = []
    
    if output_format in ["csv", "both"]:
        csv_path = f"{output_path}.csv"
        df.to_csv(csv_path, index=False)
        saved_files.append(csv_path)
        if verbose > 0:
            print(f"Saved CSV: {csv_path}")
    
    if output_format in ["json", "both"]:
        json_path = f"{output_path}.json"
        df.to_json(json_path, orient="records", date_format="iso")
        saved_files.append(json_path)
        if verbose > 0:
            print(f"Saved JSON: {json_path}")
    
    return saved_files[0] if len(saved_files) == 1 else saved_files


def main():
    """Main CLI entry point."""
    args = _parse_args()
    
    if not args.quiet:
        print("Alligator Mouth and Water State Analysis CLI")
        print("=" * 50)
    
    try:
        # Load CDS data
        if not args.quiet and args.verbose > 0:
            print(f"Loading CDS data for {args.instrument}_{args.timeframe}...")
        
        df = load_cds_data(
            args.instrument, 
            args.timeframe, 
            data_dir=args.data_dir,
            use_full=args.use_full
        )
        
        if not args.quiet:
            print(f"Loaded {len(df)} bars of data")
        
        # Perform analysis
        if not args.quiet and args.verbose > 0:
            print("Performing mouth and water state analysis...")
        
        analyzed_df = analyze_dataframe(
            df,
            lookback_periods=args.lookback_periods,
            threshold=args.threshold,
            verbose=args.verbose if not args.quiet else 0
        )
        
        # Save results
        saved_files = save_results(
            analyzed_df,
            args.instrument,
            args.timeframe,
            output_path=args.output,
            output_format=args.output_format,
            data_dir=args.data_dir,
            verbose=args.verbose if not args.quiet else 0
        )
        
        if not args.quiet:
            print("\nAnalysis complete!")
            if isinstance(saved_files, list):
                for file in saved_files:
                    print(f"Results saved to: {file}")
            else:
                print(f"Results saved to: {saved_files}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose > 1:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
