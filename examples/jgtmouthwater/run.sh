#!/usr/bin/env bash
# JGT Mouth Water Plotting Examples
# Demonstrates all chart types and saves example images

echo "=== JGT Mouth Water Plotting Examples ==="
echo

# Display help first
echo "1. Showing help for jgtmouthwater command:"
echo "----------------------------------------"
jgtmouthwater --help
echo

# Ensure we have a clean output directory
mkdir -p output
cd output

echo "2. Generating Last State Analysis Chart (no display)..."
echo "----------------------------------------"
# Generate last state analysis (default) and save output with longer timeout
timeout 300 jgtmouthwater -i EUR/USD -t m5 -c 50 -ct last_state_analysis -v 1 > last_state_output.txt 2>&1
echo "✓ Last state analysis completed - output saved to last_state_output.txt"
echo

echo "3. Generating States Timeline Chart (no display)..."
echo "------------------------------------"
# Generate states timeline chart with longer timeout
timeout 300 jgtmouthwater -i EUR/USD -t m5 -c 100 -ct states_timeline -v 1 > states_timeline_output.txt 2>&1
echo "✓ States timeline completed - output saved to states_timeline_output.txt"
echo

echo "4. Generating Zone Combined Chart (no display)..."
echo "----------------------------------"
# Generate zone combined chart with longer timeout
timeout 300 jgtmouthwater -i EUR/USD -t m5 -c 75 -ct zone_combined -v 1 > zone_combined_output.txt 2>&1
echo "✓ Zone combined completed - output saved to zone_combined_output.txt"
echo

echo "5. Testing Different Instruments..."
echo "---------------------------------"
# Test with different instrument and longer timeout
timeout 300 jgtmouthwater -i GBP/USD -t m15 -c 30 -ct last_state_analysis -v 1 > gbpusd_output.txt 2>&1
echo "✓ GBP/USD analysis completed - output saved to gbpusd_output.txt"
echo

echo "6. Summary of Generated Files:"
echo "-----------------------------"
ls -la *.txt
echo

echo "=== Example Outputs ==="
echo
echo "Last Completed State Information:"
echo "--------------------------------"
grep -A 5 "Last Completed Bar State:" last_state_output.txt 2>/dev/null || echo "State info will be shown when analysis completes"
echo

echo "=== Integration Examples ==="
echo
echo "To use in trading workflow:"
echo "1. Generate CDS data with mouth water analysis:"
echo "   jgtcli -i EUR/USD -t m5 -c 100 -mw"
echo
echo "2. Create specialized visualization:"
echo "   jgtmouthwater -i EUR/USD -t m5 -c 100 -ct last_state_analysis --show"
echo
echo "3. Combine with other indicators:"
echo "   jgtcli -i EUR/USD -t m5 -c 200 -ba -ta -mw -v 1"
echo

echo "=== Chart Types Summary ==="
echo
echo "Available chart types:"
echo "• last_state_analysis (default) - Detailed 2x2 analysis"
echo "• states_timeline              - 4-panel evolution view" 
echo "• zone_combined                - Price + zone integration"
echo

echo "=== Symbol Legend ==="
echo
echo "Water States: s(splash) o(eat) X(throw) ^(pop) >(enter) D(switch) .(sleep)"
echo "Directions:   ^(buy) v(sell) D(neither)"
echo "Positions:    ^(above) s(in) v(below)"
echo

echo "Examples completed! Check the output/ directory for detailed results."
echo "To view charts interactively, add --show flag to any command."
echo "Note: Charts are generated without display to prevent hanging on headless systems." 