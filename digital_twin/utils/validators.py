"""
Type checking and validation utilities.

This module provides utilities for runtime type checking and validation.
"""

from typing import Any, Union, List
import numpy as np


def is_numeric(value: Any) -> bool:
    """Check if value is numeric."""
    return isinstance(value, (int, float, np.number))


def is_positive(value: Union[float, int]) -> bool:
    """Check if value is positive."""
    return is_numeric(value) and value > 0


def is_non_negative(value: Union[float, int]) -> bool:
    """Check if value is non-negative."""
    return is_numeric(value) and value >= 0


def is_percentage(value: Union[float, int]) -> bool:
    """Check if value is a valid percentage (0-100)."""
    return is_numeric(value) and 0 <= value <= 100


def is_decimal_percentage(value: Union[float, int]) -> bool:
    """Check if value is a valid decimal percentage (0-1)."""
    return is_numeric(value) and 0 <= value <= 1


def is_in_range(value: Union[float, int], min_val: float, max_val: float) -> bool:
    """Check if value is within range."""
    return is_numeric(value) and min_val <= value <= max_val


def ensure_list(value: Union[Any, List[Any]]) -> List[Any]:
    """Ensure value is a list."""
    if isinstance(value, list):
        return value
    return [value]


__all__ = [
    "is_numeric",
    "is_positive",
    "is_non_negative",
    "is_percentage",
    "is_decimal_percentage",
    "is_in_range",
    "ensure_list",
]
