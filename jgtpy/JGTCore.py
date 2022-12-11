import json
from collections import namedtuple
from json import JSONEncoder
import os
import pathlib
from pathlib import Path

__version__ = "0.1.36"

from datetime import datetime
from datetime import timedelta
def offsetdt(time_str,nbhoursoffset=4,date_format_str= '%m/%d/%Y %H:%M:%S',output_dt_format='%Y-%m-%d %H:%M:%S'):
  given_time = datetime.strptime(time_str, date_format_str)
  final_time = given_time + timedelta(hours=nbhoursoffset)
  final_time_str = final_time.strftime(output_dt_format) 
  return final_time_str
  
def fixdtindf(_df,fieldname="dt",n=4,date_format_str= '%m/%d/%Y %H:%M:%S',output_dt_format='%Y-%m-%d %H:%M:%S'):
  #date_format_str = '%m/%d/%Y %H:%M:%S' #06/08/2022 09:00:00
  dfo=pd.DataFrame()
  for index,row in _df.iterrows():
    #print(index)
    # Given timestamp in string
    time_str = row[fieldname]
    # create datetime object from timestamp string
    given_time = datetime.strptime(time_str, date_format_str)
    #print('Given Time: ', given_time)
    # Add 2 hours to datetime object
    final_time = given_time + timedelta(hours=n)
    #print('Final Time : ', final_time)
    # Convert datetime object to string in specific format 
    final_time_str = final_time.strftime(output_dt_format) #2022-06-08 13:00:00
    #print('Final Time as string object: ', final_time_str)
    _df.at[index,fieldname]=final_time_str
    #_df[index][fieldname]=final_time_str
    # row['dt'] = final_time_str
    #df[index]['dt'] = final_time_str
    #dfo[index]=row
  return _df
  
#@title Functions Json decode dict
def povRequestDecoder(povReqDict):
	return jgt_povRequestDecoder(povReqDict) #name changes
	
def jgt_povRequestDecoder(povReqDict):
	return namedtuple('X', povReqDict.keys())(*povReqDict.values())
 
def jgtjson_Decoder(_dic):
	return namedtuple('X', _dic.keys())(*_dic.values())

def json2prop(_json):
    _dic=json.loads(_json)
    return namedtuple('X', _dic.keys())(*_dic.values())

def d2p(_dic):
    return namedtuple('X', _dic.keys())(*_dic.values())

def json2dict(_json):
    _dic=json.loads(_json)
    return namedtuple('X', _dic.keys())(*_dic.values())

def jsonfile2prop(__jsonfile,quiet=False):
    _jsonfile=pathlib.Path(__jsonfile).resolve()
    #_jsonfile= os.path.abspath(__jsonfile)
    with open(_jsonfile, 'r') as f:
      d=f.read()
      return json.loads(d)

def jsonfile2dict(__jsonfile):
    _dic=jsonfile2prop(__jsonfile)
    return namedtuple('X', _dic.keys())(*_dic.values())

def json_DecodeHierarchy(_dicParentJSON,_targetProp):
	_dicParent=json.loads(_dicParentJSON)
	_dic=_dicParent[_targetProp]
	#print(_dic)
	return namedtuple('X', _dic.keys())(*_dic.values())

def jgtjson_DecodeHierarchy(_dicParentJSON,_targetProp):
    return json_DecodeHierarchy(_dicParentJSON,_targetProp)

def cnf_Decoder(cnfDict):
	return json.loads(cnfDict)
    #return namedtuple('X', cnfDict.keys())(*cnfDict.values())
def jgt_cnf_Decoder(cnfDict):
    return jgt_cnf_Decoder(cnfDict)



