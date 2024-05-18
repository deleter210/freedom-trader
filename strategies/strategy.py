from data.data_handler import moving_average

def moving_average(data, window):
    """Calculate the moving average for the given window size."""
    return data['close'].rolling(window=window).mean()

def moving_average_crossover(data, short_window, long_window):
    """Generate trading signals based on moving average crossover strategy.
    
    Parameters:
    data (pd.DataFrame): The stock data with 'close' prices.
    short_window (int): The window size for the short moving average.
    long_window (int): The window size for the long moving average.
    
    Returns:
    str: 'buy', 'sell', or 'hold' signal based on the moving average crossover.
    """
    short_ma = moving_average(data, short_window)
    long_ma = moving_average(data, long_window)

    # Generate trading signal
    if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
        return 'buy'
    elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
        return 'sell'
    else:
        return 'hold'
