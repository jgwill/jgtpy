#!/usr/bin/env bash
# Generate example charts and save them as images

echo "=== Generating Mouth Water Chart Examples ==="
echo

# Create output directory
mkdir -p output

echo "1. Generating Last State Analysis Chart..."
jgtmouthwater -i EUR/USD -t m5 -c 50 -ct last_state_analysis --save output/last_state_analysis.png > output/last_state_output.txt 2>&1 &
LAST_PID=$!

echo "2. Generating States Timeline Chart..."
jgtmouthwater -i EUR/USD -t m5 -c 100 -ct states_timeline --save output/states_timeline.png > output/timeline_output.txt 2>&1 &
TIMELINE_PID=$!

echo "3. Generating Zone Combined Chart..."
jgtmouthwater -i EUR/USD -t m5 -c 75 -ct zone_combined --save output/zone_combined.png > output/zone_output.txt 2>&1 &
ZONE_PID=$!

# Wait for all processes to complete
wait $LAST_PID
echo "✓ Last state analysis completed"

wait $TIMELINE_PID  
echo "✓ States timeline completed"

wait $ZONE_PID
echo "✓ Zone combined completed"

echo
echo "4. Generated Files:"
ls -la output/

echo
echo "5. Example State Information:"
grep -A 3 "Last Completed Bar State:" output/last_state_output.txt 2>/dev/null || echo "State info not found"

echo
echo "✓ All examples generated successfully!" 