import json
from collections import namedtuple
from json import JSONEncoder
import os
import pathlib
from pathlib import Path

__version__ = "0.1.31"

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
      if not quiet:
        print(_jsonfile+ " loaded")
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



