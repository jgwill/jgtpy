"""Utilities to interpret Alligator mouth direction and water state.

This module mirrors the Lua helpers from jgtstrategies and exposes
Python equivalents for use in analysis scripts.
"""
from __future__ import annotations

from typing import Sequence, Tuple


def _slope(series: Sequence[float]) -> float:
    if len(series) < 2:
        return 0.0
    return series[-1] - series[-2]


def calculate_mouth_direction(
    jaw: Sequence[float],
    teeth: Sequence[float],
    lips: Sequence[float],
) -> str:
    """Return ``Buy``, ``Sell`` or ``Neither`` based on line slopes and order."""
    jaw_s = _slope(jaw)
    teeth_s = _slope(teeth)
    lips_s = _slope(lips)
    if (
        jaw_s > 0
        and teeth_s > 0
        and lips_s > 0
        and lips[-1] > teeth[-1] > jaw[-1]
    ):
        return "Buy"
    if (
        jaw_s < 0
        and teeth_s < 0
        and lips_s < 0
        and lips[-1] < teeth[-1] < jaw[-1]
    ):
        return "Sell"
    return "Neither"


def calculate_mouth_phase(
    jaw: Sequence[float],
    teeth: Sequence[float],
    lips: Sequence[float],
    threshold: float = 1e-8,
) -> str:
    """Classify separation of lines as Open, Closing, Opening or Closed."""
    dist_prev = (abs(jaw[-2] - teeth[-2]) + abs(teeth[-2] - lips[-2])) / 2.0
    dist_now = (abs(jaw[-1] - teeth[-1]) + abs(teeth[-1] - lips[-1])) / 2.0

    if dist_now > dist_prev:
        return "Opening" if dist_prev < threshold else "Open"
    if dist_now < dist_prev:
        return "Closed" if dist_now < threshold else "Closing"
    return "None"


def bar_position(price: Sequence[float], jaw: Sequence[float], teeth: Sequence[float], lips: Sequence[float]) -> str:
    """Return ``above`` if price is above all lines, ``below`` if below all lines, otherwise ``in``."""
    p = price[-1]
    highest = max(jaw[-1], teeth[-1], lips[-1])
    lowest = min(jaw[-1], teeth[-1], lips[-1])
    if p > highest:
        return "above"
    if p < lowest:
        return "below"
    return "in"


def water_state(ao_value: float, bar_pos: str, phase: str) -> str:
    """Combine AO momentum, bar position and phase to name the water state."""
    above_zero = ao_value > 0

    if bar_pos == "above" and above_zero:
        return "Splashing"
    if bar_pos == "below" and not above_zero:
        return "Splashing"
    if bar_pos == "in" and phase in {"Open", "Opening"}:
        return "Eating"
    if bar_pos == "below" and above_zero:
        return "Throwing"
    if bar_pos == "above" and not above_zero:
        return "Throwing"
    if bar_pos == "above" and not above_zero and phase == "Closing":
        return "Poping"
    if bar_pos == "below" and above_zero and phase == "Closing":
        return "Poping"
    if bar_pos == "in" and phase in {"Closing", "Opening"}:
        return "Switching"
    if bar_pos == "in" and phase == "Closed":
        return "Entering"
    return "Entering"


def parse_alligator_state(
    price: Sequence[float],
    ao: Sequence[float],
    jaw: Sequence[float],
    teeth: Sequence[float],
    lips: Sequence[float],
) -> Tuple[str, str, str, str]:
    """Wrapper returning (mouth_dir, mouth_phase, bar_pos, water_state)."""
    mouth_dir = calculate_mouth_direction(jaw, teeth, lips)
    mouth_phase = calculate_mouth_phase(jaw, teeth, lips)
    bar_pos = bar_position(price, jaw, teeth, lips)
    w_state = water_state(ao[-1], bar_pos, mouth_phase)
    return mouth_dir, mouth_phase, bar_pos, w_state
