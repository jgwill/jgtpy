for t in H1 H4 D1 m15 m5 W1 M1;do for i in "EUR/USD" "AUD/USD" "USD/CAD" "GBP/USD" "SPX500";do jgtcli -i "$i" -t "$t" -cds;done;done
