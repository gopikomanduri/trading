# volume_open_interest_strategy.py

import time
import pandas as pd
import numpy as np
import threading
import config as cr
from config import symbol, qty
from trading import fetch_real_time_data, place_buy_order, place_sell_order
from fyers_apiv3 import fyersModel


volume_oi_buy_price = None

def calculate_volume_oi_signals(df):
    df['Volume_Signal'] = np.where(df['Volume'] > df['Volume'].shift(1), 1, 0)
    df['OI_Signal'] = np.where(df['OI'] > df['OI'].shift(1), 1, 0)
    df['Buy_Signal'] = np.where((df['Volume_Signal'] == 1) & (df['OI_Signal'] == 1), 1, 0)
    df['Sell_Signal'] = np.where((df['Volume_Signal'] == 0) & (df['OI_Signal'] == 0), 1, 0)
    return df

def trading_strategy(shared_data_queue):
    print("In volume OI trading strategy")
    global volume_oi_buy_price
    df = pd.DataFrame(columns=['Close', 'Volume', 'OI'])

    while True:
        if not shared_data_queue.empty():
            market_data = shared_data_queue.get()
            new_row = {
                'Close': market_data['ltp'],
                'Volume': market_data['v'],
                'OI': market_data['oi']
            }
            new_row_df = pd.DataFrame([new_row])

            if df.empty:
                df = new_row_df
            else:
                df = pd.concat([df, new_row_df], ignore_index=True)

            if len(df) > 1:  # Ensure enough data points for decision making
                df = calculate_volume_oi_signals(df)

                if df['Buy_Signal'].iloc[-1] == 1 and volume_oi_buy_price is None:
                    volume_oi_buy_price = place_buy_order(symbol, qty, 'Volume_OI')
                    print(f"Volume OI Buy Order: Price = {volume_oi_buy_price}, Time = {pd.Timestamp.now()}")
                elif df['Sell_Signal'].iloc[-1] == 1 and volume_oi_buy_price is not None:
                    if df['Close'].iloc[-1] >= 1.1 * volume_oi_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'Volume_OI')
                        print(f"Volume OI Sell Order: Price = {sell_price}, Time = {pd.Timestamp.now()}")
                        volume_oi_buy_price = None  # Reset buy price after sell order
                    elif df['Close'].iloc[-1] < 0.8 * volume_oi_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'Volume_OI')
                        print(f'Stop loss hit at {sell_price}')
                        volume_oi_buy_price = None  # Reset buy price after sell order

        time.sleep(1)  # Sleep for a short duration to avoid busy waiting

if __name__ == "__main__":
    # shared_data_queue should be passed from the main script
    raise NotImplementedError("This script should be run as part of the main combined_strategies script.")
