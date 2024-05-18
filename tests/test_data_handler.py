import unittest
import pandas as pd
from data.data_handler import fetch_stock_list, fetch_and_process_data, moving_average

class TestDataHandler(unittest.TestCase):

    def test_fetch_stock_list(self):
        stock_list = fetch_stock_list()
        self.assertIsInstance(stock_list, list)
    
    def test_fetch_and_process_data(self):
        symbol = "FB.US"
        date_from = "01.01.2023 00:00"
        date_to = "now"
        timeframe = 1440
        data = fetch_and_process_data(symbol, date_from, date_to, timeframe)
        self.assertIsInstance(data, pd.DataFrame)

    def test_moving_average(self):
        data = pd.DataFrame({'close': [1, 2, 3, 4, 5]})
        ma = moving_average(data, 3)
        self.assertIsInstance(ma, pd.Series)

if __name__ == '__main__':
    unittest.main()
