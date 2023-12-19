import pandas as pd

# Assuming 'df' is a pandas DataFrame containing the AO and AC values

def categorize_market_state(row):
    """
    Categorizes the market state based on AO and AC values.
    
    :param row: A row from the DataFrame containing 'ao' and 'ac' values.
    :return: A string representing the market state zone category.
    """
    ao = row['ao']
    ac = row['ac']
    
    # Define your rules for categorization based on AO and AC values
    if ao > 0 and ac > 0:
        return 'buy_zone'
    elif ao < 0 and ac < 0:
        return 'sell_zone'
    else:
        return 'neutral_zone'

# Apply the categorization function to each row in the DataFrame
df['market_state_zone'] = df.apply(categorize_market_state, axis=1)

# The 'market_state_zone' column now contains the categorized market state