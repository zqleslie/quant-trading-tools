"""
Tests for quant-trading-tools indicators.
"""

import pandas as pd
import numpy as np
from quant_tools.indicators import RSI, MACD, BollingerBands, SMA


def test_sma():
    closes = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = SMA(closes, period=3)
    assert result.iloc[2] == 2.0  # (1+2+3)/3
    assert result.iloc[9] == 9.0  # (8+9+10)/3


def test_rsi_basic():
    # Uptrend should have high RSI
    closes = pd.Series(range(1, 21))
    rsi = RSI(closes, period=14)
    assert rsi.values.iloc[-1] > 50


def test_rsi_oversold():
    # Downtrend should have low RSI
    closes = pd.Series(range(20, 0, -1))
    rsi = RSI(closes, period=14)
    assert rsi.values.iloc[-1] < 50


def test_macd_cross():
    closes = pd.Series(np.random.randn(100).cumsum() + 50)
    macd = MACD(closes)
    assert len(macd.macd_line) == len(closes)
    assert len(macd.signal_line) == len(closes)
    assert len(macd.histogram) == len(closes)


def test_bollinger_bands():
    closes = pd.Series(np.random.randn(50) + 100)
    bb = BollingerBands(closes, period=20)
    assert (bb.upper > bb.middle).all()
    assert (bb.middle > bb.lower).all()


if __name__ == "__main__":
    test_sma()
    test_rsi_basic()
    test_rsi_oversold()
    test_macd_cross()
    test_bollinger_bands()
    print("All tests passed!")
