"""
Thermodynamics and temperature effects.

This module provides functions for modeling temperature effects on
battery performance, HVAC loads, and component efficiency.
"""

import numpy as np


def calculate_battery_temperature_factor(
    ambient_temp_celsius: float,
    optimal_temp: float = 25.0
) -> float:
    """
    Calculate battery performance factor based on temperature.

    Performance degrades at low and high temperatures.

    Parameters
    ----------
    ambient_temp_celsius : float
        Ambient temperature in Celsius
    optimal_temp : float
        Optimal operating temperature

    Returns
    -------
    float
        Performance factor (1.0 = optimal, <1.0 = reduced)
    """
    # Simple model: performance drops 1% per degree from optimal
    temp_diff = abs(ambient_temp_celsius - optimal_temp)
    factor = 1.0 - (temp_diff * 0.01)

    # Limit between 0.5 and 1.0
    return max(0.5, min(1.0, factor))


def calculate_hvac_load(
    cabin_volume_m3: float,
    ambient_temp_celsius: float,
    target_temp_celsius: float = 22.0,
    insulation_factor: float = 1.0
) -> float:
    """
    Calculate HVAC power requirement.

    Parameters
    ----------
    cabin_volume_m3 : float
        Cabin volume in cubic meters
    ambient_temp_celsius : float
        Ambient temperature
    target_temp_celsius : float
        Target cabin temperature
    insulation_factor : float
        Insulation quality (1.0 = standard, <1.0 = better)

    Returns
    -------
    float
        HVAC power in Watts
    """
    # Temperature difference
    temp_diff = abs(ambient_temp_celsius - target_temp_celsius)

    # Simplified model: ~100W per m³ per 10°C difference
    power = cabin_volume_m3 * (temp_diff / 10.0) * 100 * insulation_factor

    return power


def calculate_air_density_correction(
    altitude_m: float,
    temp_celsius: float = 15.0
) -> float:
    """
    Calculate air density correction for altitude and temperature.

    Parameters
    ----------
    altitude_m : float
        Altitude in meters
    temp_celsius : float
        Temperature in Celsius

    Returns
    -------
    float
        Air density in kg/m³
    """
    # Standard atmospheric model
    # ρ = ρ₀ × (1 - 0.0065h/T₀)^(g/(R×0.0065))

    T0 = 288.15  # Sea level standard temperature (K)
    rho0 = 1.225  # Sea level air density (kg/m³)
    g = 9.81
    R = 287.05  # Specific gas constant for dry air

    temp_kelvin = temp_celsius + 273.15

    # Simplified formula
    rho = rho0 * (1 - (0.0065 * altitude_m) / T0) ** 4.256

    # Temperature correction
    rho = rho * (T0 / temp_kelvin)

    return rho


__all__ = [
    "calculate_battery_temperature_factor",
    "calculate_hvac_load",
    "calculate_air_density_correction",
]
