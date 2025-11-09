"""
Output formatting utilities.

This module provides utilities for formatting numbers, currencies, and reports.
"""

from typing import Union, Optional
import numpy as np


def format_currency(
    amount: Union[float, int],
    currency: str = "AUD",
    decimals: int = 0
) -> str:
    """
    Format amount as currency.

    Parameters
    ----------
    amount : float or int
        Amount to format
    currency : str
        Currency code (default: "AUD")
    decimals : int
        Number of decimal places (default: 0)

    Returns
    -------
    str
        Formatted currency string
    """
    symbol = "$" if currency == "AUD" else currency
    if amount >= 0:
        return f"{symbol}{amount:,.{decimals}f}"
    else:
        return f"-{symbol}{abs(amount):,.{decimals}f}"


def format_percentage(
    value: Union[float, int],
    decimals: int = 1
) -> str:
    """
    Format value as percentage.

    Parameters
    ----------
    value : float or int
        Value to format (0.15 -> 15%)
    decimals : int
        Number of decimal places

    Returns
    -------
    str
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def format_number(
    value: Union[float, int],
    decimals: int = 2,
    thousands_sep: bool = True
) -> str:
    """
    Format number with thousands separator.

    Parameters
    ----------
    value : float or int
        Value to format
    decimals : int
        Number of decimal places
    thousands_sep : bool
        Include thousands separator

    Returns
    -------
    str
        Formatted number string
    """
    if thousands_sep:
        return f"{value:,.{decimals}f}"
    else:
        return f"{value:.{decimals}f}"


def format_large_number(value: Union[float, int], decimals: int = 1) -> str:
    """
    Format large numbers with K, M, B suffix.

    Parameters
    ----------
    value : float or int
        Value to format
    decimals : int
        Number of decimal places

    Returns
    -------
    str
        Formatted string (e.g., "1.5M")
    """
    abs_value = abs(value)
    sign = "-" if value < 0 else ""

    if abs_value >= 1_000_000_000:
        return f"{sign}{abs_value/1_000_000_000:.{decimals}f}B"
    elif abs_value >= 1_000_000:
        return f"{sign}{abs_value/1_000_000:.{decimals}f}M"
    elif abs_value >= 1_000:
        return f"{sign}{abs_value/1_000:.{decimals}f}K"
    else:
        return f"{sign}{abs_value:.{decimals}f}"


def format_distance(km: Union[float, int], unit: str = "km") -> str:
    """
    Format distance with unit.

    Parameters
    ----------
    km : float or int
        Distance in kilometers
    unit : str
        Unit to display ("km" or "mi")

    Returns
    -------
    str
        Formatted distance string
    """
    if unit == "mi":
        miles = km * 0.621371
        return f"{miles:,.0f} mi"
    else:
        return f"{km:,.0f} km"


def format_energy(kwh: Union[float, int], unit: str = "kWh") -> str:
    """
    Format energy with unit.

    Parameters
    ----------
    kwh : float or int
        Energy in kWh
    unit : str
        Unit to display

    Returns
    -------
    str
        Formatted energy string
    """
    if unit == "MJ":
        mj = kwh * 3.6
        return f"{mj:,.1f} MJ"
    else:
        return f"{kwh:,.1f} kWh"


def format_co2(kg_co2: Union[float, int]) -> str:
    """
    Format CO2 emissions.

    Parameters
    ----------
    kg_co2 : float or int
        CO2 in kilograms

    Returns
    -------
    str
        Formatted CO2 string
    """
    if kg_co2 >= 1000:
        tonnes = kg_co2 / 1000
        return f"{tonnes:,.1f} t CO₂"
    else:
        return f"{kg_co2:,.0f} kg CO₂"


__all__ = [
    "format_currency",
    "format_percentage",
    "format_number",
    "format_large_number",
    "format_distance",
    "format_energy",
    "format_co2",
]
