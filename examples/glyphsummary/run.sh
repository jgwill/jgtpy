#!/usr/bin/env bash
# Show glyphsummary output in both emoji and ASCII styles

glyphsummary -i AUD-CAD -t m5 --n-bars 3 --data-dir ../../data/current
echo
glyphsummary -i AUD-CAD -t m5 --n-bars 3 --data-dir ../../data/current --style ascii --show-position
