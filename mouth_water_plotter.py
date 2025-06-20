#!/usr/bin/env python
"""Alligator Mouth Water State Plotter.

Specialized plotting module for visualizing alligator mouth and water states
with appropriate glyphs, symbols, and zone color integration.
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib.figure import Figure
from typing import Dict, List, Tuple, Optional

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtpy.alligator_mouth_water import (
    MouthDirection, MouthPhase, BarPosition, WaterState,
    AlligatorMouthWaterAnalyzer
)
from jgtpy.JGTChartConfig import JGTChartConfig
from jgtpy.JGTADSRequest import JGTADSRequest
import jgtpy.JGTADS as ads
import jgtpy.adshelper as ah
from jgtutils.jgtconstants import (
    HIGH, LOW, CLOSE, OPEN,
    buyingZoneColor, sellingZoneColor, nonTradingZoneColor
)


class MouthWaterPlotConfig:
    """Configuration for mouth water plotting styles and symbols."""
    
    def __init__(self):
        # Water state glyphs and symbols
        self.water_glyphs = {
            WaterState.SPLASHING: "🌊",     # Wave emoji for splashing
            WaterState.EATING: "🍽️",       # Plate emoji for eating
            WaterState.THROWING: "💥",      # Explosion for throwing
            WaterState.POPING: "🎈",        # Balloon for popping
            WaterState.ENTERING: "🚪",      # Door for entering
            WaterState.SWITCHING: "🔄",     # Cycle for switching
            WaterState.SLEEPING: "😴",      # Sleeping for dormant
        }
        
        # Fallback ASCII symbols for environments without emoji support
        self.water_symbols = {
            WaterState.SPLASHING: "s",      # Square for splashing
            WaterState.EATING: "o",         # Circle for eating
            WaterState.THROWING: "X",       # X for throwing
            WaterState.POPING: "^",         # Up arrow for pop
            WaterState.ENTERING: ">",       # Right arrow for entering
            WaterState.SWITCHING: "d",      # Diamond for switching
            WaterState.SLEEPING: ".",       # Dot for sleeping
        }
        
        # Mouth direction symbols
        self.mouth_direction_symbols = {
            MouthDirection.BUY: "^",        # Up triangle for buy
            MouthDirection.SELL: "v",       # Down triangle for sell
            MouthDirection.NEITHER: "D",    # Diamond for neither
        }
        
        # Mouth phase symbols  
        self.mouth_phase_symbols = {
            MouthPhase.OPENING: "D",        # Diamond opening
            MouthPhase.OPEN: "o",           # Open circle
            MouthPhase.CLOSING: "s",        # Square closing
            MouthPhase.SLEEPING: ".",       # Dot sleeping
            MouthPhase.NONE: ".",           # Dot for none
        }
        
        # Bar position symbols
        self.bar_position_symbols = {
            BarPosition.ABOVE: "^",         # Up arrow
            BarPosition.IN: "s",            # Square
            BarPosition.BELOW: "v",         # Down arrow
        }
        
        # Color mappings
        self.mouth_direction_colors = {
            MouthDirection.BUY: "green",
            MouthDirection.SELL: "red", 
            MouthDirection.NEITHER: "gray"
        }
        
        self.water_state_colors = {
            WaterState.SPLASHING: "cyan",
            WaterState.EATING: "orange",
            WaterState.THROWING: "red",
            WaterState.POPING: "magenta",
            WaterState.ENTERING: "blue",
            WaterState.SWITCHING: "yellow",
            WaterState.SLEEPING: "gray"
        }
        
        self.bar_position_colors = {
            BarPosition.ABOVE: "green",
            BarPosition.IN: "orange",
            BarPosition.BELOW: "red"
        }
        
        # Size and positioning
        self.marker_size = 12
        self.last_bar_marker_size = 20  # Larger for last completed bar
        self.text_offset_ratio = 0.02  # Offset for text annotations
        self.use_emojis = False  # Toggle between emojis and ASCII symbols (False for compatibility)


class MouthWaterPlotter:
    """Main plotter class for mouth water states."""
    
    def __init__(self, config: Optional[MouthWaterPlotConfig] = None):
        self.config = config or MouthWaterPlotConfig()
        self.analyzer = AlligatorMouthWaterAnalyzer()
    
    def get_last_completed_state(self, data: pd.DataFrame) -> Tuple[pd.Series, str]:
        """Get the state of the last completed period (second to last row)."""
        if len(data) < 2:
            return None, "Insufficient data"
        
        # Last completed bar (not the current incomplete one)
        last_completed = data.iloc[-2]
        
        state_summary = (
            f"Direction: {last_completed['mouth_direction']} "
            f"Phase: {last_completed['mouth_phase']} "
            f"Position: {last_completed['bar_position']} "
            f"Water: {last_completed['water_state']}"
        )
        
        return last_completed, state_summary
    
    def create_mouth_water_addplots(
        self, 
        data: pd.DataFrame, 
        main_plot_panel_id: int = 0
    ) -> List:
        """Create mouth water state plots for mplfinance addplot."""
        plots = []
        
        # Calculate offset for positioning
        price_range = data[HIGH].max() - data[LOW].min()
        offset = price_range * self.config.text_offset_ratio
        
        # Water State Plot (main indicator)
        water_plots = self._make_water_state_addplots(data, main_plot_panel_id, offset)
        plots.extend(water_plots)
        
        # Mouth Direction Plot
        direction_plots = self._make_mouth_direction_addplots(data, main_plot_panel_id, offset * 2)
        plots.extend(direction_plots)
        
        return plots
    
    def _make_water_state_addplots(self, data: pd.DataFrame, panel_id: int, offset: float):
        """Create water state scatter plots."""
        plots = []
        
        for state in WaterState:
            mask = data['water_state'] == state.value
            if mask.any():
                # Position markers above high prices
                values = np.where(mask, data[HIGH] + offset, np.nan)
                
                # Use ASCII symbols for better compatibility
                symbol = self.config.water_symbols[state]
                color = self.config.water_state_colors[state]
                
                plot = mpf.make_addplot(
                    values,
                    panel=panel_id,
                    type="scatter",
                    markersize=self.config.marker_size,
                    marker=symbol if len(symbol) == 1 else 'o',
                    color=color,
                )
                plots.append(plot)
        
        return plots
    
    def _make_mouth_direction_addplots(self, data: pd.DataFrame, panel_id: int, offset: float):
        """Create mouth direction scatter plots."""
        plots = []
        
        for direction in MouthDirection:
            mask = data['mouth_direction'] == direction.value
            if mask.any():
                # Position markers above high prices with offset
                values = np.where(mask, data[HIGH] + offset, np.nan)
                
                symbol = self.config.mouth_direction_symbols[direction]
                color = self.config.mouth_direction_colors[direction]
                
                plot = mpf.make_addplot(
                    values,
                    panel=panel_id,
                    type="scatter",
                    markersize=self.config.marker_size,
                    marker=symbol if len(symbol) == 1 else '^',
                    color=color,
                )
                plots.append(plot)
        
        return plots
    
    def create_last_state_highlight_plot(self, data: pd.DataFrame, panel_id: int = 0):
        """Create a special plot highlighting the last completed state."""
        if len(data) < 2:
            return None
        
        last_completed = data.iloc[-2]
        
        # Create a large marker for the last completed state
        values = np.full(len(data), np.nan)
        values[-2] = last_completed[HIGH] + (data[HIGH].max() - data[LOW].min()) * 0.05
        
        # Get state info for styling
        water_state = WaterState(last_completed['water_state'])
        mouth_dir = MouthDirection(last_completed['mouth_direction'])
        
        plot = mpf.make_addplot(
            values,
            panel=panel_id,
            type="scatter",
            markersize=self.config.last_bar_marker_size,
            marker='*',  # Star for prominence
            color=self.config.water_state_colors[water_state],
            # Could add label but mplfinance doesn't support it well
        )
        
        return plot
    
    def create_specialized_mouth_water_chart(
        self,
        data: pd.DataFrame,
        instrument: str,
        timeframe: str,
        chart_type: str = "last_state",
        show: bool = True
    ) -> Tuple[Figure, list]:
        """Create specialized mouth water charts.
        
        Args:
            chart_type: 'states_timeline', 'last_state_analysis', 'zone_combined'
        """
        # Ensure mouth water columns exist
        required_cols = ['mouth_direction', 'mouth_phase', 'bar_position', 'water_state']
        if not all(col in data.columns for col in required_cols):
            raise ValueError(f"Data missing mouth water columns. Required: {required_cols}")
        
        last_state, state_summary = self.get_last_completed_state(data)
        
        if chart_type == "states_timeline":
            return self._create_states_timeline_chart(data, instrument, timeframe, show)
        elif chart_type == "last_state_analysis":
            return self._create_last_state_analysis_chart(data, instrument, timeframe, last_state, show)
        elif chart_type == "zone_combined":
            return self._create_zone_combined_chart(data, instrument, timeframe, show)
        else:
            return self._create_last_state_analysis_chart(data, instrument, timeframe, last_state, show)
    
    def _create_states_timeline_chart(self, data: pd.DataFrame, instrument: str, timeframe: str, show: bool):
        """Create chart showing state evolution over time."""
        fig, axes = plt.subplots(4, 1, figsize=(15, 12), sharex=True)
        fig.suptitle(f"{instrument} {timeframe} - Mouth Water States Timeline", fontsize=16)
        
        dates = range(len(data))
        
        # Chart 1: Water States
        ax1 = axes[0]
        water_states = [WaterState(ws).name for ws in data['water_state']]
        unique_water = list(WaterState)
        water_nums = [unique_water.index(WaterState(ws)) for ws in data['water_state']]
        
        colors = [self.config.water_state_colors[WaterState(ws)] for ws in data['water_state']]
        ax1.scatter(dates, water_nums, c=colors, alpha=0.7, s=50)
        ax1.set_title("Water States")
        ax1.set_yticks(range(len(unique_water)))
        ax1.set_yticklabels([ws.name for ws in unique_water])
        ax1.grid(True, alpha=0.3)
        
        # Chart 2: Mouth Direction
        ax2 = axes[1]
        unique_dirs = list(MouthDirection)
        dir_nums = [unique_dirs.index(MouthDirection(md)) for md in data['mouth_direction']]
        dir_colors = [self.config.mouth_direction_colors[MouthDirection(md)] for md in data['mouth_direction']]
        
        ax2.scatter(dates, dir_nums, c=dir_colors, alpha=0.7, s=50)
        ax2.set_title("Mouth Direction")
        ax2.set_yticks(range(len(unique_dirs)))
        ax2.set_yticklabels([md.name for md in unique_dirs])
        ax2.grid(True, alpha=0.3)
        
        # Chart 3: Bar Position
        ax3 = axes[2]
        unique_pos = list(BarPosition)
        pos_nums = [unique_pos.index(BarPosition(bp)) for bp in data['bar_position']]
        pos_colors = [self.config.bar_position_colors[BarPosition(bp)] for bp in data['bar_position']]
        
        ax3.scatter(dates, pos_nums, c=pos_colors, alpha=0.7, s=50)
        ax3.set_title("Bar Position")
        ax3.set_yticks(range(len(unique_pos)))
        ax3.set_yticklabels([bp.name for bp in unique_pos])
        ax3.grid(True, alpha=0.3)
        
        # Chart 4: Zone Colors (if available)
        ax4 = axes[3]
        if 'zcol' in data.columns:
            zone_colors = data['zcol'].values
            zone_map = {'red': 0, 'gray': 1, 'green': 2}
            zone_nums = [zone_map.get(zc, 1) for zc in zone_colors]
            
            ax4.scatter(dates, zone_nums, c=zone_colors, alpha=0.7, s=50)
            ax4.set_title("Zone Colors")
            ax4.set_yticks([0, 1, 2])
            ax4.set_yticklabels(['SELL', 'NEUTRAL', 'BUY'])
        else:
            ax4.text(0.5, 0.5, 'Zone data not available', ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title("Zone Colors (N/A)")
        
        ax4.set_xlabel("Bar Index")
        ax4.grid(True, alpha=0.3)
        
        # Highlight last completed bar
        last_completed_idx = len(data) - 2
        for ax in axes:
            ax.axvline(x=last_completed_idx, color='red', linestyle='--', alpha=0.7, label='Last Completed')
        
        axes[0].legend()
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, axes
    
    def _create_last_state_analysis_chart(self, data: pd.DataFrame, instrument: str, timeframe: str, last_state: pd.Series, show: bool):
        """Create detailed analysis of the last completed state."""
        if last_state is None:
            raise ValueError("No last state available")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f"{instrument} {timeframe} - Last Completed Bar Analysis", fontsize=16)
        
        # Chart 1: State Summary with Symbols
        ax1 = axes[0, 0]
        ax1.axis('off')
        
        water_state = WaterState(last_state['water_state'])
        mouth_dir = MouthDirection(last_state['mouth_direction'])
        mouth_phase = MouthPhase(last_state['mouth_phase'])
        bar_pos = BarPosition(last_state['bar_position'])
        zone_color = last_state.get('zcol', 'N/A')
        confidence = last_state.get('mouth_direction_confidence', 0)
        
        # Create visual summary with symbols
        summary_text = f"""
LAST COMPLETED BAR STATE

Water: {water_state.name} {self.config.water_symbols[water_state]}
Direction: {mouth_dir.name} {self.config.mouth_direction_symbols[mouth_dir]}
Phase: {mouth_phase.name} {self.config.mouth_phase_symbols[mouth_phase]}
Position: {bar_pos.name} {self.config.bar_position_symbols[bar_pos]}
Zone: {zone_color.upper() if isinstance(zone_color, str) else 'N/A'}

Confidence: {confidence:.3f}
        """
        
        ax1.text(0.1, 0.5, summary_text, fontsize=14, verticalalignment='center',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8),
                family='monospace')
        
        # Chart 2: Recent Water State Evolution (last 20 bars)
        ax2 = axes[0, 1]
        recent_data = data.tail(20)
        recent_dates = range(len(recent_data))
        
        water_states = [WaterState(ws) for ws in recent_data['water_state']]
        state_nums = [list(WaterState).index(ws) for ws in water_states]
        colors = [self.config.water_state_colors[ws] for ws in water_states]
        
        ax2.plot(recent_dates, state_nums, 'o-', alpha=0.7)
        ax2.scatter(recent_dates, state_nums, c=colors, s=100, alpha=0.8)
        
        # Highlight last completed (second to last point)
        if len(recent_dates) >= 2:
            ax2.scatter(recent_dates[-2], state_nums[-2], color='red', s=200, marker='*', 
                       label='Last Completed', zorder=5)
        
        ax2.set_title("Recent Water State Evolution")
        ax2.set_xticks(recent_dates[::2])  # Every other tick
        ax2.set_yticks(range(len(WaterState)))
        ax2.set_yticklabels([ws.name[:4] for ws in WaterState])
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Chart 3: State Distribution (pie chart)
        ax3 = axes[1, 0]
        
        # Count water states in recent data
        water_counts = {}
        for ws in recent_data['water_state']:
            water_counts[ws] = water_counts.get(ws, 0) + 1
        
        if water_counts:
            labels = list(water_counts.keys())
            sizes = list(water_counts.values())
            colors_pie = [self.config.water_state_colors[WaterState(label)] for label in labels]
            
            ax3.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
            ax3.set_title("Recent Water State Distribution")
        
        # Chart 4: Zone vs State Matrix
        ax4 = axes[1, 1]
        
        if 'zcol' in data.columns:
            # Create a heatmap-style visualization
            zone_state_matrix = {}
            for _, row in recent_data.iterrows():
                zone = row.get('zcol', 'gray')
                water = row['water_state']
                key = f"{zone}-{water}"
                zone_state_matrix[key] = zone_state_matrix.get(key, 0) + 1
            
            # Simple visualization
            zones = ['red', 'gray', 'green']
            waters = [ws.value for ws in WaterState]
            
            matrix = np.zeros((len(zones), len(waters)))
            for i, zone in enumerate(zones):
                for j, water in enumerate(waters):
                    key = f"{zone}-{water}"
                    matrix[i, j] = zone_state_matrix.get(key, 0)
            
            im = ax4.imshow(matrix, cmap='Blues', aspect='auto')
            ax4.set_xticks(range(len(waters)))
            ax4.set_xticklabels([w[:4] for w in waters], rotation=45)
            ax4.set_yticks(range(len(zones)))
            ax4.set_yticklabels([z.upper() for z in zones])
            ax4.set_title("Zone-State Frequency Matrix")
            
            # Add text annotations
            for i in range(len(zones)):
                for j in range(len(waters)):
                    if matrix[i, j] > 0:
                        ax4.text(j, i, f'{int(matrix[i, j])}', ha="center", va="center")
        else:
            ax4.text(0.5, 0.5, 'Zone data not available', ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title("Zone Analysis (N/A)")
        
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, axes.flatten()
    
    def _create_zone_combined_chart(self, data: pd.DataFrame, instrument: str, timeframe: str, show: bool):
        """Create chart emphasizing zone and mouth water state combinations."""
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle(f"{instrument} {timeframe} - Zone + Mouth Water Analysis", fontsize=16)
        
        dates = range(len(data))
        
        # Chart 1: Price with Zone Background Colors
        ax1 = axes[0]
        
        if 'zcol' in data.columns:
            # Color background based on zones
            for i, (idx, row) in enumerate(data.iterrows()):
                zone = row.get('zcol', 'gray')
                color = zone if zone in ['red', 'green'] else 'lightgray'
                alpha = 0.3 if zone != 'gray' else 0.1
                
                ax1.axvspan(i-0.4, i+0.4, facecolor=color, alpha=alpha)
        
        # Plot price
        ax1.plot(dates, data[CLOSE], 'k-', linewidth=1, label='Close Price')
        ax1.set_title("Price with Zone Background")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Chart 2: Combined State Visualization
        ax2 = axes[1]
        
        # Create combined visualization showing both zone and water state
        for i, (idx, row) in enumerate(data.iterrows()):
            zone = row.get('zcol', 'gray')
            water_state = WaterState(row['water_state'])
            mouth_dir = MouthDirection(row['mouth_direction'])
            
            # Zone position (y-axis)
            zone_pos = {'red': 0, 'gray': 1, 'green': 2}.get(zone, 1)
            
            # Water state affects marker style
            marker_symbol = self.config.water_symbols[water_state]
            color = self.config.mouth_direction_colors[mouth_dir]
            
            # Size based on confidence
            confidence = row.get('mouth_direction_confidence', 0.5)
            size = 50 + confidence * 100
            
            # Use valid matplotlib markers
            valid_marker = 'o' if marker_symbol in ['-', '~', '≈'] else marker_symbol
            
            ax2.scatter(i, zone_pos, c=color, s=size, marker=valid_marker, 
                       alpha=0.7)
        
        ax2.set_title("Zone vs Direction vs Water State")
        ax2.set_yticks([0, 1, 2])
        ax2.set_yticklabels(['SELL ZONE', 'NEUTRAL', 'BUY ZONE'])
        ax2.set_xlabel("Bar Index")
        ax2.grid(True, alpha=0.3)
        
        # Chart 3: State Change Points
        ax3 = axes[2]
        
        # Highlight when states change
        prev_water = None
        prev_zone = None
        change_points = []
        
        for i, (idx, row) in enumerate(data.iterrows()):
            water = row['water_state']
            zone = row.get('zcol', 'gray')
            
            if i > 0 and (water != prev_water or zone != prev_zone):
                change_points.append(i)
            
            prev_water = water
            prev_zone = zone
        
        # Plot change indicators
        if change_points:
            ax3.vlines(change_points, 0, 1, colors='red', alpha=0.7, linewidth=2, 
                      label=f'{len(change_points)} State Changes')
        
        ax3.set_title("State Change Points")
        ax3.set_ylim(0, 1)
        ax3.set_xlabel("Bar Index")
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Highlight last completed bar
        last_completed_idx = len(data) - 2
        for ax in axes:
            ax.axvline(x=last_completed_idx, color='blue', linestyle='--', alpha=0.7, 
                      label='Last Completed' if ax == axes[0] else "")
        
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, axes


def create_mouth_water_cli():
    """Create a CLI interface for mouth water plotting."""
    import argparse
    from jgtutils import jgtcommon
    import jgtpy.JGTCDS as cds
    
    parser = argparse.ArgumentParser(description="Alligator Mouth Water State Plotter")
    parser = jgtcommon.add_instrument_timeframe_arguments(parser)
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of bars")
    parser.add_argument("-ct", "--chart_type", 
                       choices=["states_timeline", "last_state_analysis", "zone_combined"], 
                       default="last_state_analysis", help="Type of chart to create")
    parser.add_argument("--show", action="store_true", default=False, help="Display the chart")
    parser.add_argument("-mw", "--mouth_water_flag", action="store_true", 
                       help="Force mouth water analysis")
    parser.add_argument("-v", "--verbose", type=int, default=0, help="Verbosity level")
    
    args = jgtcommon.parse_args(parser)
    
    try:
        print(f"Creating {args.chart_type} chart for {args.instrument} {args.timeframe}")
        
        # Load CDS data with mouth water analysis
        cc = JGTChartConfig()
        cc.nb_bar_on_chart = args.count
        
        # Get CDS data
        data = cds.createFromPDSFileToCDSFile(
            args.instrument, 
            args.timeframe,
            mouth_water_flag=True,  # Force mouth water analysis
            quiet=args.verbose == 0
        )[1]  # Get the dataframe
        
        if data is None or len(data) == 0:
            print("No data retrieved")
            return
        
        # Check if mouth water columns exist
        required_cols = ['mouth_direction', 'mouth_phase', 'bar_position', 'water_state']
        missing_cols = [col for col in required_cols if col not in data.columns]
        
        if missing_cols:
            print(f"Missing mouth water columns: {missing_cols}")
            print("Available columns:", list(data.columns))
            return
        
        # Create plotter and generate chart
        plotter = MouthWaterPlotter()
        fig, axes = plotter.create_specialized_mouth_water_chart(
            data, args.instrument, args.timeframe, args.chart_type, args.show
        )
        
        # Show last completed state info
        last_state, state_summary = plotter.get_last_completed_state(data)
        if last_state is not None:
            print(f"\nLast Completed Bar State:")
            print(f"  {state_summary}")
            
            # Show with symbols
            water_state = WaterState(last_state['water_state'])
            mouth_dir = MouthDirection(last_state['mouth_direction'])
            print(f"  Symbols: {plotter.config.water_symbols[water_state]} " +
                  f"{plotter.config.mouth_direction_symbols[mouth_dir]}")
        
    except Exception as e:
        if args.verbose > 0:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")


if __name__ == "__main__":
    create_mouth_water_cli() 