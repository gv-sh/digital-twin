"""
Date and time utilities for fleet analysis.

This module provides utilities for date arithmetic and time-based calculations.
"""

from datetime import datetime, timedelta
from typing import List
import numpy as np


def add_years(date: datetime, years: int) -> datetime:
    """Add years to a date."""
    try:
        return date.replace(year=date.year + years)
    except ValueError:
        # Handle leap year edge case (Feb 29)
        return date.replace(year=date.year + years, day=28)


def years_between(start_date: datetime, end_date: datetime) -> float:
    """Calculate years between two dates."""
    delta = end_date - start_date
    return delta.days / 365.25


def generate_date_range(
    start_date: datetime,
    end_date: datetime,
    freq: str = "M"
) -> List[datetime]:
    """
    Generate a range of dates.

    Parameters
    ----------
    start_date : datetime
        Start date
    end_date : datetime
        End date
    freq : str
        Frequency: "D" (daily), "M" (monthly), "Y" (yearly)

    Returns
    -------
    list
        List of datetime objects
    """
    dates = []
    current = start_date

    if freq == "D":
        step = timedelta(days=1)
    elif freq == "M":
        step = timedelta(days=30)
    elif freq == "Y":
        step = timedelta(days=365)
    else:
        raise ValueError(f"Unknown frequency: {freq}")

    while current <= end_date:
        dates.append(current)
        current += step

    return dates


def operating_days_in_period(
    start_date: datetime,
    end_date: datetime,
    operating_days_per_week: int = 5
) -> int:
    """
    Calculate operating days in a period.

    Parameters
    ----------
    start_date : datetime
        Start date
    end_date : datetime
        End date
    operating_days_per_week : int
        Operating days per week (default: 5)

    Returns
    -------
    int
        Number of operating days
    """
    total_days = (end_date - start_date).days
    total_weeks = total_days / 7
    return int(total_weeks * operating_days_per_week)


__all__ = [
    "add_years",
    "years_between",
    "generate_date_range",
    "operating_days_in_period",
]
