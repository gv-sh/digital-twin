"""
Multi-fuel emissions calculations.

This module provides functions to calculate CO₂, NOₓ, and PM emissions
for different fuel types and technologies.

Extended Emissions Calculation Model based on Paper A methodology for
economic-environmental accounting, extended for multi-fuel fleet analysis.

Equations implemented:
- Total Fleet Emissions: E_total = Σ_f Σ_v Σ_t (FC_f,v,t × EF_f × DF_v,t)
- Technology-Specific Trip Emissions
- Longitudinal Transition Analysis
"""

import numpy as np
from typing import Tuple, Dict, List
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


def calculate_fleet_emissions_with_degradation(
    fuel_consumption: np.ndarray,
    emission_factors: np.ndarray,
    degradation_factors: np.ndarray
) -> float:
    """
    Calculate total fleet emissions accounting for vehicle degradation.

    Extended emissions model:
    E_total = Σ_f Σ_v Σ_t (FC_f,v,t × EF_f × DF_v,t)

    Parameters
    ----------
    fuel_consumption : np.ndarray
        Fuel consumption array with shape (F, V, T) where:
        F = fuel types, V = vehicles, T = time periods
    emission_factors : np.ndarray
        Emission factor for each fuel type (F,)
    degradation_factors : np.ndarray
        Degradation factor for each vehicle at each time (V, T)
        Accounts for performance loss (e.g., 15% battery degradation)

    Returns
    -------
    float
        Total fleet emissions (kg)

    Notes
    -----
    Based on Paper A methodology extended for multi-fuel fleet analysis.
    Accounts for SO₂, NOₓ, TOC, VOC, CO, NH₃, PM10, PM2.5 emissions.

    Examples
    --------
    >>> # 2 fuel types, 3 vehicles, 12 months
    >>> fc = np.random.rand(2, 3, 12) * 1000
    >>> ef = np.array([2.68, 0.65])  # Diesel, Electric
    >>> df = np.ones((3, 12)) * 0.98  # 2% degradation factor
    >>> total = calculate_fleet_emissions_with_degradation(fc, ef, df)
    """
    F, V, T = fuel_consumption.shape

    total_emissions = 0.0
    for f in range(F):
        for v in range(V):
            for t in range(T):
                emissions = (
                    fuel_consumption[f, v, t]
                    * emission_factors[f]
                    * degradation_factors[v, t]
                )
                total_emissions += emissions

    return total_emissions


def calculate_transition_emissions(
    baseline_emissions: float,
    technology_emissions: Dict[str, float],
    adoption_rates: Dict[str, float]
) -> float:
    """
    Calculate emissions during fleet transition to new technologies.

    Longitudinal Transition Analysis:
    E_transition(t) = E_baseline(1 - r_adoption(t)) + Σ_tech E_tech(t)·r_tech(t)

    Parameters
    ----------
    baseline_emissions : float
        Baseline diesel fleet emissions (kg CO2)
    technology_emissions : dict
        Emissions for each technology {tech: emissions}
    adoption_rates : dict
        Adoption rate for each technology {tech: rate}

    Returns
    -------
    float
        Total emissions during transition (kg CO2)

    Examples
    --------
    >>> baseline = 10000.0
    >>> tech_em = {'bev': 2000.0, 'fcet': 3000.0}
    >>> rates = {'bev': 0.4, 'fcet': 0.2}
    >>> calculate_transition_emissions(baseline, tech_em, rates)
    6800.0  # 4000 from remaining diesel + 2800 from new tech
    """
    total_adoption = sum(adoption_rates.values())
    remaining_baseline = baseline_emissions * (1 - total_adoption)

    new_tech_emissions = sum(
        technology_emissions.get(tech, 0.0) * rate
        for tech, rate in adoption_rates.items()
    )

    return remaining_baseline + new_tech_emissions


def calculate_emission_intensity_by_technology(
    distance_km: float,
    fuel_type: FuelType,
    grid_intensity: float = GRID_ELECTRICITY_CO2_PER_KWH,
    consumption_per_km: float = 0.35
) -> Tuple[float, float]:
    """
    Calculate emission intensity per km for different technologies.

    Parameters
    ----------
    distance_km : float
        Distance traveled
    fuel_type : FuelType
        Technology/fuel type
    grid_intensity : float
        Grid carbon intensity (kg CO2/kWh)
    consumption_per_km : float
        Energy/fuel consumption per km (L/km or kWh/km)

    Returns
    -------
    tuple
        (total_emissions_kg, emissions_per_km)

    Examples
    --------
    >>> # BEV: 1 kWh/km, 0.65 kg CO2/kWh grid
    >>> calculate_emission_intensity_by_technology(
    ...     100, FuelType.ELECTRIC, 0.65, 1.0
    ... )
    (65.0, 0.65)
    """
    total_consumption = distance_km * consumption_per_km

    if fuel_type == FuelType.ELECTRIC:
        emissions = total_consumption * grid_intensity
    elif fuel_type == FuelType.DIESEL:
        emissions = total_consumption * DIESEL_CO2_PER_LITER
    elif fuel_type == FuelType.HYDROGEN:
        emissions = total_consumption * GREEN_H2_CO2_PER_KG
    else:
        emissions = 0.0

    intensity = emissions / distance_km if distance_km > 0 else 0.0

    return emissions, intensity


__all__ = [
    "calculate_co2_emissions",
    "calculate_nox_emissions",
    "calculate_pm_emissions",
    "calculate_total_emissions",
    "calculate_emission_reduction",
    "calculate_fleet_emissions_with_degradation",
    "calculate_transition_emissions",
    "calculate_emission_intensity_by_technology",
]
