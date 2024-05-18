import schedule
import time
from trader import execute_trade
from data_handler import fetch_and_process_data
from config import SYMBOL

def job():
    date_from = "01.01.2023 00:00"
    date_to = "now"
    data = fetch_and_process_data(SYMBOL, date_from, date_to)
    if not data.empty:
        # Update strategy data
        execute_trade(data)

schedule.every().minute.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
