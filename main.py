# quant_strategy_backtester.py
"""
Quant Strategy Backtester
=========================
Backtests multiple trading strategies with performance metrics and HTML reporting.
"""

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def sharpe_ratio(returns, risk_free=0.0):
    return np.sqrt(252) * (returns.mean() - risk_free) / returns.std()

def max_drawdown(equity_curve):
    roll_max = equity_curve.cummax()
    drawdown = equity_curve / roll_max - 1.0
    return drawdown.min()

def cagr(equity_curve):
    total_return = equity_curve[-1] / equity_curve[0]
    years = len(equity_curve) / 252
    return total_return ** (1 / years) - 1

def sma_crossover(df, short_window, long_window):
    df["SMA_Short"] = df["Close"].rolling(short_window).mean()
    df["SMA_Long"] = df["Close"].rolling(long_window).mean()
    df["Signal"] = np.where(df["SMA_Short"] > df["SMA_Long"], 1, 0)
    return df

def momentum(df, lookback=20):
    df["Signal"] = np.where(df["Close"] > df["Close"].shift(lookback), 1, 0)
    return df

def mean_reversion(df, lookback=20):
    df["Rolling_Mean"] = df["Close"].rolling(lookback).mean()
    df["Signal"] = np.where(df["Close"] < df["Rolling_Mean"], 1, 0)
    return df

def breakout(df, lookback=20):
    df["Signal"] = np.where(df["Close"] > df["Close"].rolling(lookback).max(), 1, 0)
    return df

def backtest(df, strategy, initial_capital=10000, cost_per_trade=0.0005):
    strategy_map = {
        "sma": lambda: sma_crossover(df, 20, 50),
        "momentum": lambda: momentum(df),
        "mean_reversion": lambda: mean_reversion(df),
        "breakout": lambda: breakout(df)
    }
    df = strategy_map[strategy]()
    df["Position"] = df["Signal"].shift(1)
    df["Returns"] = df["Close"].pct_change()
    df["Strategy"] = df["Position"] * df["Returns"]
    df["Strategy"] -= cost_per_trade
    df["Equity"] = (1 + df["Strategy"]).cumprod() * initial_capital
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quant Strategy Backtester")
    parser.add_argument("data_file", help="CSV file from market-data-pipeline")
    parser.add_argument("--strategy", default="sma", choices=["sma", "momentum", "mean_reversion", "breakout"])
    args = parser.parse_args()

    df = pd.read_csv(args.data_file, parse_dates=["Date"])
    df = backtest(df, args.strategy)
    metrics = {
        "CAGR": cagr(df["Equity"]),
        "Sharpe Ratio": sharpe_ratio(df["Strategy"]),
        "Max Drawdown": max_drawdown(df["Equity"]),
        "Final Portfolio Value": df["Equity"].iloc[-1]
    }
    print(metrics)
    df["Equity"].plot(title=f"Equity Curve - {args.strategy.upper()} Strategy")
    plt.show()
