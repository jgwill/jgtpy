"""
# Formulation of Target Variable for Machine Learning in Fractal Trading System

To prototype the creation of a target variable for machine learning within a fractal trading system, we will focus on the columns 'fdbb' and 'fdbs' from the dataset. These columns represent the fractal divergent bar (FDB) signals for potential entry points in the market.

## Objective

The objective is to establish a target variable that quantifies the market's movement in the direction opposite to the signal provided by the FDB. This target variable will encapsulate the concept of tension within the market movement post-signal detection, indicating whether the subsequent price action characterizes:
"""

import pandas as pd

df = pd.read_csv("Data.csv")

# Assuming 'df' is the DataFrame with the necessary columns
# 'Close' represents the closing price of each bar
# 'fdbb' and 'fdbs' are columns with binary values indicating the presence of a signal

# Define the window range for monitoring price movement
WINDOW_MIN = 90
WINDOW_MAX = 140
pipsize = 0.0001

def calculate_target_variable(df):
    # Initialize the target column with NaN values
    df['target'] = float('nan')

    # Loop through the DataFrame
    for index, row in df.iterrows():
        # Check for a buy signal
        if row['fdbb'] == 1:
            max_range = index + WINDOW_MAX
            for i in range(index + WINDOW_MIN, min(max_range, len(df))):
                # Check if an opposing sell signal is found
                if df.at[i, 'fdbs'] == 1:
                    t= (df.at[i, 'High'] - row['Low']) / pipsize
                    df.at[index, 'target'] = round(t,2)
                    break
        # Check for a sell signal
        elif row['fdbs'] == 1:
            max_range = index + WINDOW_MAX
            for i in range(index + WINDOW_MIN, min(max_range, len(df))):
                # Check if an opposing buy signal is found
                if df.at[i, 'fdbb'] == 1:
                    t=((row['Low'] - df.at[i, 'High']) * -1) / pipsize
                    df.at[index, 'target'] = round(t,2)
                    break

    # Handle cases where the price exceeds the signal bar's range
    # This part of the code needs to be customized based on how you define 'exceeding the signal bar's range'
    # Example: df.loc[df['some_condition'], 'target'] = 0 or NaN

    # Fill NaN target values for rows where no opposing signal was found within the window range
    df['target'].fillna(0, inplace=True)
    
    return df

# Apply the function to the DataFrame
df = calculate_target_variable(df)

# Output the first few rows to verify the target variable
columns_to_drop = ['jaws_tmp', 'teeth_tmp', 'lips_tmp', 'fdb', 'zcol']
df = df.drop(columns=columns_to_drop)
print(df.head())

df.to_csv("fe-form___output.csv")
dfo = df[["Date","target","Close","fdbb","fdbs"]]
dfo.to_csv("fe-form___.dfo.csv")


"""
- A corrective wave,
- A continuation of a larger impulse wave, or
- A negligible short move that may lead to a loss.

## Conditions for Target Variable Construction

1. The target variable will be contingent on the price action not exceeding the extent of the signal bar itself. If the price moves further than the signal bar in the opposite direction, the signal will be deemed invalid.
2. The target variable will track the price movement for a window of 50-120 bars following the signal.
3. If an opposing signal appears after 50 bars, the position is Closed, and the price movement at that point becomes the target variable's value.

## Proposed Methodology for Target Variable Creation

To construct this target variable, we will use the following approach:

1. **Signal Validation**: Confirm that the price has not moved beyond the signal bar's range in the opposite direction, ensuring the signal's validity.
2. **Price Movement Tracking**: From the point of a valid 'fdbb' or 'fdbs' signal, measure the price movement across the specified bar range (50-120 bars).
3. **Opposing Signal Detection**: Monitor for an opposing 'fdbs' or 'fdbb' signal that may occur within the tracking window. If detected after 50 bars, record the price movement at this juncture.
4. **Data Labeling**: Label the dataset with the quantified movement as the target variable. This will be a numerical representation of the market tension post-signal.

## Implementation Steps

1. **Data Preprocessing**: Clean the dataset for any missing or outlier values, ensuring quality data for the feature engineering process.
2. **Feature Engineering**: Develop an algorithm to calculate the target variable based on the methodology outlined above.
3. **Data Labeling**: Apply the algorithm to the dataset, labeling each instance with the target variable.
4. **Model Training**: Utilize the newly labeled dataset to train your machine learning model, tuning it to recognize patterns associated with market tension and potential profitable exits.

By following this methodology, we will create a machine learning model that can better assess the potential of fractal divergent bars within the context of market dynamics, improving the decision-making process for trade entries and exits.

### Next Steps

Once you have reviewed the proposed methodology, the next step is to begin implementing the feature engineering algorithm that will create the target variable. This will involve programming the logic to assess price movement, signal validity, and the detection of opposing signals within the specified bar range. After this, testing the algorithm on historical data will be crucial to ensure its accuracy and effectiveness.

"""