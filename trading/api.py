import requests
import hashlib
import hmac
import time
import logging
import pandas as pd
from config.config import API_URL, API_KEY, SECRET_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def trade_stock(symbol, amount, action):
    nonce = int(time.time())
    params = {
        "cmd": "makeOrder",
        "params": {
            "id": symbol,
            "amount": amount,
            "action": action
        }
    }
    params_str = '&'.join(f'{k}={v}' for k, v in params.items())
    signature = hmac.new(SECRET_KEY.encode(), params_str.encode(), hashlib.sha256).hexdigest()
    headers = {
        'X-NtApi-Sig': signature,
        'Content-Type': 'application/json',
        'X-NtApi-Auth-Token': API_KEY  # Use your actual API key here
    }
    response = requests.post(API_URL, json=params, headers=headers)
    if response.status_code == 200:
        logging.info(f"Trade {action} {amount} of {symbol} executed successfully.")
    else:
        logging.error(f"Error executing trade: {response.status_code} - {response.text}")
    return response.json()

def fetch_stock_list():
    endpoint = f"{API_URL}/securities/list"
    nonce = int(time.time())
    params = {
        "cmd": "getSecuritiesList",
        "params": {}
    }
    params_str = '&'.join(f'{k}={v}' for k, v in params.items())
    signature = hmac.new(SECRET_KEY.encode(), params_str.encode(), hashlib.sha256).hexdigest()
    headers = {
        'X-NtApi-Sig': signature,
        'Content-Type': 'application/json',
        'X-NtApi-Auth-Token': API_KEY  # Use your actual API key here
    }
    response = requests.post(endpoint, json=params, headers=headers)
    if response.status_code == 200:
        stock_list = response.json().get('securities', [])
        logging.info(f"Fetched stock list: {stock_list}")
        return stock_list
    else:
        logging.error(f"Error fetching stock list: {response.status_code}, {response.text}")
        return []

def fetch_and_process_data(symbol, date_from, date_to, timeframe):
    nonce = int(time.time())
    params = {
        "cmd": "getHloc",
        "params": {
            "id": symbol,
            "timeframe": timeframe,
            "date_from": date_from,
            "date_to": date_to,
            "intervalMode": "ClosedRay"
        }
    }
    params_str = '&'.join(f'{k}={v}' for k, v in params.items())
    signature = hmac.new(SECRET_KEY.encode(), params_str.encode(), hashlib.sha256).hexdigest()
    headers = {
        'X-NtApi-Sig': signature,
        'Content-Type': 'application/json'
    }
    response = requests.post(API_URL, json=params, headers=headers)
    if response.status_code == 200:
        data = response.json().get('hloc', {}).get(symbol, [])
        if not data:
            logging.warning("No data found for symbol.")
            return pd.DataFrame()
        df = pd.DataFrame(data, columns=['high', 'low', 'open', 'close'])
        df.index = pd.to_datetime(response.json()['xSeries'][symbol], unit='s')
        logging.info(f"Fetched and processed data for {symbol}.")
        return df
    else:
        logging.error(f"Error fetching data for {symbol}: {response.status_code}")
        return pd.DataFrame()
