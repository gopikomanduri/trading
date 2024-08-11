

# import threading
# import queue
# from data_fetcher import data_fetcher
# import main
# import macd_rsi_volume_strategy
# import dow_theory_strategy
# import volume_open_interest_strategy

# shared_data_queue = queue.Queue()

# # Start data fetcher thread
# data_fetcher_thread = threading.Thread(target=data_fetcher, args=(shared_data_queue,))
# data_fetcher_thread.start()

# # Start Supertrend strategy thread
# supertrend_thread = threading.Thread(target=main.trading_strategy, args=(shared_data_queue,))
# supertrend_thread.start()

# # Start MACD-RSI-Volume strategy thread
# macd_rsi_volume_thread = threading.Thread(target=macd_rsi_volume_strategy.trading_strategy, args=(shared_data_queue,))
# macd_rsi_volume_thread.start()

# # Start Dow Theory strategy thread
# dow_theory_thread = threading.Thread(target=dow_theory_strategy.trading_strategy, args=(shared_data_queue,))
# dow_theory_thread.start()

# # Start Volume and Open Interest strategy thread
# volume_open_interest_thread = threading.Thread(target=volume_open_interest_strategy.trading_strategy, args=(shared_data_queue,))
# volume_open_interest_thread.start()

# # Join threads to the main thread
# data_fetcher_thread.join()
# supertrend_thread.join()
# macd_rsi_volume_thread.join()
# dow_theory_thread.join()
# volume_open_interest_thread.join()

# combined_strategies.py

import threading
import queue
from data_fetcher import data_fetcher
import supertrend_strategy
import macd_rsi_volume_strategy
import dow_theory_strategy
import volume_open_interest_strategy
import price_action_strategy

shared_data_queue = queue.Queue()

# Start data fetcher thread
data_fetcher_thread = threading.Thread(target=data_fetcher, args=(shared_data_queue,))
data_fetcher_thread.start()

# Start Supertrend strategy thread
supertrend_thread = threading.Thread(target=supertrend_strategy.trading_strategy, args=(shared_data_queue,))
supertrend_thread.start()

# Start MACD-RSI-Volume strategy thread
# macd_rsi_volume_thread = threading.Thread(target=macd_rsi_volume_strategy.trading_strategy, args=(shared_data_queue,))
# macd_rsi_volume_thread.start()

# # Start Dow Theory strategy thread
# dow_theory_thread = threading.Thread(target=dow_theory_strategy.trading_strategy, args=(shared_data_queue,))
# dow_theory_thread.start()

# # Start Volume and Open Interest strategy thread
# volume_open_interest_thread = threading.Thread(target=volume_open_interest_strategy.trading_strategy, args=(shared_data_queue,))
# volume_open_interest_thread.start()

# # Start Price Action strategy thread
# price_action_thread = threading.Thread(target=price_action_strategy.trading_strategy, args=(shared_data_queue,))
# price_action_thread.start()

# Join threads to the main thread
data_fetcher_thread.join()
supertrend_thread.join()
# macd_rsi_volume_thread.join()
# dow_theory_thread.join()
# volume_open_interest_thread.join()
# price_action_thread.join()
