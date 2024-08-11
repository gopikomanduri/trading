# data_fetcher.py

import time
import queue
from fyers_apiv3 import fyersModel
# data_fetcher.py

from config import access_token, symbol

# def data_fetcher(shared_data_queue):
#     fyers = fyersModel.FyersModel(client_id="", token=access_token)

#     while True:
#         market_data = fyers.depth({"symbol": symbol, "ohlcv_flag":"1"})['d'][symbol]
#         print(market_data)
#         shared_data_queue.put({
#             'ltp': market_data['ltp'],  # Last traded price
#             'v': market_data['v'],  # Volume
#             'oi': market_data['oi']  # Open Interest
#         })
#         time.sleep(30)  # Fetch data every second to simulate real-time



import datetime
import time
import pandas as pd
import config as cr

# Initialize API
fyers = fyersModel.FyersModel(token=cr.access_token)

def fetch_historical_data(symbol=cr.symbol, resolution="1"):
    """
    Fetch historical data from 9:15 AM to now.
    """
    now = datetime.datetime.now()
    start_time = now.replace(hour=9, minute=15, second=0, microsecond=0)
    if now < start_time:
        start_time = now - datetime.timedelta(days=1)
    end_time = now

    response = fyers.history(symbol=symbol, resolution=resolution, from_date=start_time.strftime('%Y-%m-%dT%H:%M:%S'), to_date=end_time.strftime('%Y-%m-%dT%H:%M:%S'))
    data = response['data']['candles']
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

def fetch_real_time_data(symbol="AAPL"):
    """
    Fetch real-time data.
    """
    response = fyers.quotes(symbol=symbol)
    return response['data']

def data_fetcher(shared_data_queue):
    """
    # Fetch data and put it in a queue for other strategies.
    # """
    # historical_data = fetch_historical_data()
    # # You can use a queue or other data structure to share this data with other threads
    # # For simplicity, we just print it here
    # print("Historical Data:", historical_data)
    
    
    # fyers = fyersModel.FyersModel(client_id=cr.client_id, token=cr.access_token)

    while True:
        market_data = fyers.depth({"symbol": cr.symbol, "ohlcv_flag":"1"})['d'][symbol]
        print(market_data)
        shared_data_queue.put({
            'ltp': market_data['ltp'],  # Last traded price
            'v': market_data['v'],  # Volume
            'oi': market_data['oi']  # Open Interest
        })
        time.sleep(30)  # Fetch data every second to simulate real-time

    # while True:
    #     real_time_data = fetch_real_time_data()
    #     print("Real-time Data:", real_time_data)
    #     time.sleep(60)  # Adjust sleep time as needed

