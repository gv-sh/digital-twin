"""Time-series forecasting."""

import numpy as np


def forecast_trend(historical_data: np.ndarray, periods: int) -> np.ndarray:
    """Simple linear trend forecast."""
    x = np.arange(len(historical_data))
    coeffs = np.polyfit(x, historical_data, 1)
    future_x = np.arange(len(historical_data), len(historical_data) + periods)
    return np.polyval(coeffs, future_x)


__all__ = ["forecast_trend"]
