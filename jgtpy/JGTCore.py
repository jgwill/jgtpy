import json
from collections import namedtuple
from json import JSONEncoder
import os
import pathlib
from pathlib import Path

__version__ = "0.1.7"

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

def jsonfile2prop(__jsonfile):
    _jsonfile=pathlib.Path(__jsonfile).resolve()
    #_jsonfile= os.path.abspath(__jsonfile)
    print(_jsonfile)
    with open(_jsonfile, 'r') as f:
      d=f.read()
      return json.loads(d)

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

