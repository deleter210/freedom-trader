import requests
import pandas as pd
import time
from config.config import API_URL, API_KEY, SECRET_KEY
import hashlib
import hmac

def fetch_stock_list():
    # This is a hypothetical endpoint and parameters; replace with the actual API details.
    endpoint = f"{API_URL}/getStockList"
    nonce = int(time.time())
    params = {
        "cmd": "getStockList",
        "params": {}
    }
    params_str = '&'.join(f'{k}={v}' for k, v in params.items())
    signature = hmac.new(SECRET_KEY.encode(), params_str.encode(), hashlib.sha256).hexdigest()
    headers = {
        'X-NtApi-Sig': signature,
        'Content-Type': 'application/json'
    }
    response = requests.post(endpoint, json=params, headers=headers)
    if response.status_code == 200:
        stock_list = response.json().get('stocks', [])
        return stock_list
    else:
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
            return pd.DataFrame()
        df = pd.DataFrame(data, columns=['high', 'low', 'open', 'close'])
        df.index = pd.to_datetime(response.json()['xSeries'][symbol], unit='s')
        return df
    else:
        return pd.DataFrame()

def moving_average(data, window):
    return data['close'].rolling(window=window).mean()
