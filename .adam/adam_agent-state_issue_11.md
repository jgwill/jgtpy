What are the values of the function 'parse_mouth_bs_state_barpos__water' from file strategies/standard/xptoDSPrep231124v5.lua ?

The function `parse_mouth_bs_state_barpos__water` in the file `strategies/standard/xptoDSPrep231124v5.lua` determines the position of the price relative to the Alligator's mouth and the water state. Here are the possible values and conditions for the function:

* 🏊 **Price Mouth Position**:
  - `in`: If the price is within the Alligator's mouth.
  - `out`: If the price is outside the Alligator's mouth.

* 🌊 **Water State**:
  - `splashing`: If the price is outside the Alligator's mouth and the Alligator's mouth is in a "sell" state with the price below the Lips line.
  - `eating`: If the price is within the Alligator's mouth and the Alligator's mouth is in a "sell" state with the price above the Lips line.
  - `throwing`: If the price is within the Alligator's mouth and the Alligator's mouth is in a "sell" state with the price below the Jaw line.
  - `poping`: If the price is outside the Alligator's mouth and the Alligator's mouth is in a "sell" state with the previous period's price above the Lips line.
  - `entering`: If the price is within the Alligator's mouth and the Alligator's mouth is in a "sell" state with the previous period's price below the Lips line.
  - `switching`: If the price is within the Alligator's mouth and the Alligator's mouth is in a "sell" state with the Alligator's mouth in an "opening" phase.
  - `splashing`: If the price is outside the Alligator's mouth and the Alligator's mouth is in a "buy" state with the price above the Lips line.
  - `eating`: If the price is within the Alligator's mouth and the Alligator's mouth is in a "buy" state with the price below the Lips line.
  - `throwing`: If the price is within the Alligator's mouth and the Alligator's mouth is in a "buy" state with the price above the Jaw line.
  - `poping`: If the price is outside the Alligator's mouth and the Alligator's mouth is in a "buy" state with the previous period's price below the Lips line.
  - `entering`: If the price is within the Alligator's mouth and the Alligator's mouth is in a "buy" state with the previous period's price above the Lips line.
  - `switching`: If the price is within the Alligator's mouth and the Alligator's mouth is in a "buy" state with the Alligator's mouth in an "opening" phase.

These values are used to determine the current state of the Alligator's mouth and the water state, which are essential for making trading decisions based on the Alligator indicator. You can find the implementation of this function in the file `/src/jgtstrategies/strategies/standard/xptoDSPrep231124v5.lua`.



----
----



What are the values of the function 'parse_mouth_dir_state' from file strategies/standard/xptoDSPrep231124v5.lua ?

The function `parse_mouth_dir_state` in the file `strategies/standard/xptoDSPrep231124v5.lua` determines the direction and state of the Alligator's mouth based on the positions of the Jaw, Teeth, and Lips lines. Here are the possible values and conditions for the function:

* 🐊 **Gator Buy/Sell Direction**:
  - `buy`: If the Jaw, Teeth, and Lips lines are all increasing and the Lips line is above the Teeth line, and the Teeth line is above the Jaw line.
  - `sell`: If the Jaw, Teeth, and Lips lines are all decreasing and the Lips line is below the Teeth line, and the Teeth line is below the Jaw line.
  - `neither`: If neither of the above conditions is met.

* 🏊 **Gator Phase State**:
  - `open`: If the Jaw, Teeth, and Lips lines are well-separated and aligned.
  - `closed`: If the Jaw, Teeth, and Lips lines are intertwined or very close together.
  - `opening`: If the Jaw line crosses above the Teeth line while the Teeth line is still below the Lips line (for buy) or if the Jaw line crosses below the Teeth line while the Teeth line is still above the Lips line (for sell).
  - `none`: If none of the above conditions is met.

The function uses these conditions to determine the current state of the Alligator's mouth and returns the appropriate values. You can find the implementation of this function in the file `/src/jgtstrategies/strategies/standard/xptoDSPrep231124v5.lua`.


