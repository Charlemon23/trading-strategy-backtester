import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, group_by='column')
    df.reset_index(inplace=True)
    return df

def moving_average_strategy(df, short_window=50, long_window=200):
    df['SMA50'] = df['Close'].rolling(window=short_window).mean()
    df['SMA200'] = df['Close'].rolling(window=long_window).mean()
    df['Signal'] = 0
    df.loc[short_window:, 'Signal'] = np.where(
        df['SMA50'][short_window:] > df['SMA200'][short_window:], 1, -1
    )
    return df

def plot_signals(df):
    plt.figure(figsize=(14,7))
    plt.plot(df['Date'], df['Close'], label='Close Price', alpha=0.7)
    plt.plot(df['Date'], df['SMA50'], label='50-Day SMA', alpha=0.7)
    plt.plot(df['Date'], df['SMA200'], label='200-Day SMA', alpha=0.7)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Moving Average Crossover Strategy')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    df = fetch_data('AAPL', '2023-01-01', '2024-01-01')
    df = moving_average_strategy(df)
    plot_signals(df)
    print("Backtest complete.")
