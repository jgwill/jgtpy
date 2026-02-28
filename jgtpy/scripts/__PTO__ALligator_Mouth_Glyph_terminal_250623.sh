for i in  EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD;do  echo "======= $i ========";for t in M1 W1 D1 H4;do echo -n $t$': \t';python jgtpy/glyph_cli.py -i $i -t $t --data-dir /src/jgtml/data/current --n-bars 1 --show-position;done;done

echo '
======= EUR/USD ========
M1:     348: 🐊🪥🦷📈
W1:     279: 🐊🪥🦷📈📈
D1:     329: 🐊🪥🦷💧
H4:     329: 🐊🪥🦷💧
======= AUD/CAD ========
M1:     348: 🐊🪥🦷🏊
W1:     279: 🐊🪥🦷🏊
D1:     329: 🐊🪥🦷🏊
H4:     329: 🐊🪥🦷🏊
======= AUD/USD ========
M1:     348: 🐊🪥🦷💧
W1:     279: 🐊🪥🦷💧📈
D1:     329: 🐊🪥🦷🏊
H4:     329: 🐊🪥🦷🏊📈
======= USD/CAD ========
M1:     348: 🐊🪥🦷💧📈
W1:     279: 🐊🪥🦷🏊📈
D1:     329: 🐊🪥🦷💧
H4:     329: 🐊🪥🦷💧📈
======= GBP/USD ========
M1:     348: 🐊🪥🦷📈
W1:     279: 🐊🪥🦷📈📈
D1:     329: 🐊🪥🦷💧
H4:     329: 🐊🪥🦷💧
======= XAU/USD ========
M1:     393: 🐊🪥🦷📈📈
W1:     210: 🐊🪥🦷📈📈
D1:     332: 🐊🪥🦷📈📈
H4:     329: 🐊🪥🦷🏊
'
