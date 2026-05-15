"""
Example: Using quant-trading-tools to generate trading signals.

This example demonstrates how to combine multiple indicators
to generate buy/sell signals from historical price data.
"""

import pandas as pd
import numpy as np
from quant_tools import RSI, MACD, SignalGenerator, SignalType


def main():
    # Generate sample price data (replace with real data)
    np.random.seed(42)
    days = 200
    returns = np.random.randn(days) * 0.02
    closes = pd.Series(100) * (1 + returns).cumprod()

    # Calculate indicators
    rsi = RSI(closes, period=14)
    macd = MACD(closes)
    bb = BollingerBands(closes, period=20)

    # Generate signals
    sg = SignalGenerator(long_threshold=1.5, short_threshold=-1.5)
    sg.add_indicator("rsi", rsi.values, oversold=30, overbought=70, weight=1.0)
    sg.add_indicator("macd", macd.histogram, weight=0.5)

    signals = sg.run()

    # Summary
    long_count = (signals["signal"] == SignalType.LONG).sum()
    short_count = (signals["signal"] == SignalType.SHORT).sum()
    neutral_count = (signals["signal"] == SignalType.NEUTRAL).sum()

    print(f"Signal Summary:")
    print(f"  LONG:   {long_count}")
    print(f"  SHORT:  {short_count}")
    print(f"  NEUTRAL: {neutral_count}")

    # Show last 10 signals
    print(f"\nLast 10 signals:")
    print(signals.tail(10).to_string())


if __name__ == "__main__":
    main()
