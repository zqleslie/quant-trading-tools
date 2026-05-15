# quant-trading-tools

Python utilities for quantitative trading and technical analysis.

## Features

- **Indicator Library**: Common technical indicators (RSI, MACD, Bollinger Bands, etc.)
- **Signal Generator**: Rule-based signal detection with backtesting support
- **Risk Manager**: Position sizing, stop-loss, and portfolio risk calculations
- **Data Pipeline**: OHLCV data normalization and cleaning utilities

## Installation

`ash
pip install -r requirements.txt
`

## Quick Start

`python
from quant_tools import RSI, MACD, SignalGenerator

# Calculate RSI
rsi = RSI(closes, period=14)

# Generate signals
sg = SignalGenerator()
sg.add_indicator('rsi', rsi, oversold=30, overbought=70)
signals = sg.run()
`

## Modules

| Module | Description |
|--------|-------------|
| indicators.py | Technical indicators |
| signals.py | Signal generation engine |
| isk.py | Risk management utilities |
| data.py | OHLCV data pipeline |

## License

MIT
