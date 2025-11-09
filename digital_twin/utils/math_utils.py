"""
Mathematical utilities for numerical methods and calculations.

This module provides utility functions for interpolation, numerical methods,
and common mathematical operations.
"""

import numpy as np
from typing import List, Tuple, Callable, Optional
from scipy import interpolate


def linear_interpolate(
    x: float,
    x_points: List[float],
    y_points: List[float]
) -> float:
    """
    Perform linear interpolation.

    Parameters
    ----------
    x : float
        Point at which to interpolate
    x_points : list of float
        Known x coordinates
    y_points : list of float
        Known y coordinates

    Returns
    -------
    float
        Interpolated value
    """
    return np.interp(x, x_points, y_points)


def cubic_spline_interpolate(
    x: np.ndarray,
    x_points: np.ndarray,
    y_points: np.ndarray
) -> np.ndarray:
    """
    Perform cubic spline interpolation.

    Parameters
    ----------
    x : ndarray
        Points at which to interpolate
    x_points : ndarray
        Known x coordinates
    y_points : ndarray
        Known y coordinates

    Returns
    -------
    ndarray
        Interpolated values
    """
    cs = interpolate.CubicSpline(x_points, y_points)
    return cs(x)


def moving_average(data: np.ndarray, window: int) -> np.ndarray:
    """
    Calculate moving average of data.

    Parameters
    ----------
    data : ndarray
        Input data
    window : int
        Window size for moving average

    Returns
    -------
    ndarray
        Moving average values
    """
    return np.convolve(data, np.ones(window) / window, mode='valid')


def exponential_decay(
    initial_value: float,
    decay_rate: float,
    time: float
) -> float:
    """
    Calculate exponential decay.

    Parameters
    ----------
    initial_value : float
        Initial value
    decay_rate : float
        Decay rate (lambda)
    time : float
        Time elapsed

    Returns
    -------
    float
        Value after decay
    """
    return initial_value * np.exp(-decay_rate * time)


def calculate_gradient(
    distance: np.ndarray,
    elevation: np.ndarray
) -> np.ndarray:
    """
    Calculate gradient from distance and elevation profiles.

    Parameters
    ----------
    distance : ndarray
        Distance points in meters
    elevation : ndarray
        Elevation points in meters

    Returns
    -------
    ndarray
        Gradient at each point (radians)
    """
    # Calculate rise over run
    rise = np.diff(elevation)
    run = np.diff(distance)

    # Avoid division by zero
    run = np.where(run == 0, 1e-10, run)

    # Calculate angle in radians
    gradient = np.arctan(rise / run)

    # Pad to original length
    gradient = np.concatenate([[gradient[0]], gradient])

    return gradient


def calculate_percentile(data: np.ndarray, percentile: float) -> float:
    """
    Calculate percentile of data.

    Parameters
    ----------
    data : ndarray
        Input data
    percentile : float
        Percentile to calculate (0-100)

    Returns
    -------
    float
        Percentile value
    """
    return np.percentile(data, percentile)


def root_mean_square(data: np.ndarray) -> float:
    """
    Calculate root mean square.

    Parameters
    ----------
    data : ndarray
        Input data

    Returns
    -------
    float
        RMS value
    """
    return np.sqrt(np.mean(data ** 2))


def weighted_average(
    values: np.ndarray,
    weights: np.ndarray
) -> float:
    """
    Calculate weighted average.

    Parameters
    ----------
    values : ndarray
        Values to average
    weights : ndarray
        Weights for each value

    Returns
    -------
    float
        Weighted average
    """
    return np.average(values, weights=weights)


def compound_growth(
    initial_value: float,
    growth_rate: float,
    periods: int
) -> float:
    """
    Calculate compound growth.

    Parameters
    ----------
    initial_value : float
        Initial value
    growth_rate : float
        Growth rate per period (e.g., 0.03 for 3%)
    periods : int
        Number of periods

    Returns
    -------
    float
        Final value after compound growth
    """
    return initial_value * ((1 + growth_rate) ** periods)


def solve_quadratic(a: float, b: float, c: float) -> Tuple[complex, complex]:
    """
    Solve quadratic equation ax² + bx + c = 0.

    Parameters
    ----------
    a, b, c : float
        Coefficients of quadratic equation

    Returns
    -------
    tuple
        Two roots (may be complex)
    """
    discriminant = b**2 - 4*a*c
    root1 = (-b + np.sqrt(discriminant + 0j)) / (2*a)
    root2 = (-b - np.sqrt(discriminant + 0j)) / (2*a)
    return root1, root2


__all__ = [
    "linear_interpolate",
    "cubic_spline_interpolate",
    "moving_average",
    "exponential_decay",
    "calculate_gradient",
    "calculate_percentile",
    "root_mean_square",
    "weighted_average",
    "compound_growth",
    "solve_quadratic",
]
