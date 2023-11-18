cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
make dist && pip uninstall jgtpy -y && \
  pip install dist/jgtpy-$cversion-py3-none-any.whl  && \
  jgtcli -i "USD/CAD" -t "m15" -o -cds -v 2 && echo "--------TST1 passed " && \
  jgtcli -i "USD/CAD,EUR/USD,SPX500" -t "m15,m5,H1,H4,D1,W1" -c 1500 -o -cds -v 2
