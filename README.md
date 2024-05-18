# Freedom-Trader Bot

## Overview

Freedom-Trader is an automated trading bot designed to trade stocks using the Freedom24 API. The bot fetches real-time stock data, applies trading strategies, executes trades, and updates a user-friendly dashboard.

## Features

- **Dynamic Stock List**: Fetches and displays available stocks from Freedom24 API.
- **Trading Strategies**: Implements moving average crossover strategy.
- **Real-time Data**: Updates stock prices and indicators in real-time.
- **Trade Execution**: Automatically executes buy/sell orders based on strategy signals.
- **User Interface**: Interactive dashboard using Dash for visualization and control.


## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/freedom-trader.git
    cd freedom-trader
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv tradebot-env
    source tradebot-env/bin/activate  # On Windows: tradebot-env\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure API Credentials**:
    - Update `config/config.py` with your Freedom24 API URL, public key, and secret key.

5. **Run the Application**:
    ```bash
    python main.py
    ```

## Usage

- **Dashboard**: Access the dashboard at `http://127.0.0.1:5000/dashboard` to view real-time data and manage trading parameters.
- **Logs**: Check the logs for detailed information on trading activities and errors.

## Enhanced Functionality Suggestions

1. **Advanced Trading Strategies**: Integrate machine learning, sentiment analysis, and additional technical indicators.
2. **Risk Management**: Implement stop loss, take profit, and position sizing mechanisms.
3. **Real-Time Data and Alerts**: Use WebSockets, notifications, and enhanced dashboard features.
4. **User Interface Improvements**: Add interactive charts, user customization, and mobile compatibility.
5. **Backtesting and Simulation**: Implement backtesting on historical data and a simulation mode.
6. **Logging and Reporting**: Maintain detailed logs and generate periodic reports.
7. **Security Enhancements**: Add two-factor authentication and data encryption.
8. **API Enhancements**: Support multiple exchanges and implement API rate limiting.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License.
