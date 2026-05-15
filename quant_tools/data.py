"""
OHLCV data pipeline utilities.
"""

import numpy as np
import pandas as pd


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize OHLCV DataFrame to standard format.

    Expected columns (case-insensitive):
    - timestamp/open/high/low/close/volume

    Returns DataFrame with lowercase columns, sorted by time.
    """
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]

    # Rename common variants
    rename_map = {
        "time": "timestamp",
        "date": "timestamp",
        "o": "open",
        "h": "high",
        "l": "low",
        "c": "close",
        "v": "volume",
        "close_time": "close_timestamp",
    }
    df = df.rename(columns=rename_map)

    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Parse timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Numeric columns
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna(subset=["close"])


def resample_ohlcv(df: pd.DataFrame, timeframe: str = "1h") -> pd.DataFrame:
    """
    Resample OHLCV data to a higher timeframe.

    Args:
        df: Normalized OHLCV DataFrame
        timeframe: Target timeframe (e.g. '1h', '4h', '1D')

    Returns:
        Resampled OHLCV DataFrame
    """
    df = df.set_index("timestamp")

    agg_rules = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }

    resampled = df.resample(timeframe).agg(agg_rules)
    resampled = resampled.dropna(subset=["close"])
    resampled = resampled.reset_index()

    return resampled


def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add return columns to OHLCV data.

    Adds:
    - returns: Simple close-to-close returns
    - log_returns: Log returns
    - high_low_range: (High - Low) / Close
    """
    df = df.copy()
    df["returns"] = df["close"].pct_change()
    df["log_returns"] = (df["close"] / df["close"].shift(1)).apply(
        lambda x: np.log(x) if x > 0 else 0
    )
    df["high_low_range"] = (df["high"] - df["low"]) / df["close"]

    return df
