# main.py

from jgtfxc import get_price_history,connect,disconnect,status

status()

connect()

d=get_price_history('EUR/USD', 'H4')
d.to_csv('../EURUSD_H4.csv')
print(d)


status()

d=get_price_history('AUD/USD', 'H4')
d.to_csv('../AUDUSD_H4.csv')
print(d)


disconnect()

status()