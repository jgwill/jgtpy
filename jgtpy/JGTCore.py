import json
from collections import namedtuple
from json import JSONEncoder
import os
import pathlib
from pathlib import Path
import pandas as pd

__version__ = "0.1.77"

from datetime import datetime
from datetime import timedelta
def offsetdt(time_str,nbhoursoffset=4,date_format_str= '%m/%d/%Y %H:%M:%S',output_dt_format='%Y-%m-%d %H:%M:%S'):
  given_time = datetime.strptime(time_str, date_format_str)
  final_time = given_time + timedelta(hours=nbhoursoffset)
  final_time_str = final_time.strftime(output_dt_format) 
  return final_time_str
  
def fixdtindf(dfsrc,fieldname="dt",n=4,date_format_str= '%m/%d/%Y %H:%M:%S',output_dt_format='%Y-%m-%d %H:%M:%S'):
  #date_format_str = '%m/%d/%Y %H:%M:%S' #06/08/2022 09:00:00
  dfo=pd.DataFrame()
  for index,row in dfsrc.iterrows():
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
    dfsrc.at[index,fieldname]=final_time_str
    #_df[index][fieldname]=final_time_str
    # row['dt'] = final_time_str
    #df[index]['dt'] = final_time_str
    #dfo[index]=row
  return dfsrc
  
#@title Functions Json decode dict
def povRequestDecoder(povReqDict):
	return jgt_povRequestDecoder(povReqDict) #name changes
	
def jgt_povRequestDecoder(povReqDict):
	return namedtuple('X', povReqDict.keys())(*povReqDict.values())
 
def jgtjson_Decoder(dicsrc):
	return namedtuple('X', dicsrc.keys())(*dicsrc.values())

def json2prop(jsonsrc):
    _dic=json.loads(jsonsrc)
    return namedtuple('X', _dic.keys())(*_dic.values())

def d2p(dicsrc):
    return namedtuple('X', dicsrc.keys())(*dicsrc.values())

def json2dict(jsonsrc):
    _dic=json.loads(jsonsrc)
    return namedtuple('X', _dic.keys())(*_dic.values())

def jsonfile2prop(__jsonfile,quiet=False):
    _jsonfile=pathlib.Path(__jsonfile).resolve()
    #_jsonfile= os.path.abspath(__jsonfile)
    with open(_jsonfile, 'r') as f:
      d=f.read()
      return json.loads(d)

def jsonfile2dict(jsoninputfile):
    _dic=jsonfile2prop(jsoninputfile)
    return namedtuple('X', _dic.keys())(*_dic.values())

def json_DecodeHierarchy(dicParentJSON,targetProp):
	dicParent=json.loads(dicParentJSON)
	dicResult=dicParent[targetProp]
	#print(_dic)
	return namedtuple('X', dicResult.keys())(*dicResult.values())

def jgtjson_DecodeHierarchy(dicParentJSON,targetProp):
    return json_DecodeHierarchy(dicParentJSON,targetProp)

def cnf_Decoder(cnfDict):
	return json.loads(cnfDict)
    #return namedtuple('X', cnfDict.keys())(*cnfDict.values())
def jgt_cnf_Decoder(cnfDict):
    return jgt_cnf_Decoder(cnfDict)



