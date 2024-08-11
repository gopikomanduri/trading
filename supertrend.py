# supertrend.py

import pandas as pd

def calculate_supertrend(df, period=7, multiplier=3):
    df['ATR'] = df['Close'].rolling(window=period).std() * multiplier
    df['UpperBand'] = ((df['High'] + df['Low']) / 2) + df['ATR']
    df['LowerBand'] = ((df['High'] + df['Low']) / 2) - df['ATR']
    df['Supertrend'] = df['UpperBand']
    
    for i in range(1, len(df)):
        if df['Close'][i] > df['Supertrend'][i-1]:
            df['Supertrend'][i] = df['LowerBand'][i]
        elif df['Close'][i] < df['Supertrend'][i-1]:
            df['Supertrend'][i] = df['UpperBand'][i]
        else:
            df['Supertrend'][i] = df['Supertrend'][i-1]
    
    return df['Supertrend']
