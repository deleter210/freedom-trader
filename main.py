import time
from config.config import SYMBOL, SHORT_WINDOW, LONG_WINDOW, TRADE_AMOUNT, TIMEFRAME
from data.data_handler import fetch_and_process_data, fetch_stock_list, moving_average
from strategies.strategy import moving_average_crossover
from trading.trader import execute_trade


def main():
    while True:
        execute_trade()
        time.sleep(60)  # Wait for 1 minute before checking again

if __name__ == "__main__":
    main()
