"""
Energy consumption calculations based on physical models.

This module implements physics-based models for calculating vehicle energy
consumption including gravitational, rolling resistance, and aerodynamic components.
"""

import numpy as np
from typing import Union
from digital_twin.core.constants import (
    GRAVITY_ACCELERATION,
    ROLLING_RESISTANCE_COEFF,
    DEFAULT_DRAG_COEFFICIENT,
    DEFAULT_FRONTAL_AREA,
    AIR_DENSITY_SEA_LEVEL,
)


def calculate_wheel_energy(
    mass: float,
    grade: float,
    distance: float,
    velocity: float,
    air_density: float = AIR_DENSITY_SEA_LEVEL,
    frontal_area: float = DEFAULT_FRONTAL_AREA,
    drag_coefficient: float = DEFAULT_DRAG_COEFFICIENT,
    rolling_resistance: float = ROLLING_RESISTANCE_COEFF,
) -> float:
    """
    Calculate energy consumption at the wheel.

    E_wheel = mg·sin(θ)·d + C_rr·mg·d + ½ρ(C_d·A)v²d + E_aux

    Parameters
    ----------
    mass : float
        Vehicle mass in kg
    grade : float
        Road grade (slope angle in radians)
    distance : float
        Distance traveled in meters
    velocity : float
        Vehicle velocity in m/s
    air_density : float
        Air density in kg/m³
    frontal_area : float
        Vehicle frontal area in m²
    drag_coefficient : float
        Aerodynamic drag coefficient
    rolling_resistance : float
        Rolling resistance coefficient

    Returns
    -------
    float
        Energy consumption in Joules
    """
    # Gravitational potential energy (climbing work)
    E_gravity = mass * GRAVITY_ACCELERATION * np.sin(grade) * distance

    # Rolling resistance energy
    E_rolling = rolling_resistance * mass * GRAVITY_ACCELERATION * distance

    # Aerodynamic drag energy
    E_aero = (
        0.5 * drag_coefficient * air_density * frontal_area *
        (velocity ** 2) * distance
    )

    # Total energy at wheel
    E_wheel = E_gravity + E_rolling + E_aero

    return E_wheel


def calculate_energy_with_efficiency(
    wheel_energy: float,
    powertrain_efficiency: float,
    auxiliary_power: float = 0.0,
    time_hours: float = 1.0
) -> float:
    """
    Calculate total energy consumption including efficiency losses.

    Parameters
    ----------
    wheel_energy : float
        Energy at wheel in Joules
    powertrain_efficiency : float
        Powertrain efficiency (0-1)
    auxiliary_power : float
        Auxiliary power draw in Watts (HVAC, etc.)
    time_hours : float
        Operating time in hours

    Returns
    -------
    float
        Total energy consumption in Joules
    """
    # Account for powertrain efficiency
    total_energy = wheel_energy / powertrain_efficiency

    # Add auxiliary energy
    auxiliary_energy = auxiliary_power * time_hours * 3600  # Convert to Joules

    return total_energy + auxiliary_energy


def calculate_regenerative_braking_energy(
    mass: float,
    initial_velocity: float,
    final_velocity: float,
    regen_efficiency: float = 0.70
) -> float:
    """
    Calculate energy recovered from regenerative braking.

    Parameters
    ----------
    mass : float
        Vehicle mass in kg
    initial_velocity : float
        Initial velocity in m/s
    final_velocity : float
        Final velocity in m/s
    regen_efficiency : float
        Regenerative braking efficiency (0-1)

    Returns
    -------
    float
        Energy recovered in Joules
    """
    # Kinetic energy change
    delta_ke = 0.5 * mass * (initial_velocity**2 - final_velocity**2)

    # Energy recovered (accounting for efficiency)
    energy_recovered = delta_ke * regen_efficiency

    return max(0, energy_recovered)


def calculate_specific_energy_consumption(
    total_energy_joules: float,
    distance_km: float,
    mass_kg: float
) -> float:
    """
    Calculate specific energy consumption (energy per unit distance per unit mass).

    Parameters
    ----------
    total_energy_joules : float
        Total energy consumed in Joules
    distance_km : float
        Distance traveled in km
    mass_kg : float
        Vehicle mass in kg

    Returns
    -------
    float
        Specific energy consumption in kWh/100km/tonne
    """
    # Convert to kWh
    energy_kwh = total_energy_joules / 3_600_000

    # Convert mass to tonnes
    mass_tonnes = mass_kg / 1000

    # Calculate per 100 km per tonne
    specific_consumption = (energy_kwh / distance_km * 100) / mass_tonnes

    return specific_consumption


__all__ = [
    "calculate_wheel_energy",
    "calculate_energy_with_efficiency",
    "calculate_regenerative_braking_energy",
    "calculate_specific_energy_consumption",
]
