import pandas as pd
from jgtutils.jgtconstants import MFI,MFI_SQUAT,MFI_GREEN,MFI_FADE,MFI_FAKE,MFI_SIGNAL,MFI_VAL,MFI_SQUAT_STR,MFI_FAKE_STR,MFI_FADE_STR,MFI_GREEN_STR,MFI_SQUAT_ID,MFI_FAKE_ID,MFI_FADE_ID,MFI_GREEN_ID

def mfi_str_to_id(mfi_str:str):
    if mfi_str == MFI_SQUAT_STR:
        return MFI_SQUAT_ID
    elif mfi_str == MFI_FAKE_STR:
        return MFI_FAKE_ID
    elif mfi_str == MFI_FADE_STR:
        return MFI_FADE_ID
    elif mfi_str == MFI_GREEN_STR:
        return MFI_GREEN_ID
    else:
        return 0

def mfi_signal_to_str(mfi_signal:int):
    if mfi_signal == MFI_SQUAT:
        return MFI_SQUAT_STR
    elif mfi_signal == MFI_FAKE:
        return MFI_FAKE_STR
    elif mfi_signal == MFI_FADE:
        return MFI_FADE_STR
    elif mfi_signal == MFI_GREEN:
        return MFI_GREEN_STR
    else:
        return "0"

def mfi_id_to_str(mfi_id:int):
    """
    Convert the MFI ID to its string representation.
    
    Parameters:
    mfi_id (int): The MFI ID to convert to its string representation.
    
    Returns:
    str: The string representation of the MFI ID.
    
    Possible values:
    - MFI_SQUAT_ID: MFI_SQUAT_STR
    - MFI_FAKE_ID: MFI_FAKE_STR
    - MFI_FADE_ID: MFI_FADE_STR
    - MFI_GREEN_ID: MFI_GREEN_STR
    - 0: "0"
    
    """
    if mfi_id == MFI_SQUAT_ID:
        return MFI_SQUAT_STR
    elif mfi_id == MFI_FAKE_ID:
        return MFI_FAKE_STR
    elif mfi_id == MFI_FADE_ID:
        return MFI_FADE_STR
    elif mfi_id == MFI_GREEN_ID:
        return MFI_GREEN_STR
    else:
        return "0"

def get_mfi_features_column_list_by_timeframe(t:str):
    """
    Get the list of columns that are MFI features for the given timeframe and its related timeframes.
    
    Parameters:
    t (str): The timeframe to get the MFI features columns for.
    
    Returns:
    list: The list of columns that are MFI features for the given timeframe and its related timeframes
    """
    mfi_str_selected_columns = [MFI_VAL+'_M1',MFI_VAL+'_W1']
    
    if t=='H4' or t=='H8' or t=='H6' or t=='H1' or t=='m15' or t=='m5':
      mfi_str_selected_columns.append(MFI_VAL+'_D1')
      
    if t=='H1' or t=='m15' or t=='m5':
        mfi_str_selected_columns.append(MFI_VAL+'_H4')
        
    if t=='m15' or t=='m5':
        mfi_str_selected_columns.append(MFI_VAL+'_H1')
    
    if t=='m5':
        mfi_str_selected_columns.append(MFI_VAL+'_m15')
        
    mfi_str_selected_columns.append(MFI_VAL)
    return mfi_str_selected_columns


def column_mfi_str_in_dataframe_to_id(df:pd.DataFrame,t:str):
    """
    Convert the MFI string columns in the dataframe to their corresponding MFI ID.
    
    Parameters:
    df (pd.DataFrame): The dataframe to convert the MFI string columns to their corresponding MFI ID.
    t (str): The timeframe to get the MFI features columns for.
    
    Returns:
    pd.DataFrame: The dataframe with the MFI string columns converted to their corresponding MFI ID.
    """
    mfi_str_selected_columns=get_mfi_features_column_list_by_timeframe(t)
    for col_name in mfi_str_selected_columns:
        #check if the column exists in the dataframe
        if col_name not in df.columns:
            continue
        df[col_name] = df[col_name].apply(lambda x: int(mfi_str_to_id(x)))
    return df

def column_mfi_str_back_to_str_in_dataframe(df:pd.DataFrame,t:str):
    mfi_str_selected_columns=get_mfi_features_column_list_by_timeframe(t)
    for col_name in mfi_str_selected_columns:
        #check if the column exists in the dataframe
        if col_name not in df.columns:
            continue
        df[col_name] = df[col_name].apply(lambda x: mfi_id_to_str(x)).copy()
    return df