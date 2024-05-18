import logging
from trading.api import trade_stock
from data.data_handler import get_historical_data, moving_average
from strategies.strategy import moving_average_crossover

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_trade(symbol, short_window, long_window, trade_amount, timeframe):
    data = get_historical_data(symbol, "01.01.2023 00:00", "now", timeframe)
    if data.empty:
        logging.warning("No data available to trade.")
        return

    signal = moving_average_crossover(data, short_window, long_window)
    
    if signal == 'buy':
        trade_stock(symbol, trade_amount, 'buy')
        log_trade('buy', trade_amount, symbol)
    elif signal == 'sell':
        trade_stock(symbol, trade_amount, 'sell')
        log_trade('sell', trade_amount, symbol)

def log_trade(action, amount, symbol):
    logging.info(f"{action.upper()} {amount} of {symbol}")
