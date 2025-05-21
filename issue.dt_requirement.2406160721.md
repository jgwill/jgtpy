* _dt_requirements in def _get_ph_surely_fresh(... should be UTC and 

should return a date requirement that is different according to the timeframe and if the market is closed


Refactor using this rule about the trading hours : 
>Open: Sundays, between 5:00 and 5:15 pm EST. Close: Fridays, around 4:55 pm EST. Closed: Fridays 5:00 pm to Sunday 5:00 pm EST.

If we are the weekend, we will want that '_dt_requirements' to be the moment it closed.  Consider it is different foreach timeframes.ex. value when it closes : 

```
M1 : 2024-05-31 21:00:00
W1 : 2024-06-08 21:00:00
D1 : 2024-06-13 21:00:00
H8 : 2024-06-14 13:00:00
H6 : 2024-06-14 15:00:00
H4 : 2024-06-14 17:00:00
H3 : 2024-06-14 18:00:00
H2 : 2024-06-14 19:00:00
H1 : 2024-06-14 20:00:00
m30 : 2024-06-14 20:30:00
m15 : 2024-06-14 20:30:00
m5 : 2024-06-14 20:40:00
m1 : 2024-06-14 20:44:00
```


----
----
# granularizing with a get dt required


new function that get the supposed datetime for a timeframe according to a received input datetime.  Example for input datetime "2024-06-14 20:45:00" : 


```
M1 : 2024-05-31 21:00:00
W1 : 2024-06-08 21:00:00
D1 : 2024-06-13 21:00:00
H8 : 2024-06-14 13:00:00
H6 : 2024-06-14 15:00:00
H4 : 2024-06-14 17:00:00
H3 : 2024-06-14 18:00:00
H2 : 2024-06-14 19:00:00
H1 : 2024-06-14 20:00:00
m30 : 2024-06-14 20:30:00
m15 : 2024-06-14 20:30:00
m5 : 2024-06-14 20:40:00
m1 : 2024-06-14 20:44:00
```

## Observed pattern for rules is 

* always the last completed period
* it means: for M1 the previous month, W1 the last week, etc
