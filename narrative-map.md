# Narrative Map

## Commit Timeline

- c49510e: expand Alligator mouth state spec
- e4b6746: applying previous commit introducing CLI docs and main entry point.
- b440b49: add example scripts for each CLI
- 9d967b7: add Python porting plan for Alligator mouth utilities.

- 3956666: Applying previous commit introducing example READMEs.

- 5d69b85: Applying previous commit introducing extended examples and CLI docs.
- 53db715: add Examples section to llms.txt.

These changes document the command line tools and provide runnable examples to showcase usage.

- 9d967b7: add Alligator water and mouth state specification.
- 9d967b7: expand spec with algorithm outline for direction, phase, and water states.
- 04afaf2: add parity and visualization guidance to spec.
- cd1a53d: add alligator_state module for mouth & water logic.
- cd1a53d: cross-link Lua strategy docs in Alligator spec.
- df45e8f: document output tuple for mouth/water state.

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
    
    ## 8. Algorithm Outline
    
    Below is a high level description of how those Lua utilities operate.  The intent
    is to provide enough guidance for a Python reimplementation while still keeping
    the specification accessible to non-programmers.
    
    1. **Direction Calculation**
       - Evaluate the slope of `jaw`, `teeth` and `lips` over the last two bars.
       - If all three slope upward and maintain the order *lips > teeth > jaw* the
         direction is **Buy**.
       - If all slope downward in the order *lips < teeth < jaw* the direction is
         **Sell**.
       - Any other configuration yields **Neither**.
    
    2. **Phase Determination**
       - Measure the absolute distances between the lines.
       - Growing distances move the phase from *Closed* → *Opening* → *Open*.
       - Shrinking distances reverse the flow: *Open* → *Closing* → *Closed*.
    
    3. **Bar Position**
       - Compare current price to the three lines to know if it is **above**, **in**
         or **below** the mouth.  This position assists with water state names like
         *Entering* or *Throwing*.
    
    4. **Water State Decision**
       - Use AO to check if momentum is **Above** or **Below** the zero line.
       - Merge the bar position and mouth phase to emit final labels such as
         *Splashing* or *Switching*.
    
    This outline is intentionally simplified; corner cases in the Lua scripts handle
    flat markets and data gaps.  Any Python port should replicate those checks so
    the strategy behaves identically across languages.
    
    
    ## 9. Python Porting Plan
    
    The first milestone is to replicate the Lua helpers in a small Python module. This module should expose four functions mirroring the calculation steps above:
    
    1. `calculate_mouth_direction(jaw, teeth, lips)` – return `Buy`, `Sell` or `Neither`.
    2. `calculate_mouth_phase(jaw, teeth, lips)` – determine `Open`, `Closing`, `Opening` or `Closed`.
    3. `bar_position(price, jaw, teeth, lips)` – categorize the current bar as **above**, **in**, or **below** the mouth.
    4. `water_state(ao_value, bar_pos, phase)` – combine AO momentum with the bar position and phase to yield final labels.
    
    When these four pieces are complete, a wrapper can emit `mouth_dir`, `mouth_state` and `water_state` each bar, matching the behavior of the Lua utilities.  The implementation should log mismatches or ambiguous states so they can be reconciled with the original strategy.
    
    ## 10. Edge Cases and Lua Parity
    
    Porting should mirror the Lua reference `parse_mouth_dir_state` and `parse_mouth_bs_state_barpos__water`. Some notable corner cases:
    
    - **Flat markets** – when all lines are nearly horizontal for several bars, freeze the mouth phase to avoid flapping between open and closed.
    - **Gaps in data** – handle missing AO or line values by carrying forward the last valid state.
    - **Naming mismatches** – older Lua scripts label `Poping` as `Popping`. The Python port should accept either spelling for compatibility.
    
    Any deviations from the Lua implementation must be logged so strategies can be validated across languages.
    
    ## 11. Visualization Snippet
    
    To confirm behavior visually, plot the jaw, teeth and lips along with the AO zero line. Color bars by `water_state`:
    
    ```python
    # pseudo-code for visualization
    import matplotlib.pyplot as plt
    
    plt.plot(jaw, label="Jaw")
    plt.plot(teeth, label="Teeth")
    plt.plot(lips, label="Lips")
    plt.axhline(0, color="gray", linestyle="--")  # AO zero line
    plt.scatter(price.index, price, c=water_state_colors)
    plt.legend()
    plt.show()
    ```
    
    This optional snippet helps verify that transitions like *Splashing* or *Entering* align with the indicator data.

    ## 12. Related Lua Implementations

    Development of the mouth and water logic originally happened in the
    `jgwill/jgtstrategies` repository. Several Lua scripts there call the helper
    functions to emit trading signals:

    - `strategies/standard/xpto231120v4.lua` – first reference emitting mouth state events.
    - `strategies/standard/xpto231120v4fix.lua` – bug-fix version with extended state handling.
    - `strategies/standard/xpto231123v4fix_bop.lua` – variant integrating BOP logic.
    - `strategies/standard/xpto231125v4fix.lua` – refined parsing of water state transitions.
    - `strategies/standard/xptoDSPrep231124v5.lua` – dataset preparation script that logs mouth and water states.
    - `stratagies/standard/jgtstrategiesfunctions250523.lua` – function library with `parse_mouth_dir_state` and `parse_mouth_bs_state_barpos__water`.
    - `strategies/standard/_mouth_signal_state_analysis.csv` – example output showing `mouth_dir`, `mouth_state`, `mouth_bar_pos` and `water_state`.

    Copies also exist inside **jgtstratpy** under `jgtstratpy/src/lua_strat/`. See
    `docs/mouth_water_index.md` in `jgwill/jgtstrategies` for the full list. These
    ## 13. Output Structure

    Lua scripts typically emit four values per bar which are logged in `_mouth_signal_state_analysis.csv`:

    - `mouth_dir` – the bias from `Buy`, `Sell` or `Neither`.
    - `mouth_phase` – one of `Open`, `Closed`, `Opening` or `Closing`.
    - `mouth_bar_pos` – whether price is `above`, `in` or `below` the mouth.
    - `water_state` – labels such as `Splashing`, `Eating`, `Throwing`, `Poping`, `Entering` or `Switching`.

    The Python wrapper `parse_alligator_state` should return these four elements so output mirrors the Lua helpers.

    references provide context and test cases when verifying the Python port.
```
