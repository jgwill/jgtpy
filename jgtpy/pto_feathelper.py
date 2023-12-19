
#@STCGoal Aim to host function for creating the features




#%% Function to calculate Rate of Change for AC values

def calculate_ac_rate_of_change(df, period=1):
    df['AC_Rate_of_Change'] = df['ac'].pct_change(periods=period)
    return df


def test_ac():    
    # Applying the function to the DataFrame
    df = calculate_ac_rate_of_change(df)
    print(df)