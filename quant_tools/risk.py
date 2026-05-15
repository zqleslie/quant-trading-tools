"""
Risk management utilities for position sizing and portfolio risk.
"""

import numpy as np


class PositionSizer:
    """
    Calculate position sizes based on different sizing strategies.
    """

    @staticmethod
    def fixed_fraction(portfolio_value: float, risk_per_trade: float = 0.02) -> float:
        """
        Risk a fixed fraction of portfolio per trade.

        Args:
            portfolio_value: Total portfolio value
            risk_per_trade: Fraction to risk (default 2%)

        Returns:
            Dollar amount to risk on this trade
        """
        return portfolio_value * risk_per_trade

    @staticmethod
    def kelly_criterion(win_rate: float, avg_win: float, avg_loss: float) -> float:
        """
        Kelly Criterion for optimal position sizing.

        Args:
            win_rate: Historical win rate (0-1)
            avg_win: Average winning trade (as multiple of risk)
            avg_loss: Average losing trade (as multiple of risk, positive number)

        Returns:
            Kelly percentage (0-1), or 0 if edge is negative
        """
        if avg_loss == 0:
            return 0.0

        b = avg_win / avg_loss  # Win/loss ratio
        k = win_rate - ((1 - win_rate) / b)

        # Use half-Kelly for safety
        return max(0.0, k / 2)

    @staticmethod
    def volatility_adjusted(
        portfolio_value: float,
        risk_per_trade: float,
        atr: float,
        price: float,
    ) -> int:
        """
        Size position based on volatility (ATR).

        Args:
            portfolio_value: Total portfolio value
            risk_per_trade: Dollar amount to risk
            atr: Average True Range
            price: Current price

        Returns:
            Number of shares/contracts to trade
        """
        if atr == 0 or price == 0:
            return 0

        risk_amount = portfolio_value * risk_per_trade
        stop_distance = 2 * atr  # 2x ATR stop loss
        position_value = risk_amount / (stop_distance / price)

        return int(position_value / price)


class RiskManager:
    """
    Portfolio-level risk management.
    """

    def __init__(
        self,
        max_drawdown: float = 0.10,
        max_single_loss: float = 0.02,
        max_correlation: float = 0.7,
    ):
        self.max_drawdown = max_drawdown
        self.max_single_loss = max_single_loss
        self.max_correlation = max_correlation

    def check_drawdown(self, current_value: float, peak_value: float) -> bool:
        """Check if portfolio drawdown exceeds limit."""
        if peak_value == 0:
            return False
        drawdown = (peak_value - current_value) / peak_value
        return drawdown >= self.max_drawdown

    def check_concentration(self, position_value: float, portfolio_value: float) -> bool:
        """Check if single position exceeds risk limit."""
        if portfolio_value == 0:
            return False
        return (position_value / portfolio_value) > self.max_single_loss

    def should_reduce_exposure(self, current_value: float, peak_value: float) -> bool:
        """
        Risk reduction trigger.
        Returns True if trading should be paused or size reduced.
        """
        return self.check_drawdown(current_value, peak_value)
