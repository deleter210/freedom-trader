import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("trading_bot.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)


API_KEY = '9d06661ea5d6a71e18924abea260e7a0'
SECRET_KEY = 'dedd4e71018e09e1359c7a066dee868d5b499092'
API_URL = 'https://tradernet.com/'
SHORT_WINDOW = 40
LONG_WINDOW = 100
TRADE_AMOUNT = 10
TIMEFRAME = 1440  # Daily timeframe in minutes