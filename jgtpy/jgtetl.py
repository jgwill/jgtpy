
from datetime import datetime
from datetime import timedelta

def offsetdt(time_str,nbhoursoffset=4,date_format_str= '%m/%d/%Y %H:%M:%S',output_dt_format='%Y-%m-%d %H:%M:%S'):
  given_time = datetime.strptime(time_str, date_format_str)
  final_time = given_time + timedelta(hours=nbhoursoffset)
  final_time_str = final_time.strftime(output_dt_format) 
  return final_time_str

def svc_offset_dt_by_tf(ori_time_str,_tf,direction=-1,amount=89,date_format_str= '%m/%d/%Y %H:%M:%S',output_dt_format='%Y-%m-%d %H:%M:%S'):
  _nbhour = pto_nbhourbytfofoffset2212(_tf,amount) * direction
  _r = offsetdt(ori_time_str,_nbhour,date_format_str,output_dt_format)
  return _r
#@STCStatus We Need 89 Periods to prepare the First Frame of our Data
def pto_nbhourbytfofoffset2212(_tf,amount=89):
  _r=1
  if _tf == "m1":
    _r = 1* amount
  if _tf == "mi1":
    _r = 1* amount
  if _tf == "min1":
    _r = 1* amount
  if _tf == "m5":
    _r = 5* amount
  if _tf == "m15":
    _r = 15* amount
  if _tf == "m30":
    _r = 30* amount
  if _tf == "H1":
    _r = 60* amount
  if _tf == "H2":
    _r = 120* amount
  if _tf == "H3":
    _r = 180* amount
  if _tf == "H4":
    _r = 240* amount
  if _tf == "H6":
    _r = 360* amount
  if _tf == "H8":
    _r = 480* amount
  if _tf == "D1":
    _r = 1440* amount
  if _tf == "W1":
    _r = 10080* amount
  if _tf == "M1":
    _r = 43200* amount
  return round(_r / 60)
  
