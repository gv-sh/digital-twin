"""Risk-adjusted returns and variance analysis."""

import numpy as np


def calculate_sharpe_ratio(
    mean_return: float,
    std_return: float,
    risk_free_rate: float = 0.03
) -> float:
    """Calculate Sharpe ratio."""
    if std_return == 0:
        return 0.0
    return (mean_return - risk_free_rate) / std_return


def calculate_var(
    returns: np.ndarray,
    confidence_level: float = 0.95
) -> float:
    """Calculate Value at Risk."""
    return np.percentile(returns, (1 - confidence_level) * 100)


__all__ = ["calculate_sharpe_ratio", "calculate_var"]
