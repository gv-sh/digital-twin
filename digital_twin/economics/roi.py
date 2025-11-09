"""
ROI and NPV calculations.

This module implements financial analysis including:
NPV = -I₀ + Σ(CF_t/(1+r)^t), IRR, payback period
"""

import numpy as np
from typing import List
from digital_twin.core.constants import DEFAULT_DISCOUNT_RATE


def calculate_npv(
    initial_investment: float,
    annual_cashflows: List[float],
    discount_rate: float = DEFAULT_DISCOUNT_RATE
) -> float:
    """
    Calculate Net Present Value.

    NPV = -I₀ + Σ(CF_t/(1+r)^t)

    Parameters
    ----------
    initial_investment : float
        Initial capital investment
    annual_cashflows : list of float
        Annual cash flows
    discount_rate : float
        Annual discount rate

    Returns
    -------
    float
        Net Present Value
    """
    npv = -initial_investment
    for t, cashflow in enumerate(annual_cashflows, start=1):
        npv += cashflow / ((1 + discount_rate) ** t)
    return npv


def calculate_irr(
    initial_investment: float,
    annual_cashflows: List[float],
    max_iterations: int = 1000
) -> float:
    """
    Calculate Internal Rate of Return using Newton-Raphson method.

    Parameters
    ----------
    initial_investment : float
        Initial investment
    annual_cashflows : list of float
        Annual cash flows
    max_iterations : int
        Maximum iterations for convergence

    Returns
    -------
    float
        IRR as decimal (e.g., 0.15 for 15%)
    """
    # Initial guess
    irr = 0.1

    for _ in range(max_iterations):
        npv = -initial_investment
        npv_derivative = 0

        for t, cf in enumerate(annual_cashflows, start=1):
            npv += cf / ((1 + irr) ** t)
            npv_derivative -= t * cf / ((1 + irr) ** (t + 1))

        if abs(npv) < 0.01:  # Converged
            return irr

        # Newton-Raphson update
        if npv_derivative != 0:
            irr = irr - npv / npv_derivative

    return irr


def calculate_payback_period(
    initial_investment: float,
    annual_cashflows: List[float]
) -> float:
    """
    Calculate payback period in years.

    Parameters
    ----------
    initial_investment : float
        Initial investment
    annual_cashflows : list of float
        Annual cash flows

    Returns
    -------
    float
        Payback period in years
    """
    cumulative = 0
    for year, cashflow in enumerate(annual_cashflows, start=1):
        cumulative += cashflow
        if cumulative >= initial_investment:
            # Interpolate within the year
            previous_cumulative = cumulative - cashflow
            fraction = (initial_investment - previous_cumulative) / cashflow
            return year - 1 + fraction

    return float('inf')  # Never pays back


def calculate_roi(
    total_profit: float,
    initial_investment: float
) -> float:
    """
    Calculate Return on Investment.

    ROI = (Total Profit / Initial Investment) × 100

    Parameters
    ----------
    total_profit : float
        Total profit over analysis period
    initial_investment : float
        Initial investment

    Returns
    -------
    float
        ROI as percentage
    """
    if initial_investment == 0:
        return 0.0
    return (total_profit / initial_investment) * 100


__all__ = [
    "calculate_npv",
    "calculate_irr",
    "calculate_payback_period",
    "calculate_roi",
]
