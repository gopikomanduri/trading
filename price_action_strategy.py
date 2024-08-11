# price_action_strategy.py

import time
import pandas as pd
import numpy as np
from config import symbol, qty
from trading import place_buy_order, place_sell_order

price_action_buy_price = None

def calculate_price_action_signals(df):
    df['High'] = df['Close'].rolling(window=20).max()
    df['Low'] = df['Close'].rolling(window=20).min()
    df['Buy_Signal'] = np.where(df['Close'] == df['Low'], 1, 0)
    df['Sell_Signal'] = np.where(df['Close'] == df['High'], 1, 0)
    return df

def trading_strategy(shared_data_queue):
    print("In price action trading strategy")
    global price_action_buy_price
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

            if len(df) > 20:  # Ensure enough data points for decision making
                df = calculate_price_action_signals(df)

                if df['Buy_Signal'].iloc[-1] == 1 and price_action_buy_price is None:
                    price_action_buy_price = place_buy_order(symbol, qty, 'Price_Action')
                    print(f"Price Action Buy Order: Price = {price_action_buy_price}, Time = {pd.Timestamp.now()}")
                elif df['Sell_Signal'].iloc[-1] == 1 and price_action_buy_price is not None:
                    if df['Close'].iloc[-1] >= 1.1 * price_action_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'Price_Action')
                        print(f"Price Action Sell Order: Price = {sell_price}, Time = {pd.Timestamp.now()}")
                        price_action_buy_price = None  # Reset buy price after sell order
                    elif df['Close'].iloc[-1] < 0.8 * price_action_buy_price:
                        sell_price = place_sell_order(symbol, qty, 'Price_Action')
                        print(f'Stop loss hit at {sell_price}')
                        price_action_buy_price = None  # Reset buy price after sell order

        time.sleep(1)  # Sleep for a short duration to avoid busy waiting

if __name__ == "__main__":
    # shared_data_queue should be passed from the main script
    raise NotImplementedError("This script should be run as part of the main combined_strategies script.")
