"""
Multi-fuel emissions calculations.

This module provides functions to calculate CO₂, NOₓ, and PM emissions
for different fuel types and technologies.
"""

from typing import Tuple
from digital_twin.core.constants import (
    DIESEL_CO2_PER_LITER,
    GRID_ELECTRICITY_CO2_PER_KWH,
    GREEN_H2_CO2_PER_KG,
    GREY_H2_CO2_PER_KG,
    DIESEL_NOX_PER_KM,
    DIESEL_PM_PER_KM,
)
from digital_twin.core.types import FuelType


def calculate_co2_emissions(
    fuel_consumed: float,
    fuel_type: FuelType,
    grid_carbon_intensity: float = GRID_ELECTRICITY_CO2_PER_KWH,
    h2_production_method: str = "green"
) -> float:
    """
    Calculate CO₂ emissions based on fuel consumption.

    Parameters
    ----------
    fuel_consumed : float
        Amount of fuel/energy consumed (liters, kWh, or kg)
    fuel_type : FuelType
        Type of fuel
    grid_carbon_intensity : float
        Grid carbon intensity in kg CO₂/kWh
    h2_production_method : str
        Hydrogen production method ("green" or "grey")

    Returns
    -------
    float
        CO₂ emissions in kg
    """
    if fuel_type == FuelType.DIESEL:
        return fuel_consumed * DIESEL_CO2_PER_LITER

    elif fuel_type == FuelType.ELECTRIC:
        return fuel_consumed * grid_carbon_intensity

    elif fuel_type == FuelType.HYDROGEN:
        if h2_production_method == "green":
            return fuel_consumed * GREEN_H2_CO2_PER_KG
        else:
            return fuel_consumed * GREY_H2_CO2_PER_KG

    elif fuel_type in [FuelType.HYBRID_DIESEL_ELECTRIC, FuelType.HYBRID_PETROL_ELECTRIC]:
        # Simplified: assume 50/50 split
        diesel_emissions = (fuel_consumed * 0.5) * DIESEL_CO2_PER_LITER
        electric_emissions = (fuel_consumed * 0.5) * grid_carbon_intensity
        return diesel_emissions + electric_emissions

    else:
        return 0.0


def calculate_nox_emissions(
    distance_km: float,
    fuel_type: FuelType,
    euro_standard: str = "VI"
) -> float:
    """
    Calculate NOₓ emissions.

    Parameters
    ----------
    distance_km : float
        Distance traveled in km
    fuel_type : FuelType
        Type of fuel
    euro_standard : str
        Euro emission standard (for diesel/petrol vehicles)

    Returns
    -------
    float
        NOₓ emissions in grams
    """
    if fuel_type == FuelType.DIESEL:
        return distance_km * DIESEL_NOX_PER_KM

    elif fuel_type in [FuelType.ELECTRIC, FuelType.HYDROGEN]:
        return 0.0  # Zero direct emissions

    elif fuel_type in [FuelType.HYBRID_DIESEL_ELECTRIC, FuelType.HYBRID_PETROL_ELECTRIC]:
        return distance_km * DIESEL_NOX_PER_KM * 0.5  # Reduced by hybrid operation

    else:
        return 0.0


def calculate_pm_emissions(
    distance_km: float,
    fuel_type: FuelType
) -> float:
    """
    Calculate particulate matter (PM) emissions.

    Parameters
    ----------
    distance_km : float
        Distance traveled in km
    fuel_type : FuelType
        Type of fuel

    Returns
    -------
    float
        PM emissions in grams
    """
    if fuel_type == FuelType.DIESEL:
        return distance_km * DIESEL_PM_PER_KM

    elif fuel_type in [FuelType.ELECTRIC, FuelType.HYDROGEN]:
        return 0.0  # Zero direct emissions

    elif fuel_type in [FuelType.HYBRID_DIESEL_ELECTRIC, FuelType.HYBRID_PETROL_ELECTRIC]:
        return distance_km * DIESEL_PM_PER_KM * 0.5

    else:
        return 0.0


def calculate_total_emissions(
    fuel_consumed: float,
    distance_km: float,
    fuel_type: FuelType
) -> Tuple[float, float, float]:
    """
    Calculate total emissions (CO₂, NOₓ, PM).

    Parameters
    ----------
    fuel_consumed : float
        Amount of fuel/energy consumed
    distance_km : float
        Distance traveled in km
    fuel_type : FuelType
        Type of fuel

    Returns
    -------
    tuple
        (CO₂ in kg, NOₓ in g, PM in g)
    """
    co2 = calculate_co2_emissions(fuel_consumed, fuel_type)
    nox = calculate_nox_emissions(distance_km, fuel_type)
    pm = calculate_pm_emissions(distance_km, fuel_type)

    return co2, nox, pm


def calculate_emission_reduction(
    baseline_co2: float,
    new_co2: float
) -> float:
    """
    Calculate emission reduction percentage.

    Parameters
    ----------
    baseline_co2 : float
        Baseline CO₂ emissions in kg
    new_co2 : float
        New technology CO₂ emissions in kg

    Returns
    -------
    float
        Emission reduction percentage
    """
    if baseline_co2 == 0:
        return 0.0

    reduction = ((baseline_co2 - new_co2) / baseline_co2) * 100
    return reduction


__all__ = [
    "calculate_co2_emissions",
    "calculate_nox_emissions",
    "calculate_pm_emissions",
    "calculate_total_emissions",
    "calculate_emission_reduction",
]
