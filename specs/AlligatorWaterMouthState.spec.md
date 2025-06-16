# Alligator Water & Mouth State Logic

This specification outlines how the **Alligator** indicator is interpreted to derive two behavioral states used by trading models in this repository.

## 1. Inputs

- `jaw`, `teeth`, and `lips` series representing the Alligator moving averages.
- `gator_oscillator` values measuring the distance between the lines.
- `awesome_oscillator` (AO) values to judge momentum relative to the waterline (zero).

## 2. Mouth State

The *mouth state* reflects how widely the Alligator lines diverge or converge.

1. **Opening** – consecutive bars show increasing distance between `jaw` and `teeth` *and* between `teeth` and `lips`. This hints at the start of a trend.
2. **Open** – distances remain wide. The market is trending and the Alligator is "eating".
3. **Closing** – distances shrink after being open. Momentum may be fading.
4. **Sleeping** – distances are minimal; lines intertwine. The market lacks direction.

The gator oscillator can be used to measure these distance changes: growing bars indicate opening, shrinking bars indicate closing, and near‑zero bars mean sleeping.

## 3. Water State

The *water state* uses the AO zero line to determine directional bias.

- **Above Water** – AO is greater than zero, implying upward momentum.
- **Below Water** – AO is less than zero, implying downward momentum.

A crossing of the zero line signals a possible shift in water state.

## 4. Combined Interpretation

Trading logic can combine mouth and water states. Examples:

- **Feeding Up** – mouth open or opening *and* AO above water.
- **Feeding Down** – mouth open or opening *and* AO below water.
- **Sleeping Underwater** – mouth sleeping or closing while AO remains below water.

These combined states help scripts decide when to enter or exit positions or when to avoid trading due to consolidation.

