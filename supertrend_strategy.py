# main.py

import time
import pandas as pd
import numpy as np
import threading
from config import symbol, qty
from trading import fetch_real_time_data, place_buy_order, place_sell_order



supertrend_buy_price = None

def calculate_supertrend(df, period=14, multiplier=3):
    df['ATR'] = df['Close'].rolling(window=period).std()  # Simplified ATR calculation
    df['Upperband'] = df['Close'] + (multiplier * df['ATR'])
    df['Lowerband'] = df['Close'] - (multiplier * df['ATR'])
    df['In_Uptrend'] = np.where(df['Close'] > df['Upperband'], 1, 0)
    df['In_Downtrend'] = np.where(df['Close'] < df['Lowerband'], 1, 0)
    return df

def trading_strategy(shared_data_queue):
    print("In supertrend trading strategy")
    global supertrend_buy_price
    df = pd.DataFrame(columns=['Close'])

    while True:
        if not shared_data_queue.empty():
            market_data = shared_data_queue.get()
            price = market_data['ltp']
            new_row = {'Close': price}
            new_row_df = pd.DataFrame([new_row])

            if df.empty:
                df = new_row_df
            else:
                df = pd.concat([df, new_row_df], ignore_index=True)

            if len(df) > 1:  # Ensure enough data points for decision making
                df = calculate_supertrend(df)

                if df['In_Uptrend'].iloc[-1] == 1 and supertrend_buy_price is None:
                    supertrend_buy_price = place_buy_order(symbol, qty, 'Supertrend')
                    print(f"Supertrend Buy Order: Price = {supertrend_buy_price}, Time = {pd.Timestamp.now()}")
                elif df['In_Downtrend'].iloc[-1] == 1 and supertrend_buy_price is not None:
                    if df['Close'].iloc[-1] >= 1.1 * supertrend_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'Supertrend')
                        print(f"Supertrend Sell Order: Price = {sell_price}, Time = {pd.Timestamp.now()}")
                        supertrend_buy_price = None  # Reset buy price after sell order
                    elif df['Close'].iloc[-1] < 0.8 * supertrend_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'Supertrend')
                        print(f'Stop loss hit at {sell_price}')
                        supertrend_buy_price = None  # Reset buy price after sell order

        time.sleep(120)  # Sleep for a short duration to avoid busy waiting

if __name__ == "__main__":
    # shared_data_queue should be passed from the main script
    raise NotImplementedError("This script should be run as part of the main combined_strategies script.")
