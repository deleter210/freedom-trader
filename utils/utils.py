import hashlib
import hmac
import time

from config.config import SECRET_KEY

def generate_signature(params, secret_key=SECRET_KEY):
    params_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(secret_key.encode(), params_string.encode(), hashlib.sha256).hexdigest()
    return signature

def get_nonce():
    return int(time.time())
