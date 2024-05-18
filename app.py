from flask import Flask, render_template
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from data_handler import fetch_and_process_data, moving_average, fetch_stock_list
from config import SYMBOL, SHORT_WINDOW, LONG_WINDOW, TRADE_AMOUNT, TIMEFRAME

app = Flask(__name__)

# Initialize Dash
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Global variables to store the bot's parameters
symbol = SYMBOL
short_window = SHORT_WINDOW
long_window = LONG_WINDOW
trade_amount = TRADE_AMOUNT
timeframe = TIMEFRAME
trade_logs = []

# Function to update the plot
def update_graph(symbol, short_window, long_window, timeframe):
    date_from = "01.01.2023 00:00"
    date_to = "now"
    data = fetch_and_process_data(symbol, date_from, date_to, timeframe)
    if data.empty:
        return {}

    short_ma = moving_average(data, short_window)
    long_ma = moving_average(data, long_window)

    trace_candlestick = go.Candlestick(
        x=data.index,
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name='Candlestick'
    )
    trace_short_ma = go.Scatter(x=data.index, y=short_ma, mode='lines', name='Short MA')
    trace_long_ma = go.Scatter(x=data.index, y=long_ma, mode='lines', name='Long MA')

    return {
        'data': [trace_candlestick, trace_short_ma, trace_long_ma],
        'layout': go.Layout(title=f'Stock Price and Moving Averages for {symbol}')
    }

# Fetch stock list for dropdown menu
stock_list = fetch_stock_list()

# Dash layout
dash_app.layout = html.Div(children=[
    html.H1(children='Trading Bot Dashboard'),

    html.Div([
        dcc.Dropdown(
            id='symbol-dropdown',
            options=[{'label': stock, 'value': stock} for stock in stock_list],
            value=SYMBOL,
            placeholder='Select stock symbol'
        ),
        dcc.Input(id='short-window-input', type='number', value=SHORT_WINDOW, placeholder='Enter short window size'),
        dcc.Input(id='long-window-input', type='number', value=LONG_WINDOW, placeholder='Enter long window size'),
        dcc.Input(id='trade-amount-input', type='number', value=TRADE_AMOUNT, placeholder='Enter trade amount'),
        dcc.Dropdown(
            id='timeframe-dropdown',
            options=[
                {'label': '1 Minute', 'value': 1},
                {'label': '5 Minutes', 'value': 5},
                {'label': '15 Minutes', 'value': 15},
                {'label': '1 Hour', 'value': 60},
                {'label': '1 Day', 'value': 1440}
            ],
            value=TIMEFRAME,
            placeholder='Select timeframe'
        ),
        html.Button(id='update-button', n_clicks=0, children='Update'),
        html.Button(id='start-button', n_clicks=0, children='Start Trading Bot')
    ], style={'display': 'flex', 'gap': '10px', 'margin-bottom': '20px'}),

    dcc.Graph(id='stock-price-graph'),

    html.Div(id='trade-log', children=[], style={'whiteSpace': 'pre-line', 'border': '1px solid black', 'padding': '10px', 'height': '200px', 'overflowY': 'scroll'}),

    dcc.Interval(
        id='interval-component',
        interval=1*60*1000,  # in milliseconds
        n_intervals=0
    )
])

@dash_app.callback(
    Output('stock-price-graph', 'figure'),
    Output('trade-log', 'children'),
    Input('interval-component', 'n_intervals'),
    Input('update-button', 'n_clicks'),
    State('symbol-dropdown', 'value'),
    State('short-window-input', 'value'),
    State('long-window-input', 'value'),
    State('trade-amount-input', 'value'),
    State('timeframe-dropdown', 'value')
)
def update_output(n_intervals, n_clicks, symbol_value, short_window_value, long_window_value, trade_amount_value, timeframe_value):
    global symbol, short_window, long_window, trade_amount, timeframe, trade_logs
    if n_clicks > 0:
        symbol = symbol_value
        short_window = short_window_value
        long_window = long_window_value
        trade_amount = trade_amount_value
        timeframe = timeframe_value
    graph = update_graph(symbol, short_window, long_window, timeframe)
    trade_logs_str = '\n'.join(trade_logs)
    return graph, trade_logs_str

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start_bot():
    execute_trade()
    return "Trading bot started!"

if __name__ == "__main__":
    app.run(debug=True)
