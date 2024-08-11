# # trading.py

# from fyers_apiv3 import fyersModel
# from config import client_id, access_token, symbol, qty

# fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)

# def fetch_real_time_data(symbol):
#     data = fyers.quotes({'symbols': symbol})
#     print(data)
#     if data['s'] == 'ok':
#         return data['d'][0]['v']['lp']
#     return None


# def place_buy_order(symbol, qty):
#     data = {"symbol": symbol, "qty": qty, "type": 2, "side": 1, "productType": "CNC", "limitPrice": 0, "stopPrice": 0, "validity": "DAY", "disclosedQty": 0, "offlineOrder": "False", "stopLoss": 0, "takeProfit": 0}
#     response = 'ok'
#     if response == 'ok':
#         buy_price = fetch_real_time_data(symbol)
#         print(f'Buy order placed at {buy_price}')
#         return buy_price
#     return None

# def place_sell_order(symbol, qty):
#     data = {"symbol": symbol, "qty": qty, "type": 2, "side": -1, "productType": "CNC", "limitPrice": 0, "stopPrice": 0, "validity": "DAY", "disclosedQty": 0, "offlineOrder": "False", "stopLoss": 0, "takeProfit": 0}
#     response = 'ok'
#     if response == 'ok':
#         sell_price = fetch_real_time_data(symbol)
#         print(f'Sell order placed at {sell_price}')
#         return sell_price
#     return None



# def place_buy_order_org(symbol, qty):
#     data = {"symbol": symbol, "qty": qty, "type": 2, "side": 1, "productType": "CNC", "limitPrice": 0, "stopPrice": 0, "validity": "DAY", "disclosedQty": 0, "offlineOrder": "False", "stopLoss": 0, "takeProfit": 0}
#     response = fyers.place_order(data)
#     if response['s'] == 'ok':
#         buy_price = fetch_real_time_data(symbol)
#         print(f'Buy order placed at {buy_price}')
#         return buy_price
#     return None

# def place_sell_order_org(symbol, qty):
#     data = {"symbol": symbol, "qty": qty, "type": 2, "side": -1, "productType": "CNC", "limitPrice": 0, "stopPrice": 0, "validity": "DAY", "disclosedQty": 0, "offlineOrder": "False", "stopLoss": 0, "takeProfit": 0}
#     response = fyers.place_order(data)
#     if response['s'] == 'ok':
#         sell_price = fetch_real_time_data(symbol)
#         print(f'Sell order placed at {sell_price}')
#         return sell_price
#     return None

# trading.py

from fyers_apiv3 import fyersModel
from config import client_id, access_token, symbol, qty
from datetime import datetime

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)

def fetch_real_time_data(symbol):
    data = fyers.quotes({'symbols': symbol})
    print("fetched quote data ")
    print(data)
    if data['s'] == 'ok':
        return data['d'][0]['v']['lp']
    return None

def place_buy_order(symbol, qty, indicator):
    data = {"symbol": symbol, "qty": qty, "type": 2, "side": 1, "productType": "CNC", "limitPrice": 0, "stopPrice": 0, "validity": "DAY", "disclosedQty": 0, "offlineOrder": "False", "stopLoss": 0, "takeProfit": 0}
    response = 'ok' #fyers.place_order(data)
    # if response['s'] == 'ok':
    if response == 'ok':
        buy_price = fetch_real_time_data(symbol)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'Buy order placed at {buy_price} by {indicator} at {timestamp}')
        return buy_price
    return None

def place_sell_order(symbol, qty, indicator):
    data = {"symbol": symbol, "qty": qty, "type": 2, "side": -1, "productType": "CNC", "limitPrice": 0, "stopPrice": 0, "validity": "DAY", "disclosedQty": 0, "offlineOrder": "False", "stopLoss": 0, "takeProfit": 0}
    response =  'ok' #fyers.place_order(data)
    if response == 'ok':
        sell_price = fetch_real_time_data(symbol)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'Sell order placed at {sell_price} by {indicator} at {timestamp}')
        return sell_price
    return None

