from flask import Flask, render_template, request, redirect, url_for
import logging
from data.data_handler import fetch_stock_list
from trading.trader import execute_trade
from config.config import SHORT_WINDOW, LONG_WINDOW, TRADE_AMOUNT, TIMEFRAME
import dash_app

app = dash_app.server

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    stock_list = fetch_stock_list()
    logging.info(f"Stock list passed to template: {stock_list}")
    return render_template('dashboard.html', stock_list=stock_list, short_window=SHORT_WINDOW, long_window=LONG_WINDOW, trade_amount=TRADE_AMOUNT, timeframe=TIMEFRAME)

@app.route('/start', methods=['POST'])
def start_bot():
    symbol = request.form['symbol']
    short_window = int(request.form['short_window'])
    long_window = int(request.form['long_window'])
    trade_amount = int(request.form['trade_amount'])
    timeframe = int(request.form['timeframe'])
    logging.info(f"Starting trading bot with symbol={symbol}, short_window={short_window}, long_window={long_window}, trade_amount={trade_amount}, timeframe={timeframe}")
    execute_trade(symbol, short_window, long_window, trade_amount, timeframe)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
