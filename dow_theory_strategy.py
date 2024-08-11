# # dow_theory_strategy.py

# import time
# import pandas as pd
# import numpy as np
# import threading
# from config import symbol, qty
# from trading import fetch_real_time_data, place_buy_order, place_sell_order

# buy_price = None

# def identify_trend(df):
#     df['Higher_High'] = np.nan
#     df['Lower_Low'] = np.nan

#     for i in range(1, len(df)-1):
#         if df['High'].iloc[i] > df['High'].iloc[i-1] and df['High'].iloc[i] > df['High'].iloc[i+1]:
#             df.at[i, 'Higher_High'] = df['High'].iloc[i]
#         if df['Low'].iloc[i] < df['Low'].iloc[i-1] and df['Low'].iloc[i] < df['Low'].iloc[i+1]:
#             df.at[i, 'Lower_Low'] = df['Low'].iloc[i]

#     df['Uptrend'] = df['Higher_High'].notnull() & df['Higher_High'].shift(-1).isnull()
#     df['Downtrend'] = df['Lower_Low'].notnull() & df['Lower_Low'].shift(-1).isnull()

#     return df

# def trading_strategy():
#     global buy_price
#     df = pd.DataFrame(columns=['Close', 'High', 'Low'])

#     while True:
#         # Fetch real-time data and append to DataFrame
#         price = fetch_real_time_data(symbol)
#         if price is not None:
#             new_row = {'Close': price, 'High': price, 'Low': price}
#             new_row_df = pd.DataFrame([new_row])
#             df = pd.concat([df, new_row_df], ignore_index=True)
            
#             if len(df) > 3:  # Ensure enough data points for trend identification
#                 df = identify_trend(df)
                
#                 # Trading logic based on Dow Theory
#                 if df['Uptrend'].iloc[-2] and buy_price is None:
#                     buy_price = place_buy_order(symbol, qty)
#                 elif df['Downtrend'].iloc[-2] and buy_price is not None:
#                     sell_price = place_sell_order(symbol, qty)
#                     buy_price = None  # Reset buy price after sell order
                
#         time.sleep(60)  # Wait for a minute before fetching new data

# if __name__ == "__main__":
#     # Run the trading strategy in a separate thread
#     strategy_thread = threading.Thread(target=trading_strategy)
#     strategy_thread.start()

# dow_theory_strategy.py
# dow_theory_strategy.py

import time
import pandas as pd
import numpy as np
import threading
from config import symbol, qty
from trading import fetch_real_time_data, place_buy_order, place_sell_order



dow_theory_buy_price = None

def calculate_dow_theory_signals(df):
    df['High'] = df['Close'].rolling(window=20).max()
    df['Low'] = df['Close'].rolling(window=20).min()
    df['Buy_Signal'] = np.where(df['Close'] > df['High'].shift(1), 1, 0)
    df['Sell_Signal'] = np.where(df['Close'] < df['Low'].shift(1), 1, 0)
    return df

def trading_strategy(shared_data_queue):
    print("In dow theory  trading strategy")
    global dow_theory_buy_price
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
                df = calculate_dow_theory_signals(df)

                if df['Buy_Signal'].iloc[-1] == 1 and dow_theory_buy_price is None:
                    dow_theory_buy_price = place_buy_order(symbol, qty, 'Dow_Theory')
                    print(f"Dow Theory Buy Order: Price = {dow_theory_buy_price}, Time = {pd.Timestamp.now()}")
                elif df['Sell_Signal'].iloc[-1] == 1 and dow_theory_buy_price is not None:
                    if df['Close'].iloc[-1] >= 1.1 * dow_theory_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'Dow_Theory')
                        print(f"Dow Theory Sell Order: Price = {sell_price}, Time = {pd.Timestamp.now()}")
                        dow_theory_buy_price = None  # Reset buy price after sell order
                    elif df['Close'].iloc[-1] < 0.8 * dow_theory_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'Dow_Theory')
                        print(f'Stop loss hit at {sell_price}')
                        dow_theory_buy_price = None  # Reset buy price after sell order

        time.sleep(1)  # Sleep for a short duration to avoid busy waiting

if __name__ == "__main__":
    # shared_data_queue should be passed from the main script
    raise NotImplementedError("This script should be run as part of the main combined_strategies script.")
