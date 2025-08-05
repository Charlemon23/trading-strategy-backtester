A professional-grade Python tool for backtesting multiple trading strategies with detailed performance metrics.

This framework reads OHLCV datasets from the **Market Data Pipeline** repository and simulates strategies including **SMA Crossover**, **Momentum**, **Mean Reversion**, and **Breakout**. It calculates risk-adjusted metrics and produces equity curve visualizations.

---

## Features
- **Multiple Strategies**:
  - SMA Crossover
  - Momentum
  - Mean Reversion
  - Breakout
- **Risk Metrics**:
  - Sharpe Ratio
  - Max Drawdown
  - CAGR
- **Transaction Cost & Slippage Modeling**
- **Equity Curve Visualization**
- **Multi-Asset Ready**: Backtest any dataset in `/data/` from `market-data-pipeline`

---

## Installation
```bash
git clone https://github.com/<your-username>/quant-strategy-backtester.git
cd quant-strategy-backtester
pip install -r requirements.txt
