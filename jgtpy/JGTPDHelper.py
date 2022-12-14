#@title PD Columen Cleanup Functions

def jgtpd_drop_col_by_name(_df,colname,_axis = 1,_quiet=False):
  """Drop Column in DF by Name

  Args:
        _df (DataFrame source)
        ctxcolname (column name from)
        _axis (  axis)
        _quiet (quiet output)
        
  Returns:
    Clean DataFrame 
  """
  if colname in _df.columns:
    return _df.drop(_df.loc[:, colname:colname].columns,axis = _axis)
  else:
    if not _quiet:
      print('Col:' + colname + ' was not there')
    return _df

def __ids_cleanse_ao_peak_secondary_columns(_df,_quiet=False):
  _df=jgtpd_drop_col_by_name(_df,'p0',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p1',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p2',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p3',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p4',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p5',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p6',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p7',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p8',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p9',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p10',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p11',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p12',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p13',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p14',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p15',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p16',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p17',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p18',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p19',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p20',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p21',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p22',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p23',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p24',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p25',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p26',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p27',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p28',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p29',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'p30',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n0',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n1',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n2',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n3',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n4',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n5',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n6',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n7',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n8',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n9',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n10',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n11',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n12',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n13',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n14',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n15',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n16',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n17',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n18',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n19',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n20',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n21',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n22',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n23',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n24',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n25',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n26',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n27',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n28',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n29',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'n30',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao0',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao1',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao2',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao3',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao4',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao5',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao6',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao7',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao8',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao9',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao10',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao11',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao12',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao13',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao14',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao15',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao16',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao17',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao18',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao19',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao20',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao21',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao22',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao23',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao24',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao25',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao26',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao27',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao28',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao29',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao30',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao0',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao1',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao2',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao3',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao4',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao5',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao6',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao7',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao8',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao9',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao10',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao11',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao12',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao13',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao14',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao15',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao16',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao17',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao18',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao19',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao20',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao21',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao22',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao23',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao24',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao25',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao26',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao27',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao28',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao29',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao30',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac0',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac1',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac2',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac3',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac4',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac5',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac6',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac7',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac8',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac9',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac0',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac1',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac2',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac3',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac4',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac5',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac6',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac7',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac8',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac9',1,_quiet) 
  return _df

def pds_cleanse_original_columns(_df,_quiet=True):
  _df=jgtpd_drop_col_by_name(_df,'AskHigh',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'BidHigh',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'AskLow',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'BidLow',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'AskClose',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'BidClose',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'BidOpen',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'AskOpen',1,_quiet)
  return _df

def pds_cleanse_extra_columns(_df,_quiet=True):
  _df=pds_cleanse_original_columns(_df,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'LowisBellowJaw',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'HighisAboveJaw',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'LowisBellowTeeth',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'HighisAboveTeeth',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'HighisAboveLips',1,_quiet)
  _df=jgtpd_drop_col_by_name(_df,'LowisBellowLips',1,_quiet)
  _df=__ids_cleanse_ao_peak_secondary_columns(_df,_quiet)
  if not _quiet:
    print("Columns cleanup was executed")
  return _df