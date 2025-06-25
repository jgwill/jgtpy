#!/bin/bash

DEFAULT_SCENARIO="HIGH_TIMEFRAME"
HIGH_TIMEFRAMES="M1 W1 D1 H4"
LOW_TIMEFRAMES="H4 H1 m15 m5"
TIMEFRAMES="$HIGH_TIMEFRAMES"

if [ -z "$TF" ]; then
if [ -z "$1" ]; then
  #echo "No scenario provided, using default: $DEFAULT_SCENARIO"
  SCENARIO=$DEFAULT_SCENARIO
else
  SCENARIO=$1
  TIMEFRAMES="$LOW_TIMEFRAMES"
fi
else
        TIMEFRAMES="$TF"
fi

INSTRUMENTS="EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD"
#if var INST is set, use it
if [ -n "$INST" ]; then
  INSTRUMENTS="$INST"
fi

#default scenario
#s="python jgtpy/glyph_cli.py"
s="python jgtpy/glyph_signals_cli.py"

data_dir=/src/jgtml/data/current
nb_bar=1


echo "------------ $(tlid min)------------"
for i in $INSTRUMENTS;do
        echo "  "
        echo "======= $i ========"
        for t in $TIMEFRAMES;do
                #fp=$(jgtcli -i $i -t $t -vp)
                #ld=$(tail -1 $fp|tr ',' ' '|awk '{print $1" "$2}')
                #echo -n $ld$'\t'$t$': \t'
                echo -n "$t: "$'\t'
                $s -i $i -t $t \
                        --data-dir $data_dir \
                        --n-bars $nb_bar

        done
done


