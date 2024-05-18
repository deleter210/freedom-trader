from data_handler import get_historical_data, moving_average

def moving_average_crossover(data, short_window, long_window):
    short_ma = moving_average(data, short_window)
    long_ma = moving_average(data, long_window    # Get historical data
    historical_data = get_historical_data(symbol)
    
    # Calculate moving averages
    short_ma = moving_average(historical_data, short_window)
    long_ma = moving_average(historical_data, long_window)
    
    # Determine trading signal
    if short_ma.iloc[-1] > long_ma.iloc[-1]:
        return 'buy'
    elif short_ma.iloc[-1] < long_ma.iloc[-1]:
        return 'sell'
    else:
        return 'hold'
