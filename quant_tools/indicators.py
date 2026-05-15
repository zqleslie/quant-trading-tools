"""
Technical indicators for quantitative analysis.
"""

import numpy as np
import pandas as pd


def SMA(closes: pd.Series, period: int = 20) -> pd.Series:
    """Simple Moving Average"""
    return closes.rolling(window=period).mean()


def EMA(closes: pd.Series, period: int = 20) -> pd.Series:
    """Exponential Moving Average"""
    return closes.ewm(span=period, adjust=False).mean()


class RSI:
    """Relative Strength Index"""

    def __init__(self, closes: pd.Series, period: int = 14):
        self.period = period
        self.values = self._calculate(closes)

    def _calculate(self, closes: pd.Series) -> pd.Series:
        delta = closes.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.ewm(alpha=1/self.period, min_periods=self.period).mean()
        avg_loss = loss.ewm(alpha=1/self.period, min_periods=self.period).mean()

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def is_oversold(self, threshold: float = 30) -> pd.Series:
        return self.values < threshold

    def is_overbought(self, threshold: float = 70) -> pd.Series:
        return self.values > threshold


class MACD:
    """Moving Average Convergence Divergence"""

    def __init__(self, closes: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
        self.fast = fast
        self.slow = slow
        self.signal_period = signal
        self.macd_line = EMA(closes, fast) - EMA(closes, slow)
        self.signal_line = EMA(self.macd_line, signal)
        self.histogram = self.macd_line - self.signal_line

    def is_bullish_cross(self) -> pd.Series:
        return (self.macd_line > self.signal_line) & (self.macd_line.shift(1) <= self.signal_line.shift(1))

    def is_bearish_cross(self) -> pd.Series:
        return (self.macd_line < self.signal_line) & (self.macd_line.shift(1) >= self.signal_line.shift(1))


class BollingerBands:
    """Bollinger Bands"""

    def __init__(self, closes: pd.Series, period: int = 20, std_dev: float = 2.0):
        self.period = period
        self.std_dev = std_dev
        self.middle = SMA(closes, period)
        self.std = closes.rolling(window=period).std()
        self.upper = self.middle + (self.std * std_dev)
        self.lower = self.middle - (self.std * std_dev)
        self.width = (self.upper - self.lower) / self.middle

    def is_touching_upper(self, closes: pd.Series) -> pd.Series:
        return closes >= self.upper

    def is_touching_lower(self, closes: pd.Series) -> pd.Series:
        return closes <= self.lower

    def bandwidth(self) -> pd.Series:
        return self.width * 100
