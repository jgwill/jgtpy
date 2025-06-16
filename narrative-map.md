# Narrative Map

## Commit Timeline

- c49510e: expand Alligator mouth state spec
- e4b6746: applying previous commit introducing CLI docs and main entry point.
- b440b49: add example scripts for each CLI

- 3956666: Applying previous commit introducing example READMEs.

- 5d69b85: Applying previous commit introducing extended examples and CLI docs.
- <pending>: add Examples section to llms.txt.

These changes document the command line tools and provide runnable examples to showcase usage.

- <pending>: add Alligator water and mouth state specification.

### Alligator Water & Mouth Spec

The file `specs/AlligatorWaterMouthState.spec.md` now contains a detailed description of how the Alligator indicator is interpreted. For quick reference the entire spec is reproduced below.



```markdown
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
    
    
    ## 5. Mouth Direction and Phase
    
    The strategy breaks the mouth state into **direction** and **phase** as outlined in the `jgwill/jgtstrategies` research notes:
    
    - **Direction** expresses bias:
      - **Buy** – jaw, teeth and lips slope upward and lips are above teeth which are above the jaw.
      - **Sell** – jaw, teeth and lips slope downward and lips are below teeth which are below the jaw.
      - **Neither** – any other configuration.
    - **Phase** expresses separation between lines:
      - **Open** – lines are well separated and aligned with the direction.
      - **Closed** – lines are intertwined or nearly crossing.
      - **Opening** – direction has just shifted and the lines are starting to separate.
      - **None** – no clear pattern.
    
    Both direction and phase feed into trade filters. A change in phase often triggers a `signal_alligator_mouth_state_changed` event in the strategy layer.
    
    ## 6. Detailed Water States
    
    When price interacts with the mouth, the water state describes how price "swims" relative to the jaw, teeth and lips:
    
    - **Splashing** – price outside the mouth as it moves away in the direction of the trend.
    - **Eating** – price inside the mouth but still trending with direction.
    - **Throwing** – price deep inside the mouth and pushing against the jaw line.
    - **Poping** – price outside the mouth with previous bar showing a potential reversal.
    - **Entering** – price sliding back inside the mouth after being outside.
    - **Switching** – price still inside while the mouth transitions from opening to closing or vice versa.
    
    These labels help scripts react to transitional bars or stop conditions.
    
    ## 7. Implementation Hints
    
    The Lua functions `parse_mouth_dir_state` and `parse_mouth_bs_state_barpos__water` from `jgwill/jgtstrategies` encapsulate the above logic. They examine current and previous bar positions to emit `mouth_dir`, `mouth_state`, `mouth_bar_pos` and `water_state` values. Refer to those functions when porting the logic to Python.
    
```

