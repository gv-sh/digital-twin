"""
Battery and component degradation models.

This module implements degradation models for batteries and other components:
P(t) = P₀·e^(-λt)·∏(1-r_cycle)

Extended Fleet Durability and Performance Model based on Paper B corrosion
methodology, adapted for vehicle performance degradation and validated with
Queensland trial data.

Equations implemented:
- Battery Performance Degradation: P_battery(t) = P_0·e^(-λt)·∏(1-r_cycle,i)
- Linear Degradation Model: C(t) = C_0(1 - k_deg·cycles)
- Operational Range Model: R_effective(t) = R_rated·P_battery(t)·f_temp·f_load·f_gradient

Queensland Trial Calibration:
- 15% battery degradation over 1.5 years
- 100-200 km operational range per trip
- ~300 km full charge capacity
"""

import numpy as np
from typing import Optional
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


def calculate_operational_range(
    rated_range: float,
    battery_performance_factor: float,
    temperature_factor: float = 1.0,
    load_factor: float = 1.0,
    gradient_factor: float = 1.0
) -> float:
    """
    Calculate effective operational range with environmental and operational factors.

    Operational Range Model:
    R_effective(t) = R_rated · P_battery(t) · f_temp · f_load · f_gradient

    Parameters
    ----------
    rated_range : float
        Manufacturer-rated range (km)
    battery_performance_factor : float
        Battery performance factor (0-1) from degradation model
    temperature_factor : float
        Temperature correction factor (0-1)
        < 1.0 in extreme cold/heat
    load_factor : float
        Load capacity utilization factor (0-1)
        < 1.0 for heavier loads
    gradient_factor : float
        Route gradient impact factor (0-1)
        < 1.0 for hilly terrain

    Returns
    -------
    float
        Effective operational range (km)

    Notes
    -----
    Validated against Queensland trials showing 100-200 km operational range
    from 300 km rated capacity.

    Examples
    --------
    >>> # Ideal conditions with some degradation
    >>> calculate_operational_range(300.0, 0.85, 1.0, 1.0, 1.0)
    255.0

    >>> # Winter conditions, full load, hilly terrain
    >>> calculate_operational_range(300.0, 0.85, 0.8, 0.9, 0.85)
    156.06
    """
    effective_range = (
        rated_range
        * battery_performance_factor
        * temperature_factor
        * load_factor
        * gradient_factor
    )
    return max(0.0, effective_range)


def calculate_degradation_rate_from_trials(
    initial_capacity: float,
    final_capacity: float,
    years: float
) -> float:
    """
    Calculate degradation rate from trial data.

    Useful for calibrating models to observed data like Queensland trials.

    Parameters
    ----------
    initial_capacity : float
        Initial capacity or performance metric
    final_capacity : float
        Observed final capacity
    years : float
        Time period of observation

    Returns
    -------
    float
        Estimated degradation rate λ

    Examples
    --------
    >>> # Queensland trials: 15% degradation over 1.5 years
    >>> calculate_degradation_rate_from_trials(300.0, 255.0, 1.5)
    0.106  # Approximately 10.6% per year
    """
    if years <= 0 or initial_capacity <= 0:
        return 0.0

    # From P(t) = P_0 * e^(-λt)
    # λ = -ln(P(t)/P_0) / t
    capacity_ratio = final_capacity / initial_capacity
    degradation_rate = -np.log(capacity_ratio) / years

    return degradation_rate


def estimate_end_of_life(
    current_capacity: float,
    initial_capacity: float,
    degradation_rate: float = BATTERY_DEGRADATION_RATE,
    eol_threshold: float = 0.80
) -> float:
    """
    Estimate time until battery reaches end-of-life threshold.

    Parameters
    ----------
    current_capacity : float
        Current battery capacity
    initial_capacity : float
        Initial battery capacity
    degradation_rate : float
        Degradation rate λ (default from Queensland trials)
    eol_threshold : float
        End-of-life threshold (0.80 = 80% capacity)

    Returns
    -------
    float
        Years until end-of-life

    Examples
    --------
    >>> # Battery at 90% capacity
    >>> estimate_end_of_life(270.0, 300.0, 0.106, 0.80)
    # Returns estimated years to 80% threshold
    """
    current_soh = current_capacity / initial_capacity

    if current_soh <= eol_threshold:
        return 0.0

    # From P(t) = P_0 * e^(-λt)
    # t = -ln(P_threshold/P_current) / λ
    if degradation_rate <= 0:
        return float('inf')

    time_to_eol = -np.log(eol_threshold / current_soh) / degradation_rate

    return max(0.0, time_to_eol)


def calculate_performance_with_environmental_factors(
    base_performance: float,
    ambient_temp_c: float,
    load_kg: float,
    max_load_kg: float,
    route_elevation_gain_m: float,
    route_distance_km: float,
    optimal_temp_c: float = 25.0,
    temp_sensitivity: float = 0.01
) -> float:
    """
    Calculate adjusted performance accounting for environmental factors.

    Parameters
    ----------
    base_performance : float
        Base performance metric (range, capacity, etc.)
    ambient_temp_c : float
        Ambient temperature (°C)
    load_kg : float
        Current load (kg)
    max_load_kg : float
        Maximum rated load (kg)
    route_elevation_gain_m : float
        Total elevation gain (m)
    route_distance_km : float
        Route distance (km)
    optimal_temp_c : float
        Optimal operating temperature (°C)
    temp_sensitivity : float
        Performance loss per degree from optimal

    Returns
    -------
    float
        Adjusted performance

    Notes
    -----
    This function combines multiple operational factors to provide realistic
    performance estimates under various conditions.

    Examples
    --------
    >>> # Ideal conditions
    >>> calculate_performance_with_environmental_factors(
    ...     300.0, 25.0, 18000, 36000, 100, 120
    ... )
    # Returns adjusted range
    """
    # Temperature factor
    temp_deviation = abs(ambient_temp_c - optimal_temp_c)
    temp_factor = max(0.5, 1.0 - temp_sensitivity * temp_deviation)

    # Load factor
    load_ratio = load_kg / max_load_kg if max_load_kg > 0 else 1.0
    load_factor = max(0.7, 1.0 - 0.3 * load_ratio)

    # Gradient factor (approximate)
    avg_grade = route_elevation_gain_m / (route_distance_km * 1000) if route_distance_km > 0 else 0.0
    gradient_factor = max(0.7, 1.0 - 10 * avg_grade)

    adjusted_performance = (
        base_performance
        * temp_factor
        * load_factor
        * gradient_factor
    )

    return adjusted_performance


__all__ = [
    "calculate_battery_degradation",
    "calculate_cycle_degradation",
    "calculate_combined_degradation",
    "estimate_remaining_life",
    "calculate_operational_range",
    "calculate_degradation_rate_from_trials",
    "estimate_end_of_life",
    "calculate_performance_with_environmental_factors",
]
