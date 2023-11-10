#!/bin/bash

# Set the variables to be replaced
declare -A replacements=(
    ["'gray'"]="nonTradingZoneColor"
    ["'red'"]="sellingZoneColor"
    ["'green'"]="buyingZoneColor"
    ["'jaw'"]="indicator_currentDegree_alligator_jaw_column_name"
    ["'teeth'"]="indicator_currentDegree_alligator_teeth_column_name"
    ["'lips'"]="indicator_currentDegree_alligator_lips_column_name"
    ["'bjaw'"]="indicator_sixDegreeLarger_alligator_jaw_column_name"
    ["'bteeth'"]="indicator_sixDegreeLarger_alligator_teeth_column_name"
    ["'blips'"]="indicator_sixDegreeLarger_alligator_lips_column_name"
    ["'ao'"]="indicator_AO_awesomeOscillator_column_name"
    ["'ac'"]="indicator_AC_accelerationDeceleration_column_name"
    ["'aoaz'"]="indicator_AO_aboveZero_column_name"
    ["'aobz'"]="indicator_AO_bellow_zero_column_name"
    ["'zlc'"]="indicator_zeroLineCross_column_name"
    ["'gl'"]="indicator_gatorOscillator_low_column_name"
    ["'gh'"]="indicator_gatorOscillator_high_column_name"
    ["'mfi'"]="indicator_mfi_marketFacilitationIndex_column_name"
    ["'fh'"]="indicator_fractal_high_degree2_column_name"
    ["'fl'"]="indicator_fractal_low_degree2_column_name"
    ["'fh3'"]="indicator_fractal_high_degree3_column_name"
    ["'fl3'"]="indicator_fractal_low_degree3_column_name"
    ["'fh5'"]="indicator_fractal_high_degree5_column_name"
    ["'fl5'"]="indicator_fractal_low_degree5_column_name"
    ["'fh8'"]="indicator_fractal_high_degree8_column_name"
    ["'fl8'"]="indicator_fractal_low_degree8_column_name"
    ["'fh13'"]="indicator_fractal_high_degree13_column_name"
    ["'fl13'"]="indicator_fractal_low_degree13_column_name"
    ["'fh21'"]="indicator_fractal_high_degree21_column_name"
    ["'fl21'"]="indicator_fractal_low_degree21_column_name"
    ["'fh34'"]="indicator_fractal_high_degree34_column_name"
    ["'fl34'"]="indicator_fractal_low_degree34_column_name"
    ["'fh55'"]="indicator_fractal_high_degree55_column_name"
    ["'fl55'"]="indicator_fractal_low_degree55_column_name"
    ["'fh89'"]="indicator_fractal_high_degree89_column_name"
    ["'fl89'"]="indicator_fractal_low_degree89_column_name"
    ["'aof'"]="indicator_ao_fractalPeakOfMomentum_column_name"
    ["'aofvalue'"]="indicator_ao_fractalPeakValue_column_name"
    ["'fdb'"]="signalCode_fractalDivergentBar_column_name"
    ["'fdbs'"]="signalSell_fractalDivergentBar_column_name"
    ["'fdbb'"]="signalBuy_fractalDivergentBar_column_name"
    ["'acs'"]="signalSell_AC_deceleration_column_name"
    ["'acb'"]="signalBuy_AC_acceleration_column_name"
    ["'fs'"]="signalSell_fractal_column_name"
    ["'fb'"]="signalBuy_fractal_column_name"
    ["'zlcb'"]="signalBuy_zeroLineCrossing_column_name"
    ["'zlcs'"]="signalSell_zeroLineCrossing_column_name"
    ["'zcol'"]="signal_zcol_column_name"
    ["'sz'"]="signalSell_zoneSignal_column_name"
    ["'bz'"]="signalBuy_zoneSinal_column_name"
    ["'ss'"]="signalSell_saucer_column_name"
    ["'sb'"]="signalBuy_saucer_column_name"
)

# Find all Python files in the current directory
python_files=$(find . -type f -name "*.py")

# Loop through each Python file
for file in $python_files; do
    echo "Processing $file"
    
    # Counter for replacements in the current file
    replacements_count=0
    
    # Loop through each replacement
    for search in "${!replacements[@]}"; do
        replace="${replacements[$search]}"
        # Count and replace
        count=$(grep -o "$search" "$file" | wc -l)
        replacements_count=$((replacements_count + count))
        sed -i "s/$search/$replace/g" "$file"
    done
    
    # Output the count for the current file
    echo "Replacements in $file: $replacements_count"
done

echo "Replacement complete."
