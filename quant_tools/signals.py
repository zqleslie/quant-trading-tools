"""
Signal generation engine for rule-based trading signals.
"""

from enum import Enum
from typing import Optional
import pandas as pd


class SignalType(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"


class SignalGenerator:
    """
    Combines multiple indicators to generate trading signals.

    Usage:
        sg = SignalGenerator()
        sg.add_indicator('rsi', rsi_values, oversold=30, overbought=70)
        sg.add_indicator('macd_cross', macd_bullish, weight=2.0)
        signals = sg.run()
    """

    def __init__(self, long_threshold: float = 2.0, short_threshold: float = -2.0):
        self.indicators: list[dict] = []
        self.long_threshold = long_threshold
        self.short_threshold = short_threshold

    def add_indicator(
        self,
        name: str,
        values: pd.Series,
        oversold: Optional[float] = None,
        overbought: Optional[float] = None,
        weight: float = 1.0,
    ):
        """
        Add an indicator to the signal generator.

        For oscillators (like RSI): provide oversold/overbought thresholds.
        For binary signals (like MACD cross): pass boolean Series directly.
        """
        self.indicators.append({
            "name": name,
            "values": values,
            "oversold": oversold,
            "overbought": overbought,
            "weight": weight,
        })

    def run(self) -> pd.DataFrame:
        """Generate combined signals from all indicators."""
        if not self.indicators:
            raise ValueError("No indicators added")

        # Use the first indicator's index as reference
        base_index = self.indicators[0]["values"].index
        scores = pd.Series(0.0, index=base_index)

        for ind in self.indicators:
            vals = ind["values"]
            w = ind["weight"]

            if ind["oversold"] is not None and ind["overbought"] is not None:
                # Oscillator: oversold → +score (buy), overbought → -score (sell)
                bull_signal = (vals < ind["oversold"]).astype(float) * w
                bear_signal = (vals > ind["overbought"]).astype(float) * (-w)
                scores += bull_signal + bear_signal
            else:
                # Binary signal: True for bullish, False for bearish
                if vals.dtype == bool:
                    scores += vals.astype(float) * (2 * w - w)  # +w or -w
                else:
                    scores += vals * w

        # Generate final signal
        result = pd.DataFrame(index=base_index)
        result["score"] = scores
        result["signal"] = pd.Series(SignalType.NEUTRAL, index=base_index)
        result.loc[scores >= self.long_threshold, "signal"] = SignalType.LONG
        result.loc[scores <= self.short_threshold, "signal"] = SignalType.SHORT

        return result
