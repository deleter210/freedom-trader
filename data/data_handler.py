import requests
import pandas as pd
import time
import hashlib
import hmac
import logging
from config.config import API_URL, API_KEY, SECRET_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_list():
    endpoint = f"{API_URL}/api"
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
        'X-NtApi-Auth-Token': API_KEY
    }
    
    try:
        response = requests.post(endpoint, json=params, headers=headers)
        if response.status_code == 200:
            stock_list = response.json().get('securities', [])
            logging.info(f"Fetched stock list: {stock_list}")
            return [stock['ticker'] for stock in stock_list]  # Extract only the ticker symbols
        elif response.status_code == 401:
            logging.error("Unauthorized access. Please check your API key and secret key.")
        else:
            logging.error(f"Error fetching stock list: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
    
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

get_historical_data = fetch_and_process_data

def moving_average(data, window):
    """Calculate the moving average for the given window size."""
    return data['close']
