# # macd_rsi_volume_strategy.py

# import time
# import pandas as pd
# import ta
# from config import symbol, qty
# from trading import fetch_real_time_data, place_buy_order, place_sell_order

# buy_price = None

# def calculate_indicators(df):
#     df['MACD'] = ta.trend.macd(df['Close'])
#     df['MACD_signal'] = ta.trend.macd_signal(df['Close'])
#     df['RSI'] = ta.momentum.rsi(df['Close'])
#     df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
#     return df

# def trading_strategy():
#     global buy_price
#     df = pd.DataFrame(columns=['Close', 'High', 'Low', 'Volume'])

#     while True:
#         # Fetch real-time data
#         price = fetch_real_time_data(symbol)
#         volume = fetch_real_time_data(symbol)  # Adjust to fetch volume data as well
#         if price is not None and volume is not None:
#             new_row = {'Close': price, 'High': price, 'Low': price, 'Volume': volume}
#             new_row_df = pd.DataFrame([new_row])
#             df = pd.concat([df, new_row_df], ignore_index=True)
            
#             # Calculate indicators
#             df = calculate_indicators(df)
            
#             # Trading logic based on MACD, RSI, and volume
#             if (df['MACD'].iloc[-1] > df['MACD_signal'].iloc[-1] and
#                 df['RSI'].iloc[-1] < 70 and
#                 df['Volume'].iloc[-1] > df['Volume_MA'].iloc[-1] and
#                 buy_price is None):
#                 buy_price = place_buy_order(symbol, qty)
#             elif (df['MACD'].iloc[-1] < df['MACD_signal'].iloc[-1] and
#                   df['RSI'].iloc[-1] > 30 and
#                   df['Volume'].iloc[-1] > df['Volume_MA'].iloc[-1] and
#                   buy_price is not None):
#                 sell_price = place_sell_order(symbol, qty)
#                 buy_price = None  # Reset buy price after sell order
                
#         time.sleep(60)  # Wait for a minute before fetching new data

# if __name__ == "__main__":
#     trading_strategy()

# macd_rsi_volume_strategy.py

import time
import pandas as pd
import numpy as np
import threading
from config import symbol, qty
from trading import fetch_real_time_data, place_buy_order, place_sell_order


macd_rsi_volume_buy_price = None

def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    return df

def calculate_rsi(df, period=14):
    delta = df['Close'].diff(1)
    gain = delta.mask(delta < 0, 0)
    loss = -delta.mask(delta > 0, 0)
    avg_gain = gain.ewm(com=(period - 1), min_periods=period).mean()
    avg_loss = loss.ewm(com=(period - 1), min_periods=period).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def trading_strategy(shared_data_queue):
    print("In macd trading strategy")
    global macd_rsi_volume_buy_price
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

            if len(df) > 26:  # Ensure enough data points for decision making
                df = calculate_macd(df)
                df = calculate_rsi(df)

                if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] and df['RSI'].iloc[-1] < 30 and macd_rsi_volume_buy_price is None:
                    macd_rsi_volume_buy_price = place_buy_order(symbol, qty, 'MACD_RSI_Volume')
                    print(f"MACD RSI Volume Buy Order: Price = {macd_rsi_volume_buy_price}, Time = {pd.Timestamp.now()}")
                elif df['MACD'].iloc[-1] < df['Signal'].iloc[-1] and df['RSI'].iloc[-1] > 70 and macd_rsi_volume_buy_price is not None:
                    if df['Close'].iloc[-1] >= 1.1 * macd_rsi_volume_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'MACD_RSI_Volume')
                        print(f"MACD RSI Volume Sell Order: Price = {sell_price}, Time = {pd.Timestamp.now()}")
                        macd_rsi_volume_buy_price = None  # Reset buy price after sell order
                    elif df['Close'].iloc[-1] < 0.8 * macd_rsi_volume_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'MACD_RSI_Volume')
                        print(f'Stop loss hit at {sell_price}')
                        macd_rsi_volume_buy_price = None  # Reset buy price after sell order

        time.sleep(1)  # Sleep for a short duration to avoid busy waiting

if __name__ == "__main__":
    # shared_data_queue should be passed from the main script
    raise NotImplementedError("This script should be run as part of the main combined_strategies script.")
