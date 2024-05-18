import requests
import json
from config.config import API_PUBLIC_KEY, API_SECRET_KEY, BASE_URL
from utils.utils import generate_signature, get_nonce

def api_request(endpoint, params):
    url = f"{BASE_URL}/{endpoint}"
    params['apiKey'] = API_PUBLIC_KEY
    params['nonce'] = get_nonce()
    signature = generate_signature(params)
    headers = {'X-NtApi-Sig': signature}
    response = requests.post(url, data=params, headers=headers)
    return response.json()

def get_historical_data(symbol, date_from, date_to, timeframe=1440):
    params = {
        "cmd": "getHloc",
        "params": {
            "id": symbol,
            "count": -1,
            "timeframe": timeframe,
            "date_from": date_from,
            "date_to": date_to,
            "intervalMode": "ClosedRay"
        }
    }
    return api_request('', params)

def trade_stock(symbol, amount, trade_type):
    params = {
        'symbol': symbol,
        'amount': amount,
        'type': trade_type
    }
    return api_request('tradeStock', params)
