from api import trade_stock
from data_handler import fetch_and_process_data, moving_average
from strategy import moving_average_crossover
from config import SYMBOL, SHORT_WINDOW, LONG_WINDOW, TRADE_AMOUNT

def execute_trade(data=None):
    if data is None:
        date_from = "01.01.2023 00:00"
        date_to = "now"
        data = fetch_and_process_data(SYMBOL, date_from, date_to, TIMEFRAME)
    
    if data.empty:
        print("No data available to trade.")
        return

    signal = moving_average_crossover(data, SHORT_WINDOW, LONG_WINDOW)
    
    if signal == 'buy':
        trade_stock(SYMBOL, TRADE_AMOUNT, 'buy')
        log_trade('buy')
    elif signal == 'sell':
        trade_stock(SYMBOL, TRARE_AMOUNT, 'sell')
        log_trade('sell')

def log_trade(action):
    global trade_logs
    trade_logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action.upper()} {TRADE_AMOUNT} of {SYMBOL}")
