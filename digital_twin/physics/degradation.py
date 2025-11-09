"""
Battery and component degradation models.

This module implements degradation models for batteries and other components:
P(t) = P₀·e^(-λt)·∏(1-r_cycle)
"""

import numpy as np
from digital_twin.core.constants import BATTERY_DEGRADATION_RATE, BATTERY_CYCLE_LIFE


def calculate_battery_degradation(
    initial_capacity: float,
    years: float,
    degradation_rate: float = BATTERY_DEGRADATION_RATE
) -> float:
    """
    Calculate battery capacity after degradation using exponential decay.

    P(t) = P₀·e^(-λt)

    Parameters
    ----------
    initial_capacity : float
        Initial battery capacity (kWh or range in km)
    years : float
        Number of years of operation
    degradation_rate : float
        Annual degradation rate (lambda)

    Returns
    -------
    float
        Degraded capacity
    """
    capacity_degraded = initial_capacity * np.exp(-degradation_rate * years)
    return capacity_degraded


def calculate_cycle_degradation(
    initial_capacity: float,
    cycles: int,
    degradation_per_cycle: float = 0.0001
) -> float:
    """
    Calculate battery degradation from charge cycles.

    Parameters
    ----------
    initial_capacity : float
        Initial battery capacity
    cycles : int
        Number of charge cycles
    degradation_per_cycle : float
        Degradation rate per cycle

    Returns
    -------
    float
        Degraded capacity
    """
    # Compound degradation over cycles
    capacity = initial_capacity * ((1 - degradation_per_cycle) ** cycles)
    return capacity


def calculate_combined_degradation(
    initial_capacity: float,
    years: float,
    cycles: int,
    calendar_degradation_rate: float = BATTERY_DEGRADATION_RATE,
    degradation_per_cycle: float = 0.0001
) -> float:
    """
    Calculate combined calendar and cycle degradation.

    P(t) = P₀·e^(-λt)·(1-r_cycle)^n_cycles

    Parameters
    ----------
    initial_capacity : float
        Initial battery capacity
    years : float
        Years of operation
    cycles : int
        Number of charge cycles
    calendar_degradation_rate : float
        Calendar aging rate
    degradation_per_cycle : float
        Degradation per cycle

    Returns
    -------
    float
        Degraded capacity
    """
    # Calendar aging
    calendar_factor = np.exp(-calendar_degradation_rate * years)

    # Cycle aging
    cycle_factor = (1 - degradation_per_cycle) ** cycles

    # Combined
    capacity = initial_capacity * calendar_factor * cycle_factor

    return capacity


def estimate_remaining_life(
    current_capacity: float,
    initial_capacity: float,
    end_of_life_threshold: float = 0.80
) -> float:
    """
    Estimate remaining useful life of battery.

    Parameters
    ----------
    current_capacity : float
        Current battery capacity
    initial_capacity : float
        Initial battery capacity
    end_of_life_threshold : float
        Capacity threshold for end of life (0.80 = 80%)

    Returns
    -------
    float
        Estimated years of remaining life
    """
    current_soh = current_capacity / initial_capacity

    if current_soh <= end_of_life_threshold:
        return 0.0

    # Estimate remaining degradation
    remaining_degradation = current_soh - end_of_life_threshold

    # Estimate years (assuming linear approximation)
    # This is simplified - real degradation is non-linear
    years_remaining = remaining_degradation / BATTERY_DEGRADATION_RATE

    return years_remaining


__all__ = [
    "calculate_battery_degradation",
    "calculate_cycle_degradation",
    "calculate_combined_degradation",
    "estimate_remaining_life",
]
